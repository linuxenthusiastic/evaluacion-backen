import json
import redis
from decouple import config
from cache.base import BaseCache

REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0')


class RedisCache(BaseCache):
    """Implementación concreta de caché usando Redis."""

    def _get_client(self):
        try:
            client = redis.from_url(REDIS_URL, decode_responses=True)
            client.ping()
            return client
        except Exception:
            return None

    def get(self, key: str):
        client = self._get_client()
        if not client:
            return None
        try:
            data = client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

    def set(self, key: str, value, ttl: int = 300):
        client = self._get_client()
        if not client:
            return
        try:
            client.setex(key, ttl, json.dumps(value, default=str))
        except Exception:
            return

    def delete_pattern(self, pattern: str):
        client = self._get_client()
        if not client:
            return
        try:
            keys = client.keys(pattern)
            if keys:
                client.delete(*keys)
        except Exception:
            return
