# ENH-E5 G04 P02 — Visualization / Findings Integration

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G04`
- Trial: `01`
- Package: `P02`
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 依存Package: `P01`
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

Visualizationを独立analytical Stageにせず、各Exploratory Stageの表現手段として統合し、Findingsを既存Result/Annotation/Lineageのprojectionとして成立させる。

## 2. Visualization placement rule

- `Profile` / `Data Quality` / `Distribution` / `Relationships` / `Comparison`の各contextで必要なchart/table/controlを、そのanalytical context内に配置する。
- `Visualization`というNavigation Stageを新設しない。
- chart type選択やvisual encodingはpresentation concernであり、analysis Family/Stage taxonomyと同列に扱わない。
- existing chart/render operationがbackend executionを伴う場合でも、そのruntime operationをNavigation Stageと同一視しない。
- current result/operationがsupportしないvisualizationを、見た目だけのために新analysis methodとして追加しない。

## 3. Findings responsibility

`Findings`はEDAで得た既存の保存済みResult/Annotation/Lineage等を閲覧・再利用するnavigation contextである。

- new persistent `Finding` / `Evidence` aggregateを作らない。
- existing Result type/semantic ownershipを平坦化しない。
- exploratory findingをcausal effectやconfirmatory conclusionへ自動変換しない。
- Findingsから元Dataset/View/Spec/Execution/Result等の既存lineageへ辿れる性質を壊さない。

## 4. Non-causal interpretation

current UI/resultがexploratory associationに対してnon-causal interpretation warningを持つ箇所は維持する。Relationships/Comparison/Findingsへの再配置を理由にwarningを削除・弱体化しない。

## 5. In scope

- existing chart/table controlsのStage内再配置
- chart rendering stateのfrontend integration
- Findings projection
- existing Result/Annotation/Lineageへのnavigation/linkage
- focused UI/result tests

## 6. Out of scope / 禁止

- Visualization Stage
- chart目的のnew statistical engine
- new persistent Finding/Evidence model
- causal claimへの意味変更
- Result schemaの共通score化/平坦化

## 7. Focused verification

- VisualizationというStage/tab/sidebar itemが存在しない。
- Distribution/Relationships/Comparison等でexisting chart/controlを利用できる。
- chart/control切替でunderlying analytical semanticsが変化しない。
- Findingsがnew DB entityなしでexisting saved result系resourceを表示する。
- existing lineage accessが維持される。
- non-causal warningが該当surfaceで保持される。

## 8. Package Acceptance Checklist

- [ ] Visualizationは表現手段としてStage内部にある
- [ ] standalone Visualization Stageなし
- [ ] Findingsはexisting resourcesのprojection
- [ ] new Finding/Evidence persistenceなし
- [ ] non-causal semantics保持
- [ ] lineage保持
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
