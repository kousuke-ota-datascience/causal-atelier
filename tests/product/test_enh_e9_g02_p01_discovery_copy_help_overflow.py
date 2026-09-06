"""Focused ENH-E9 G02 P01 coverage for Discovery clarity and local overflow."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_discovery_surface_has_purposeful_title_and_objective_rationale_help() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert "Discovery: Causal Structure Candidates" in html
    assert "データから候補因果構造を探索" in html
    assert 'name="objective"' in html
    assert 'name="rationale"' in html
    assert "このDiscovery実行で比較・検討したい候補因果構造" in html
    assert "選択したalgorithm、parameter、比較方法" in html


def test_graph_candidate_overflow_is_local_and_identity_rendering_is_unchanged() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    css = (REPOSITORY / "frontend" / "styles.css").read_text(encoding="utf-8")

    assert "#graph-candidates" in css
    assert "overflow-x: auto" in css
    assert "#graph-candidates table" in css
    render_candidates = app[app.index("function renderGraphCandidates()") : app.index("async function inspectCandidate(")]
    assert "c.candidate_id" in render_candidates
    assert "c.parent_graph_version_id||c.source_result_id||'root'" in render_candidates
    assert "inspectCandidate('${c.candidate_kind}','${c.candidate_id}')" in render_candidates
