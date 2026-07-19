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

    @classmethod
    def from_env(cls) -> "WebSettings":
        root = Path(os.getenv("CAUSAL_ATELIER_STATE_DIR", ".causal-atelier")).resolve()
        database_url = os.getenv(
            "CAUSAL_ATELIER_DATABASE_URL",
            f"sqlite:///{root / 'metadata.db'}",
        )
        return cls(
            database_url=database_url,
            artifact_root=Path(
                os.getenv("CAUSAL_ATELIER_ARTIFACT_ROOT", root / "objects")
            ).resolve(),
            workspace_root=Path(
                os.getenv("CAUSAL_ATELIER_WORKSPACE_ROOT", root / "workspaces")
            ).resolve(),
            artifact_backend=os.getenv(
                "CAUSAL_ATELIER_ARTIFACT_BACKEND", "LOCAL"
            ).upper(),
            s3_bucket=os.getenv("CAUSAL_ATELIER_S3_BUCKET"),
            s3_endpoint_url=os.getenv("CAUSAL_ATELIER_S3_ENDPOINT_URL"),
            azure_blob_container=os.getenv("CAUSAL_ATELIER_AZURE_BLOB_CONTAINER"),
            azure_storage_connection_string=os.getenv(
                "CAUSAL_ATELIER_AZURE_STORAGE_CONNECTION_STRING"
            ),
            azure_storage_account_url=os.getenv(
                "CAUSAL_ATELIER_AZURE_STORAGE_ACCOUNT_URL"
            ),
            azure_storage_credential=os.getenv(
                "CAUSAL_ATELIER_AZURE_STORAGE_CREDENTIAL"
            ),
            auth_mode=os.getenv("CAUSAL_ATELIER_AUTH_MODE", "development").lower(),
            oidc_issuer=os.getenv("CAUSAL_ATELIER_OIDC_ISSUER"),
            oidc_audience=os.getenv("CAUSAL_ATELIER_OIDC_AUDIENCE"),
            oidc_jwks_url=os.getenv("CAUSAL_ATELIER_OIDC_JWKS_URL"),
            auto_create_schema=_bool("CAUSAL_ATELIER_AUTO_CREATE_SCHEMA", False),
            query_async_threshold_bytes=int(
                os.getenv("CAUSAL_ATELIER_QUERY_ASYNC_THRESHOLD_BYTES", "100000000")
            ),
            query_max_result_rows=int(
                os.getenv("CAUSAL_ATELIER_QUERY_MAX_RESULT_ROWS", "10000")
            ),
            query_max_sample_rows=int(
                os.getenv("CAUSAL_ATELIER_QUERY_MAX_SAMPLE_ROWS", "50000")
            ),
            small_cell_threshold=int(
                os.getenv("CAUSAL_ATELIER_SMALL_CELL_THRESHOLD", "5")
            ),
            worker_poll_seconds=float(
                os.getenv("CAUSAL_ATELIER_WORKER_POLL_SECONDS", "1")
            ),
            worker_lease_seconds=int(
                os.getenv("CAUSAL_ATELIER_WORKER_LEASE_SECONDS", "300")
            ),
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
