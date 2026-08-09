"""ENH-E4 G05 canonical family Result and Artifact types."""

from alembic import op


revision = "20260809_product_0010"
down_revision = "20260809_product_0009"
branch_labels = None
depends_on = None


_RESULT_TYPES = "'DISCOVERY_GRAPH_RESULT','IDENTIFICATION_RESULT','DATA_ELIGIBILITY_RESULT','TREATMENT_EFFECT_RESULT','DIAGNOSTICS_RESULT','REFUTATION_RESULT','SENSITIVITY_RESULT','DATA_PROFILE_RESULT','DISTRIBUTION_RESULT','ASSOCIATION_RESULT','GROUP_SUMMARY_RESULT','CHART_RESULT','SPLIT_RESULT','TRAINING_RESULT','EVALUATION_RESULT','ERROR_ANALYSIS_RESULT','PREDICTIVE_EXPLANATION_RESULT','MODEL_CARD_RESULT'"
_STATUSES = "'GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE','IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW','PASS','WARN','FAIL','ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE','ROBUST','FRAGILE','TRAINED','TRAINED_WITH_WARNINGS','EVALUATED','INSUFFICIENT_TEST_SAMPLE','NOT_APPLICABLE'"
_ARTIFACT_TYPES = "'DATASET_FILE','GRAPH_JSON','GRAPH_IMAGE','EFFECT_TABLE','DIAGNOSTICS_TABLE','MANIFEST','CONFIG_SNAPSHOT','LOG','SCIENTIFIC_RESULT_JSON','SCIENTIFIC_REPORT','CHART_SPECIFICATION','PARTITION_INDEX','FITTED_PREPROCESSOR','FITTED_MODEL','PREDICTION','PREDICTIVE_EXPLANATION','MODEL_CARD'"


def upgrade() -> None:
    op.drop_constraint("ck_product_result_type", "product_result", type_="check")
    op.drop_constraint("ck_product_result_scientific_status", "product_result", type_="check")
    op.drop_constraint("ck_product_result_status_matrix", "product_result", type_="check")
    op.create_check_constraint("ck_product_result_type", "product_result", f"result_type IN ({_RESULT_TYPES})")
    op.create_check_constraint("ck_product_result_scientific_status", "product_result", f"scientific_status IN ({_STATUSES})")
    op.create_check_constraint("ck_product_result_status_matrix", "product_result", "(result_type IN ('DATA_PROFILE_RESULT','DISTRIBUTION_RESULT','ASSOCIATION_RESULT','GROUP_SUMMARY_RESULT','CHART_RESULT','ERROR_ANALYSIS_RESULT','MODEL_CARD_RESULT') AND scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS')) OR (result_type = 'SPLIT_RESULT' AND scientific_status = 'PASS') OR (result_type = 'TRAINING_RESULT' AND scientific_status IN ('TRAINED','TRAINED_WITH_WARNINGS')) OR (result_type = 'EVALUATION_RESULT' AND scientific_status IN ('EVALUATED','INSUFFICIENT_TEST_SAMPLE')) OR (result_type = 'PREDICTIVE_EXPLANATION_RESULT' AND scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','NOT_APPLICABLE')) OR (result_type = 'DISCOVERY_GRAPH_RESULT' AND scientific_status IN ('GENERATED','GENERATED_WITH_WARNINGS','UNRELIABLE')) OR (result_type = 'IDENTIFICATION_RESULT' AND scientific_status IN ('IDENTIFIED','NOT_IDENTIFIED','PARTIALLY_IDENTIFIED','REQUIRES_REVIEW')) OR (result_type IN ('DATA_ELIGIBILITY_RESULT','DIAGNOSTICS_RESULT') AND scientific_status IN ('PASS','WARN','FAIL')) OR (result_type = 'TREATMENT_EFFECT_RESULT' AND scientific_status IN ('ESTIMATED','INSUFFICIENT_OVERLAP','INSUFFICIENT_SAMPLE','ESTIMATION_UNRELIABLE','REQUIRES_REVIEW')) OR (result_type = 'REFUTATION_RESULT' AND scientific_status IN ('NO_FAILURE_DETECTED','FAILURE_DETECTED','INCONCLUSIVE')) OR (result_type = 'SENSITIVITY_RESULT' AND scientific_status IN ('ROBUST','FRAGILE','INCONCLUSIVE'))")
    op.drop_constraint("ck_product_artifact_type", "product_artifact", type_="check")
    op.create_check_constraint("ck_product_artifact_type", "product_artifact", f"artifact_type IN ({_ARTIFACT_TYPES})")


def downgrade() -> None:
    raise NotImplementedError("G05 family output type migration is intentionally forward-only")
