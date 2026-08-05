"""Pipeline configuration document IO kept local to the pipeline use case."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


def load_yaml_mapping(path: Path | str) -> dict[str, Any]:
    resolved = Path(path)
    with resolved.open(encoding="utf-8") as stream:
        document = yaml.safe_load(stream) or {}
    if not isinstance(document, Mapping):
        raise ValueError(f"YAML root must be a mapping: {resolved}")
    return dict(document)


def dump_yaml(path: Path | str, document: Mapping[str, Any]) -> None:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(
        yaml.safe_dump(dict(document), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def resolve_project_path(path: Path | str, project_root: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else project_root / value


__all__ = ["dump_yaml", "load_yaml_mapping", "resolve_project_path"]
