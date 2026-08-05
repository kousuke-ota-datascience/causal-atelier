"""GraphVersionService – create, edit, and fix graph versions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from ariadne.product.domain.enums import ExecutionOperation, GraphType, ResultType
from ariadne.product.domain.errors import EntityNotFound, InvalidAnalysisSpec, ProjectBoundaryViolation
from ariadne.product.domain.graph_semantics import canonical_graph
from ariadne.product.domain.graph_version import GraphVersion
from ariadne.product.ports.clock import ClockPort, SystemClock


@dataclass
class CreateGraphVersionCommand:
    project_id: str
    source_result_id: str
    name: str
    graph_type: GraphType
    graph_json: dict[str, Any]
    created_by: str
    parent_graph_version_id: str | None = None
    edit_rationale: str | None = None


@dataclass
class UpdateDraftCommand:
    graph_version_id: str
    graph_json: dict[str, Any]
    edit_rationale: str | None = None


class GraphVersionService:
    def __init__(self, uow_factory: Any, clock: ClockPort | None = None) -> None:
        self._uow_factory = uow_factory
        self._clock = clock or SystemClock()

    def create_from_discovery_result(self, command: CreateGraphVersionCommand) -> GraphVersion:
        now = self._clock.now()
        graph_json = canonical_graph(command.graph_type, command.graph_json)
        content_hash = _hash_graph(graph_json)

        with self._uow_factory() as uow:
            project = uow.projects.get(command.project_id)
            if project is None:
                raise EntityNotFound("Project", command.project_id)

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

            graph_version = GraphVersion(
                project_id=command.project_id,
                source_result_id=command.source_result_id,
                parent_graph_version_id=command.parent_graph_version_id,
                name=command.name,
                graph_type=command.graph_type,
                graph_json=graph_json,
                content_hash=content_hash,
                edit_rationale=command.edit_rationale,
                created_by=command.created_by,
                created_at=now,
            )

            uow.graph_versions.add(graph_version)
            uow.commit()

        return graph_version

    def update_draft(self, command: UpdateDraftCommand) -> GraphVersion:
        with self._uow_factory() as uow:
            gv = uow.graph_versions.get(command.graph_version_id)
            if gv is None:
                raise EntityNotFound("GraphVersion", command.graph_version_id)
            gv.apply_edit(command.graph_json, command.edit_rationale)
            gv.content_hash = _hash_graph(gv.graph_json)
            uow.graph_versions.update(gv)
            uow.commit()
        return gv

    def fix_graph(self, graph_version_id: str) -> GraphVersion:
        with self._uow_factory() as uow:
            gv = uow.graph_versions.get(graph_version_id)
            if gv is None:
                raise EntityNotFound("GraphVersion", graph_version_id)
            gv.fix()
            uow.graph_versions.update(gv)
            uow.commit()
        return gv


def _hash_graph(graph_json: dict[str, Any]) -> str:
    canonical = json.dumps(graph_json, sort_keys=True).encode()
    return hashlib.sha256(canonical).hexdigest()
