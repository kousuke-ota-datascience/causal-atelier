# Ariadne ENH-E5 G03 実装指示書 — Gate Coding Contract（Gate実装契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G03
- Gate title: Causal Family Recomposition
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 契約状態: **DRAFT_FOR_REVIEW**（レビュー前ドラフト）
- Execution Mode: `WORK_PACKAGE`


## 0. 実装時の参照ポリシー — Gate contractとPackage contractの分離

本Gateは`WORK_PACKAGE`で実行する。

本06は、Operator / Planning担当がGate全体のacceptance claim、scope、禁止事項、Package分解、candidate assemblyを管理するための**Gate-level normative contract**である。一方、**Package Coding Agentのnormative implementation contractは、各Agentへ割り当てられたPxx 1文書のみ**とする。

Package Coding Agentへ本06、07、P00、00〜30、ADR、他Pxx、過去Enhancement、issue、commit message、外部Webその他の資料を併読させ、仕様を再合成させてはならない（MUST NOT）。Gate-level constraintのうち各Packageに必要な内容は、Planning担当がPxxを`FROZEN`にする前に当該Pxx本文へ収束させる。

current repositoryのproduction code、existing tests、schema/type/interface、configuration、route/API implementation、repository structureは、Package Agentがcurrent implementation factを確認し実装方法を決めるために参照してよい。ただしrepositoryは仕様authorityではない。

> **Repositoryから実装方法を発見してよいが、仕様を発見してはならない。**

Pxxだけではnormativeなrequired behaviorを一意に決定できない場合、Package Agentは探索範囲を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。

Pxxの外部にnormative decisionが残っている場合、そのPxxを`FROZEN`にしてはならない。Package完了はGate PASSを意味しない。

## 1. Gate定義 / acceptance claim

### 目的
current Causal Discovery/Inference surfacesをSetup/Discovery/Identification/Estimation/Effects/Diagnostics/Sensitivityへ再配置し、IdentificationとEstimationの責務分離を明示する。

### PASS後に後続Gateが利用できる成果
ユーザーとG05が、causal design/execution/resultsをdistinct Stage contextで利用しつつ既存causal semanticsへ依存できる。

### この単位を1つのGateとする理由
この境界は、独立してaccept/protectできる1つのsemantic claimである。実装量が大きい場合は、Execution Modeが`WORK_PACKAGE`のときにWork Packageで分割する。

## 2. 実装時に有効な前提

- Familyはanalytical capabilityのcontextである。
- Navigation StageはUI/application上の作業・閲覧contextである。
- `Navigation Stage != Execution Stage` を維持する。
- Stageの名称・数はFamilyごとに異なってよい。
- Stage navigationを必須のsequential workflowとはみなさない。
- このGateで明示的に変更しない限り、既存のanalysis execution/persistence semanticsを保護する。
- 外部analytical engineの追加はENH-E5のscope外である。

このGateに対応するAcceptance target:
- AC-G03-001: Causalの7 Navigation Stageすべてへ到達でき、canonical routeを使用する。
- AC-G03-002: Discoveryは現行graph discovery/candidate/direct-registration操作を保持する。
- AC-G03-003: Identificationは独立route/surfaceを持ち、identification strategy/adjustment/eligibility result contextをEstimationから分離して保持する。
- AC-G03-004: Estimationは新規estimatorを追加せず、現行estimator選択、warning/revision rule、execution semanticsを保持する。
- AC-G03-005: Effectsはestimation configurationと混同せず、treatment-effect result/compare semanticsを提示する。
- AC-G03-006: Diagnosticsは既存eligibility/estimation diagnosticsを保持する。
- AC-G03-007: Sensitivityは現行Refutation/Sensitivity操作・methodを保持する。
- AC-G03-008: Navigationはnon-sequentialとする。operation prerequisiteはactionをblockしてよいが、Stage navigation自体をblockしない。
- AC-G03-009: 既存causal regression testがPASSする。

## 3. Execution Mode の決定

Mode: `WORK_PACKAGE`。

Operator / Planning担当は`06_G03_P00_work_package_plan.md`と計画済みPxxを用いてPackage分解・依存関係・統合順序を管理する。ただしPackage Coding Agentへ渡すnormative inputは**assigned Pxxのみ**とし、06 / P00 / 他Pxxを併読させてscopeや仕様を再合成させてはならない。Package completionはGate PASSを意味しない。

## 4. 必須の実装semantics

実装は、保護対象upstream contractの意味を変えずにGate目的を成立させなければならない（MUST）。このGateで明示的に必要としない限り、現在のanalysis spec、execution plan、result schema、algorithmを保持するadditive/refactoring変更を優先する。

