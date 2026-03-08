from fbref import FBRef
from scraper import Scraper
from stats import PlayerStatModel
from stats.schema import PredictRow
from services.stats import build_model_rows, build_predict_rows
from schemas import League, PredictionField, Season
from database import get_session
import nodriver as uc


player_stat_model = PlayerStatModel()


async def main():
    scraper_client = await Scraper.start()
    fbref_client = FBRef(scraper=scraper_client)
    league = League.PREMIER_LEAGUE
    season = Season.S_25
    field = PredictionField.SOT

    date = "2026-03-14"

    matches = await fbref_client.get_date_matches(league, season, date)

    with get_session() as session:
        rows = build_model_rows(session, league, field)

    players_in_model = set()
    for row in rows:
        players_in_model.add(row.player_id)

    player_stat_model.build_model(field, rows)

    predict_rows: list[PredictRow] = []

    with get_session() as session:
        for match in matches:
            rows = [
                row
                for row in build_predict_rows(session, match)
                if row.player_id in players_in_model
            ]
            predict_rows.extend(rows)
            break

    predictions = player_stat_model.predict_probabilities(field, predict_rows, gte=1)

    for row, prediction in zip(predict_rows, predictions):
        print(row.player_id, prediction)

    print(predictions)


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
