# src/database/base_repository.py

from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.database.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository for SQLAlchemy ORM models."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[ModelType]:
        """Return all records of the model."""
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """Return a record by primary key."""
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> ModelType:
        """Create and store a new record."""
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj_id: int, data: dict) -> Optional[ModelType]:
        """Update an existing record and return the updated model instance."""
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        updated = result.scalar_one_or_none()
        await self.session.commit()
        return updated

    async def delete(self, obj_id: int) -> None:
        """Delete a record by ID."""
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(stmt)
        await self.session.commit()
