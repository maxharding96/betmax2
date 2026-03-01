import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLMResultsWrapper
from scipy.stats import nbinom
import pandas as pd
import numpy as np
from schemas import PredictionField
from schema import BuildModelRow, PredictRow


DECAY_RATE = -0.0065


class PlayerStatModel:
    _models: dict[PredictionField, GLMResultsWrapper]

    def __init__(self, decay_rate: float = DECAY_RATE):
        self._models = {}
        self._decay_rate = decay_rate

    def build_model(self, field: PredictionField, data: list[BuildModelRow]) -> None:
        df = pd.DataFrame([row.model_dump() for row in data])
        df = self._calculate_weight_col(df)

        model = smf.glm(
            formula="stat ~ C(player_id) + C(opponent_id) + is_home + started",
            data=df,
            family=sm.families.NegativeBinomial(),
            var_weights=df["weight"],
            offset=np.log(df["min"] / 90),
        ).fit()

        self._models[field] = model

    def predict_probabilities(
        self, field: PredictionField, data: list[PredictRow], gte: int
    ) -> np.ndarray:
        lambdas = self._predict(field, data)
        model = self._get_model(field)

        alpha = model.scale
        n = 1 / alpha
        p = n / (n + lambdas)

        return nbinom.sf(gte - 1, n=n, p=p)

    def _predict(self, field: PredictionField, data: list[PredictRow]) -> pd.Series:
        model = self._get_model(field)
        df = pd.DataFrame([row.model_dump() for row in data])
        return model.predict(df, offset=np.log(df["avg_minutes"] / 90))

    def _get_model(self, field: PredictionField) -> GLMResultsWrapper:
        model = self._models.get(field)
        if model is None:
            raise ValueError(
                f"No model built for field '{field}'. Call build_model() first."
            )
        return model

    def _calculate_weight_col(self, df: pd.DataFrame) -> pd.DataFrame:
        reference_date = df["date"].max()
        days_ago = (reference_date - df["date"]).dt.days
        return df.assign(weight=np.exp(self._decay_rate * days_ago))
