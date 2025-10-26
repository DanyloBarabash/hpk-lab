from dataclasses import dataclass


@dataclass
class CatConfig:
    """Configuration limits for cat API models."""

    min_fact_length: int = 10
    max_fact_length: int = 300

    min_url_length: int = 10
    max_url_length: int = 300

    min_length_value: int = 1
    max_length_value: int = 10000


cat_config = CatConfig()
