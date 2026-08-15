# ENH-E7 G04 P04 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
- Trial: 01
- Package: P04
- State: PACKAGE_COMPLETE
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: cc4fb35b66545af50ed96fd2f80aff7f9a619a5e

## 実施したscope

- Chromium integration runnerに、Analysis reload、Analysis→Project Management return、Analysis→Results / Lineage、Back/Forwardのcross-surfaceシナリオを追加した。
- history restore / duplicate-entry guard / stale Analysis shell clearをfocused product testで固定した。

## Changed files / responsibility

- `tests/browser_e2e/run_enh_e7_project_integration.py`: selected Project identityを保ったPM→Analysis→PM、およびAnalysis→Results→Back/Forwardのbrowser evidenceを追加した。
- `tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py`: cross-surface browser coverageとshared transition authorityを検査するfocused product testを追加した。
- 本status report: package handoff evidence。

## Required invariant conclusion

- Chromium E2EでPM→Analysis→PM、Analysis→Results、Back/Forward、reloadの各遷移がpathname・Project identity・visible workspaceを整合させた。
- `popstate`はroute-authoritative restoreへ集約され、同一pathnameへのhistory同期はno-opであるためduplicate entryを追加しない。
- PM / Resultsへ戻ると`TopLevelSurfaceActivation`と`clearAnalysisNavigationShell`によりstale Analysis shellを残さない。
- backend/API/persistence semanticsは変更していない。

## Focused verification

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py`
  - exit code: 0
  - result: 3 passed
- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py tests/product/test_enh_e7_g01_p07_project_integration_regression.py tests/product/test_enh_e6_g01_p01_navigation_transition.py tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py`
  - exit code: 0
  - result: 12 passed
- `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
  - exit code: 0
  - result: PASS (`create-to-overview`, `project-routes-reload-history`, `project-analysis-launcher`, `cross-surface-reload-history`)
  - evidence: `test-results/browser_e2e/enh-e7-project-integration-evidence.json`
- `node --check frontend/app.js`, `python3 -m py_compile tests/browser_e2e/run_enh_e7_project_integration.py`, `git diff --check`
  - exit code: 0
  - result: PASS
- source/diff audit
  - result: browser test scopeのみを変更した。DOM ownership、event binding、backend/API/persistence semanticsにout-of-scope changeおよびdead codeはない。

## Remaining / blocker

- None within P04 scope.
- P01〜P03の未コミット変更および既存の範囲外documentation / G03 artifactsは本packageでは変更・stageしていない。

## Scope guard確認

- legacy URL normalizationおよびoperation behavior修復（P05）、Acceptance Criteria、P05以降のpackage scope、backend/API/persistence semanticsは変更していない。
