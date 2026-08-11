# ENH-E5 G03 P03 — Causal Regression / Candidate

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G03`
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

7 Stage再配置後もcurrent Causal capabilityのgraph discovery、identification/eligibility、estimation、effect、diagnostics、refutation/sensitivity semanticsが維持されることをself-verifyし、Fixed Trial Candidateを組み立てる。

## 2. Regression dimensions

- Discovery operations
- Identification / data eligibility
- current estimator selection / warning / revision rule
- execution trigger and Result semantics
- effect result/compare
- diagnostics
- refutation/sensitivity
- non-sequential navigation / deep link
- Navigation/Execution separation

## 3. Required negative checks

- DoWhy/EconML/new estimator dependencyがない。
- `Identification` / `Estimation`等のNavigation Stage名をruntime `StageType`へ追加・aliasしていない。
- strict wizard / completion stateを追加していない。
- IdentificationとEstimationを再び同一surfaceへ潰していない。
- Effectsにestimation configurationを書き込むUIを追加していない。
- current causal warningを弱めていない。

## 4. Required scenarios

少なくとも以下のscenarioを自動testまたはrepeatable integration evidenceで確認する。

1. Discoveryのcurrent graph/candidate/direct-registration path。
2. Identification/eligibility contextの表示。
3. prerequisite不足のEstimation direct load → Stage表示可能、実行actionは理由付きblock。
4. valid current estimator execution path。
5. Effectsで推定result/compareを表示。
6. Diagnosticsでexisting diagnosticを表示。
7. Sensitivityでcurrent refutation/sensitivity operationを実行/表示。
8. 7 canonical routesのdirect load。
9. existing causal focused/regression tests。

## 5. In scope

- regression test補強
- current causal focused suite実行
- 本Gate scope内regression bug修正
- candidate self-verification evidence

## 6. Out of scope / 禁止

- testを通すためのwarning/assertion弱体化
- new causal methodology
- schema migration/new dependency
- Gate PASS判定

## 7. Package Acceptance Checklist

- [ ] current Causal regression tests green
- [ ] 7 Stage regression green
- [ ] Identification/Estimation separation evidenceあり
- [ ] Effects/Diagnostics/Sensitivity evidenceあり
- [ ] non-sequential navigation evidenceあり
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
