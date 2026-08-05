from __future__ import annotations

from pathlib import Path

from ariadne.domain import metadata as m
from ariadne.infrastructure.persistence import Database


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_application_does_not_import_infrastructure_package() -> None:
    application = REPOSITORY_ROOT / "src/ariadne/application"
    violations = [
        path
        for path in application.rglob("*.py")
        if "ariadne.infrastructure" in path.read_text(encoding="utf-8")
    ]
    assert violations == []


def test_api_routers_depend_on_metadata_port_and_domain_entities() -> None:
    routers = REPOSITORY_ROOT / "src/ariadne/interfaces/api/routers"
    for path in routers.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "sqlalchemy.orm import Session" not in source
        assert "infrastructure.persistence import models" not in source
        assert "infrastructure.persistence.models" not in source


def test_sqlalchemy_unit_of_work_commits_metadata(tmp_path: Path) -> None:
    database = Database(f"sqlite:///{tmp_path / 'metadata.db'}")
    database.create_schema()

    role = m.Role(code="TEST_ROLE", name="Test role", system_managed=False)
    with database.unit_of_work() as unit_of_work:
        unit_of_work.metadata.add(role)

    with database.unit_of_work() as unit_of_work:
        assert unit_of_work.metadata.get(m.Role, role.id) is not None
