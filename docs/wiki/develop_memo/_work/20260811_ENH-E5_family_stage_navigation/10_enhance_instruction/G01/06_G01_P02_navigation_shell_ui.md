# ENH-E5 G01 P02 — Navigation Shell UI

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G01`
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

Project workspace内に、Familyをglobal analytical context、Navigation StageをFamily-local contextとして視覚的に分離したnavigation shellを成立させる。

## 2. Target layout / hierarchy

実装上のDOM/component構造はcurrent frontendに適合させてよいが、外部挙動は次を満たす。

```text
Project header / global context

[ Exploratory ] [ Predictive ] [ Causal ]
-----------------------------------------------------------
Stage sidebar             | Main content
(selected Family only)    | selected Navigation Stage
-----------------------------------------------------------
Global project surfaces: Research Context / Data / Results-Lineage 等
```

Family tabsとStage sidebarは異なるnavigation dimensionである。

## 3. Family navigation requirements

- Family tabsにはcanonical catalogから得た`Exploratory / Predictive / Causal`の3 Familyだけを、catalog-defined orderで表示する。
- Current Familyを視覚上・accessibility state上の両方で識別可能にする。
- Family tab clickはP01で成立したroute transitionを使い、そのFamilyのcatalog-defined default Stageへ遷移する。
- Family label/order/defaultをfrontendに別途hard-codeしない。
- Project Management、Research Context、Data、Results/Lineage、Overviewをanalytical Family tabとして混在させない。

## 4. Stage sidebar requirements

- sidebarにはCurrent Familyのcatalogが所有するStageだけをcatalog-defined orderで表示する。
- Current Stageを視覚上・accessibility state上の両方で識別可能にする。
- Stage clickは同じFamilyを維持してcanonical routeへ遷移する。
- Family間でStage数を揃えるdummy Stageを作らない。
- Stage navigationにprevious/next completionやwizard進行条件を課さない。
- Stage renderer/contentが未実装の時点でもnavigation shellはStage identityをExecution Stageへ変換してはならない。

## 5. Error / loading behavior

- catalog取得中は、誤ったFamily/Stageを推測表示せずloading stateを表す。
- catalog取得失敗は明示的errorとして扱い、静的な別catalogへsilent fallbackしない。
- P01がunknown Family/Stageを返した場合、navigation errorとして表示し、有効候補を提示する。勝手に先頭Family/Stageへ遷移しない。

## 6. In scope

- Family tab component / rendering
- Family-local Stage sidebar
- current/active/accessibility state
- catalog loading/error state
- existing workspace shellへの組込み
- global project surfaceとのvisual/navigation responsibility分離
- frontend automated tests

## 7. Out of scope / 禁止

- Family固有のanalytical content再設計（G02-G04相当）
- route semanticsの再定義
- catalogのfrontend static複製
- navigation state DB persistence
- new Overview tab
- Result/Lineage global surface削除
- Execution Stage / runner / planner変更

## 8. Focused verification

最低限、以下を自動テストで証明する。

- catalogの3 Familyだけがtop analytical tabsへ表示される。
- Current Familyのactive stateがFamily switchで更新される。
- sidebarがCurrent FamilyのStageだけを表示し、Family変更で内容が置換される。
- Current Stage active stateがrouteに追随する。
- Stage orderがcatalog orderと一致する。
- Management / Context / Data / Results-Lineage等がFamily tabsへ混入しない。
- catalog loading/error/unknown routeの各状態がsilent fallbackしない。
- keyboard/focus/ARIA等、current frontendが採用するaccessibility patternを壊さない。
- Family/Stage clickがP01のcanonical route transitionを利用する。

## 9. Package Acceptance Checklist

- [ ] FamilyとStageが別navigation dimensionとして表示される
- [ ] Family/Stage label/order/defaultのfrontend重複定義がない
- [ ] active stateがURL/current routeと一致する
- [ ] global project surfacesがFamily tab外に残る
- [ ] error/loading時にsilent fallbackしない
- [ ] Execution Stageへのmappingがない
- [ ] focused frontend testsがgreenである

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
