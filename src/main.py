from fastapi import FastAPI
from src.core import router as common_routes
from src.storage import router as storage_router

app = FastAPI(
    title="Lab FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0"
)

app.include_router(common_routes.router)

# Include storage module routes
app.include_router(storage_router.router)
