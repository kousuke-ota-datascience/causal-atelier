"""ENH-E9 regression guard for stage-separated causal Estimation submission."""

from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


REPOSITORY = _repository_root()


def test_estimation_action_bypasses_hidden_identification_form_validation() -> None:
    module = (REPOSITORY / "frontend" / "causal_estimation_submission.js").read_text(
        encoding="utf-8"
    )

    assert "const button=$('#run-estimation')||$('#estimation-inputs button');" in module
    assert "button.type='button';" in module
    assert "button.id='run-estimation';" in module
    assert "button.onclick=runEstimation;" in module
    assert "form.onsubmit=event=>event.preventDefault();" in module


def test_estimation_uses_identification_lineage_instead_of_hidden_current_form_inputs() -> None:
    module = (REPOSITORY / "frontend" / "causal_estimation_submission.js").read_text(
        encoding="utf-8"
    )

    assert "selectedIdentificationResult()" in module
    assert "`/executions/${upstream.execution.execution_id}/prefill`" in module
    assert "dataset_version_id:prefill.dataset_version_id" in module
    assert "input_graph_version_id:prefill.input_graph_version_id" in module
    assert "input_result_id:upstream.result_id" in module
    assert "const spec=structuredClone(prefill.analysis_spec);" in module
    assert "spec.operation_spec={inference_options:{}};" in module
    assert "spec.validation_override=override;" in module
    assert "dataset_version_id:values.get" not in module
    assert "input_graph_version_id:values.get" not in module


def test_causal_runtime_loads_estimation_action_after_app_runtime_is_available() -> None:
    presentation = (REPOSITORY / "frontend" / "causal_stage_presentation.js").read_text(
        encoding="utf-8"
    )

    assert "global.addEventListener('DOMContentLoaded'" in presentation
    assert "function loadRuntimeScript(src,datasetKey)" in presentation
    assert "loadRuntimeScript('/causal_estimation_submission.js','causal-estimation-submission');" in presentation


def test_stage_renderer_remains_presentation_only() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    surface = app[
        app.index("function renderCausalStageSurface(") :
        app.index("const EXPLORATORY_STAGE_OPERATIONS")
    ]

    assert "surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);" in surface
    assert "disabled" not in surface
    assert "/execution-batches" not in surface
