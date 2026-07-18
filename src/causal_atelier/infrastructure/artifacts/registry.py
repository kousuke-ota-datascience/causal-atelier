"""Artifact registry and manifest helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from causal_atelier.infrastructure.config import dump_yaml, hash_file, load_yaml_mapping


@dataclass(frozen=True)
class ArtifactSpec:
    """One planned or created artifact."""

    name: str
    path: Path
    required: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize this artifact spec."""

        return {
            "name": self.name,
            "path": str(self.path),
            "required": self.required,
        }


@dataclass(frozen=True)
class ArtifactRegistry:
    """Pipeline artifact contract."""

    artifacts: tuple[ArtifactSpec, ...] = ()

    def for_stage(self, stage: str) -> dict[str, str]:
        """Return artifact paths whose names are prefixed by a stage name."""

        prefix = f"{stage}."
        return {
            artifact.name.removeprefix(prefix): str(artifact.path)
            for artifact in self.artifacts
            if artifact.name.startswith(prefix)
        }

    def to_dict(self) -> dict[str, Any]:
        """Serialize the registry."""

        return {"artifacts": [artifact.to_dict() for artifact in self.artifacts]}


@dataclass(frozen=True)
class RunManifest:
    """Manifest written for a completed stage."""

    run_id: str
    stage: str
    resolved_output_dir: Path
    created_at: str
    config_paths: dict[str, Path]
    config_hashes: dict[str, str]
    artifacts: dict[str, Path]
    random_seed: int | None = None
    metadata: dict[str, Any] | None = None

    @classmethod
    def build(
        cls,
        *,
        run_id: str,
        stage: str,
        output_dir: Path,
        config_paths: Mapping[str, Path],
        artifacts: Mapping[str, Path],
        random_seed: int | None,
        metadata: Mapping[str, Any] | None = None,
    ) -> "RunManifest":
        """Build a manifest and hash existing config files."""

        hashes = {
            name: hash_file(path)
            for name, path in config_paths.items()
            if path.exists()
        }
        return cls(
            run_id=run_id,
            stage=stage,
            resolved_output_dir=output_dir,
            created_at=datetime.now(timezone.utc).isoformat(),
            config_paths=dict(config_paths),
            config_hashes=hashes,
            artifacts=dict(artifacts),
            random_seed=random_seed,
            metadata=dict(metadata or {}),
        )

    @classmethod
    def read(cls, path: Path) -> dict[str, Any]:
        """Read a manifest as a mapping."""

        return load_yaml_mapping(path)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the manifest."""

        data = {
            "run_id": self.run_id,
            "stage": self.stage,
            "resolved_output_dir": str(self.resolved_output_dir),
            "created_at": self.created_at,
            "random_seed": self.random_seed,
            "artifacts": {name: str(path) for name, path in self.artifacts.items()},
            "metadata": self.metadata or {},
        }
        for name, path in self.config_paths.items():
            data[f"resolved_{name}_path"] = str(path)
        for name, digest in self.config_hashes.items():
            data[f"resolved_{name}_hash"] = digest
        return data

    def write(self, path: Path) -> None:
        """Write the manifest to YAML."""

        dump_yaml(path, self.to_dict())


__all__ = ["ArtifactRegistry", "ArtifactSpec", "RunManifest"]
