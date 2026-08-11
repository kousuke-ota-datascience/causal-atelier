# ENH-E5 G02 P03 — Predictive Regression / Candidate

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G02`
- Trial: `01`
- Package: `P03`
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 依存Package: `P01,P02`
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

Predictive再配置後のsemantic compatibilityをGate-wideにself-verifyし、Test Agentへ渡せるFixed Trial Candidateの実装側evidenceを揃える。

## 2. Regression dimensions

以下を独立に確認する。

1. **Configuration compatibility** — current visible controls、validation、default、generated spec。
2. **Execution compatibility** — existing split/prepare/train/evaluate/(explain) path。
3. **Result compatibility** — prediction-bearing output、metrics、explanation、model-card/artifact/lineage。
4. **Navigation semantics** — 6 Stage到達、canonical route、non-sequential movement。
5. **State preservation** — active session内の未保存form value。
6. **Scope protection** — new engine/scoring/model registry/schema changeがない。

## 3. Required negative checks

- `NavigationStage`をExecution `StageType`/runner selectionへ渡すcode pathが追加されていない。
- Predict Stageのためだけのnew standalone scoring endpoint/runnerが追加されていない。
- Model Managementにwrite/deploy/promotion operationが追加されていない。
- snapshot/test期待値を更新することでspec semantic差分を隠していない。
- Explainabilityからcausal claimへ意味を強めていない。

## 4. Focused / regression verification

current repositoryから影響範囲の既存Predictive testを特定して実行する。さらにP01/P02で追加したcompatibility/navigation testsを全て実行する。

少なくとも以下のscenario evidenceを含める。

- representative Setup入力→generated spec→Train execution trigger
- Train完了後のMetrics参照
- prediction output有/無のPredict表示
- Explainability表示とwarning
- Model Management read-only projection
- Setup入力変更→別Stage→Setupへ戻った際のvalue保持
- 6 canonical routesのdirect load

full suiteを実行可能なrepository baselineでは関連full suiteも実行し、実行不能ならcommand/阻害要因を正確に報告する。testをskip/xfail/弱体化してgreen化しない。

## 5. In scope

- regression test追加/補強
- compatibility evidence
- candidate self-verification
- regressionで発見した本Gate scope内bug修正

## 6. Out of scope / 禁止

- regression結果を理由としたrequirement変更
- baselineの既存仕様を推測で再定義すること
- new analytical engine/dependency/schema migration
- Gate PASS判定

## 7. Package Acceptance Checklist

- [ ] P01/P02の全focused testsがgreen
- [ ] current Predictive regression testsがgreen
- [ ] representative generated spec semantic equivalence確認
- [ ] execution path regression確認
- [ ] output / warning / read-only boundary確認
- [ ] prohibited scopeのdiffがない
- [ ] Fixed Trial Candidate SHAを記録可能な状態

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
