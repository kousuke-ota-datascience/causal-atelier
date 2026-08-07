"""Verified Dataset/Analysis View loading shared by analytical families."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd

from ariadne.capabilities.exploratory.view_compiler import AnalysisViewCompiler
from ariadne.product.domain.errors import ArtifactHashMismatch, EntityNotFound, InvalidSchema
from ariadne.product.persistence.orm_models import AnalysisViewOrm, ArtifactOrm, DatasetVersionOrm
from ariadne.product.ports.artifact_store import ArtifactStorePort


class AnalysisFrameProvider:
    def __init__(self, session_factory: Any, artifact_store: ArtifactStorePort) -> None:
        self._session_factory = session_factory
        self._store = artifact_store
        self._compiler = AnalysisViewCompiler()

    def load(
        self,
        project_id: str,
        dataset_version_id: str,
        analysis_view_id: str | None,
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        with self._session_factory() as session:
            dataset, frame = self._load_dataset(session, dataset_version_id)
            if dataset.project_id != project_id:
                raise EntityNotFound("DatasetVersion", dataset_version_id)
            if analysis_view_id:
                view = session.get(AnalysisViewOrm, analysis_view_id)
                if view is None or view.project_id != project_id:
                    raise EntityNotFound("AnalysisView", analysis_view_id)
                if view.source_dataset_version_id != dataset_version_id:
                    raise InvalidSchema("Analysis View and Dataset Version do not match")
                if view.status != "FIXED":
                    raise InvalidSchema("Analysis View must be FIXED")
                compiled = self._compiler.compile(
                    frame,
                    dataset.schema_json,
                    view.spec_json,
                    source_dataset_content_hash=dataset.content_hash,
                )
                if compiled.manifest != view.manifest_json:
                    raise ArtifactHashMismatch("Fixed Analysis View no longer reproduces its manifest")
                return compiled.frame, compiled.manifest
            return frame, {
                "schema_version": "analysis-view-manifest/1",
                "source_dataset_content_hash": dataset.content_hash,
                "materialized_hash": dataset.content_hash,
                "source_row_count": len(frame),
                "output_row_count": len(frame),
                "output_columns": list(frame.columns),
                "view_spec": None,
            }

    def _load_dataset(
        self, session: Any, dataset_version_id: str,
    ) -> tuple[DatasetVersionOrm, pd.DataFrame]:
        dataset = session.get(DatasetVersionOrm, dataset_version_id)
        if dataset is None:
            raise EntityNotFound("DatasetVersion", dataset_version_id)
        artifact = session.get(ArtifactOrm, dataset.source_artifact_id)
        if artifact is None:
            raise EntityNotFound("Artifact", dataset.source_artifact_id)
        suffix = Path(artifact.object_key).suffix or ".csv"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / f"dataset{suffix}"
            self._store.retrieve(artifact.object_key, path)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != artifact.content_hash or actual != dataset.content_hash:
                raise ArtifactHashMismatch("Dataset Artifact hash mismatch")
            frame = pd.read_parquet(path) if suffix.lower() == ".parquet" else pd.read_csv(path)
        return dataset, frame
