from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import Season
from data import DataService
from fbref import FBRefCache
from scraper import Scraper
from odds import OddsService
from redis_client import RedisClient
import io_schema as io


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


redis = RedisClient()
scraper = Scraper()

data_service = DataService()
odds_service = OddsService(redis=redis, scraper=scraper)
fbref_cache = FBRefCache(redis)


@app.post("/get-matches")
async def get_matches(input: io.GetMatchesInput):
    matches = await odds_service.get_matches(input.league)
    scraper.stop()

    output = io.GetMatchesOutput(matches=matches)
    return output.model_dump()


@app.post("/get-rows")
async def get_rows(input: io.GetRowsInput):
    matches = await odds_service.get_matches(input.league)
    home_team_to_match = {match.home_team: match for match in matches}

    players_in_model = data_service.build_model(input.league, input.field)

    all_rows = []
    for home_team in input.home_teams:
        match = home_team_to_match[home_team]

        match_odds = await odds_service.get_odds(match, input.field, input.over)
        if not match_odds:
            continue

        rows = data_service.make_prediction(
            match, players_in_model, input.field, input.over, match_odds
        )

        all_rows.extend(rows)

    scraper.stop()

    output = io.GetRowsOutput(rows=all_rows)
    return output.model_dump()
