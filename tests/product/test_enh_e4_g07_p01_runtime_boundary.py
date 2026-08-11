"""G07 P01 contracts for the Product/legacy runtime boundary.

These checks deliberately inspect the repository import graph rather than only
the direct imports in Product roots.  A legacy dependency hidden behind a
Product adapter must fail the same way as a direct dependency.
"""

from __future__ import annotations

import ast
from collections import deque
from pathlib import Path

import tomllib


REPOSITORY = Path(__file__).parents[2]
SOURCE_ROOT = REPOSITORY / "src"
ARIADNE_ROOT = SOURCE_ROOT / "ariadne"
LEGACY_PREFIX = "ariadne.legacy"


def _module_name(path: Path) -> str:
    relative = path.relative_to(SOURCE_ROOT).with_suffix("")
    parts = relative.parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _all_modules() -> dict[str, Path]:
    return {
        _module_name(path): path
        for path in ARIADNE_ROOT.rglob("*.py")
    }


def _resolve_from_import(module: str, node: ast.ImportFrom) -> set[str]:
    """Return repository module candidates referenced by one ``from`` import."""
    package = module.rsplit(".", 1)[0] if "." in module else ""
    if node.level:
        base_parts = package.split(".") if package else []
        base_parts = base_parts[: len(base_parts) - node.level + 1]
        if node.module:
            base_parts.extend(node.module.split("."))
        base = ".".join(part for part in base_parts if part)
    else:
        base = node.module or ""
    if not base.startswith("ariadne"):
        return set()
    values = {base}
    values.update(f"{base}.{alias.name}" for alias in node.names if alias.name != "*")
    return values


def _imports_by_module() -> dict[str, set[str]]:
    imports: dict[str, set[str]] = {}
    for module, path in _all_modules().items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        dependencies: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                dependencies.update(alias.name for alias in node.names if alias.name.startswith("ariadne"))
            elif isinstance(node, ast.ImportFrom):
                dependencies.update(_resolve_from_import(module, node))
        imports[module] = dependencies
    return imports


def _legacy_path_from(roots: tuple[str, ...]) -> list[str] | None:
    modules = _all_modules()
    imports = _imports_by_module()
    pending: deque[list[str]] = deque([[root] for root in roots])
    visited: set[str] = set()
    while pending:
        path = pending.popleft()
        current = path[-1]
        if current in visited:
            continue
        visited.add(current)
        if current == LEGACY_PREFIX or current.startswith(f"{LEGACY_PREFIX}."):
            return path
        for dependency in sorted(imports.get(current, set())):
            if dependency in modules:
                pending.append([*path, dependency])
    return None


def _package_roots(*packages: str) -> tuple[str, ...]:
    """Expand a source package so its non-imported modules remain guarded."""
    return tuple(
        module
        for module in _all_modules()
        if any(module == package or module.startswith(f"{package}.") for package in packages)
    )


def test_canonical_product_runtime_roots_cannot_reach_legacy() -> None:
    roots = _package_roots(
        "ariadne.product",
        "ariadne.interfaces.web_api",
        "ariadne.interfaces.worker",
    )
    assert _legacy_path_from(roots) is None


def test_retained_shared_science_cannot_reach_legacy_orchestration() -> None:
    roots = _package_roots(
        "ariadne.causal",
        "ariadne.preprocessing",
        "ariadne.shared",
        "ariadne.scientific",
    )
    assert _legacy_path_from(roots) is None


def test_product_deployment_surfaces_use_only_canonical_runtime_roots() -> None:
    pyproject = tomllib.loads((REPOSITORY / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    assert scripts["ariadne-api"] == "ariadne.interfaces.web_api.app:main"
    assert scripts["ariadne-worker"] == "ariadne.interfaces.worker.runner:main"
    assert not any(value.startswith(LEGACY_PREFIX) for value in scripts.values())
    assert "src/ariadne/legacy/**" in pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["exclude"]

    dockerignore = (REPOSITORY / ".dockerignore").read_text(encoding="utf-8").splitlines()
    dockerfile = (REPOSITORY / "Dockerfile").read_text(encoding="utf-8")
    compose = (REPOSITORY / "compose.yaml").read_text(encoding="utf-8")
    assert "src/ariadne/legacy" in dockerignore
    assert 'CMD ["uvicorn", "ariadne.interfaces.web_api.app:app"' in dockerfile
    assert 'command: ["ariadne-worker"]' in compose
    assert LEGACY_PREFIX not in dockerfile
    assert LEGACY_PREFIX not in compose
