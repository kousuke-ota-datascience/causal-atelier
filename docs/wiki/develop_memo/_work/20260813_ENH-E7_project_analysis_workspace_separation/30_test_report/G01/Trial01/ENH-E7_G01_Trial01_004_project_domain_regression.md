# ENH-E7 G01 Trial01 Test Item 004 — project_domain_regression

- Result: PASS
- Fixed Trial Candidate full SHA: `7936151d98de7fe467c176039add47da6af987c4`
- Tested Repository State full SHA: `fe3b59cca9b5ed5b250beb1b79dd0d451a161db7`
- Exact command / method: `uv run pytest -q tests/product/test_research_context_e3.py tests/product/test_analysis_view_e3.py tests/product/test_results_lineage_export_e3.py tests/product/test_cross_analysis_lineage_e3.py`
- Exit code: 0; `12 passed in 18.24s`

## AC mapping

| AC | Result |
| --- | --- |
| AC-G01-03 | PASS |
| AC-G01-07 | PASS |
| AC-G01-08 | PASS |
| AC-G01-10 | PASS |
| AC-G01-12 | PASS |

## Raw relevant evidence

- Research Context API lifecycle / history / project isolation testsがPASSした。
- Analysis View compilationとAPI lifecycle（validate / fix / fixed immutability）testsがPASSした。
- Project-local Results summary / comparison / export / artifact / annotation testsがPASSした。
- Cross-analysis lineage aggregation testsがPASSした。

## Facts

- 4 test file、12 testがAPI integration / unit domain layerでPASSした。
- 各testはProjectを作成してProject-scoped resourceを操作し、Research Context、Dataset / Analysis View、Results / Lineageの既存domain semanticsを検査する。

## Interpretation

- Project作成を起点とする既存domain resource lifecycleとResults / Lineage cross-analysis機能に回帰は検出されなかった。UI責務移設によるbackend domain semanticsの変更を示す証拠はない。

## Protected contract / Transition Debt relation

- 本Test ItemはAnalysis execution domainを置換しない既存resource semanticsを確認する。Transition Debtの追加は検出されなかった。

## Reproduction procedure

1. repository rootで記載の4 test fileをpytestに渡す。
2. exit code 0および12件のPASSを確認する。
