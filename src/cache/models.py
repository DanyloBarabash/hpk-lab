from pydantic import BaseModel


class CacheItem(BaseModel):
    key: str
    value: str
    ttl: int | None = None
