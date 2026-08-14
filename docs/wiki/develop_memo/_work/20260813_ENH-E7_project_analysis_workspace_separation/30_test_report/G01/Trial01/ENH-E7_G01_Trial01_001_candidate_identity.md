# ENH-E7 G01 Trial01 Test Item 001 — candidate_identity

- Result: PASS
- Fixed Trial Candidate full SHA: `7936151d98de7fe467c176039add47da6af987c4`
- Tested Repository State full SHA: `fe3b59cca9b5ed5b250beb1b79dd0d451a161db7`
- Exact command / method: `git rev-parse HEAD`; `git merge-base --is-ancestor 7936151d98de7fe467c176039add47da6af987c4 HEAD`; `git diff --name-status 7936151d98de7fe467c176039add47da6af987c4..HEAD`; `git status --short`
- Exit code: 0

## AC mapping

| AC | Relation |
| --- | --- |
| META | Fixed Trial Candidateとtested checkoutのidentity audit |

## Raw relevant evidence

- Fixed CandidateはImplementation Completion Reportから取得した`7936151d98de7fe467c176039add47da6af987c4`である。
- tested checkoutは`fe3b59cca9b5ed5b250beb1b79dd0d451a161db7`である。
- `merge-base --is-ancestor`は成功した。
- Fixed Candidate後の差分は`20_implementation_reports/G01/Trial01/`配下のcompletion/detail report 2ファイルだけである。
- `git status --short`は出力なしである。

## Facts

- tested checkoutはFixed Candidateのevidence-only descendantであり、production、test、migration、dependency codeの差分を含まない。

## Interpretation

- Fixed Trial CandidateをProduct candidate identityとして一意に扱える。tested checkoutのreport-only差分はcandidate identityを変更しない。

## Protected contract / Transition Debt relation

- 本Test Itemはprotected contractの振る舞いを判定しない。Transition Debtの追加はdiff上確認されない。

## Reproduction procedure

1. Completion ReportのFixed Trial Candidate SHAを取得する。
2. `git rev-parse HEAD`でtested checkoutを取得する。
3. `git merge-base --is-ancestor <fixed> HEAD`と`git diff --name-status <fixed>..HEAD`を実行する。
4. candidate-affecting差分またはdirty treeがないことを確認する。
