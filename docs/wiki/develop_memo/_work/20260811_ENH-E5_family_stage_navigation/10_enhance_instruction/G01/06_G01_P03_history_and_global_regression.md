# ENH-E5 G01 P03 — History / Global Regression

文書区分: Primary Execution Contract（Work Package実装契約）
自己完結性: MUST（必須）

- Gate: `G01`
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

P01/P02で成立したnavigation shellについて、direct load、browser history、legacy normalization、global workspace regressionを閉じ、Gate candidateとして統合可能な状態にする。

## 2. History / direct-load requirements

- canonical URLへのdirect loadで同じProject / Family / Stageを復元する。
- Stage click、Family switchはbrowser historyへ正しく反映し、back/forwardで過去のFamily / Stageへ戻れる。
- reloadしてもURLから同じFamily / Stageが復元される。DBやsession上のlast-stage memoryを復元sourceにしない。
- legacy routeを開いた場合はcanonical targetへnormalizeし、以降のhistory entryはcanonical routeを使用する。
- invalid routeをback/forwardで踏んだ場合もsilent fallbackしない。

## 3. Global workspace regression requirements

navigation再編後も、既存global project surfaceの意味を保持する。

- Project Management / project context
- Research Context
- Data / Dataset / Analysis View
- Results / Lineageおよび既存global result access

これらをanalytical Family tabへ移動・削除・semantic renameしない。既存Project identity / contextをFamily switchで失わない。

## 4. Non-sequential navigation requirements

- Stage間移動にcompletion flag、previous step完了、execution status等を要求しない。
- operation固有のprerequisiteがある場合でも、それはactionのavailabilityでありsidebar routeへの移動を禁止する理由にしない。
- history復元時に「順序違反」を理由として別Stageへredirectしない。

## 5. In scope

- browser history / popstate相当のintegration
- direct load / reload
- legacy normalization integration
- global workspace navigation regression
- invalid-route regression
- Gate-wide navigation tests

## 6. Out of scope / 禁止

- Family固有analytical semantics変更
- new execution action
- Result/Lineage schema変更
- navigation DB persistence / last-stage memory
- historyを利用したworkflow completion tracking

## 7. Focused verification

最低限、以下のE2Eまたはfrontend integration evidenceを作る。

1. Predictiveの任意Stage → Exploratory default → browser back →元Predictive Stage。
2. 同一Family内Stage A→B→back/forwardでURLとactive stateが一致する。
3. canonical deep linkを新規loadして正しいFamily/Stageがactiveになる。
4. reload後も同一URL/stateになる。
5. `/explore`、`/predictive`、`/causal`legacy entryがcanonical routeへnormalizeされる。
6. unknown Family/Stageで明示的errorを示す。
7. global Research Context / Data / Results-Lineage entryがFamily switch後も利用可能である。
8. Stage navigationにwizard completion guardがない。
9. navigation変更により既存analytical execution regressionが壊れていないことを、影響範囲のexisting testsで確認する。

## 8. Package Acceptance Checklist

- [ ] direct load / reload / back / forwardがcanonical URLと一致する
- [ ] legacy entryがcanonical routeへnormalizeされる
- [ ] global project surfacesが保持される
- [ ] Project contextがFamily switchで失われない
- [ ] non-sequential navigationが維持される
- [ ] invalid routeのsilent fallbackがない
- [ ] focused / affected regression testsがgreenである

## 9. Candidate assembly input

本Package終了時点でP01/P02を含むcurrent branch全体に対し、navigation shellのfocused regressionを実行する。Gate PASSは判定しないが、Gate-level Test Agentへ渡せるFixed Trial Candidateを作るための実装側self-verification evidenceを揃える。

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
