"""Result domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import ResultType, ScientificStatus


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Result:
    result_id: str = field(default_factory=_new_id)
    execution_id: str = ""
    result_type: ResultType = ResultType.DISCOVERY_GRAPH_RESULT
    scientific_status: ScientificStatus = ScientificStatus.GRAPH_PRODUCED
    summary_json: dict[str, Any] = field(default_factory=dict)
    payload_json: dict[str, Any] = field(default_factory=dict)
    diagnostics_json: dict[str, Any] = field(default_factory=dict)
    warning_json: list[Any] = field(default_factory=list)
    created_at: datetime | None = None
