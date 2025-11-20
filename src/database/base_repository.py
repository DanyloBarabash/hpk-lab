import logging
from typing import Generic, List, Optional, Type, TypeVar

import sentry_sdk
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)

logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository for SQLAlchemy ORM models."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[ModelType]:
        """Return all records of the model."""
        logger.info(f"[DB][{self.model.__name__}][GET_ALL] Fetching all records")

        try:
            stmt = select(self.model)
            result = await self.session.execute(stmt)
            items = result.scalars().all()

            logger.info(f"[DB][{self.model.__name__}][GET_ALL] OK ({len(items)} records)")
            return items

        except Exception as e:
            logger.exception(f"[DB][{self.model.__name__}][GET_ALL] Error")
            sentry_sdk.capture_exception(e)
            raise

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """Return a record by primary key."""
        logger.info(f"[DB][{self.model.__name__}][GET] id={obj_id}")

        try:
            stmt = select(self.model).where(self.model.id == obj_id)
            result = await self.session.execute(stmt)
            item = result.scalar_one_or_none()

            if item is None:
                logger.warning(f"[DB][{self.model.__name__}][GET] id={obj_id} not found")
            else:
                logger.info(f"[DB][{self.model.__name__}][GET] OK")

            return item

        except Exception as e:
            logger.exception(f"[DB][{self.model.__name__}][GET] Error id={obj_id}")
            sentry_sdk.capture_exception(e)
            raise

    async def create(self, data: dict) -> ModelType:
        """Create and store a new record."""
        logger.info(f"[DB][{self.model.__name__}][CREATE] data={data}")

        try:
            obj = self.model(**data)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)

            logger.info(f"[DB][{self.model.__name__}][CREATE] OK id={obj.id}")
            return obj

        except Exception as e:
            logger.exception(f"[DB][{self.model.__name__}][CREATE] Error")
            sentry_sdk.capture_exception(e)
            await self.session.rollback()
            raise

    async def update(self, obj_id: int, data: dict) -> Optional[ModelType]:
        """Update an existing record and return the updated model instance."""
        logger.info(f"[DB][{self.model.__name__}][UPDATE] id={obj_id}, data={data}")

        try:
            stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model)
            result = await self.session.execute(stmt)
            updated = result.scalar_one_or_none()
            await self.session.commit()

            if updated:
                logger.info(f"[DB][{self.model.__name__}][UPDATE] OK id={obj_id}")
            else:
                logger.warning(f"[DB][{self.model.__name__}][UPDATE] id={obj_id} not found")

            return updated

        except Exception as e:
            logger.exception(f"[DB][{self.model.__name__}][UPDATE] Error id={obj_id}")
            sentry_sdk.capture_exception(e)
            await self.session.rollback()
            raise

    async def delete(self, obj_id: int) -> None:
        """Delete a record by ID."""
        logger.info(f"[DB][{self.model.__name__}][DELETE] id={obj_id}")

        try:
            stmt = delete(self.model).where(self.model.id == obj_id)
            await self.session.execute(stmt)
            await self.session.commit()

            logger.info(f"[DB][{self.model.__name__}][DELETE] OK id={obj_id}")

        except Exception as e:
            logger.exception(f"[DB][{self.model.__name__}][DELETE] Error id={obj_id}")
            sentry_sdk.capture_exception(e)
            await self.session.rollback()
            raise
