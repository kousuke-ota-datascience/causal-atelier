"""Focused ENH-E7 G02 P05 coverage for Predictive stage-surface migration."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_predictive_stage_surfaces_preserve_the_existing_workflow_sequence() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    for stage in ("setup", "train", "metrics", "explainability", "model-management", "predict"):
        assert stage in html
    for result_type in ("TRAINING_RESULT", "EVALUATION_RESULT", "ERROR_ANALYSIS_RESULT", "PREDICTIVE_EXPLANATION_RESULT", "MODEL_CARD_RESULT"):
        assert result_type in app
    assert "function renderPredictiveStageSurface(stageSlug)" in app
    assert "renderPredictiveStageSurface(context?.familySlug==='predictive'?context.stageSlug:null);" in app


def test_predict_stage_reads_only_the_existing_prediction_artifact() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    surface = app[app.index("const PREDICTIVE_STAGE_ARTIFACT_TYPES") : app.index("async function renderOperationAvailability()")]
    details = app[app.index("function renderPredictiveDetails()") : app.index("window.showPredictiveExecution")]

    assert "predict:['PREDICTION']" in surface
    assert "Prediction outputはありません。" in details
    assert "PREDICTION_RESULT" not in app
    assert "/executions" not in surface


def test_stage_presentation_filters_existing_reads_without_new_execution_semantics() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    details = app[app.index("function renderPredictiveDetails()") : app.index("window.showPredictiveExecution")]

    assert "PREDICTIVE_STAGE_RESULT_TYPES[stage]" in details
    assert "PREDICTIVE_STAGE_ARTIFACT_TYPES[stage]" in details
    assert "details.results].filter" in details
    assert "details.artifacts.filter" in details
    assert "/execution-plans" not in details
    assert "method:'POST'" not in details
