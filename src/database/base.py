from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from src.settings import settings


DATABASE_URL: str = settings.postgres

# Async engine for PostgreSQL
engine = create_async_engine(
    url=DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

# Async session factory
db_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base ORM class for all SQLAlchemy models."""
    pass


async def _init_citext(conn):
    """Initialize PostgreSQL CITEXT extension if supported."""
    try:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext;"))
    except Exception:
        pass


async def _init_db_models():
    """
    Initialize all tables on startup.
    Should be called inside FastAPI lifespan.
    """
    try:
        async with engine.begin() as conn:
            await _init_citext(conn)
            await conn.run_sync(Base.metadata.create_all)

    except IntegrityError:
        # Tables already exist — safe to ignore
        pass

    except Exception as error:
        print(f"DB init error: {error}")


async def get_db_session():
    """FastAPI dependency: yields an async DB session."""
    async with db_session_factory() as session:
        yield session
