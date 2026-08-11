# ENH-E5 G01 P01 — Route / Navigation State

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G01`
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

URLをCurrent Family / Current Navigation Stageのcanonical stateとして扱うroute/state層を成立させる。UI shellの描画そのものは本Packageでは行わない。

## 2. 固定する意味論

- canonical analysis routeは`/projects/{project_id}/analysis/{family_slug}/{stage_slug}`とする。
- `family_slug` / `stage_slug` / Familyごとの`default_stage`は、G00で成立したcanonical navigation catalogをsource-of-truthとして利用する。route層で別catalog、別enum、別defaultをhard-codeしない。
- Family slugはcatalog上のstable identityを用いる。表示labelからslugをその場で生成しない。
- Family切替は対象Familyの`default_stage`へ遷移する。直前StageをFamily別に記憶して復元する機能は実装しない。
- browser URLからFamily / Stageを復元できること。Current Family / StageをDBやworkspace-stateへ永続化しない。
- unknown Familyまたはunknown Stageを、別Family/Stageへ黙ってfallbackしてはならない。明示的navigation errorと、catalogから導出した有効な移動候補を返せる状態にする。
- Navigation Stageを`StageType`、`StageDefinition`、runner selection、ExecutionPlan dependencyへ変換しない。
- `AnalysisSpecification`、`ExecutionPlan`、`Execution`、`StageExecution`へNavigation Stage fieldを追加しない。

## 3. Legacy route normalization

既存のanalytical entry routeを無断削除しない。現在repositoryに存在するlegacy routeのうち、少なくとも以下をcanonical routeへnormalizeする。

- `/explore`系entry → `Exploratory` Familyのcatalog-defined default Stage
- `/predictive`系entry → `Predictive` Familyのcatalog-defined default Stage
- `/causal`系entry → `Causal` Familyのcatalog-defined default Stage

project_idを保持できる既存routeでは同一Projectを保持する。legacy pathにProject identityが存在しない場合の既存Project解決semanticsを、このPackageの都合で新設・変更しない。

normalize先Stage名をroute層で重複定義せず、対象Familyのcatalog-defined defaultを利用する。

## 4. In scope

- route parse / serialize
- navigation catalogからのFamily / Stage validation
- current routeからCurrent Family / Stageを導出するstate adapter
- legacy analytical entryのcanonical normalization
- unknown Family / Stage error state
- 上記に対するunit/frontend-router test

## 5. Out of scope / 禁止

- Family tab / Stage sidebarのvisual rendering
- Family固有content panelの再配置
- DB migration / navigation state persistence / last-stage memory
- new Overview Family/tab
- analytical execution API / CLI / runner contractの変更
- `Navigation Stage == Execution Stage`を仮定するmapping
- family/stage labelの翻訳やUX copy再設計を理由としたcanonical identity変更

## 6. 実装要件

1. route parserはproject_id、family_slug、stage_slugを分離して扱い、catalogに照らしてdeterministicにvalidationする。
2. serializerは同じnavigation stateに対して同じcanonical pathを生成する。
3. direct load時にURLだけからCurrent Family / Stageを復元できる。
4. Family変更commandはcatalog-defined default Stageを選択してcanonical routeを生成する。
5. Stage変更commandはCurrent Familyを保持し、そのFamilyが所有しないStageを受理しない。
6. legacy normalizationはcanonical routeへの一方向normalizationとし、canonical routeからlegacy routeへ戻さない。
7. unknown routeはheuristic fallbackせずerror stateを返す。有効候補はcatalogから導出する。
8. current repositoryに既存router/history abstractionがある場合はそれを利用してよいが、その既存挙動から新しい仕様を推測しない。

## 7. Focused verification

最低限、以下を自動テストで証明する。

- 3 Familyそれぞれについてcanonical routeのparse/serialize round-tripが成立する。
- direct loadでURLからCurrent Family / Stageが復元される。
- Family switchで対象Familyのcatalog-defined default Stageへ遷移する。
- last-stage memoryを参照しない。
- Family AのStageをFamily Bのrouteへ指定するとinvalidになる。
- unknown Family / Stageが明示的errorになり、黙ったfallbackがない。
- `/explore`、`/predictive`、`/causal`系legacy entryが該当Family defaultへnormalizeされる。
- navigation route処理がExecution `StageType` / runner selectionを参照しないことを、構造testまたはdependency-level assertionで確認する。

既存testの具体的なfile/pathはrepository factとして探索してよい。test名や配置が異なる場合でも、上記semantic evidenceを弱めてはならない。

## 8. Package Acceptance Checklist

- [ ] canonical routeがcatalog-drivenである
- [ ] Current Family / StageがURLから復元可能である
- [ ] Family switchがcatalog-defined default Stageを用いる
- [ ] legacy route normalizationがある
- [ ] unknown routeの黙ったfallbackがない
- [ ] DB persistence / last-stage memoryを追加していない
- [ ] Execution Stage dependencyを追加していない
- [ ] focused testsがgreenである

## 9. Protected semantics

本Packageは既存analysis spec、execution plan、execution lifecycle、Result/Artifact semanticsを変更してはならない。current branchに先行Package/Gateの変更が統合済みであることはOperatorがFROZEN前に保証する。Package Agentはその保証を外部文書から再構成しない。

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
