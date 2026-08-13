# ENH-E7 G01 — Project Management Surface Contract

**Status:** DRAFT_NOT_FROZEN  
**Execution Mode:** WORK_PACKAGE

## Gate claim

Projectの作成・選択・管理が独立したURL-authoritative Project Management surfaceとして成立し、downstreamがProject route、section ownership、analysis input resource ownershipへ安全に依存できる。

## Work Package一覧

- P01 — Project Navigation Authority — dependency: NONE
- P02 — Projects / New Project Surface — dependency: P01
- P03 — Overview / Project Lifecycle — dependency: P01,P02
- P04 — Research Context Surface — dependency: P01,P03
- P05 — Data / Analysis View Surface — dependency: P01,P03
- P06 — Results / Lineage Surface — dependency: P01,P03
- P07 — Project Integration / Regression — dependency: P02,P03,P04,P05,P06

## Active contract rule

- Architecture Review完了後、Human/operatorが06/07をFROZENに変更した時点でGate contractがexecution authorityになる。
- PxxはdependencyとpreflightがPASSした場合だけexecution eligibleになる。
- 08はformal FAILまでinactive。
- 09はsemantic Gate contract amendmentが明示的に承認された場合だけactiveになる。
