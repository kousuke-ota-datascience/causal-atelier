"""Cross-stage validation for the integrated pipeline."""

from __future__ import annotations

from pathlib import Path

from causal_atelier.causal.design import CausalDesign
from causal_atelier.infrastructure.config import load_yaml_mapping
from causal_atelier.preprocessing.common import FeatureRole, FeatureSemanticsCatalog
from causal_atelier.shared.validation import ValidationIssue, ValidationResult, ValidationSeverity

from .planning import ExecutionPlan, StagePlan


class CrossStageValidator:
    """Validate plan-level and cross-stage contracts."""

    def validate(self, plan: ExecutionPlan) -> ValidationResult:
        """Validate an execution plan."""

        issues: list[ValidationIssue] = []
        for stage in plan.enabled_stages():
            issues.extend(self.validate_stage(stage, plan))
        issues.extend(self.validate_feature_semantics(plan))
        issues.extend(self.validate_causal_design(plan))
        issues.extend(self.validate_adjustment_sets(plan))
        return ValidationResult(issues)

    def validate_stage(self, stage: StagePlan, plan: ExecutionPlan) -> list[ValidationIssue]:
        """Validate one stage plan."""

        issues: list[ValidationIssue] = []
        for name, path in stage.config_paths.items():
            if not path.exists():
                issues.append(_error("config_missing", f"missing config file: {path}", f"{stage.name}.{name}"))
        for name, path in stage.output_paths.items():
            if name.endswith("dir") or name == "output_dir":
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except OSError as exc:
                    issues.append(_error("output_dir_invalid", str(exc), f"{stage.name}.{name}"))
        if stage.name == "inference":
            manifest = stage.input_paths["discovery_manifest"]
            discovery_enabled = any(candidate.name == "discovery" and candidate.enabled for candidate in plan.stages)
            if manifest.exists():
                issues.extend(self.validate_discovery_manifest_schema(manifest))
            elif not discovery_enabled:
                issues.append(_error("discovery_manifest_missing", f"missing discovery manifest: {manifest}", "inference.discovery_manifest"))
            else:
                issues.append(
                    ValidationIssue(
                        ValidationSeverity.INFO,
                        "discovery_manifest_planned",
                        f"discovery manifest will be produced by this run: {manifest}",
                        "inference.discovery_manifest",
                    )
                )
        return issues

    def validate_discovery_manifest_schema(self, manifest_path: Path) -> list[ValidationIssue]:
        """Validate minimum discovery manifest schema."""

        try:
            manifest = load_yaml_mapping(manifest_path)
        except Exception as exc:
            return [_error("discovery_manifest_unreadable", str(exc), "inference.discovery_manifest")]
        required = {"run_id", "stage", "resolved_output_dir", "artifacts"}
        missing = sorted(required.difference(manifest))
        if missing:
            return [
                _error(
                    "discovery_manifest_invalid",
                    f"manifest missing keys: {missing}",
                    "inference.discovery_manifest",
                )
            ]
        if manifest.get("stage") != "discovery":
            return [
                _error(
                    "discovery_manifest_invalid_stage",
                    f"expected discovery manifest, got {manifest.get('stage')!r}",
                    "inference.discovery_manifest",
                )
            ]
        return []

    def validate_feature_semantics(self, plan: ExecutionPlan) -> list[ValidationIssue]:
        """Validate discovery/inference feature semantics when both configs exist."""

        discovery = _stage_by_name(plan, "discovery")
        inference = _stage_by_name(plan, "inference")
        if discovery is None or inference is None:
            return []
        discovery_path = discovery.config_paths.get("feature_config")
        inference_path = inference.config_paths.get("feature_semantics")
        if discovery_path is None or inference_path is None or not discovery_path.exists() or not inference_path.exists():
            return []
        try:
            discovery_catalog = FeatureSemanticsCatalog.from_feature_config_mapping(load_yaml_mapping(discovery_path))
            inference_catalog = FeatureSemanticsCatalog.from_mapping(load_yaml_mapping(inference_path))
            mode = _inference_mode(inference)
            if mode == "edge_weight":
                mismatches = _compare_discovery_nodes_to_inference_semantics(
                    discovery_catalog,
                    inference_catalog,
                )
            elif mode == "treatment_effect":
                mismatches = self._validate_treatment_effect_semantics_subset(
                    inference,
                    inference_catalog,
                )
            else:
                mismatches = [f"unsupported inference mode for semantics validation: {mode}"]
        except Exception as exc:
            return [_error("feature_semantics_invalid", str(exc), "feature_semantics")]
        return [
            _error("feature_semantics_mismatch", mismatch, "feature_semantics")
            for mismatch in mismatches
        ]

    def validate_causal_design(self, plan: ExecutionPlan) -> list[ValidationIssue]:
        """Validate causal design presence and minimum treatment/outcome semantics."""

        inference = _stage_by_name(plan, "inference")
        if inference is None or not inference.enabled:
            return []
        design_path = inference.config_paths.get("causal_design")
        semantics_path = inference.config_paths.get("feature_semantics")
        if design_path is None or not design_path.exists():
            return [_error("causal_design_missing", f"missing causal design: {design_path}", "causal_design")]
        try:
            design = CausalDesign.from_mapping(load_yaml_mapping(design_path))
        except Exception as exc:
            return [_error("causal_design_invalid", str(exc), "causal_design")]
        if semantics_path is None or not semantics_path.exists():
            return []
        try:
            catalog = FeatureSemanticsCatalog.from_mapping(load_yaml_mapping(semantics_path)).by_name()
        except Exception as exc:
            return [_error("feature_semantics_invalid", str(exc), "feature_semantics")]
        issues: list[ValidationIssue] = []
        treatment = catalog.get(design.treatment.name)
        outcome = catalog.get(design.outcome.name)
        if treatment is None or treatment.role.value != "treatment":
            issues.append(_error("treatment_semantics_invalid", f"treatment is not role=treatment: {design.treatment.name}", "causal_design.treatment"))
        if outcome is None or outcome.role.value != "outcome":
            issues.append(_error("outcome_semantics_invalid", f"outcome is not role=outcome: {design.outcome.name}", "causal_design.outcome"))
        return issues

    def validate_adjustment_sets(self, plan: ExecutionPlan) -> list[ValidationIssue]:
        """Validate configured adjustment sets for obvious bad controls."""

        inference = _stage_by_name(plan, "inference")
        if inference is None or not inference.enabled:
            return []
        feature_config_path = inference.config_paths.get("feature_config")
        if feature_config_path is None or not feature_config_path.exists():
            return []
        try:
            config = load_yaml_mapping(feature_config_path)
        except Exception as exc:
            return [_error("feature_config_invalid", str(exc), "inference.feature_config")]
        semantics_path = inference.config_paths.get("feature_semantics")
        if semantics_path is None or not semantics_path.exists():
            return [_error("feature_semantics_missing", f"missing feature semantics: {semantics_path}", "feature_semantics")]
        try:
            catalog = FeatureSemanticsCatalog.from_mapping(load_yaml_mapping(semantics_path)).by_name()
        except Exception as exc:
            return [_error("feature_semantics_invalid", str(exc), "feature_semantics")]
        adjustment_sets = dict(config.get("adjustment_sets", {}))
        issues: list[ValidationIssue] = []
        for set_name, set_config in adjustment_sets.items():
            if set_name == "exclude_patterns":
                continue
            variables = list(set_config.get("variables", set_config.get("include", [])))
            for variable in variables:
                issues.extend(
                    _validate_adjustment_variable_semantics(
                        str(variable),
                        catalog,
                        f"adjustment_sets.{set_name}",
                    )
                )
        return issues

    def _validate_treatment_effect_semantics_subset(
        self,
        inference: StagePlan,
        inference_catalog: FeatureSemanticsCatalog,
    ) -> list[str]:
        """Validate treatment/outcome/selected covariates for treatment-effect mode."""

        catalog = inference_catalog.by_name()
        config = load_yaml_mapping(inference.config_paths["config"])
        feature_config = load_yaml_mapping(inference.config_paths["feature_config"])
        treatment_config = dict(config.get("treatment_effect", {}))
        treatment = str(_arg_value(inference.resolved_args, "--treatment") or treatment_config.get("treatment", "treated"))
        outcome = str(_arg_value(inference.resolved_args, "--outcome") or treatment_config.get("outcome", "outcome_sales_value"))
        strategy = str(
            _arg_value(inference.resolved_args, "--adjustment-strategy")
            or treatment_config.get("adjustment_strategy", "pre_treatment_covariates")
        )
        covariates = _arg_values(inference.resolved_args, "--covariates")
        if covariates is None:
            covariates = _adjustment_variables(feature_config, strategy, treatment_config)

        issues: list[str] = []
        treatment_spec = catalog.get(treatment)
        if treatment_spec is None:
            issues.append(f"treatment missing from feature semantics: {treatment}")
        elif treatment_spec.role != FeatureRole.TREATMENT:
            issues.append(f"treatment role is not treatment: {treatment}")
        outcome_spec = catalog.get(outcome)
        if outcome_spec is None:
            issues.append(f"outcome missing from feature semantics: {outcome}")
        elif outcome_spec.role != FeatureRole.OUTCOME:
            issues.append(f"outcome role is not outcome: {outcome}")
        for covariate in covariates:
            variable_issues = _validate_adjustment_variable_semantics(
                str(covariate),
                catalog,
                f"treatment_effect.{strategy}",
            )
            issues.extend(issue.message for issue in variable_issues)
        return issues


