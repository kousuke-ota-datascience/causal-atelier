# ENH-E9 G05 P01 — Integrated Regression Acceptance Preparation

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G05`  
**Package:** `P01`  
**Depends on:** G01–G04 canonical `999_gate_decision = PASS`

## 1. Objective

G01–G04 PASS成果を統合したrepository stateで、critical Causal journeyのIndependent Verificationを安全に実行できるcandidateを準備する。

G05は新しいproduct capabilityや新しいscientific semanticsを追加するGateではない。Allowed workは、passed Gate semanticsを変えないintegration-only defect correction、fixture/orchestration/synchronization wiring、non-browser protected regression、candidate finalization evidenceに限る。

## 2. Entry criteria

Coding開始前に次をすべて満たすこと。

1. branch=`bugfix/ariadne_mvp_e9`
2. working tree clean
3. G01, G02, G03, G04それぞれについてcanonical `999_gate_decision`がexactly one存在し`PASS`
4. 本P01がexactly one解決されFROZEN
5. current Trialにformal 08 remediation contractなし

`READY_FOR_TEST`、package complete、Candidate AssemblyはPASSの代替authorityではない。

## 3. Critical journey

```text
Analysis Context
 -> Discovery execution
 -> Graph candidate review / comparison
 -> adopt / FIXED Graph
 -> Identification
 -> Estimation from selected Identification Result
 -> Effects
 -> Diagnostics
```

Journey全体で同一project / Analysis Context / Dataset Version / Graph / Result / Execution lineageを追跡可能にする。

## 4. Passed Gate semantics to preserve

### G01

- Saved Analysis View explicit read-only display
- Active Research Context meaning/help
- Analysis View lifecycle / Context ownership / restore / invalidation semantics

### G02

- Discovery title/help/overflow
- Select All/Clearはselection-onlyでadopt/fixを暗黙実行しない
- current comparison candidate identification
- algorithm/persisted parameter summary authority
- modal-local adoption feedback
- authoritative Graph Mermaid source export
- Graph Candidate identity / DRAFT-FIXED GraphVersion / FIXED immutability / designated Outcome lineage

### G03

- Population/Comparator help
- Treatment candidate authority = selected Dataset Version schema
- stale Treatmentをsilent保持しない
- FIXED Graph designated Outcome → Identification automatic/read-only inheritance
- selected Identification Result → Estimation lineage

### G04

- Effectsはpersisted `TREATMENT_EFFECT_RESULT` authority
- Diagnosticsはpersisted structured `DIAGNOSTICS_RESULT` authority
- applicability = `ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE`
- frontend scientific recomputation/string parsingなし
- numeric/scientific correctnessはG04 unit/integration authorityでありG05 Browser E2Eで再証明しない

## 5. Allowed implementation scope

Allowed:

- critical journey fixture/bootstrap dataの整合
- canonical Compose/browser harness wiring
- route/state synchronization修正
- fixed sleep依存をobservable state/element conditionへ置換
- passed Gate contractに完全に従うintegration wiring defect correction
- Browser failure evidence capture（screenshot/log/route/stage/checkpoint）準備
- test orchestration/configurationのintegration-only修正

Product codeを変更する場合、その変更がG01–G04の既存contractを満たすためのintegration defect correctionであることをdiff/reportで明示する。

## 6. Explicitly forbidden

- G01–G04 claim/ACのsilent変更
- passed GateのUI/semantic redesign
- new Navigation Stage / runtime Stage
- new Graph/Result/Execution lifecycle
- new estimator/diagnostic semantics
- frontend causal/scientific recomputation
- independent Outcome override
- fixtureを通すためのproduction validation弱体化
- test assertion削除/弱体化/skip/xfail
- Browser E2EをPackage focused verificationとして実行

Passed Gate semantic changeが必要ならP01で直さず、owner Gateのamendment routeへ停止する。

## 7. Browser fixture / synchronization requirements

Browser E2E自体はP01では実行しないが、Independent Verificationで使うfixture/harnessをreadyにする。

Requirements:

- Analysis ContextからDiagnosticsまで同一project lineageで到達可能
- FIXED Graph designated OutcomeをIdentificationで利用可能
- selected Identification ResultからEstimationへ到達可能
- persisted Treatment Effect / Diagnostics Resultが後段Stageで参照可能
- synchronizationはfixed sleepだけをauthorityにしない
- observable route/element/state/API readinessを使用
- failure evidenceとしてcurrent route、visible Stage、last successful checkpoint、screenshot/logを取得可能

## 8. Non-browser protected regression — mandatory

P01ではBrowserを起動せず、最低限:

1. relevant static/syntax checks
2. G01 protected context/view tests
3. G02 Graph identity/lifecycle/comparison/adoption/fix regressions
4. G03 Graph→Identification→Estimation lineage regressions
5. G04 Treatment Effect / structured Diagnostics contract regressions
6. route/catalog / Navigation Stage != Execution state regressions
7. fixture/bootstrap consistency checks
8. candidate-affecting working tree clean audit

を実施する。

G04 numeric ESS/weights/balance expected valuesをG05で別実装して再計算する必要はない。G04 PASS authorityを信頼し、cross-layer connectivityだけを準備する。

## 9. Candidate finalization boundary

P01 complete条件:

- §5の必要なintegration preparation完了
- §8 non-browser protected regression PASS
- browser fixture/harness prerequisites ready
- unresolved blockerなし
- scope外semantic changeなし
- package checkpoint/report produced

P01 complete後Candidate Assemblyでexact Fixed Trial Candidateを確定する。Coding AgentはG05 PASSを宣言しない。

## 10. Stop rule

以下は推測/局所修正せずBLOCKED:

- G01–G04のどれかがcanonical 999 PASSでない
- critical journey成立にpassed Gate semantic変更が必要
- fixtureを成立させるためproduction scientific semantics変更が必要
- Browser harness requirementを満たすためnew product capabilityが必要
- lineage source-of-truthが一意に追えない

owner Gate semantic defectならそのGateのamendment pathへ戻す。
