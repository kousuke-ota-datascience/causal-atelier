"""Focused ENH-E7 G01 P05 coverage for the Data and Analysis View surface."""

import re
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _section(html: str, section_id: str) -> str:
    match = re.search(
        rf'<section id="{section_id}" class="workspace.*?</section>', html, flags=re.DOTALL
    )
    assert match is not None
    return match.group(0)


def test_data_owns_dataset_version_schema_preview_and_analysis_view_lifecycle() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    data = _section(html, "data")
    explore = _section(html, "explore")

    for identifier in ("dataset-form", "datasets", "preview", "analysis-view-form", "analysis-view-list"):
        assert f'id="{identifier}"' in data
    assert 'id="analysis-view-form"' not in explore
    assert "window.preview=async id=>" in app
    assert "window.fixAnalysisView=async id=>" in app


def test_fixed_analysis_views_remain_cross_family_inputs() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$('#exploration-view').innerHTML" in app
    assert "$('#predictive-view').innerHTML" in app
    assert "state.analysisViews.filter(view=>view.status==='FIXED')" in app
    assert "/projects/${state.project.project_id}/analysis-views" in app
