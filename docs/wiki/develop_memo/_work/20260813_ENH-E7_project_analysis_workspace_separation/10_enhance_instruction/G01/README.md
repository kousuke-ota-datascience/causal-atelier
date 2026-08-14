# ENH-E7 G01 — Project Management Surface Contract

**Status:** GATE_CONTRACT_FROZEN / PACKAGE_ELIGIBILITY_DERIVED_BY_PREFLIGHT  
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

- Architecture ReviewはHuman承認済みであり、G01 Gate contractに明示的blocking stateはない。
- Pxxの実行可否は、declared status literalではなくpreflightが次から導出する。
  - assigned Pxxが一意に解決できる
  - runtime identityが有効
  - current branchが対象branch
  - Gate contractに明示的blocking stateがない
  - `Depends on` の必須dependency completion evidenceが存在する
- `READY_TO_EXECUTE` 等のpackage status literalをworkflow cursorとして使用しない。
- package完了後に次Pxx文書を手動編集してunlockしない。
- 08はformal FAILまでinactive。
- 09はsemantic Gate contract amendmentが明示的に承認された場合だけactiveになる。
