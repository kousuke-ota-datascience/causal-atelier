# ENH-E7 G04 P06 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
- Trial: 01
- Package: P06
- State: PACKAGE_COMPLETE
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: cc4fb35b66545af50ed96fd2f80aff7f9a619a5e

## 実施したscope

- browser integration runnerを`/` entry、full Projects→PM→Analysis Family/Stage→Results→PM journey、reload、Back/Forwardまで拡張した。
- 各workspaceでvisible top-level rootが正確に1つであることと、console/page errorが0件であることを実測するようにした。
- history mutation / global event binding / temporary fallbackのsource auditをfocused coverageへ追加した。

## Changed files / responsibility

- `tests/browser_e2e/run_enh_e7_project_integration.py`: root normalization、surface root排他性、Family/Stage遷移、console/page-error監査をChromium journeyへ追加した。
- `tests/product/test_enh_e7_g04_p06_full_integration_cleanup.py`: full journey runnerとduplicate history/event authority cleanup auditのfocused product testを追加した。
- 本status report: package handoff evidence。

## Required invariant conclusion

- Chromiumで`/`→`/projects`正規化、Projects→PM→Analysis→Family/Stage→Results→PM、reload、Back/ForwardがPASSした。
- 各検証点でworkspaceに対応するtop-level rootのみがvisibleであり、stale global shellは同時表示されない。
- page error / console errorは0件だった。
- `popstate`およびProject / Analysis history同期authorityは各1箇所で、temporary routing fallbackは検出されなかった。
- legacy compatibility codeはP05のprotected behaviorであり、削除対象ではない。

## Focused verification

- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g04_p06_full_integration_cleanup.py`
  - exit code: 0
  - result: 3 passed
- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g04_p06_full_integration_cleanup.py tests/product/test_enh_e7_g04_p04_cross_surface_history_navigation.py tests/product/test_enh_e7_g03_p06_surface_architecture_integration.py tests/product/test_enh_e7_g03_p05_obsolete_global_shell_cleanup.py tests/product/test_enh_e7_g01_p07_project_integration_regression.py`
  - exit code: 0
  - result: 12 passed
- `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
  - exit code: 0
  - result: PASS (`create-to-overview`, `project-routes-reload-history`, `project-analysis-launcher`, `cross-surface-reload-history`, `full-g04-root-pm-analysis-results-pm`; console/page error 0)
  - evidence: `test-results/browser_e2e/enh-e7-project-integration-evidence.json`
- `python3 -m py_compile tests/browser_e2e/run_enh_e7_project_integration.py`, `git diff --check`
  - exit code: 0
  - result: PASS
- source/diff audit
  - result: test harness / focused coverageのみを変更。protected backend/API/persistence semantics、DOM ownership、operation semanticsへout-of-scope changeおよびdead compatibility code追加はない。

## Remaining / blocker

- None within P06 scope.
- P01〜P05の未コミット変更および既存の範囲外documentation / G03 artifactsは本packageでは変更・stageしていない。

## Scope guard確認

- new feature、visual polish、Acceptance Criteria、次package scope、backend/API/persistence semanticsは変更していない。
