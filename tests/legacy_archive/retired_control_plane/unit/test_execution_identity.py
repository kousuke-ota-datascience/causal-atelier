"""Identity invariant tests for ExecutionIdentity.

Requirement source: docs/wiki/requirement_definition/01_web_service_requirements_v1.4.md
  - CLI identity must not carry an Ariadne execution_id.
  - Web identity must carry an Ariadne execution_id.
  - Namespace and primary_id must be consistent.
"""

from __future__ import annotations

import pytest

from ariadne.shared.identity import ExecutionIdentity, cli_identity, web_identity


class TestCLIIdentityInvariants:
    def test_cli_identity_has_no_execution_id(self) -> None:
        identity = cli_identity(mlflow_run_id="abc123")
        assert identity.execution_id is None

    def test_cli_identity_with_mlflow_run_id(self) -> None:
        identity = cli_identity(mlflow_run_id="abc123")
        assert identity.mlflow_run_id == "abc123"
        assert identity.primary_namespace == "MLFLOW"
        assert identity.primary_id == "abc123"

    def test_cli_identity_without_tracking(self) -> None:
        identity = cli_identity(mlflow_run_id=None)
        assert identity.mlflow_run_id is None
        assert identity.primary_namespace == "NONE"
        assert identity.primary_id is None

    def test_cli_identity_with_execution_id_raises(self) -> None:
        with pytest.raises(ValueError, match="CLI identity must not have execution_id"):
            ExecutionIdentity(
                origin="CLI",
                execution_id="some-ariadne-id",
                mlflow_run_id=None,
                primary_namespace="NONE",
                primary_id=None,
            )


class TestWebIdentityInvariants:
    def test_web_identity_requires_execution_id(self) -> None:
        with pytest.raises(ValueError, match="WEB identity requires execution_id"):
            ExecutionIdentity(
                origin="WEB",
                execution_id=None,
                mlflow_run_id=None,
                primary_namespace="ARIADNE",
                primary_id=None,
            )

    def test_web_identity_execution_id_is_primary(self) -> None:
        identity = web_identity(execution_id="exec-001")
        assert identity.execution_id == "exec-001"
        assert identity.primary_namespace == "ARIADNE"
        assert identity.primary_id == "exec-001"

    def test_web_identity_mlflow_run_id_may_be_none(self) -> None:
        identity = web_identity(execution_id="exec-001")
        assert identity.mlflow_run_id is None

    def test_web_identity_mlflow_run_id_optional(self) -> None:
        identity = web_identity(execution_id="exec-001", mlflow_run_id="mlflow-run-42")
        assert identity.mlflow_run_id == "mlflow-run-42"
        assert identity.primary_namespace == "ARIADNE"
        assert identity.primary_id == "exec-001"


class TestNamespaceConsistency:
    def test_ariadne_namespace_requires_execution_id(self) -> None:
        with pytest.raises(ValueError):
            ExecutionIdentity(
                origin="WEB",
                execution_id=None,
                mlflow_run_id=None,
                primary_namespace="ARIADNE",
                primary_id=None,
            )

    def test_mlflow_namespace_requires_mlflow_run_id(self) -> None:
        with pytest.raises(ValueError, match="primary_namespace MLFLOW requires mlflow_run_id"):
            ExecutionIdentity(
                origin="CLI",
                execution_id=None,
                mlflow_run_id=None,
                primary_namespace="MLFLOW",
                primary_id=None,
            )
