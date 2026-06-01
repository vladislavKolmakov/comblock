from datetime import datetime, timezone
from types import SimpleNamespace
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.database.session import get_db_session
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    async def override_get_db() -> AsyncGenerator[object, None]:
        yield object()

    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_get_news_list_returns_items(client: TestClient) -> None:
    fake_news = SimpleNamespace(
        id=1,
        url="https://ria.ru/test-1.html",
        title="Title 1",
        source="ria.ru",
        published_at=None,
        short_text=None,
        full_text=None,
        author=None,
        categories=None,
        tags=None,
        views_count=None,
        comments_count=None,
        keywords=None,
        summary=None,
        region=None,
        topic=None,
        has_video=None,
        enrichment_status=None,
        error_message=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        images=[],
    )
    with patch("app.api.news.NewsRepository.get_news_list", new=AsyncMock(return_value=[fake_news])):
        response = client.get("/news?limit=10&offset=0")

    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    assert len(payload["items"]) == 1
    assert payload["items"][0]["url"] == "https://ria.ru/test-1.html"


def test_get_news_by_id_returns_404_when_not_found(client: TestClient) -> None:
    with patch("app.api.news.NewsRepository.get_news_by_id", new=AsyncMock(return_value=None)):
        response = client.get("/news/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "News not found"


def test_post_enrich_returns_accepted(client: TestClient) -> None:
    with patch("app.api.news.NewsEnrichmentService.enrich_news", new=AsyncMock(return_value=None)):
        response = client.post(
            "/news/enrich",
            json={"urls": ["https://ria.ru/20200101/example.html"]},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "accepted",
        "message": "Enrichment started",
    }
