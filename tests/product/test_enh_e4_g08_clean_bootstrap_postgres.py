"""G08 clean Product bootstrap acceptance evidence on real PostgreSQL."""

from __future__ import annotations

import os

import httpx
import pytest

from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.web_api.app import create_app


@pytest.mark.anyio
@pytest.mark.postgres
async def test_g08_product_migrated_database_starts_application_and_serves_product_api(
    monkeypatch: pytest.MonkeyPatch,
    postgres_engine,
) -> None:  # type: ignore[no-untyped-def]
    """Runner reset/upgrade precedes this Product API initialization and query."""
    database_url = os.environ["ARIADNE_PRODUCT_TEST_DATABASE_URL"]
    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
    dependencies._get_session_factory.cache_clear()
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=create_app()), base_url="http://test",
        ) as client:
            ready = await client.get("/health/ready")
            projects = await client.get("/api/v1/projects")
        assert ready.status_code == 200
        assert ready.json() == {"status": "ok"}
        assert projects.status_code == 200
        assert projects.json() == {"items": [], "next_cursor": None}
    finally:
        dependencies._get_session_factory.cache_clear()
