import contextlib
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.auth.auth_bearer import get_current_user
from app.database import get_db
from app.main import app
from app.models import Term, User


@pytest.fixture(autouse=True)
def disable_lifespan(monkeypatch):
    """Turn off lifespan for tests to avoid startup hooks."""

    @contextlib.asynccontextmanager
    async def null_lifespan(app_obj):
        yield

    monkeypatch.setattr(app.router, "lifespan_context", null_lifespan)


@pytest.fixture
def mock_db(mocker):
    """Fixture to mock the database session, query chain, and current user."""

    mock_session = mocker.MagicMock()
    mock_query = mocker.MagicMock()
    mock_filter = mocker.MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_session.query.return_value = mock_query
    mock_filter.first.return_value = None

    mock_user = mocker.MagicMock(spec=User)
    mock_user.id = 1
    mock_user.email = "testuser@example.com"

    return mock_session, mock_query, mock_filter, mock_user


@pytest.fixture
def client(mock_db):
    mock_session, _, _, mock_user = mock_db

    def override_get_db():
        yield mock_session

    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_explain_term_success(client, mock_db):
    mock_session, mock_query, mock_filter, _ = mock_db

    term_obj = Term(
        id=1,
        term="Docker",
        formal_definition="A platform for containerizing applications.",
        simple_definition="A tool for running apps in containers.",
        example="Docker lets you run nginx in a container.",
        why_it_matters="It simplifies deployment and scaling.",
        category="DevOps",
        category_id=1,
        difficulty=1,
        created_at=datetime.now(timezone.utc),
    )

    mock_filter.first.return_value = term_obj

    resp = client.post("/api/v1/terms/", json={"term": "Docker"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["term"].lower() == "docker"
    assert "formal_definition" in data
    assert "simple_definition" in data


def test_explain_term_not_found(client, mock_db):
    mock_session, mock_query, mock_filter, _ = mock_db

    mock_filter.first.return_value = None

    resp = client.post("/api/v1/terms/", json={"term": "NonexistentTerm"})
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
