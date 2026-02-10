from fbref import FBRef
from scraper import Scraper
from schemas import League, Season
import nodriver as uc


async def main():
    scraper_client = await Scraper.start()
    fbref_client = FBRef(scraper=scraper_client)

    async for match_report in fbref_client.get_match_reports(
        League.PREMIER_LEAGUE, Season.S_25
    ):
        pass

    scraper_client.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
