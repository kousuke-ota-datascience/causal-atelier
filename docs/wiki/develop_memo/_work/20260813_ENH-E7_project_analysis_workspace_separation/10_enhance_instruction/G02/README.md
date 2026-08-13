# ENH-E7 G02 — Analysis Workspace Contract

**Status:** DRAFT_NOT_FROZEN  
**Execution Mode:** WORK_PACKAGE

## Gate claim

Analysis WorkspaceがProject Managementとは別analysis surfaceとして成立し、Analysis Context、Family/Stage navigation、既存Causal/Exploratory/Predictive surfaceのStage Contents配置、cross-surface navigation、legacy compatibility、browser history semanticsを一体として利用できる。

## Work Package一覧

- P01 — Analysis Shell / Analysis Context — dependency: G01 PASS
- P02 — Project <-> Analysis Routing — dependency: P01
- P03 — Causal Stage Surface Migration — dependency: P01,P02
- P04 — Exploratory Stage Surface Migration — dependency: P01,P02
- P05 — Predictive Stage Surface Migration — dependency: P01,P02
- P06 — Legacy Cutover / Integration / Regression — dependency: P03,P04,P05

## Active contract rule

- Architecture Review完了後、Human/operatorが06/07をFROZENに変更した時点でGate contractがexecution authorityになる。
- PxxはdependencyとpreflightがPASSした場合だけexecution eligibleになる。
- 08はformal FAILまでinactive。
- 09はsemantic Gate contract amendmentが明示的に承認された場合だけactiveになる。
