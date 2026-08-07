"""Asynchronous predictive execution-plan and worker application service."""

from __future__ import annotations

import platform
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sqlalchemy import or_, select

from ariadne.capabilities.predictive import (
    PredictivePlanner,
    register_predictive_explain_runner,
    register_predictive_split_runner,
    register_predictive_training_runners,
)
from ariadne.capabilities.predictive.modeling import MODEL_REGISTRY
from ariadne.product.application.analysis_frame_service import AnalysisFrameProvider
from ariadne.product.domain.analysis_specification import AnalysisSpecification
from ariadne.product.domain.enums import (
    AnalysisFamily,
    AnalysisMode,
    VersionedResourceStatus,
)
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidExecutionPlan,
    InvalidSchema,
    InvalidStateTransition,
    ProjectArchived,
)
from ariadne.product.domain.execution_plan import (
    ExecutionPlan,
    StageBinding,
    StageDefinition,
    StageType,
)
from ariadne.product.domain.schemas import canonical_hash
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    AnalysisViewOrm,
    DatasetVersionOrm,
    ExecutionPlanOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    FamilyStageExecutionOrm,
    LineageEdgeOrm,
    ProjectOrm,
    ResearchContextVersionOrm,
)
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.plan_validator import PlanValidator
from ariadne.product.workflow.runner_registry import StageRunnerRegistry


