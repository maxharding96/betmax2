import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLMResultsWrapper
from scipy.stats import nbinom
import pandas as pd
import numpy as np
from schemas import League, PredictionField
from .schema import BuildModelRow, PredictRow


DECAY_RATE = -0.0065

ModelKey = tuple[League, PredictionField]


class PlayerStatModel:
    _models: dict[ModelKey, GLMResultsWrapper]

    def __init__(self, decay_rate: float = DECAY_RATE):
        self._models = {}
        self._decay_rate = decay_rate

    def build_model(
        self, league: League, field: PredictionField, data: list[BuildModelRow]
    ) -> None:
        df = pd.DataFrame([row.model_dump() for row in data])
        df = self._calculate_weight_col(df)

        league_mean = 0.3319  # Or pull from your DB results
        league_disp = 1.2606
        calculated_alpha = (league_disp - 1) / league_mean

        offset = np.log(df["min"] / 90)

        model = smf.glm(
            formula="stat ~ C(player_id) + C(opponent_id) + is_home + started",
            data=df,
            family=sm.families.NegativeBinomial(alpha=calculated_alpha),
            var_weights=df["weight"],
            offset=offset,
        ).fit()

        self._models[league, field] = model

    def predict_probabilities(
        self, league: League, field: PredictionField, data: list[PredictRow], over: int
    ) -> np.ndarray:
        lambdas = self._predict(league, field, data)
        model = self._get_model(league, field)

        alpha = model.family.alpha
        n = 1 / alpha
        p = n / (n + lambdas)

        return nbinom.sf(over, n=n, p=p)

    def _predict(
        self, league: League, field: PredictionField, data: list[PredictRow]
    ) -> pd.Series:
        model = self._get_model(league, field)
        df = pd.DataFrame([row.model_dump() for row in data])
        return model.predict(df, offset=np.log(df["avg_minutes"] / 90))

    def _get_model(self, league: League, field: PredictionField) -> GLMResultsWrapper:
        model = self._models.get((league, field))
        if model is None:
            raise ValueError(
                f"No model built for league '{league}' & field '{field}'. Call build_model() first."
            )
        return model

    def _calculate_weight_col(self, df: pd.DataFrame) -> pd.DataFrame:
        reference_date = df["date"].max()
        days_ago = (reference_date - df["date"]).dt.days
        return df.assign(weight=np.exp(self._decay_rate * days_ago))
