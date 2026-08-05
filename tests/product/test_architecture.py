from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).parents[2] / "src" / "ariadne"
REPOSITORY = ROOT.parents[1]


def imports_under(directory: Path) -> list[str]:
    values=[]
    for path in directory.rglob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                values.append(node.module)
            elif isinstance(node, ast.Import):
                values.extend(alias.name for alias in node.names)
    return values


def test_product_and_new_interfaces_do_not_import_legacy_control_plane():
    for directory in (ROOT / "product", ROOT / "interfaces" / "web_api"):
        imports=imports_under(directory)
        assert not any(name.startswith("ariadne.legacy") for name in imports)
        assert not any(name in {"ariadne.application", "ariadne.domain", "ariadne.interfaces.api"} or
                       name.startswith(("ariadne.application.", "ariadne.domain.", "ariadne.interfaces.api.")) for name in imports)


def test_scientific_has_no_repository_web_or_orm_dependency():
    imports=imports_under(ROOT / "scientific")
    forbidden=("ariadne.product.persistence", "ariadne.product.application", "ariadne.interfaces.web_api")
    assert not any(name.startswith(forbidden) for name in imports)


def test_product_runtime_excludes_legacy_control_plane():
    pyproject = (REPOSITORY / "pyproject.toml").read_text(encoding="utf-8")
    compose = (REPOSITORY / "compose.yaml").read_text(encoding="utf-8")
    dockerignore = (REPOSITORY / ".dockerignore").read_text(encoding="utf-8")
    assert 'src/ariadne/legacy/**' in pyproject
    assert "src/ariadne/legacy" in dockerignore
    assert not any(alias in pyproject for alias in (
        "ariadne-discovery =", "ariadne-inference =", "ariadne-pipeline =",
    ))
    assert not any(value in compose for value in (
        "ariadne.legacy", "alembic.ini upgrade", "ARIADNE_DATABASE_URL", "mlflow",
    ))
