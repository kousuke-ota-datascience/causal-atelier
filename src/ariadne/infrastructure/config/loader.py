"""YAML loading, dumping, and small schema primitives."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from ariadne.infrastructure.config.paths import resolve_project_path


def ensure_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    """Validate that a parsed YAML value is a mapping."""

    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return value


def ensure_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    """Normalize a YAML list-like value to a tuple."""

    if value is None:
        return ()
    if not isinstance(value, list | tuple):
        raise ValueError(f"{field_name} must be a list")
    return tuple(value)


def clean_none_values(value: dict[str, Any]) -> dict[str, Any]:
    """Drop keys whose value is ``None``."""

    return {key: child for key, child in value.items() if child is not None}


def validate_choice(value: str, choices: tuple[str, ...], field_name: str) -> str:
    """Validate that a string belongs to a finite set."""

    if value not in choices:
        raise ValueError(f"{field_name} must be one of {choices}: {value}")
    return value


def load_yaml(path: Path | str) -> Any:
    """Load a YAML file and return the parsed value."""

    yaml_path = Path(path)
    with yaml_path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_yaml_mapping(path: Path | str) -> dict[str, Any]:
    """Load a YAML file whose root must be a mapping."""

    yaml_path = Path(path)
    data = load_yaml(yaml_path) or {}
    if not isinstance(data, Mapping):
        raise ValueError(f"YAML root must be a mapping: {yaml_path}")
    return dict(data)


def dump_yaml(path: Path | str, data: Mapping[str, Any]) -> None:
    """Write a mapping as YAML."""

    yaml_path = Path(path)
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path.write_text(
        yaml.safe_dump(dict(data), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def write_yaml_snapshots(
    *,
    output_dir: Path,
    snapshots: Mapping[str, Mapping[str, Any]],
) -> None:
    """Write multiple YAML snapshots under an artifact directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, data in snapshots.items():
        dump_yaml(output_dir / filename, data)


__all__ = [
    "clean_none_values",
    "dump_yaml",
    "ensure_mapping",
    "ensure_tuple",
    "load_yaml",
    "load_yaml_mapping",
    "resolve_project_path",
    "validate_choice",
    "write_yaml_snapshots",
]
