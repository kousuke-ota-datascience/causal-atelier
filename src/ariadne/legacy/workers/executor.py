"""Transactional-outbox worker connected to the existing stage runners."""

from __future__ import annotations

import logging
import os
import shutil
import socket
import traceback
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from ariadne import __version__

from ariadne.application.pipeline.discovery import DiscoveryStageRunner
from ariadne.application.analysis_ready import AnalysisReadyExecutor
from ariadne.application.pipeline.etl import execute_completejourney_etl
from ariadne.application.pipeline.inference import InferenceStageRunner
from ariadne.application.pipeline.planning import StagePlan
from ariadne.application.data_catalog import DataCatalogService
from ariadne.application.run_execution import ExecutionService
from ariadne.infrastructure.artifact_store import (
    artifact_location,
    build_artifact_store,
)
from ariadne.infrastructure.data_query import PyArrowQueryEngine
from ariadne.infrastructure.persistence import Database
from ariadne.infrastructure.persistence import models as m
from ariadne.infrastructure.settings import WebSettings
from ariadne.infrastructure.tracking.exceptions import (
    TrackingDisabledError,
    TrackingDuplicateRunError,
    TrackingError,
)
from ariadne.infrastructure.tracking.redaction import redact_secret
from ariadne.infrastructure.tracking.settings import TrackingSettings
from ariadne.workers.materialization import WorkspaceMaterializer
from ariadne.workers.projection import WorkerProjectionService
from ariadne.workers.state_management import OutboxConsumer, ExecutionStateManager

logger = logging.getLogger(__name__)


