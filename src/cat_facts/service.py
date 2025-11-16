# src/cat_facts/service.py

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.cat_facts.repository import (
    CatFactRepository,
    CatFactStatsRepository,
)
from src.cat_facts.models import (
    CatFactCreate,
    CatFactOut,
    CatFactStatsOut,
)


class CatFactService:
    """Service layer for cat facts and statistics."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.fact_repo = CatFactRepository(session)
        self.stats_repo = CatFactStatsRepository(session)

    async def create_fact(self, data: CatFactCreate) -> CatFactOut:
        """Create a new local fact + initialize its statistics."""

        payload = data.model_dump()
        if payload.get("image_url"):
            payload["image_url"] = str(payload["image_url"])

        fact = await self.fact_repo.create(payload)

        await self.stats_repo.create_initial(fact.id)

        return CatFactOut.model_validate(fact)

    async def get_local_random_fact(self) -> Optional[CatFactOut]:
        """Return random local fact and update its statistics."""

        fact = await self.fact_repo.get_random()
        if not fact:
            return None

        # Update statistics
        await self.stats_repo.increment_request_count(fact.id)

        return CatFactOut.model_validate(fact)

    async def get_fact(self, source: str) -> dict:
        """
        Return a fact depending on source:
        - external → fetch from APIs
        - local → fetch from DB + update stats
        """

        if source == "external":
            return await self.get_external_fact()

        # Local
        fact = await self.get_local_random_fact()
        if not fact:
            return {
                "message": "No local facts available",
                "source": "local"
            }

        return {
            "id": fact.id,
            "text": fact.text,
            "image_url": fact.image_url,
            "created_at": fact.created_at,
            "updated_at": fact.updated_at,
            "source": "local"
        }

    async def get_fact_stats(self, fact_id: int) -> Optional[CatFactStatsOut]:
        """Return statistics for a specific fact."""

        stats = await self.stats_repo.get_by_fact_id(fact_id)
        if not stats:
            return None

        return CatFactStatsOut.model_validate(stats)
