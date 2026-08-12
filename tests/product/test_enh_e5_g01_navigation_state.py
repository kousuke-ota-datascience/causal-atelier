"""Focused contract tests for ENH-E5 G01 P01 URL navigation state."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_navigation_state_preserves_canonical_routes_and_rejects_invalid_routes() -> None:
    repository = Path(__file__).parents[2]
    script = f"""
const fs = require('fs');
const vm = require('vm');
vm.runInThisContext(fs.readFileSync({str(repository / 'frontend/navigation_state.js')!r}, 'utf8'));
const catalog = {{families: [
  {{slug:'exploratory',default_stage_id:'profile',stages:[{{slug:'profile'}},{{slug:'findings'}}]}},
  {{slug:'predictive',default_stage_id:'setup',stages:[{{slug:'setup'}},{{slug:'metrics'}}]}},
  {{slug:'causal',default_stage_id:'setup',stages:[{{slug:'setup'}},{{slug:'estimation'}}]}},
]}};
const n = globalThis.AnalysisNavigation;
const context = n.parse('/projects/p1/analysis/causal/estimation/resource/result/r1', catalog);
if (n.serialize(context) !== '/projects/p1/analysis/causal/estimation/resource/result/r1') throw Error('round trip failed');
if (context.stageSlug !== 'estimation') throw Error('explicit stage not retained');
const legacy = n.parse('/projects/p1/explore', catalog);
if (n.serialize(n.legacyContext(catalog, legacy.projectId, legacy.legacy)) !== '/projects/p1/analysis/exploratory/profile') throw Error('legacy mapping failed');
for (const path of ['/projects/p1/analysis/unknown/setup', '/projects/p1/analysis/causal/unknown', '/projects/p1/analysis/causal/setup/resource/unknown/r1']) {{
  try {{ n.parse(path, catalog); throw Error('invalid route accepted: ' + path); }}
  catch (error) {{ if (!(error instanceof n.NavigationRouteError)) throw error; }}
}}
(async () => {{
  const api = async (path) => path === '/executions/e1'
    ? {{analysis_family: 'PREDICTIVE'}}
    : (() => {{ throw Error('unexpected resource request: ' + path); }})();
  const direct = await n.contextForResource(catalog, api, 'p1', 'execution', 'e1');
  if (direct.familySlug !== 'predictive' || direct.stageSlug !== 'setup') throw Error('resource default route failed');
  try {{
    await n.contextForResource(catalog, api, 'p1', 'execution', 'e1', {{familySlug: 'causal', stageSlug: 'setup'}});
    throw Error('family mismatch accepted');
  }} catch (error) {{
    if (!(error instanceof n.NavigationRouteError) || error.code !== 'NAVIGATION_RESOURCE_FAMILY_MISMATCH') throw error;
  }}
}})().catch((error) => {{ console.error(error); process.exitCode = 1; }});
"""
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout
