"""Read-only Product queries used by the HTTP interface."""

from __future__ import annotations

from typing import Any

from ariadne.product.domain.errors import EntityNotFound, ProjectBoundaryViolation


class ProductQueryService:
    def __init__(self, uow_factory: Any) -> None:
        self._uow_factory = uow_factory

    def list_executions(self, project_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            if uow.projects.get(project_id) is None:
                raise EntityNotFound("Project", project_id)
            return uow.executions.list_by_project(project_id)

    def list_results(self, execution_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            if uow.executions.get(execution_id) is None:
                raise EntityNotFound("Execution", execution_id)
            return uow.results.list_by_execution(execution_id)

    def get_result(self, result_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            result = uow.results.get(result_id)
            if result is None:
                raise EntityNotFound("Result", result_id)
            return result

    def result_artifact_ids(self, result_id: str) -> list[str]:
        with self._uow_factory() as uow:
            if uow.results.get(result_id) is None:
                raise EntityNotFound("Result", result_id)
            return [artifact.artifact_id for artifact in uow.artifacts.list_by_result(result_id)]

    def result_project_id(self, result_id: str) -> str:
        with self._uow_factory() as uow:
            result = uow.results.get(result_id)
            if result is None:
                raise EntityNotFound("Result", result_id)
            execution = uow.executions.get(result.execution_id)
            if execution is None:
                raise EntityNotFound("Execution", result.execution_id)
            return execution.project_id

    def get_graph_version(self, graph_version_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            graph = uow.graph_versions.get(graph_version_id)
            if graph is None:
                raise EntityNotFound("GraphVersion", graph_version_id)
            return graph

    def list_graph_versions(self, project_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            if uow.projects.get(project_id) is None:
                raise EntityNotFound("Project", project_id)
            return uow.graph_versions.list_by_project(project_id)

    def get_annotation(self, annotation_id: str):  # type: ignore[no-untyped-def]
        with self._uow_factory() as uow:
            annotation = uow.annotations.get(annotation_id)
            if annotation is None:
                raise EntityNotFound("Annotation", annotation_id)
            return annotation

    def export_result(self, result_id: str) -> dict[str, Any]:
        with self._uow_factory() as uow:
            result = uow.results.get(result_id)
            if result is None:
                raise EntityNotFound("Result", result_id)
            execution = uow.executions.get(result.execution_id)
            if execution is None:
                raise EntityNotFound("Execution", result.execution_id)
            dataset = uow.dataset_versions.get(execution.dataset_version_id)
            if dataset is None:
                raise EntityNotFound("DatasetVersion", execution.dataset_version_id)
            graph = (
                uow.graph_versions.get(execution.input_graph_version_id)
                if execution.input_graph_version_id else None
            )
            artifacts = uow.artifacts.list_by_result(result_id)
            return {
                "manifest_version": "1.0",
                "result": {
                    "result_id": result.result_id,
                    "result_type": result.result_type.value,
                    "scientific_status": result.scientific_status.value,
                    "summary": result.summary_json,
                    "diagnostics": result.diagnostics_json,
                    "warnings": result.warning_json,
                },
                "execution": {
                    "execution_id": execution.execution_id,
                    "snapshot_hash": execution.snapshot_hash,
                    "snapshot_schema_version": execution.snapshot_schema_version,
                    "input_result_id": execution.input_result_id,
                    "operation": execution.operation.value,
                    "analysis_spec": execution.analysis_spec_json,
                    "algorithm_or_estimator": execution.algorithm_or_estimator,
                    "parameters": execution.parameter_json,
                    "random_seed": execution.random_seed,
                    "code_version": execution.code_version,
                    "runtime_versions": execution.runtime_version_json,
                },
                "dataset": {"dataset_version_id": dataset.dataset_version_id, "content_hash": dataset.content_hash},
                "graph": None if graph is None else {
                    "graph_version_id": graph.graph_version_id,
                    "content_hash": graph.content_hash,
                    "graph_origin": graph.graph_origin.value,
                    "designated_outcome_node": graph.designated_outcome_node,
                    "provenance": graph.provenance_json,
                },
                "artifacts": [
                    {"artifact_id": item.artifact_id, "content_hash": item.content_hash, "artifact_type": item.artifact_type.value}
                    for item in artifacts
                ],
            }
