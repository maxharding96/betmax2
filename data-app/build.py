from fbref import FBRef
from scraper import Scraper
from schemas import League, Season
import nodriver as uc
from services.fbref import create_fbref_match
from crud.match import count_season_matches
from database import get_session


async def main():
    scraper_client = await Scraper.start()
    fbref_client = FBRef(scraper=scraper_client)

    league = League.CHAMPIONSHIP
    season = Season.S_25

    with get_session() as session:
        match_count = count_season_matches(session, season)

    # process_count = 100
    # end_index = match_count + process_count
    end_index = -1

    print(f"Found {match_count} stored for the {season} season.")

    async for match in fbref_client.get_played_matches(
        league, season, start_index=match_count, end_index=end_index
    ):
        with get_session() as session:
            create_fbref_match(session, match)

    scraper_client.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
