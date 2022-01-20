from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from oteapi.plugins import load_plugins

from app.context import datafilter

from .dummycache import DummyCache

# from oteapi.strategies.parse import text_json
load_plugins()

app = FastAPI()
app.include_router(datafilter.router, prefix="/datasource")
client = TestClient(app)


async def override_depends_redis() -> DummyCache:
    return DummyCache(
        {
            "dataresource-6506911a-cf30-4b20-a14c-19641b8c272b": {
                "filterType": "dataresource/json",
                "configuration": {},
            }
        }
    )


app.dependency_overrides[datafilter.depends_redis] = override_depends_redis


def test_create_dataresource():
    abspath = Path(__file__).absolute().parent / "address.json"

    response = client.post(
        "/datasource/",
        json={
            # TODO: figure out how to get the file download strategy to
            # work within the docker
            # "downloadUrl": f"file://{abspath}",
            "downloadUrl": "https://filesamples.com/samples/code/json/sample2.json",
            "mediaType": "text/json",
        },
    )
    # Ensure that session returns with a session id
    print("=" * 70)
    print(response.json())
    print("=" * 70)
    assert response.status_code == 200
    assert "resource_id" in response.json()


def test_get_dataresource():
    response = client.get(
        "/dataresource/dataresource-6506911a-cf30-4b20-a14c-19641b8c272b",
        json={},
    )
    assert response.status_code == 200


def test_initialize_dataresource():
    response = client.post(
        "/dataresource/dataresource-6506911a-cf30-4b20-a14c-19641b8c272b/" "initialize",
        json={},
    )
    assert response.status_code == 200
