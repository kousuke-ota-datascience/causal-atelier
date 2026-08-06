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

            processing: set[str] = set()

            def add_result_chain(current: Any, depth: int = 0) -> None:
                if depth > 32:
                    raise ValueError("Lineage maximum depth exceeded")
                if current.result_id in processing:
                    raise ValueError("Lineage cycle detected")
                if current.result_id in visited:
                    return
                processing.add(current.result_id)
                add_node(LineageNode("Result", current.result_id,
                                     f"Result ({current.result_type.value})", {
                    "scientific_status": current.scientific_status.value,
                }))
                generating = uow.executions.get(current.execution_id)
                if generating is None:
                    processing.remove(current.result_id); return
                if generating.project_id != execution_project_id:
                    raise ValueError("Lineage crosses a Project boundary")
                project = uow.projects.get(generating.project_id)
                if project:
                    add_node(LineageNode("Project", project.project_id, project.name, {
                        "topic": project.topic, "objective": project.objective,
                    }))
                    add_edge(project.project_id, generating.execution_id)
                add_node(LineageNode("Execution", generating.execution_id,
                                     f"Execution ({generating.operation.value})", {
                    "algorithm_or_estimator": generating.algorithm_or_estimator,
                    "parameters": generating.parameter_json,
                    "snapshot_hash": generating.snapshot_hash,
                    "snapshot_schema_version": generating.snapshot_schema_version,
                    "status": generating.status.value,
                }))
                add_edge(generating.execution_id, current.result_id)
                add_dataset(generating.dataset_version_id, generating.execution_id)
                add_artifacts(generating.execution_id, current.result_id)
                add_annotations(target_result_id=current.result_id)
                if generating.input_result_id:
                    upstream = uow.results.get(generating.input_result_id)
                    if upstream:
                        add_result_chain(upstream, depth + 1)
                        add_edge(upstream.result_id, generating.execution_id)
                if generating.input_graph_version_id:
                    graph = uow.graph_versions.get(generating.input_graph_version_id)
                    if graph:
                        add_graph_chain(graph, generating.execution_id, depth + 1)
                processing.remove(current.result_id)

            graph_processing: set[str] = set()

            def add_graph_chain(graph: Any, consumer_id: str, depth: int) -> None:
                if depth > 32 or graph.graph_version_id in graph_processing:
                    raise ValueError("Graph lineage cycle or maximum depth detected")
                graph_processing.add(graph.graph_version_id)
                add_node(LineageNode("GraphVersion", graph.graph_version_id, graph.name, {
                    "graph_type": graph.graph_type.value,
                    "graph_origin": graph.graph_origin.value,
                    "provenance": graph.provenance_json,
                    "content_hash": graph.content_hash,
                    "status": graph.status.value,
                }))
                add_edge(graph.graph_version_id, consumer_id)
                add_annotations(graph_version_id=graph.graph_version_id)
                if graph.source_result_id:
                    source = uow.results.get(graph.source_result_id)
                    if source:
                        add_result_chain(source, depth + 1)
                        add_edge(source.result_id, graph.graph_version_id)
                if graph.parent_graph_version_id:
                    parent = uow.graph_versions.get(graph.parent_graph_version_id)
                    if parent:
                        add_graph_chain(parent, graph.graph_version_id, depth + 1)
                graph_processing.remove(graph.graph_version_id)

            root_execution = uow.executions.get(result.execution_id)
            execution_project_id = root_execution.project_id if root_execution else ""
            add_result_chain(result)

        return LineageView(nodes=nodes, edges=edges)
