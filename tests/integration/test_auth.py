import os
import pytest
from fastapi.testclient import TestClient

# Force a local SQLite DB for tests before importing the app/database modules
os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"

from app.main import app
from app.database import Base, SessionLocal, engine, get_db

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_register_and_login_happy_path(client):
    resp = client.post("/api/v1/auth/register", json={"email": "user@example.com", "password": "pytestpass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

    resp = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "pytestpass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_register_duplicate_user_error(client):
    # Register the first time
    resp1 = client.post("/api/v1/auth/register", json={"email": "dupe@example.com", "password": "pytestpass123"})
    assert resp1.status_code == 200
    # Register again with the same email
    resp2 = client.post("/api/v1/auth/register", json={"email": "dupe@example.com", "password": "pytestpass123"})
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["detail"].lower()
