# test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def client():
    # use a fresh DB file for integration tests
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client

def test_create_and_list(client):
    payload = {"title":"Integration Paper","authors":"I. Tester","year":2021}
    r = client.post("/api/citations/", json=payload)
    assert r.status_code == 200 or r.status_code == 201
    data = r.json()
    assert data["title"] == "Integration Paper"

    r2 = client.get("/api/citations/")
    assert r2.status_code == 200
    assert any(item["title"] == "Integration Paper" for item in r2.json())
