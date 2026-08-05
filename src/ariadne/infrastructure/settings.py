"""Environment based settings for the web control and execution planes."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class WebSettings:
    """Runtime settings deliberately kept independent from web frameworks."""

    database_url: str
    artifact_root: Path
    workspace_root: Path
    artifact_backend: str = "LOCAL"
    s3_bucket: str | None = None
    s3_endpoint_url: str | None = None
    azure_blob_container: str | None = None
    azure_storage_connection_string: str | None = None
    azure_storage_account_url: str | None = None
    azure_storage_credential: str | None = None
    auth_mode: str = "development"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_url: str | None = None
    auto_create_schema: bool = False
    query_async_threshold_bytes: int = 100_000_000
    query_max_result_rows: int = 10_000
    query_max_sample_rows: int = 50_000
    small_cell_threshold: int = 5
    worker_poll_seconds: float = 1.0
    worker_lease_seconds: int = 300
    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "ariadne"
    mlflow_enabled: bool = True
    mlflow_timeout_seconds: int = 30
    mlflow_tag_prefix: str = "ariadne."

    @classmethod
    def from_env(cls) -> "WebSettings":
        root = Path(os.getenv("ARIADNE_STATE_DIR", ".ariadne")).resolve()
        database_url = os.getenv(
            "ARIADNE_DATABASE_URL",
            f"sqlite:///{root / 'metadata.db'}",
        )
        return cls(
            database_url=database_url,
            artifact_root=Path(
                os.getenv("ARIADNE_ARTIFACT_ROOT", root / "objects")
            ).resolve(),
            workspace_root=Path(
                os.getenv("ARIADNE_WORKSPACE_ROOT", root / "workspaces")
            ).resolve(),
            artifact_backend=os.getenv(
                "ARIADNE_ARTIFACT_BACKEND", "LOCAL"
            ).upper(),
            s3_bucket=os.getenv("ARIADNE_S3_BUCKET"),
            s3_endpoint_url=os.getenv("ARIADNE_S3_ENDPOINT_URL"),
            azure_blob_container=os.getenv("ARIADNE_AZURE_BLOB_CONTAINER"),
            azure_storage_connection_string=os.getenv(
                "ARIADNE_AZURE_STORAGE_CONNECTION_STRING"
            ),
            azure_storage_account_url=os.getenv(
                "ARIADNE_AZURE_STORAGE_ACCOUNT_URL"
            ),
            azure_storage_credential=os.getenv(
                "ARIADNE_AZURE_STORAGE_CREDENTIAL"
            ),
            auth_mode=os.getenv("ARIADNE_AUTH_MODE", "development").lower(),
            oidc_issuer=os.getenv("ARIADNE_OIDC_ISSUER"),
            oidc_audience=os.getenv("ARIADNE_OIDC_AUDIENCE"),
            oidc_jwks_url=os.getenv("ARIADNE_OIDC_JWKS_URL"),
            auto_create_schema=_bool("ARIADNE_AUTO_CREATE_SCHEMA", False),
            query_async_threshold_bytes=int(
                os.getenv("ARIADNE_QUERY_ASYNC_THRESHOLD_BYTES", "100000000")
            ),
            query_max_result_rows=int(
                os.getenv("ARIADNE_QUERY_MAX_RESULT_ROWS", "10000")
            ),
            query_max_sample_rows=int(
                os.getenv("ARIADNE_QUERY_MAX_SAMPLE_ROWS", "50000")
            ),
            small_cell_threshold=int(
                os.getenv("ARIADNE_SMALL_CELL_THRESHOLD", "5")
            ),
            worker_poll_seconds=float(
                os.getenv("ARIADNE_WORKER_POLL_SECONDS", "1")
            ),
            worker_lease_seconds=int(
                os.getenv("ARIADNE_WORKER_LEASE_SECONDS", "300")
            ),
            mlflow_tracking_uri=os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"),
            mlflow_experiment_name=os.getenv("MLFLOW_EXPERIMENT_NAME", "ariadne"),
            mlflow_enabled=_bool("MLFLOW_ENABLED", True),
            mlflow_timeout_seconds=int(os.getenv("MLFLOW_TIMEOUT_SECONDS", "30")),
            mlflow_tag_prefix=os.getenv("MLFLOW_TAG_PREFIX", "ariadne."),
        )

    def ensure_directories(self) -> None:
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
        if self.database_url.startswith("sqlite:///"):
            Path(self.database_url.removeprefix("sqlite:///")).parent.mkdir(
                parents=True,
                exist_ok=True,
            )


__all__ = ["WebSettings"]
