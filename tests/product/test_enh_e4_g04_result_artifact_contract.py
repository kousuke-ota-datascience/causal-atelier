from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import pytest

from ariadne.product.application.output_ownership_service import (
    ArtifactReuseRef,
    OutputArtifact,
    OutputOwnershipService,
    ResultReuseRef,
)
from ariadne.product.domain.artifact import Artifact
from ariadne.product.domain.enums import (
    AnalysisFamily, ArtifactScope, ArtifactType, ResultLevel, ResultReuseRole, ResultType, ScientificStatus,
)
from ariadne.product.domain.errors import (
    InvalidAnalysisSpec, OutputCompensationError, OutputOwnershipError,
)
from ariadne.product.domain.execution import Execution
from ariadne.product.domain.result import Result
from ariadne.product.domain.stage_execution import StageExecution
from ariadne.product.ports.artifact_store import StoredArtifact
from ariadne.product.workflow.output_contract import (
    FAMILY_OUTPUT_CONTRACTS, ResultCardinality, output_contract_for,
)


class MemoryStore:
    def __init__(self, *, fail_store_at: int | None = None, fail_delete: bool = False) -> None:
        self.objects: dict[str, bytes] = {}
        self.store_calls = 0
        self.deleted: list[str] = []
        self.fail_store_at = fail_store_at
        self.fail_delete = fail_delete

    def store(self, source_path: Path, object_key: str, media_type: str = "application/octet-stream") -> StoredArtifact:
        self.store_calls += 1
        if self.fail_store_at == self.store_calls:
            raise OSError("injected store failure")
        content = source_path.read_bytes()
        self.objects[object_key] = content
        import hashlib
        return StoredArtifact(object_key, hashlib.sha256(content).hexdigest(), len(content), media_type)

    def retrieve(self, object_key: str, dest_path: Path) -> None:
        dest_path.write_bytes(self.objects[object_key])

    def exists(self, object_key: str) -> bool:
        return object_key in self.objects

    def delete(self, object_key: str) -> None:
        if self.fail_delete:
            raise OSError("injected cleanup failure")
        self.deleted.append(object_key)
        self.objects.pop(object_key, None)


class MemoryUow:
    def __init__(self, *, commit_failure: bool = False, stage: StageExecution | None = None) -> None:
        self.results = _MemoryRepo()
        self.artifacts = _MemoryRepo()
        self.stage_executions = _MemoryStageRepo(stage)
        self.commit_failure = commit_failure
        self.committed = False

    def __enter__(self):  # type: ignore[no-untyped-def]
        return self

    def __exit__(self, exc_type, *args) -> None:  # type: ignore[no-untyped-def]
        if exc_type:
            self.rollback()

    def commit(self) -> None:
        if self.commit_failure:
            raise OSError("injected database commit failure")
        self.committed = True

    def rollback(self) -> None:
        return None


class _MemoryRepo:
    def __init__(self) -> None:
        self.items = {}

    def add_many(self, values) -> None:  # type: ignore[no-untyped-def]
        self.items.update({item.result_id if hasattr(item, "result_id") else item.artifact_id: item for item in values})

    def get(self, item_id: str):  # type: ignore[no-untyped-def]
        return self.items.get(item_id)


class _MemoryStageRepo:
    def __init__(self, stage: StageExecution | None) -> None:
        self.stage = stage

    def get(self, stage_id: str) -> StageExecution | None:
        return self.stage if self.stage and self.stage.stage_execution_id == stage_id else None


def _execution(family: AnalysisFamily = AnalysisFamily.CAUSAL) -> Execution:
    return Execution(execution_id="execution", project_id="project", analysis_family=family)


def _stage(execution_id: str = "execution") -> StageExecution:
    return StageExecution(execution_id=execution_id, stage_key="analysis")


def _result(execution_id: str = "execution", stage_id: str | None = "stage") -> Result:
    return Result(
        execution_id=execution_id,
        result_level=ResultLevel.STAGE_RESULT,
        stage_execution_id=stage_id,
        result_type=ResultType.DIAGNOSTICS_RESULT,
        scientific_status=ScientificStatus.PASS,
    )


def _service(store: MemoryStore, uow: MemoryUow) -> OutputOwnershipService:
    @contextmanager
    def factory():
        yield uow
    return OutputOwnershipService(factory, store)


def test_g04_ac001_result_levels_and_ownership_validation_are_explicit() -> None:
    execution = _execution()
    stage = _stage()
    assert Result(execution_id="execution", result_level=ResultLevel.EXECUTION_RESULT).stage_execution_id is None
    with pytest.raises(InvalidAnalysisSpec):
        Result(execution_id="execution", result_level=ResultLevel.EXECUTION_RESULT, stage_execution_id="stage")
    with pytest.raises(InvalidAnalysisSpec):
        Result(execution_id="execution", result_level=ResultLevel.STAGE_RESULT)
    store = MemoryStore(); uow = MemoryUow(stage=stage)
    with pytest.raises(OutputOwnershipError):
        _service(store, uow).persist(
            execution, stage=stage, results=(_result("other", stage.stage_execution_id),),
            contract=output_contract_for(AnalysisFamily.CAUSAL),
        )


