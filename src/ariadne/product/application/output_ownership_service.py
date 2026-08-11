"""Canonical Result/Artifact metadata ownership and physical-store compensation."""

from __future__ import annotations

import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.enums import ArtifactScope, ArtifactType, ResultLevel, ResultReuseRole
from ariadne.product.domain.errors import OutputCompensationError, OutputOwnershipError
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.ports.artifact_store import ArtifactStorePort
from ariadne.product.workflow.output_contract import WorkflowOutputContract


@dataclass(frozen=True)
class OutputArtifact:
    artifact_type: ArtifactType
    content: bytes
    media_type: str = "application/octet-stream"
    metadata_json: dict[str, Any] | None = None


@dataclass(frozen=True)
class ResultReuseRef:
    result_id: str
    role: ResultReuseRole

    def __post_init__(self) -> None:
        if not isinstance(self.role, ResultReuseRole):
            raise TypeError("Result reuse role must be a typed ResultReuseRole")


@dataclass(frozen=True)
class ArtifactReuseRef:
    artifact_id: str


class OutputOwnershipService:
    """The sole canonical Product output metadata writer for G04 paths."""

    def __init__(self, uow_factory: Any, artifact_store: ArtifactStorePort) -> None:
        self._uow_factory = uow_factory
        self._artifact_store = artifact_store

    def persist(
        self,
        execution: Execution,
        *,
        stage: StageExecution | None,
        results: tuple[Result, ...] = (),
        artifacts: tuple[OutputArtifact, ...] = (),
        contract: WorkflowOutputContract,
    ) -> tuple[tuple[Result, ...], tuple[Artifact, ...]]:
        contract.validate(len(results), len(artifacts))
        self._validate_results(execution, stage, results, contract)
        for result in results:
            if result.result_level is ResultLevel.STAGE_RESULT and stage is None:
                raise OutputOwnershipError("StageResult requires a StageExecution")

        # Validate against the canonical persisted ownership graph before any
        # physical write. The detached domain object is not authority by itself.
        if stage is not None:
            with self._uow_factory() as uow:
                persisted_stage = uow.stage_executions.get(stage.stage_execution_id)
                if persisted_stage is None or persisted_stage.execution_id != execution.execution_id:
                    raise OutputOwnershipError("StageExecution is not owned by the canonical Execution")

        stored: list[tuple[str, str]] = []
        metadata: list[Artifact] = []
        try:
            with tempfile.TemporaryDirectory() as directory:
                for descriptor in artifacts:
                    artifact_id = str(uuid.uuid4())
                    object_key = f"outputs/{execution.execution_id}/{artifact_id}"
                    source = Path(directory) / artifact_id
                    source.write_bytes(descriptor.content)
                    saved = self._artifact_store.store(source, object_key, descriptor.media_type)
                    stored.append((artifact_id, saved.object_key))
                    result_id = results[0].result_id if len(results) == 1 else None
                    metadata.append(Artifact(
                        artifact_id=artifact_id,
                        project_id=execution.project_id,
                        execution_id=execution.execution_id,
                        stage_execution_id=stage.stage_execution_id if stage else None,
                        result_id=result_id,
                        artifact_scope=ArtifactScope.EXECUTION_OUTPUT,
                        artifact_type=descriptor.artifact_type,
                        object_key=saved.object_key,
                        content_hash=saved.content_hash,
                        media_type=saved.media_type,
                        size_bytes=saved.size_bytes,
                        metadata_json=descriptor.metadata_json or {},
                    ))
                with self._uow_factory() as uow:
                    uow.results.add_many(list(results))
                    uow.artifacts.add_many(metadata)
                    uow.commit()
        except Exception as exc:
            reconciliation: list[dict[str, str]] = []
            for artifact_id, object_key in stored:
                try:
                    self._artifact_store.delete(object_key)
                except Exception as cleanup_error:
                    reconciliation.append({
                        "artifact_id": artifact_id,
                        "object_key": object_key,
                        "error": str(cleanup_error),
                    })
            if reconciliation:
                raise OutputCompensationError(
                    "Output operation failed and cleanup requires reconciliation",
                    reconciliation,
                ) from exc
            raise
        return results, tuple(metadata)

    def _validate_results(
        self,
        execution: Execution,
        stage: StageExecution | None,
        results: tuple[Result, ...],
        contract: WorkflowOutputContract,
    ) -> None:
        for result in results:
            if result.execution_id != execution.execution_id:
                raise OutputOwnershipError("Result belongs to a different Execution")
            if result.result_level is not contract.result_level:
                raise OutputOwnershipError("Result level disagrees with workflow output contract")
            if result.result_level is ResultLevel.STAGE_RESULT:
                if stage is None or result.stage_execution_id != stage.stage_execution_id:
                    raise OutputOwnershipError("StageResult stage ownership mismatch")

    def reuse_result(self, reference: ResultReuseRef) -> Result:
        if not isinstance(reference, ResultReuseRef):
            raise TypeError("Result reuse requires a typed ResultReuseRef")
        with self._uow_factory() as uow:
            result = uow.results.get(reference.result_id)
            if result is None:
                raise OutputOwnershipError("Result ID does not resolve to a canonical Result")
            return result

    def reuse_artifact(self, reference: ArtifactReuseRef) -> Artifact:
        if not isinstance(reference, ArtifactReuseRef):
            raise TypeError("Artifact reuse requires a typed ArtifactReuseRef")
        with self._uow_factory() as uow:
            artifact = uow.artifacts.get(reference.artifact_id)
            if artifact is None or artifact.artifact_scope is not ArtifactScope.EXECUTION_OUTPUT:
                raise OutputOwnershipError("Artifact ID does not resolve to an execution output")
            return artifact
