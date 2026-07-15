from fastapi.testclient import TestClient

from app.api.main import app
from app.db.session import init_db, session_factory
from app.repositories.repository_repository import RepositoryRepository


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_search_endpoint_returns_match() -> None:
    init_db()
    session = session_factory()
    try:
        repository = RepositoryRepository(session)
        repository.create_with_context(
            owner_username="pytest-owner",
            owner_profile_url="https://github.com/pytest-owner",
            repository_name="pytest-demo-repo",
            source_platform="github",
            repository_url="https://github.com/pytest-owner/pytest-demo-repo",
            raw_description="A demo repository for testing semantic search behavior.",
            ai_generated_summary="This repository is a test fixture for semantic search similarity tasks.",
            embedding_vector="demo-vector",
        )
    finally:
        session.close()

    response = client.post("/api/search", json={"query": "pytest-demo-repo"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["query"] == "pytest-demo-repo"
    assert len(payload["matches"]) >= 1
