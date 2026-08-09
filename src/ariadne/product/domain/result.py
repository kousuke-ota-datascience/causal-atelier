"""Result domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ariadne.product.domain.enums import ResultLevel, ResultType, ScientificStatus
from ariadne.product.domain.errors import InvalidAnalysisSpec


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Result:
    result_id: str = field(default_factory=_new_id)
    execution_id: str = ""
    result_level: ResultLevel = ResultLevel.EXECUTION_RESULT
    stage_execution_id: str | None = None
    result_type: ResultType = ResultType.DISCOVERY_GRAPH_RESULT
    scientific_status: ScientificStatus = ScientificStatus.GENERATED
    summary_json: dict[str, Any] = field(default_factory=dict)
    payload_json: dict[str, Any] = field(default_factory=dict)
    diagnostics_json: dict[str, Any] = field(default_factory=dict)
    warning_json: list[Any] = field(default_factory=list)
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        self.validate_ownership()
        self.validate_status()

    def validate_ownership(self) -> None:
        # Detached scientific inputs may be used by the in-memory workflow
        # boundary. Persistence/application ownership rejects an empty ID.
        if not self.execution_id:
            return
        if self.result_level is ResultLevel.EXECUTION_RESULT and self.stage_execution_id is not None:
            raise InvalidAnalysisSpec("ExecutionResult cannot reference a stage")
        if self.result_level is ResultLevel.STAGE_RESULT and not self.stage_execution_id:
            raise InvalidAnalysisSpec("StageResult requires a stage_execution_id")

    def validate_status(self) -> None:
        allowed = {
            ResultType.DISCOVERY_GRAPH_RESULT: {
                ScientificStatus.GENERATED,
                ScientificStatus.GENERATED_WITH_WARNINGS,
                ScientificStatus.UNRELIABLE,
            },
            ResultType.IDENTIFICATION_RESULT: {
                ScientificStatus.IDENTIFIED,
                ScientificStatus.NOT_IDENTIFIED,
                ScientificStatus.PARTIALLY_IDENTIFIED,
                ScientificStatus.REQUIRES_REVIEW,
            },
            ResultType.DATA_ELIGIBILITY_RESULT: {
                ScientificStatus.PASS, ScientificStatus.WARN, ScientificStatus.FAIL,
            },
            ResultType.TREATMENT_EFFECT_RESULT: {
                ScientificStatus.ESTIMATED,
                ScientificStatus.INSUFFICIENT_OVERLAP,
                ScientificStatus.INSUFFICIENT_SAMPLE,
                ScientificStatus.ESTIMATION_UNRELIABLE,
                ScientificStatus.REQUIRES_REVIEW,
            },
            ResultType.DIAGNOSTICS_RESULT: {
                ScientificStatus.PASS, ScientificStatus.WARN, ScientificStatus.FAIL,
            },
            ResultType.REFUTATION_RESULT: {
                ScientificStatus.NO_FAILURE_DETECTED,
                ScientificStatus.FAILURE_DETECTED,
                ScientificStatus.INCONCLUSIVE,
            },
            ResultType.SENSITIVITY_RESULT: {
                ScientificStatus.ROBUST,
                ScientificStatus.FRAGILE,
                ScientificStatus.INCONCLUSIVE,
            },
        }
        if self.scientific_status not in allowed[self.result_type]:
            raise InvalidAnalysisSpec(
                f"{self.scientific_status.value} is invalid for {self.result_type.value}"
            )
