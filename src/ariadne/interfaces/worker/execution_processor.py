"""ExecutionProcessor – processes a single claimed Execution end-to-end."""

from __future__ import annotations

import tempfile
import hashlib
import json
from pathlib import Path
from typing import Any

from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.enums import (
    ArtifactType,
    ExecutionOperation,
    ExecutionStatus,
    ResultType,
    ScientificStatus,
    GraphVersionStatus,
)
from ariadne.product.domain.errors import ArtifactHashMismatch
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result
from ariadne.product.application.execution_service import _compute_snapshot_hash
from ariadne.capabilities.causal.workflow import CausalPlanner, register_causal_runners
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.ports.scientific_core import (
    ScientificResultDescriptor,
    ScientificCorePort,
)
from ariadne.product.ports.unit_of_work import UnitOfWork

import logging

logger = logging.getLogger(__name__)


class ExecutionProcessor:
    def __init__(
        self,
        uow_factory: Any,
        scientific_core: ScientificCorePort,
        artifact_store: ArtifactStorePort,
        clock: ClockPort | None = None,
    ) -> None:
        self._uow_factory = uow_factory
        self._core = scientific_core
        self._store = artifact_store
        self._clock = clock or SystemClock()

    def process(self, execution: Execution) -> None:
        """Process an execution atomically claimed as RUNNING."""
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution.execution_id)
            if execution is None or execution.status != ExecutionStatus.RUNNING:
                return

        try:
            self._execute(execution)
        except Exception as exc:
            logger.exception("Execution %s failed: %s", execution.execution_id, exc)
            self._mark_failed(execution.execution_id, str(exc))

    def _execute(self, execution: Execution) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            output_dir = tmp / "output"
            output_dir.mkdir()

            # Retrieve dataset artifact
            dataset_path = tmp / "dataset"
            with self._uow_factory() as uow:
                dsv = uow.dataset_versions.get(execution.dataset_version_id)
                if dsv is None:
                    raise RuntimeError(f"DatasetVersion not found: {execution.dataset_version_id}")
                artifact = uow.artifacts.get(dsv.source_artifact_id)
                if artifact is None:
                    raise RuntimeError(f"Dataset Artifact not found: {dsv.source_artifact_id}")

            # Determine file suffix from media type or object key
            suffix = Path(artifact.object_key).suffix or ".parquet"
            dataset_path = dataset_path.with_suffix(suffix)
            self._store.retrieve(artifact.object_key, dataset_path)
            actual_hash = _sha256_file(dataset_path)
            if actual_hash != artifact.content_hash or actual_hash != dsv.content_hash:
                raise ArtifactHashMismatch(
                    f"Dataset Artifact hash mismatch for {artifact.artifact_id}"
                )

            if self._is_cancelled(execution.execution_id):
                return

            graph_path = (
                self._retrieve_graph(execution, tmp)
                if execution.operation != ExecutionOperation.DISCOVERY else None
            )
            self._verify_snapshot(execution, dsv.content_hash)
            upstream, upstream_execution = self._retrieve_upstream(execution)
            descriptors = self._dispatch_generic(
                execution, dataset_path, graph_path, upstream, upstream_execution, output_dir
            )
            if not descriptors:
                if self._is_cancelled(execution.execution_id):
                    return
                raise RuntimeError("Scientific Core returned no Results")

            now = self._clock.now()
            snapshot_warnings = execution.analysis_spec_json.get("scientific_warnings", [])
            results: list[Result] = []
            for descriptor in descriptors:
                summary = dict(descriptor.summary)
                payload = dict(descriptor.payload)
                if descriptor.result_type == ResultType.DISCOVERY_GRAPH_RESULT:
                    outcome = execution.analysis_spec_json.get("operation_spec", {}).get(
                        "designated_outcome_node"
                    )
                    if outcome is not None:
                        summary["designated_outcome_node"] = outcome
                        payload["designated_outcome_node"] = outcome
                results.append(Result(
                    execution_id=execution.execution_id,
                    result_type=descriptor.result_type,
                    scientific_status=descriptor.scientific_status,
                    summary_json=summary,
                    payload_json=payload,
                    diagnostics_json=descriptor.diagnostics,
                    warning_json=[*descriptor.warnings, *snapshot_warnings],
                    created_at=now,
                ))

            # Store artifacts in artifact store
            stored_artifacts: list[Artifact] = []
            stored_keys: list[str] = []
            for result, descriptor in zip(results, descriptors, strict=True):
                for art in descriptor.artifacts:
                    art_path = art.path
                    artifact_type = _guess_artifact_type(art_path)
                    object_key = (
                        f"projects/{execution.project_id}/executions/{execution.execution_id}"
                        f"/{result.result_id}/{art_path.name}"
                    )
                    stored = self._store.store(art_path, object_key)
                    stored_keys.append(stored.object_key)
                    stored_artifacts.append(Artifact(
                        project_id=execution.project_id,
                        execution_id=execution.execution_id,
                        result_id=result.result_id,
                        artifact_type=artifact_type,
                        object_key=stored.object_key,
                        content_hash=stored.content_hash,
                        media_type=stored.media_type,
                        size_bytes=stored.size_bytes,
                        metadata_json={"content_role": art.content_role},
                        created_at=now,
                    ))

            # Persist result, artifacts, and update execution status in one transaction
            try:
                with self._uow_factory() as uow:
                    exec_entity = uow.executions.get(execution.execution_id)
                    if exec_entity is None or exec_entity.status != ExecutionStatus.RUNNING:
                        for key in stored_keys:
                            self._store.delete(key)
                        return
                    uow.results.add_many(results)
                    uow.artifacts.add_many(stored_artifacts)
                    exec_entity.mark_succeeded(now)
                    uow.executions.update(exec_entity)
                    uow.commit()
            except Exception:
                for key in stored_keys:
                    try:
                        self._store.delete(key)
                    except Exception:
                        logger.exception("Unable to clean orphan artifact %s", key)
                raise

    def _dispatch_generic(
        self,
        execution: Execution,
        dataset_path: Path,
        graph_path: Path | None,
        upstream: Result | None,
        upstream_execution: Execution | None,
        output_dir: Path,
    ) -> list[ScientificResultDescriptor]:
        registry = StageRunnerRegistry()
        register_causal_runners(registry, self._core)
        plan = CausalPlanner().build_for_execution(execution)
        stage_key = plan.stages[0].stage_key
        inputs: dict[str, Any] = {
            "dataset_path": dataset_path,
            "output_dir": output_dir,
        }
        if graph_path is not None:
            inputs["graph_path"] = graph_path
        if upstream is not None:
            inputs["upstream_result"] = upstream
        if upstream_execution is not None:
            inputs["upstream_execution"] = upstream_execution
        outcome = GenericExecutor(registry, clock=self._clock.now).execute(
            execution.execution_id,
            plan,
            external_inputs={stage_key: inputs},
            snapshots={"snapshot_hash": execution.snapshot_hash},
            cancelled=lambda: self._is_cancelled(execution.execution_id),
        )
        if outcome.status == "CANCELLED":
            return []
        if outcome.status != "SUCCEEDED":
            error = outcome.stages[-1].last_error or {"message": "Causal Stage failed"}
            raise RuntimeError(str(error.get("message", error)))
        return list(outcome.stages[-1].output_binding["scientific_descriptors"])

    def _retrieve_upstream(self, execution: Execution) -> tuple[Result | None, Execution | None]:
        if execution.input_result_id is None:
            return None, None
        with self._uow_factory() as uow:
            result = uow.results.get(execution.input_result_id)
            if result is None:
                raise RuntimeError(f"Upstream Result not found: {execution.input_result_id}")
            generating = uow.executions.get(result.execution_id)
            if generating is None:
                raise RuntimeError(f"Upstream Execution not found: {result.execution_id}")
            return result, generating

    def _verify_snapshot(self, execution: Execution, dataset_content_hash: str) -> None:
        with self._uow_factory() as uow:
            graph = (
                uow.graph_versions.get(execution.input_graph_version_id)
                if execution.input_graph_version_id else None
            )
        actual = _compute_snapshot_hash(
            objective=execution.objective_snapshot,
            rationale=execution.rationale_snapshot,
            dataset_version_id=execution.dataset_version_id,
            dataset_content_hash=dataset_content_hash,
            input_graph_version_id=execution.input_graph_version_id,
            input_graph_content_hash=graph.content_hash if graph else None,
            input_result_id=execution.input_result_id,
            operation=execution.operation,
            algorithm_or_estimator=execution.algorithm_or_estimator,
            parameter_json=execution.parameter_json,
            random_seed=execution.random_seed,
            analysis_spec_json=execution.analysis_spec_json,
            code_version=execution.code_version,
            runtime_version_json=execution.runtime_version_json,
        )
        if actual != execution.snapshot_hash:
            raise ArtifactHashMismatch("Execution snapshot hash mismatch")

    def _retrieve_graph(self, execution: Execution, tmp: Path) -> Path:
        if execution.input_graph_version_id is None:
            raise RuntimeError("input_graph_version_id required for operation")
        with self._uow_factory() as uow:
            gv = uow.graph_versions.get(execution.input_graph_version_id)
            if gv is None:
                raise RuntimeError(f"GraphVersion not found: {execution.input_graph_version_id}")
            if gv.status != GraphVersionStatus.FIXED:
                raise RuntimeError("Estimation input GraphVersion is not FIXED")
            graph_json = gv.graph_json
            expected_hash = gv.content_hash

        graph_path = tmp / "input_graph.json"
        graph_path.write_text(json.dumps(graph_json, sort_keys=True), encoding="utf-8")
        canonical_hash = hashlib.sha256(
            json.dumps(graph_json, sort_keys=True).encode("utf-8")
        ).hexdigest()
        if canonical_hash != expected_hash:
            raise ArtifactHashMismatch("GraphVersion content hash mismatch")
        return graph_path

    def _is_cancelled(self, execution_id: str) -> bool:
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            return execution is None or execution.status == ExecutionStatus.CANCELLED

    def _mark_failed(self, execution_id: str, error_summary: str) -> None:
        now = self._clock.now()
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution_id)
            if execution and execution.status == ExecutionStatus.RUNNING:
                execution.mark_failed(now, error_summary)
                uow.executions.update(execution)
                uow.commit()


