# ENH-E7 G04 P01 Package Execution Status

- Enhancement: ENH-E7
- Gate: G04
- Trial: 01
- Package: P01
- State: PACKAGE_COMPLETE
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: cc4fb35b66545af50ed96fd2f80aff7f9a619a5e

## 実施したscope

- `/` の初期ロードをhistory replaceで `/projects` に正規化した。
- root正規化後、Projects top-level surfaceのみをactivateするようにした。
- `/projects/<id>` short routeのoverview正規化、`/projects` / `/projects/new`、create成功時overview遷移をfocused coverageで確認した。

## Changed files / responsibility

- `frontend/app.js`: route restorationのroot entryをroute-authoritativeにした。
- `tests/product/test_enh_e7_g04_p01_root_project_route_reintegration.py`: root replacement、short route canonicalization、route別top-level surface、create destinationを検査するfocused product testを追加した。
- 本status report: package handoff evidence。

## Required invariant conclusion

- `/` は `history.replaceState` 経由で `/projects` へ移行するため、rootをBack先として残すduplicate entryを作らない。
- `/` のrestore pathはlegacy Project/Data workspaceをactivateせず、Projects surfaceをactivateする。
- `/projects/<id>` は既存の `ProjectNavigation.parse` / `synchronizeProjectHistory(..., 'REPLACE')` により `/projects/<id>/overview` へcanonicalizeされる。
- create成功時は既存のreplace遷移によりnew Project overviewを表示する。

## Focused verification

- `uv run pytest -q tests/product/test_enh_e7_g04_p01_root_project_route_reintegration.py tests/product/test_enh_e7_g01_p02_projects_new_project_surface.py tests/product/test_enh_e7_g03_p01_top_level_surface_activation_authority.py`
  - exit code: 0
  - result: 9 passed
- `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g04_p01_root_project_route_reintegration.py`
  - exit code: 0
  - result: 3 passed
- `node --check frontend/app.js`
  - exit code: 0
  - result: PASS
- `git diff --check`
  - exit code: 0
  - result: PASS
- source/diff audit
  - result: DOM ownership is still delegated to `TopLevelSurfaceActivation`; this package changes neither event binding nor backend/API/persistence semantics and introduces no dead route handler.

## Remaining / blocker

- None within P01 scope.
- The working tree contained pre-existing, out-of-scope documentation changes and G03 artifacts. They were not modified or staged by this package.

## Scope guard確認

- P02 selected Project local navigation, P03 Analysis state, P04 cross-surface history, and all backend/API/persistence behavior were not changed.
