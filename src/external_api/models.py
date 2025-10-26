from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from src.external_api.config import cat_config as cfg


class CatFactModel(BaseModel):
    fact: str = Field(
        ...,
        description="Random cat fact text",
        min_length=cfg.min_fact_length,
        max_length=cfg.max_fact_length,
    )
    length: int = Field(
        ...,
        description="Length of the fact text",
        ge=cfg.min_length_value,
        le=cfg.max_length_value,
    )

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CatImageModel(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="URL of the cat image",
        min_length=cfg.min_url_length,
        max_length=cfg.max_url_length,
    )

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CatCombinedModel(BaseModel):
    fact: str = Field(
        ...,
        description="Random cat fact text",
        min_length=cfg.min_fact_length,
        max_length=cfg.max_fact_length,
    )
    image_url: HttpUrl = Field(
        ...,
        description="URL of the cat image",
        min_length=cfg.min_url_length,
        max_length=cfg.max_url_length,
    )

    model_config: ConfigDict = ConfigDict(from_attributes=True)