## 5. 許可されるscope

- Causalの7つのStage surface
- 現行discovery graph操作
- 現行identification/data eligibility
- 現行estimation method/execution
- effect比較
- diagnostics
- refutation/sensitivity

## 6. 明示的な禁止scope

- DoWhy/EconML
- new estimator library
- Analysis Management stage
- automatic causal identification proof
- strict stage wizard

全Gate共通の禁止事項:
- testをgreenにすることだけを目的としたassertion弱体化、test削除、skip、xfailは禁止;
- requirement/ACの無断変更は禁止;
- 後続Gateの作業をこのGateへ混入させない;
- 未承認のschema/dependency/engine拡張は禁止。

## 7. 保護対象となる既PASS Gate contract

先行ENH-E5 Gateのfinal-PASS contractすべて。**freeze前に具体的Gate ID / protected invariant / evidence identityを本06へ転記すること。未確定のままAgent executionへ渡してはならない。**

本06をfreezeする担当者が、必要なprotected Gate identity / evidenceをfreeze前に本節へ具体値として転記する。Coding AgentへCurrent State Control Sheetの再探索を要求しない。

## 8. Transition Debt

計画上は`NONE`。後続へ延期したscopeはTransition Debtではない。

一時的な例外挙動が不可避になった場合は停止し、architecture/Humanの明示的判断を求める。文書化されていないdebtを勝手に作らない。

## 9. Schema / migration / API / runtime ポリシー

- DB schema migration: 明示的なamendmentがない限り`PROHIBITED`。
- AnalysisSpecification/Execution/Result schema変更: このGateで明示しない限り`PROHIBITED`。
- Execution lifecycle: 既存semanticsを保持する。
- API変更: このGateで明示的に必要とするadditive変更だけを許可する。
- legacy analytical route: 保持または明示的にnormalizeし、無断削除しない。

## 10. 自動テスト義務

- AC-G03-001について自動テストevidenceを実装する: Causalの7 Navigation Stageすべてへ到達でき、canonical routeを使用する。
- AC-G03-002について自動テストevidenceを実装する: Discoveryは現行graph discovery/candidate/direct-registration操作を保持する。
- AC-G03-003について自動テストevidenceを実装する: Identificationは独立route/surfaceを持ち、identification strategy/adjustment/eligibility result contextをEstimationから分離して保持する。
- AC-G03-004について自動テストevidenceを実装する: Estimationは新規estimatorを追加せず、現行estimator選択、warning/revision rule、execution semanticsを保持する。
- AC-G03-005について自動テストevidenceを実装する: Effectsはestimation configurationと混同せず、treatment-effect result/compare semanticsを提示する。
- AC-G03-006について自動テストevidenceを実装する: Diagnosticsは既存eligibility/estimation diagnosticsを保持する。
- AC-G03-007について自動テストevidenceを実装する: Sensitivityは現行Refutation/Sensitivity操作・methodを保持する。
- AC-G03-008について自動テストevidenceを実装する: Navigationはnon-sequentialとする。operation prerequisiteはactionをblockしてよいが、Stage navigation自体をblockしない。
- AC-G03-009について自動テストevidenceを実装する: 既存causal regression testがPASSする。

変更moduleに対するfocused existing testと、diffの影響を受けるすべての保護対象upstream contractを対象としたregression testも実行する。

## 11. Candidate Assembly（候補成果物の組み立て）

`READY_FOR_TEST`へ移行する前に:
1. 必須の実装scopeがすべて完了していること;
2. Packageがある場合、すべてに有効なcheckpoint reportがあること;
3. 未解決blockerが`NONE`であること;
4. focusedおよびGate-wide self-verificationが記録されていること;
5. production/test/migration/dependency diffがレビュー済みであること;
6. implementation completion reportにFixed Trial Candidate SHAが1つ記録されていること。

## 12. Coding Agent の禁止作業

Coding Agentは以下をしてはならない:
- Gate PASSを判定する;
- 07 Acceptance Criteriaを変更する;
- Package完了をpartial PASSとして扱う;
- amendmentなしに既PASS Gateのsemanticsを変更する;
- 対象外の後続featureを実装する。

## 13. 必須成果物

- Trial01（またはcurrent Trial）のimplementation completion report
- 必要に応じたGate-local implementation ledger/detail
- `WORK_PACKAGE`時のPackage checkpoint/status report
- 正確なFixed Trial Candidate SHA
- 実行commandとtest evidence
- 明示的なblocker status

## 14. 外部参照ポリシー

source code pathおよび観測したruntime/test outputはevidenceとして参照してよい。実行に必要な規範的ルールは本contract、およびWork Package modeでは割り当てられたPxx contractに記載する。
