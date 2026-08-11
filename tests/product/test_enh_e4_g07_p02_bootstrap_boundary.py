"""G07 P02 contracts for the Product-only migration/bootstrap boundary."""

from __future__ import annotations

import ast
import configparser
import os
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text


REPOSITORY = Path(__file__).parents[2]


def _product_head() -> str:
    config = Config(str(REPOSITORY / "alembic_product.ini"))
    heads = ScriptDirectory.from_config(config).get_heads()
    assert len(heads) == 1, f"Product migration chain must have exactly one head: {heads}"
    return heads[0]


def _env_contracts() -> tuple[set[str], set[str], set[str]]:
    """Extract imports, environment keys, and Alembic version tables from env.py."""
    path = REPOSITORY / "product_migrations" / "env.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    environment_keys: set[str] = set()
    version_tables: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "getenv" and node.args and isinstance(node.args[0], ast.Constant):
                environment_keys.add(str(node.args[0].value))
            if node.func.attr == "configure":
                for keyword in node.keywords:
                    if keyword.arg == "version_table" and isinstance(keyword.value, ast.Constant):
                        version_tables.add(str(keyword.value.value))
    return imports, environment_keys, version_tables


def test_product_alembic_configuration_is_product_only() -> None:
    product_config = configparser.ConfigParser()
    product_config.read(REPOSITORY / "alembic_product.ini", encoding="utf-8")
    root_config = configparser.ConfigParser()
    root_config.read(REPOSITORY / "alembic.ini", encoding="utf-8")
    imports, environment_keys, version_tables = _env_contracts()

    assert product_config["alembic"]["script_location"] == "product_migrations"
    if (REPOSITORY / "alembic.ini").exists():
        assert root_config["alembic"]["script_location"] == "migrations"
    else:
        # Dockerfile.test intentionally omits the root chain from the test image.
        assert not (REPOSITORY / "migrations").exists()
    assert "ariadne.product.persistence.orm_models" in imports
    assert "ARIADNE_PRODUCT_DATABASE_URL" in environment_keys
    assert version_tables == {"alembic_version_product"}
    assert _product_head()


def test_repository_managed_bootstrap_surfaces_cannot_invoke_root_chain() -> None:
    if not (REPOSITORY / "compose.yaml").exists():
        # The PostgreSQL test image deliberately contains only Product migration assets.
        assert not (REPOSITORY / "alembic.ini").exists()
        assert not (REPOSITORY / "migrations").exists()
        return

    compose = (REPOSITORY / "compose.yaml").read_text(encoding="utf-8")
    dockerfile = (REPOSITORY / "Dockerfile").read_text(encoding="utf-8")
    dockerfile_test = (REPOSITORY / "Dockerfile.test").read_text(encoding="utf-8")
    runner = (REPOSITORY / "scripts/test/run_product_postgres_tests_in_container.sh").read_text(
        encoding="utf-8"
    )

    assert 'command: ["alembic", "-c", "alembic_product.ini", "upgrade", "head"]' in compose
    assert "COPY --chmod=0644 alembic_product.ini ./" in dockerfile
    assert "COPY --chmod=0755 product_migrations ./product_migrations" in dockerfile
    assert "COPY alembic_product.ini ./" in dockerfile_test
    assert "COPY product_migrations ./product_migrations" in dockerfile_test
    assert "alembic -c alembic_product.ini upgrade head" in runner
    assert "alembic -c alembic_product.ini current" in runner
    for active_surface in (compose, dockerfile, dockerfile_test, runner):
        assert "-c alembic.ini" not in active_surface
        assert "COPY migrations " not in active_surface
        assert "./migrations" not in active_surface


@pytest.mark.postgres
def test_fresh_product_database_has_only_product_migration_authority() -> None:
    database_url = os.getenv("ARIADNE_PRODUCT_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("ARIADNE_PRODUCT_TEST_DATABASE_URL is not configured")
    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        tables = set(inspect(engine).get_table_names())
        with engine.connect() as connection:
            database_head = connection.scalar(text("SELECT version_num FROM alembic_version_product"))
        assert database_head == _product_head()
        assert "alembic_version_product" in tables
        assert "alembic_version" not in tables
        assert {"product_project", "product_execution", "product_result", "product_artifact"} <= tables
        # `app_user` is created by the root historical chain and is not Product metadata.
        assert "app_user" not in tables
    finally:
        engine.dispose()
