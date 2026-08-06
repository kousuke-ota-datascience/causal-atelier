"""GraphVersionService – create, edit, and fix graph versions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from ariadne.product.domain.enums import (
    ExecutionOperation, GraphOrigin, GraphType, GraphVersionStatus, ResultType,
)
from ariadne.product.domain.errors import (
    EntityNotFound,
    GraphParentNotFixed,
    InvalidAnalysisSpec,
    InvalidGraphEditBase,
    ProjectBoundaryViolation,
)
from ariadne.product.domain.graph_semantics import canonical_graph
from ariadne.product.domain.graph_version import GraphVersion
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.application.project_policy import require_active_project


@dataclass
class CreateGraphVersionCommand:
    project_id: str
    source_result_id: str | None
    name: str
    graph_type: GraphType
    graph_json: dict[str, Any]
    created_by: str
    graph_origin: GraphOrigin = GraphOrigin.DISCOVERED
    provenance_json: dict[str, Any] | None = None
    parent_graph_version_id: str | None = None
    designated_outcome_node: str | None = None
    edit_rationale: str | None = None


@dataclass
class UpdateDraftCommand:
    graph_version_id: str
    graph_json: dict[str, Any]
    project_id: str | None = None
    edit_rationale: str | None = None
    designated_outcome_node: str | None = None
    update_outcome: bool = False
    expected_content_hash: str | None = None


@dataclass
class CreateGraphEditDraftCommand:
    project_id: str
    base_candidate_kind: str
    base_candidate_id: str
    change_kind: GraphOrigin
    name: str
    edit_rationale: str
    created_by: str


class GraphVersionService:
    def __init__(self, uow_factory: Any, clock: ClockPort | None = None) -> None:
        self._uow_factory = uow_factory
        self._clock = clock or SystemClock()

    def create_from_discovery_result(self, command: CreateGraphVersionCommand) -> GraphVersion:
        if command.graph_origin != GraphOrigin.DISCOVERED:
            raise InvalidAnalysisSpec("create_from_discovery_result requires DISCOVERED origin")
        return self.create(command)

    def create(self, command: CreateGraphVersionCommand) -> GraphVersion:
        now = self._clock.now()
        graph_json = canonical_graph(command.graph_type, command.graph_json)
        content_hash = _hash_graph(graph_json)

        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            require_active_project(project)

            if command.source_result_id is not None:
                result = uow.results.get(command.source_result_id)
                if result is None:
                    raise EntityNotFound("Result", command.source_result_id)
                source_execution = uow.executions.get(result.execution_id)
                if source_execution is None:
                    raise EntityNotFound("Execution", result.execution_id)
                if source_execution.project_id != command.project_id:
                    raise ProjectBoundaryViolation("Source Result is not in the same project")
                if result.result_type != ResultType.DISCOVERY_GRAPH_RESULT:
                    raise InvalidAnalysisSpec("Source Result must be DISCOVERY_GRAPH_RESULT")
                if source_execution.operation != ExecutionOperation.DISCOVERY:
                    raise InvalidAnalysisSpec("Source Execution must be DISCOVERY")

            if command.parent_graph_version_id is not None:
                parent = uow.graph_versions.get(command.parent_graph_version_id)
                if parent is None:
                    raise EntityNotFound("GraphVersion", command.parent_graph_version_id)
                if parent.project_id != command.project_id:
                    raise ProjectBoundaryViolation("Parent GraphVersion not in same project")
                if parent.status != GraphVersionStatus.FIXED:
                    raise GraphParentNotFixed("Parent GraphVersion must be FIXED")
                self._assert_acyclic_parent(uow, parent)

            outcome = command.designated_outcome_node
            if outcome is None and command.parent_graph_version_id is not None:
                outcome = parent.designated_outcome_node
            if outcome is None and command.source_result_id is not None:
                outcome = _result_outcome(result, source_execution)
            if outcome is not None and outcome not in graph_json["nodes"]:
                raise InvalidAnalysisSpec("designated_outcome_node must be a Graph node")

            graph_version = GraphVersion(
                project_id=command.project_id,
                source_result_id=command.source_result_id,
                parent_graph_version_id=command.parent_graph_version_id,
                designated_outcome_node=outcome,
                name=command.name,
                graph_type=command.graph_type,
                graph_origin=command.graph_origin,
                provenance_json=command.provenance_json or {},
                graph_json=graph_json,
                content_hash=content_hash,
                edit_rationale=command.edit_rationale,
                created_by=command.created_by,
                created_at=now,
            )

            uow.graph_versions.add(graph_version)
            uow.commit()

        return graph_version

    def create_user_defined(self, command: CreateGraphVersionCommand) -> GraphVersion:
        if command.graph_origin != GraphOrigin.USER_DEFINED:
            raise InvalidAnalysisSpec("create_user_defined requires USER_DEFINED origin")
        return self.create(command)

    def create_imported(self, command: CreateGraphVersionCommand) -> GraphVersion:
        if command.graph_origin != GraphOrigin.IMPORTED:
            raise InvalidAnalysisSpec("create_imported requires IMPORTED origin")
        return self.create(command)

    def create_constraint_adjusted(self, command: CreateGraphVersionCommand) -> GraphVersion:
        if command.graph_origin != GraphOrigin.CONSTRAINT_ADJUSTED:
            raise InvalidAnalysisSpec("create_constraint_adjusted requires CONSTRAINT_ADJUSTED origin")
        provenance = command.provenance_json or {}
        if provenance.get("constraint_mode") != "POST_HOC":
            raise InvalidAnalysisSpec("constraint_mode=POST_HOC is required")
        return self.create(command)

    def create_from_parent_edit(self, command: CreateGraphVersionCommand) -> GraphVersion:
        if command.graph_origin != GraphOrigin.USER_EDITED:
            raise InvalidAnalysisSpec("create_from_parent_edit requires USER_EDITED origin")
        if not command.edit_rationale:
            raise InvalidAnalysisSpec("edit_rationale is required for USER_EDITED")
        return self.create(command)

    def update_draft(self, command: UpdateDraftCommand) -> GraphVersion:
        with self._uow_factory() as uow:
            gv = uow.graph_versions.get(command.graph_version_id)
            if gv is None:
                raise EntityNotFound("GraphVersion", command.graph_version_id)
            if command.project_id is not None and gv.project_id != command.project_id:
                raise ProjectBoundaryViolation("GraphVersion not in same project")
            project = uow.projects.get(gv.project_id)
            if project is None:
                raise EntityNotFound("Project", gv.project_id)
            require_active_project(project)
            if command.expected_content_hash is not None and command.expected_content_hash != gv.content_hash:
                raise InvalidAnalysisSpec("Graph Version content hash has changed")
            gv.apply_edit(
                command.graph_json,
                command.edit_rationale,
                command.designated_outcome_node,
                update_outcome=command.update_outcome,
            )
            gv.content_hash = _hash_graph(gv.graph_json)
            uow.graph_versions.update(gv)
            uow.commit()
        return gv

    def fix_graph(self, graph_version_id: str, project_id: str | None = None) -> GraphVersion:
        with self._uow_factory() as uow:
            gv = uow.graph_versions.get(graph_version_id)
            if gv is None:
                raise EntityNotFound("GraphVersion", graph_version_id)
            if project_id is not None and gv.project_id != project_id:
                raise ProjectBoundaryViolation("GraphVersion not in same project")
            project = uow.projects.get(gv.project_id)
            if project is None:
                raise EntityNotFound("Project", gv.project_id)
            require_active_project(project)
            gv.validate_outcome()
            if gv.graph_origin in {GraphOrigin.USER_EDITED, GraphOrigin.CONSTRAINT_ADJUSTED} and not (
                gv.edit_rationale and gv.edit_rationale.strip()
            ):
                raise InvalidAnalysisSpec("edit_rationale is required before FIX")
            gv.fix()
            uow.graph_versions.update(gv)
            uow.commit()
        return gv

    def create_edit_draft_from_candidate(
        self, command: CreateGraphEditDraftCommand
    ) -> GraphVersion:
        if command.change_kind not in {GraphOrigin.USER_EDITED, GraphOrigin.CONSTRAINT_ADJUSTED}:
            raise InvalidGraphEditBase("change_kind must be USER_EDITED or CONSTRAINT_ADJUSTED")
        if not command.edit_rationale.strip():
            raise InvalidAnalysisSpec("edit_rationale is required")
        now = self._clock.now()
        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)
            require_active_project(project)

            if command.base_candidate_kind == "GRAPH_VERSION":
                parent = uow.graph_versions.get(command.base_candidate_id)
                if parent is None:
                    raise EntityNotFound("GraphVersion", command.base_candidate_id)
                if parent.project_id != command.project_id:
                    raise ProjectBoundaryViolation("Parent GraphVersion not in same project")
                if parent.status != GraphVersionStatus.FIXED:
                    raise GraphParentNotFixed("Parent GraphVersion must be FIXED")
            elif command.base_candidate_kind == "DISCOVERY_RESULT":
                result = uow.results.get(command.base_candidate_id)
                if result is None:
                    raise EntityNotFound("Result", command.base_candidate_id)
                execution = uow.executions.get(result.execution_id)
                if execution is None:
                    raise EntityNotFound("Execution", result.execution_id)
                if execution.project_id != command.project_id:
                    raise ProjectBoundaryViolation("Discovery Result not in same project")
                if result.result_type != ResultType.DISCOVERY_GRAPH_RESULT:
                    raise InvalidGraphEditBase("Candidate must be a Discovery Graph Result")
                graph_type = GraphType(result.payload_json.get("graph_type"))
                graph_json = canonical_graph(graph_type, result.payload_json)
                content_hash = _hash_graph(graph_json)
                parent = next((
                    item for item in uow.graph_versions.list_by_project(command.project_id)
                    if item.graph_origin == GraphOrigin.DISCOVERED
                    and item.source_result_id == result.result_id
                    and item.content_hash == content_hash
                    and item.status == GraphVersionStatus.FIXED
                ), None)
                if parent is None:
                    parent = GraphVersion(
                        project_id=command.project_id,
                        source_result_id=result.result_id,
                        designated_outcome_node=_result_outcome(result, execution),
                        name=f"{command.name} (algorithm output)",
                        graph_type=graph_type,
                        graph_origin=GraphOrigin.DISCOVERED,
                        provenance_json={
                            "algorithm_output": True,
                            "source_execution_id": execution.execution_id,
                        },
                        graph_json=graph_json,
                        content_hash=content_hash,
                        status=GraphVersionStatus.FIXED,
                        created_by=command.created_by,
                        created_at=now,
                    )
                    parent.validate_outcome()
                    uow.graph_versions.add(parent)
            else:
                raise InvalidGraphEditBase("Unknown base_candidate_kind")

            self._assert_acyclic_parent(uow, parent)
            child = GraphVersion(
                project_id=command.project_id,
                parent_graph_version_id=parent.graph_version_id,
                designated_outcome_node=parent.designated_outcome_node,
                name=command.name,
                graph_type=parent.graph_type,
                graph_origin=command.change_kind,
                provenance_json={"derived_from": parent.graph_version_id},
                graph_json=dict(parent.graph_json),
                content_hash=parent.content_hash,
                edit_rationale=command.edit_rationale,
                status=GraphVersionStatus.DRAFT,
                created_by=command.created_by,
                created_at=now,
            )
            uow.graph_versions.add(child)
            uow.commit()
            return child

    @staticmethod
    def _assert_acyclic_parent(uow: Any, parent: GraphVersion) -> None:
        visited: set[str] = set()
        current: GraphVersion | None = parent
        while current is not None:
            if current.graph_version_id in visited:
                raise InvalidAnalysisSpec("Graph parent cycle detected")
            visited.add(current.graph_version_id)
            current = (
                uow.graph_versions.get(current.parent_graph_version_id)
                if current.parent_graph_version_id else None
            )


def _hash_graph(graph_json: dict[str, Any]) -> str:
    canonical = json.dumps(graph_json, sort_keys=True).encode()
    return hashlib.sha256(canonical).hexdigest()


def _result_outcome(result: Any, execution: Any) -> str | None:
    for source in (result.payload_json, result.summary_json):
        value = source.get("designated_outcome_node") if isinstance(source, dict) else None
        if isinstance(value, str) and value:
            return value
    operation_spec = execution.analysis_spec_json.get("operation_spec", {})
    value = operation_spec.get("designated_outcome_node")
    return value if isinstance(value, str) and value else None
