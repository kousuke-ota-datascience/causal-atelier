"""Explicit family/output cardinality and Artifact-only policy for G04."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ariadne.product.domain.enums import AnalysisFamily, ResultLevel
from ariadne.product.domain.errors import OutputOwnershipError


class ResultCardinality(str, Enum):
    ZERO = "ZERO"
    ONE = "ONE"
    MANY = "MANY"


@dataclass(frozen=True)
class WorkflowOutputContract:
    family: AnalysisFamily
    result_level: ResultLevel
    result_cardinality: ResultCardinality
    artifact_only_allowed: bool

    def validate(self, result_count: int, artifact_count: int) -> None:
        if self.result_cardinality is ResultCardinality.ZERO and result_count != 0:
            raise OutputOwnershipError(f"{self.family.value} contract permits zero Results only")
        if self.result_cardinality is ResultCardinality.ONE and result_count != 1:
            raise OutputOwnershipError(f"{self.family.value} contract requires exactly one Result")
        if self.result_cardinality is ResultCardinality.MANY and result_count < 1:
            raise OutputOwnershipError(f"{self.family.value} contract requires at least one Result")
        if artifact_count and result_count == 0 and not self.artifact_only_allowed:
            raise OutputOwnershipError(f"{self.family.value} contract rejects Artifact-only output")


FAMILY_OUTPUT_CONTRACTS: dict[AnalysisFamily, WorkflowOutputContract] = {
    AnalysisFamily.CAUSAL: WorkflowOutputContract(
        AnalysisFamily.CAUSAL, ResultLevel.STAGE_RESULT, ResultCardinality.ONE, False,
    ),
    AnalysisFamily.EXPLORATORY: WorkflowOutputContract(
        AnalysisFamily.EXPLORATORY, ResultLevel.STAGE_RESULT, ResultCardinality.ONE, False,
    ),
    # Predictive partition stages are an explicit supported Artifact-only case.
    AnalysisFamily.PREDICTIVE: WorkflowOutputContract(
        AnalysisFamily.PREDICTIVE, ResultLevel.STAGE_RESULT, ResultCardinality.ZERO, True,
    ),
}


def output_contract_for(family: AnalysisFamily) -> WorkflowOutputContract:
    return FAMILY_OUTPUT_CONTRACTS[family]
