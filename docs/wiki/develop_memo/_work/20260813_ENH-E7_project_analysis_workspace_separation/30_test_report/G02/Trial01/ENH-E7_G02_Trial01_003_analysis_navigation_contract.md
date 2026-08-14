# ENH-E7 G02 Trial01 Test Item 003 — analysis_navigation_contract

- Result: PASS
- Fixed Trial Candidate full SHA: `ba9fd568e20458468f18edf312100499bb03290d`
- Tested Repository State full SHA: `9a0f42f8d8798c91245f3138d899ca77eb414cfb`
- Exact command / method: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q tests/product/test_enh_e7_g02_p06_legacy_cutover_integration.py tests/product/test_enh_e6_g01_p01_navigation_transition.py tests/product/test_enh_e6_g01_p02_stage_presentation.py`
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G02-12, AC-G02-13, AC-G02-14, AC-G02-17, AC-G02-18, AC-G02-19 | PASS |

## Raw relevant evidence

- `9 passed in 1.36s`。
- legacy `/projects/p1/explore` は canonical `/projects/p1/analysis/exploratory/profile` に serialize される。
- resource route は `/projects/p1/analysis/causal/discovery/resource/result/r1` として保持される。
- `popstate` restore、catalog default stage、ENH-E6 navigation transition / stage presentation contract が成功した。

## Facts

- parallel analytical shortcut は除去され、Project surface と legacy normalization / resource route / history authority は維持される。

## Interpretation

- canonical URL、catalog-authoritative default、legacy/resource/history、および ENH-E6 protected navigation に回帰はない。

## Protected contract / Transition Debt relation

- ENH-E6 protected tests を同一実行束に含めて PASS した。legacy URL は削除でなく canonical route へ normalize される。

## Reproduction procedure

1. repository root で上記 exact command を実行する。
2. 9 tests が PASS することを確認する。