def _guess_artifact_type(path: Path) -> ArtifactType:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix == ".json" and "graph" in name:
        return ArtifactType.GRAPH_JSON
    if suffix in (".png", ".svg") and "graph" in name:
        return ArtifactType.GRAPH_IMAGE
    if "effect" in name or "result" in name:
        return ArtifactType.EFFECT_TABLE
    if "diag" in name:
        return ArtifactType.DIAGNOSTICS_TABLE
    if suffix in (".log", ".txt"):
        return ArtifactType.LOG
    return ArtifactType.LOG


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _result_document(result: Result) -> dict[str, Any]:
    return {
        "result_id": result.result_id,
        "result_type": result.result_type.value,
        "scientific_status": result.scientific_status.value,
        "summary": result.summary_json,
        "payload": result.payload_json,
        "diagnostics": result.diagnostics_json,
        "warnings": result.warning_json,
    }


def _context(execution: Execution) -> dict[str, Any]:
    return {
        "causal_question": execution.analysis_spec_json.get("causal_question", {}),
        "causal_design": execution.analysis_spec_json.get("causal_design", {}),
    }


def _inherit_scientific_context(
    current: dict[str, Any], upstream: dict[str, Any]
) -> dict[str, Any]:
    return {
        **current,
        "research_context": current.get("research_context") or upstream.get("research_context", {}),
        "causal_question": current.get("causal_question") or upstream.get("causal_question", {}),
        "causal_design": current.get("causal_design") or upstream.get("causal_design", {}),
    }
