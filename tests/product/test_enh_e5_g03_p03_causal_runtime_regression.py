"""Focused ENH-E5 G03 P03 causal runtime-preservation checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ariadne.capabilities.causal.workflow import CausalPlanner
from ariadne.product.domain.enums import ExecutionOperation
from ariadne.product.domain.execution import Execution


REPOSITORY = Path(__file__).parents[2]


def _execution(operation: ExecutionOperation) -> Execution:
    needs_graph = operation is not ExecutionOperation.DISCOVERY
    needs_result = operation in {
        ExecutionOperation.ESTIMATION,
        ExecutionOperation.REFUTATION,
        ExecutionOperation.SENSITIVITY,
    }
    return Execution(
        project_id="project", dataset_version_id="dataset", operation=operation,
        input_graph_version_id="graph" if needs_graph else None,
        input_result_id="result" if needs_result else None,
        algorithm_or_estimator="test", snapshot_hash=f"snapshot-{operation.value}",
    )


def test_causal_runtime_operation_stage_and_input_matrix_are_preserved() -> None:
    expected = {
        ExecutionOperation.DISCOVERY: ("causal.discovery.v1", {"dataset_path", "output_dir"}),
        ExecutionOperation.IDENTIFICATION: ("causal.identification.v1", {"dataset_path", "output_dir", "graph_path"}),
        ExecutionOperation.ESTIMATION: ("causal.estimation.v2", {"dataset_path", "output_dir", "graph_path", "upstream_result", "upstream_execution"}),
        ExecutionOperation.REFUTATION: ("causal.refutation.v1", {"dataset_path", "output_dir", "graph_path", "upstream_result", "upstream_execution"}),
        ExecutionOperation.SENSITIVITY: ("causal.sensitivity.v1", {"dataset_path", "output_dir", "graph_path", "upstream_result", "upstream_execution"}),
    }

    planner = CausalPlanner()
    for operation, (stage_type, input_names) in expected.items():
        plan = planner.build_for_execution(_execution(operation))
        assert len(plan.stages) == 1
        assert ".".join((
            plan.stages[0].stage_type.namespace,
            plan.stages[0].stage_type.name,
            f"v{plan.stages[0].stage_type.version}",
        )) == stage_type
        assert set(plan.stages[0].input_contract) == input_names


def test_navigation_route_change_has_no_execution_revision_metadata() -> None:
    navigation = REPOSITORY / "frontend" / "navigation_state.js"
    app_navigation_shell = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8").split(
        "async function loadProjects", 1
    )[0]
    script = f"""
const fs = require('fs');
const vm = require('vm');
vm.runInThisContext(fs.readFileSync({str(navigation)!r}, 'utf8'));
const catalog = {{families: [{{slug: 'causal', default_stage_id: 'setup', stages: [
  {{slug: 'setup'}}, {{slug: 'effects'}}, {{slug: 'sensitivity'}},
]}}]}};
const before = AnalysisNavigation.navigationContext(catalog, 'project', 'causal', 'setup');
const after = AnalysisNavigation.navigationContext(catalog, 'project', 'causal', 'effects');
if (before.projectId !== 'project' || before.familySlug !== 'causal' || before.stageSlug !== 'setup' || before.resource !== null) process.exit(1);
if (after.projectId !== 'project' || after.familySlug !== 'causal' || after.stageSlug !== 'effects' || after.resource !== null) process.exit(1);
"""

    subprocess.run(["node", "-e", script], check=True)
    assert "base_execution_id" not in navigation.read_text(encoding="utf-8")
    assert "revision_kind" not in navigation.read_text(encoding="utf-8")
    assert "change_reason" not in navigation.read_text(encoding="utf-8")
    assert "base_execution_id" not in app_navigation_shell
    assert "revision_kind" not in app_navigation_shell
    assert "change_reason" not in app_navigation_shell


def test_no_prohibited_causal_runtime_dependency_is_declared() -> None:
    project_config = (REPOSITORY / "pyproject.toml").read_text(encoding="utf-8").lower()
    causal_source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (REPOSITORY / "src" / "ariadne" / "capabilities" / "causal").glob("*.py")
    )

    for dependency in ("lightgbm", "dowhy", "econml"):
        assert dependency not in project_config
        assert f"import {dependency}" not in causal_source
        assert f"from {dependency}" not in causal_source
