from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from src.external_api.service import service
from src.external_api.models import CatFactModel, CatImageModel, CatCombinedModel


router = APIRouter(prefix="/external", tags=["External API"])


@router.get("/fact", response_model=CatFactModel)
def get_cat_fact() -> CatFactModel:
    """
    Return a random cat fact.
    """
    try:
        return service.get_cat_fact()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/image", response_model=CatImageModel)
def get_cat_image() -> CatImageModel:
    """
    Return a random cat image.
    """
    try:
        return service.get_cat_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cat", response_model=CatCombinedModel)
def get_cat_info() -> CatCombinedModel:
    """
    Return a combined cat fact and image.
    """
    try:
        return service.get_cat_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cat/html", response_class=HTMLResponse)
def get_cat_html() -> str:
    """
    Return an HTML page displaying a random cat image and fact.
    """
    try:
        result = service.get_cat_info()

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
        return f"<h3>Error loading cat info: {e}</h3>"
