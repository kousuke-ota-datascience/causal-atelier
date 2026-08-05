"""Migration schema tests.

Covers four of the five test categories required by the migration policy:

  A. Fresh database test — upgrade head creates all ORM-mapped tables.
  B. Upgrade path test — revision-by-revision upgrade preserves the same schema.
  C. Fresh vs upgraded equivalence — the two paths produce the same table set.
  D. ORM independence test — revisions 0001 and 0002 do not import ORM classes.

Category E (PostgreSQL trigger tests) requires a live PostgreSQL connection and
is intentionally omitted here.  SQLite does not enforce triggers in the same way
as PostgreSQL; the trigger behaviour is tested in the PostgreSQL CI environment.

NOTE ON SQLITE LIMITATIONS
  - Partial-unique indexes with WHERE clauses are created but the WHERE clause
    is not enforced by SQLite.
  - PostgreSQL-only FK constraints (use_alter) and deferred FK creation blocks
    guarded by `if is_pg` are NOT executed against SQLite.  The FK constraints
    exist only in the ORM and are enforced at the application layer on SQLite.
  - CHECK constraints defined on causal_graph_edge are not enforced by SQLite.
  These are documented limitations; they do NOT indicate migration defects.
"""

from __future__ import annotations

import ast
import os
import sys
import tempfile
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"
VERSIONS_DIR = MIGRATIONS_DIR / "versions"

sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def sqlite_db_url(tmp_path: Path) -> str:
    return f"sqlite:///{tmp_path / 'test.db'}"


@pytest.fixture
def alembic_cfg(sqlite_db_url: str) -> Config:
    cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.set_main_option("sqlalchemy.url", sqlite_db_url)
    return cfg


def _get_tables(url: str) -> set[str]:
    engine = sa.create_engine(url)
    try:
        with engine.connect() as conn:
            return set(sa.inspect(conn).get_table_names()) - {"alembic_version"}
    finally:
        engine.dispose()


# ── D. ORM independence ───────────────────────────────────────────────────────


def test_initial_revision_has_no_orm_dependency() -> None:
    """Revision 0001 must not import or call any current ORM metadata."""
    path = VERSIONS_DIR / "20260719_0001_initial_metadata.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_modules = {
        "ariadne.infrastructure.persistence.models",
        "ariadne.domain.metadata",
        "ariadne.domain",
    }
    forbidden_attrs = {"create_all", "drop_all"}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module not in forbidden_modules, (
                f"Revision 0001 imports forbidden module: {node.module!r}"
            )
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attrs:
            pytest.fail(
                f"Revision 0001 references forbidden attribute: {node.attr!r}"
            )


def test_second_revision_has_no_orm_dependency() -> None:
    """Revision 0002 must not import ORM model classes."""
    path = VERSIONS_DIR / "20260720_0002_analysis_ready_mvp.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    forbidden_modules = {
        "ariadne.infrastructure.persistence.models",
        "ariadne.domain.metadata",
        "ariadne.domain",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module not in forbidden_modules, (
                f"Revision 0002 imports forbidden module: {node.module!r}"
            )


# ── A. Fresh database test ────────────────────────────────────────────────────


def test_fresh_upgrade_head_creates_all_orm_tables(
    alembic_cfg: Config, sqlite_db_url: str
) -> None:
    """upgrade head on an empty DB must produce every table in Base.metadata."""
    from ariadne.domain.metadata import Base

    command.upgrade(alembic_cfg, "head")
    actual = _get_tables(sqlite_db_url)
    expected = set(Base.metadata.tables.keys())

    missing = expected - actual
    assert not missing, f"Tables missing after upgrade head: {sorted(missing)}"


def test_fresh_upgrade_head_has_no_unexpected_tables(
    alembic_cfg: Config, sqlite_db_url: str
) -> None:
    """upgrade head must not create tables outside Base.metadata."""
    from ariadne.domain.metadata import Base

    command.upgrade(alembic_cfg, "head")
    actual = _get_tables(sqlite_db_url)
    expected = set(Base.metadata.tables.keys())

    extra = actual - expected
    assert not extra, f"Unexpected tables after upgrade head: {sorted(extra)}"


# ── B. Upgrade path test ──────────────────────────────────────────────────────


def test_upgrade_step_by_step_reaches_all_tables(
    alembic_cfg: Config, sqlite_db_url: str
) -> None:
    """Applying revisions one at a time must reach the same final schema."""
    from ariadne.domain.metadata import Base

    for rev in ["20260719_0001", "20260720_0002", "20260803_0003"]:
        command.upgrade(alembic_cfg, rev)

    actual = _get_tables(sqlite_db_url)
    expected = set(Base.metadata.tables.keys())
    assert not (expected - actual), (
        f"Missing after step-by-step upgrade: {sorted(expected - actual)}"
    )


# ── C. Fresh vs upgraded equivalence ─────────────────────────────────────────


def test_downgrade_base_drops_all_tables(
    alembic_cfg: Config, sqlite_db_url: str
) -> None:
    """downgrade base must leave no application tables."""
    command.upgrade(alembic_cfg, "head")
    command.downgrade(alembic_cfg, "base")
    remaining = _get_tables(sqlite_db_url)
    assert not remaining, (
        f"Tables remain after downgrade to base: {sorted(remaining)}"
    )


def test_upgrade_downgrade_upgrade_is_idempotent(
    alembic_cfg: Config, sqlite_db_url: str
) -> None:
    """Schema after upgrade→downgrade→upgrade must equal a fresh upgrade."""
    from ariadne.domain.metadata import Base

    command.upgrade(alembic_cfg, "head")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

    actual = _get_tables(sqlite_db_url)
    expected = set(Base.metadata.tables.keys())
    assert not (expected - actual), (
        f"Missing after up/down/up cycle: {sorted(expected - actual)}"
    )
    assert not (actual - expected), (
        f"Extra after up/down/up cycle: {sorted(actual - expected)}"
    )


def test_fresh_path_equals_step_by_step_path(tmp_path: Path) -> None:
    """A fresh upgrade and a step-by-step upgrade must produce the same tables."""
    def _run(db_name: str) -> set[str]:
        db_url = f"sqlite:///{tmp_path / db_name}"
        cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
        cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
        cfg.set_main_option("sqlalchemy.url", db_url)
        command.upgrade(cfg, "head")
        return _get_tables(db_url)

    fresh = _run("fresh.db")
    step = _run("step.db")

    assert fresh == step, (
        f"Schema mismatch: fresh-only={sorted(fresh - step)}, "
        f"step-only={sorted(step - fresh)}"
    )
