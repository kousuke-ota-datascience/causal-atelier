# ENH-E5 G03 P01 — Causal Stage Mapping

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G03`
- Trial: `01`
- Package: `P01`
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 依存Package: `NONE`
- 発行時状態: **DRAFT_FOR_REVIEW**

## 0. Package Coding Agentの参照ポリシー — assigned Pxxのみ

本Pxxは、当該Package Coding Agentに対する**唯一のnormative implementation contract**である。

Package Agentは、仕様・scope・architecture decision・Acceptance Criteriaの意味を補完する目的で、06、07、P00、00〜30、ADR、他Pxx、過去Enhancement、issue、commit message、外部Webその他の資料を参照してはならない（MUST NOT）。

current repositoryのproduction code、existing tests、schema/type/interface、configuration、route/API implementation、repository structureは、**current implementation factを確認し実装方法を決めるため**に参照してよい。ただしrepositoryは仕様authorityではない。

> **Repositoryから実装方法を発見してよいが、仕様を発見してはならない。**

current codeが本Pxxと異なることを理由に、本Pxxの要求を追加・削除・緩和・変更してはならない。

本Pxxだけではnormativeなrequired behaviorを一意に決定できない場合、他資料へ探索範囲を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。

本Pxxを`FROZEN`にするPlanning担当は、Package Agentが外部の規範文書を読まずに実装・focused verificationを完結できることを事前確認する。

## 1. Package acceptance claim

current Causal capabilityを、既存analytical semanticsを保持したまま次の7 Navigation Stageへ配置できるsurface/mappingを成立させる。

1. `Setup`
2. `Discovery`
3. `Identification`
4. `Estimation`
5. `Effects`
6. `Diagnostics`
7. `Sensitivity`

Stage数を他Familyへ合わせない。Navigationはnon-sequentialである。

## 2. Stage responsibility

### Setup
current dataset/treatment/outcome/covariate/estimand等、current causal analysis configurationを保持する。current repositoryに存在しない新規設定を推測追加しない。

### Discovery
current graph discovery、candidate、direct-registration等の操作を保持する。Discovery完了を後続Stage navigationの必須条件にしない。

### Identification
identification strategy、adjustment、eligibility等、**「目的のcausal estimandを仮定とデータから識別できるか」**に関するcurrent contextを提示する。Estimation configurationと同一surfaceに潰さない。

### Estimation
current estimator selection、warning/revision rule、execution semanticsを保持する。DoWhy/EconML/new estimator libraryを追加しない。

### Effects
既に推定されたtreatment-effect Result/compare semanticsを閲覧する。estimator configuration surfaceと混同しない。

### Diagnostics
current eligibility/estimation diagnosticsを配置する。診断結果を見るためだけにNavigation Stage名と同名のExecution Stageを新設しない。

### Sensitivity
current Refutation / Sensitivity operation・methodを保持する。

## 3. In scope

- 7 Causal Stage surface/route binding
- current causal controls/operations/resultsのpresentation mapping
- existing graph/discovery, identification/eligibility, estimation, effect, diagnostic, refutation/sensitivity surface
- focused frontend/integration tests

## 4. Out of scope / 禁止

- DoWhy/EconML/new estimator library
- automatic causal identification proof system
- Analysis Management Stage
- strict wizard / stage completion progression
- current causal spec/execution/result semanticsの変更
- Navigation StageからExecution Stageへの1:1 mapping

## 5. Non-sequential navigation

operation prerequisiteはaction availabilityをblockしてよい。ただしsidebar/routeでStageへ移動すること自体をblockしてはならない。

例: estimator実行に必要なeligibility resultがない場合、Estimation画面へは移動できるが、実行actionは不足条件を明示してdisabled/blockしてよい。Navigation Stageをworkflow completion stateとして扱わない。

## 6. Focused verification

- 7 Stageすべてがcanonical routeから到達可能。
- current Discovery operationsが保持される。
- Identificationが独立surfaceとして存在する。
- Estimationのcurrent estimator/warning/revision ruleが保持される。
- Effectsがconfigurationではなくresult/compare contextとして表示される。
- Diagnosticsがcurrent diagnostic semanticsを保持する。
- Sensitivityがcurrent refutation/sensitivity operationsを保持する。
- prerequisite不足でもStage navigationは可能で、actionのみが適切にblockされる。
- execution plan/runnerへNavigation Stage identityを渡す新規dependencyがない。

## 7. Package Acceptance Checklist

- [ ] 7 Causal Stageが成立
- [ ] current causal operations/resultsを保持
- [ ] IdentificationとEstimationを分離
- [ ] EffectsとEstimation configを分離
- [ ] non-sequential navigation
- [ ] new estimator/libraryなし
- [ ] Navigation/Execution 1:1 mappingなし
- [ ] focused tests green

## 10. Checkpoint / 報告

Package完了時に以下を記録する。

- `git rev-parse HEAD` のPackage Checkpoint SHA
- `git status --short`
- 変更したproduction/test file一覧
- 実行したfocused verification commandと実測結果
- 本PxxのPackage Acceptance Checklist各項目のPASS/FAIL
- 未解決blocker。なければ`NONE`

Package完了はGate PASSを意味しない。Package AgentはGate PASSを判定しない。

## 11. 停止条件

以下のいずれかを検出した場合は、推測・外部資料探索・scope拡張を行わず停止する。

- 本Pxxだけではnormativeなrequired behaviorを一意に確定できない: `BLOCKED_CONTRACT_AMBIGUITY`
- prerequisite Packageの変更がcurrent branchへ統合されていない: `BLOCKED_PREREQUISITE`
- baseline / branch identityが想定と異なる: `BLOCKED_BASELINE_MISMATCH`
- DB migration、新dependency、新analytical engine等の未承認変更が必要: `BLOCKED_SCOPE_AMENDMENT_REQUIRED`
- protected execution / analysis semanticsとの衝突が発生: `BLOCKED_PROTECTED_CONTRACT_CONFLICT`

停止時は、観測したrepository factと不足しているnormative decisionを分離して報告する。
