from contextlib import asynccontextmanager

from src.database.base import _init_db_models
from fastapi import FastAPI
from src.core import router as common_routes
from src.storage import router as storage_router
from src.external_api import router as external_router
from src.cat_facts import router as cat_fact_router
from alembic.config import Config
from alembic import command


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    await _init_db_models()
    yield


run_migrations()


app = FastAPI(
    title="Lab FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0"
)

app.include_router(common_routes.router)

# Include storage module routes and external api router
app.include_router(storage_router.router)
app.include_router(external_router.router)
app.include_router(cat_fact_router.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is running!"}