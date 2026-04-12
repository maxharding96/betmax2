from fbref import FBRef
from scraper import Scraper
from schemas import League, Season
import nodriver as uc
from data import DataService
from crud.match import count_season_matches
from database import get_session


data_service = DataService()
scraper = Scraper()


async def main():
    fbref_client = FBRef(scraper=scraper)

    league = League.PREMIER_LEAGUE
    season = Season.S_25

    with get_session() as session:
        match_count = count_season_matches(session, season, league)

    # process_count = 100
    # end_index = match_count + process_count
    end_index = -1

    print(f"Found {match_count} stored for the {season} season.")

    async for match in fbref_client.get_played_matches(
        league, season, start_index=match_count, end_index=end_index
    ):
        with get_session() as session:
            data_service.create_fbref_match(session, match)

    scraper.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
