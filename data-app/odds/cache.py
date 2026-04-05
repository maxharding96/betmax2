from pydantic import TypeAdapter
from redis_client import RedisClient
from .schema import MatchOdds
from schemas import Match, League

adapter = TypeAdapter(list[Match])


class OddsCache:
    _prefix = "odds"

    def __init__(self, redis: RedisClient):
        self._redis = redis

    def _matches_key(self, league: League) -> str:
        return f"{self._prefix}:{league}"

    def _match_odds_key(self, match: Match) -> str:
        return f"{self._prefix}:{match.home_team}:{match.away_team}"

    def get_matches(self, league: League) -> list[Match]:
        raw = self._redis.get(self._matches_key(league))
        if raw is None:
            return None

        matches = adapter.validate_json(raw)
        return matches

    def set_matches(self, matches: list[Match]):
        match = matches[0]
        key = self._matches_key(match.league)

        ttl = 60 * 60 * 6  # 6 hours
        self._redis.set(key, adapter.dump_json(matches), ttl)

    def get_match_odds(self, match: Match) -> MatchOdds | None:
        key = self._match_odds_key(match)
        raw = self._redis.get(key)
        if raw is None:
            return None
        return MatchOdds.model_validate_json(raw)

    def set_match_odds(self, match_odds: MatchOdds) -> None:
        raw = match_odds.model_dump_json()

        ttl = 60 * 60  # 1 hour
        self._redis.set(self._match_odds_key(match_odds.match), raw, ttl)
