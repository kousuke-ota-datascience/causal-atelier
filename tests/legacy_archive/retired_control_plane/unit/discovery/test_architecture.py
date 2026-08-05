"""Architecture enforcement tests for causal discovery."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).parents[3] / "src" / "ariadne"


def _get_imports(path: Path) -> list[str]:
    """Return all top-level imported module names from a Python source file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def _all_imports_in_package(package_dir: Path) -> dict[str, list[str]]:
    """Return {relative_path: [imported_modules]} for all .py files under a dir."""
    result = {}
    for py_file in package_dir.rglob("*.py"):
        rel = str(py_file.relative_to(SRC))
        result[rel] = _get_imports(py_file)
    return result


class TestApplicationLayerDoesNotImportCLI:
    """Application layer must not depend on interfaces.cli."""

    def test_discovery_service_does_not_import_cli(self) -> None:
        app_dir = SRC / "application" / "discovery"
        for py_file in app_dir.rglob("*.py"):
            imports = _get_imports(py_file)
            cli_imports = [m for m in imports if "interfaces.cli" in m]
            assert not cli_imports, (
                f"{py_file.name} imports from interfaces.cli: {cli_imports}"
            )

    def test_pipeline_discovery_runner_does_not_import_cli(self) -> None:
        runner_file = SRC / "application" / "pipeline" / "discovery.py"
        imports = _get_imports(runner_file)
        cli_imports = [m for m in imports if "interfaces.cli" in m]
        assert not cli_imports, (
            f"DiscoveryStageRunner imports from interfaces.cli: {cli_imports}"
        )


class TestCLIDoesNotImportInfrastructure:
    """CLI thin adapter must not import heavy infrastructure modules directly."""

    def test_cli_discovery_does_not_import_pandas(self) -> None:
        cli_file = SRC / "interfaces" / "cli" / "discovery.py"
        imports = _get_imports(cli_file)
        # pandas import at module level is forbidden; inside functions is allowed
        source = cli_file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        top_level_pandas = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "pandas":
                        top_level_pandas.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and "pandas" in node.module:
                    top_level_pandas.append(node.module)
        assert not top_level_pandas, (
            "interfaces/cli/discovery.py has top-level pandas import"
        )

    def test_cli_discovery_does_not_import_logicaltabledataloader(self) -> None:
        cli_file = SRC / "interfaces" / "cli" / "discovery.py"
        imports = _get_imports(cli_file)
        assert not any("LogicalTableDataLoader" in m or "etl.registry" in m for m in imports), (
            "interfaces/cli/discovery.py imports LogicalTableDataLoader"
        )

    def test_cli_discovery_does_not_import_completejourney_preprocessor(self) -> None:
        cli_file = SRC / "interfaces" / "cli" / "discovery.py"
        imports = _get_imports(cli_file)
        assert not any("CompleteJourneyPreprocessor" in m or "preprocessing.discovery.builder" in m for m in imports), (
            "interfaces/cli/discovery.py imports CompleteJourneyPreprocessor"
        )

    def test_cli_discovery_does_not_import_causal_discovery_reporter(self) -> None:
        cli_file = SRC / "interfaces" / "cli" / "discovery.py"
        imports = _get_imports(cli_file)
        assert not any("CausalDiscoveryReporter" in m or "discovery.reporting" in m for m in imports), (
            "interfaces/cli/discovery.py imports CausalDiscoveryReporter"
        )
