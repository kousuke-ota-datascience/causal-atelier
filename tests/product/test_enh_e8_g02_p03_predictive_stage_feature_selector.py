"""Focused ENH-E8 G02 P03 Predictive presentation and selector coverage."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_setup_owns_the_only_editable_schema_backed_feature_selector() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert 'id="open-predictive-feature-selector"' in html
    assert 'name="feature_columns" value="score" required readonly' in html
    assert 'id="predictive-feature-modal"' in html
    assert 'id="predictive-feature-options"' in html
    assert 'data-predictive-stage-surface="setup"' in html
    assert 'open-predictive-feature-selector' not in html.split('data-predictive-stage-surface="train"', 1)[1]


def test_predictive_stage_results_are_not_a_shared_generic_card() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    for stage, marker in (("train", "predictive-train-feature-context"), ("predict", "predictive-predict-context"),
                          ("metrics", "predictive-results"), ("explainability", "predictive-explainability-results"),
                          ("model-management", "predictive-model-results")):
        assert f'data-predictive-stage-surface="{stage}"' in html
        assert f'id="{marker}"' in html
    assert 'data-predictive-stage-surface="train metrics explainability model-management"' not in html


def test_selector_uses_selected_dataset_schema_and_preserves_spec_field_authority() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "function selectedPredictiveDataset()" in app
    assert "Object.keys(dataset.schema||{})" in app
    assert "$('#predictive-feature-options input:checked')" in app
    assert "filter(name=>checked.has(name)).join(', ')" in app
    assert "reconcilePredictiveFeatures({announce:true})" in app
    assert "feature_spec:{feature_columns:features" in app
    assert "Feature columns (read-only):" in app
    assert "このExecution specificationに記録されたFeature columns（read-only）" in app
