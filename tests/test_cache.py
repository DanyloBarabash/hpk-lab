import asyncio

import pytest

from src.cache.service import cache_get, cache_set


@pytest.mark.asyncio
async def test_cache_set_and_get(fake_redis):
    key = "test:key"
    value = {"x": 1}

    await cache_set(key, value, ttl=5)
    result = await cache_get(key)

    assert result["x"] == 1


@pytest.mark.asyncio
async def test_cache_get_missing_key(fake_redis):
    key = "missing:key"

    result = await cache_get(key)

    assert result is None


@pytest.mark.asyncio
async def test_cache_overwrite_existing_key(fake_redis):
    key = "test:overwrite"

    await cache_set(key, {"x": 1}, ttl=5)
    await cache_set(key, {"x": 2}, ttl=5)

    result = await cache_get(key)

    assert result["x"] == 2


@pytest.mark.asyncio
async def test_cache_ttl_expiration(fake_redis):
    key = "test:ttl"
    value = {"x": 1}

    await cache_set(key, value, ttl=1)
    await asyncio.sleep(1.1)

    result = await cache_get(key)

    assert result is None
