from redis_client import RedisClient
from scraper import Scraper
from .cache import OddsCache
from .client import OddsChecker
from schemas import League, Match, Field


class OddsService:
    def __init__(self, redis: RedisClient, scraper: Scraper):
        self._cache = OddsCache(redis)
        self._client = OddsChecker(scraper)

    async def get_matches(self, league: League):
        matches = self._cache.get_matches(league)

        if not matches:
            all_matches = await self._client.get_matches(league)

            # only return one game per team
            teams = set()
            matches = []
            for match in all_matches:
                if match.home_team not in teams and match.away_team not in teams:
                    teams.add(match.home_team)
                    teams.add(match.away_team)
                    matches.append(match)

            self._cache.set_matches(matches)

        return matches

    async def get_odds(self, match: Match, field: Field, over: float):
        match_odds = self._cache.get_match_odds(match)

        if match_odds is None:
            match_odds = await self._client.get_odds(match, [Field.SH, Field.SOT])
            if match_odds is None:
                return

            self._cache.set_match_odds(match_odds)

        try:
            field_odds = match_odds.field_to_odds[field]
        except KeyError:
            # Too early to retrive match odds
            return

        return [odds for odds in field_odds if odds.point == over]
