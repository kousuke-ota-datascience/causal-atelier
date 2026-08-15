# ENH-E7 G03 Trial01 Test Item 007 — protected_semantic_smoke

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: `UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest -q` against all `test_enh_e7_g01_p01..p07` and `test_enh_e7_g02_p01..p06` product tests.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-12, AC-G03-13 | PASS |

## Direct assertion / predicate mapping

- G01 canonical Project route/lifecycle/surface contracts and G02 canonical Analysis route/family/stage contracts all execute successfully.

## Raw relevant evidence

- `35 passed in 3.03s`。

## Facts

- protected Project and Analysis product contracts pass without changes after candidate freeze.

## Interpretation

- no verified regression of G01/G02 canonical semantics; focused suites cover the protected frontend/domain contracts. This is not a claim that every backend test in the repository was run.

## Protected contract relation

- directly covers AC-G03-12/13 required protected regression.

## Reproduction procedure

1. repository root で上記 exact command と listed G01/G02 test files を実行する。
2. 35 passed を確認する。

## Browser evidence

- Supplemental browser journey is Item 008。This item is product regression; console/page error and network/service log are not applicable.
