from fbref import FBRef
from scraper import Scraper
from schemas import League, Season
import nodriver as uc
from crud.fbref import create_fbref_match
from database import get_session


async def main():
    scraper_client = await Scraper.start()
    fbref_client = FBRef(scraper=scraper_client)

    async for match in fbref_client.get_matches(League.PREMIER_LEAGUE, Season.S_25):
        with get_session() as session:
            create_fbref_match(session, match)

        break

    scraper_client.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
