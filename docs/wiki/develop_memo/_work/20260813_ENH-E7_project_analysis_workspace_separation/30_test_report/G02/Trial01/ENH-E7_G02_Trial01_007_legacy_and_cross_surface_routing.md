# ENH-E7 G02 Trial01 Test Item 007 — legacy_and_cross_surface_routing

- Result: PASS
- Fixed Trial Candidate full SHA: `ba9fd568e20458468f18edf312100499bb03290d`
- Tested Repository State full SHA: `9a0f42f8d8798c91245f3138d899ca77eb414cfb`
- Exact command / method: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g02_p02_project_analysis_routing.py tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py tests/product/test_enh_e6_g01_p01_navigation_transition.py tests/product/test_enh_e6_g01_p02_stage_presentation.py`
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G02-14, AC-G02-15, AC-G02-16, AC-G02-17, AC-G02-18 | PASS |

## Raw relevant evidence

- `12 passed in 1.78s`。
- Project launcher は catalog family の default stage へ launch する。
- Analysis routing actions は Project Management / Results Lineage に transitionし、新規 history synchronization や backend execution / persistenceを導入しない。
- legacy normalization、resource route、reload / Back / Forward browser runner contract、ENH-E6 navigation/stage contract を確認した。

## Facts

- Project → Analysis、Analysis → Project Management / Results、legacy analytical URL → canonical Analysis route、resource route と browser history の各経路が実装上の contract で維持される。

## Interpretation

- required cross-surface / legacy / history routing は PASS。

## Protected contract / Transition Debt relation

- ENH-E6 protected navigation tests を含め PASS。旧 analytical shortcut は削除されるが legacy URL compatibility は canonical normalization として残る。

## Reproduction procedure

1. repository root で上記 exact command を実行する。
2. 12 tests が PASS することを確認する。
