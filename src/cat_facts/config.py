from dataclasses import dataclass


@dataclass
class CatFactConfig:
    """Configuration for cat facts validation."""

    # Limits for fact text
    min_text_length: int = 5
    max_text_length: int = 500

    # Limits for image URLs
    min_image_url_length: int = 10
    max_image_url_length: int = 500


cat_fact_config = CatFactConfig()
