from fastapi import APIRouter, HTTPException
from src.cache.models import CacheItem
from src.cache.service import cache_set, cache_get
import logging
import sentry_sdk

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cache", tags=["cache"])


@router.post("/set")
async def set_cache(item: CacheItem):
    try:
        logger.info(f"[CACHE][SET] Set cache item: {item.key}")
        logger.debug(f"payload={item.model_dump_json()}")

        await cache_set(item.key, item.value, ttl=item.ttl)

        logger.info("[CACHE][SET] cache stored OK")

        return {"status": "saved", "key": item.key}
    except Exception as e:
        logger.error(f"[CACHE][SET] error: {e}")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=f"Cache set error")

@router.get("/get/{key}")
async def get_cache(key: str):
    try:
        logger.info(f"[CACHE][GET] get cache item with key: {key}")
        value = await cache_get(key)

        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")

        logger.info("[CACHE][GET] get cache OK")
        return {"key": key, "value": value}
    except Exception as e:
        logger.error(f"[CACHE][GET] error: {e}")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail=f"Cache get error")
