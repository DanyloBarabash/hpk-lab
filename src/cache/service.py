import json
from src.core.redis_client import get_redis


async def cache_set(key: str, value, ttl: int | None = None):
    redis = get_redis()
    await redis.set(key, json.dumps(value), ex=ttl)


async def cache_get(key: str):
    redis = get_redis()
    data = await redis.get(key)
    return json.loads(data) if data else None
