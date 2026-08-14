"""Focused ENH-E7 G01 P06 coverage for the Project-local Results surface."""

import re
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _results_section() -> str:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    match = re.search(r'<section id="results" class="workspace.*?</section>', html, flags=re.DOTALL)
    assert match is not None
    return match.group(0)


def test_results_surface_owns_cross_analysis_filters_comparison_artifacts_lineage_and_annotations() -> None:
    section = _results_section()
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    for identifier in (
        "result-summary", "result-family-filter", "result-type-filter", "result-status-filter",
        "unified-result-list", "compare-results", "result-comparison", "artifacts", "lineage",
        "annotation-form", "annotations",
    ):
        assert f'id="{identifier}"' in section
    assert "api(`/projects/${state.project.project_id}/results`)" in app
    assert "api(`/projects/${state.project.project_id}/results/summary`)" in app
    assert "api(`/projects/${state.project.project_id}/comparisons`" in app
    assert "api(`/projects/${state.project.project_id}/workspace-annotations`" in app


def test_results_surface_is_project_local_and_does_not_absorb_stage_execution_control() -> None:
    section = _results_section()
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "execution-batches" not in section
    assert "run-predictive" not in section
    result_handlers = app[app.index("function filteredUnifiedResults()") : app.index("async function refreshAll()")]
    assert "execution-batches" not in result_handlers
    assert "execution-plans" not in result_handlers
