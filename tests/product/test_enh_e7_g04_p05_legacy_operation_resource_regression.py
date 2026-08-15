"""Focused ENH-E7 G04 P05 regression coverage for legacy routes and operations."""

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _route_result() -> str:
    script = """
const fs = require('fs');
globalThis.window = globalThis;
eval(fs.readFileSync('frontend/navigation_state.js', 'utf8'));
const catalog = {families:[
  {slug:'exploratory', default_stage_id:'profile', stages:[{slug:'profile'}]},
  {slug:'predictive', default_stage_id:'setup', stages:[{slug:'setup'}]},
  {slug:'causal', default_stage_id:'setup', stages:[{slug:'setup'}, {slug:'discovery'}]},
]};
const n = AnalysisNavigation;
const legacy = ['explore', 'predictive', 'causal'].map(route => {
  const parsed = n.parse(`/projects/p1/${route}`, catalog);
  return n.serialize(n.legacyContext(catalog, parsed.projectId, parsed.legacy));
});
const resource = n.parse('/projects/p1/analysis/causal/discovery/resource/result/r1', catalog);
if (n.serialize(resource) !== '/projects/p1/analysis/causal/discovery/resource/result/r1') throw Error('resource route changed');
console.log(JSON.stringify({legacy, resource:n.serialize(resource)}));
"""
    result = subprocess.run(
        ["node", "-e", script], cwd=REPOSITORY, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def test_legacy_and_resource_routes_keep_canonical_analysis_semantics() -> None:
    assert _route_result() == (
        '{"legacy":["/projects/p1/analysis/exploratory/profile",'
        '"/projects/p1/analysis/predictive/setup",'
        '"/projects/p1/analysis/causal/setup"],'
        '"resource":"/projects/p1/analysis/causal/discovery/resource/result/r1"}'
    )


def test_data_quality_is_read_only_and_exploratory_operation_result_contracts_remain_fixed() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    runners = (REPOSITORY / "src" / "ariadne" / "capabilities" / "exploratory" / "runners.py").read_text(encoding="utf-8")
    surface = app[app.index("function renderExploratoryStageSurface(") : app.index("async function renderOperationAvailability()")]

    assert "DATA_QUALITY" not in app
    assert "Data Qualityは既存Profile resultをread-onlyで表示します。" in surface
    assert "/exploration/executions" not in surface
    assert "/exploration/preview" not in surface
    assert '"TIME_TREND": ("GROUP_SUMMARY_RESULT", "exploratory-time-trend-result/1")' in runners
    assert '"CHART": ("CHART_RESULT", "exploratory-chart-result/1")' in runners
    assert 'artifact_type="CHART_SPECIFICATION"' in runners
    assert 'media_type="application/vnd.vegalite.v5+json"' in runners


def test_causal_and_predictive_stage_navigation_remains_presentation_only() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    causal = app[app.index("function renderCausalStageSurface(") : app.index("async function renderOperationAvailability()")]
    predictive = app[app.index("function renderPredictiveStageSurface(") : app.index("async function renderOperationAvailability()")]

    assert "surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);" in causal
    assert "/execution-batches" not in causal and "/executions" not in causal
    assert "surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);" in predictive
    assert "/execution-plans" not in predictive and "method:'POST'" not in predictive


def test_route_restore_uses_resource_authority_without_backend_or_persistence_changes() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    restore = app[app.index("async function restoreProjectRoute()") : app.index("function clearAnalysisNavigationShell()")]

    assert "source:'legacy-route-normalization'" in restore
    assert "AnalysisNavigation.contextForResource" in restore
    assert "await applyAnalysisNavigation(parsed,{historyMode:ANALYSIS_HISTORY_MODES.NONE,source:'route-restore'});" in restore
    assert "method:'POST'" not in restore
    assert "method:'PUT'" not in restore