class Worker:
    """Poll and execute durable outbox work one item at a time."""

    def __init__(
        self, database: Database, settings: WebSettings, *, worker_id: str | None = None
    ) -> None:
        self.database = database
        self.settings = settings
        self.worker_id = worker_id or f"{socket.gethostname()}:{os.getpid()}"
        self.store = build_artifact_store(settings)
        self.query_engine = PyArrowQueryEngine(
            max_result_rows=settings.query_max_result_rows,
            max_sample_rows=settings.query_max_sample_rows,
        )
        self.outbox = OutboxConsumer(
            database,
            worker_id=self.worker_id,
            lease_seconds=settings.worker_lease_seconds,
        )
        self.materializer = WorkspaceMaterializer(self.store)
        self.projection = WorkerProjectionService(self.store, self.query_engine)
        self.run_state = ExecutionStateManager(
            worker_id=self.worker_id,
            lease_seconds=settings.worker_lease_seconds,
            workspace_root=settings.workspace_root,
        )
        self.tracker = self._build_tracker()

    def run_once(self) -> bool:
        return self.outbox.consume_one(self._dispatch)

    def _build_tracker(self) -> Any:
        from ariadne.infrastructure.tracking.null_tracker import NullTracker
        if not self.settings.mlflow_enabled:
            return NullTracker()
        from ariadne.infrastructure.tracking.mlflow_tracker import MlflowTracker
        from ariadne.infrastructure.tracking.settings import TrackingSettings
        ts = TrackingSettings(
            tracking_uri=self.settings.mlflow_tracking_uri,
            experiment_name=self.settings.mlflow_experiment_name,
            enabled=True,
            timeout_seconds=self.settings.mlflow_timeout_seconds,
            tag_prefix=self.settings.mlflow_tag_prefix,
            max_retry_attempts=3,
        )
        return MlflowTracker(ts)

    def _ensure_mlflow_run(self, session: Session, run: m.Execution) -> None:
        """Ensure a MLflow Run exists for this execution and save it to DB.

        Implements idempotent ensure per section 6.2 of the MLflow coding spec.
        On tracking errors, the error is recorded and execution continues.
        """
        if not self.settings.mlflow_enabled or run.mlflow_tracking_status == "NOT_REQUIRED":
            return
        if run.mlflow_run_id:
            run.mlflow_tracking_status = "ACTIVE"
            return
        experiment_name = self.settings.mlflow_experiment_name
        tags: dict[str, str] = {
            "ariadne.execution_origin": "WEB",
            "ariadne.execution_id": run.id,
            "ariadne.project_id": run.project_id,
            "ariadne.execution_mode": run.execution_mode,
        }
        if run.pipeline_definition_version_id:
            tags["ariadne.pipeline_definition_version_id"] = run.pipeline_definition_version_id
        if run.code_commit:
            tags["ariadne.code_commit"] = run.code_commit
        try:
            ref = self.tracker.create_or_resume_run(
                experiment_name=experiment_name,
                tags=tags,
                execution_id=run.id,
            )
            run.mlflow_experiment_id = ref.experiment_id
            run.mlflow_run_id = ref.run_id
            run.mlflow_tracking_status = "ACTIVE"
            logger.info(
                "MLflow Run ensured: execution_id=%s run_id=%s", run.id, ref.run_id
            )
        except TrackingDuplicateRunError as exc:
            run.mlflow_tracking_status = "ERROR"
            run.mlflow_tracking_error = redact_secret(str(exc))
            logger.error("Duplicate MLflow runs for execution %s: %s", run.id, exc)
        except TrackingDisabledError:
            pass
        except TrackingError as exc:
            run.mlflow_tracking_status = "ERROR"
            run.mlflow_tracking_error = redact_secret(str(exc))
            logger.error("MLflow ensure failed for execution %s: %s", run.id, exc)

    def _terminate_mlflow_run(
        self, session: Session, run: m.Execution, mlflow_status: str
    ) -> None:
        """Terminate the MLflow Run and update tracking status.  Errors are recorded, not raised."""
        if not self.settings.mlflow_enabled or not run.mlflow_run_id:
            return
        try:
            self.tracker.terminate_run(run.mlflow_run_id, mlflow_status)
            run.mlflow_tracking_status = "FINISHED"
        except TrackingError as exc:
            run.mlflow_tracking_status = "ERROR"
            run.mlflow_tracking_error = redact_secret(str(exc))
            logger.error("Failed to terminate MLflow run %s: %s", run.mlflow_run_id, exc)

    def _dispatch(self, session: Session, event: m.OutboxEvent) -> None:
        if event.event_type == "EXECUTE_EXECUTION":
            self.execute_run(session, event.payload_json["execution_id"])
        elif event.event_type == "CANCEL_EXECUTION":
            self.cancel_run(session, event.payload_json["execution_id"])
        elif event.event_type == "PROFILE_DATASET_TABLE":
            self.projection.profile_table(
                session,
                event.payload_json["dataset_table_version_id"],
                event.payload_json["profile_id"],
            )
        elif event.event_type == "EXECUTE_VISUALIZATION_QUERY":
            self.projection.execute_visualization_query(
                session, event.payload_json["query_id"]
            )
        else:
            raise ValueError(f"Unsupported outbox event: {event.event_type}")

    def execute_run(self, session: Session, execution_id: str) -> None:
        run = session.get(m.Execution, execution_id)
        if not run or run.status in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            return
        service = ExecutionService(session)
        if run.status == "CANCEL_REQUESTED":
            self._finish_cancelled(session, run, service)
            return
        run.status = "VALIDATING"
        service.add_event(run.id, "EXECUTION_VALIDATING", {})
        validation = session.scalar(
            select(m.ValidationExecution)
            .where(m.ValidationExecution.execution_id == run.id)
            .order_by(m.ValidationExecution.started_at.desc())
        )
        if validation and validation.status == "INVALID":
            run.status = "FAILED"
            run.error_code = "VALIDATION_FAILED"
            run.error_summary = "Run plan validation failed"
            run.finished_at = m.utcnow()
            service.add_event(run.id, "EXECUTION_FAILED", {"error_code": run.error_code})
            return
        run.status = "RUNNING"
        run.started_at = m.utcnow()
        service.add_event(run.id, "EXECUTION_STARTED", {"worker_id": self.worker_id})
        self._ensure_mlflow_run(session, run)
        session.commit()
        stages = session.scalars(
            select(m.StageExecution)
            .where(m.StageExecution.execution_id == run.id)
            .order_by(m.StageExecution.ordinal)
        ).all()
        workspace_outputs: dict[str, Path] = {}
        try:
            for stage in stages:
                session.refresh(run)
                if run.status == "CANCEL_REQUESTED":
                    self._finish_cancelled(session, run, service)
                    return
                if stage.status == "SUCCEEDED":
                    continue
                self._bind_dependency_artifacts(session, stage)
                attempt = self._create_attempt(session, stage)
                service.add_event(
                    run.id,
                    "STAGE_STARTED",
                    {
                        "stage_key": stage.stage_key,
                        "attempt_number": attempt.attempt_number,
                    },
                    stage_execution_id=stage.id,
                    attempt_id=attempt.id,
                )
                session.commit()
                try:
                    output_dir = self._execute_stage(
                        session, run, stage, attempt, workspace_outputs
                    )
                    workspace_outputs[stage.stage_key] = output_dir
                    attempt.status = "SUCCEEDED"
                    attempt.finished_at = m.utcnow()
                    attempt.exit_code = 0
                    stage.status = "SUCCEEDED"
                    stage.selected_attempt_id = attempt.id
                    stage.finished_at = m.utcnow()
                    preparation = session.get(
                        m.StageAttemptInputPreparation, attempt.id
                    )
                    if preparation:
                        preparation.status = "SUCCEEDED"
                        preparation.finished_at = m.utcnow()
                    service.add_event(
                        run.id,
                        "STAGE_SUCCEEDED",
                        {"stage_key": stage.stage_key},
                        stage_execution_id=stage.id,
                        attempt_id=attempt.id,
                    )
                    session.commit()
                except Exception as exc:
                    attempt_id = attempt.id
                    stage_id = stage.id
                    session.rollback()
                    attempt = session.get(m.StageAttempt, attempt_id)
                    stage = session.get(m.StageExecution, stage_id)
                    attempt.status = "FAILED"
                    attempt.finished_at = m.utcnow()
                    attempt.exit_code = 1
                    attempt.error_class = type(exc).__name__
                    attempt.error_code = "STAGE_EXECUTION_FAILED"
                    attempt.error_message = str(exc)[:4000]
                    attempt.error_detail_json = {
                        "traceback": traceback.format_exc(limit=20)
                    }
                    preparation = session.get(
                        m.StageAttemptInputPreparation, attempt.id
                    )
                    if preparation:
                        preparation.status = "FAILED"
                        preparation.error_summary = str(exc)[:4000]
                        preparation.finished_at = m.utcnow()
                    stage.status = "FAILED"
                    stage.error_code = attempt.error_code
                    stage.error_summary = attempt.error_message
                    stage.finished_at = m.utcnow()
                    raise
            run.status = "SUCCEEDED"
            run.finished_at = m.utcnow()
            service.add_event(run.id, "EXECUTION_SUCCEEDED", {})
            self._terminate_mlflow_run(session, run, "FINISHED")
        except Exception as exc:
            run = session.get(m.Execution, execution_id)
            run.status = "FAILED"
            run.finished_at = m.utcnow()
            run.error_code = "STAGE_EXECUTION_FAILED"
            run.error_summary = str(exc)[:4000]
            service.add_event(
                run.id,
                "EXECUTION_FAILED",
                {"error_code": run.error_code, "error_summary": run.error_summary},
            )
            self._terminate_mlflow_run(session, run, "FAILED")

    def cancel_run(self, session: Session, execution_id: str) -> None:
        run = session.get(m.Execution, execution_id)
        if run and run.status == "CANCEL_REQUESTED":
            self._finish_cancelled(session, run, ExecutionService(session))

    def _create_attempt(self, session: Session, stage: m.StageExecution) -> m.StageAttempt:
        attempt = self.run_state.create_attempt(session, stage)
        requested = session.get(m.StageExecutionInputPreparation, stage.id)
        if requested:
            session.add(
                m.StageAttemptInputPreparation(
                    stage_attempt_id=attempt.id,
                    stage_execution_id=stage.id,
                    input_mode=stage.input_mode,
                    actual_selected_columns_json=requested.requested_columns_json,
                    excluded_columns_json=[],
                    resolved_conditioning_json=requested.conditioning_spec_json,
                    status="RUNNING",
                )
            )
        return attempt

    def _execute_stage(
        self,
        session: Session,
        run: m.Execution,
        stage: m.StageExecution,
        attempt: m.StageAttempt,
        upstream_workspaces: dict[str, Path],
    ) -> Path:
        workspace = Path(attempt.workspace_ref)
        output_dir = workspace / "outputs"
        output_dir.mkdir(parents=True)
        if stage.stage_type == "ETL":
            etl_outputs = self._run_etl(session, run, stage, workspace, output_dir)
            self._register_stage_outputs(
                session,
                run,
                stage,
                attempt,
                output_dir,
                etl_outputs,
            )
            return output_dir
        if stage.input_mode == "ANALYSIS_READY":
            parameters = {
                row.parameter_name: row.value_json
                for row in session.scalars(
                    select(m.StageExecutionParameter).where(
                        m.StageExecutionParameter.stage_execution_id == stage.id
                    )
                ).all()
            }
            artifacts, resolved = AnalysisReadyExecutor(self.store).execute(
                session, stage, output_dir, parameters
            )
            attempt_preparation = session.get(
                m.StageAttemptInputPreparation, attempt.id
            )
            if attempt_preparation:
                for name, value in resolved.items():
                    setattr(attempt_preparation, name, value)
            self._register_stage_outputs(
                session, run, stage, attempt, output_dir, artifacts
            )
            if attempt_preparation:
                feature_output = session.get(
                    m.StageExecutionArtifactOutput, (stage.id, "feature_frame")
                )
                preparation_output = session.get(
                    m.StageExecutionArtifactOutput, (stage.id, "input_preparation")
                )
                attempt_preparation.feature_frame_artifact_id = (
                    feature_output.artifact_id if feature_output else None
                )
                attempt_preparation.resolved_preparation_artifact_id = (
                    preparation_output.artifact_id if preparation_output else None
                )
            self._project_results(session, run, stage, artifacts, output_dir)
            return output_dir
        config_paths = self._materialize_configs(session, stage, workspace)
        dataset_yaml = self._materialize_dataset(session, stage, workspace)
        parameters = {
            row.parameter_name: row.value_json
            for row in session.scalars(
                select(m.StageExecutionParameter).where(
                    m.StageExecutionParameter.stage_execution_id == stage.id
                )
            ).all()
        }
        if stage.stage_type == "DISCOVERY":
            plan = self._discovery_plan(
                stage, workspace, output_dir, config_paths, dataset_yaml, parameters
            )
            runner = DiscoveryStageRunner()
        elif stage.stage_type == "INFERENCE":
            manifest = self._materialize_discovery_manifest(
                session,
                stage,
                workspace,
                upstream_workspaces,
            )
            plan = self._inference_plan(
                stage,
                workspace,
                output_dir,
                config_paths,
                dataset_yaml,
                manifest,
                parameters,
            )
            runner = InferenceStageRunner()
        else:
            raise ValueError(f"Unsupported stage type: {stage.stage_type}")
        issues = runner.validate_plan(plan)
        errors = [issue for issue in issues if issue.severity.value == "error"]
        if errors:
            raise ValueError("; ".join(issue.message for issue in errors))
        session.commit()
        raw_result = runner.run(plan)
        artifacts = {
            name: Path(path) for name, path in raw_result.get("artifacts", {}).items()
        }
        self._register_stage_outputs(
            session, run, stage, attempt, output_dir, artifacts
        )
        self._project_results(session, run, stage, artifacts, output_dir)
        return output_dir

    def _run_etl(
        self,
        session: Session,
        run: m.Execution,
        stage: m.StageExecution,
        workspace: Path,
        output_dir: Path,
    ) -> dict[str, Path]:
        raw_dir = workspace / "data/00_raw/completejourney/rdata"
        raw_dir.mkdir(parents=True)
        inputs = session.scalars(
            select(m.StageExecutionDatasetInput).where(
                m.StageExecutionDatasetInput.stage_execution_id == stage.id
            )
        ).all()
        if not inputs:
            raise ValueError("Complete Journey ETL requires a raw Dataset Version")
        tables = session.scalars(
            select(m.DatasetTableVersion).where(
                m.DatasetTableVersion.dataset_version_id == inputs[0].dataset_version_id
            )
        ).all()
        for table in tables:
            stored = session.get(m.StoredObject, table.stored_object_id)
            source = self.store.resolve_local_path(artifact_location(stored))
            extension = source.suffix or f".{table.file_format.lower()}"
            shutil.copyfile(source, raw_dir / f"{table.logical_name}{extension}")
        session.commit()
        outputs = execute_completejourney_etl(workspace)
        target_dataset_id = self._parameter(session, stage.id, "output_dataset_id")
        dataset = (
            session.get(m.Dataset, target_dataset_id) if target_dataset_id else None
        )
        if not dataset:
            dataset = m.Dataset(
                project_id=run.project_id,
                slug=f"etl-{run.id[:12]}",
                name=f"ETL output {run.id[:12]}",
                dataset_kind="PROCESSED",
                created_by=run.submitted_by,
            )
            session.add(dataset)
            session.flush()
        table_requests = []
        for name, path in outputs.items():
            object_info = self.store.put_file(path)
            table_requests.append(
                {
                    "logical_name": name,
                    "object": {
                        "backend": object_info.location.backend,
                        "namespace": object_info.location.namespace,
                        "key": object_info.location.key,
                        "version": object_info.location.version,
                        "media_type": "application/vnd.apache.parquet",
                        "format": "PARQUET",
                        "size_bytes": object_info.size_bytes,
                        "checksum": object_info.checksum,
                    },
                }
            )
        version = DataCatalogService(
            session, self.store, self.query_engine
        ).create_version(
            dataset=dataset,
            actor_user_id=run.submitted_by,
            source_type="ETL",
            source_metadata={
                "execution_id": run.id,
                "stage_execution_id": stage.id,
                "etl_type": "COMPLETE_JOURNEY",
            },
            tables=table_requests,
            profile=True,
        )
        version.origin_stage_execution_id = stage.id
        return {f"dataset_{name}": path for name, path in outputs.items()}

    def _materialize_configs(
        self, session: Session, stage: m.StageExecution, workspace: Path
    ) -> dict[str, Path]:
        return self.materializer.configurations(session, stage, workspace)

    def _materialize_dataset(
        self, session: Session, stage: m.StageExecution, workspace: Path
    ) -> Path:
        return self.materializer.dataset(session, stage, workspace)

    def _materialize_discovery_manifest(
        self,
        session: Session,
        stage: m.StageExecution,
        workspace: Path,
        upstream_workspaces: dict[str, Path],
    ) -> Path:
        return self.materializer.discovery_manifest(
            session, stage, workspace, upstream_workspaces
        )

    def _discovery_plan(
        self,
        stage: m.StageExecution,
        workspace: Path,
        output_dir: Path,
        configs: dict[str, Path],
        dataset_yaml: Path,
        parameters: dict[str, Any],
    ) -> StagePlan:
        analysis = configs.get("analysis_config") or configs.get("config")
        features = configs.get("feature_config")
        if not analysis or not features:
            raise ValueError("Discovery requires analysis_config and feature_config")
        args = [
            "--project-root",
            str(workspace),
            "--analysis-config",
            str(analysis),
            "--feature-config",
            str(features),
            "--dataset-yaml",
            str(dataset_yaml),
            "--output-dir",
            str(output_dir),
        ]
        _append_parameters(args, parameters, _DISCOVERY_PARAMETERS)
        return StagePlan(
            name="discovery",
            enabled=True,
            input_paths={},
            output_paths={
                "output_dir": output_dir,
                "manifest": output_dir / "manifest.yaml",
            },
            config_paths={"analysis_config": analysis, "feature_config": features},
            resolved_args=args,
            metadata={"stage_execution_id": stage.id},
        )

    def _inference_plan(
        self,
        stage: m.StageExecution,
        workspace: Path,
        output_dir: Path,
        configs: dict[str, Path],
        dataset_yaml: Path,
        manifest: Path,
        parameters: dict[str, Any],
    ) -> StagePlan:
        analysis = configs.get("config") or configs.get("analysis_config")
        features = configs.get("feature_config")
        if not analysis or not features:
            raise ValueError(
                "Inference requires analysis_config/config and feature_config"
            )
        mode = (
            "edge_weight"
            if stage.analysis_mode == "EDGE_WEIGHT"
            else "treatment_effect"
        )
        args = [
            "--project-root",
            str(workspace),
            "--config",
            str(analysis),
            "--feature-config",
            str(features),
            "--dataset-yaml",
            str(dataset_yaml),
            "--discovery-manifest",
            str(manifest),
            "--output-dir",
            str(output_dir),
            "--mode",
            mode,
        ]
        _append_parameters(args, parameters, _INFERENCE_PARAMETERS)
        config_paths = {"config": analysis, "feature_config": features}
        config_paths.update(
            {
                name: path
                for name, path in configs.items()
                if name in {"causal_design", "feature_semantics"}
            }
        )
        return StagePlan(
            name="inference",
            enabled=True,
            input_paths={
                "discovery_manifest": manifest,
                **{
                    name: path
                    for name, path in configs.items()
                    if name in {"causal_design", "feature_semantics"}
                },
            },
            output_paths={
                "output_dir": output_dir,
                "manifest": output_dir / "manifest.yaml",
            },
            config_paths=config_paths,
            resolved_args=args,
            metadata={"stage_execution_id": stage.id, "analysis_mode": stage.analysis_mode},
        )

    def _register_stage_outputs(
        self,
        session: Session,
        run: m.Execution,
        stage: m.StageExecution,
        attempt: m.StageAttempt,
        output_dir: Path,
        declared_artifacts: dict[str, Path],
    ) -> None:
        registered: dict[str, m.Artifact] = {}
        paths = {
            name: path for name, path in declared_artifacts.items() if path.is_file()
        }
        known_paths = {path.resolve() for path in paths.values()}
        for path in output_dir.rglob("*"):
            if (
                path.is_file()
                and path.name != "manifest.yaml"
                and path.resolve() not in known_paths
            ):
                relative = str(path.relative_to(output_dir))
                paths.setdefault(relative.replace("/", "_"), path)
        for name, path in paths.items():
            artifact = self._register_artifact(session, run, stage, attempt, name, path)
            registered[name] = artifact
        upstream_ids = session.scalars(
            select(m.StageExecutionArtifactInput.artifact_id).where(
                m.StageExecutionArtifactInput.stage_execution_id == stage.id
            )
        ).all()
        graph_inputs = session.scalars(
            select(m.StageExecutionGraphInput).where(
                m.StageExecutionGraphInput.stage_execution_id == stage.id
            )
        ).all()
        graph_artifact_ids = [
            graph.graph_artifact_id
            for item in graph_inputs
            if (graph := session.get(m.CausalGraphVersion, item.causal_graph_version_id))
        ]
        for artifact in registered.values():
            for upstream_id in upstream_ids:
                session.add(
                    m.ArtifactLineage(
                        downstream_artifact_id=artifact.id,
                        upstream_artifact_id=upstream_id,
                        relationship_type="DERIVED_FROM",
                    )
                )
            for graph_artifact_id in graph_artifact_ids:
                session.add(
                    m.ArtifactLineage(
                        downstream_artifact_id=artifact.id,
                        upstream_artifact_id=graph_artifact_id,
                        relationship_type="USED_GRAPH",
                    )
                )
        manifest_document = {
            "schema_version": "2",
            "execution_id": run.id,
            "stage_execution_id": stage.id,
            "attempt_id": attempt.id,
            "stage_type": stage.stage_type,
            "analysis_mode": stage.analysis_mode,
            "input_mode": stage.input_mode,
            "input_resource_ids": self._input_ids(session, stage.id),
            "configuration_versions": self._config_versions(session, stage.id),
            "artifacts": {
                name: {"artifact_id": artifact.id, "checksum": artifact.content_hash}
                for name, artifact in registered.items()
            },
            "saved_graph_versions": {
                item.input_name: {
                    "causal_graph_version_id": item.causal_graph_version_id,
                    "content_hash": item.content_hash_snapshot,
                }
                for item in graph_inputs
            },
            "random_seed": run.random_seed,
            "code_commit": run.code_commit,
            "package_version": __version__,
            "container_image_digest": run.container_image_digest,
            "runtime_metadata": attempt.runtime_metadata_json,
            "warnings": [],
            # Kept for the existing inference adapter during migration.
            "stage": stage.stage_type.lower(),
            "resolved_output_dir": str(output_dir),
        }
        manifest_path = output_dir / "manifest.yaml"
        manifest_path.write_text(
            yaml.safe_dump(manifest_document, sort_keys=False), encoding="utf-8"
        )
        manifest = self._register_artifact(
            session, run, stage, attempt, "manifest", manifest_path, kind="MANIFEST"
        )
        for artifact in registered.values():
            session.add(
                m.ArtifactLineage(
                    downstream_artifact_id=manifest.id,
                    upstream_artifact_id=artifact.id,
                    relationship_type="PACKAGES",
                )
            )
        session.add(
            m.ManifestRecord(
                execution_id=run.id,
                stage_execution_id=stage.id,
                scope="STAGE",
                artifact_id=manifest.id,
                schema_version="2",
                content_hash=manifest.content_hash,
                projection_json=manifest_document,
            )
        )

    def _register_artifact(
        self,
        session: Session,
        run: m.Execution,
        stage: m.StageExecution,
        attempt: m.StageAttempt,
        name: str,
        path: Path,
        *,
        kind: str | None = None,
    ) -> m.Artifact:
        stored_info = self.store.put_file(path)
        stored = session.scalar(
            select(m.StoredObject).where(
                m.StoredObject.backend == self.store.backend,
                m.StoredObject.bucket == stored_info.location.namespace,
                m.StoredObject.object_key == stored_info.location.key,
                m.StoredObject.object_version == (stored_info.location.version or ""),
            )
        )
        if not stored:
            stored = m.StoredObject(
                backend=self.store.backend,
                bucket=stored_info.location.namespace,
                object_key=stored_info.location.key,
                object_version=stored_info.location.version or "",
                media_type=_media_type(path),
                format=path.suffix.removeprefix(".").upper(),
                size_bytes=stored_info.size_bytes,
                checksum=stored_info.checksum,
                status="AVAILABLE",
            )
            session.add(stored)
            session.flush()
        artifact_kind, metadata = _artifact_kind(name, path, stage)
        artifact = m.Artifact(
            project_id=run.project_id,
            artifact_kind=kind or artifact_kind,
            logical_name=str(path.relative_to(Path(attempt.workspace_ref)))
            if path.is_relative_to(Path(attempt.workspace_ref))
            else path.name,
            status="AVAILABLE",
            stored_object_id=stored.id,
            produced_by_attempt_id=attempt.id,
            media_type=_media_type(path),
            schema_version="1",
            content_hash=stored_info.checksum,
            metadata_json=metadata,
        )
        session.add(artifact)
        session.flush()
        output_name = name[:250]
        existing = session.get(m.StageExecutionArtifactOutput, (stage.id, output_name))
        if not existing:
            session.add(
                m.StageExecutionArtifactOutput(
                    stage_execution_id=stage.id,
                    output_name=output_name,
                    artifact_id=artifact.id,
                    required=name == "manifest",
                )
            )
        return artifact

    def _project_results(
        self,
        session: Session,
        run: m.Execution,
        stage: m.StageExecution,
        artifacts: dict[str, Path],
        output_dir: Path,
    ) -> None:
        self.projection.project_results(session, stage, artifacts, output_dir)

    def _finish_cancelled(
        self, session: Session, run: m.Execution, service: ExecutionService
    ) -> None:
        self._terminate_mlflow_run(session, run, "KILLED")
        self.run_state.finish_cancelled(session, run, service)

    def _bind_dependency_artifacts(self, session: Session, stage: m.StageExecution) -> None:
        self.run_state.bind_dependency_artifacts(session, stage)

    @staticmethod
    def _parameter(session: Session, stage_id: str, name: str) -> Any:
        row = session.get(m.StageExecutionParameter, (stage_id, name))
        return row.value_json if row else None

    @staticmethod
    def _input_ids(session: Session, stage_id: str) -> dict[str, dict[str, str]]:
        return {
            "datasets": {
                item.input_name: item.dataset_version_id
                for item in session.scalars(
                    select(m.StageExecutionDatasetInput).where(
                        m.StageExecutionDatasetInput.stage_execution_id == stage_id
                    )
                ).all()
            },
            "artifacts": {
                item.input_name: item.artifact_id
                for item in session.scalars(
                    select(m.StageExecutionArtifactInput).where(
                        m.StageExecutionArtifactInput.stage_execution_id == stage_id
                    )
                ).all()
            },
            "saved_graphs": {
                item.input_name: item.causal_graph_version_id
                for item in session.scalars(
                    select(m.StageExecutionGraphInput).where(
                        m.StageExecutionGraphInput.stage_execution_id == stage_id
                    )
                ).all()
            },
        }

    @staticmethod
    def _config_versions(session: Session, stage_id: str) -> dict[str, dict[str, str]]:
        return {
            item.input_name: {
                "configuration_version_id": item.configuration_version_id,
                "content_hash": item.content_hash_snapshot,
            }
            for item in session.scalars(
                select(m.StageExecutionConfigInput).where(
                    m.StageExecutionConfigInput.stage_execution_id == stage_id
                )
            ).all()
        }


