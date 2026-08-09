"""G07 P03 contracts for standalone scientific CLI lifecycle boundaries."""

from __future__ import annotations

import ast
import tomllib
from collections import deque
from dataclasses import fields
from pathlib import Path

from ariadne.interfaces.cli.manifest import CliManifest


REPOSITORY = Path(__file__).parents[2]
SOURCE_ROOT = REPOSITORY / "src"
ARIADNE_ROOT = SOURCE_ROOT / "ariadne"
LOW_LEVEL_UTILITY = {
    "ariadne-discover",
    "ariadne-estimate",
    "ariadne-identify",
    "ariadne-refute",
    "ariadne-sensitivity",
}
FORBIDDEN_PREFIXES = ("ariadne.legacy", "ariadne.product.persistence")
RESERVED_PERSISTENT_IDENTITIES = {
    "execution_id", "stage_execution_id", "result_id", "artifact_id",
}


def _module_name(path: Path) -> str:
    parts = path.relative_to(SOURCE_ROOT).with_suffix("").parts
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def _modules() -> dict[str, Path]:
    return {_module_name(path): path for path in ARIADNE_ROOT.rglob("*.py")}


def _from_imports(module: str, node: ast.ImportFrom) -> set[str]:
    package = module.rsplit(".", 1)[0] if "." in module else ""
    if node.level:
        parts = package.split(".") if package else []
        parts = parts[: len(parts) - node.level + 1]
        if node.module:
            parts.extend(node.module.split("."))
        base = ".".join(part for part in parts if part)
    else:
        base = node.module or ""
    if not base.startswith("ariadne"):
        return set()
    return {base, *(f"{base}.{item.name}" for item in node.names if item.name != "*")}


def _imports() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for module, path in _modules().items():
        dependencies: set[str] = set()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                dependencies.update(item.name for item in node.names if item.name.startswith("ariadne"))
            elif isinstance(node, ast.ImportFrom):
                dependencies.update(_from_imports(module, node))
        graph[module] = dependencies
    return graph


def _forbidden_path(roots: tuple[str, ...]) -> list[str] | None:
    modules, graph = _modules(), _imports()
    queue: deque[list[str]] = deque([[root] for root in roots])
    visited: set[str] = set()
    while queue:
        path = queue.popleft()
        current = path[-1]
        if current in visited:
            continue
        visited.add(current)
        if current.startswith(FORBIDDEN_PREFIXES):
            return path
        for dependency in sorted(graph.get(current, set())):
            if dependency in modules:
                queue.append([*path, dependency])
    return None


def test_all_analysis_cli_scripts_are_explicitly_low_level_utilities() -> None:
    pyproject = tomllib.loads((REPOSITORY / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    analysis_scripts = {
        name: target
        for name, target in scripts.items()
        if target.startswith("ariadne.interfaces.cli.")
    }
    assert set(analysis_scripts) == LOW_LEVEL_UTILITY
    assert all(target.endswith(":main") for target in analysis_scripts.values())


def test_low_level_cli_has_no_legacy_or_product_persistence_reachability() -> None:
    pyproject = tomllib.loads((REPOSITORY / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    roots = tuple(scripts[name].split(":", 1)[0] for name in sorted(LOW_LEVEL_UTILITY))
    assert _forbidden_path(roots) is None


def test_portable_cli_manifest_cannot_claim_product_persistent_identity() -> None:
    manifest_fields = {field.name for field in fields(CliManifest)}
    assert RESERVED_PERSISTENT_IDENTITIES.isdisjoint(manifest_fields)
