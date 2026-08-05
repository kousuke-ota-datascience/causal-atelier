"""ComparisonQueryService – generate a Comparison Projection from Results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.errors import EntityNotFound, InvalidAnalysisSpec


@dataclass(frozen=True)
class ComparisonView:
    common_conditions: dict[str, Any]
    changed_conditions: list[dict[str, Any]]
    result_differences: list[dict[str, Any]]
    warnings: list[str]
    lineage_summary: dict[str, Any]


class ComparisonQueryService:
    def __init__(self, uow_factory: Any) -> None:
        self._uow_factory = uow_factory

    def compare(self, result_ids: list[str]) -> ComparisonView:
        if len(result_ids) < 2:
            raise InvalidAnalysisSpec("At least 2 result_ids are required for comparison")

        with self._uow_factory() as uow:
            results = uow.results.get_many(result_ids)
            if len(results) != len(result_ids):
                missing = set(result_ids) - {r.result_id for r in results}
                raise EntityNotFound("Result", next(iter(missing)))

            # Verify same project and operation
            execution_ids = [r.execution_id for r in results]
            executions = [uow.executions.get(eid) for eid in execution_ids]
            if any(e is None for e in executions):
                raise EntityNotFound("Execution", "one or more")

            project_ids = {e.project_id for e in executions if e}  # type: ignore[union-attr]
            if len(project_ids) > 1:
                raise InvalidAnalysisSpec("All results must belong to the same project")

            operations = {e.operation for e in executions if e}  # type: ignore[union-attr]
            if len(operations) > 1:
                raise InvalidAnalysisSpec("All results must have the same operation type")

        return _build_comparison(results, executions)  # type: ignore[arg-type]


def _build_comparison(results: list[Any], executions: list[Any]) -> ComparisonView:
    """Build a comparison projection from results and their executions."""
    # Flatten execution snapshots to field-level for diff
    snapshot_fields: list[dict[str, Any]] = []
    for exec_ in executions:
        snap = {
            "algorithm_or_estimator": exec_.algorithm_or_estimator,
            "parameter_json": exec_.parameter_json,
            "random_seed": exec_.random_seed,
            "analysis_spec_json": exec_.analysis_spec_json,
            "dataset_version_id": exec_.dataset_version_id,
            "input_graph_version_id": exec_.input_graph_version_id,
        }
        snapshot_fields.append(snap)

    # Identify common vs changed conditions
    all_keys = set()
    for snap in snapshot_fields:
        all_keys.update(snap.keys())

    common: dict[str, Any] = {}
    changed: list[dict[str, Any]] = []

    for key in sorted(all_keys):
        values = [snap.get(key) for snap in snapshot_fields]
        if all(v == values[0] for v in values):
            common[key] = values[0]
        else:
            changed.append({"field": key, "values": values})

    # Build result differences
    result_diffs: list[dict[str, Any]] = []
    for r in results:
        result_diffs.append({
            "result_id": r.result_id,
            "scientific_status": r.scientific_status.value,
            "summary": r.summary_json,
            "warnings": r.warning_json,
        })

    lineage: dict[str, Any] = {
        "execution_ids": [e.execution_id for e in executions],
        "result_ids": [r.result_id for r in results],
    }

    return ComparisonView(
        common_conditions=common,
        changed_conditions=changed,
        result_differences=result_diffs,
        warnings=[],
        lineage_summary=lineage,
    )
