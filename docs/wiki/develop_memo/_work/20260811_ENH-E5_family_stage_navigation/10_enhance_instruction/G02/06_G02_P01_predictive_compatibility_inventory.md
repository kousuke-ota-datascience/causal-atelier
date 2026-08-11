# ENH-E5 G02 P01 — Predictive Compatibility Inventory / Guardrail

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G02`
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

Predictive UI再配置の前に、current repositoryから既存Predictive configuration/controlとgenerated `predictive-analysis-spec/1` semanticsを全量特定し、それらを失わないcompatibility guardrailをcode/testとして成立させる。

## 2. Normative compatibility rule

- **現行visible Predictive controlは100%保持する。** 削除、意味変更、default変更、入力制約の無断変更をしない。
- current UIに存在するcontrolの正確な一覧・field binding・defaultはrepository factとして調査する。推測で項目を追加しない。
- 同等inputから生成される`predictive-analysis-spec/1`の既存visible/hidden/default semanticsを保持する。
- current hidden preprocessing/model/split defaultを新UI都合で変更しない。
- `AnalysisSpecification.analysis_family`等の既存contractを維持し、Navigation Stage fieldをspecへ追加しない。

## 3. 調査対象と成果

Package Agentはcurrent repositoryを読み、少なくとも次をfactとしてinventoryする。

- Predictive画面の全visible input/control
- controlごとのsource component/form field
- generated analysis-spec fieldへのbinding
- UIで明示されないがgenerated specへ入るdefault/hidden semantics
- validation / enable-disable condition
- split / train / evaluation / explain関連の既存execution trigger
- prediction-bearing Result/Artifactの既存有無とaccess path
- metrics / explainability / model-card / fitted-model / lineageの既存表示元

このinventoryを、将来別資料を読まなくてもregressionで守れるよう**自動テスト・fixture・明示的mapping table等のrepository-local executable/inspectable guardrail**へ落とす。新しい製品仕様をinventoryから推論してはならない。

## 4. In scope

- current Predictive control/spec bindingのfact inventory
- compatibility fixture / regression test
- necessary test helper
- 後続P02が安全にrecomposeできる最小限のnon-behavioral refactoring

## 5. Out of scope / 禁止

- Predictive Stage UIの本格再配置
- control削除/追加を伴うproduct redesign
- `predictive-analysis-spec/1` schema version変更
- preprocessing/model default変更
- LightGBM等のnew engine
- standalone scoring API/execution
- model registry CRUD/deployment

## 6. Focused verification

最低限、以下を証明する。

- current visible controlsがinventory/guardrailから漏れていないことを、DOM/form definition等のcurrent factと照合できる。
- representative input setについて、再配置前baselineと同等の`predictive-analysis-spec/1` payload/semantic fieldが得られる。
- hidden/default fieldsが意図せず変化していない。
- existing Predictive validation behaviorを弱めていない。
- current Predictive focused testsがgreenである。

テストがbaseline snapshotを利用する場合、意味のあるfield差分を単にsnapshot更新で受け入れてはならない。差分が発生したら本Pxxとの整合を確認し、仕様変更が必要なら`BLOCKED_CONTRACT_AMBIGUITY`またはamendment要求とする。

## 7. Package Acceptance Checklist

- [ ] visible control全量inventoryがrepository factから取得されている
- [ ] field/default/hidden semanticsのguardrailがある
- [ ] `predictive-analysis-spec/1` schema/semanticsを変更していない
- [ ] predictive execution trigger semanticsを変更していない
- [ ] new analytical engine/APIを追加していない
- [ ] focused compatibility testsがgreenである

## 8. 後続Packageへ残すcontract

P02は本Packageの外部文書を読むのではなく、P02自身のcontractだけで実行される。本Packageで得たcurrent factのうちP02のnormative実装に必要なものは、Planning担当がP02をFROZENする前にP02本文へ収束させる。Package Agent同士で口頭・暗黙の仕様引継ぎをしない。

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
