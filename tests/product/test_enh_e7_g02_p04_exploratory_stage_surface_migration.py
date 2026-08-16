"""Focused ENH-E7 G02 P04 coverage for Exploratory stage-surface migration."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_every_exploratory_stage_maps_only_to_existing_operations_and_results() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    for stage, operations in {
        "profile": "['PROFILE']", "distribution": "['DISTRIBUTION']",
        "relationships": "['ASSOCIATION']", "comparison": "['GROUP_SUMMARY','TIME_TREND']",
        "findings": "['CHART']",
    }.items():
        assert f"{stage}:{operations}" in app
    for result_type in ("DATA_PROFILE_RESULT", "DISTRIBUTION_RESULT", "ASSOCIATION_RESULT", "GROUP_SUMMARY_RESULT"):
        assert result_type in app
    # Findings deliberately keeps the saved Exploratory Results surface rather than filtering it.
    assert "findings:null" in app
    assert "sampling:operation==='CHART'?{size:1000}:null" in app


def test_data_quality_is_read_only_profile_availability_without_an_execution() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    surface = app[app.index("function renderExploratoryStageSurface(") : app.index("async function renderOperationAvailability()")]

    assert 'id="exploratory-data-quality"' in html
    assert "const isDataQuality=stageSlug==='data-quality'" in surface
    assert "NO_PROFILE_RESULT" in surface
    assert "data-quality-profile-return" in surface
    assert "DATA_QUALITY" not in app
    assert "/exploration/executions" not in surface
    assert "/exploration/preview" not in surface


def test_stage_surface_reuses_existing_preview_execution_and_saved_result_handlers() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "$('#preview-exploration').onclick" in app
    assert "$('#exploration-form').onsubmit" in app
    assert "async function loadExplorationResults()" in app
    assert "function visibleExploratoryResults()" in app
    assert "function renderExplorationResults()" in app
    assert "TIME_TREND" in app and "GROUP_SUMMARY_RESULT" in app
