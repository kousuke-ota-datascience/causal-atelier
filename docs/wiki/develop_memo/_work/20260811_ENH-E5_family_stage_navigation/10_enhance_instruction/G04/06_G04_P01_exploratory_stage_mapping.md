# ENH-E5 G04 P01 — Exploratory Stage Mapping

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G04`
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

current Explore & Visualize capabilityを、analytical semanticsを変えず次の6 Navigation Stageへ再配置する基礎surface/mappingを成立させる。

1. `Profile`
2. `Data Quality`
3. `Distribution`
4. `Relationships`
5. `Comparison`
6. `Findings`

EDAはstrict sequential workflowではなく探索観点によるnavigationである。

## 2. Stage responsibility

### Profile
current dataset/profile/Analysis View contextから取得可能なshape/schema/type/cardinality/summary等のprofile情報を扱う。current implementationに存在しないprofile metricを推測追加しない。

### Data Quality
current data/profile capabilityから事実として取得・導出できるmissing/duplicate/invalid/outlier candidate等のquality情報を扱う。未support metricを捏造しない。

### Distribution
current univariate distribution operation/resultを扱う。histogram等のvisualizationはこのStage内の表現手段とする。

### Relationships
current association/relationship operation/resultを扱う。相関・associationをcausal effectとして表現しない。

### Comparison
current group summary / segment / time comparison等、current repositoryがsupportする比較operation/resultを扱う。

### Findings
current saved exploratory Result / Annotation / Lineage等を利用して探索結果を再訪できるsurfaceとする。new persistent `Finding` entityを追加しない。

## 3. Operation mapping rule

current Explore operationの正確なtype/nameはrepository factとして確認する。Stage assignmentは上記analytical responsibilityに従うが、operation semantics・parameter・Result schema・algorithmを変更しない。

同じoperation/resultを複数Stageから参照する必要がある場合、presentation projectionとして共有してよい。Navigation StageとExecution Stageの1:1 mappingを作らない。

## 4. In scope

- 6 Exploratory Stage route/content foundation
- current profile/data-quality factのplacement
- current distribution/association/group/time operation/resultのplacement
- Findings surface foundation
- focused tests

## 5. Out of scope / 禁止

- standalone `Visualization` Stage
- new EDA/statistical engine/method
- new persistent Findings/Evidence entity
- exploratory associationへのcausal interpretation
- current Explore spec/execution/result semantics変更

## 6. Focused verification

- 6 Stageすべてがcanonical routeから到達できる。
- Profileがcurrent profile contextを保持する。
- Data Qualityがcurrent sourceに存在しないmetricを表示しない。
- Distribution/Relationships/Comparisonでcurrent operation semanticsが保持される。
- Findingsがexisting saved Result/Annotation/Lineage等のprojectionでありnew entityを要求しない。
- Stage navigationがnon-sequentialである。
- Execution `StageType`へ6 Navigation Stageを追加していない。

## 7. Package Acceptance Checklist

- [ ] 6 Exploratory Stage成立
- [ ] existing profile/quality fact保持
- [ ] existing exploratory operation/result保持
- [ ] no fabricated metric
- [ ] no causal reinterpretation
- [ ] no new Finding entity
- [ ] no Navigation/Execution 1:1 mapping
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
