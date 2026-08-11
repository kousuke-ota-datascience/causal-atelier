"""Application service for G3 predictive specification and split validation."""

from __future__ import annotations

import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import select

from ariadne.capabilities.predictive import (
    PredictivePlanner,
    register_predictive_split_runner,
    validate_predictive_specification,
)
from ariadne.product.application.analysis_frame_service import AnalysisFrameProvider
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidSchema,
    LegacyProductAuthorityDisabled,
    PredictiveValidationError,
    ProjectArchived,
)
from ariadne.product.domain.schemas import SchemaRegistry, canonical_hash
from ariadne.product.persistence.orm_models import (
    ExecutionPlanOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyStageExecutionOrm,
    LineageEdgeOrm,
    ProjectOrm,
)
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry

PREDICTIVE_SCHEMA_VERSION = "predictive-analysis-spec/1"
_PREDICTIVE_SCHEMAS = SchemaRegistry()
_PREDICTIVE_SCHEMAS.register(PREDICTIVE_SCHEMA_VERSION, validate_predictive_specification)


class PredictiveSplitService:
    """Retained historical partition-artifact reader.

    Split validation used to create a second, Family-ORM execution lifecycle.
    G05 deliberately does not retain that Product mutation authority: predictive
    submission is owned by ``PredictiveWorkflowService`` and canonical
    ``ExecutionService``.
    """

    def __init__(
        self,
        session_factory: Any,
        artifact_store: ArtifactStorePort,
        *,
        execution_service: ExecutionService,
    ) -> None:
        self._session_factory = session_factory
        self._store = artifact_store
        self._execution_service = execution_service
        self._frames = AnalysisFrameProvider(session_factory, artifact_store)

    def validate_and_save(
        self,
        project_id: str,
        *,
        dataset_version_id: str,
        analysis_view_id: str | None,
        family_spec: dict[str, Any],
        requested_by: str = "system",
    ) -> dict[str, Any]:
        """Reject the retired Family-ORM split-validation write lifecycle.

        The retained implementation below is intentionally unreachable until it
        can be removed after historical data retirement.  It must never become a
        fallback when canonical predictive submission fails.
        """
        raise LegacyProductAuthorityDisabled("PredictiveSplitService.validate_and_save")

        _PREDICTIVE_SCHEMAS.validate(PREDICTIVE_SCHEMA_VERSION, family_spec)
        with self._session_factory() as session:
            project = session.get(ProjectOrm, project_id)
            if project is None:
                raise EntityNotFound("Project", project_id)
            if project.status == "ARCHIVED":
                raise ProjectArchived(project_id)
        frame, view_manifest = self._frames.load(
            project_id, dataset_version_id, analysis_view_id,
        )
        specification_id = canonical_hash({
            "schema_version": PREDICTIVE_SCHEMA_VERSION,
            "dataset_version_id": dataset_version_id,
            "analysis_view_id": analysis_view_id,
            "family_spec": family_spec,
        })
        plan = PredictivePlanner().build_for_spec(
            project_id=project_id,
            specification_id=specification_id,
            family_spec=family_spec,
        )
        execution_id = str(uuid.uuid4())
        source_snapshot = {
            "schema_version": "predictive-source-snapshot/1",
            "dataset_version_id": dataset_version_id,
            "dataset_content_hash": view_manifest["source_dataset_content_hash"],
            "analysis_view_id": analysis_view_id,
            "analysis_view_hash": view_manifest["view_spec_hash"] if analysis_view_id else None,
            "materialized_hash": view_manifest["materialized_hash"],
        }
        registry = StageRunnerRegistry()
        register_predictive_split_runner(registry)
        outcome = GenericExecutor(registry).execute(
            execution_id,
            plan,
            external_inputs={plan.stages[0].stage_key: {
                "frame": frame,
                "source_snapshot": source_snapshot,
            }},
            snapshots={"specification_hash": specification_id, **source_snapshot},
        )
        if outcome.status != "SUCCEEDED" or len(outcome.artifacts) != 1:
            error = outcome.stages[-1].last_error or {"message": "Predictive split failed"}
            if error.get("type") == "PredictiveValidationError":
                raise PredictiveValidationError(
                    str(error.get("code", "PREDICTIVE_SPLIT_INVALID")),
                    str(error.get("message", "Predictive split validation failed")),
                    path=error.get("path"),
                )
            if error.get("type") == "InvalidSchema":
                raise InvalidSchema(str(error.get("message", "Predictive split schema is invalid")))
            raise ValueError(str(error.get("message", error)))
        artifact_draft = outcome.artifacts[0]
        artifact_id = str(uuid.uuid4())
        object_key = f"projects/{project_id}/executions/{execution_id}/{artifact_id}.json"
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            handle.write(artifact_draft.content)
            temporary = Path(handle.name)
        try:
            stored = self._store.store(temporary, object_key, artifact_draft.media_type)
        finally:
            temporary.unlink(missing_ok=True)
        now = _now()
        stage_id = str(uuid.uuid4())
        snapshot = {
            "schema_version": "family-execution-snapshot/1",
            "analysis_family": "PREDICTIVE",
            "source": source_snapshot,
            "specification_hash": specification_id,
            "plan_hash": plan.plan_hash,
            "runtime": {"runner": "predictive.split/1"},
        }
        try:
            with self._session_factory() as session:
                plan_row = session.scalar(select(ExecutionPlanOrm).where(
                    ExecutionPlanOrm.plan_hash == plan.plan_hash
                ))
                if plan_row is None:
                    plan_row = ExecutionPlanOrm(
                        execution_plan_id=plan.execution_plan_id,
                        project_id=project_id,
                        analysis_specification_id=specification_id,
                        analysis_family="PREDICTIVE",
                        plan_schema_version=plan.plan_schema_version,
                        planner_id=plan.planner_id,
                        planner_version=plan.planner_version,
                        stages_json=[stage.as_dict() for stage in plan.stages],
                        dependencies_json=[binding.as_dict() for binding in plan.dependencies],
                        plan_hash=plan.plan_hash,
                        created_at=now,
                    )
                    session.add(plan_row)
                    session.flush()
                session.add(FamilyExecutionOrm(
                    execution_id=execution_id,
                    project_id=project_id,
                    dataset_version_id=dataset_version_id,
                    analysis_view_id=analysis_view_id,
                    execution_plan_id=plan_row.execution_plan_id,
                    analysis_family="PREDICTIVE",
                    specification_schema_version=PREDICTIVE_SCHEMA_VERSION,
                    specification_snapshot_json=family_spec,
                    snapshot_json=snapshot,
                    snapshot_hash=canonical_hash(snapshot),
                    status="SUCCEEDED",
                    retry_count=0,
                    requested_by=requested_by,
                    requested_at=now,
                    started_at=now,
                    finished_at=now,
                ))
                session.flush()
                output = outcome.stages[0].output_binding["partition_manifest"]
                session.add(FamilyStageExecutionOrm(
                    stage_execution_id=stage_id,
                    execution_id=execution_id,
                    stage_key="split",
                    stage_type_json=plan.stages[0].stage_type.as_dict(),
                    ordinal=0,
                    status="SUCCEEDED",
                    attempt_history_json=[{
                        "attempt_number": 1,
                        "worker_id": "predictive-split-validation-api",
                        "started_at": now.isoformat(),
                        "finished_at": now.isoformat(),
                    }],
                    input_binding_json={"source_snapshot": source_snapshot},
                    output_binding_json={
                        "partition_artifact_id": artifact_id,
                        "partition_manifest": output,
                    },
                    started_at=now,
                    finished_at=now,
                ))
                session.flush()
                metadata = {
                    **artifact_draft.metadata,
                    "source_snapshot": source_snapshot,
                    "view_manifest": view_manifest,
                }
                session.add(FamilyArtifactOrm(
                    artifact_id=artifact_id,
                    project_id=project_id,
                    execution_id=execution_id,
                    stage_execution_id=stage_id,
                    result_id=None,
                    family="PREDICTIVE",
                    artifact_type=artifact_draft.artifact_type,
                    schema_version=artifact_draft.schema_version,
                    media_type=stored.media_type,
                    object_key=stored.object_key,
                    content_hash=stored.content_hash,
                    size_bytes=stored.size_bytes,
                    metadata_json=metadata,
                    created_at=now,
                ))
                self._lineage(
                    session, project_id, "DatasetVersion", dataset_version_id,
                    "USED_INPUT", "Execution", execution_id,
                    {"dataset_content_hash": source_snapshot["dataset_content_hash"]}, now,
                )
                if analysis_view_id:
                    self._lineage(
                        session, project_id, "AnalysisView", analysis_view_id,
                        "USED_INPUT", "Execution", execution_id,
                        {"analysis_view_hash": source_snapshot["analysis_view_hash"]}, now,
                    )
                self._lineage(
                    session, project_id, "Execution", execution_id,
                    "GENERATED", "Artifact", artifact_id,
                    {"content_hash": stored.content_hash, "schema_version": artifact_draft.schema_version}, now,
                )
                session.commit()
        except Exception:
            self._store.delete(stored.object_key)
            raise
        return {
            "schema_version": "predictive-split-validation/1",
            "status": "VALID",
            "execution_id": execution_id,
            "task_type": family_spec["task_type"],
            "strategy": family_spec["split_spec"]["strategy"],
            "partition_counts": outcome.stages[0].output_binding["partition_manifest"]["partition_counts"],
            "partition_artifact": {
                "artifact_id": artifact_id,
                "schema_version": artifact_draft.schema_version,
                "content_hash": stored.content_hash,
                "size_bytes": stored.size_bytes,
                "selection_contract": artifact_draft.metadata["selection_contract"],
            },
            "source_snapshot": source_snapshot,
        }

    def get_partition_artifact(self, project_id: str, artifact_id: str) -> FamilyArtifactOrm:
        """Return a bounded read-only projection of a historical Family artifact."""
        with self._session_factory() as session:
            artifact = session.get(FamilyArtifactOrm, artifact_id)
            if (
                artifact is None or artifact.project_id != project_id
                or artifact.family != "PREDICTIVE" or artifact.artifact_type != "PARTITION_INDEX"
            ):
                raise EntityNotFound("PartitionArtifact", artifact_id)
            return artifact

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
        created_at: datetime,
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
            created_at=created_at,
        ))


def _now() -> datetime:
    return datetime.now(timezone.utc)
