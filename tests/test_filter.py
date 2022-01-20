from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import datafilter
from oteapi.plugins.plugins import import_module

from .dummycache import DummyCache
from .strategies.filter import demofilter


app = FastAPI()

app.include_router(datafilter.router, prefix="/filter")
client = TestClient(app)
#import_module("strategies.filter.demofilter")

async def override_depends_redis() -> DummyCache:
    return DummyCache(
        {
            "filter-961f5314-9e8e-411e-a216-ba0eb8e8bc6e": {
                "filterType": "filter/demo",
                "configuration": {},
            }
        }
    )


app.dependency_overrides[datafilter.depends_redis] = override_depends_redis


def test_create_filter():
    response = client.post(
        "/filter/",
        json={
            "filterType": "filter/demo",
            "query": "SELECT * FROM Test",
            "condition": "",
            "limit": 1,
            "configuration": {"demoData": ["a", "b", "c"]},
        },
    )
    # Ensure that session returns with a session id
    assert "filter_id" in response.json()
    assert response.status_code == 200


def test_get_filter():
    response = client.get("/filter/filter-961f5314-9e8e-411e-a216-ba0eb8e8bc6e")
    assert response.status_code == 200


def test_initialize_filter():
    response = client.post(
        "/filter/filter-961f5314-9e8e-411e-a216-ba0eb8e8bc6e/initialize", json={}
    )
    assert response.status_code == 200
