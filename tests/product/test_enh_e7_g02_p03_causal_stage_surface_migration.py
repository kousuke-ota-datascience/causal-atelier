"""Focused ENH-E7 G02 P03 coverage for Causal stage-surface migration."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_existing_causal_operations_are_owned_by_their_presentation_stages() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    expected = {
        "setup": ("Direct Graph Registration",),
        "discovery": ('id="discovery-form"', "Discovery Executions", "Graph Candidates"),
        "identification": ('id="identification-inputs"', "Identification / Eligibility / Gate"),
        "estimation": ('id="estimation-inputs"',),
        "effects": ("Treatment Effects", 'id="treatment-effect-results"'),
        "diagnostics": ("Diagnostics", 'id="diagnostics-results"'),
        "sensitivity": ('id="refutation-form"', 'id="sensitivity-form"'),
    }
    for stage, markers in expected.items():
        assert f'data-causal-stage-surface="{stage}"' in html
        for marker in markers:
            assert marker in html
    assert 'data-causal-stage-surface="effects diagnostics"' not in html


def test_stage_navigation_only_changes_presentation_visibility() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    surface = app[app.index("function renderCausalStageSurface(") : app.index("async function renderOperationAvailability()")]

    assert "surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);" in surface
    assert "renderCausalStageSurface(context.stageSlug);" in app
    assert "renderCausalStageSurface(null);" in app
    assert "/execution-batches" not in surface
    assert "/executions" not in surface
    assert "history.pushState" not in surface


def test_existing_causal_handlers_and_backend_stage_model_remain_unchanged() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    for identifier in ("discovery-form", "inference-form", "run-identification", "refutation-form", "sensitivity-form"):
        assert f'id="{identifier}"' in html
    for handler in ("$('#discovery-form').onsubmit", "$('#run-identification').onclick", "$('#inference-form').onsubmit", "$('#refutation-form').onsubmit", "$('#sensitivity-form').onsubmit"):
        assert handler in app
    assert "new backend stage" not in app.lower()
