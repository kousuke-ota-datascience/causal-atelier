"""Focused ENH-E8 G02 P02 Causal Stage ownership coverage."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _surface(html: str, stage: str) -> str:
    return "\n".join(
        line for line in html.splitlines() if f'data-causal-stage-surface="{stage}"' in line
    )


def test_causal_primary_surfaces_are_stage_owned_and_have_japanese_purposes() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    presentation = (REPOSITORY / "frontend" / "causal_stage_presentation.js").read_text(encoding="utf-8")

    for stage in ("identification", "estimation", "effects", "diagnostics", "sensitivity"):
        assert f"{stage}:Object.freeze" in presentation
    for expected in ("因果効果を識別", "選択したIdentification Result", "保存済み（saved）の処置効果", "balance、overlap", "Refutationと感度分析"):
        assert expected in presentation
    assert 'data-causal-stage-surface="effects diagnostics"' not in html
    assert 'id="treatment-effect-results"' in _surface(html, "effects")
    assert 'id="diagnostics-results"' in _surface(html, "diagnostics")
    assert 'id="refutation-form"' in _surface(html, "sensitivity")
    assert 'id="sensitivity-form"' in _surface(html, "sensitivity")


def test_wrong_stage_controls_are_hidden_by_the_presentation_only_surface_renderer() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    surface = app[app.index("function renderCausalStageSurface(") : app.index("const EXPLORATORY_STAGE_OPERATIONS")]

    assert "surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);" in surface
    assert "disabled" not in surface
    assert "/execution-batches" not in surface
    assert "history.pushState" not in surface


def test_causal_results_render_to_separate_estimation_effects_and_diagnostics_surfaces() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "resultRows('ESTIMATION',$('#estimation-results'))" in app
    assert "causalResultRows(['TREATMENT_EFFECT_RESULT'],$('#treatment-effect-results'))" in app
    assert "causalResultRows(['DIAGNOSTICS_RESULT'],$('#diagnostics-results'))" in app
    assert "$('#compare-effects').onclick=()=>compareChecked('#treatment-effect-results','#effects-comparison',2);" in app
