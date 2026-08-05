"""Execution identity context with explicit namespace separation.

CLI runs use MLflow as the primary tracking namespace; Ariadne execution_id is
None.  Web/API runs use Ariadne as the primary namespace; mlflow_run_id is None
until the Worker starts processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ExecutionIdentity:
    """Identity context that separates Ariadne and MLflow namespaces.

    Invariants:
    - ``origin == "WEB"`` requires ``execution_id`` to be non-None.
    - ``origin == "CLI"`` requires ``execution_id`` to be None.
    - ``primary_namespace == "ARIADNE"`` requires ``execution_id`` to be non-None.
    - ``primary_namespace == "MLFLOW"`` requires ``mlflow_run_id`` to be non-None.
    - ``primary_namespace == "NONE"`` means tracking is disabled; no pseudo-IDs.
    """

    origin: Literal["CLI", "WEB"]
    execution_id: str | None
    mlflow_run_id: str | None
    primary_namespace: Literal["MLFLOW", "ARIADNE", "NONE"]
    primary_id: str | None

    def __post_init__(self) -> None:
        if self.origin == "WEB" and self.execution_id is None:
            raise ValueError("WEB identity requires execution_id")
        if self.origin == "CLI" and self.execution_id is not None:
            raise ValueError("CLI identity must not have execution_id (Ariadne Execution not created for CLI)")
        if self.primary_namespace == "ARIADNE" and self.execution_id is None:
            raise ValueError("primary_namespace ARIADNE requires execution_id")
        if self.primary_namespace == "MLFLOW" and self.mlflow_run_id is None:
            raise ValueError("primary_namespace MLFLOW requires mlflow_run_id")


def cli_identity(mlflow_run_id: str | None) -> ExecutionIdentity:
    """Build a CLI identity.  When tracking is disabled, mlflow_run_id is None."""
    return ExecutionIdentity(
        origin="CLI",
        execution_id=None,
        mlflow_run_id=mlflow_run_id,
        primary_namespace="MLFLOW" if mlflow_run_id else "NONE",
        primary_id=mlflow_run_id,
    )


def web_identity(execution_id: str, mlflow_run_id: str | None = None) -> ExecutionIdentity:
    """Build a Web identity.  mlflow_run_id may be None until Worker starts."""
    return ExecutionIdentity(
        origin="WEB",
        execution_id=execution_id,
        mlflow_run_id=mlflow_run_id,
        primary_namespace="ARIADNE",
        primary_id=execution_id,
    )


__all__ = ["ExecutionIdentity", "cli_identity", "web_identity"]
