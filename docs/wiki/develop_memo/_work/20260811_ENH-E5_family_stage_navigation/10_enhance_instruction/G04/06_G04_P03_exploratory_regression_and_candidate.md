# ENH-E5 G04 P03 — Exploratory Regression / Candidate

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G04`
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

Exploratory再配置後もcurrent Explore/Profile/operation/Result semanticsとnon-causal boundaryが維持されることをself-verifyし、Fixed Trial Candidateの実装側evidenceを揃える。

## 2. Regression dimensions

- dataset/profile access
- current data-quality facts
- distribution operations/results
- relationships/association operations/results
- group/time/segment comparison operations/results
- visualization controls
- saved Result/Annotation/Lineage projection
- non-causal interpretation warning
- 6 Stage canonical navigation

## 3. Required negative checks

- `Visualization` Navigation Stageが追加されていない。
- new EDA/statistical method/dependencyが追加されていない。
- new persistent Finding/Evidence entity/table/schemaが追加されていない。
- association/correlationをcausal effectとして表現するcopy/semantic変更がない。
- Navigation Stage名がExecution `StageType`へ追加・aliasされていない。
- testsをgreenにするためexisting warning/assertionを弱めていない。

## 4. Required scenarios

最低限、次を自動testまたはrepeatable integration evidenceで確認する。

1. Profile Stageからcurrent dataset/profile contextを参照。
2. Data Qualityでcurrent sourceに存在するquality factだけを表示。
3. Distributionでcurrent distribution operation/resultを利用。
4. Relationshipsでcurrent association operation/resultとnon-causal boundaryを確認。
5. Comparisonでcurrent group/time/segment comparisonを利用。
6. Findingsでexisting saved result/annotation/lineageへ到達。
7. 6 canonical routesをdirect load。
8. existing exploratory focused/regression tests。

## 5. In scope

- regression test補強
- existing exploratory suite実行
- 本Gate scope内regression bug修正
- candidate self-verification evidence

## 6. Out of scope / 禁止

- new analysis method/entity/schema
- product requirement変更
- Gate PASS判定

## 7. Package Acceptance Checklist

- [ ] current exploratory regression tests green
- [ ] 6 Stage scenario green
- [ ] visualization placement regression green
- [ ] Findings/lineage regression green
- [ ] non-causal semantics regression green
- [ ] prohibited engine/schema/runtime-stage diffなし
- [ ] Fixed Trial Candidate SHA記録可能

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
