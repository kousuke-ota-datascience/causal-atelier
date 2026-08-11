"""SQLAlchemy-backed repository implementations for the product domain."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import or_, select, text
from sqlalchemy.orm import Session

from ariadne.product.domain.annotation import Annotation
from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.dataset_version import DatasetVersion
from ariadne.product.domain.enums import (
    ArtifactScope,
    ArtifactType,
    AnalysisFamily,
    ExecutionOperation,
    ExecutionStatus,
    GraphOrigin,
    GraphType,
    GraphVersionStatus,
    ProjectStatus,
    ResultType,
    ResultLevel,
    ScientificStatus,
    StageExecutionStatus,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.stage_execution import StageAttempt, StageExecution
from ariadne.product.domain.execution_plan import StageType
from ariadne.product.domain.graph_version import GraphVersion
from ariadne.product.domain.project import Project
from ariadne.product.domain.result import Result
from ariadne.product.domain.errors import InvalidStateTransition
from ariadne.product.persistence.orm_models import (
    AnnotationOrm,
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    GraphVersionOrm,
    ProjectOrm,
    ResultOrm,
    StageAttemptOrm,
    StageExecutionOrm,
)


# ── Mapping helpers ────────────────────────────────────────────────────────────

def _orm_to_project(orm: ProjectOrm) -> Project:
    return Project(
        project_id=orm.project_id,
        name=orm.name,
        topic=orm.topic,
        objective=orm.objective,
        memo=orm.memo,
        status=ProjectStatus(orm.status),
        created_at=orm.created_at,
        updated_at=orm.updated_at,
    )


def _project_to_orm(p: Project, existing: ProjectOrm | None = None) -> ProjectOrm:
    orm = existing or ProjectOrm()
    orm.project_id = p.project_id
    orm.name = p.name
    orm.topic = p.topic
    orm.objective = p.objective
    orm.memo = p.memo
    orm.status = p.status.value
    if p.created_at:
        orm.created_at = p.created_at
    if p.updated_at:
        orm.updated_at = p.updated_at
    return orm


def _orm_to_artifact(orm: ArtifactOrm) -> Artifact:
    return Artifact(
        artifact_id=orm.artifact_id,
        project_id=orm.project_id,
        execution_id=orm.execution_id,
        stage_execution_id=orm.stage_execution_id,
        result_id=orm.result_id,
        artifact_scope=ArtifactScope(orm.artifact_scope),
        artifact_type=ArtifactType(orm.artifact_type),
        object_key=orm.object_key,
        content_hash=orm.content_hash,
        media_type=orm.media_type,
        size_bytes=orm.size_bytes,
        metadata_json=orm.metadata_json or {},
        created_at=orm.created_at,
    )


def _artifact_to_orm(a: Artifact) -> ArtifactOrm:
    orm = ArtifactOrm()
    orm.artifact_id = a.artifact_id
    orm.project_id = a.project_id
    orm.execution_id = a.execution_id
    orm.stage_execution_id = a.stage_execution_id
    orm.result_id = a.result_id
    orm.artifact_scope = a.artifact_scope.value
    orm.artifact_type = a.artifact_type.value
    orm.object_key = a.object_key
    orm.content_hash = a.content_hash
    orm.media_type = a.media_type
    orm.size_bytes = a.size_bytes
    orm.metadata_json = a.metadata_json
    if a.created_at:
        orm.created_at = a.created_at
    return orm


def _orm_to_dataset_version(orm: DatasetVersionOrm) -> DatasetVersion:
    return DatasetVersion(
        dataset_version_id=orm.dataset_version_id,
        project_id=orm.project_id,
        source_artifact_id=orm.source_artifact_id,
        dataset_key=orm.dataset_key,
        name=orm.name,
        version_label=orm.version_label,
        content_hash=orm.content_hash,
        schema_json=orm.schema_json or {},
        profile_summary_json=orm.profile_summary_json or {},
        row_count=orm.row_count,
        column_count=orm.column_count,
        source_note=orm.source_note,
        created_at=orm.created_at,
    )


def _dataset_version_to_orm(dv: DatasetVersion) -> DatasetVersionOrm:
    orm = DatasetVersionOrm()
    orm.dataset_version_id = dv.dataset_version_id
    orm.project_id = dv.project_id
    orm.source_artifact_id = dv.source_artifact_id
    orm.dataset_key = dv.dataset_key
    orm.name = dv.name
    orm.version_label = dv.version_label
    orm.content_hash = dv.content_hash
    orm.schema_json = dv.schema_json
    orm.profile_summary_json = dv.profile_summary_json
    orm.row_count = dv.row_count
    orm.column_count = dv.column_count
    orm.source_note = dv.source_note
    if dv.created_at:
        orm.created_at = dv.created_at
    return orm


def _orm_to_execution(orm: ExecutionOrm) -> Execution:
    return Execution(
        execution_id=orm.execution_id,
        project_id=orm.project_id,
        analysis_family=AnalysisFamily(orm.analysis_family),
        dataset_version_id=orm.dataset_version_id,
        input_graph_version_id=orm.input_graph_version_id,
        input_result_id=orm.input_result_id,
        batch_key=orm.batch_key,
        operation=ExecutionOperation(orm.operation),
        objective_snapshot=orm.objective_snapshot,
        rationale_snapshot=orm.rationale_snapshot,
        analysis_spec_json=orm.analysis_spec_json or {},
        algorithm_or_estimator=orm.algorithm_or_estimator,
        parameter_json=orm.parameter_json or {},
        random_seed=orm.random_seed,
        code_version=orm.code_version,
        runtime_version_json=orm.runtime_version_json or {},
        snapshot_hash=orm.snapshot_hash,
        snapshot_schema_version=orm.snapshot_schema_version,
        status=ExecutionStatus(orm.status),
        retry_count=orm.retry_count,
        last_error_summary=orm.last_error_summary,
        requested_by=orm.requested_by,
        requested_at=orm.requested_at,
        started_at=orm.started_at,
        finished_at=orm.finished_at,
        base_execution_id=orm.base_execution_id,
        revision_kind=orm.revision_kind,
        change_reason=orm.change_reason,
        lease_owner=orm.lease_owner,
        lease_expires_at=orm.lease_expires_at,
    )


def _execution_to_orm(e: Execution, existing: ExecutionOrm | None = None) -> ExecutionOrm:
    orm = existing or ExecutionOrm()
    orm.execution_id = e.execution_id
    orm.project_id = e.project_id
    orm.analysis_family = e.analysis_family.value
    orm.dataset_version_id = e.dataset_version_id
    orm.input_graph_version_id = e.input_graph_version_id
    orm.input_result_id = e.input_result_id
    orm.batch_key = e.batch_key
    orm.operation = e.operation.value
    orm.objective_snapshot = e.objective_snapshot
    orm.rationale_snapshot = e.rationale_snapshot
    orm.analysis_spec_json = e.analysis_spec_json
    orm.algorithm_or_estimator = e.algorithm_or_estimator
    orm.parameter_json = e.parameter_json
    orm.random_seed = e.random_seed
    orm.code_version = e.code_version
    orm.runtime_version_json = e.runtime_version_json
    orm.snapshot_hash = e.snapshot_hash
    orm.snapshot_schema_version = e.snapshot_schema_version
    orm.status = e.status.value
    orm.retry_count = e.retry_count
    orm.last_error_summary = e.last_error_summary
    orm.requested_by = e.requested_by
    if e.requested_at:
        orm.requested_at = e.requested_at
    orm.started_at = e.started_at
    orm.finished_at = e.finished_at
    orm.base_execution_id = e.base_execution_id
    orm.revision_kind = e.revision_kind
    orm.change_reason = e.change_reason
    orm.lease_owner = e.lease_owner
    orm.lease_expires_at = e.lease_expires_at
    return orm


def _orm_to_result(orm: ResultOrm) -> Result:
    return Result(
        result_id=orm.result_id,
        execution_id=orm.execution_id,
        result_level=ResultLevel(orm.result_level),
        stage_execution_id=orm.stage_execution_id,
        result_type=ResultType(orm.result_type),
        scientific_status=ScientificStatus(orm.scientific_status),
        summary_json=orm.summary_json or {},
        payload_json=orm.payload_json or {},
        diagnostics_json=orm.diagnostics_json or {},
        warning_json=orm.warning_json or [],
        created_at=orm.created_at,
    )


def _result_to_orm(r: Result) -> ResultOrm:
    orm = ResultOrm()
    orm.result_id = r.result_id
    orm.execution_id = r.execution_id
    orm.result_level = r.result_level.value
    orm.stage_execution_id = r.stage_execution_id
    orm.result_type = r.result_type.value
    orm.scientific_status = r.scientific_status.value
    orm.summary_json = r.summary_json
    orm.payload_json = r.payload_json
    orm.diagnostics_json = r.diagnostics_json
    orm.warning_json = r.warning_json
    if r.created_at:
        orm.created_at = r.created_at
    return orm


def _orm_to_graph_version(orm: GraphVersionOrm) -> GraphVersion:
    return GraphVersion(
        graph_version_id=orm.graph_version_id,
        project_id=orm.project_id,
        source_result_id=orm.source_result_id,
        parent_graph_version_id=orm.parent_graph_version_id,
        designated_outcome_node=orm.designated_outcome_node,
        name=orm.name,
        graph_type=GraphType(orm.graph_type),
        graph_origin=GraphOrigin(orm.graph_origin),
        provenance_json=orm.provenance_json or {},
        graph_json=orm.graph_json or {},
        content_hash=orm.content_hash,
        edit_rationale=orm.edit_rationale,
        status=GraphVersionStatus(orm.status),
        created_by=orm.created_by,
        created_at=orm.created_at,
    )


def _graph_version_to_orm(gv: GraphVersion, existing: GraphVersionOrm | None = None) -> GraphVersionOrm:
    orm = existing or GraphVersionOrm()
    orm.graph_version_id = gv.graph_version_id
    orm.project_id = gv.project_id
    orm.source_result_id = gv.source_result_id
    orm.parent_graph_version_id = gv.parent_graph_version_id
    orm.designated_outcome_node = gv.designated_outcome_node
    orm.name = gv.name
    orm.graph_type = gv.graph_type.value
    orm.graph_origin = gv.graph_origin.value
    orm.provenance_json = gv.provenance_json
    orm.graph_json = gv.graph_json
    orm.content_hash = gv.content_hash
    orm.edit_rationale = gv.edit_rationale
    orm.status = gv.status.value
    orm.created_by = gv.created_by
    if gv.created_at:
        orm.created_at = gv.created_at
    return orm


def _orm_to_annotation(orm: AnnotationOrm) -> Annotation:
    return Annotation(
        annotation_id=orm.annotation_id,
        project_id=orm.project_id,
        target_result_id=orm.target_result_id,
        target_graph_version_id=orm.target_graph_version_id,
        statement=orm.statement,
        rationale=orm.rationale,
        assumptions_json=orm.assumptions_json or [],
        limitations_json=orm.limitations_json or [],
        created_by=orm.created_by,
        created_at=orm.created_at,
        updated_at=orm.updated_at,
    )


def _annotation_to_orm(a: Annotation, existing: AnnotationOrm | None = None) -> AnnotationOrm:
    orm = existing or AnnotationOrm()
    orm.annotation_id = a.annotation_id
    orm.project_id = a.project_id
    orm.target_result_id = a.target_result_id
    orm.target_graph_version_id = a.target_graph_version_id
    orm.statement = a.statement
    orm.rationale = a.rationale
    orm.assumptions_json = a.assumptions_json
    orm.limitations_json = a.limitations_json
    orm.created_by = a.created_by
    if a.created_at:
        orm.created_at = a.created_at
    if a.updated_at:
        orm.updated_at = a.updated_at
    return orm


# ── Repository implementations ─────────────────────────────────────────────────

class SqlProjectRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, project: Project) -> None:
        self._session.add(_project_to_orm(project))

    def get(self, project_id: str) -> Project | None:
        orm = self._session.get(ProjectOrm, project_id)
        return _orm_to_project(orm) if orm else None

    def update(self, project: Project) -> None:
        orm = self._session.get(ProjectOrm, project.project_id)
        if orm:
            _project_to_orm(project, existing=orm)

    def list(self) -> list[Project]:
        rows = self._session.scalars(select(ProjectOrm).order_by(ProjectOrm.created_at)).all()
        return [_orm_to_project(row) for row in rows]


class SqlDatasetVersionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, dataset_version: DatasetVersion) -> None:
        self._session.add(_dataset_version_to_orm(dataset_version))

    def get(self, dataset_version_id: str) -> DatasetVersion | None:
        orm = self._session.get(DatasetVersionOrm, dataset_version_id)
        return _orm_to_dataset_version(orm) if orm else None

    def list_by_project(self, project_id: str) -> list[DatasetVersion]:
        rows = self._session.scalars(
            select(DatasetVersionOrm).where(DatasetVersionOrm.project_id == project_id)
        ).all()
        return [_orm_to_dataset_version(r) for r in rows]

    def exists_hash(self, project_id: str, dataset_key: str, content_hash: str) -> bool:
        row = self._session.scalars(
            select(DatasetVersionOrm).where(
                DatasetVersionOrm.project_id == project_id,
                DatasetVersionOrm.dataset_key == dataset_key,
                DatasetVersionOrm.content_hash == content_hash,
            )
        ).first()
        return row is not None


class SqlExecutionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_many(self, executions: list[Execution]) -> None:
        for e in executions:
            self._session.add(_execution_to_orm(e))

    def get(self, execution_id: str) -> Execution | None:
        orm = self._session.get(ExecutionOrm, execution_id)
        return _orm_to_execution(orm) if orm else None

    def list_by_project(self, project_id: str) -> list[Execution]:
        rows = self._session.scalars(
            select(ExecutionOrm).where(ExecutionOrm.project_id == project_id)
        ).all()
        return [_orm_to_execution(r) for r in rows]

    def claim_next(
        self,
        worker_token: str,
        *,
        worker_id: str | None = None,
        lease_seconds: int = 1800,
    ) -> Execution | None:
        """Atomically claim one canonical Execution; the caller commits."""
        if lease_seconds <= 0:
            raise ValueError("lease_seconds must be positive")
        now = datetime.now(timezone.utc)
        owner = worker_id or worker_token
        orm = self._session.scalars(
            select(ExecutionOrm)
            .where(
                or_(
                    ExecutionOrm.status == "QUEUED",
                    (
                        (ExecutionOrm.status == "RUNNING")
                        & ExecutionOrm.lease_expires_at.is_not(None)
                        & (ExecutionOrm.lease_expires_at <= now)
                    ),
                )
            )
            .order_by(ExecutionOrm.requested_at)
            .with_for_update(skip_locked=True)
            .limit(1)
        ).first()
        if orm is None:
            return None
        orm.status = ExecutionStatus.RUNNING.value
        orm.started_at = now
        orm.lease_owner = owner
        orm.lease_expires_at = now + timedelta(seconds=lease_seconds)
        orm._worker_token = worker_token
        self._session.flush()
        return _orm_to_execution(orm)

    def renew_lease(self, execution_id: str, owner: str, lease_seconds: int = 1800) -> None:
        if lease_seconds <= 0:
            raise ValueError("lease_seconds must be positive")
        orm = self._session.get(ExecutionOrm, execution_id)
        if orm is None:
            raise ValueError(f"Execution not found: {execution_id}")
        if orm.lease_owner != owner or orm.status != ExecutionStatus.RUNNING.value:
            raise PermissionError("lease owner mismatch")
        orm.lease_expires_at = datetime.now(timezone.utc) + timedelta(seconds=lease_seconds)

    def update(self, execution: Execution, *, owner: str | None = None) -> None:
        orm = self._session.get(ExecutionOrm, execution.execution_id)
        if orm is None:
            raise ValueError(f"Execution not found: {execution.execution_id}")
        if orm.lease_owner is not None and owner != orm.lease_owner:
            raise PermissionError("lease owner mismatch")
        _execution_to_orm(execution, existing=orm)

    def complete(self, execution: Execution, owner: str) -> None:
        """Persist a lifecycle mutation only for the current lease owner."""
        if execution.status is ExecutionStatus.SUCCEEDED:
            stages = list(self._session.scalars(select(StageExecutionOrm).where(
                StageExecutionOrm.execution_id == execution.execution_id
            )))
            if not stages or any(
                row.status not in {"SUCCEEDED", "SKIPPED_DUE_TO_PREREQUISITE"}
                for row in stages
            ):
                raise InvalidStateTransition(
                    "Execution", ExecutionStatus.RUNNING, ExecutionStatus.SUCCEEDED
                )
        self.update(execution, owner=owner)


def _stage_type(value: dict[str, Any]) -> StageType:
    return StageType(value["namespace"], value["name"], value["version"])


def _json_safe(value: Any) -> Any:
    """Persist orchestration projections, never arbitrary runner objects."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value) and not isinstance(value, type):
        return _json_safe(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)


