# G02 P00 — Work Package Plan

- Status: `FROZEN`

| Package | Scope | Depends on | Exit evidence |
|---|---|---|---|
| P01 | common Analysis Stage presentation framework / current-stage identity / sidebar grouping / vertical layout primitive | G01 PASS | package checkpoint |
| P02 | Causal Stage surface separation + 日本語guidance | P01 | package checkpoint |
| P03 | Predictive Stage separation + Dataset-schema-backed feature selector + Train/Predict read-only feature context + draft/spec compatibility | P02 | package checkpoint |

## Execution rule

shared frontend fileへ触れる可能性が高いため、P01 -> P02 -> P03 の順に実行する。

同一Trial内のpackage correction/restartではTrial番号を増やさない。

P03はCausal Discovery column-selector interactionをreuse/generalizeしてよいが、P02/Causal behaviorを維持し、backend analytical capability変更へscope拡大してはならない。

## Candidate Assembly exit

- required packageがすべてcompletion criteriaを満たす
- integrated focused/protected testがgreen
- Predictive selector test + Causal Discovery protected regressionがgreen
- unresolved package blockerなし
- 1つのcommit SHAをTrial candidateとして固定
- Implementation Completion Reportでcandidate identityとIndependent Verificationへのreadinessを記録
