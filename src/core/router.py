from fastapi import APIRouter
import datetime

router = APIRouter(prefix="/common", tags=["common"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Service is running"}


@router.get("/time")
def get_time():
    return {"server_time": datetime.datetime.now().isoformat()}
