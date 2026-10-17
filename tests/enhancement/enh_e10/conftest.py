from __future__ import annotations

import pytest


@pytest.fixture
def predictive_spec_factory():  # type: ignore[no-untyped-def]
    """Build the fixed, deterministic predictive specification used by ENH-E10."""
    def build(task_type: str = "BINARY_CLASSIFICATION") -> dict:  # type: ignore[type-arg]
        metric = "ROC_AUC" if task_type == "BINARY_CLASSIFICATION" else "RMSE"
        return {
            "schema_version": "predictive-analysis-spec/1",
            "task_type": task_type,
            "prediction_question": {
                "prediction_unit": "customer", "target": "converted",
                "prediction_time": "2026-01-01T00:00:00Z", "horizon": "30 days",
                "intended_use": "prioritize outreach",
                "deployment_population": "eligible customers",
            },
            "feature_spec": {
                "feature_columns": ["score"],
                "availability_cutoff": {"score": {
                    "column": "score", "available_at": "PREDICTION_TIME", "allowed": True,
                }},
                "excluded_columns": ["converted", "customer_id"],
            },
            "split_spec": {
                "strategy": "RANDOM", "train_ratio": 0.6,
                "validation_ratio": 0.2, "test_ratio": 0.2,
                "group_column": None, "time_column": None,
                "train_cutoff": None, "validation_cutoff": None,
                "stratify": False, "seed": 17,
            },
            "preprocessing_spec": {}, "model_spec": {}, "tuning_spec": {},
            "evaluation_spec": {
                "primary_metric": metric, "secondary_metrics": [], "subgroups": [],
            },
            "explanation_spec": {},
        }
    return build