def test_g04_ac001_ac005_family_cardinality_contract_is_explicit() -> None:
    assert set(FAMILY_OUTPUT_CONTRACTS) == set(AnalysisFamily)
    assert all(contract.result_level is ResultLevel.STAGE_RESULT for contract in FAMILY_OUTPUT_CONTRACTS.values())
    assert output_contract_for(AnalysisFamily.CAUSAL).result_cardinality is ResultCardinality.ONE
    assert output_contract_for(AnalysisFamily.CAUSAL).artifact_only_allowed is False
    assert output_contract_for(AnalysisFamily.PREDICTIVE).result_cardinality is ResultCardinality.ZERO
    assert output_contract_for(AnalysisFamily.PREDICTIVE).artifact_only_allowed is True


def test_g04_ac003_store_failure_leaves_no_metadata_and_cleans_written_siblings() -> None:
    store = MemoryStore(fail_store_at=2); uow = MemoryUow(stage=_stage())
    service = _service(store, uow)
    with pytest.raises(OSError, match="injected store failure"):
        service.persist(
            _execution(), stage=uow.stage_executions.stage,
            artifacts=(
                OutputArtifact(ArtifactType.LOG, b"one"),
                OutputArtifact(ArtifactType.LOG, b"two"),
            ), contract=output_contract_for(AnalysisFamily.PREDICTIVE),
        )
    assert uow.results.items == {} and uow.artifacts.items == {}
    assert store.objects == {} and len(store.deleted) == 1


def test_g04_ac003_db_failure_cleans_physical_object_and_cleanup_failure_is_reconcilable() -> None:
    store = MemoryStore(); uow = MemoryUow(commit_failure=True, stage=_stage())
    with pytest.raises(OSError, match="injected database commit failure"):
        _service(store, uow).persist(
            _execution(), stage=uow.stage_executions.stage,
            artifacts=(OutputArtifact(ArtifactType.LOG, b"bytes"),),
            contract=output_contract_for(AnalysisFamily.PREDICTIVE),
        )
    assert store.objects == {}

    store = MemoryStore(fail_delete=True); uow = MemoryUow(commit_failure=True, stage=_stage())
    with pytest.raises(OutputCompensationError) as caught:
        _service(store, uow).persist(
            _execution(), stage=uow.stage_executions.stage,
            artifacts=(OutputArtifact(ArtifactType.LOG, b"bytes"),),
            contract=output_contract_for(AnalysisFamily.PREDICTIVE),
        )
    assert caught.value.reconciliation[0]["object_key"].startswith("outputs/")
    assert "artifact_id" in caught.value.reconciliation[0]


def test_g04_ac004_typed_reuse_requires_semantic_id_and_typed_role() -> None:
    stage = _stage(); store = MemoryStore(); uow = MemoryUow(stage=stage)
    result = _result(); artifact = Artifact(
        project_id="project", artifact_scope=ArtifactScope.EXECUTION_OUTPUT,
        execution_id="execution", object_key="physical/key", content_hash="hash",
        artifact_type=ArtifactType.LOG,
    )
    uow.results.items[result.result_id] = result
    uow.artifacts.items[artifact.artifact_id] = artifact
    service = _service(store, uow)
    assert service.reuse_result(ResultReuseRef(result.result_id, ResultReuseRole.UPSTREAM_INPUT)) is result
    assert service.reuse_artifact(ArtifactReuseRef(artifact.artifact_id)) is artifact
    with pytest.raises(TypeError):
        service.reuse_result("physical/key")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        service.reuse_result("content-hash-only")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        service.reuse_artifact("physical/key")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        service.reuse_artifact("content-hash-only")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ResultReuseRef(result.result_id, "UPSTREAM_INPUT")  # type: ignore[arg-type]


def test_g04_ac005_artifact_only_is_explicitly_allowed_or_rejected() -> None:
    execution = _execution(AnalysisFamily.PREDICTIVE); stage = _stage()
    store = MemoryStore(); uow = MemoryUow(stage=stage)
    _, artifacts = _service(store, uow).persist(
        execution, stage=stage, artifacts=(OutputArtifact(ArtifactType.LOG, b"manifest"),),
        contract=output_contract_for(AnalysisFamily.PREDICTIVE),
    )
    assert len(artifacts) == 1
    with pytest.raises(OutputOwnershipError):
        _service(MemoryStore(), MemoryUow(stage=stage)).persist(
            _execution(), stage=stage, artifacts=(OutputArtifact(ArtifactType.LOG, b"manifest"),),
            contract=output_contract_for(AnalysisFamily.CAUSAL),
        )
