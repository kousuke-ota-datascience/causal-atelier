"""Materialize immutable objects into isolated worker workspaces."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from ariadne.application.ports import ArtifactLocation, ArtifactStore
from ariadne.infrastructure.artifact_store import artifact_location
from ariadne.infrastructure.persistence import models as m


class WorkspaceMaterializer:
    def __init__(self, store: ArtifactStore) -> None:
        self.store = store

    def copy(self, location: ArtifactLocation, destination: Path) -> Path:
        source = self.store.resolve_local_path(location)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return destination

    def configurations(
        self, session: Session, stage: m.StageExecution, workspace: Path
    ) -> dict[str, Path]:
        target = workspace / "inputs/configs"
        target.mkdir(parents=True)
        paths: dict[str, Path] = {}
        inputs = session.scalars(
            select(m.StageExecutionConfigInput).where(
                m.StageExecutionConfigInput.stage_execution_id == stage.id
            )
        ).all()
        for item in inputs:
            version = session.get(m.ConfigurationVersion, item.configuration_version_id)
            if version.content_hash != item.content_hash_snapshot:
                raise ValueError(
                    f"Configuration immutability violation: {item.input_name}"
                )
            path = target / f"{item.input_name}.yaml"
            path.write_text(
                yaml.safe_dump(version.canonical_json, sort_keys=False),
                encoding="utf-8",
            )
            paths[item.input_name] = path
        return paths

    def dataset(
        self, session: Session, stage: m.StageExecution, workspace: Path
    ) -> Path:
        inputs = session.scalars(
            select(m.StageExecutionDatasetInput).where(
                m.StageExecutionDatasetInput.stage_execution_id == stage.id
            )
        ).all()
        if not inputs:
            raise ValueError(f"{stage.stage_type} requires a Dataset Version input")
        dataset_dir = workspace / "inputs/datasets" / inputs[0].dataset_version_id
        dataset_dir.mkdir(parents=True)
        tables = session.scalars(
            select(m.DatasetTableVersion)
            .where(
                m.DatasetTableVersion.dataset_version_id
                == inputs[0].dataset_version_id
            )
            .order_by(m.DatasetTableVersion.ordinal)
        ).all()
        registry: dict[str, Any] = {
            "default": {
                "file": {"path": str(dataset_dir), "name": "", "type": "parquet"}
            },
        }
        for table in tables:
            stored = session.get(m.StoredObject, table.stored_object_id)
            extension = ".parquet" if table.file_format == "PARQUET" else ".csv"
            name = f"{table.logical_name}{extension}"
            self.copy(artifact_location(stored), dataset_dir / name)
            registry[table.logical_name] = {
                "file": {"name": name, "type": table.file_format.lower()}
            }
        registry_path = dataset_dir / "registry.yaml"
        registry_path.write_text(
            yaml.safe_dump(registry, sort_keys=False), encoding="utf-8"
        )
        return registry_path

    def discovery_manifest(
        self,
        session: Session,
        stage: m.StageExecution,
        workspace: Path,
        upstream_workspaces: dict[str, Path],
    ) -> Path:
        dependencies = session.scalars(
            select(m.StageExecutionDependency).where(
                m.StageExecutionDependency.stage_execution_id == stage.id
            )
        ).all()
        for dependency in dependencies:
            upstream = session.get(m.StageExecution, dependency.depends_on_stage_execution_id)
            if upstream.stage_key in upstream_workspaces:
                candidate = upstream_workspaces[upstream.stage_key] / "manifest.yaml"
                if candidate.exists():
                    return candidate
        artifact_inputs = session.scalars(
            select(m.StageExecutionArtifactInput).where(
                m.StageExecutionArtifactInput.stage_execution_id == stage.id
            )
        ).all()
        discovery_dir = workspace / "inputs/artifacts/discovery"
        discovery_dir.mkdir(parents=True)
        for item in artifact_inputs:
            artifact = session.get(m.Artifact, item.artifact_id)
            stored = (
                session.get(m.StoredObject, artifact.stored_object_id)
                if artifact.stored_object_id
                else None
            )
            if not stored:
                continue
            if artifact.artifact_kind == "MANIFEST":
                target = discovery_dir / "manifest-input.yaml"
                self.copy(artifact_location(stored), target)
                try:
                    document = yaml.safe_load(target.read_text()) or {}
                    if Path(document.get("resolved_output_dir", "")).exists():
                        return target
                except Exception:
                    pass
            if artifact.artifact_kind == "DISCOVERY_EDGES":
                algorithm = artifact.metadata_json.get(
                    "algorithm"
                ) or item.input_name.removeprefix("edges_")
                self.copy(
                    artifact_location(stored),
                    discovery_dir / algorithm / "edges.csv",
                )
        edges = list(discovery_dir.glob("*/edges.csv"))
        if not edges:
            raise ValueError(
                "Inference requires a materializable Discovery Edge Artifact"
            )
        manifest = {
            "execution_id": "materialized",
            "stage": "discovery",
            "resolved_output_dir": str(discovery_dir),
            "artifacts": {path.parent.name: str(path) for path in edges},
        }
        target = discovery_dir / "manifest.yaml"
        target.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        return target


__all__ = ["WorkspaceMaterializer"]