_DISCOVERY_PARAMETERS = {
    "campaign_id": "--campaign-id",
    "pre_weeks": "--pre-weeks",
    "alpha": "--alpha",
    "alpha_grid": "--alpha-grid",
    "bootstrap_samples": "--bootstrap-samples",
    "bootstrap_sample_fraction": "--bootstrap-sample-fraction",
    "random_seed": "--random-seed",
    "pc_indep_test": "--pc-indep-test",
    "collinearity_threshold": "--collinearity-threshold",
    "algorithms": "--algorithms",
    "notears_threshold": "--notears-threshold",
}

_INFERENCE_PARAMETERS = {
    "campaign_id": "--campaign-id",
    "pre_weeks": "--pre-weeks",
    "collinearity_threshold": "--collinearity-threshold",
    "algorithms": "--algorithms",
    "edge_robust_se": "--edge-robust-se",
    "min_samples": "--min-samples",
    "treatment": "--treatment",
    "outcome": "--outcome",
    "estimand": "--estimand",
    "adjustment_strategy": "--adjustment-strategy",
    "covariates": "--covariates",
    "effect_methods": "--effect-methods",
    "robust_se": "--robust-se",
}


def _append_parameters(
    args: list[str], values: dict[str, Any], mapping: dict[str, str]
) -> None:
    for name, flag in mapping.items():
        value = values.get(name)
        if value is None:
            continue
        args.append(flag)
        if isinstance(value, list):
            args.extend(str(item) for item in value)
        elif isinstance(value, bool):
            if not value:
                args.pop()
        else:
            args.append(str(value))


