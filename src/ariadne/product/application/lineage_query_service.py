"""LineageQueryService – traverse lineage from a Result upward."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.errors import EntityNotFound


@dataclass(frozen=True)
class LineageNode:
    node_type: str
    entity_id: str
    label: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LineageView:
    nodes: list[LineageNode]
    edges: list[tuple[str, str]]  # (from_id, to_id)


class LineageQueryService:
    def __init__(self, uow_factory: Any) -> None:
        self._uow_factory = uow_factory

    def get_lineage(self, result_id: str) -> LineageView:
        with self._uow_factory() as uow:
            result = uow.results.get(result_id)
            if result is None:
                raise EntityNotFound("Result", result_id)

            nodes: list[LineageNode] = []
            edges: list[tuple[str, str]] = []
            visited: set[str] = set()
            edge_set: set[tuple[str, str]] = set()

            def add_node(node: LineageNode) -> None:
                if node.entity_id not in visited:
                    visited.add(node.entity_id)
                    nodes.append(node)

            def add_edge(source: str, target: str) -> None:
                edge = (source, target)
                if edge not in edge_set:
                    edge_set.add(edge)
                    edges.append(edge)

            def add_artifacts(execution_id: str, target_result_id: str) -> None:
                artifacts = {
                    artifact.artifact_id: artifact
                    for artifact in (
                        uow.artifacts.list_by_execution(execution_id)
                        + uow.artifacts.list_by_result(target_result_id)
                    )
                }
                for artifact in artifacts.values():
                    add_node(LineageNode("Artifact", artifact.artifact_id, artifact.artifact_type.value, {
                        "object_key": artifact.object_key,
                        "content_hash": artifact.content_hash,
                    }))
                    add_edge(target_result_id, artifact.artifact_id)

            def add_annotations(*, target_result_id: str | None = None,
                                graph_version_id: str | None = None) -> None:
                annotations = uow.annotations.list_by_target(
                    result_id=target_result_id, graph_version_id=graph_version_id
                )
                target_id = target_result_id or graph_version_id
                if target_id is None:
                    return
                for annotation in annotations:
                    add_node(LineageNode("Annotation", annotation.annotation_id, "Annotation", {
                        "statement": annotation.statement[:80],
                        "rationale": annotation.rationale,
                    }))
                    add_edge(target_id, annotation.annotation_id)

            def add_dataset(dataset_version_id: str, execution_id: str) -> None:
                dataset = uow.dataset_versions.get(dataset_version_id)
                if dataset is None:
                    return
                add_node(LineageNode("DatasetVersion", dataset.dataset_version_id, dataset.name, {
                    "dataset_key": dataset.dataset_key,
                    "version_label": dataset.version_label,
                    "content_hash": dataset.content_hash,
                }))
                add_edge(dataset.dataset_version_id, execution_id)
                source_artifact = uow.artifacts.get(dataset.source_artifact_id)
                if source_artifact:
                    add_node(LineageNode("Artifact", source_artifact.artifact_id, "DATASET_FILE", {
                        "object_key": source_artifact.object_key,
                        "content_hash": source_artifact.content_hash,
                    }))
                    add_edge(source_artifact.artifact_id, dataset.dataset_version_id)

            add_node(LineageNode("Result", result.result_id, f"Result ({result.result_type.value})", {
                "scientific_status": result.scientific_status.value,
            }))
            execution = uow.executions.get(result.execution_id)
            if execution:
                project = uow.projects.get(execution.project_id)
                if project:
                    add_node(LineageNode("Project", project.project_id, project.name, {
                        "topic": project.topic,
                        "objective": project.objective,
                    }))
                    add_edge(project.project_id, execution.execution_id)
                add_node(LineageNode("Execution", execution.execution_id, f"Execution ({execution.operation.value})", {
                    "algorithm_or_estimator": execution.algorithm_or_estimator,
                    "parameters": execution.parameter_json,
                    "objective_snapshot": execution.objective_snapshot,
                    "rationale_snapshot": execution.rationale_snapshot,
                    "code_version": execution.code_version,
                    "status": execution.status.value,
                }))
                add_edge(execution.execution_id, result.result_id)
                add_dataset(execution.dataset_version_id, execution.execution_id)
                add_artifacts(execution.execution_id, result.result_id)

                if execution.input_graph_version_id:
                    graph = uow.graph_versions.get(execution.input_graph_version_id)
                    if graph:
                        add_node(LineageNode("GraphVersion", graph.graph_version_id, graph.name, {
                            "graph_type": graph.graph_type.value,
                            "content_hash": graph.content_hash,
                            "status": graph.status.value,
                        }))
                        add_edge(graph.graph_version_id, execution.execution_id)
                        add_annotations(graph_version_id=graph.graph_version_id)
                        discovery_result = uow.results.get(graph.source_result_id)
                        if discovery_result:
                            add_node(LineageNode("Result", discovery_result.result_id, "Discovery Result", {
                                "scientific_status": discovery_result.scientific_status.value,
                            }))
                            add_edge(discovery_result.result_id, graph.graph_version_id)
                            discovery_execution = uow.executions.get(discovery_result.execution_id)
                            if discovery_execution:
                                add_node(LineageNode("Execution", discovery_execution.execution_id,
                                                    "Discovery Execution", {
                                    "algorithm_or_estimator": discovery_execution.algorithm_or_estimator,
                                    "parameters": discovery_execution.parameter_json,
                                    "objective_snapshot": discovery_execution.objective_snapshot,
                                    "rationale_snapshot": discovery_execution.rationale_snapshot,
                                    "code_version": discovery_execution.code_version,
                                    "status": discovery_execution.status.value,
                                }))
                                add_edge(discovery_execution.execution_id, discovery_result.result_id)
                                add_dataset(discovery_execution.dataset_version_id,
                                            discovery_execution.execution_id)
                                add_artifacts(discovery_execution.execution_id,
                                              discovery_result.result_id)
                            add_annotations(target_result_id=discovery_result.result_id)
            add_annotations(target_result_id=result.result_id)

        return LineageView(nodes=nodes, edges=edges)
