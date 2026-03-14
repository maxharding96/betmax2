from redis_client import RedisClient
from .schema import MatchOdds
from fbref.schema import Match


class OddsCache:
    _prefix = "odds"

    def __init__(self, redis: RedisClient, ttl_minutes: int = 60):
        self._redis = redis
        self._ttl = ttl_minutes * 60

    def _match_key(self, match: Match) -> str:
        return f"{self._prefix}:{match.home_team}:{match.away_team}"

    def get_match_odds(self, match: Match) -> MatchOdds | None:
        raw = self._redis.get(self._match_key(match))
        if raw is None:
            return None
        return MatchOdds.model_validate_json(raw)

    def set_match_odds(self, match_odds: MatchOdds) -> None:
        raw = match_odds.model_dump_json()
        self._redis.set(self._match_key(match_odds.match), raw, self._ttl)
