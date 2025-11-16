from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update

from src.database.base_repository import BaseRepository
from src.cat_facts.schema import CatFact, CatFactStats
from src.database.utils import get_datetime


class CatFactRepository(BaseRepository[CatFact]):
    """Repository for managing local cat facts."""

    def __init__(self, session: AsyncSession):
        super().__init__(CatFact, session)

    async def get_random(self) -> Optional[CatFact]:
        """Return a random local cat fact."""
        stmt = (
            select(CatFact)
            .order_by(func.random())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class CatFactStatsRepository(BaseRepository[CatFactStats]):
    """Repository for managing statistics of cat facts."""

    def __init__(self, session: AsyncSession):
        super().__init__(CatFactStats, session)

    async def get_by_fact_id(self, fact_id: int) -> Optional[CatFactStats]:
        """Return stats for a specific fact, or None if not found."""
        stmt = select(CatFactStats).where(CatFactStats.fact_id == fact_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_initial(self, fact_id: int) -> CatFactStats:
        """Create initial statistics record for a fact."""
        obj = CatFactStats(
            fact_id=fact_id,
            request_count=0,
            last_requested_at=None,
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def increment_request_count(self, fact_id: int) -> Optional[CatFactStats]:
        """Increment request counter and update last_requested_at."""
        stmt = (
            update(CatFactStats)
            .where(CatFactStats.fact_id == fact_id)
            .values(
                request_count=CatFactStats.request_count + 1,
                last_requested_at=get_datetime(),
            )
            .returning(CatFactStats)
        )
        result = await self.session.execute(stmt)
        updated = result.scalar_one_or_none()
        await self.session.commit()
        return updated
