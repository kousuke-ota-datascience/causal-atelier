from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_exploratory_family_is_a_canonical_non_causal_analysis_stage_surface() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'data-top-level-surface-root="analysis"' in html
    assert 'id="analysis-family-tabs"' in html
    assert 'id="analysis-stage-sidebar"' in html
    assert 'data-workspace="explore"' not in html
    # The existing Explore content is a stage-owned presentation substrate, not
    # an independently routable top-level workspace.
    assert 'id="explore" class="workspace"' in html
    assert all(value in html for value in (
        'id="analysis-view-form"', 'id="analysis-view-list"',
        'id="exploration-form"', 'id="exploration-output"',
        'id="exploration-results"', "Preview（未保存）",
    ))
    assert all(operation in javascript for operation in (
        "PROFILE", "DISTRIBUTION", "ASSOCIATION", "GROUP_SUMMARY",
        "TIME_TREND", "CHART",
    ))
    assert "EXPLORATORY" in html
    assert "因果効果または確認的結論ではありません" in html
    assert all(value in javascript for value in (
        "/analysis-views", "/exploration/preview", "/exploration/executions",
        "/exploration/results", "waitForExploration", "Causal draft",
        "Predictive draft", "source_relation.warning",
    ))
    assert "探索的結果です。因果効果または確認的結論ではありません。" in javascript
    navigation = (REPOSITORY / "frontend" / "navigation_state.js").read_text(encoding="utf-8")
    assert 'explore: ["exploratory", "profile"]' in navigation
    assert "function serialize(context)" in navigation


def test_saved_exploration_waits_for_the_worker_terminal_state() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "response.status==='QUEUED'" in javascript
    assert "execution.status==='SUCCEEDED'" in javascript
    assert "execution.status==='FAILED'" in javascript
    assert "await waitForExploration(response.execution_id)" in javascript


def test_dataset_refresh_preserves_a_selected_analysis_view_dataset() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "const selected=select.dataset.selectedDatasetVersionId||select.value" in javascript
    assert "if(state.datasets.some(d=>d.dataset_version_id===selected)){select.value=selected" in javascript
    assert "select.dataset.selectedDatasetVersionId=select.value" in javascript


def test_exploration_result_draft_transitions_submit_exploratory_mode() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "createExplorationDraft('${result.result_id}','CAUSAL')" in javascript
    assert "createExplorationDraft('${result.result_id}','PREDICTIVE')" in javascript
    assert "const researchContextVersionId=$('#common-context').value" in javascript
    assert (
        "body:JSON.stringify({target_family:family,analysis_mode:'EXPLORATORY',"
        "research_context_version_id:researchContextVersionId||undefined})"
        in javascript
    )
