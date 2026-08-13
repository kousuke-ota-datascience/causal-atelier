"""Analysis View and saved exploratory-analysis application service."""

from __future__ import annotations

import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import func, or_, select

from ariadne.capabilities.exploratory import (
    AnalysisViewCompiler,
    ExploratoryPlanner,
    register_exploratory_runners,
)
from ariadne.product.domain.analysis_specification import validate_exploratory_spec
from ariadne.product.domain.analysis_view import (
    VIEW_SCHEMA_VERSION,
    AnalysisView,
    validate_analysis_view_payload,
)
from ariadne.product.domain.errors import (
    ArtifactHashMismatch,
    EntityNotFound,
    InvalidSchema,
    LegacyProductAuthorityDisabled,
    ProjectArchived,
    ResourceImmutable,
)
from ariadne.product.domain.lineage import assert_generic_lineage_allowed
from ariadne.product.domain.schemas import SchemaRegistry, canonical_hash
from ariadne.product.application.analysis_frame_service import AnalysisFrameProvider
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.domain.enums import AnalysisFamily
from ariadne.product.domain.execution import Execution
from ariadne.product.persistence.orm_models import (
    AnalysisViewOrm,
    AnalysisSpecificationOrm,
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionPlanOrm,
    ExecutionOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
    LineageEdgeOrm,
    ProjectOrm,
    ResearchContextVersionOrm,
    ResultOrm,
)
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry

EXPLORATORY_SCHEMA_VERSION = "exploratory-analysis-spec/1"
_WORKSPACE_SCHEMAS = SchemaRegistry()
_WORKSPACE_SCHEMAS.register(VIEW_SCHEMA_VERSION, validate_analysis_view_payload)
_WORKSPACE_SCHEMAS.register(EXPLORATORY_SCHEMA_VERSION, validate_exploratory_spec)


@dataclass(frozen=True)
class ExploratoryResultProjection:
    """Family-facing read model backed by a canonical Product Result."""

    result_id: str
    project_id: str
    execution_id: str
    stage_execution_id: str
    analysis_family: str
    result_type: str
    schema_version: str
    analytical_status: str
    summary_json: dict[str, Any]
    payload_json: dict[str, Any]
    diagnostics_json: dict[str, Any]
    warning_json: list[Any]
    created_at: datetime | None


