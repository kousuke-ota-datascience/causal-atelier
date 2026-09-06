"""ENH-E9 G04 P04 frontend contract checks for persisted diagnostics only."""

from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


SOURCE = ( _repository_root() / "frontend" / "causal_diagnostics_presentation.js").read_text(encoding="utf-8")


def test_structured_weighting_and_balance_fields_are_primary_authority() -> None:
    assert "function weightingSection(payload)" in SOURCE
    assert "const weighting=payload.weighting;" in SOURCE
    assert "const structured=payload.balance&&typeof payload.balance==='object'&&!Array.isArray(payload.balance)" in SOURCE
    assert "structured.before" in SOURCE
    assert "structured.after" in SOURCE
    assert "structured?.after_applicability" in SOURCE
    assert "weighting.effective_sample_size||{}" in SOURCE
    assert "weighting.treated" in SOURCE
    assert "weighting.control" in SOURCE
    assert "stats.extreme_rule" in SOURCE


def test_null_and_legacy_payloads_are_presented_without_scientific_fallbacks() -> None:
    assert "legacy balance is shown only as before-balance" in SOURCE
    assert "Post-weight balance: ${applicability?'not provided / not applicable'" in SOURCE
    assert "whole-estimator final weightではありません" in SOURCE
    assert "weight/ESS/after-balanceはnot applicableです" in SOURCE
    assert "ess.treated===null||ess.treated===undefined?'N/A'" in SOURCE
    assert "ess.control===null||ess.control===undefined?'N/A'" in SOURCE


def test_renderer_does_not_recompute_or_infer_weighting_science() -> None:
    weighting = SOURCE[SOURCE.index("function weightingSection(payload)") : SOURCE.index("function overlapSection", SOURCE.index("function weightingSection(payload)"))]

    for forbidden in ("Math.", "quantile", "weighting.definition.split", "weighting.definition.match", "estimatorName("):
        assert forbidden not in weighting
    assert "weighting.applicability" in weighting
