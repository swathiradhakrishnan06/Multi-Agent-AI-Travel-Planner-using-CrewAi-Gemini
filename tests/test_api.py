# tests/test_api.py
import json
from fastapi.testclient import TestClient
import pytest

# Import the app
from src.travel_planner.api import app  # if your PYTHONPATH treats src as package root
# If import fails, use "from travel_planner.api import app"

client = TestClient(app)


def mock_kickoff_success(inputs):
    # Return a small predictable dict that the crew would return
    return {
        "recommended": [
            {"id": "1", "price": 400.0, "route": ["MEL", "SIN", "BLR"], "stopover": "SIN"},
            {"id": "2", "price": 420.0, "route": ["MEL", "KUL", "BLR"], "stopover": "KUL"},
        ],
        "meta": {"queried_at": "2025-08-01"}
    }


@pytest.fixture(autouse=True)
def patch_crew_kickoff(monkeypatch):
    # Patch the crew.kickoff used by the API to avoid real external calls
    import travel_planner.crew as crew_module
    monkeypatch.setattr(crew_module.crew, "kickoff", mock_kickoff_success)
    yield


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_plan_trip_success():
    payload = {
        "origin": "MEL",
        "destination": "BLR",
        "date": "2025-08-01",
        "interests": ["food", "culture"]
    }
    r = client.post("/plan-trip", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    assert "recommended" in body["data"]
    assert isinstance(body["data"]["recommended"], list)
