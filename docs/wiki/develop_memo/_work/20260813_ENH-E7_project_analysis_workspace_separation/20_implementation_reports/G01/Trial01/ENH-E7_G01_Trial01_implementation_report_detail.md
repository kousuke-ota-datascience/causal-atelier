# Gate-local Implementation Report Detail — ENH-E7 G01 Trial01

> Candidate Assembly Agent の authority は ENH-E7-specific Candidate Assembly prompt に従う。

## Package ledger

| Package | State | Checkpoint full SHA | Status report | Checkpoint report |
| --- | --- | --- | --- | --- |
| P01 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P01_Trial01_package_execution_status.md` | N/A |
| P02 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P02_Trial01_package_execution_status.md` | N/A |
| P03 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P03_Trial01_package_execution_status.md` | N/A |
| P04 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P04_Trial01_package_execution_status.md` | N/A |
| P05 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P05_Trial01_package_execution_status.md` | N/A |
| P06 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P06_Trial01_package_execution_status.md` | N/A |
| P07 | PACKAGE_COMPLETE | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` | `packages/ENH-E7_G01_P07_Trial01_package_execution_status.md` | N/A |

Checkpoint SHA は各 package handoff 時点の traceability evidence であり、Trial Candidate SHA ではない。

## Integration observations

- `frontend/project_navigation.js` が Project route の正規化と所有権を持つ。
- `frontend/app.js` と `frontend/index.html` は Project management surface と Analysis surface の接続・互換ルートを担う。
- P01–P07 の focused product tests と近接する E3/E6 regression tests を一括実行し、39 passed を確認した。

## Protected contract observations

- `tests/product/test_enh_e6_g01_p01_navigation_transition.py` を Gate-wide selection に含め、既存の navigation transition contract は PASS した。
- Predictive、exploratory、Research Context、Results lineage/export の product contract tests も同 selection に含めて PASS した。

## Candidate-affecting diff audit

- 実装: `.dockerignore`、`Dockerfile.browser-e2e`、`frontend/app.js`、`frontend/index.html`、`frontend/project_navigation.js`。
- 検証: P01–P07 product tests、および `tests/browser_e2e/run_enh_e7_project_integration.py`。
- 上記と package handoff reports は commit `7936151d98de7fe467c176039add47da6af987c4` に含めた。freeze 前に working tree が clean であることを確認した。
- freeze 後に追加する本 detail/report completion は evidence-only である。

## Candidate Assembly verification commands/results

1. `git diff --cached --check` — PASS。
2. `uv run pytest -q tests/product/test_enh_e7_g01_p01_project_navigation_authority.py tests/product/test_enh_e7_g01_p02_projects_new_project_surface.py tests/product/test_enh_e7_g01_p03_overview_project_lifecycle.py tests/product/test_enh_e7_g01_p04_research_context_surface.py tests/product/test_enh_e7_g01_p05_data_analysis_view_surface.py tests/product/test_enh_e7_g01_p06_results_lineage_surface.py tests/product/test_enh_e7_g01_p07_project_integration_regression.py tests/product/test_research_context_e3.py tests/product/test_analysis_view_e3.py tests/product/test_exploratory_frontend_contract_e3.py tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py tests/product/test_predictive_frontend_contract_e3.py tests/product/test_enh_e6_g01_p01_navigation_transition.py` — **39 passed in 19.28s**。
3. Chromium E2E: `docker run --rm --entrypoint python --network ariadne-e1a_default ... ariadne-e1a-browser-e2e:playwright-1.62.0 /workspace/tests/browser_e2e/run_enh_e7_project_integration.py` — PASS。確認 scenario は `create-to-overview`、`legacy-analysis-shortcut`、`project-routes-reload-history`。
4. `git status --short` — 出力なし（freeze 前 clean）。

## Fixed Trial Candidate full SHA

`7936151d98de7fe467c176039add47da6af987c4`
