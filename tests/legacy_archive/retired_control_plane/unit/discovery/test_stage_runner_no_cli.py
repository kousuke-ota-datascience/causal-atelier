"""Tests that DiscoveryStageRunner does not import from interfaces.cli."""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).parents[3] / "src" / "ariadne"


def _get_all_string_literals(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]


class TestStageRunnerNoCLIDependency:
    def test_stage_runner_source_does_not_reference_cli_main(self) -> None:
        runner_path = SRC / "application" / "pipeline" / "discovery.py"
        source = runner_path.read_text(encoding="utf-8")
        assert "interfaces.cli.discovery" not in source, (
            "DiscoveryStageRunner must not import from interfaces.cli.discovery"
        )
        assert "discovery_main" not in source, (
            "DiscoveryStageRunner must not alias or call discovery_main"
        )

    def test_stage_runner_uses_application_service(self) -> None:
        runner_path = SRC / "application" / "pipeline" / "discovery.py"
        source = runner_path.read_text(encoding="utf-8")
        assert "build_discovery_application_service" in source or "DiscoveryApplicationService" in source, (
            "DiscoveryStageRunner should use the Application Service"
        )

    def test_stage_runner_imports_from_application_layer_only(self) -> None:
        runner_path = SRC / "application" / "pipeline" / "discovery.py"
        source = runner_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("ariadne.interfaces.cli"), (
                    f"DiscoveryStageRunner imports from CLI layer: {node.module}"
                )
