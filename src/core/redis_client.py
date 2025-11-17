from redis import asyncio as aioredis
from src.settings import settings


def get_redis() -> aioredis.Redis:
    return aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
