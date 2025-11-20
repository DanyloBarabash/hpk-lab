import os
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from src.cache import router as cache_router
from src.cat_facts import router as cat_fact_router
from src.core import router as common_routes
from src.core.logging.logging_config import setup_logging
from src.core.logging.sentry import init_sentry
from src.database.base import _init_db_models  # noqa
from src.external_api import router as external_router
from src.storage import router as storage_router


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_sentry()
    setup_logging()
    # # Initialize DB tables on startup
    # await _init_db_models()
    yield


if os.getenv("TESTING") != "1":
    run_migrations()


app = FastAPI(
    title="Lab FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(common_routes.router)

# Include storage module routes and external api router
app.include_router(storage_router.router)
app.include_router(external_router.router)
app.include_router(cat_fact_router.router)
app.include_router(cache_router.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is running!"}
