# ENH-E5 G03 P02 — Identification / Estimation Separation

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G03`
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

Causal UI/application上でIdentificationとEstimationの責務境界を明確にし、既存execution semanticsを変更せず、ユーザーが「識別可能性」と「推定方法」を別contextとして扱える状態を成立させる。

## 2. Identification contract

Identificationは次の問いを扱うcontextである。

> 観測データと仮定から、目的のcausal estimandを識別できるか。

current systemが保持する範囲で、identification strategy、adjustment set/context、data eligibility、assumption/warning等を提示する。current codeに存在しないformal proof engine、IV/DiD等の新strategy、automatic identification expression generatorを推測追加しない。

Identificationのresult/contextをEstimation form controlへ単純に埋め込んで独立Stageを消してはならない。

## 3. Estimation contract

Estimationは、識別された/選択されたestimandを有限標本からどのcurrent estimatorで推定するかを扱う。

- current estimator selectionを保持する。
- current warning / revision rule / eligibility gateを保持する。
- current execution plan / runner semanticsを保持する。
- Navigation Stage `Estimation`をruntime `StageType`として新設・aliasしない。

## 4. Effects / Diagnostics / Sensitivityとの境界

- Estimationは**設定・実行**。Effectsは**推定済みeffectの閲覧/比較**。
- Diagnosticsは妥当性/eligibility/estimation diagnosticsの閲覧。
- Sensitivityはcurrent refutation/sensitivity operation。
- 同じbackend Result/Artifactを複数Navigation Stageがprojectionしてよい。1:1 execution mappingは不要。

## 5. Prerequisite behavior

- Identification/eligibilityが不足している場合、Estimation Stageへのnavigation自体は許可する。
- 実行できないactionは理由を明示してblockする。
- Stage orderを強制するwizard stateを追加しない。
- browser deep linkでEstimationへ直接到達しても、未完了前Stageへ強制redirectしない。

## 6. In scope

- Identification/Estimation UI responsibility分離
- existing eligibility/strategy/resultのprojection
- action availability / warning presentation
- Effects/Diagnostics/Sensitivityとの責務境界調整
- focused tests

## 7. Out of scope / 禁止

- new causal estimator/engine
- automatic identification proof
- new persistence model for identification navigation state
- strict sequence/wizard
- current Result/schema semantics変更

## 8. Focused verification

- IdentificationとEstimationが別canonical Stage/routeとして存在する。
- 同じcontrol/actionが責務不明瞭な形で両Stageへ重複しない。
- current eligibility/identification contextがIdentification側から確認できる。
- current estimator selection/execution actionがEstimation側で保持される。
- prerequisite不足時はactionが理由付きでblockされ、navigationはblockされない。
- Effectsがestimator configurationを持たない。
- Navigation Stage追加によりExecution `StageType`が増えていない。

## 9. Package Acceptance Checklist

- [ ] Identificationの問いとsurfaceが独立
- [ ] Estimationのcurrent estimator semantics保持
- [ ] Effects/Diagnostics/Sensitivity境界明確
- [ ] prerequisiteはaction-level
- [ ] deep linkでstage-order redirectなし
- [ ] runtime execution abstraction変更なし
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
