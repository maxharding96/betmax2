from odds import OddsChecker, OddsCache
from odds.schema import 
import nodriver as uc
from schemas import League, Field
from scraper import Scraper

odds_cache = OddsCache()


async def main():
    scraper = await Scraper.start()
    oc = OddsChecker(scraper=scraper)

    league = League.PREMIER_LEAGUE
    fields = [Field.SOT, Field.SH]

    odds = odds_redis.get(league)

    if odds is None:
        output = await oc.get_matches(League.PREMIER_LEAGUE)

        odds: list[GetOddsOutput] = []

        for match in output.matches:
            odds_output = await oc.get_odds(match, fields)
            if odds_output:
                odds.append(odds_output)

            break

        print(odds)

        odds_redis.set(league, odds)

    print(odds)

    scraper.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
