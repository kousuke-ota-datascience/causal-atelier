# ENH-E6 G01 P01 — Navigation Transition Authority

- Status: `DRAFT`
- Role: assigned package implementation contract after freeze

## Outcome

Family/Stage Navigation Contextのapply lifecycleを単一authorityへ収束する。

## Required

- canonical context validation
- state commit
- history mode handling
- Family/Stage render
- operation availability refresh
- deterministic focus
- Family click / Stage click / canonical restore / popstate が同authorityを利用

## Excluded

- Causal stage presentation mappingの最終値
- browser E2E作成
- backend catalog変更

## Focused acceptance

- normal analysis entry後にcontext applyを再利用可能
- duplicate push/replaceなし
- popstateがnew history entryを作らない
- catalog invalidはexplicit error
