from __future__ import annotations

import ast
from pathlib import Path

from causal_atelier.causal.design import CausalDesign
from causal_atelier.infrastructure.config import hash_mapping, load_yaml_mapping
from causal_atelier.preprocessing.common import FeatureRole, FeatureSemanticSpec, FeatureSemanticsCatalog
from causal_atelier.shared.validation import ValidationIssue, ValidationResult, ValidationSeverity


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_validation_result_detects_errors() -> None:
    result = ValidationResult(
        [ValidationIssue(ValidationSeverity.ERROR, "bad", "message")]
    )

    assert result.has_errors


def test_yaml_hash_and_causal_design_schema() -> None:
    config = load_yaml_mapping(
        PROJECT_ROOT / "configs/causal/inference/designs/completejourney_household.yaml"
    )
    design = CausalDesign.from_mapping(config)

    assert design.estimand.value == "ATE"
    assert design.treatment.name == "treated"
    assert len(hash_mapping(design.to_dict())) == 64


def test_feature_semantics_catalog_loads_roles() -> None:
    catalog = FeatureSemanticsCatalog.from_mapping(
        load_yaml_mapping(PROJECT_ROOT / "configs/preprocessing/feature_semantics.yaml")
    ).by_name()

    assert catalog["treated"].role == FeatureRole.TREATMENT
    assert catalog["outcome_sales_value"].role == FeatureRole.OUTCOME
    assert FeatureSemanticSpec(
        name="x",
        role=FeatureRole.COVARIATE,
        source_table="t",
        source_column="c",
        unit_id="u",
    ).allowed_for_adjustment is False


def test_shared_layer_does_not_import_application_or_causal_packages() -> None:
    forbidden = {
        "causal_atelier.application",
        "causal_atelier.causal",
        "causal_atelier.interfaces",
    }
    for path in (PROJECT_ROOT / "src/causal_atelier/shared").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported = {node.module}
            else:
                continue
            assert not any(
                name == prefix or name.startswith(f"{prefix}.")
                for name in imported
                for prefix in forbidden
            ), path