def _stage_by_name(plan: ExecutionPlan, name: str) -> StagePlan | None:
    for stage in plan.stages:
        if stage.name == name:
            return stage
    return None


def _error(code: str, message: str, location: str | None = None) -> ValidationIssue:
    return ValidationIssue(ValidationSeverity.ERROR, code, message, location)


def _compare_discovery_nodes_to_inference_semantics(
    discovery_catalog: FeatureSemanticsCatalog,
    inference_catalog: FeatureSemanticsCatalog,
) -> list[str]:
    """Require strict semantic equality for discovery graph nodes."""

    inference_by_name = inference_catalog.by_name()
    issues: list[str] = []
    for feature in discovery_catalog.features:
        inference_feature = inference_by_name.get(feature.name)
        if inference_feature is None:
            issues.append(f"discovery graph node missing from inference feature semantics: {feature.name}")
            continue
        left_fields = feature.comparable_fields()
        right_fields = inference_feature.comparable_fields()
        for field, left_value in left_fields.items():
            right_value = right_fields[field]
            if left_value != right_value:
                issues.append(
                    f"discovery graph node semantics mismatch for {feature.name}.{field}: {left_value!r} != {right_value!r}"
                )
    return issues


def _validate_adjustment_variable_semantics(
    variable: str,
    catalog: dict[str, object],
    location: str,
) -> list[ValidationIssue]:
    """Validate one adjustment variable against feature semantics."""

    spec = catalog.get(variable)
    if spec is None:
        return [
            _error(
                "adjustment_semantics_missing",
                f"adjustment variable missing from feature semantics: {variable}",
                location,
            )
        ]
    issues: list[ValidationIssue] = []
    if spec.role != FeatureRole.COVARIATE:
        issues.append(
            _error(
                "adjustment_role_invalid",
                f"adjustment variable role must be covariate: {variable} role={spec.role.value}",
                location,
            )
        )
    if not spec.allowed_for_adjustment:
        issues.append(
            _error(
                "adjustment_not_allowed",
                f"adjustment variable is not allowed_for_adjustment: {variable}",
                location,
            )
        )
    if spec.post_treatment:
        issues.append(
            _error(
                "adjustment_post_treatment",
                f"adjustment variable is post-treatment: {variable}",
                location,
            )
        )
    if spec.role in {
        FeatureRole.TREATMENT,
        FeatureRole.OUTCOME,
        FeatureRole.MEDIATOR,
        FeatureRole.COLLIDER,
    }:
        issues.append(
            _error(
                "adjustment_forbidden_role",
                f"adjustment variable has forbidden role: {variable} role={spec.role.value}",
                location,
            )
        )
    return issues


def _inference_mode(inference: StagePlan) -> str:
    override = _arg_value(inference.resolved_args, "--mode")
    if override is not None:
        return override
    config_path = inference.config_paths.get("config")
    if config_path is not None and config_path.exists():
        return str(load_yaml_mapping(config_path).get("mode", "edge_weight"))
    return "edge_weight"


def _arg_value(args: list[str], option: str) -> str | None:
    if option not in args:
        return None
    index = args.index(option)
    if index + 1 >= len(args):
        return None
    return args[index + 1]


def _arg_values(args: list[str], option: str) -> list[str] | None:
    if option not in args:
        return None
    index = args.index(option) + 1
    values: list[str] = []
    while index < len(args) and not args[index].startswith("--"):
        values.append(args[index])
        index += 1
    return values


def _adjustment_variables(
    feature_config: dict[str, object],
    strategy: str,
    treatment_config: dict[str, object],
) -> list[str]:
    if strategy == "manual":
        return [str(value) for value in treatment_config.get("covariates") or []]
    adjustment_sets = dict(feature_config.get("adjustment_sets", {}))
    selected = dict(adjustment_sets.get(strategy, {}))
    return [str(value) for value in selected.get("variables", selected.get("include", []))]


__all__ = ["CrossStageValidator"]
