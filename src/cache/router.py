from fastapi import APIRouter, HTTPException
from src.cache.models import CacheItem
from src.cache.service import cache_set, cache_get

router = APIRouter(prefix="/cache", tags=["cache"])


@router.post("/set")
async def set_cache(item: CacheItem):
    await cache_set(item.key, item.value, ttl=item.ttl)
    return {"status": "saved", "key": item.key}


@router.get("/get/{key}")
async def get_cache(key: str):
    value = await cache_get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"key": key, "value": value}
