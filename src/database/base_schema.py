import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

from pydantic import BaseModel, ConfigDict

from src.database.utils import get_datetime


class UpdatedMix:
    """SQLAlchemy mixin that adds timestamp columns to ORM models."""

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_datetime,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_datetime,
    )

    def update_time(self) -> None:
        """Set 'updated_at' to the current datetime."""
        self.updated_at = get_datetime()


class BaseOutModel(BaseModel):
    """Base Pydantic model for all models using UpdatedMix."""

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
