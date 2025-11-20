import logging

import sentry_sdk
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.external_api.models import CatCombinedModel, CatFactModel, CatImageModel
from src.external_api.service import service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/external", tags=["External API"])


@router.get("/fact", response_model=CatFactModel)
def get_cat_fact() -> CatFactModel:
    logger.info("[EXTERNAL][FACT] Request cat fact")

    try:
        result = service.get_cat_fact()
        logger.info("[EXTERNAL][FACT] Success")
        return result

    except Exception as e:
        logger.exception("[EXTERNAL][FACT] Error while fetching cat fact")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve cat fact")


@router.get("/image", response_model=CatImageModel)
def get_cat_image() -> CatImageModel:
    logger.info("[EXTERNAL][IMAGE] Request cat image")

    try:
        result = service.get_cat_image()
        logger.info("[EXTERNAL][IMAGE] Success")
        return result

    except Exception as e:
        logger.exception("[EXTERNAL][IMAGE] Error fetching cat image")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve cat image")


@router.get("/cat", response_model=CatCombinedModel)
def get_cat_info() -> CatCombinedModel:
    logger.info("[EXTERNAL][CAT] Request combined cat fact + image")

    try:
        result = service.get_cat_info()
        logger.info("[EXTERNAL][CAT] Success")
        return result

    except Exception as e:
        logger.exception("[EXTERNAL][CAT] Error fetching combined cat info")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve cat info")


@router.get("/cat/html", response_class=HTMLResponse)
def get_cat_html() -> str:
    logger.info("[EXTERNAL][CAT HTML] Request cat HTML page")

    try:
        result = service.get_cat_info()

        logger.info("[EXTERNAL][CAT HTML] Success")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Random Cat Fact</title>
        </head>
        <body>
            <div class="container">
                <img src="{result.image_url}" alt="Cute cat photo" />
                <p>{result.fact}</p>
            </div>
        </body>
        </html>
        """
        return html_content

    except Exception as e:
        logger.exception("[EXTERNAL][CAT HTML] Error building cat HTML response")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to load cat HTML")
