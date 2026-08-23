from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_effects_and_diagnostics_have_stage_specific_guidance():
    source = (FRONTEND / "causal_stage_presentation.js").read_text(encoding="utf-8")

    assert "effects:Object.freeze" in source
    assert "diagnostics:Object.freeze" in source
    assert "purpose:'このページでは、保存済みTreatment Effect Result" in source
    assert "displayScope:'Treatment / Outcome / Estimand / Estimator / Adjustment set" in source
    assert "purpose:'このページでは、推定値そのものの大きさではなく" in source
    assert "Sample loss" in source
    assert "Covariate balance（現行Resultではunweighted / before weighting）" in source
    assert "ESS、weight diagnostics、weighted / post-adjustment balance" in source
    assert "applyStageGuidance(presentation)" in source


def test_diagnostics_presentation_replaces_raw_json_primary_surface():
    source = (FRONTEND / "causal_diagnostics_presentation.js").read_text(encoding="utf-8")

    for expected in (
        "Analysis context",
        "Sample support",
        "Covariate balance",
        "Propensity overlap",
        "Scientific warnings",
        "Associated Treatment Effect",
        "Technical details / Lineage",
    ):
        assert expected in source

    assert "Unweighted / before weighting" in source
    assert "n_input" in source
    assert "n_complete" in source
    assert "n_treated" in source
    assert "n_control" in source
    assert "sample_loss" in source
    assert "standardized_mean_difference" in source
    assert "n_ps_below_0_01" in source
    assert "n_ps_above_0_99" in source
    assert "item.result_type==='TREATMENT_EFFECT_RESULT'" in source

    # Backend-owned gaps must not be fabricated by the presentation layer.
    assert "現行backend Resultに構造化保存されていない" in source


def test_diagnostics_module_is_loaded_with_other_causal_presentations():
    source = (FRONTEND / "causal_stage_presentation.js").read_text(encoding="utf-8")

    assert "loadRuntimeScript('/causal_effects_presentation.js','causal-effects-presentation')" in source
    assert "loadRuntimeScript('/causal_diagnostics_presentation.js','causal-diagnostics-presentation')" in source


def test_diagnostics_backend_handoff_is_documented():
    handoff = ROOT / "docs/wiki/develop_memo/_work/20260823_ENH-E9_causal_result_presentation_followup/01_backend_handoff.md"
    source = handoff.read_text(encoding="utf-8")

    assert "Effective sample size (ESS)" in source
    assert "Weight diagnostics" in source
    assert "Weighted / post-adjustment balance" in source
    assert "新しい`DIAGNOSTICS` runtime operationを追加しない" in source
