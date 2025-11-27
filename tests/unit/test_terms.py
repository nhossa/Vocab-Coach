import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.main import app
from app.models import Term
from app.database import get_db
import contextlib


@pytest.fixture(autouse=True)
def disable_lifespan(monkeypatch):
    """Turn off lifespan for tests to avoid startup hooks."""
    @contextlib.asynccontextmanager
    async def null_lifespan(app_obj):
        yield
    monkeypatch.setattr(app.router, "lifespan_context", null_lifespan)


@pytest.fixture
def mock_db(mocker):
    """Fixture to mock the database session and query chain."""
    mock_session = mocker.MagicMock()
    # Default: no term found
    mock_query = mocker.MagicMock()
    mock_filter = mocker.MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_session.query.return_value = mock_query
    mock_filter.first.return_value = None
    return mock_session, mock_query, mock_filter


@pytest.fixture
def client(mock_db):
    mock_session, _, _ = mock_db
    def override_get_db():
        yield mock_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# --- Parametrized tests (@pytest.mark.parametrize) ---

def test_explain_term_success(client, mock_db, mocker):
    mock_session, mock_query, mock_filter = mock_db
    # Simulate found term
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

# --- Testing functions with inputs/outputs ---
# --- Asserting expected output (assert) ---



def test_explain_term_not_found(client, mock_db):
    mock_session, mock_query, mock_filter = mock_db
    # Simulate not found
    mock_filter.first.return_value = None
    resp = client.post("/api/v1/terms/", json={"term": "NonexistentTerm"})
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
