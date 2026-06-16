import json
import redis
from decouple import config

REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0')

def get_redis():
    try:
        client = redis.from_url(REDIS_URL,decode_responses=True)
        client.ping()
        return client
    except Exception:
        return None

def cache_get(key: str):
    client = get_redis()
    if not client:
        return None
    try:
        data = client.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None

def cache_set(key: str, value, ttl: int= 300):
    client = get_redis()
    if not client:
        return
    try:
        client.setex(key, ttl, json.dumps(value,default=str))
    except Exception:
        return

def cache_delete_pattern(pattern: str):
    client = get_redis()
    if not client:
        return
    try:
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
    except Exception:
        return
