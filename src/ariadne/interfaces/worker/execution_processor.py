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
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.ports.scientific_core import (
    DiscoveryInput,
    EstimationInput,
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

            # Run scientific core
            if execution.operation == ExecutionOperation.DISCOVERY:
                sci_output = self._run_discovery(execution, dataset_path, output_dir)
                result_type = ResultType.DISCOVERY_GRAPH_RESULT
                payload_json = sci_output.graph_json
                summary_json = sci_output.summary
                diagnostics_json = sci_output.diagnostics
                warnings = sci_output.warnings
                scientific_status = sci_output.scientific_status
                artifact_paths = sci_output.artifacts
            else:
                # ESTIMATION – also needs graph artifact
                graph_path = self._retrieve_graph(execution, tmp)
                est_output = self._run_estimation(execution, dataset_path, graph_path, output_dir)
                result_type = ResultType.TREATMENT_EFFECT_RESULT
                payload_json = est_output.payload
                summary_json = est_output.summary
                diagnostics_json = est_output.diagnostics
                warnings = est_output.warnings
                scientific_status = est_output.scientific_status
                artifact_paths = est_output.artifacts

            # Build result and artifacts
            now = self._clock.now()
            result = Result(
                execution_id=execution.execution_id,
                result_type=result_type,
                scientific_status=scientific_status,
                summary_json=summary_json,
                payload_json=payload_json,
                diagnostics_json=diagnostics_json,
                warning_json=warnings,
                created_at=now,
            )

            # Store artifacts in artifact store
            stored_artifacts: list[Artifact] = []
            stored_keys: list[str] = []
            for art_path in artifact_paths:
                artifact_type = _guess_artifact_type(art_path)
                object_key = (
                    f"projects/{execution.project_id}/executions/{execution.execution_id}"
                    f"/{art_path.name}"
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
                    uow.results.add_many([result])
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

    def _run_discovery(self, execution: Execution, dataset_path: Path, output_dir: Path) -> Any:
        from ariadne.product.ports.scientific_core import DiscoveryInput
        input_ = DiscoveryInput(
            dataset_path=dataset_path,
            algorithm=execution.algorithm_or_estimator,
            parameters=execution.parameter_json,
            random_seed=execution.random_seed,
            analysis_spec=execution.analysis_spec_json,
        )
        return self._core.run_discovery(input_, output_dir)

    def _run_estimation(
        self, execution: Execution, dataset_path: Path, graph_path: Path, output_dir: Path
    ) -> Any:
        from ariadne.product.ports.scientific_core import EstimationInput
        input_ = EstimationInput(
            dataset_path=dataset_path,
            graph_path=graph_path,
            estimator=execution.algorithm_or_estimator,
            parameters=execution.parameter_json,
            random_seed=execution.random_seed,
            analysis_spec=execution.analysis_spec_json,
        )
        return self._core.run_estimation(input_, output_dir)

    def _retrieve_graph(self, execution: Execution, tmp: Path) -> Path:
        if execution.input_graph_version_id is None:
            raise RuntimeError("input_graph_version_id required for ESTIMATION")
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
