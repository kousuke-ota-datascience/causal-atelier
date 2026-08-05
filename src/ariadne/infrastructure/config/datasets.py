from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml


class PlaceholderDict(dict[str, str]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    search_from = current if current.is_dir() else current.parent

    for path in (search_from, *search_from.parents):
        if (path / "pyproject.toml").exists():
            return path

    raise RuntimeError(f"pyproject.toml was not found from {search_from}")


def resolve_placeholders(value: Any, placeholders: Mapping[str, str]) -> Any:
    if isinstance(value, str):
        return value.format_map(PlaceholderDict(placeholders))

    if isinstance(value, Mapping):
        return {
            key: resolve_placeholders(child, placeholders)
            for key, child in value.items()
        }

    if isinstance(value, list):
        return [resolve_placeholders(child, placeholders) for child in value]

    return value


def load_dataset_definition(
    path: Path,
    project_root: Path,
    extra_placeholders: Mapping[str, str] | None = None,
) -> Mapping[str, Any]:
    with path.open(encoding="utf-8") as file:
        dataset_definition = yaml.safe_load(file) or {}

    placeholders = {
        "path_sys_base": str(project_root),
        "path_sysy_base": str(project_root),
    }
    if extra_placeholders is not None:
        placeholders.update(extra_placeholders)

    return resolve_placeholders(dataset_definition, placeholders)
