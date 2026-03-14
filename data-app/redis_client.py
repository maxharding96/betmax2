import redis


class RedisClient:
    def __init__(self, host="localhost", port=6379):
        self._r = redis.Redis(host=host, port=port, decode_responses=True)

    def get(self, key: str) -> str | None:
        return self._r.get(key)

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        self._r.setex(key, ttl_seconds, value)

    def delete(self, key: str) -> None:
        self._r.delete(key)
