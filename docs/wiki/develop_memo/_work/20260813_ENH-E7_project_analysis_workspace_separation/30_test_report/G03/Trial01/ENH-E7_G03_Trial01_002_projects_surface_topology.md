# ENH-E7 G03 Trial01 Test Item 002 — projects_surface_topology

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g03_p01_top_level_surface_activation_authority.py tests/product/test_enh_e7_g03_p02_projects_surface_separation.py`; Chromium direct DOM/visibility probe for `/projects` and `/projects/new`.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-01 | PASS |
| AC-G03-08, AC-G03-09, AC-G03-10, AC-G03-11 | PASS (negative topology portion) |

## Direct assertion / predicate mapping

- `/projects` と `/projects/new` の visible top-level root はともに唯一の `projects`。
- 両 route で PM local navigation、Analysis Context、family navigation、stage navigation は runtime 非表示。

## Raw relevant evidence

- Focused structural suite は 15 passed の一部として PASS。
- Chromium: `projects`/`project_new` は `activeRoots:["projects"]`、`projectNavVisible:false`、`contextVisible:false`、`familyVisible:false`、`stageVisible:false`。

## Facts

- Projects routes は Project/Analysis chrome を表示しない。

## Interpretation

- Projects Surface の exclusive ownership が direct runtime predicate で成立する。

## Protected contract relation

- Projects/new route は canonical Project entry surface として維持される。

## Reproduction procedure

1. 上記 pytest command を実行する。
2. Compose browser-e2e で `/projects`、`/projects/new` の root/visibility predicate を evaluate する。

## Browser evidence

- Success screenshot: `test-results/browser_e2e/enh-e7-g03-p06-projects.png`。
- direct probe は `getClientRects().length > 0` で ancestor hidden を含む可視性を判定した。console/page error: none。network/service log: API READY。
