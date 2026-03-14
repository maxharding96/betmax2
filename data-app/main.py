from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from schemas import League, Field, Season
from stats import PlayerStatModel
from stats.schema import PredictRow
from services.stats import build_model_rows, build_predict_rows
from fbref import FBRef
from database import get_session
from scraper import Scraper
from odds import OddsChecker, OddsCache
from redis_client import RedisClient


CURRENT_SEASON = Season.S_25

origins = [
    "http://localhost:5173",  # Your frontend dev server
    "http://127.0.0.1:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


class PredictInput(BaseModel):
    field: Field
    over: int
    league: League
    date: str


class Prediction(BaseModel):
    player: str
    prediction: float


class PredictOutput(BaseModel):
    predictions: list[Prediction]


player_stat_model = PlayerStatModel()

redis = RedisClient()
odds_cache = OddsCache(redis)


@app.post("/predict")
async def predict(input: PredictInput):
    field = input.field
    over = input.over
    league = input.league
    date = input.date

    scrpr = await Scraper.start()

    fbref_client = FBRef(scrpr)
    oddschecker = OddsChecker(scrpr)

    matches = await fbref_client.get_date_matches(league, CURRENT_SEASON, date)

    for match in matches:
        match_odds = odds_cache.get_match_odds(match)
        if match_odds is None:
            match_odds = await oddschecker.get_odds(match, [Field.SH, Field.SOT])
            odds_cache.set_match_odds(match_odds)

        return match_odds.model_dump()

    # with get_session() as session:
    #     rows = build_model_rows(session, league, field)

    # players_in_model = set()
    # for row in rows:
    #     players_in_model.add(row.player_id)

    # player_stat_model.build_model(league, field, rows)

    # predict_rows: list[PredictRow] = []

    # with get_session() as session:
    #     for match in matches:
    #         rows = [
    #             row
    #             for row in build_predict_rows(session, match)
    #             if row.player_id in players_in_model
    #         ]
    #         predict_rows.extend(rows)
    #         break

    # predictions = player_stat_model.predict_probabilities(
    #     league, field, predict_rows, over
    # )

    # player_prediction = [
    #     Prediction(player=row.player_name, prediction=prediction)
    #     for row, prediction in zip(predict_rows, predictions)
    # ]

    # output = PredictOutput(predictions=player_prediction)

    # return output.model_dump()
