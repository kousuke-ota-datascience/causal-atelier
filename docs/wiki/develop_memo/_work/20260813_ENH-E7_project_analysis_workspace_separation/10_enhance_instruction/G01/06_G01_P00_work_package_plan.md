# ENH-E7 G01 P00 Work Package Plan

**文書種別:** Planning / Operator Artifact  
**Status:** DRAFT_NOT_FROZEN  
**P00はimplementation Work Packageではない。**

## 1. Work Package Modeが必要な理由

複数のUI ownership / routing boundaryにまたがるためbounded execution、dependency control、failure localizationが必要である。
ただしGate semantic claimは不可分である。

## 2. Effective Gate semantic boundary

- Gate claim: Projectの作成・選択・管理が独立したURL-authoritative Project Management surfaceとして成立し、downstreamがProject route、section ownership、analysis input resource ownershipへ安全に依存できる。
- Downstream result: G02はselected Project routing、Data-owned Analysis View management、Results/Lineage ownership、安定したProject Management return targetへ依存できる。
- 共通constraint:
  - existing domain semanticsを保護する。
  - package completionをGate PASSと扱わない。
  - Pxxをself-containedにする。
  - Coding AgentはP00 / 06 / 07 / other Pxxを仕様補完目的で読まない。

## 3. Package map

| Package | Purpose | Depends on | Entry criterion | Exit criterion | Focused verification |
|---|---|---|---|---|---|
| P01 | Project routeのparse / serialize / normalization / browser history behaviorを作成・集約する。 | NONE | Gate entry criteria + preflight PASS | Focused Project route contract testがPASSする。 | assigned Pxxのfocused test |
| P02 | Project ListとNew Projectをroute-backedな別surfaceとして成立させる。 | P01 | Gate entry criteria + preflight PASS + dependency complete: P01 | Project list/create focused testがPASSする。 | assigned Pxxのfocused test |
| P03 | selected Projectのmetadata / lifecycle responsibilityをOverviewへ移設する。 | P01,P02 | Gate entry criteria + preflight PASS + dependency complete: P01,P02 | Overview ownership/lifecycle regressionがPASSする。 | assigned Pxxのfocused test |
| P04 | existing Research Context lifecycle/history/Related AnalysisをProject Context surfaceへ配置する。 | P01,P03 | Gate entry criteria + preflight PASS + dependency complete: P01,P03 | Research Context regressionがPASSする。 | assigned Pxxのfocused test |
| P05 | DataをDataset / Version / Schema・Preview / Analysis View lifecycle managementのauthorityとする。 | P01,P03 | Gate entry criteria + preflight PASS + dependency complete: P01,P03 | Dataset / Analysis View regressionがPASSする。 | assigned Pxxのfocused test |
| P06 | Results / LineageをProject-local persisted cross-analysis aggregation surfaceとして成立させる。 | P01,P03 | Gate entry criteria + preflight PASS + dependency complete: P01,P03 | Results / Lineage regressionがPASSする。 | assigned Pxxのfocused test |
| P07 | G01 Project surfaceを統合し、Candidate Assembly前にbrowser/history/domain regressionを確認する。 | P02,P03,P04,P05,P06 | Gate entry criteria + preflight PASS + dependency complete: P02,P03,P04,P05,P06 | G01 gate-wide self-checkとcritical browser journeyがPASSする。 | assigned Pxxのfocused test |

## 4. Execution rule

dependencyは上表をauthorityとする。
すべてのdependencyが満たされ、source overlap riskが許容される場合のみparallel executionを検討できる。

## 5. Package completion semantics

`PACKAGE_COMPLETE`はassigned scope実装、focused verification PASS、checkpoint full SHA固定、report作成を意味する。

`READY_FOR_TEST`、Gate PASS、verified-state promotion、downstream unlockを意味しない。

## 6. Candidate Assembly

Required package set: P01, P02, P03, P04, P05, P06, P07。

package-chain audit、integration self-check、protected regression、candidate-affecting working-tree audit、
Fixed Trial Candidate freeze、Completion Report作成を行う。

## 7. Remediation

formal FAIL後はdistinct remediation identityを使用し、元Pxxを同一Trialのように再利用しない。
