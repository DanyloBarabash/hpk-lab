from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from datetime import datetime

from src.database.base import Base
from src.database.base_schema import UpdatedMix


class CatFact(Base, UpdatedMix):
    """Local cat fact."""

    __tablename__ = "cat_facts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True
    )

    stats: Mapped["CatFactStats"] = relationship(
        back_populates="fact",
        uselist=False,
        cascade="all, delete"
    )


class CatFactStats(Base, UpdatedMix):
    """Statistics for local cat facts."""

    __tablename__ = "cat_fact_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    fact_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cat_facts.id"),
        unique=True,
        nullable=False
    )

    request_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_requested_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False),
        nullable=True
    )

    fact: Mapped["CatFact"] = relationship(
        back_populates="stats"
    )
