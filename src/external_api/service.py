import httpx
import asyncio
import requests
from src.cache.service import cache_get, cache_set
from src.external_api.models import CatFactModel, CatImageModel, CatCombinedModel
from src.settings import settings


class CatService:
    """Services to get image and fact about cat"""

    fact_url: str = "https://catfact.ninja/fact"
    image_url: str = "https://api.thecatapi.com/v1/images/search"

    def get_cat_fact(self) -> CatFactModel:
        """
        Fetch a random cat fact from catfact.ninja API.
        :return: CatFactModel with fact text and its length.
        """
        cache_key = "cache:external:cat_fact"

        # get from cache
        cached = asyncio.run(cache_get(cache_key))
        if cached:
            return CatFactModel(**cached)

        # fetch from API
        response = requests.get(self.fact_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # save to cache
        asyncio.run(cache_set(cache_key, data, settings.redis_TTL))

        return CatFactModel(**data)

    def get_cat_image(self) -> CatImageModel:
        """
        Fetch a random cat image from thecatapi.com API.
        :return: CatImageModel with image URL.
        """
        cache_key = "cache:external:cat_image"

        # get from cache
        cached = asyncio.run(cache_get(cache_key))
        if cached:
            return CatImageModel(**cached)

        # fetch from API
        response = requests.get(self.image_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # save to cache
        asyncio.run(cache_set(cache_key, data, settings.redis_TTL))

        return CatImageModel(url=data[0]["url"])
    def get_cat_info(self) -> CatCombinedModel:
        """
        Combine cat fact and image into a single model.
        :return: CatCombinedModel containing fact and image URL.
        """
        fact: CatFactModel = self.get_cat_fact()
        image: CatImageModel = self.get_cat_image()
        return CatCombinedModel(fact=fact.fact, image_url=image.url)


service = CatService()
