# G04 P00 Work Package Plan

- Status: `DRAFT_NOT_FROZEN`

## Draft package decomposition

| Package | Scope | Dependency |
|---|---|---|
| P01 | diagnostics contract/source reconciliation + estimator applicability implementation | G03 PASS |
| P02 | ESS / weight diagnostics structured persistence | P01 |
| P03 | balance before/after structured persistence + integration | P02 |
| P04 | frontend structured consumption / regression wiring if required | P03 |

Final package DAGはbaseline source reviewとexact contract freeze後に確定する。

## Guard

PxxはGate semantic claimを変更できない。scientific ambiguityが判明した場合は推測実装せずGate contract authoringへ戻す。
