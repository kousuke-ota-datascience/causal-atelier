# ENH-E7 G01 Trial01 Implementation Report Detail

## Package ledger

| Package | State | Status report | Optional implementation HEAD |
| --- | --- | --- | --- |
| P01 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P01_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P02 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P02_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P03 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P03_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P04 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P04_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P05 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P05_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P06 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P06_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |
| P07 | `PACKAGE_COMPLETE` | `packages/ENH-E7_G01_P07_Trial01_package_execution_status.md` | `0979bcf417142cf565d8a5f9cfa271de3c96a7a5` |

Package-level implementation HEADはtraceability evidenceであり、candidate identityではない。

## Integration observations

- `frontend/project_navigation.js`がProject routeの正規化とownershipを担い、`frontend/app.js` / `frontend/index.html`がProject Management surfaceと既存Analysis surfaceの接続を担う。
- P01–P07 focused product testsとResearch Context、Analysis View、Results / Lineage、Predictive、ENH-E6 navigation regressionをGate-wide selectionで実行した。

## Protected contract observations

- `tests/product/test_enh_e6_g01_p01_navigation_transition.py`はPASSし、ENH-E6 G01のcanonical Analysis Family / Stage navigation・transition semanticsに回帰は検出されなかった。
- `test_predictive_frontend_contract_e3.py`および`test_exploratory_frontend_contract_e3.py`もPASSし、Analysis View cross-family inputとlegacy analytical UI compatibilityに対する回帰は検出されなかった。

## Candidate-affecting diff audit

- Fixed Candidate `7936151d98de7fe467c176039add47da6af987c4`には、Project routing / surface implementation、P01–P07 product tests、`run_enh_e7_project_integration.py`、browser runner packagingが含まれる。
- `7936151…`からAssembly開始時HEAD `266b627…`までの差分はcompletion/detail reportの2ファイルのみである。
- freeze前および再検証後の`git status --short`は出力なし、`git diff --check`はPASSである。

## Candidate Assembly verification commands/results

1. `uv run pytest -q tests/product/test_enh_e7_g01_p01_project_navigation_authority.py tests/product/test_enh_e7_g01_p02_projects_new_project_surface.py tests/product/test_enh_e7_g01_p03_overview_project_lifecycle.py tests/product/test_enh_e7_g01_p04_research_context_surface.py tests/product/test_enh_e7_g01_p05_data_analysis_view_surface.py tests/product/test_enh_e7_g01_p06_results_lineage_surface.py tests/product/test_enh_e7_g01_p07_project_integration_regression.py tests/product/test_research_context_e3.py tests/product/test_analysis_view_e3.py tests/product/test_exploratory_frontend_contract_e3.py tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py tests/product/test_predictive_frontend_contract_e3.py tests/product/test_enh_e6_g01_p01_navigation_transition.py` — PASS; 39 passed in 16.27s。
2. `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e build browser-e2e` — current `Dockerfile.browser-e2e`からP07 runnerを含むimageをbuild。BuildKit provenance metadataの書込みはdisk-fullで警告されたが、image exportおよびrunner copyは完了した。
3. `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --rm --no-deps --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py` — PASS。evidenceは`test-results/browser_e2e/enh-e7-project-integration-evidence.json`にあり、3 scenarioすべてPASS。
4. `git diff --check`および`git status --short` — PASS / clean（report編集前）。

## Fixed Trial Candidate full SHA

`7936151d98de7fe467c176039add47da6af987c4`
