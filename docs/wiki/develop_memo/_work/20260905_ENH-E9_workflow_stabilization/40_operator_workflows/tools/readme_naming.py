#!/usr/bin/env python3
"""Deterministic nested README naming for the Agentic Enhancement Workflow Template."""
from __future__ import annotations

from pathlib import Path
import re

README_BASENAME = "README.md"


def _tokenize_component(component: str) -> str:
    """Map one directory component to a stable PATH_ID token.

    Numbered workflow directories collapse to their numeric namespace:
      00_enhance_background -> 00
      20_implementation_reports -> 20
      40_operator_workflows -> 40

    Other components retain their semantic identity after filesystem-safe
    normalization. Runtime identifiers such as G01 and Trial01 therefore stay
    unchanged.
    """
    m = re.match(r"^(\d{2})_(.+)$", component)
    if m:
        return m.group(1)
    token = re.sub(r"[^A-Za-z0-9.-]+", "_", component).strip("_")
    if not token:
        raise ValueError(f"directory component has no usable README token: {component!r}")
    return token


def readme_path_id(template_root: Path, directory: Path) -> str:
    root = template_root.resolve()
    directory = directory.resolve()
    try:
        rel = directory.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"directory is outside template root: {directory}") from exc
    if rel == Path("."):
        return ""
    return "_".join(_tokenize_component(part) for part in rel.parts)


def readme_filename_for_directory(template_root: Path, directory: Path) -> str:
    """Return the canonical README filename for a directory.

    The template root alone keeps README.md. Every nested directory gets a
    path-derived postfix filename.
    """
    path_id = readme_path_id(template_root, directory)
    return README_BASENAME if not path_id else f"README_{path_id}.md"


def expected_readme_path(template_root: Path, directory: Path) -> Path:
    return directory / readme_filename_for_directory(template_root, directory)


def nested_readme_migration_map(template_root: Path) -> dict[Path, Path]:
    """Return old->new paths for every nested README.md currently present."""
    root = template_root.resolve()
    mapping: dict[Path, Path] = {}
    targets: dict[Path, Path] = {}
    for old in sorted(root.rglob(README_BASENAME)):
        if old.parent == root:
            continue
        new = expected_readme_path(root, old.parent)
        if new in targets and targets[new] != old:
            raise ValueError(f"README naming collision: {targets[new]} and {old} -> {new}")
        targets[new] = old
        mapping[old] = new
    return mapping


def validate_readme_names(template_root: Path) -> list[str]:
    """Return naming violations for README-like Markdown files."""
    root = template_root.resolve()
    errors: list[str] = []
    root_readme = root / README_BASENAME
    if not root_readme.is_file():
        errors.append(f"root README missing: {root_readme}")

    for stale in sorted(root.rglob(README_BASENAME)):
        if stale.parent != root:
            errors.append(f"nested unqualified README is forbidden: {stale.relative_to(root)}")

    seen_targets: dict[str, Path] = {}
    for path in sorted(root.rglob("README_*.md")):
        if path.parent == root:
            # Root-level README_* documents are not local index READMEs and are
            # outside this naming rule.
            continue
        expected = readme_filename_for_directory(root, path.parent)
        if path.name != expected:
            errors.append(
                f"non-canonical nested README name: {path.relative_to(root)}; expected {expected}"
            )
        rel = path.relative_to(root).as_posix()
        if expected in seen_targets and seen_targets[expected] != path:
            errors.append(
                f"README filename collision: {seen_targets[expected].relative_to(root)} and {rel}"
            )
        else:
            seen_targets[expected] = path
    return errors
