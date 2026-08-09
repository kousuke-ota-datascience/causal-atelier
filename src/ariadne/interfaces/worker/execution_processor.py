"""ExecutionProcessor – processes a single claimed Execution end-to-end."""

from __future__ import annotations

import tempfile
import hashlib
import json
import uuid
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.enums import (
    AnalysisFamily,
    ArtifactScope,
    ArtifactType,
    ExecutionOperation,
    ExecutionStatus,
    ResultType,
    ResultLevel,
    ScientificStatus,
    GraphVersionStatus,
)
from ariadne.product.domain.errors import ArtifactHashMismatch
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result
from ariadne.product.application.execution_service import _compute_snapshot_hash
from ariadne.capabilities.causal.workflow import CausalPlanner, register_causal_runners
from ariadne.capabilities.exploratory import ExploratoryPlanner, register_exploratory_runners
from ariadne.capabilities.predictive import (
    PredictivePlanner,
    register_predictive_explain_runner,
    register_predictive_split_runner,
    register_predictive_training_runners,
)
from ariadne.product.workflow.executor import GenericExecutor
from ariadne.product.workflow.runner_registry import StageRunnerRegistry
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.ports.clock import ClockPort, SystemClock
from ariadne.product.ports.scientific_core import (
    ArtifactDescriptor,
    ScientificResultDescriptor,
    ScientificCorePort,
)
from ariadne.product.ports.unit_of_work import UnitOfWork
from ariadne.product.persistence.orm_models import LineageEdgeOrm
from ariadne.product.domain.lineage import assert_generic_lineage_allowed

import logging

logger = logging.getLogger(__name__)


