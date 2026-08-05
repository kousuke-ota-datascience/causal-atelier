"""Path utilities that do not depend on a stage implementation."""

from __future__ import annotations

from pathlib import Path


def resolve_project_path(path: Path | str, project_root: Path) -> Path:
    """Resolve an absolute or project-relative path."""

    value = Path(path)
    return value if value.is_absolute() else project_root / value


def ensure_directory(path: Path | str) -> Path:
    """Create a directory if needed and return it as a path."""

    value = Path(path)
    value.mkdir(parents=True, exist_ok=True)
    return value


def relative_to_project(path: Path | str, project_root: Path) -> str:
    """Return a project-relative representation when possible."""

    value = Path(path)
    try:
        return str(value.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(value)


__all__ = ["ensure_directory", "relative_to_project", "resolve_project_path"]
