import os

import fakeredis.aioredis
import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"

from src.main import app  # noqa


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def fake_redis(monkeypatch):
    redis = fakeredis.aioredis.FakeRedis()

    monkeypatch.setattr("src.cache.service.get_redis", lambda: redis)

    return redis
