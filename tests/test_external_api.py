from unittest.mock import Mock, patch

import pytest
import requests

FACT_TEXT = "Cats sleep for 12–16 hours every day. Long fact to satisfy model length limits."

IMAGE_URL = "https://example.com/images/supercat_1234567890.jpg"


def make_mock_response(json_data: dict, status_code: int = 200) -> Mock:
    mock_resp = Mock()
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.return_value = None
    mock_resp.status_code = status_code
    return mock_resp


@pytest.fixture
def mock_requests_get():
    with patch("src.external_api.service.requests.get") as mock:
        yield mock


def test_cat_fact(client, mock_requests_get):
    fact = FACT_TEXT

    mock_requests_get.return_value = make_mock_response({"fact": fact, "length": len(fact)})

    response = client.get("/external/fact")
    assert response.status_code == 200

    data = response.json()
    assert data["fact"] == fact
    assert data["length"] == len(fact)


def test_cat_image(client, mock_requests_get):
    mock_requests_get.return_value = make_mock_response([{"url": IMAGE_URL}])

    response = client.get("/external/image")
    assert response.status_code == 200

    data = response.json()
    assert data["url"] == IMAGE_URL


def test_cat_combined(client, mock_requests_get):
    fact = FACT_TEXT

    mock_requests_get.side_effect = [
        make_mock_response({"fact": fact, "length": len(fact)}),
        make_mock_response([{"url": IMAGE_URL}]),
    ]

    response = client.get("/external/cat")
    assert response.status_code == 200

    data = response.json()
    assert data["fact"] == fact
    assert data["image_url"] == IMAGE_URL


def mock_failed_request(*args, **kwargs):
    raise Exception("API failed")


@patch("src.external_api.service.CatService.get_cat_fact", side_effect=mock_failed_request)
def test_cat_fact_error(mock_method, client):
    response = client.get("/external/fact")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat fact"


@patch("src.external_api.service.CatService.get_cat_image", side_effect=mock_failed_request)
def test_cat_image_error(mock_method, client):
    response = client.get("/external/image")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat image"


@patch("src.external_api.service.CatService.get_cat_info", side_effect=mock_failed_request)
def test_cat_combined_error(mock_method, client):
    response = client.get("/external/cat")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve cat info"


@patch("src.external_api.service.CatService.get_cat_fact", side_effect=requests.Timeout)
def test_cat_fact_timeout(mock_method, client):
    response = client.get("/external/fact")
    assert response.status_code == 500


def test_cat_fact_wrong_method(client):
    response = client.post("/external/fact")
    assert response.status_code == 405


def test_external_wrong_route(client):
    response = client.get("/external/not-found")
    assert response.status_code == 404
