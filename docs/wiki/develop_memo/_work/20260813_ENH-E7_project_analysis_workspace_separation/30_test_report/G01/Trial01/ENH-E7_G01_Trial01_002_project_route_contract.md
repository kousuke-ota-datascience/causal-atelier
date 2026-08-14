# ENH-E7 G01 Trial01 Test Item 002 — project_route_contract

- Result: PASS
- Fixed Trial Candidate full SHA: `7936151d98de7fe467c176039add47da6af987c4`
- Tested Repository State full SHA: `fe3b59cca9b5ed5b250beb1b79dd0d451a161db7`
- Exact command / method: `uv run pytest -q tests/product/test_enh_e7_g01_p01_project_navigation_authority.py`
- Exit code: 0; `3 passed in 2.01s`

## AC mapping

| AC | Result |
| --- | --- |
| AC-G01-01 | PASS |
| AC-G01-02 | PASS |
| AC-G01-03 | PASS |
| AC-G01-04 | PASS |
| AC-G01-05 | PASS |
| AC-G01-11 | PASS |

## Raw relevant evidence

- `test_enh_e7_g01_p01_project_navigation_authority.py`はcanonical Project routeのparse / serialize、`/projects/<id>`から`/overview`へのnormalization、history integrationを対象にする。
- test commandは3件すべてPASSした。

## Facts

- ルート契約テストはProject route authorityを対象とし、Analysis route ownershipを対象外として分離している。

## Interpretation

- Test Item 002がcoverするcanonical list/new route、作成後Overview遷移、overview normalization、local navigation URL、historyのfrontend contractに違反は検出されなかった。

## Protected contract / Transition Debt relation

- Project route authorityは既存Analysis route authorityを置換しない。Transition Debtの導入は検出されなかった。

## Reproduction procedure

1. repository rootで指定pytest commandを実行する。
2. exit code 0および全test PASSを確認する。