class ExecutionProcessor:
    def __init__(
        self,
        uow_factory: Any,
        scientific_core: ScientificCorePort,
        artifact_store: ArtifactStorePort,
        clock: ClockPort | None = None,
        owner_token: str | None = None,
    ) -> None:
        self._uow_factory = uow_factory
        self._core = scientific_core
        self._store = artifact_store
        self._clock = clock or SystemClock()
        self._owner_token = owner_token

    def process(self, execution: Execution) -> None:
        """Process an execution atomically claimed as RUNNING."""
        with self._uow_factory() as uow:
            execution = uow.executions.get(execution.execution_id)
            if execution is None or execution.status != ExecutionStatus.RUNNING:
                return
            # Existing test/adapter callers pass only the claimed entity.  The
            # persisted lease remains the source of truth for the completion
            # owner; the long-running worker passes owner_token explicitly.
            if self._owner_token is None:
                self._owner_token = execution.lease_owner

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
            stages_by_key = {stage.stage_key: stage for stage in self._load_stages(execution.execution_id)}
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
                stage_key = payload.pop("_canonical_stage_key", None)
                stage = stages_by_key.get(stage_key) if stage_key else None
                results.append(Result(
                    execution_id=execution.execution_id,
                    result_level=ResultLevel.STAGE_RESULT if stage else ResultLevel.EXECUTION_RESULT,
                    stage_execution_id=stage.stage_execution_id if stage else None,
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
            family_snapshot = dict(
                execution.runtime_version_json.get("family_snapshot", {})
            )
            analysis_view_snapshot = dict(family_snapshot.get("analysis_view", {}))
            for result, descriptor in zip(results, descriptors, strict=True):
                for art in descriptor.artifacts:
                    art_path = art.path
                    artifact_type = _guess_artifact_type(art_path)
                    _, _, artifact_schema_version = art.content_role.partition("|")
                    object_key = (
                        f"projects/{execution.project_id}/executions/{execution.execution_id}"
                        f"/{result.result_id}/{art_path.name}"
                    )
                    stored = self._store.store(
                        art_path, object_key,
                        media_type="application/json" if "|" in art.content_role else "application/octet-stream",
                    )
                    stored_keys.append(stored.object_key)
                    stored_artifacts.append(Artifact(
                        project_id=execution.project_id,
                        execution_id=execution.execution_id,
                        stage_execution_id=result.stage_execution_id,
                        result_id=result.result_id,
                        artifact_scope=ArtifactScope.EXECUTION_OUTPUT,
                        artifact_type=artifact_type,
                        object_key=stored.object_key,
                        content_hash=stored.content_hash,
                        media_type=stored.media_type,
                        size_bytes=stored.size_bytes,
                        metadata_json={
                            "content_role": art.content_role,
                            "schema_version": artifact_schema_version or "artifact/1",
                            **(
                                {
                                    "view_manifest": {
                                        "source_dataset_content_hash": dsv.content_hash,
                                        "view_spec_hash": analysis_view_snapshot.get("hash"),
                                    }
                                }
                                if execution.analysis_family is AnalysisFamily.EXPLORATORY
                                else {}
                            ),
                        },
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
                    artifact_by_type = {artifact.artifact_type: artifact for artifact in stored_artifacts}
                    result_by_type = {result.result_type: result for result in results}
                    for child, parent in ((ArtifactType.FITTED_PREPROCESSOR, ArtifactType.PARTITION_INDEX), (ArtifactType.FITTED_MODEL, ArtifactType.FITTED_PREPROCESSOR), (ArtifactType.PREDICTION, ArtifactType.FITTED_MODEL)):
                        if child in artifact_by_type and parent in artifact_by_type:
                            assert_generic_lineage_allowed("Artifact", "DERIVED_FROM", "Artifact")
                            uow._session.add(LineageEdgeOrm(lineage_edge_id=str(uuid.uuid4()), project_id=execution.project_id, source_type="Artifact", source_id=artifact_by_type[child].artifact_id, relation_type="DERIVED_FROM", target_type="Artifact", target_id=artifact_by_type[parent].artifact_id, evidence_json={}, created_by="worker", created_at=now))
                    prediction = artifact_by_type.get(ArtifactType.PREDICTION)
                    evaluation = next((result for result in results if result.result_type is ResultType.EVALUATION_RESULT), None)
                    if prediction is not None and evaluation is not None:
                        assert_generic_lineage_allowed("Artifact", "EVIDENCE_FOR", "Result")
                        uow._session.add(LineageEdgeOrm(lineage_edge_id=str(uuid.uuid4()), project_id=execution.project_id, source_type="Artifact", source_id=prediction.artifact_id, relation_type="EVIDENCE_FOR", target_type="Result", target_id=evaluation.result_id, evidence_json={}, created_by="worker", created_at=now))
                    if execution.analysis_family is AnalysisFamily.PREDICTIVE:
                        _add_predictive_output_lineage(
                            uow._session, execution, result_by_type,
                            artifact_by_type, now,
                        )
                    exec_entity.mark_succeeded(now)
                    if self._owner_token is None:
                        uow.executions.update(exec_entity)
                    else:
                        uow.executions.complete(exec_entity, self._owner_token)
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
        inputs: dict[str, dict[str, Any]]
        if execution.analysis_family is AnalysisFamily.CAUSAL:
            register_causal_runners(registry, self._core)
            plan = CausalPlanner().build_for_execution(execution)
            stage_key = plan.stages[0].stage_key
            inputs = {stage_key: {"dataset_path": dataset_path, "output_dir": output_dir}}
            if graph_path is not None:
                inputs[stage_key]["graph_path"] = graph_path
            if upstream is not None:
                inputs[stage_key]["upstream_result"] = upstream
            if upstream_execution is not None:
                inputs[stage_key]["upstream_execution"] = upstream_execution
        elif execution.analysis_family is AnalysisFamily.EXPLORATORY:
            register_exploratory_runners(registry)
            family_spec = dict(execution.analysis_spec_json.get("family_spec", {}))
            plan = ExploratoryPlanner().build_for_spec(
                project_id=execution.project_id,
                specification_id=execution.snapshot_hash,
                family_spec=family_spec,
            )
            inputs = {plan.stages[0].stage_key: {"frame": _read_frame(dataset_path)}}
        elif execution.analysis_family is AnalysisFamily.PREDICTIVE:
            register_predictive_split_runner(registry)
            register_predictive_training_runners(registry)
            register_predictive_explain_runner(registry)
            family_spec = dict(execution.analysis_spec_json.get("family_spec", {}))
            plan = PredictivePlanner().build_full_plan(
                project_id=execution.project_id,
                specification_id=execution.snapshot_hash,
                family_spec=family_spec,
            )
            frame = _read_frame(dataset_path)
            source_snapshot = {
                "schema_version": "predictive-source-snapshot/1",
                "dataset_version_id": execution.dataset_version_id,
                "dataset_content_hash": _sha256_file(dataset_path),
                "analysis_view_id": execution.analysis_spec_json.get("analysis_view_id"),
                "analysis_view_hash": (
                    execution.runtime_version_json
                    .get("family_snapshot", {})
                    .get("analysis_view", {})
                    .get("hash")
                ),
                "materialized_hash": _sha256_file(dataset_path),
            }
            inputs = {
                "split": {"frame": frame, "source_snapshot": source_snapshot},
                "prepare": {"frame": frame},
            }
        else:  # pragma: no cover - AnalysisFamily is exhaustive
            raise RuntimeError(f"Unsupported analysis family: {execution.analysis_family.value}")
        outcome = GenericExecutor(registry, clock=self._clock.now).execute(
            execution.execution_id,
            plan,
            external_inputs=inputs,
            snapshots={
                **execution.runtime_version_json.get("family_snapshot", {}),
                "snapshot_hash": execution.snapshot_hash,
            },
            cancelled=lambda: self._is_cancelled(execution.execution_id),
            worker_id=self._owner_token or execution.lease_owner or "worker",
            stage_executions=tuple(self._load_stages(execution.execution_id)),
        )
        self._persist_stages(execution.execution_id, outcome.stages)
        if outcome.status == "CANCELLED":
            return []
        if outcome.status != "SUCCEEDED":
            error = outcome.stages[-1].last_error or {"message": "Causal Stage failed"}
            raise RuntimeError(str(error.get("message", error)))
        if execution.analysis_family is AnalysisFamily.CAUSAL:
            return list(outcome.stages[-1].output_binding["scientific_descriptors"])
        return _family_descriptors(outcome, output_dir)

    def _load_stages(self, execution_id: str) -> list[Any]:
        with self._uow_factory() as uow:
            return uow.stage_executions.list_for_execution(execution_id)

    def _persist_stages(self, execution_id: str, stages: tuple[Any, ...]) -> None:
        owner = self._owner_token
        with self._uow_factory() as uow:
            for stage in stages:
                uow.stage_executions.update(stage, owner=owner)
            uow.commit()

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
                if self._owner_token is None:
                    uow.executions.update(execution)
                else:
                    uow.executions.complete(execution, self._owner_token)
                uow.commit()


def _guess_artifact_type(path: Path) -> ArtifactType:
    for value in ArtifactType:
        if path.name.startswith(f"{value.value}-"):
            return value
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


def _read_frame(path: Path) -> pd.DataFrame:
    """Load a canonical dataset artifact for family runners without a second DB path."""
    if path.suffix.lower() in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _family_descriptors(outcome: Any, output_dir: Path) -> list[ScientificResultDescriptor]:
    """Adapt detached family runner drafts to the canonical Result boundary.

    The family result type/status/schema is retained in the payload.  The
    current canonical Result vocabulary has no predictive/exploratory members,
    so DIAGNOSTICS_RESULT/PASS is the lossless envelope metadata rather than a
    claim that the result is causal diagnostics.
    """
    descriptors: list[ScientificResultDescriptor] = []
    pending_artifacts: list[ArtifactDescriptor] = []
    for stage_key, run_result in outcome.stage_results:
        artifacts_by_result_type: dict[str, list[ArtifactDescriptor]] = {}
        unbound_artifacts: list[ArtifactDescriptor] = []
        for index, draft in enumerate(run_result.artifacts):
            path = output_dir / f"{draft.artifact_type}-{stage_key}-{index}.json"
            path.write_bytes(draft.content)
            descriptor = ArtifactDescriptor(
                path,
                content_role=f"{draft.artifact_type}|{draft.schema_version}",
                result_type=draft.result_type,
            )
            if draft.result_type:
                artifacts_by_result_type.setdefault(draft.result_type, []).append(descriptor)
            else:
                unbound_artifacts.append(descriptor)
        if not run_result.results:
            pending_artifacts.extend(unbound_artifacts)
            for values in artifacts_by_result_type.values():
                pending_artifacts.extend(values)
            continue
        for result_index, draft in enumerate(run_result.results):
            artifacts = list(artifacts_by_result_type.get(draft.result_type, ()))
            if result_index == 0:
                artifacts = [*pending_artifacts, *unbound_artifacts, *artifacts]
            descriptors.append(ScientificResultDescriptor(
                result_type=ResultType(draft.result_type),
                scientific_status=ScientificStatus(draft.analytical_status),
                summary=draft.summary,
                payload={
                    **draft.payload,
                    "schema_version": draft.schema_version,
                    "_canonical_stage_key": stage_key,
                },
                diagnostics=draft.diagnostics,
                warnings=list(draft.warnings),
                artifacts=artifacts,
            ))
            if result_index == 0:
                pending_artifacts = []
    return descriptors


def _add_predictive_output_lineage(
    session: Any,
    execution: Execution,
    results: dict[ResultType, Result],
    artifacts: dict[ArtifactType, Artifact],
    created_at: Any,
) -> None:
    """Preserve predictive explanation/model-card scientific provenance."""

    def add(
        source_type: str, source_id: str, relation_type: str,
        target_type: str, target_id: str, evidence: dict[str, Any],
    ) -> None:
        assert_generic_lineage_allowed(source_type, relation_type, target_type)
        session.add(LineageEdgeOrm(
            lineage_edge_id=str(uuid.uuid4()), project_id=execution.project_id,
            source_type=source_type, source_id=source_id, relation_type=relation_type,
            target_type=target_type, target_id=target_id, evidence_json=evidence,
            created_by="worker", created_at=created_at,
        ))

    explanation = results.get(ResultType.PREDICTIVE_EXPLANATION_RESULT)
    model_card = results.get(ResultType.MODEL_CARD_RESULT)
    if explanation is not None:
        explanation_artifact = artifacts.get(ArtifactType.PREDICTIVE_EXPLANATION)
        if explanation_artifact is not None:
            add("Artifact", explanation_artifact.artifact_id, "EVIDENCE_FOR", "Result",
                explanation.result_id, {"purpose": "predictive_explanation"})
    if model_card is None:
        return
    for target_type, target_id in (
        ("AnalysisSpecification", execution.analysis_spec_json.get("analysis_specification_id")),
        ("DatasetVersion", execution.dataset_version_id),
        ("AnalysisView", execution.analysis_spec_json.get("analysis_view_id")),
    ):
        if target_id:
            add("Result", model_card.result_id, "DOCUMENTS", target_type, target_id,
                {"document": "model_card"})
    for artifact_type in (
        ArtifactType.PARTITION_INDEX, ArtifactType.FITTED_PREPROCESSOR,
        ArtifactType.FITTED_MODEL, ArtifactType.PREDICTION,
    ):
        artifact = artifacts.get(artifact_type)
        if artifact is not None:
            add("Result", model_card.result_id, "SUMMARIZES", "Artifact",
                artifact.artifact_id, {"artifact_type": artifact_type.value})
    evaluation = results.get(ResultType.EVALUATION_RESULT)
    if evaluation is not None:
        add("Result", model_card.result_id, "SUMMARIZES", "Result",
            evaluation.result_id, {"result_type": ResultType.EVALUATION_RESULT.value})


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