def _artifact_kind(
    name: str, path: Path, stage: m.StageExecution
) -> tuple[str, dict[str, Any]]:
    lowered = f"{name} {path}".lower()
    metadata: dict[str, Any] = {}
    if "input_preparation" in lowered:
        return "INPUT_PREPARATION", metadata
    if "feature_frame" in lowered:
        return "FEATURE_FRAME", metadata
    if stage.stage_type == "ETL" and path.suffix.lower() in {".csv", ".parquet"}:
        metadata["logical_table"] = name.removeprefix("dataset_")
        return "DATASET_TABLE", metadata
    if path.name == "edges.csv":
        metadata["algorithm"] = path.parent.name
        return "DISCOVERY_EDGES", metadata
    if "feature_semantics" in lowered:
        return "RESOLVED_FEATURE_SEMANTICS", metadata
    if "resolved" in lowered and path.suffix in {".yaml", ".json"}:
        return "RESOLVED_CONFIG", metadata
    if "edge_effect" in lowered:
        return "EDGE_WEIGHT_ESTIMATES", metadata
    if "treatment_effect" in lowered and path.suffix == ".csv":
        return "TREATMENT_EFFECT_ESTIMATES", metadata
    if "diagnostic" in lowered or "balance" in lowered or "overlap" in lowered:
        return "DIAGNOSTIC_TABLE", metadata
    if path.suffix == ".md":
        return "REPORT", metadata
    if path.suffix in {".csv", ".parquet"}:
        return "DIAGNOSTIC_TABLE", metadata
    return "LOG", metadata


def _media_type(path: Path) -> str:
    return {
        ".csv": "text/csv",
        ".parquet": "application/vnd.apache.parquet",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".json": "application/json",
        ".md": "text/markdown",
        ".png": "image/png",
    }.get(path.suffix.lower(), "application/octet-stream")


__all__ = ["Worker"]