class PredictiveWorkflowService:
    def __init__(self, session_factory: Any, artifact_store: ArtifactStorePort) -> None:
        self._session_factory = session_factory
        self._store = artifact_store
        self._frames = AnalysisFrameProvider(session_factory, artifact_store)

    def create_plan(self, project_id: str, specification_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            specification = self._fixed_predictive_specification(
                session, project_id, specification_id
            )
            plan = PredictivePlanner().build_plan(self._planning_context(specification))
            PlanValidator(self._runner_registry()).validate(plan)
            row = session.scalar(select(ExecutionPlanOrm).where(
                ExecutionPlanOrm.plan_hash == plan.plan_hash
            ))
            if row is None:
                row = ExecutionPlanOrm(
                    execution_plan_id=plan.execution_plan_id,
                    project_id=project_id,
                    analysis_specification_id=specification_id,
                    analysis_family="PREDICTIVE",
                    plan_schema_version=plan.plan_schema_version,
                    planner_id=plan.planner_id,
                    planner_version=plan.planner_version,
                    stages_json=[stage.as_dict() for stage in plan.stages],
                    dependencies_json=[edge.as_dict() for edge in plan.dependencies],
                    plan_hash=plan.plan_hash,
                    created_at=_now(),
                )
                session.add(row)
                session.commit()
                session.refresh(row)
            return self._plan_response(row)

    def get_plan(self, project_id: str, plan_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            return self._plan_response(self._plan(session, project_id, plan_id))

    def validate_plan(self, project_id: str, plan_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            row = self._plan(session, project_id, plan_id)
            order = PlanValidator(self._runner_registry()).validate(self._plan_domain(row))
            return {
                "execution_plan_id": plan_id,
                "valid": True,
                "plan_hash": row.plan_hash,
                "execution_order": list(order),
            }

    def submit_execution(
        self,
        project_id: str,
        *,
        specification_id: str,
        plan_id: str,
        seed: int,
        requested_by: str,
        base_execution_id: str | None = None,
        revision_kind: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise InvalidSchema("Execution seed must be an integer")
        with self._session_factory() as session:
            self._active_project(session, project_id)
            spec_row = self._fixed_predictive_specification(
                session, project_id, specification_id
            )
            plan_row = self._plan(session, project_id, plan_id)
            if plan_row.analysis_specification_id != specification_id:
                raise InvalidExecutionPlan(
                    "PLAN_SPECIFICATION_MISMATCH",
                    "Execution Plan does not reference the submitted Specification",
                )
            plan = self._plan_domain(plan_row)
            PlanValidator(self._runner_registry()).validate(plan)
            specification_seed = int(spec_row.family_spec_json["split_spec"]["seed"])
            if seed != specification_seed:
                raise InvalidExecutionPlan(
                    "SEED_SPECIFICATION_MISMATCH",
                    "Execution seed must equal the immutable Specification split seed",
                )
            dataset = session.get(DatasetVersionOrm, spec_row.dataset_version_id)
            assert dataset is not None
            context = session.get(
                ResearchContextVersionOrm, spec_row.research_context_version_id
            )
            assert context is not None
            view = (
                session.get(AnalysisViewOrm, spec_row.analysis_view_id)
                if spec_row.analysis_view_id
                else None
            )
            snapshot = {
                "schema_version": "family-execution-snapshot/1",
                "analysis_family": "PREDICTIVE",
                "research_context": {
                    "id": context.research_context_version_id,
                    "hash": context.canonical_hash,
                },
                "dataset_version": {"id": dataset.dataset_version_id, "hash": dataset.content_hash},
                "analysis_view": {
                    "id": view.analysis_view_id if view else None,
                    "hash": view.content_hash if view else None,
                },
                "analysis_specification": {
                    "id": spec_row.analysis_specification_id,
                    "hash": spec_row.canonical_hash,
                },
                "execution_plan": {"id": plan_id, "hash": plan_row.plan_hash},
                "versions": {
                    "code": "ariadne/0.1.0",
                    "python": platform.python_version(),
                    "numpy": np.__version__,
                    "pandas": pd.__version__,
                    "schemas": [
                        "analysis-specification/1",
                        "predictive-analysis-spec/1",
                        "execution-plan/1",
                    ],
                },
                "seed": seed,
                "revision": {
                    "base_execution_id": base_execution_id,
                    "kind": revision_kind,
                } if base_execution_id else None,
            }
            execution = FamilyExecutionOrm(
                execution_id=str(uuid.uuid4()),
                project_id=project_id,
                dataset_version_id=spec_row.dataset_version_id,
                analysis_view_id=spec_row.analysis_view_id,
                research_context_version_id=spec_row.research_context_version_id,
                analysis_specification_id=specification_id,
                execution_plan_id=plan_id,
                analysis_family="PREDICTIVE",
                specification_schema_version=spec_row.family_spec_schema_version,
                specification_snapshot_json=spec_row.family_spec_json,
                snapshot_json=snapshot,
                snapshot_hash=canonical_hash(snapshot),
                status="QUEUED",
                retry_count=0,
                requested_by=requested_by,
                requested_at=_now(),
            )
            session.add(execution)
            session.flush()
            for ordinal, stage in enumerate(plan.stages):
                session.add(FamilyStageExecutionOrm(
                    stage_execution_id=str(uuid.uuid4()),
                    execution_id=execution.execution_id,
                    stage_key=stage.stage_key,
                    stage_type_json=stage.stage_type.as_dict(),
                    ordinal=ordinal,
                    status="PENDING",
                    attempt_history_json=[],
                    input_binding_json={},
                    output_binding_json={},
                ))
            for source_type, source_id, evidence in (
                ("ResearchContextVersion", context.research_context_version_id, {"hash": context.canonical_hash}),
                ("DatasetVersion", dataset.dataset_version_id, {"hash": dataset.content_hash}),
                ("AnalysisSpecification", specification_id, {"hash": spec_row.canonical_hash}),
                ("ExecutionPlan", plan_id, {"hash": plan_row.plan_hash}),
            ):
                self._lineage(
                    session,
                    project_id,
                    source_type,
                    source_id,
                    "USED_INPUT",
                    "Execution",
                    execution.execution_id,
                    evidence,
                )
            if view:
                self._lineage(
                    session,
                    project_id,
                    "AnalysisView",
                    view.analysis_view_id,
                    "USED_INPUT",
                    "Execution",
                    execution.execution_id,
                    {"hash": view.content_hash},
                )
            if base_execution_id:
                base = self._execution(session, project_id, base_execution_id)
                self._lineage(
                    session,
                    project_id,
                    "Execution",
                    base.execution_id,
                    "REVISED_FROM" if revision_kind == "REVISED" else "DERIVED_FROM",
                    "Execution",
                    execution.execution_id,
                    {"revision_kind": revision_kind},
                )
            session.commit()
            return self._execution_response(execution)

    def claim_next(
        self, worker_token: str, *, worker_id: str, lease_seconds: int = 1800
    ) -> str | None:
        with self._session_factory() as session:
            execution = session.scalar(
                select(FamilyExecutionOrm)
                .where(
                    FamilyExecutionOrm.status == "QUEUED",
                    FamilyExecutionOrm.analysis_family == "PREDICTIVE",
                    FamilyExecutionOrm.analysis_specification_id.is_not(None),
                )
                .order_by(FamilyExecutionOrm.requested_at, FamilyExecutionOrm.execution_id)
                .with_for_update(skip_locked=True)
            )
            if execution is None:
                return None
            started = _now()
            execution.status = "RUNNING"
            execution.started_at = started
            execution.worker_token = worker_token
            execution.worker_id = worker_id
            execution.lease_expires_at = started + timedelta(seconds=lease_seconds)
            session.commit()
            return execution.execution_id

    def process_execution(self, execution_id: str, *, worker_token: str) -> None:
        stored_keys: list[str] = []
        outcome: Any | None = None
        with self._session_factory() as session:
            execution = session.get(FamilyExecutionOrm, execution_id)
            if execution is None:
                raise EntityNotFound("Execution", execution_id)
            if execution.status != "RUNNING" or execution.worker_token != worker_token:
                return
            plan_row = session.get(ExecutionPlanOrm, execution.execution_plan_id)
            assert plan_row is not None
            plan = self._plan_domain(plan_row)
            project_id = execution.project_id
            dataset_version_id = execution.dataset_version_id
            analysis_view_id = execution.analysis_view_id
            snapshots = dict(execution.snapshot_json)
            worker_id = execution.worker_id or "predictive-worker"
        try:
            frame, view_manifest = self._frames.load(
                project_id, dataset_version_id, analysis_view_id
            )
            source_snapshot = {
                "schema_version": "predictive-source-snapshot/1",
                "dataset_version_id": dataset_version_id,
                "dataset_content_hash": view_manifest["source_dataset_content_hash"],
                "analysis_view_id": analysis_view_id,
                "analysis_view_hash": (
                    view_manifest["view_spec_hash"] if analysis_view_id else None
                ),
                "materialized_hash": view_manifest["materialized_hash"],
            }
            committed: list[tuple[str, Any]] = []

            def capture(stage: Any, result: Any) -> None:
                committed.append((stage.stage_key, result))

            def cancelled() -> bool:
                with self._session_factory() as session:
                    current = session.get(FamilyExecutionOrm, execution_id)
                    return (
                        current is None
                        or current.status == "CANCELLED"
                        or current.worker_token != worker_token
                    )

            outcome = GenericExecutor(
                self._runner_registry(), commit=capture
            ).execute(
                execution_id,
                plan,
                external_inputs={
                    "split": {"frame": frame, "source_snapshot": source_snapshot},
                    "prepare": {"frame": frame},
                },
                snapshots=snapshots,
                worker_id=worker_id,
                cancelled=cancelled,
            )
            if outcome.status == "CANCELLED":
                return
            execution_error = next(
                (stage.last_error for stage in outcome.stages if stage.last_error),
                {"message": "Predictive execution failed"},
            ) if outcome.status == "FAILED" else None
            now = _now()
            with self._session_factory() as session:
                execution = session.get(FamilyExecutionOrm, execution_id)
                assert execution is not None
                if (
                    execution.status != "RUNNING"
                    or execution.worker_token != worker_token
                ):
                    return
                stage_rows = {
                    row.stage_key: row
                    for row in session.scalars(select(FamilyStageExecutionOrm).where(
                        FamilyStageExecutionOrm.execution_id == execution_id
                    ))
                }
                artifacts_by_stage: dict[str, list[str]] = {}
                result_ids_by_type: dict[str, str] = {}
                artifact_ids_by_type: dict[str, str] = {}
                for stage_key, run_result in committed:
                    stage_row = stage_rows[stage_key]
                    result_ids: list[str] = []
                    for draft in run_result.results:
                        self._validate_result(draft.result_type, draft.analytical_status)
                        result_id = str(uuid.uuid4())
                        result_ids.append(result_id)
                        result_ids_by_type[draft.result_type] = result_id
                        session.add(FamilyResultOrm(
                            result_id=result_id,
                            project_id=project_id,
                            execution_id=execution_id,
                            stage_execution_id=stage_row.stage_execution_id,
                            analysis_family="PREDICTIVE",
                            result_type=draft.result_type,
                            schema_version=draft.schema_version,
                            analytical_status=draft.analytical_status,
                            summary_json=draft.summary,
                            payload_json=draft.payload,
                            diagnostics_json=draft.diagnostics,
                            warning_json=list(draft.warnings),
                            created_at=now,
                        ))
                        self._lineage(
                            session,
                            project_id,
                            "Execution",
                            execution_id,
                            "GENERATED",
                            "Result",
                            result_id,
                            {"stage_key": stage_key},
                        )
                    session.flush()
                    for draft in run_result.artifacts:
                        artifact_id = str(uuid.uuid4())
                        artifact_ids_by_type[draft.artifact_type] = artifact_id
                        object_key = (
                            f"projects/{project_id}/executions/{execution_id}/"
                            f"{stage_key}/{artifact_id}.json"
                        )
                        stored = self._store_draft(draft.content, object_key, draft.media_type)
                        stored_keys.append(stored.object_key)
                        artifacts_by_stage.setdefault(stage_key, []).append(artifact_id)
                        target_result_id = (
                            result_ids_by_type.get(draft.result_type)
                            if draft.result_type
                            else (result_ids[0] if result_ids else None)
                        )
                        if draft.result_type and target_result_id is None:
                            raise InvalidSchema(
                                "Artifact references an uncommitted Result type: "
                                f"{draft.result_type}"
                            )
                        session.add(FamilyArtifactOrm(
                            artifact_id=artifact_id,
                            project_id=project_id,
                            execution_id=execution_id,
                            stage_execution_id=stage_row.stage_execution_id,
                            result_id=target_result_id,
                            family="PREDICTIVE",
                            artifact_type=draft.artifact_type,
                            schema_version=draft.schema_version,
                            media_type=stored.media_type,
                            object_key=stored.object_key,
                            content_hash=stored.content_hash,
                            size_bytes=stored.size_bytes,
                            metadata_json={**draft.metadata, "view_manifest": view_manifest},
                            created_at=now,
                        ))
                        self._lineage(
                            session,
                            project_id,
                            "Result" if target_result_id else "Execution",
                            target_result_id or execution_id,
                            "GENERATED",
                            "Artifact",
                            artifact_id,
                            {"stage_key": stage_key, "content_hash": stored.content_hash},
                        )
                        if (
                            stage_key in {"evaluate", "explain"}
                            and target_result_id is not None
                        ):
                            self._lineage(
                                session,
                                project_id,
                                "Artifact",
                                artifact_id,
                                "EVIDENCE_FOR",
                                "Result",
                                target_result_id,
                                {"stage_key": stage_key},
                            )
                session.flush()
                chain = [
                    key
                    for key in ("split", "prepare", "train", "evaluate", "explain")
                    if key in artifacts_by_stage
                ]
                for source_key, target_key in zip(chain, chain[1:]):
                    for target_artifact_id in artifacts_by_stage[target_key]:
                        self._lineage(
                            session,
                            project_id,
                            "Artifact",
                            target_artifact_id,
                            "DERIVED_FROM",
                            "Artifact",
                            artifacts_by_stage[source_key][0],
                            {"source_stage": source_key, "target_stage": target_key},
                        )
                self._add_g5_lineage(
                    session,
                    execution,
                    result_ids_by_type,
                    artifact_ids_by_type,
                )
                for stage in outcome.stages:
                    row = stage_rows[stage.stage_key]
                    _write_stage_state(row, stage)
                execution.status = outcome.status
                execution.finished_at = now
                execution.lease_expires_at = None
                execution.worker_token = None
                if execution_error is not None:
                    execution.last_error_json = execution_error
                session.commit()
        except Exception as exc:
            for key in stored_keys:
                self._store.delete(key)
            with self._session_factory() as session:
                execution = session.get(FamilyExecutionOrm, execution_id)
                if execution and execution.status == "RUNNING":
                    execution.status = "FAILED"
                    execution.finished_at = _now()
                    execution.lease_expires_at = None
                    execution.worker_token = None
                    execution.last_error_json = {
                        "type": type(exc).__name__, "message": str(exc)
                    }
                    if outcome is not None:
                        stage_rows = {
                            row.stage_key: row
                            for row in session.scalars(
                                select(FamilyStageExecutionOrm).where(
                                    FamilyStageExecutionOrm.execution_id == execution_id
                                )
                            )
                        }
                        for stage in outcome.stages:
                            row = stage_rows[stage.stage_key]
                            _write_stage_state(row, stage)
                            if row.status == "SUCCEEDED":
                                row.status = "PENDING"
                                row.output_binding_json = {}
                        terminal = next(
                            (
                                stage_rows[stage.stage_key]
                                for stage in reversed(outcome.stages)
                                if stage.attempts
                            ),
                            None,
                        )
                        if terminal is not None:
                            terminal.status = "FAILED"
                            terminal.last_error_json = execution.last_error_json
                    session.commit()
            raise

    def list_executions(self, project_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._project(session, project_id)
            rows = session.scalars(select(FamilyExecutionOrm).where(
                FamilyExecutionOrm.project_id == project_id,
                FamilyExecutionOrm.analysis_family == "PREDICTIVE",
                FamilyExecutionOrm.analysis_specification_id.is_not(None),
            ).order_by(FamilyExecutionOrm.requested_at.desc()))
            return [self._execution_response(row) for row in rows]

    def list_family_executions(self, project_id: str) -> list[dict[str, Any]]:
        """Return user-visible Generic Workflow executions across analysis families."""
        with self._session_factory() as session:
            self._project(session, project_id)
            rows = session.scalars(select(FamilyExecutionOrm).where(
                FamilyExecutionOrm.project_id == project_id,
                or_(
                    FamilyExecutionOrm.analysis_family != "PREDICTIVE",
                    FamilyExecutionOrm.analysis_specification_id.is_not(None),
                ),
            ).order_by(FamilyExecutionOrm.requested_at.desc()))
            return [self._execution_response(row) for row in rows]

    def get_execution(self, project_id: str, execution_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            return self._execution_response(self._execution(session, project_id, execution_id))

    def get_stages(self, project_id: str, execution_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._execution(session, project_id, execution_id)
            rows = session.scalars(select(FamilyStageExecutionOrm).where(
                FamilyStageExecutionOrm.execution_id == execution_id
            ).order_by(FamilyStageExecutionOrm.ordinal))
            return [self._stage_response(row) for row in rows]

    def list_results(self, project_id: str, execution_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._execution(session, project_id, execution_id)
            rows = session.scalars(select(FamilyResultOrm).where(
                FamilyResultOrm.execution_id == execution_id
            ).order_by(FamilyResultOrm.created_at))
            return [self._result_response(row) for row in rows]

    def list_artifacts(self, project_id: str, execution_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._execution(session, project_id, execution_id)
            rows = session.scalars(select(FamilyArtifactOrm).where(
                FamilyArtifactOrm.execution_id == execution_id
            ).order_by(FamilyArtifactOrm.created_at, FamilyArtifactOrm.artifact_id))
            return [self._artifact_response(row) for row in rows]

    def list_lineage(self, project_id: str, execution_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._execution(session, project_id, execution_id)
            result_ids = list(session.scalars(select(FamilyResultOrm.result_id).where(
                FamilyResultOrm.execution_id == execution_id
            )))
            artifact_ids = list(session.scalars(select(FamilyArtifactOrm.artifact_id).where(
                FamilyArtifactOrm.execution_id == execution_id
            )))
            owned_ids = {execution_id, *result_ids, *artifact_ids}
            rows = session.scalars(select(LineageEdgeOrm).where(
                LineageEdgeOrm.project_id == project_id,
                (
                    LineageEdgeOrm.source_id.in_(owned_ids)
                    | LineageEdgeOrm.target_id.in_(owned_ids)
                ),
            ).order_by(LineageEdgeOrm.created_at, LineageEdgeOrm.lineage_edge_id))
            return [self._lineage_response(row) for row in rows]

    def cancel(self, project_id: str, execution_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            row = self._execution(session, project_id, execution_id)
            if row.status not in {"QUEUED", "RUNNING"}:
                raise InvalidStateTransition("Execution", row.status, "CANCELLED")
            row.status = "CANCELLED"
            row.finished_at = _now()
            row.lease_expires_at = None
            row.worker_token = None
            for stage in session.scalars(select(FamilyStageExecutionOrm).where(
                FamilyStageExecutionOrm.execution_id == execution_id,
                FamilyStageExecutionOrm.status.in_(["PENDING", "READY"]),
            )):
                stage.status = "SKIPPED_DUE_TO_PREREQUISITE"
                stage.finished_at = row.finished_at
            session.commit()
            return self._execution_response(row)

    def retry(self, project_id: str, execution_id: str) -> dict[str, Any]:
        physical_keys: list[str] = []
        with self._session_factory() as session:
            row = self._execution(session, project_id, execution_id)
            if row.status != "FAILED":
                raise InvalidStateTransition("Execution", row.status, "QUEUED")
            results = list(session.scalars(select(FamilyResultOrm).where(
                FamilyResultOrm.execution_id == execution_id
            )))
            artifacts = list(session.scalars(select(FamilyArtifactOrm).where(
                FamilyArtifactOrm.execution_id == execution_id
            )))
            owned_ids = {result.result_id for result in results}
            owned_ids.update(artifact.artifact_id for artifact in artifacts)
            if owned_ids:
                for edge in session.scalars(select(LineageEdgeOrm).where(
                    (LineageEdgeOrm.source_id.in_(owned_ids))
                    | (LineageEdgeOrm.target_id.in_(owned_ids))
                )):
                    session.delete(edge)
            for artifact in artifacts:
                physical_keys.append(artifact.object_key)
                session.delete(artifact)
            for result in results:
                session.delete(result)
            row.status = "QUEUED"
            row.retry_count += 1
            row.last_error_json = None
            row.started_at = None
            row.finished_at = None
            row.worker_token = None
            row.worker_id = None
            for stage in session.scalars(select(FamilyStageExecutionOrm).where(
                FamilyStageExecutionOrm.execution_id == execution_id
            )):
                stage.status = "PENDING"
                stage.last_error_json = None
                stage.started_at = None
                stage.finished_at = None
                stage.attempt_history_json = []
                stage.input_binding_json = {}
                stage.output_binding_json = {}
            session.commit()
            response = self._execution_response(row)
        for key in physical_keys:
            self._store.delete(key)
        return response

    def rerun(self, project_id: str, execution_id: str, *, requested_by: str) -> dict[str, Any]:
        with self._session_factory() as session:
            base = self._execution(session, project_id, execution_id)
            if base.status not in {"SUCCEEDED", "FAILED", "CANCELLED"}:
                raise InvalidStateTransition("Execution", base.status, "RERUN")
            specification_id = str(base.analysis_specification_id)
            plan_id = base.execution_plan_id
            seed = int(base.snapshot_json["seed"])
        return self.submit_execution(
            project_id,
            specification_id=specification_id,
            plan_id=plan_id,
            seed=seed,
            requested_by=requested_by,
            base_execution_id=execution_id,
            revision_kind="RERUN",
        )

    def revise(
        self,
        project_id: str,
        execution_id: str,
        *,
        specification_id: str,
        seed: int,
        requested_by: str,
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            base = self._execution(session, project_id, execution_id)
            if base.status not in {"SUCCEEDED", "FAILED", "CANCELLED"}:
                raise InvalidStateTransition("Execution", base.status, "REVISED")
        plan = self.create_plan(project_id, specification_id)
        return self.submit_execution(
            project_id,
            specification_id=specification_id,
            plan_id=plan["execution_plan_id"],
            seed=seed,
            requested_by=requested_by,
            base_execution_id=execution_id,
            revision_kind="REVISED",
        )

    def prefill(self, project_id: str, execution_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            row = self._execution(session, project_id, execution_id)
            return {
                "base_execution_id": execution_id,
                "analysis_specification_id": row.analysis_specification_id,
                "execution_plan_id": row.execution_plan_id,
                "seed": row.snapshot_json["seed"],
                "revision_context": row.snapshot_json.get("revision"),
            }

    def capabilities(self, project_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._project(session, project_id)
        return {
            "schema_version": "predictive-capabilities/1",
            "gate": "G5_EXPLAIN_UI",
            "task_types": ["BINARY_CLASSIFICATION", "REGRESSION"],
            "split_strategies": ["RANDOM", "STRATIFIED", "GROUP", "TIME_BASED"],
            "preprocessing_steps": ["MEAN_IMPUTATION", "STANDARDIZATION", "ONE_HOT"],
            "model_registry": list(MODEL_REGISTRY),
            "metrics": {
                "BINARY_CLASSIFICATION": [
                    "ROC_AUC", "PR_AUC", "LOG_LOSS", "BRIER", "ACCURACY", "F1",
                ],
                "REGRESSION": ["MAE", "RMSE", "R2"],
            },
            "compatibility": {
                entry["model_id"]: entry["supported_tasks"] for entry in MODEL_REGISTRY
            },
            "explanation_methods": [{
                "method": "LINEAR_COEFFICIENT_CONTRIBUTION",
                "supported_models": [
                    "logistic_regression.v1",
                    "linear_regression.v1",
                ],
                "supports_global": True,
                "supports_local": True,
                "model_output_scales": ["LOG_ODDS", "PREDICTION"],
            }],
            "training_available": True,
            "evaluation_available": True,
            "explanation_available": True,
            "model_card_available": True,
        }

    @staticmethod
    def _runner_registry() -> StageRunnerRegistry:
        registry = StageRunnerRegistry()
        register_predictive_split_runner(registry)
        register_predictive_training_runners(registry)
        register_predictive_explain_runner(registry)
        return registry

    @staticmethod
    def _add_g5_lineage(
        session: Any,
        execution: FamilyExecutionOrm,
        result_ids: dict[str, str],
        artifact_ids: dict[str, str],
    ) -> None:
        explanation_id = result_ids.get("PREDICTIVE_EXPLANATION_RESULT")
        model_card_id = result_ids.get("MODEL_CARD_RESULT")
        if explanation_id:
            for artifact_type in (
                "FITTED_PREPROCESSOR",
                "FITTED_MODEL",
                "PREDICTION",
            ):
                artifact_id = artifact_ids.get(artifact_type)
                if artifact_id:
                    PredictiveWorkflowService._lineage(
                        session,
                        execution.project_id,
                        "Artifact",
                        artifact_id,
                        "USED_INPUT",
                        "Result",
                        explanation_id,
                        {"purpose": "predictive_explanation"},
                    )
        if not model_card_id:
            return
        for target_type, target_id in (
            ("AnalysisSpecification", execution.analysis_specification_id),
            ("DatasetVersion", execution.dataset_version_id),
            ("AnalysisView", execution.analysis_view_id),
        ):
            if target_id:
                PredictiveWorkflowService._lineage(
                    session,
                    execution.project_id,
                    "Result",
                    model_card_id,
                    "DOCUMENTS",
                    target_type,
                    target_id,
                    {"document": "model_card"},
                )
        for artifact_type in (
            "PARTITION_INDEX",
            "FITTED_PREPROCESSOR",
            "FITTED_MODEL",
            "PREDICTION",
        ):
            artifact_id = artifact_ids.get(artifact_type)
            if artifact_id:
                PredictiveWorkflowService._lineage(
                    session,
                    execution.project_id,
                    "Result",
                    model_card_id,
                    "SUMMARIZES",
                    "Artifact",
                    artifact_id,
                    {"artifact_type": artifact_type},
                )
        evaluation_id = result_ids.get("EVALUATION_RESULT")
        if evaluation_id:
            PredictiveWorkflowService._lineage(
                session,
                execution.project_id,
                "Result",
                model_card_id,
                "SUMMARIZES",
                "Result",
                evaluation_id,
                {"result_type": "EVALUATION_RESULT"},
            )

    @staticmethod
    def _planning_context(row: AnalysisSpecificationOrm) -> Any:
        from ariadne.product.workflow.contracts import PlanningContext

        return PlanningContext(PredictiveWorkflowService._specification_domain(row))

    @staticmethod
    def _specification_domain(row: AnalysisSpecificationOrm) -> AnalysisSpecification:
        return AnalysisSpecification(
            analysis_specification_id=row.analysis_specification_id,
            project_id=row.project_id,
            specification_key=row.specification_key,
            version_number=row.version_number,
            status=VersionedResourceStatus(row.status),
            analysis_family=AnalysisFamily(row.analysis_family),
            research_context_version_id=row.research_context_version_id,
            dataset_version_id=row.dataset_version_id,
            analysis_view_id=row.analysis_view_id,
            analysis_mode=AnalysisMode(row.analysis_mode),
            family_spec_schema_version=row.family_spec_schema_version,
            family_spec=dict(row.family_spec_json),
            revision_context=row.revision_context_json,
            warnings=list(row.warnings_json),
            canonical_hash=row.canonical_hash,
            created_by=row.created_by,
            created_at=row.created_at,
        )

    @staticmethod
    def _plan_domain(row: ExecutionPlanOrm) -> ExecutionPlan:
        stages = tuple(StageDefinition(
            stage_key=value["stage_key"],
            stage_type=StageType(**value["stage_type"]),
            input_contract=dict(value["input_contract"]),
            output_contract=dict(value["output_contract"]),
            parameters=dict(value["parameters"]),
            resource_policy=dict(value.get("resource_policy", {})),
            enabled=bool(value.get("enabled", True)),
        ) for value in row.stages_json)
        dependencies = tuple(StageBinding(**value) for value in row.dependencies_json)
        return ExecutionPlan(
            execution_plan_id=row.execution_plan_id,
            project_id=row.project_id,
            analysis_specification_id=row.analysis_specification_id,
            analysis_family=AnalysisFamily(row.analysis_family),
            planner_id=row.planner_id,
            planner_version=row.planner_version,
            stages=stages,
            dependencies=dependencies,
            plan_schema_version=row.plan_schema_version,
            plan_hash=row.plan_hash,
            created_at=row.created_at,
        )

    @staticmethod
    def _fixed_predictive_specification(
        session: Any, project_id: str, specification_id: str
    ) -> AnalysisSpecificationOrm:
        row = session.get(AnalysisSpecificationOrm, specification_id)
        if row is None or row.project_id != project_id:
            raise EntityNotFound("AnalysisSpecification", specification_id)
        if row.status != "FIXED":
            raise InvalidExecutionPlan("SPEC_NOT_FIXED", "Specification must be FIXED")
        if row.analysis_family != "PREDICTIVE":
            raise InvalidSchema("Predictive execution requires a PREDICTIVE Specification")
        return row

    @staticmethod
    def _project(session: Any, project_id: str) -> ProjectOrm:
        row = session.get(ProjectOrm, project_id)
        if row is None:
            raise EntityNotFound("Project", project_id)
        return row

    @classmethod
    def _active_project(cls, session: Any, project_id: str) -> ProjectOrm:
        row = cls._project(session, project_id)
        if row.status == "ARCHIVED":
            raise ProjectArchived(project_id)
        return row

    @staticmethod
    def _plan(session: Any, project_id: str, plan_id: str) -> ExecutionPlanOrm:
        row = session.get(ExecutionPlanOrm, plan_id)
        if row is None or row.project_id != project_id:
            raise EntityNotFound("ExecutionPlan", plan_id)
        return row

    @staticmethod
    def _execution(session: Any, project_id: str, execution_id: str) -> FamilyExecutionOrm:
        row = session.get(FamilyExecutionOrm, execution_id)
        if (
            row is None
            or row.project_id != project_id
            or row.analysis_family != "PREDICTIVE"
            or row.analysis_specification_id is None
        ):
            raise EntityNotFound("Execution", execution_id)
        return row

    @staticmethod
    def _plan_response(row: ExecutionPlanOrm) -> dict[str, Any]:
        return {
            "execution_plan_id": row.execution_plan_id,
            "project_id": row.project_id,
            "analysis_specification_id": row.analysis_specification_id,
            "analysis_family": row.analysis_family,
            "plan_schema_version": row.plan_schema_version,
            "planner_id": row.planner_id,
            "planner_version": row.planner_version,
            "stages": row.stages_json,
            "dependencies": row.dependencies_json,
            "plan_hash": row.plan_hash,
            "created_at": row.created_at,
        }

    @staticmethod
    def _execution_response(row: FamilyExecutionOrm) -> dict[str, Any]:
        return {
            "execution_id": row.execution_id,
            "project_id": row.project_id,
            "analysis_family": row.analysis_family,
            "research_context_version_id": row.research_context_version_id,
            "dataset_version_id": row.dataset_version_id,
            "analysis_view_id": row.analysis_view_id,
            "analysis_specification_id": row.analysis_specification_id,
            "execution_plan_id": row.execution_plan_id,
            "snapshot_hash": row.snapshot_hash,
            "snapshot": row.snapshot_json,
            "status": row.status,
            "retry_count": row.retry_count,
            "last_error": row.last_error_json,
            "requested_by": row.requested_by,
            "requested_at": row.requested_at,
            "started_at": row.started_at,
            "finished_at": row.finished_at,
        }

    @staticmethod
    def _stage_response(row: FamilyStageExecutionOrm) -> dict[str, Any]:
        return {
            "stage_execution_id": row.stage_execution_id,
            "stage_key": row.stage_key,
            "stage_type": row.stage_type_json,
            "ordinal": row.ordinal,
            "status": row.status,
            "attempt_history": row.attempt_history_json,
            "input_binding": row.input_binding_json,
            "output_binding": row.output_binding_json,
            "last_error": row.last_error_json,
            "started_at": row.started_at,
            "finished_at": row.finished_at,
        }

    @staticmethod
    def _result_response(row: FamilyResultOrm) -> dict[str, Any]:
        return {
            "result_id": row.result_id,
            "execution_id": row.execution_id,
            "stage_execution_id": row.stage_execution_id,
            "analysis_family": row.analysis_family,
            "result_type": row.result_type,
            "schema_version": row.schema_version,
            "analytical_status": row.analytical_status,
            "summary": row.summary_json,
            "payload": row.payload_json,
            "diagnostics": row.diagnostics_json,
            "warnings": row.warning_json,
        }

    @staticmethod
    def _artifact_response(row: FamilyArtifactOrm) -> dict[str, Any]:
        return {
            "artifact_id": row.artifact_id,
            "execution_id": row.execution_id,
            "stage_execution_id": row.stage_execution_id,
            "result_id": row.result_id,
            "analysis_family": row.family,
            "family": row.family,
            "artifact_type": row.artifact_type,
            "schema_version": row.schema_version,
            "media_type": row.media_type,
            "content_hash": row.content_hash,
            "size_bytes": row.size_bytes,
            "metadata": row.metadata_json,
        }

    @staticmethod
    def _lineage_response(row: LineageEdgeOrm) -> dict[str, Any]:
        return {
            "lineage_edge_id": row.lineage_edge_id,
            "source_type": row.source_type,
            "source_id": row.source_id,
            "relation_type": row.relation_type,
            "target_type": row.target_type,
            "target_id": row.target_id,
            "evidence": row.evidence_json,
        }

    @staticmethod
    def _validate_result(result_type: str, status: str) -> None:
        allowed = {
            "SPLIT_RESULT": {"PASS", "WARN", "FAIL"},
            "TRAINING_RESULT": {"TRAINED", "TRAINED_WITH_WARNINGS", "FAILED_VALIDATION"},
            "EVALUATION_RESULT": {
                "EVALUATED", "EVALUATED_WITH_WARNINGS", "INSUFFICIENT_TEST_SAMPLE",
            },
            "ERROR_ANALYSIS_RESULT": {"GENERATED", "GENERATED_WITH_WARNINGS"},
            "PREDICTIVE_EXPLANATION_RESULT": {
                "GENERATED", "GENERATED_WITH_WARNINGS", "NOT_APPLICABLE",
            },
            "MODEL_CARD_RESULT": {"GENERATED", "GENERATED_WITH_WARNINGS"},
        }
        if result_type not in allowed or status not in allowed[result_type]:
            raise InvalidSchema(f"Invalid Predictive Result status: {result_type}/{status}")

    def _store_draft(self, content: bytes, object_key: str, media_type: str) -> Any:
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            handle.write(content)
            path = Path(handle.name)
        try:
            return self._store.store(path, object_key, media_type)
        finally:
            path.unlink(missing_ok=True)

    @staticmethod
    def _lineage(
        session: Any,
        project_id: str,
        source_type: str,
        source_id: str,
        relation_type: str,
        target_type: str,
        target_id: str,
        evidence: dict[str, Any],
    ) -> None:
        session.add(LineageEdgeOrm(
            lineage_edge_id=str(uuid.uuid4()),
            project_id=project_id,
            source_type=source_type,
            source_id=source_id,
            relation_type=relation_type,
            target_type=target_type,
            target_id=target_id,
            evidence_json=evidence,
            created_by="system",
            created_at=_now(),
        ))


def _binding_summary(value: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, pd.DataFrame):
            summary[key] = {"kind": "dataframe", "rows": len(item), "columns": list(item.columns)}
        elif isinstance(item, dict):
            summary[key] = {
                "schema_version": item.get("schema_version"),
                "canonical_hash": item.get("canonical_hash"),
                "keys": sorted(item),
            }
        else:
            summary[key] = {"kind": type(item).__name__}
    return summary


def _write_stage_state(row: FamilyStageExecutionOrm, stage: Any) -> None:
    row.status = stage.status.value
    row.started_at = stage.started_at
    row.finished_at = stage.finished_at
    row.last_error_json = stage.last_error
    row.input_binding_json = _binding_summary(stage.input_binding)
    row.output_binding_json = _binding_summary(stage.output_binding)
    row.attempt_history_json = [
        {
            "attempt_number": attempt.attempt_number,
            "worker_id": attempt.worker_id,
            "started_at": attempt.started_at.isoformat(),
            "finished_at": (
                attempt.finished_at.isoformat() if attempt.finished_at else None
            ),
            "error": attempt.error,
        }
        for attempt in stage.attempts
    ]


def _now() -> datetime:
    return datetime.now(timezone.utc)
