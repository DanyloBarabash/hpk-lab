from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

from src.database.base_schema import BaseOutModel
from src.cat_facts.config import cat_fact_config as cfg


class CatFactCreate(BaseModel):
    """DTO for creating a new local cat fact."""

    text: str = Field(
        ...,
        description="Fact text",
        min_length=cfg.min_text_length,
        max_length=cfg.max_text_length,
    )

    image_url: Optional[HttpUrl] = Field(
        None,
        description="Optional image URL",
        min_length=cfg.min_image_url_length,
        max_length=cfg.max_image_url_length,
    )


class CatFactUpdate(BaseModel):
    """DTO for partially updating a cat fact."""

    text: Optional[str] = Field(
        None,
        description="Updated fact text",
        min_length=cfg.min_text_length,
        max_length=cfg.max_text_length,
    )

    image_url: Optional[HttpUrl] = Field(
        None,
        description="Updated image URL",
        min_length=cfg.min_image_url_length,
        max_length=cfg.max_image_url_length,
    )


class CatFactOut(BaseOutModel):
    """DTO returned for cat facts."""

    text: str
    image_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CatFactStatsOut(BaseOutModel):
    """DTO for returning statistics for a local cat fact."""

    fact_id: int
    request_count: int
    last_requested_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
