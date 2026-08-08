"""Predictive planners for split validation and the full staged workflow."""

from __future__ import annotations

from typing import Any

from ariadne.product.domain.analysis_specification import PREDICTIVE_SCHEMA_VERSION
from ariadne.product.domain.enums import AnalysisFamily, VersionedResourceStatus
from ariadne.product.domain.errors import InvalidExecutionPlan
from ariadne.product.domain.execution_plan import (
    ExecutionPlan,
    StageBinding,
    StageDefinition,
    StageType,
)
from ariadne.product.workflow.contracts import PlanningContext


class PredictivePlanner:
    family = AnalysisFamily.PREDICTIVE
    spec_versions = frozenset({PREDICTIVE_SCHEMA_VERSION})
    planner_id = "predictive.split"
    planner_version = "1"

    def build_plan(self, context: PlanningContext) -> ExecutionPlan:
        specification = context.specification
        if specification.status is not VersionedResourceStatus.FIXED:
            raise InvalidExecutionPlan("SPEC_NOT_FIXED", "Specification must be FIXED")
        return self.build_full_plan(
            project_id=specification.project_id,
            specification_id=specification.analysis_specification_id,
            family_spec=specification.family_spec,
        )

    def build_for_spec(
        self,
        *,
        project_id: str,
        specification_id: str,
        family_spec: dict[str, Any],
    ) -> ExecutionPlan:
        stage = StageDefinition(
            stage_key="split",
            stage_type=StageType("predictive", "split", "1"),
            input_contract={
                "frame": "analysis-frame/1",
                "source_snapshot": "predictive-source-snapshot/1",
            },
            output_contract={"partition_manifest": "partition-artifact/1"},
            parameters=family_spec,
        )
        return ExecutionPlan.build(
            project_id=project_id,
            analysis_specification_id=specification_id,
            analysis_family=self.family,
            planner_id=self.planner_id,
            planner_version=self.planner_version,
            stages=(stage,),
        )

    def build_full_plan(
        self,
        *,
        project_id: str,
        specification_id: str,
        family_spec: dict[str, Any],
    ) -> ExecutionPlan:
        split = StageDefinition(
            stage_key="split",
            stage_type=StageType("predictive", "split", "1"),
            input_contract={
                "frame": "analysis-frame/1",
                "source_snapshot": "predictive-source-snapshot/1",
            },
            output_contract={"partition_manifest": "partition-artifact/1"},
            parameters=family_spec,
        )
        prepare = StageDefinition(
            stage_key="prepare",
            stage_type=StageType("predictive", "prepare", "1"),
            input_contract={
                "frame": "analysis-frame/1",
                "partition_manifest": "partition-artifact/1",
            },
            output_contract={
                "training_bundle": "predictive-training-bundle/1",
                "evaluation_bundle": "predictive-evaluation-bundle/1",
                "fitted_preprocessor": "fitted-preprocessor/1",
                "explanation_dataset": "predictive-explanation-dataset/1",
                "explanation_specification": "predictive-explanation-specification/1",
                "sampling_definition": "predictive-explanation-sampling/1",
            },
            parameters=family_spec,
        )
        train = StageDefinition(
            stage_key="train",
            stage_type=StageType("predictive", "train", "1"),
            input_contract={
                "training_bundle": "predictive-training-bundle/1",
                "fitted_preprocessor": "fitted-preprocessor/1",
            },
            output_contract={
                "frozen_model": "fitted-model/1",
                "training_summary": "predictive-training-summary/1",
            },
            parameters=family_spec,
        )
        evaluate = StageDefinition(
            stage_key="evaluate",
            stage_type=StageType("predictive", "evaluate", "1"),
            input_contract={
                "frozen_model": "fitted-model/1",
                "evaluation_bundle": "predictive-evaluation-bundle/1",
                "fitted_preprocessor": "fitted-preprocessor/1",
            },
            output_contract={"evaluation_summary": "predictive-evaluation-summary/1"},
            parameters=family_spec,
        )
        stages = [split, prepare, train, evaluate]
        dependencies = [
            StageBinding("split", "partition_manifest", "prepare", "partition_manifest"),
            StageBinding("prepare", "training_bundle", "train", "training_bundle"),
            StageBinding(
                "prepare", "fitted_preprocessor", "train", "fitted_preprocessor"
            ),
            StageBinding("train", "frozen_model", "evaluate", "frozen_model"),
            StageBinding(
                "prepare", "evaluation_bundle", "evaluate", "evaluation_bundle"
            ),
            StageBinding(
                "prepare", "fitted_preprocessor", "evaluate", "fitted_preprocessor"
            ),
        ]
        if family_spec.get("explanation_spec"):
            explain = StageDefinition(
                stage_key="explain",
                stage_type=StageType("predictive", "explain", "1"),
                input_contract={
                    "frozen_model": "fitted-model/1",
                    "fitted_preprocessor": "fitted-preprocessor/1",
                    "explanation_dataset": "predictive-explanation-dataset/1",
                    "explanation_specification": (
                        "predictive-explanation-specification/1"
                    ),
                    "sampling_definition": "predictive-explanation-sampling/1",
                    "training_summary": "predictive-training-summary/1",
                    "evaluation_summary": "predictive-evaluation-summary/1",
                    "partition_manifest": "partition-artifact/1",
                },
                output_contract={
                    "explanation_summary": "predictive-explanation-summary/1",
                    "model_card": "predictive-model-card-result/1",
                },
                parameters=family_spec,
            )
            stages.append(explain)
            dependencies.extend([
                StageBinding("train", "frozen_model", "explain", "frozen_model"),
                StageBinding(
                    "prepare",
                    "fitted_preprocessor",
                    "explain",
                    "fitted_preprocessor",
                ),
                StageBinding(
                    "prepare",
                    "explanation_dataset",
                    "explain",
                    "explanation_dataset",
                ),
                StageBinding(
                    "prepare",
                    "explanation_specification",
                    "explain",
                    "explanation_specification",
                ),
                StageBinding(
                    "prepare",
                    "sampling_definition",
                    "explain",
                    "sampling_definition",
                ),
                StageBinding(
                    "train",
                    "training_summary",
                    "explain",
                    "training_summary",
                ),
                StageBinding(
                    "evaluate",
                    "evaluation_summary",
                    "explain",
                    "evaluation_summary",
                ),
                StageBinding(
                    "split",
                    "partition_manifest",
                    "explain",
                    "partition_manifest",
                ),
            ])
        return ExecutionPlan.build(
            project_id=project_id,
            analysis_specification_id=specification_id,
            analysis_family=self.family,
            planner_id="predictive.full",
            planner_version="1",
            stages=tuple(stages),
            dependencies=tuple(dependencies),
        )