def _orm_to_stage(orm: StageExecutionOrm, attempts: list[StageAttemptOrm]) -> StageExecution:
    return StageExecution(
        stage_execution_id=orm.stage_execution_id,
        execution_id=orm.execution_id,
        stage_key=orm.stage_key,
        stage_type=_stage_type(orm.stage_type_json),
        ordinal=orm.ordinal,
        dependencies=tuple(orm.dependencies_json or []),
        status=StageExecutionStatus(orm.status),
        input_binding=orm.input_binding_json or {},
        output_binding=orm.output_binding_json or {},
        attempts=[StageAttempt(
            attempt_number=item.attempt_number,
            worker_id=item.worker_id,
            started_at=item.started_at,
            stage_attempt_id=item.stage_attempt_id,
            finished_at=item.finished_at,
            error=item.error_json,
        ) for item in attempts],
        last_error=orm.last_error_json,
        started_at=orm.started_at,
        finished_at=orm.finished_at,
    )


class SqlStageExecutionRepository:
    """Canonical StageExecution persistence; claim authority remains Execution."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def _owner_check(self, execution_id: str, owner: str | None) -> ExecutionOrm:
        parent = self._session.get(ExecutionOrm, execution_id)
        if parent is None:
            raise ValueError(f"Execution not found: {execution_id}")
        if parent.lease_owner is not None and owner != parent.lease_owner:
            raise PermissionError("lease owner mismatch")
        expiry = parent.lease_expires_at
        expired = (
            expiry <= datetime.now() if expiry is not None and expiry.tzinfo is None
            else expiry <= datetime.now(timezone.utc) if expiry is not None else False
        )
        if owner is not None and expired:
            raise PermissionError("execution lease expired")
        return parent

    def add_many(self, stages: list[StageExecution]) -> None:
        for stage in stages:
            self._owner_check(stage.execution_id, None)
            self._session.add(StageExecutionOrm(
                stage_execution_id=stage.stage_execution_id,
                execution_id=stage.execution_id,
                stage_key=stage.stage_key,
                stage_type_json=stage.stage_type.as_dict(),
                ordinal=stage.ordinal,
                dependencies_json=list(stage.dependencies),
                status=stage.status.value,
                input_binding_json=_json_safe(stage.input_binding),
                output_binding_json=_json_safe(stage.output_binding),
                last_error_json=_json_safe(stage.last_error),
                started_at=stage.started_at,
                finished_at=stage.finished_at,
            ))

    def add(self, stage: StageExecution) -> None:
        self.add_many([stage])

    def get(self, stage_execution_id: str) -> StageExecution | None:
        orm = self._session.get(StageExecutionOrm, stage_execution_id)
        if orm is None:
            return None
        attempts = list(self._session.scalars(
            select(StageAttemptOrm)
            .where(StageAttemptOrm.stage_execution_id == stage_execution_id)
            .order_by(StageAttemptOrm.attempt_number)
        ))
        return _orm_to_stage(orm, attempts)

    def list_for_execution(self, execution_id: str) -> list[StageExecution]:
        rows = list(self._session.scalars(
            select(StageExecutionOrm)
            .where(StageExecutionOrm.execution_id == execution_id)
            .order_by(StageExecutionOrm.ordinal, StageExecutionOrm.stage_key)
        ))
        return [self.get(row.stage_execution_id) for row in rows]  # type: ignore[misc]

    def update(self, stage: StageExecution, *, owner: str | None = None) -> None:
        parent = self._owner_check(stage.execution_id, owner)
        if stage.status is StageExecutionStatus.RUNNING and parent.status != ExecutionStatus.RUNNING.value:
            raise InvalidStateTransition("StageExecution", parent.status, StageExecutionStatus.RUNNING)
        orm = self._session.get(StageExecutionOrm, stage.stage_execution_id)
        if orm is None:
            raise ValueError(f"StageExecution not found: {stage.stage_execution_id}")
        orm.status = stage.status.value
        orm.input_binding_json = _json_safe(stage.input_binding)
        orm.output_binding_json = _json_safe(stage.output_binding)
        orm.last_error_json = _json_safe(stage.last_error)
        orm.started_at = stage.started_at
        orm.finished_at = stage.finished_at
        existing = {
            item.attempt_number: item
            for item in self._session.scalars(select(StageAttemptOrm).where(
                StageAttemptOrm.stage_execution_id == stage.stage_execution_id
            ))
        }
        for attempt in stage.attempts:
            row = existing.get(attempt.attempt_number)
            if row is None:
                self._session.add(StageAttemptOrm(
                    stage_attempt_id=attempt.stage_attempt_id,
                    stage_execution_id=stage.stage_execution_id,
                    attempt_number=attempt.attempt_number,
                    worker_id=attempt.worker_id,
                    started_at=attempt.started_at,
                    finished_at=attempt.finished_at,
                    error_json=_json_safe(attempt.error),
                ))
            else:
                if row.stage_attempt_id != attempt.stage_attempt_id:
                    raise ValueError("stage attempt identity cannot be rewritten")
                row.finished_at = attempt.finished_at
                row.error_json = _json_safe(attempt.error)

    def start_attempt(self, stage: StageExecution, *, owner: str, worker_id: str, at: datetime) -> StageAttempt:
        self._owner_check(stage.execution_id, owner)
        attempt = stage.start_attempt(worker_id, at)
        self.update(stage, owner=owner)
        return attempt

    def attempts(self, stage_execution_id: str) -> list[StageAttempt]:
        stage = self.get(stage_execution_id)
        return [] if stage is None else stage.attempts


class SqlResultRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_many(self, results: list[Result]) -> None:
        for r in results:
            self._session.add(_result_to_orm(r))
        # Artifact rows may reference these newly-created Results in the same UoW.
        # There are no ORM relationships to give SQLAlchemy an ordering hint.
        self._session.flush()

    def get(self, result_id: str) -> Result | None:
        orm = self._session.get(ResultOrm, result_id)
        return _orm_to_result(orm) if orm else None

    def list_by_execution(self, execution_id: str) -> list[Result]:
        rows = self._session.scalars(
            select(ResultOrm).where(ResultOrm.execution_id == execution_id)
        ).all()
        return [_orm_to_result(r) for r in rows]

    def get_many(self, result_ids: list[str]) -> list[Result]:
        rows = self._session.scalars(
            select(ResultOrm).where(ResultOrm.result_id.in_(result_ids))
        ).all()
        return [_orm_to_result(r) for r in rows]


class SqlArtifactRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_many(self, artifacts: list[Artifact]) -> None:
        for a in artifacts:
            self._session.add(_artifact_to_orm(a))

    def get(self, artifact_id: str) -> Artifact | None:
        orm = self._session.get(ArtifactOrm, artifact_id)
        return _orm_to_artifact(orm) if orm else None

    def list_by_execution(self, execution_id: str) -> list[Artifact]:
        rows = self._session.scalars(
            select(ArtifactOrm).where(ArtifactOrm.execution_id == execution_id)
        ).all()
        return [_orm_to_artifact(r) for r in rows]

    def list_by_result(self, result_id: str) -> list[Artifact]:
        rows = self._session.scalars(
            select(ArtifactOrm).where(ArtifactOrm.result_id == result_id)
        ).all()
        return [_orm_to_artifact(r) for r in rows]


class SqlGraphVersionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, graph_version: GraphVersion) -> None:
        self._session.add(_graph_version_to_orm(graph_version))

    def get(self, graph_version_id: str) -> GraphVersion | None:
        orm = self._session.get(GraphVersionOrm, graph_version_id)
        return _orm_to_graph_version(orm) if orm else None

    def list_by_project(self, project_id: str) -> list[GraphVersion]:
        rows = self._session.scalars(
            select(GraphVersionOrm).where(GraphVersionOrm.project_id == project_id)
        ).all()
        return [_orm_to_graph_version(r) for r in rows]

    def update(self, graph_version: GraphVersion) -> None:
        orm = self._session.get(GraphVersionOrm, graph_version.graph_version_id)
        if orm:
            _graph_version_to_orm(graph_version, existing=orm)


class SqlAnnotationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, annotation: Annotation) -> None:
        self._session.add(_annotation_to_orm(annotation))

    def get(self, annotation_id: str) -> Annotation | None:
        orm = self._session.get(AnnotationOrm, annotation_id)
        return _orm_to_annotation(orm) if orm else None

    def update(self, annotation: Annotation) -> None:
        orm = self._session.get(AnnotationOrm, annotation.annotation_id)
        if orm:
            _annotation_to_orm(annotation, existing=orm)

    def list_by_target(
        self,
        *,
        result_id: str | None = None,
        graph_version_id: str | None = None,
    ) -> list[Annotation]:
        stmt = select(AnnotationOrm)
        if result_id is not None:
            stmt = stmt.where(AnnotationOrm.target_result_id == result_id)
        if graph_version_id is not None:
            stmt = stmt.where(AnnotationOrm.target_graph_version_id == graph_version_id)
        rows = self._session.scalars(stmt).all()
        return [_orm_to_annotation(r) for r in rows]
