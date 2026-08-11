"""D3 static authority boundaries for the final Phase D audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _source(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_g05_d3_worker_and_cli_have_no_legacy_product_lifecycle_authority() -> None:
    worker = _source("src/ariadne/interfaces/worker/runner.py")
    assert "uow.executions.claim_next" in worker
    assert "FamilyExecutionOrm" not in worker
    assert ".claim_next(" not in worker.replace("uow.executions.claim_next(", "")

    for path in (ROOT / "src/ariadne/interfaces/cli").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "FamilyExecutionOrm" not in source, path
        assert "FamilyStageExecutionOrm" not in source, path
        assert "FamilyResultOrm" not in source, path
        assert "FamilyArtifactOrm" not in source, path
        assert "SqlUnitOfWork" not in source, path


def test_g05_d3_family_adapters_reject_or_delegate_before_retained_family_write_source() -> None:
    exploratory = _source("src/ariadne/product/application/exploratory_service.py")
    predictive = _source("src/ariadne/product/application/predictive_workflow_service.py")
    split = _source("src/ariadne/product/application/predictive_split_service.py")

    for source, operation in (
        (exploratory, "ExploratoryWorkspaceService.claim_next"),
        (exploratory, "ExploratoryWorkspaceService.process_execution"),
        (predictive, "PredictiveWorkflowService.claim_next"),
        (predictive, "PredictiveWorkflowService.process_execution"),
        (split, "PredictiveSplitService.validate_and_save"),
    ):
        assert f'raise LegacyProductAuthorityDisabled("{operation}")' in source

    assert predictive.index("self._require_execution_service()") < predictive.index("FamilyExecutionOrm(")
    assert exploratory.index("execution_service = self._require_execution_service()") < exploratory.index("FamilyExecutionOrm(")
    assert split.index('raise LegacyProductAuthorityDisabled("PredictiveSplitService.validate_and_save")') < split.index("FamilyExecutionOrm(")


def test_g05_d3_historical_partition_adapter_is_read_only_and_separate_from_canonical_lookup() -> None:
    split = _source("src/ariadne/product/application/predictive_split_service.py")
    historical = split[split.index("def get_partition_artifact"):split.index("@staticmethod", split.index("def get_partition_artifact"))]
    assert "FamilyArtifactOrm" in historical
    assert "session.add" not in historical
    assert "session.delete" not in historical

    predictive = _source("src/ariadne/product/application/predictive_workflow_service.py")
    canonical_get = predictive[predictive.index("def get_execution"):predictive.index("def get_stages")]
    assert "FamilyExecutionOrm" not in canonical_get
