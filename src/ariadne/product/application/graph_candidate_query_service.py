"""Read-only Graph Candidate and Graph Comparison projections."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ariadne.product.domain.enums import GraphVersionStatus, ProjectStatus, ResultType
from ariadne.product.domain.errors import EntityNotFound, InvalidAnalysisSpec, ProjectBoundaryViolation


@dataclass(frozen=True)
class CandidateRef:
    candidate_kind: str
    candidate_id: str


@dataclass(frozen=True)
class GraphCandidateView:
    candidate_kind: str
    candidate_id: str
    source_result_id: str | None
    graph_version_id: str | None
    parent_graph_version_id: str | None
    graph_type: str
    graph_origin: str
    version_status: str | None
    scientific_status: str | None
    fixed: bool
    designated_outcome_node: str | None
    summary: dict[str, Any]
    warnings: list[Any]
    allowed_actions: dict[str, Any]
    graph: dict[str, Any] | None = None


@dataclass(frozen=True)
class GraphComparisonView:
    candidates: list[GraphCandidateView]
    compatibility: dict[str, Any]
    differences: list[dict[str, Any]]
    warnings: list[str] = field(default_factory=list)


class GraphCandidateQueryService:
    def __init__(self, uow_factory: Any) -> None:
        self._uow_factory = uow_factory

    def list_candidates(self, project_id: str) -> list[GraphCandidateView]:
        with self._uow_factory() as uow:
            project = uow.projects.get(project_id)
            if project is None:
                raise EntityNotFound("Project", project_id)
            writable = project.status == ProjectStatus.ACTIVE
            results = []
            executions_by_id: dict[str, Any] = {}
            for execution in uow.executions.list_by_project(project_id):
                executions_by_id[execution.execution_id] = execution
                results.extend(
                    result for result in uow.results.list_by_execution(execution.execution_id)
                    if result.result_type == ResultType.DISCOVERY_GRAPH_RESULT
                )
            graphs = uow.graph_versions.list_by_project(project_id)
            result_views = {
                result.result_id: self._from_result(
                    result, executions_by_id[result.execution_id], writable=writable
                )
                for result in results
            }
            graph_views = {
                graph.graph_version_id: self._from_graph(graph, writable=writable)
                for graph in graphs
            }

            children: dict[str, list[Any]] = {}
            by_source: dict[str, list[Any]] = {}
            for graph in graphs:
                if graph.parent_graph_version_id:
                    children.setdefault(graph.parent_graph_version_id, []).append(graph)
                elif graph.source_result_id:
                    by_source.setdefault(graph.source_result_id, []).append(graph)
            for values in [*children.values(), *by_source.values()]:
                values.sort(key=lambda item: (_time_key(item.created_at), item.graph_version_id))

            ordered: list[GraphCandidateView] = []
            visited: set[str] = set()

            def append_graph(graph: Any) -> None:
                if graph.graph_version_id in visited:
                    return
                visited.add(graph.graph_version_id)
                ordered.append(graph_views[graph.graph_version_id])
                for child in children.get(graph.graph_version_id, []):
                    append_graph(child)

            for result in sorted(results, key=lambda item: (
                _time_key(executions_by_id[item.execution_id].requested_at), item.result_id
            )):
                ordered.append(result_views[result.result_id])
                for graph in by_source.get(result.result_id, []):
                    append_graph(graph)
            for graph in sorted(
                graphs, key=lambda item: (_time_key(item.created_at), item.graph_version_id)
            ):
                append_graph(graph)
            return ordered

    def get_candidate(
        self, project_id: str, candidate_kind: str, candidate_id: str
    ) -> GraphCandidateView:
        with self._uow_factory() as uow:
            project = uow.projects.get(project_id)
            if project is None:
                raise EntityNotFound("Project", project_id)
            writable = project.status == ProjectStatus.ACTIVE
            if candidate_kind == "GRAPH_VERSION":
                graph = uow.graph_versions.get(candidate_id)
                if graph is None:
                    raise EntityNotFound("GraphVersion", candidate_id)
                if graph.project_id != project_id:
                    raise ProjectBoundaryViolation("Graph Candidate not in same project")
                return self._from_graph(graph, detail=True, writable=writable)
            if candidate_kind == "DISCOVERY_RESULT":
                result = uow.results.get(candidate_id)
                if result is None:
                    raise EntityNotFound("Result", candidate_id)
                execution = uow.executions.get(result.execution_id)
                if execution is None:
                    raise EntityNotFound("Execution", result.execution_id)
                if execution.project_id != project_id:
                    raise ProjectBoundaryViolation("Graph Candidate not in same project")
                if result.result_type != ResultType.DISCOVERY_GRAPH_RESULT:
                    raise InvalidAnalysisSpec("Result is not a Discovery Graph Result")
                return self._from_result(result, execution, detail=True, writable=writable)
            raise InvalidAnalysisSpec("candidate_kind is invalid")

    def compare(self, project_id: str, refs: list[CandidateRef]) -> GraphComparisonView:
        if len(refs) < 2:
            raise InvalidAnalysisSpec("At least two Graph Candidates are required")
        keys = [(item.candidate_kind, item.candidate_id) for item in refs]
        if len(keys) != len(set(keys)):
            raise InvalidAnalysisSpec("Graph Candidate references must be unique")
        candidates = [
            self.get_candidate(project_id, item.candidate_kind, item.candidate_id)
            for item in refs
        ]
        graphs = [item.graph or {} for item in candidates]
        graph_types = {item.graph_type for item in candidates}
        node_sets = [set(graph.get("nodes", [])) for graph in graphs]
        reasons: list[str] = []
        if len(graph_types) != 1:
            reasons.append("GRAPH_TYPE_MISMATCH")
        if any(nodes != node_sets[0] for nodes in node_sets[1:]):
            reasons.append("NODE_NAMESPACE_MISMATCH")
        compatible = not reasons
        differences: list[dict[str, Any]] = []
        if compatible:
            base_edges = _edges_by_pair(graphs[0])
            for candidate, graph in zip(candidates[1:], graphs[1:], strict=True):
                edges = _edges_by_pair(graph)
                base_pairs, pairs = set(base_edges), set(edges)
                changed = sorted(base_pairs & pairs & {
                    key for key in base_pairs & pairs if base_edges[key] != edges[key]
                })
                differences.append({
                    "base_candidate_id": candidates[0].candidate_id,
                    "candidate_id": candidate.candidate_id,
                    "added_edges": [edges[key] for key in sorted(pairs - base_pairs)],
                    "removed_edges": [base_edges[key] for key in sorted(base_pairs - pairs)],
                    "endpoint_changed_edges": [
                        {"nodes": list(key), "before": base_edges[key], "after": edges[key]}
                        for key in changed
                    ],
                    "common_edge_count": len((base_pairs & pairs) - set(changed)),
                })
        return GraphComparisonView(
            candidates=candidates,
            compatibility={
                "compatible": compatible,
                "reasons": reasons,
                "common_nodes": sorted(set.intersection(*node_sets)) if node_sets else [],
            },
            differences=differences,
            warnings=([] if compatible else [
                "Graph structures are not directly comparable; individual candidate tabs remain available."
            ]),
        )

    @staticmethod
    def _from_result(
        result: Any, execution: Any, *, detail: bool = False, writable: bool = True
    ) -> GraphCandidateView:
        graph = result.payload_json
        outcome = (
            graph.get("designated_outcome_node")
            or result.summary_json.get("designated_outcome_node")
            or execution.analysis_spec_json.get("operation_spec", {}).get("designated_outcome_node")
        )
        return GraphCandidateView(
            candidate_kind="DISCOVERY_RESULT",
            candidate_id=result.result_id,
            source_result_id=result.result_id,
            graph_version_id=None,
            parent_graph_version_id=None,
            graph_type=str(graph.get("graph_type", "UNKNOWN")),
            graph_origin="ALGORITHM_OUTPUT",
            version_status=None,
            scientific_status=result.scientific_status.value,
            fixed=False,
            designated_outcome_node=outcome,
            summary={
                **result.summary_json,
                "node_count": len(graph.get("nodes", [])),
                "edge_count": len(graph.get("edges", [])),
            },
            warnings=list(result.warning_json),
            allowed_actions={
                "can_edit": False,
                "can_fix": writable,
                "can_create_child": writable,
                "can_use_for_inference": False,
                "disabled_reasons": [
                    "ALGORITHM_OUTPUT_READ_ONLY",
                    *([] if writable else ["PROJECT_ARCHIVED"]),
                ],
            },
            graph=graph if detail else None,
        )

    @staticmethod
    def _from_graph(
        graph: Any, *, detail: bool = False, writable: bool = True
    ) -> GraphCandidateView:
        fixed = graph.status == GraphVersionStatus.FIXED
        disabled: list[str] = []
        if fixed:
            disabled.append("GRAPH_FIXED_IMMUTABLE")
        if fixed and not graph.designated_outcome_node:
            disabled.append("GRAPH_OUTCOME_REQUIRED")
        if not writable:
            disabled.append("PROJECT_ARCHIVED")
        return GraphCandidateView(
            candidate_kind="GRAPH_VERSION",
            candidate_id=graph.graph_version_id,
            source_result_id=graph.source_result_id,
            graph_version_id=graph.graph_version_id,
            parent_graph_version_id=graph.parent_graph_version_id,
            graph_type=graph.graph_type.value,
            graph_origin=graph.graph_origin.value,
            version_status=graph.status.value,
            scientific_status=None,
            fixed=fixed,
            designated_outcome_node=graph.designated_outcome_node,
            summary={
                "name": graph.name,
                "node_count": len(graph.graph_json.get("nodes", [])),
                "edge_count": len(graph.graph_json.get("edges", [])),
                "edit_rationale": graph.edit_rationale,
                "content_hash": graph.content_hash,
            },
            warnings=list(graph.provenance_json.get("warnings", [])),
            allowed_actions={
                "can_edit": writable and not fixed,
                "can_fix": writable and not fixed,
                "can_create_child": writable and fixed,
                "can_use_for_inference": writable and fixed and bool(graph.designated_outcome_node),
                "disabled_reasons": disabled,
            },
            graph=graph.graph_json if detail else None,
        )


def _edges_by_pair(graph: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    values: dict[tuple[str, str], dict[str, Any]] = {}
    for edge in graph.get("edges", []):
        source, target = str(edge["source"]), str(edge["target"])
        first, second = sorted((source, target))
        if source == first:
            endpoints = [edge["endpoint_source"], edge["endpoint_target"]]
        else:
            endpoints = [edge["endpoint_target"], edge["endpoint_source"]]
        values[(first, second)] = {"nodes": [first, second], "endpoints": endpoints}
    return values


def _time_key(value: Any) -> str:
    return value.isoformat() if hasattr(value, "isoformat") else ""
