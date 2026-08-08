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
def predictive_spec_factory():  # type: ignore[no-untyped-def]
    def build(task_type: str = "BINARY_CLASSIFICATION") -> dict:  # type: ignore[type-arg]
        metric = "ROC_AUC" if task_type == "BINARY_CLASSIFICATION" else "RMSE"
        return {
            "schema_version": "predictive-analysis-spec/1",
            "task_type": task_type,
            "prediction_question": {
                "prediction_unit": "customer", "target": "converted",
                "prediction_time": "2026-01-01T00:00:00Z", "horizon": "30 days",
                "intended_use": "prioritize outreach",
                "deployment_population": "eligible customers",
            },
            "feature_spec": {
                "feature_columns": ["score"],
                "availability_cutoff": {"score": {
                    "column": "score", "available_at": "PREDICTION_TIME", "allowed": True,
                }},
                "excluded_columns": ["converted", "customer_id"],
            },
            "split_spec": {
                "strategy": "RANDOM", "train_ratio": 0.6,
                "validation_ratio": 0.2, "test_ratio": 0.2,
                "group_column": None, "time_column": None,
                "train_cutoff": None, "validation_cutoff": None,
                "stratify": False, "seed": 17,
            },
            "preprocessing_spec": {}, "model_spec": {}, "tuning_spec": {},
            "evaluation_spec": {
                "primary_metric": metric, "secondary_metrics": [], "subgroups": [],
            },
            "explanation_spec": {},
        }
    return build


@pytest.fixture
async def client(product_env):  # type: ignore[no-untyped-def]
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_app()), base_url="http://test"
    ) as value:
        yield value
