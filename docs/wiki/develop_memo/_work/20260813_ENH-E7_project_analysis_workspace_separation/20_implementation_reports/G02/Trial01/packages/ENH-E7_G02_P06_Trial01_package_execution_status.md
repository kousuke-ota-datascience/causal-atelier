# ENH-E7 G02 P06 Package Execution Status

- Enhancement: ENH-E7
- Gate: G02
- Trial: 01
- Package: P06
- State: PACKAGE_COMPLETE
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: b50d6ff0d04a1ce36292cf0f791981e3ec4ffbcc

## 実施したscope

old analytical sidebar shortcutを削除し、Project Overview の catalog-driven Analysis launcher を唯一の UI entryとした。legacy URL normalization、canonical Analysis route、resource route、browser history、Project / Results transition は維持した。

## Changed files / responsibility

- `frontend/index.html`: duplicated analytical sidebar shortcutを削除した。
- `frontend/app.js`: shortcut-only transitionを削除し、canonical Analysis transitionが shell を保持する `retainAnalysisShell` を追加した。
- `tests/browser_e2e/run_enh_e7_project_integration.py`: browser journey を Project launcher 経由へ更新した。
- `tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py`: P06 focused coverageを追加した。
- `tests/product/test_enh_e6_g01_p01_navigation_transition.py`、`tests/product/test_enh_e6_g01_p02_stage_presentation.py`、`tests/product/test_enh_e7_g01_p07_project_integration_regression.py`: shortcut削除後の protected navigation contractへ更新した。
- backend/API/persistence/config/migration は変更していない。

## Focused verification

- exact command / method: `python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py --repo-root . --gate G02 --package P06 --trial 01`
- exit code / result: `0`; `Agent Execution Readiness: PASS`。
- exact command / method: `uv run pytest -q tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py`
- exit code / result: `0`; `3 passed in 2.42s`。
- exact command / method: `uv run pytest -q tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py tests/product/test_enh_e6_g01_p01_navigation_transition.py tests/product/test_enh_e6_g01_p02_stage_presentation.py tests/product/test_enh_e5_g01_navigation_state.py tests/product/test_enh_e7_g01_p01_project_navigation_authority.py tests/product/test_enh_e7_g01_p07_project_integration_regression.py tests/product/test_enh_e7_g02_p01_analysis_shell_context.py tests/product/test_enh_e7_g02_p02_project_analysis_routing.py`
- exit code / result: `0`; `22 passed in 4.08s`。
- exact command / method: `node --check frontend/app.js` および `git diff --check`
- exit code / result: `0`; JavaScript syntax と diff whitespace error は検出されなかった。
- exact command / method: `docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e1a --profile e2e run --build --rm --entrypoint python browser-e2e tests/browser_e2e/run_enh_e7_project_integration.py`
- exit code / result: 実行セッションの終了出力は取得できなかった。一方、`test-results/browser_e2e/enh-e7-project-integration-evidence.json`（2026-08-14T10:45:17Z）は今回の commandを記録し、`create-to-overview`、`project-analysis-launcher`、`project-routes-reload-history` の全 scenario と全体 status が `PASS`。

## Remaining / blocker

なし。ディスク容量拡張後に更新済み frontend/browser image で Chromium journey を再実行し、`project-analysis-launcher` を含む current PASS evidence を取得した。

## Scope guard確認

- G02/P06 の assigned primary execution contract のみを仕様として使用した。
- Gate 06 / 07、P00、他 Pxx、background、既存 implementation/test reports、previous workflow artifacts、ADR、issue、external Web は読んでいない。
- compatibility URLを削除せず、他 package、Gate級 acceptance、未承認 backend/API/persistence semantic change を行っていない。

## Facts

- legacy URL normalization は `AnalysisNavigation.legacyContext` と `source:'legacy-route-normalization'` に残っている。
- resource route は `AnalysisNavigation.contextForResource` によりfamily整合性を確認して復元する。
- old sidebar shortcutを除去した後、canonical Analysis transitionは `retainAnalysisShell:true` で shellを維持する。
- source-level integration testは Project → Analysis launcher、Analysis → Project / Results、legacy URL、resource route、history authorityを確認した。

## Interpretation

source-level implementation、focused/nearby verification、および current Chromium browser journeyにunresolved failureはない。P06のpackage completion criteriaを満たすため、状態は `PACKAGE_COMPLETE` とする。Gate PASS/FAILは宣言しない。
