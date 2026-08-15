# ENH-E7 G04 — Navigation / State Reintegration & Full Regression Contract

Status: FROZEN  
**Execution Mode:** WORK_PACKAGE

Freeze basis: `40_operator_workflows/architecture_review/04_G04_source_confirmation.md` confirmed AR-E7-09/10 with zero unresolved semantic blockers. `06` and `07` are the execution authority; this README is an index, not a source of acceptance-criteria supplementation.

## Gate claim

G03で成立したtop-level surface architectureを維持したまま、
canonical Project routing、Analysis context、Family/Stage state、cross-surface navigation、
legacy normalization、resource/operation semantics、browser historyを再結合し、
ENH-E7をcorrected Product-complete状態にする。

## Work Package一覧

- P01 — Root / Project Route Reintegration — dependency: G03 PASS
- P02 — Project Management Navigation / State — dependency: P01
- P03 — Analysis Context / Family / Stage State — dependency: P02
- P04 — Cross-surface Routing / Browser History — dependency: P02,P03
- P05 — Legacy / Operation / Resource Regression — dependency: P04
- P06 — Full Integration / Cleanup — dependency: P05

## Active contract rule

- G03 surface architectureはblocking protected contract。
- G04でold global shellを復活させてはならない。
- G04 final PASSをpost-escape ENH-E7 Product completionとする。
- 08はformal FAILまでinactive。
- 09はsemantic Gate contract amendment時のみactive。
- G04は既存 API / persistence / domain semanticsを変更せず、frontend route/state/presentation bindingを再結合する。
