from __future__ import annotations

import os
from pathlib import Path

import pytest
import httpx
from sqlalchemy import event

from ariadne.interfaces.web_api import dependencies
from ariadne.interfaces.web_api.app import create_app
from ariadne.product.persistence.orm_models import ProductBase


@pytest.fixture
def product_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database_url = f"sqlite:///{tmp_path / 'product.db'}"
    monkeypatch.setenv("ARIADNE_PRODUCT_DATABASE_URL", database_url)
    monkeypatch.setenv("ARIADNE_ARTIFACT_ROOT", str(tmp_path / "objects"))
    dependencies._get_session_factory.cache_clear()
    factory = dependencies._get_session_factory()
    engine = factory.kw["bind"]
    @event.listens_for(engine, "connect")
    def foreign_keys(dbapi_connection, _):  # type: ignore[no-untyped-def]
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
    ProductBase.metadata.create_all(engine)
    yield database_url, tmp_path
    dependencies._get_session_factory.cache_clear()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client(product_env):  # type: ignore[no-untyped-def]
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_app()), base_url="http://test"
    ) as value:
        yield value
