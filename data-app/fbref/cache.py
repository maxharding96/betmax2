from pydantic import TypeAdapter
from redis_client import RedisClient
from .schema import Match

A_WEEK = 7 * 24 * 60

adapter = TypeAdapter(list[Match])


class FBRefCache:
    _prefix = "fbref"

    def __init__(self, redis: RedisClient, ttl_minutes: int = A_WEEK):
        self._redis = redis
        self._ttl = ttl_minutes * 60

    def _date_matches_key(self, date: str) -> str:
        return f"{self._prefix}:{date}"

    def get_date_matches(self, date: str) -> list[Match] | None:
        raw = self._redis.get(self._date_matches_key(date))
        if raw is None:
            return None

        matches = adapter.validate_json(raw)

        return matches

    def set_date_matches(self, matches: list[Match]) -> None:
        match = matches[0]
        key = self._date_matches_key(match.date)

        self._redis.set(key, adapter.dump_json(matches), self._ttl)
