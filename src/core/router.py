from fastapi import APIRouter, HTTPException
import datetime
import logging
import sentry_sdk

router = APIRouter(prefix="/common", tags=["common"])

logger = logging.getLogger(__name__)


@router.get("/healthcheck")
def healthcheck():
    logger.info("[COMMON][HEALTHCHECK] Service health check called")
    return {"status": "ok", "message": "Service is running"}


@router.get("/time")
def get_time():
    logger.info("[COMMON][TIME] Get server time")
    try:
        now = datetime.datetime.now().isoformat()
        logger.debug(f"[COMMON][TIME] current time={now}")
        return {"server_time": now}
    except Exception as e:
        logger.exception("[COMMON][TIME] error")
        sentry_sdk.capture_exception(e)
        raise HTTPException(500, "Failed to get server time")


@router.get("/sentry-debug")
async def trigger_error():
    logger.info("[COMMON][SENTRY-DEBUG] Trigger manual Sentry exception")

    try:
        division_by_zero = 1 / 0

        return {"division_by_zero": division_by_zero}

    except Exception as e:
        logger.exception("[COMMON][SENTRY-DEBUG] Division by zero error")
        sentry_sdk.capture_exception(e)
        raise HTTPException(500, "Triggered Sentry test error")
