"""D2 boundaries: Product execution mutations require canonical lifecycle DI."""

from __future__ import annotations

import pytest
from typing import cast

from ariadne.adapters.local_artifact_store import LocalArtifactStore
from ariadne.interfaces.web_api import dependencies
from ariadne.product.application.exploratory_service import ExploratoryWorkspaceService
from ariadne.product.application.predictive_workflow_service import PredictiveWorkflowService
from ariadne.product.application.predictive_split_service import PredictiveSplitService
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.domain.errors import EntityNotFound, LegacyProductAuthorityDisabled


def _unused_session_factory():  # type: ignore[no-untyped-def]
    raise AssertionError("legacy mutation must reject before opening a session")


class _DeleteSpyStore(LocalArtifactStore):
    def __init__(self, root):  # type: ignore[no-untyped-def]
        super().__init__(root)
        self.delete_calls: list[str] = []

    def delete(self, object_key: str) -> None:
        self.delete_calls.append(object_key)


class _CanonicalLookupMiss:
    def get_execution(self, execution_id: str):  # type: ignore[no-untyped-def]
        raise EntityNotFound("Execution", execution_id)


def test_g05_d2_missing_canonical_dependency_rejects_all_product_execution_mutations(
    tmp_path,
) -> None:  # type: ignore[no-untyped-def]
    store = _DeleteSpyStore(tmp_path / "objects")
    exploratory = ExploratoryWorkspaceService(_unused_session_factory, store)
    predictive = PredictiveWorkflowService(_unused_session_factory, store)
    split = PredictiveSplitService(
        _unused_session_factory, store, execution_service=cast(ExecutionService, object()),
    )

    for operation in (
        lambda: exploratory.submit_execution(
            "project", dataset_version_id="dataset", analysis_view_id=None,
            family_spec={},
        ),
        lambda: exploratory.create_analysis_draft("project", "result", "CAUSAL"),
        lambda: predictive.submit_execution(
            "project", specification_id="spec", plan_id="plan", seed=1,
            requested_by="d2",
        ),
        lambda: predictive.cancel("project", "execution"),
        lambda: predictive.retry("project", "execution"),
        lambda: predictive.rerun("project", "execution", requested_by="d2"),
        lambda: predictive.revise(
            "project", "execution", specification_id="spec", seed=1,
            change_reason="d2", requested_by="d2",
        ),
        lambda: predictive.prefill("project", "execution"),
        lambda: split.validate_and_save(
            "project", dataset_version_id="dataset", analysis_view_id=None, family_spec={},
        ),
    ):
        with pytest.raises(LegacyProductAuthorityDisabled):
            operation()
    assert store.delete_calls == []


def test_g05_d2_canonical_lookup_miss_does_not_fallback_to_legacy_retry_or_cancel(
    tmp_path,
) -> None:  # type: ignore[no-untyped-def]
    service = PredictiveWorkflowService(
        _unused_session_factory,
        _DeleteSpyStore(tmp_path / "objects"),
        execution_service=cast(ExecutionService, _CanonicalLookupMiss()),
    )
    for operation in (
        lambda: service.cancel("project", "missing"),
        lambda: service.retry("project", "missing"),
    ):
        with pytest.raises(EntityNotFound):
            operation()


@pytest.mark.anyio
async def test_g05_d2_fastapi_family_service_providers_inject_canonical_execution_service(
    product_env,
) -> None:  # type: ignore[no-untyped-def]
    exploratory = await dependencies.get_exploratory_workspace_service()
    predictive = await dependencies.get_predictive_workflow_service()
    split = await dependencies.get_predictive_split_service()
    assert exploratory._execution_service is not None
    assert predictive._execution_service is not None
    assert split._execution_service is not None
