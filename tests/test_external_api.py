from unittest.mock import patch

import requests


def test_cat_fact(client):
    response = client.get("/external/fact")
    assert response.status_code == 200
    assert "fact" in response.json()


def test_cat_image(client):
    response = client.get("/external/image")
    assert response.status_code == 200
    assert "url" in response.json()


def test_cat_combined(client):
    response = client.get("/external/cat")
    assert response.status_code == 200
    data = response.json()
    assert "fact" in data
    assert "image_url" in data


def mock_failed_request(*args, **kwargs):
    """Симуляція падіння зовнішнього API"""
    raise Exception("API failed")


@patch("src.external_api.service.requests.get", side_effect=mock_failed_request)
def test_cat_fact_error(mock_get, client):
    response = client.get("/external/fact")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat fact"


@patch("src.external_api.service.requests.get", side_effect=mock_failed_request)
def test_cat_image_error(mock_get, client):
    response = client.get("/external/image")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat image"


@patch("src.external_api.service.requests.get", side_effect=mock_failed_request)
def test_cat_combined_error(mock_get, client):
    response = client.get("/external/cat")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat info"


@patch("src.external_api.service.requests.get", side_effect=requests.Timeout)
def test_cat_fact_timeout(mock_get, client):
    response = client.get("/external/fact")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat fact"


MockInvalidResponse = type(
    "MockInvalidResponse",
    (),
    {
        "json": lambda: {"invalid": "data"},
        "raise_for_status": lambda: None,
    },
)


@patch("src.external_api.service.requests.get", return_value=MockInvalidResponse())
def test_cat_fact_invalid_format(mock_get, client):
    response = client.get("/external/fact")
    assert response.status_code == 500


def test_cat_fact_wrong_method(client):
    response = client.post("/external/fact")
    assert response.status_code == 405


def test_external_wrong_route(client):
    response = client.get("/external/not-found")
    assert response.status_code == 404
