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

            def add_node(node: LineageNode) -> None:
                if node.entity_id not in visited:
                    visited.add(node.entity_id)
                    nodes.append(node)

            # Result node
            add_node(LineageNode("Result", result.result_id, f"Result ({result.result_type.value})", {
                "scientific_status": result.scientific_status.value,
            }))

            # Execution
            execution = uow.executions.get(result.execution_id)
            if execution:
                add_node(LineageNode("Execution", execution.execution_id, f"Execution ({execution.operation.value})", {
                    "algorithm_or_estimator": execution.algorithm_or_estimator,
                    "status": execution.status.value,
                }))
                edges.append((execution.execution_id, result.result_id))

                # Dataset Version
                dsv = uow.dataset_versions.get(execution.dataset_version_id)
                if dsv:
                    add_node(LineageNode("DatasetVersion", dsv.dataset_version_id, dsv.name, {
                        "dataset_key": dsv.dataset_key,
                        "version_label": dsv.version_label,
                    }))
                    edges.append((dsv.dataset_version_id, execution.execution_id))

                # Input Graph Version (Estimation)
                if execution.input_graph_version_id:
                    gv = uow.graph_versions.get(execution.input_graph_version_id)
                    if gv:
                        add_node(LineageNode("GraphVersion", gv.graph_version_id, gv.name, {
                            "graph_type": gv.graph_type.value,
                            "status": gv.status.value,
                        }))
                        edges.append((gv.graph_version_id, execution.execution_id))

                        # Upstream discovery result
                        disc_result = uow.results.get(gv.source_result_id)
                        if disc_result and disc_result.result_id not in visited:
                            add_node(LineageNode("Result", disc_result.result_id, "Discovery Result", {
                                "scientific_status": disc_result.scientific_status.value,
                            }))
                            edges.append((disc_result.result_id, gv.graph_version_id))

                            disc_exec = uow.executions.get(disc_result.execution_id)
                            if disc_exec and disc_exec.execution_id not in visited:
                                add_node(LineageNode("Execution", disc_exec.execution_id, "Discovery Execution", {
                                    "algorithm_or_estimator": disc_exec.algorithm_or_estimator,
                                }))
                                edges.append((disc_exec.execution_id, disc_result.result_id))

            # Artifacts
            artifacts = uow.artifacts.list_by_result(result_id)
            for art in artifacts:
                add_node(LineageNode("Artifact", art.artifact_id, art.artifact_type.value, {
                    "object_key": art.object_key,
                }))
                edges.append((result.result_id, art.artifact_id))

            # Annotations
            annotations = uow.annotations.list_by_target(result_id=result_id)
            for ann in annotations:
                add_node(LineageNode("Annotation", ann.annotation_id, "Annotation", {
                    "statement": ann.statement[:80],
                }))
                edges.append((result.result_id, ann.annotation_id))

        return LineageView(nodes=nodes, edges=edges)
