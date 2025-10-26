from fastapi import FastAPI
from src.core import router as common_routes
from src.storage import router as storage_router
from src.external_api import router as external_router

app = FastAPI(
    title="Lab FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0"
)

app.include_router(common_routes.router)

# Include storage module routes and external api router
app.include_router(storage_router.router)
app.include_router(external_router.router)
