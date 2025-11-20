import asyncio
import requests
import logging
import sentry_sdk

from src.cache.service import cache_get, cache_set
from src.external_api.models import CatFactModel, CatImageModel, CatCombinedModel
from src.settings import settings

logger = logging.getLogger(__name__)


class CatService:
    """Services to get image and fact about cat"""

    fact_url: str = "https://catfact.ninja/fact"
    image_url: str = "https://api.thecatapi.com/v1/images/search"

    def get_cat_fact(self) -> CatFactModel:
        logger.info("[EXTERNAL][FACT] Fetching cat fact")

        cache_key = "cache:external:cat_fact"

        try:
            cached = asyncio.run(cache_get(cache_key))
            if cached:
                logger.info("[EXTERNAL][FACT] Cache HIT")
                return CatFactModel(**cached)
            logger.info("[EXTERNAL][FACT] Cache MISS")
        except Exception as e:
            logger.error(f"[EXTERNAL][FACT] Cache error: {e}")
            sentry_sdk.capture_exception(e)

        try:
            response = requests.get(self.fact_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info("[EXTERNAL][FACT] API success")

            try:
                asyncio.run(cache_set(cache_key, data, settings.redis_TTL))
                logger.info("[EXTERNAL][FACT] Cached fact OK")
            except Exception as e:
                logger.error(f"[EXTERNAL][FACT] Cache save error: {e}")
                sentry_sdk.capture_exception(e)

            return CatFactModel(**data)

        except Exception as e:
            logger.exception("[EXTERNAL][FACT] API error")
            sentry_sdk.capture_exception(e)
            raise

    def get_cat_image(self) -> CatImageModel:
        logger.info("[EXTERNAL][IMAGE] Fetching cat image")

        cache_key = "cache:external:cat_image"

        try:
            cached = asyncio.run(cache_get(cache_key))
            if cached:
                logger.info("[EXTERNAL][IMAGE] Cache HIT")
                return CatImageModel(**cached)
            logger.info("[EXTERNAL][IMAGE] Cache MISS")
        except Exception as e:
            logger.error(f"[EXTERNAL][IMAGE] Cache error: {e}")
            sentry_sdk.capture_exception(e)

        try:
            response = requests.get(self.image_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info("[EXTERNAL][IMAGE] API success")

            try:
                asyncio.run(cache_set(cache_key, data, settings.redis_TTL))
                logger.info("[EXTERNAL][IMAGE] Cached image OK")
            except Exception as e:
                logger.error(f"[EXTERNAL][IMAGE] Cache save error: {e}")
                sentry_sdk.capture_exception(e)

            return CatImageModel(url=data[0]["url"])

        except Exception as e:
            logger.exception("[EXTERNAL][IMAGE] API error")
            sentry_sdk.capture_exception(e)
            raise

    def get_cat_info(self) -> CatCombinedModel:
        logger.info("[EXTERNAL][CAT] Fetching combined info")

        try:
            fact = self.get_cat_fact()
            image = self.get_cat_image()
            logger.info("[EXTERNAL][CAT] Combined info success")
            return CatCombinedModel(fact=fact.fact, image_url=image.url)
        except Exception as e:
            logger.exception("[EXTERNAL][CAT] Combined info error")
            sentry_sdk.capture_exception(e)
            raise


service = CatService()
