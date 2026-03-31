from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import Field, Season
from stats import PlayerStatModel
from services.stats import build_model_rows, build_predict_rows
from fbref import FBRefCache
from database import get_session
from scraper import Scraper
from odds import OddsChecker, OddsCache
from redis_client import RedisClient
import difflib
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


player_stat_model = PlayerStatModel()

redis = RedisClient()
odds_cache = OddsCache(redis)
fbref_cache = FBRefCache(redis)


@app.post("/get-matches")
async def get_matches(input: io.GetMatchesInput):
    league = input.league

    matches = odds_cache.get_matches(league)

    if not matches:
        scrpr = await Scraper.start()
        oddschecker = OddsChecker(scrpr)

        matches = await oddschecker.get_matches(league)
        odds_cache.set_matches(matches)

        scrpr.stop()

    output = io.GetMatchesOutput(matches=matches)
    return output.model_dump()


@app.post("/get-rows")
async def get_rows(input: io.GetRowsInput):
    match = input.match
    field = input.field
    over = input.over

    # build model
    with get_session() as session:
        rows = build_model_rows(session, match.league, field)

    players_in_model = set()
    for row in rows:
        players_in_model.add(row.player_id)

    player_stat_model.build_model(match.league, field, rows)

    # get the odds
    match_odds = odds_cache.get_match_odds(match)

    if match_odds is None:
        scrpr = await Scraper.start()
        oddschecker = OddsChecker(scrpr)

        match_odds = await oddschecker.get_odds(match, [Field.SH, Field.SOT])
        if match_odds is None:
            raise HTTPException(404, "Unable to retrieve match odds.")

        odds_cache.set_match_odds(match_odds)

        scrpr.stop()

    try:
        field_odds = match_odds.field_to_odds[field]
    except KeyError:
        # Too early to retrive match odds
        output = io.GetRowsOutput(rows=[])
        return output.model_dump()

    player_to_odds = {odds.player: odds for odds in field_odds if odds.point == over}
    players = list(player_to_odds.keys())

    # get the predicitons
    with get_session() as session:
        predict_rows = [
            row
            for row in build_predict_rows(session, match)
            if row.player_id in players_in_model
        ]

    predictions = player_stat_model.predict_probabilities(
        match.league, field, predict_rows, over
    )

    rows = []

    for row, prediction in zip(predict_rows, predictions):
        player_match = find_most_similar_name(row.player_name, players)

        if player_match is None:
            continue

        row = io.Row(
            player=row.player_name,
            team=row.team,
            opponent=row.opponent,
            venue="home" if row.is_home else "away",
            odds=player_to_odds[player_match].value,
            prediction=prediction,
        )

        rows.append(row)

    output = io.GetRowsOutput(rows=rows)
    return output.model_dump()


def find_most_similar_name(target_name, name_list) -> str | None:
    """
    Finds the closest match to target_name within name_list.
    Returns None if the list is empty.
    """
    # get_close_matches returns a list of matches ranked by similarity
    # n=1 ensures we only get the single best match
    # cutoff=0.0 ensures we get the best match even if it's not very similar
    matches = difflib.get_close_matches(target_name, name_list, n=1, cutoff=0.0)

    return matches[0] if matches else None
