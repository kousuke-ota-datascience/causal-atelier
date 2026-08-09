"""Focused mutation and writer-boundary checks for E4-G06 P06."""

from __future__ import annotations

import inspect

from ariadne.interfaces.worker.execution_processor import ExecutionProcessor
from ariadne.product.application.execution_service import ExecutionService
from ariadne.product.domain.lineage import LineageAuthority, classify_lineage_authority


def test_p06_retry_mutates_the_existing_execution_identity() -> None:
    source = inspect.getsource(ExecutionService.retry_execution)
    assert "uow.executions.get(execution_id)" in source
    assert "execution.increment_retry()" in source
    assert "create" not in source.lower()


def test_p06_worker_persists_only_guarded_generic_lineage() -> None:
    source = inspect.getsource(ExecutionProcessor._execute)
    assert 'relation_type="GENERATED"' not in source
    assert 'assert_generic_lineage_allowed("Artifact", "DERIVED_FROM", "Artifact")' in source
    assert 'assert_generic_lineage_allowed("Artifact", "EVIDENCE_FOR", "Result")' in source
    helper = inspect.getsource(ExecutionProcessor.__module__ and __import__(ExecutionProcessor.__module__, fromlist=["_add_predictive_output_lineage"])._add_predictive_output_lineage)
    assert "assert_generic_lineage_allowed" in helper
    assert classify_lineage_authority("Artifact", "DERIVED_FROM", "Artifact") is LineageAuthority.GENERIC_ONLY
