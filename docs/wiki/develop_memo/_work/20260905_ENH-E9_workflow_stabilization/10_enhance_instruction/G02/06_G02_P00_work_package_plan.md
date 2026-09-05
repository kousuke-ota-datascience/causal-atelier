# G02 P00 Work Package Plan

- Status: `DRAFT_NOT_FROZEN`
- Gate: `G02`

## Draft package decomposition

| Package | Scope | Dependency |
|---|---|---|
| P01 | Discovery operation copy/help/overflow residual | G01 PASS |
| P02 | Graph candidate selection/comparison clarity residual | P01 |
| P03 | Graph adoption feedback/export residual | P02 |

Packageはbaselineで`RESIDUAL`確認された項目だけを含む。不要packageはfreeze前に削除/再構成する。

## Candidate assembly rule

Pxx completionはGate PASSではない。all required packages `PACKAGE_COMPLETE`後にCandidate Assemblyを行い、Gate-wide regressionとFixed Trial Candidate SHAを確定する。
