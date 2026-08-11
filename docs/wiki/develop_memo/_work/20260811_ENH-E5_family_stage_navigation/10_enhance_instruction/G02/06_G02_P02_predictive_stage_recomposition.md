# ENH-E5 G02 P02 — Predictive Stage Recomposition

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G02`
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

既存Predictive capabilityを、分析意味論を変更せず次の6 Navigation Stageへ再配置する。

1. `Setup`
2. `Train`
3. `Predict`
4. `Metrics`
5. `Explainability`
6. `Model Management`

Navigation Stageはpresentation/navigation contextであり、Execution Stageへ1:1 mappingしない。

## 2. Stage responsibility

### 2.1 Setup

- current Predictive configuration/input controlを**全て**保持する。
- 目的変数、feature/input、split、training/evaluation/explain設定その他current UIに存在する設定を、意味/default/validationを変えず配置する。
- P01で保護されたgenerated spec semanticsを維持する。

### 2.2 Train

- current model-training actionを提供する。
- actionは既存のsplit/prepare/train/evaluate/(explain) workflow semanticsをそのまま起動する。
- `NavigationStage.TRAIN`等をruntime `StageType`へ変換してexecution planを作らない。

### 2.3 Predict

- new standalone scoring engine/APIを導入しない。
- current systemが既に生成・保持するprediction-bearing Result/Artifact/outputだけを表示対象とする。
- 利用可能なprediction outputが存在しない場合、「実行可能な新規Predict」を暗黙に作らず、利用可能なprediction resultがないことをdeterministicに表示する。

### 2.4 Metrics

- existing evaluation / error-analysis semanticsを表示する。
- metric viewを新たなExecution Stageとして起動する前提を置かない。既存executionが生成したevaluation Result/Artifactを参照してよい。

### 2.5 Explainability

- current explainability output/operationを保持する。
- predictive explanationをcausal effectとして表現しない既存warning/meaningを維持する。
- 1 Navigation Stageから既存の複数explanation operation/use caseを利用してよい。

### 2.6 Model Management

- scopeはread-onlyのfitted model / model card / artifact / lineage projectionに限定する。
- model registry CRUD、deployment、promotion、serving lifecycleを追加しない。

## 3. Form state preservation

active page session中にFamily/Stageを切り替えても、current Predictive画面で保護対象となる未保存form valueを不必要に破棄しない。実装方式はcurrent frontend state architectureに適合させてよいが、navigationするだけで入力値が初期defaultへ戻る挙動を導入しない。

browser reloadや別Project移動など、current systemで既にstate破棄される境界を本Packageだけで新たに永続化対象へ拡張しない。

## 4. In scope

- 6 Predictive Stage content/surfaceへの既存control/output再配置
- existing train action wiring
- existing prediction-bearing output display
- metrics / explainability / model metadata display
- session内form state preservation
- focused UI/integration tests

## 5. Out of scope / 禁止

- visible Predictive controlの削除
- input/default/validation semantics変更
- `predictive-analysis-spec/1` schema変更
- hidden preprocessing/model default変更
- LightGBM/new model family追加
- standalone scoring execution/API
- model registry CRUD/deployment
- Navigation StageとExecution Stageの1:1 mapping

## 6. Focused verification

最低限、以下を自動テストで証明する。

- 6 Stageすべてにcanonical navigationから到達できる。
- Setupにcurrent visible controlsが欠落なく存在し、representative inputでgenerated spec semanticsがP01 guardrailと一致する。
- Train actionがexisting execution pathを利用し、Navigation Stageをruntime Stageとして渡さない。
- Predictにnew scoring request/APIが増えていない。
- prediction outputなしの状態がdeterministicに表示される。
- Metricsがexisting evaluation dataを表示する。
- Explainabilityのpredictive-not-causal semantics/warningが保持される。
- Model Managementがread-onlyである。
- Stage切替後も保護対象の未保存form valueが保持される。

## 7. Package Acceptance Checklist

- [ ] 6 Predictive Stageが成立している
- [ ] visible controls 100%保持
- [ ] generated spec semantics維持
- [ ] existing train workflow維持
- [ ] Predictでnew scoring engine/APIなし
- [ ] Metrics/Explainability責務分離
- [ ] Model Management read-only
- [ ] session内form state保持
- [ ] Navigation/Execution 1:1 mappingなし

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
