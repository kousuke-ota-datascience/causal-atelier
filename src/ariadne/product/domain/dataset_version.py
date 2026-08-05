"""DatasetVersion domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class DatasetVersion:
    dataset_version_id: str = field(default_factory=_new_id)
    project_id: str = ""
    source_artifact_id: str = ""
    dataset_key: str = ""
    name: str = ""
    version_label: str = ""
    content_hash: str = ""
    schema_json: dict[str, Any] = field(default_factory=dict)
    profile_summary_json: dict[str, Any] = field(default_factory=dict)
    row_count: int = 0
    column_count: int = 0
    source_note: str | None = None
    created_at: datetime | None = None