class ExploratoryWorkspaceService:
    def __init__(
        self,
        session_factory: Any,
        artifact_store: ArtifactStorePort,
        *,
        execution_service: ExecutionService | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._store = artifact_store
        self._compiler = AnalysisViewCompiler()
        self._frames = AnalysisFrameProvider(session_factory, artifact_store)
        self._execution_service = execution_service

    def _require_execution_service(self) -> ExecutionService:
        if self._execution_service is None:
            raise LegacyProductAuthorityDisabled(
                "ExploratoryWorkspaceService Product execution operation"
            )
        return self._execution_service

    def create_view(
        self,
        project_id: str,
        *,
        view_key: str,
        name: str,
        spec: dict[str, Any],
        actor: str = "system",
    ) -> AnalysisViewOrm:
        _WORKSPACE_SCHEMAS.validate(VIEW_SCHEMA_VERSION, spec)
        if spec["source_dataset_version_id"] == "":
            raise InvalidSchema("source_dataset_version_id is required")
        with self._session_factory() as session:
            self._active_project(session, project_id)
            dataset = session.get(DatasetVersionOrm, spec["source_dataset_version_id"])
            if dataset is None:
                raise EntityNotFound("DatasetVersion", spec["source_dataset_version_id"])
            if dataset.project_id != project_id:
                raise InvalidSchema("Dataset Version belongs to a different Project")
            latest = session.scalar(select(func.max(AnalysisViewOrm.version_number)).where(
                AnalysisViewOrm.project_id == project_id, AnalysisViewOrm.view_key == view_key,
            )) or 0
            domain = AnalysisView(
                project_id=project_id,
                view_key=_required_text("view_key", view_key, 100),
                version_number=latest + 1,
                name=_required_text("name", name, 200),
                view_spec=spec,
                created_by=actor,
            )
            self._compiler.validate(dataset.schema_json, spec)
            row = AnalysisViewOrm(
                analysis_view_id=domain.analysis_view_id,
                project_id=project_id,
                source_dataset_version_id=spec["source_dataset_version_id"],
                view_key=domain.view_key,
                version_number=domain.version_number,
                name=domain.name,
                status="DRAFT",
                schema_version="analysis-view/1",
                spec_json=spec,
                manifest_json={},
                created_by=actor,
                created_at=_now(),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return row

    def update_view(
        self, project_id: str, analysis_view_id: str, *, name: str | None, spec: dict[str, Any] | None
    ) -> AnalysisViewOrm:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._view(session, project_id, analysis_view_id)
            if row.status == "FIXED":
                raise ResourceImmutable("FIXED Analysis View cannot be updated")
            if spec is not None:
                _WORKSPACE_SCHEMAS.validate(VIEW_SCHEMA_VERSION, spec)
                if spec["source_dataset_version_id"] != row.source_dataset_version_id:
                    raise InvalidSchema("Analysis View source Dataset cannot be changed")
                dataset = session.get(DatasetVersionOrm, row.source_dataset_version_id)
                assert dataset is not None
                self._compiler.validate(dataset.schema_json, spec)
                row.spec_json = spec
            if name is not None:
                row.name = _required_text("name", name, 200)
            session.commit(); session.refresh(row)
            return row

    def validate_view(self, project_id: str, analysis_view_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            row = self._view(session, project_id, analysis_view_id)
            dataset, frame = self._load_frame(session, row.source_dataset_version_id)
            compiled = self._compiler.compile(
                frame, dataset.schema_json, row.spec_json,
                source_dataset_content_hash=dataset.content_hash,
            )
            return {"valid": True, "manifest": compiled.manifest}

    def fix_view(self, project_id: str, analysis_view_id: str) -> AnalysisViewOrm:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._view(session, project_id, analysis_view_id)
            if row.status == "FIXED":
                return row
            dataset, frame = self._load_frame(session, row.source_dataset_version_id)
            compiled = self._compiler.compile(
                frame, dataset.schema_json, row.spec_json,
                source_dataset_content_hash=dataset.content_hash,
            )
            row.status = "FIXED"
            row.content_hash = canonical_hash(row.spec_json)
            row.manifest_json = compiled.manifest
            row.fixed_at = _now()
            session.commit(); session.refresh(row)
            return row

    def get_view(self, project_id: str, analysis_view_id: str) -> AnalysisViewOrm:
        with self._session_factory() as session:
            return self._view(session, project_id, analysis_view_id)

    def list_views(self, project_id: str) -> list[AnalysisViewOrm]:
        with self._session_factory() as session:
            if session.get(ProjectOrm, project_id) is None:
                raise EntityNotFound("Project", project_id)
            return list(session.scalars(select(AnalysisViewOrm).where(
                AnalysisViewOrm.project_id == project_id
            ).order_by(AnalysisViewOrm.created_at, AnalysisViewOrm.analysis_view_id)))

    def preview(
        self,
        project_id: str,
        *,
        dataset_version_id: str,
        analysis_view_id: str | None,
        family_spec: dict[str, Any],
    ) -> dict[str, Any]:
        self._validate_exploratory_spec(family_spec)
        frame, manifest = self._analysis_frame(project_id, dataset_version_id, analysis_view_id)
        outcome = self._run_in_memory("preview", project_id, family_spec, frame)
        result = outcome.results[0]
        return {
            "schema_version": result.schema_version,
            "analysis_family": "EXPLORATORY",
            "result_type": result.result_type,
            "analytical_status": result.analytical_status,
            "summary": result.summary,
            "payload": result.payload,
            "warnings": list(result.warnings),
            "view_manifest": manifest,
            "saved": False,
        }

    def submit_execution(
        self,
        project_id: str,
        *,
        dataset_version_id: str,
        analysis_view_id: str | None,
        family_spec: dict[str, Any],
        requested_by: str = "system",
    ) -> FamilyExecutionOrm | Execution:
        execution_service = self._require_execution_service()
        self._validate_exploratory_spec(family_spec)
        with self._session_factory() as session:
            self._active_project(session, project_id)
            dataset = session.get(DatasetVersionOrm, dataset_version_id)
            if dataset is None or dataset.project_id != project_id:
                raise EntityNotFound("DatasetVersion", dataset_version_id)
            view = None
            if analysis_view_id:
                view = self._view(session, project_id, analysis_view_id)
                if view.status != "FIXED": raise InvalidSchema("Analysis View must be FIXED")
                if view.source_dataset_version_id != dataset_version_id:
                    raise InvalidSchema("Analysis View and Dataset Version do not match")
            specification_id = canonical_hash({
                "schema_version": EXPLORATORY_SCHEMA_VERSION,
                "dataset_version_id": dataset_version_id,
                "analysis_view_id": analysis_view_id,
                "family_spec": family_spec,
            })
            plan = ExploratoryPlanner().build_for_spec(
                project_id=project_id, specification_id=specification_id, family_spec=family_spec
            )
            plan_row = session.scalar(select(ExecutionPlanOrm).where(ExecutionPlanOrm.plan_hash == plan.plan_hash))
            if plan_row is None:
                plan_row = ExecutionPlanOrm(
                    execution_plan_id=plan.execution_plan_id, project_id=project_id,
                    analysis_specification_id=specification_id, analysis_family="EXPLORATORY",
                    plan_schema_version=plan.plan_schema_version, planner_id=plan.planner_id,
                    planner_version=plan.planner_version,
                    stages_json=[item.as_dict() for item in plan.stages],
                    dependencies_json=[item.as_dict() for item in plan.dependencies],
                    plan_hash=plan.plan_hash, created_at=_now(),
                )
                session.add(plan_row); session.flush()
            snapshot = {
                "schema_version": "family-execution-snapshot/1",
                "analysis_family": "EXPLORATORY",
                "dataset_version_id": dataset_version_id,
                "dataset_content_hash": dataset.content_hash,
                "analysis_view_id": analysis_view_id,
                "analysis_view_hash": view.content_hash if view else None,
                "specification_hash": specification_id,
                "plan_hash": plan.plan_hash,
                "runtime": {"runner": "exploratory-runners/1"},
            }
            # Product API wiring supplies this service.  The retained Family
            # ORM branch below is not reachable through a Product mutation.
            session.commit()
            canonical = execution_service.create_family_execution(
                    project_id=project_id,
                    dataset_version_id=dataset_version_id,
                    analysis_family=AnalysisFamily.EXPLORATORY,
                    family_spec=family_spec,
                    requested_by=requested_by,
                    analysis_view_id=analysis_view_id,
                    execution_plan_id=plan_row.execution_plan_id,
                    code_version="exploratory-runners/1",
                    runtime_version_json={"family_snapshot": snapshot},
            )
            return canonical
            execution = FamilyExecutionOrm(
                execution_id=str(uuid.uuid4()), project_id=project_id,
                dataset_version_id=dataset_version_id, analysis_view_id=analysis_view_id,
                execution_plan_id=plan_row.execution_plan_id, analysis_family="EXPLORATORY",
                specification_schema_version=EXPLORATORY_SCHEMA_VERSION,
                specification_snapshot_json=family_spec, snapshot_json=snapshot,
                snapshot_hash=canonical_hash(snapshot), status="QUEUED", retry_count=0,
                requested_by=requested_by, requested_at=_now(),
            )
            session.add(execution)
            for ordinal, stage in enumerate(plan.stages):
                session.add(FamilyStageExecutionOrm(
                    stage_execution_id=str(uuid.uuid4()), execution_id=execution.execution_id,
                    stage_key=stage.stage_key, stage_type_json=stage.stage_type.as_dict(),
                    ordinal=ordinal, status="PENDING", attempt_history_json=[],
                    input_binding_json={}, output_binding_json={},
                ))
            self._add_lineage(session, project_id, "DatasetVersion", dataset_version_id,
                              "USED_INPUT", "Execution", execution.execution_id,
                              {"snapshot_hash": execution.snapshot_hash})
            if view:
                self._add_lineage(session, project_id, "AnalysisView", view.analysis_view_id,
                                  "USED_INPUT", "Execution", execution.execution_id,
                                  {"content_hash": view.content_hash})
            session.commit(); session.refresh(execution)
            return execution

    def claim_next(
        self,
        worker_token: str,
        *,
        worker_id: str,
        lease_seconds: int = 300,
    ) -> str | None:
        """Reject the retired Family-table claim authority.

        Product workers must use ``uow.executions.claim_next`` and dispatch only
        after the canonical Execution has been leased.
        """
        raise LegacyProductAuthorityDisabled("ExploratoryWorkspaceService.claim_next")
        with self._session_factory() as session:
            execution = session.scalar(
                select(FamilyExecutionOrm)
                .where(
                    FamilyExecutionOrm.status == "QUEUED",
                    FamilyExecutionOrm.analysis_family == "EXPLORATORY",
                )
                .order_by(FamilyExecutionOrm.requested_at, FamilyExecutionOrm.execution_id)
                .with_for_update(skip_locked=True)
            )
            if execution is None:
                return None
            started_at = _now()
            execution.status = "RUNNING"
            execution.started_at = started_at
            execution.worker_token = worker_token
            execution.worker_id = worker_id
            execution.lease_expires_at = started_at + timedelta(seconds=lease_seconds)
            stage_row = session.scalar(select(FamilyStageExecutionOrm).where(
                FamilyStageExecutionOrm.execution_id == execution.execution_id
            ).order_by(FamilyStageExecutionOrm.ordinal))
            assert stage_row is not None
            stage_row.status = "RUNNING"
            stage_row.started_at = started_at
            stage_row.attempt_history_json = [{
                "attempt_number": 1,
                "worker_id": worker_id,
                "worker_token": worker_token,
                "lease_expires_at": execution.lease_expires_at.isoformat(),
                "started_at": started_at.isoformat(),
            }]
            execution_id = execution.execution_id
            session.commit()
            return execution_id

    def process_execution(self, execution_id: str, *, worker_token: str) -> None:
        """Reject the retired Family-table processing authority.

        Canonical ``ExecutionProcessor`` owns Product stage lifecycle and output
        persistence; retained scientific helpers are not reached through this
        legacy facade.
        """
        raise LegacyProductAuthorityDisabled("ExploratoryWorkspaceService.process_execution")
        stored_keys: list[str] = []
        with self._session_factory() as session:
            execution = session.get(FamilyExecutionOrm, execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            if execution.status != "RUNNING" or execution.worker_token != worker_token:
                return
            project_id = execution.project_id
            dataset_version_id = execution.dataset_version_id
            analysis_view_id = execution.analysis_view_id
            specification_snapshot = dict(execution.specification_snapshot_json)
        try:
            frame, manifest = self._analysis_frame(
                project_id, dataset_version_id, analysis_view_id
            )
            outcome = self._run_in_memory(
                execution_id, project_id, specification_snapshot, frame,
            )
            if outcome.status != "SUCCEEDED":
                raise RuntimeError(outcome.stages[0].last_error or "Exploratory Stage failed")
            now = _now()
            with self._session_factory() as session:
                execution = session.get(FamilyExecutionOrm, execution_id); assert execution is not None
                stage_row = session.scalar(select(FamilyStageExecutionOrm).where(
                    FamilyStageExecutionOrm.execution_id == execution_id
                )); assert stage_row is not None
                result_ids: list[str] = []
                for draft in outcome.results:
                    self._validate_result(draft.result_type, draft.schema_version, draft.analytical_status)
                    result_id = str(uuid.uuid4()); result_ids.append(result_id)
                    session.add(FamilyResultOrm(
                        result_id=result_id, project_id=execution.project_id,
                        execution_id=execution_id, stage_execution_id=stage_row.stage_execution_id,
                        analysis_family="EXPLORATORY", result_type=draft.result_type,
                        schema_version=draft.schema_version, analytical_status=draft.analytical_status,
                        summary_json=draft.summary, payload_json=draft.payload,
                        diagnostics_json=draft.diagnostics, warning_json=list(draft.warnings), created_at=now,
                    ))
                    self._add_lineage(session, execution.project_id, "Execution", execution_id,
                                      "GENERATED", "Result", result_id,
                                      {"stage_execution_id": stage_row.stage_execution_id})
                session.flush()
                for index, draft in enumerate(outcome.artifacts):
                    artifact_id = str(uuid.uuid4())
                    with tempfile.NamedTemporaryFile(delete=False) as handle:
                        handle.write(draft.content); path = Path(handle.name)
                    try:
                        object_key = f"projects/{execution.project_id}/executions/{execution_id}/{artifact_id}"
                        stored = self._store.store(path, object_key, draft.media_type)
                    finally:
                        path.unlink(missing_ok=True)
                    stored_keys.append(stored.object_key)
                    session.add(FamilyArtifactOrm(
                        artifact_id=artifact_id, project_id=execution.project_id,
                        execution_id=execution_id, stage_execution_id=stage_row.stage_execution_id,
                        result_id=result_ids[0] if result_ids else None, family="EXPLORATORY",
                        artifact_type=draft.artifact_type, schema_version=draft.schema_version,
                        media_type=stored.media_type, object_key=stored.object_key,
                        content_hash=stored.content_hash, size_bytes=stored.size_bytes,
                        metadata_json={**draft.metadata, "view_manifest": manifest}, created_at=now,
                    ))
                    if result_ids:
                        self._add_lineage(session, execution.project_id, "Result", result_ids[0],
                                          "GENERATED", "Artifact", artifact_id,
                                          {"content_hash": stored.content_hash})
                stage_row.status = "SUCCEEDED"; stage_row.finished_at = now
                stage_row.output_binding_json = outcome.stages[0].output_binding
                attempts = [dict(item) for item in stage_row.attempt_history_json]
                attempts[-1]["finished_at"] = now.isoformat()
                stage_row.attempt_history_json = attempts
                execution.status = "SUCCEEDED"; execution.finished_at = now
                execution.lease_expires_at = None
                session.commit()
        except Exception as exc:
            for key in stored_keys:
                self._store.delete(key)
            with self._session_factory() as session:
                execution = session.get(FamilyExecutionOrm, execution_id)
                if execution and execution.status == "RUNNING":
                    execution.status = "FAILED"; execution.finished_at = _now()
                    execution.lease_expires_at = None
                    execution.last_error_json = {"type": type(exc).__name__, "message": str(exc)}
                    stage = session.scalar(select(FamilyStageExecutionOrm).where(
                        FamilyStageExecutionOrm.execution_id == execution_id
                    ))
                    if stage:
                        stage.status = "FAILED"; stage.finished_at = execution.finished_at
                        stage.last_error_json = execution.last_error_json
                    session.commit()
            raise

    def get_execution(self, project_id: str, execution_id: str) -> FamilyExecutionOrm | Execution:
        execution_service = self._require_execution_service()
        if execution_service is not None:
            execution = execution_service.get_execution(execution_id)
            if (
                execution.project_id != project_id
                or execution.analysis_family is not AnalysisFamily.EXPLORATORY
            ):
                raise EntityNotFound("Execution", execution_id)
            return execution
        with self._session_factory() as session:
            row = session.get(FamilyExecutionOrm, execution_id)
            if row is None or row.project_id != project_id: raise EntityNotFound("Execution", execution_id)
            return row

    def list_executions(self, project_id: str) -> list[FamilyExecutionOrm | Execution]:
        execution_service = self._require_execution_service()
        if execution_service is not None:
            # ExecutionService intentionally exposes one identity at a time;
            # the canonical repository is the read authority for new writes.
            # The session factory remains available for query projection only.
            with self._session_factory() as session:
                from ariadne.product.persistence.orm_models import ExecutionOrm
                rows = list(session.scalars(select(ExecutionOrm).where(
                    ExecutionOrm.project_id == project_id,
                    ExecutionOrm.analysis_family == "EXPLORATORY",
                ).order_by(ExecutionOrm.requested_at.desc())))
            return [execution_service.get_execution(row.execution_id) for row in rows]
        with self._session_factory() as session:
            return list(session.scalars(select(FamilyExecutionOrm).where(
                FamilyExecutionOrm.project_id == project_id,
                FamilyExecutionOrm.analysis_family == "EXPLORATORY",
            ).order_by(FamilyExecutionOrm.requested_at.desc())))

    def list_results(self, project_id: str) -> list[FamilyResultOrm | ExploratoryResultProjection]:
        self._require_execution_service()
        if self._execution_service is not None:
            with self._session_factory() as session:
                rows = session.execute(
                    select(ResultOrm, ExecutionOrm)
                    .join(ExecutionOrm, ResultOrm.execution_id == ExecutionOrm.execution_id)
                    .where(
                        ExecutionOrm.project_id == project_id,
                        ExecutionOrm.analysis_family == AnalysisFamily.EXPLORATORY.value,
                    )
                    .order_by(ResultOrm.created_at.desc(), ResultOrm.result_id)
                ).all()
            return [self._canonical_result_projection(result, execution) for result, execution in rows]
        with self._session_factory() as session:
            return list(session.scalars(select(FamilyResultOrm).where(
                FamilyResultOrm.project_id == project_id,
                FamilyResultOrm.analysis_family == "EXPLORATORY",
            ).order_by(FamilyResultOrm.created_at.desc())))

    def get_result(self, project_id: str, result_id: str) -> FamilyResultOrm | ExploratoryResultProjection:
        self._require_execution_service()
        if self._execution_service is not None:
            with self._session_factory() as session:
                row = session.execute(
                    select(ResultOrm, ExecutionOrm)
                    .join(ExecutionOrm, ResultOrm.execution_id == ExecutionOrm.execution_id)
                    .where(
                        ResultOrm.result_id == result_id,
                        ExecutionOrm.project_id == project_id,
                        ExecutionOrm.analysis_family == AnalysisFamily.EXPLORATORY.value,
                    )
                ).one_or_none()
            if row is None:
                raise EntityNotFound("Result", result_id)
            return self._canonical_result_projection(*row)
        with self._session_factory() as session:
            row = session.get(FamilyResultOrm, result_id)
            if row is None or row.project_id != project_id: raise EntityNotFound("Result", result_id)
            return row

    def create_analysis_draft(
        self,
        project_id: str,
        result_id: str,
        target_family: str,
        analysis_mode: str = "EXPLORATORY",
        research_context_version_id: str | None = None,
        family_spec_schema_version: str | None = None,
        family_spec: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._require_execution_service()
        if target_family not in {"CAUSAL", "PREDICTIVE"}:
            raise InvalidSchema("target_family must be CAUSAL or PREDICTIVE")
        if analysis_mode not in {"EXPLORATORY", "CONFIRMATORY"}:
            raise InvalidSchema("analysis_mode must be EXPLORATORY or CONFIRMATORY")
        if family_spec is not None and not isinstance(family_spec, dict):
            raise InvalidSchema("family_spec must be an object")
        if self._execution_service is not None:
            with self._session_factory() as session:
                row = session.execute(
                    select(ResultOrm, ExecutionOrm)
                    .join(ExecutionOrm, ResultOrm.execution_id == ExecutionOrm.execution_id)
                    .where(
                        ResultOrm.result_id == result_id,
                        ExecutionOrm.project_id == project_id,
                        ExecutionOrm.analysis_family == AnalysisFamily.EXPLORATORY.value,
                    )
                ).one_or_none()
                if row is None:
                    raise EntityNotFound("Result", result_id)
                _, execution = row
                context_id = self._handoff_context_id(
                    session, project_id, result_id, research_context_version_id,
                )
                analysis_view_id = self._handoff_analysis_view(
                    session, project_id, result_id, execution.dataset_version_id,
                    (execution.analysis_spec_json or {}).get("analysis_view_id"),
                )
                session.flush()
                specification_id = str(uuid.uuid4())
                expected_schema = (
                    "causal-analysis-spec/2"
                    if target_family == "CAUSAL"
                    else "predictive-analysis-spec/1"
                )
                if family_spec_schema_version not in {None, expected_schema}:
                    raise InvalidSchema(
                        f"{target_family} requires family schema {expected_schema}"
                    )
                specification_key = f"exploratory-handoff-{result_id}-{target_family.lower()}"
                specification_version = (session.scalar(select(func.max(
                    AnalysisSpecificationOrm.version_number
                )).where(
                    AnalysisSpecificationOrm.project_id == project_id,
                    AnalysisSpecificationOrm.specification_key == specification_key,
                )) or 0) + 1
                warning_evidence = {
                    "code": "EXPLORATORY_REUSE_SAME_DATA",
                    "source_result_id": result_id,
                    "dataset_version_id": execution.dataset_version_id,
                }
                warnings = [warning_evidence] if analysis_mode == "CONFIRMATORY" else []
                specification = AnalysisSpecificationOrm(
                    analysis_specification_id=specification_id,
                    project_id=project_id,
                    specification_key=specification_key,
                    version_number=specification_version,
                    status="DRAFT",
                    schema_version="analysis-specification/1",
                    analysis_family=target_family,
                    research_context_version_id=context_id,
                    dataset_version_id=execution.dataset_version_id,
                    analysis_view_id=analysis_view_id,
                    analysis_mode=analysis_mode,
                    family_spec_schema_version=family_spec_schema_version or expected_schema,
                    family_spec_json=family_spec or {},
                    revision_context_json=None,
                    warnings_json=warnings,
                    created_by="system",
                    created_at=_now(),
                )
                session.add(specification)
                relation = {
                    "relation_type": "MOTIVATED",
                    "source_result_id": result_id,
                    "analysis_mode": analysis_mode,
                    "dataset_version_id": execution.dataset_version_id,
                }
                self._add_lineage(
                    session, project_id, "Result", result_id, "MOTIVATED",
                    "AnalysisSpecification", specification_id, relation,
                )
                session.commit()
                return {
                    "analysis_specification_id": specification_id,
                    "analysis_family": target_family,
                    "dataset_version_id": execution.dataset_version_id,
                    "analysis_view_id": analysis_view_id,
                    "research_context_version_id": context_id,
                    "analysis_mode": analysis_mode,
                    "status": "DRAFT",
                    "warnings": warnings,
                    "source_relation": relation,
                }
        raise LegacyProductAuthorityDisabled("ExploratoryWorkspaceService.create_analysis_draft")

    @staticmethod
    def _handoff_context_id(
        session: Any,
        project_id: str,
        result_id: str,
        requested_context_id: str | None,
    ) -> str:
        edges = session.scalars(select(LineageEdgeOrm).where(
            LineageEdgeOrm.project_id == project_id,
            or_(
                (LineageEdgeOrm.source_type == "Result")
                & (LineageEdgeOrm.source_id == result_id)
                & (LineageEdgeOrm.target_type == "ResearchContextVersion"),
                (LineageEdgeOrm.target_type == "Result")
                & (LineageEdgeOrm.target_id == result_id)
                & (LineageEdgeOrm.source_type == "ResearchContextVersion"),
            ),
        ))
        context_ids = {
            edge.target_id if edge.target_type == "ResearchContextVersion" else edge.source_id
            for edge in edges
        }
        if len(context_ids) == 1:
            context_id = next(iter(context_ids))
            if requested_context_id not in {None, context_id}:
                raise InvalidSchema("research_context_version_id conflicts with source Result lineage")
        else:
            if not requested_context_id:
                raise InvalidSchema(
                    "research_context_version_id is required when source Result lineage is not unique"
                )
            context_id = requested_context_id
        context = session.get(ResearchContextVersionOrm, context_id)
        if context is None or context.project_id != project_id:
            raise EntityNotFound("ResearchContextVersion", context_id)
        return context_id

    @staticmethod
    def _handoff_analysis_view(
        session: Any,
        project_id: str,
        result_id: str,
        dataset_version_id: str,
        source_analysis_view_id: str | None,
    ) -> str | None:
        if source_analysis_view_id is None:
            return None
        source = session.get(AnalysisViewOrm, source_analysis_view_id)
        if source is None or source.project_id != project_id:
            raise EntityNotFound("AnalysisView", source_analysis_view_id)
        if source.source_dataset_version_id != dataset_version_id:
            raise InvalidSchema("Analysis View and Dataset Version do not match")
        selection = {
            "schema_version": "analysis-view/1",
            "source_dataset_version_id": dataset_version_id,
            **{
                name: source.spec_json[name]
                for name in (
                    "row_filter", "selected_columns", "derived_columns",
                    "missing_value_policy", "time_cutoff", "sampling",
                )
            },
        }
        draft_id = str(uuid.uuid4())
        view_key = f"exploratory-handoff-{result_id}"
        version = (session.scalar(select(func.max(AnalysisViewOrm.version_number)).where(
            AnalysisViewOrm.project_id == project_id,
            AnalysisViewOrm.view_key == view_key,
        )) or 0) + 1
        session.add(AnalysisViewOrm(
            analysis_view_id=draft_id,
            project_id=project_id,
            source_dataset_version_id=dataset_version_id,
            view_key=view_key,
            version_number=version,
            name="Exploratory handoff selection",
            status="DRAFT",
            schema_version="analysis-view/1",
            spec_json=selection,
            manifest_json={},
            created_by="system",
            created_at=_now(),
        ))
        return draft_id

    @staticmethod
    def _canonical_result_projection(
        result: ResultOrm, execution: ExecutionOrm,
    ) -> ExploratoryResultProjection:
        payload = result.payload_json or {}
        schema_version = payload.get("schema_version")
        if not isinstance(schema_version, str) or not schema_version:
            raise InvalidSchema(
                "Canonical Exploratory Result is missing its preserved schema_version"
            )
        if result.stage_execution_id is None:
            raise InvalidSchema("Canonical Exploratory Result must retain StageExecution ownership")
        return ExploratoryResultProjection(
            result_id=result.result_id,
            project_id=execution.project_id,
            execution_id=result.execution_id,
            stage_execution_id=result.stage_execution_id,
            analysis_family=execution.analysis_family,
            result_type=result.result_type,
            schema_version=schema_version,
            analytical_status=result.scientific_status,
            summary_json=result.summary_json or {},
            payload_json=payload,
            diagnostics_json=result.diagnostics_json or {},
            warning_json=result.warning_json or [],
            created_at=result.created_at,
        )

    def _analysis_frame(
        self, project_id: str, dataset_version_id: str, analysis_view_id: str | None
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        return self._frames.load(project_id, dataset_version_id, analysis_view_id)

    def _run_in_memory(
        self, execution_id: str, project_id: str, spec: dict[str, Any], frame: pd.DataFrame
    ) -> Any:
        registry = StageRunnerRegistry(); register_exploratory_runners(registry)
        plan = ExploratoryPlanner().build_for_spec(
            project_id=project_id,
            specification_id=canonical_hash(spec), family_spec=spec,
        )
        return GenericExecutor(registry).execute(
            execution_id, plan, external_inputs={plan.stages[0].stage_key: {"frame": frame}}
        )

    def _load_frame(self, session: Any, dataset_version_id: str) -> tuple[DatasetVersionOrm, pd.DataFrame]:
        dataset = session.get(DatasetVersionOrm, dataset_version_id)
        if dataset is None: raise EntityNotFound("DatasetVersion", dataset_version_id)
        artifact = session.get(ArtifactOrm, dataset.source_artifact_id)
        if artifact is None: raise EntityNotFound("Artifact", dataset.source_artifact_id)
        suffix = Path(artifact.object_key).suffix or ".csv"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / f"dataset{suffix}"
            self._store.retrieve(artifact.object_key, path)
            import hashlib
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != artifact.content_hash or actual != dataset.content_hash:
                raise ArtifactHashMismatch("Dataset Artifact hash mismatch")
            frame = pd.read_parquet(path) if suffix.lower() == ".parquet" else pd.read_csv(path)
        return dataset, frame

    @staticmethod
    def _active_project(session: Any, project_id: str) -> ProjectOrm:
        project = session.get(ProjectOrm, project_id)
        if project is None: raise EntityNotFound("Project", project_id)
        if project.status == "ARCHIVED": raise ProjectArchived(project_id)
        return project

    @staticmethod
    def _view(session: Any, project_id: str, analysis_view_id: str) -> AnalysisViewOrm:
        row = session.get(AnalysisViewOrm, analysis_view_id)
        if row is None or row.project_id != project_id: raise EntityNotFound("AnalysisView", analysis_view_id)
        return row

    @staticmethod
    def _validate_exploratory_spec(spec: dict[str, Any]) -> None:
        _WORKSPACE_SCHEMAS.validate(EXPLORATORY_SCHEMA_VERSION, spec)

    @staticmethod
    def _validate_result(result_type: str, schema_version: str, status: str) -> None:
        allowed_types = {
            "DATA_PROFILE_RESULT", "DISTRIBUTION_RESULT", "ASSOCIATION_RESULT",
            "GROUP_SUMMARY_RESULT", "CHART_RESULT",
        }
        if result_type not in allowed_types or not schema_version.startswith("exploratory-"):
            raise InvalidSchema("Invalid exploratory Result schema")
        if status not in {"GENERATED", "GENERATED_WITH_WARNINGS", "INSUFFICIENT_DATA"}:
            raise InvalidSchema("Invalid exploratory analytical status")

    @staticmethod
    def _add_lineage(
        session: Any, project_id: str, source_type: str, source_id: str,
        relation_type: str, target_type: str, target_id: str, evidence: dict[str, Any],
    ) -> None:
        assert_generic_lineage_allowed(source_type, relation_type, target_type)
        session.add(LineageEdgeOrm(
            lineage_edge_id=str(uuid.uuid4()), project_id=project_id,
            source_type=source_type, source_id=source_id, relation_type=relation_type,
            target_type=target_type, target_id=target_id, evidence_json=evidence,
            created_by="system", created_at=_now(),
        ))


def _required_text(name: str, value: str, maximum: int) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > maximum:
        raise InvalidSchema(f"{name} must be 1..{maximum} characters")
    return normalized


def _now() -> datetime:
    return datetime.now(timezone.utc)
