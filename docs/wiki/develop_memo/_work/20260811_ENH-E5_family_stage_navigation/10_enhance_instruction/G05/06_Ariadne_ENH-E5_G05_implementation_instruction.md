# Ariadne ENH-E5 G05 実装指示書 — Gate Coding Contract（Gate実装契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G05
- Gate title: Cross-family Convergence and Product Regression（Family横断収束・product regression）
- Branch: `feature/ariadne_mvp_e5`
- Baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- 契約状態: **DRAFT_FOR_REVIEW**（レビュー前ドラフト）
- Execution Mode: `SINGLE_EXECUTION`


## 0. 実装時の参照ポリシー — 本06のみをnormative sourceとする

本Gateは`SINGLE_EXECUTION`で実行する。Coding Agentに対する**唯一のnormative implementation contractは本06文書のみ**である。

Coding Agentは`WHAT / WHY / scope / responsibility / prohibited change / required outcome`を本06だけから判断しなければならない（MUST）。仕様を補完する目的で、00〜30、ADR、Gate decomposition、07、他Gate文書、過去Enhancement、issue、commit message、外部Webその他の資料を参照してはならない（MUST NOT）。

current repositoryのproduction code、existing tests、schema/type/interface、configuration、route/API implementation、repository structureは、current implementation factを確認し実装方法を決めるために参照してよい。ただしrepositoryは仕様authorityではない。

> **Repositoryから実装方法を発見してよいが、仕様を発見してはならない。**

current codeが本06と異なることを理由に、本06の要求を追加・削除・緩和・変更してはならない。

本06だけではrequired behavior、ownership、scope、compatibility、migration、architecture choiceを一意に決定できない場合、他資料を探索して補完せず`BLOCKED_CONTRACT_AMBIGUITY`で停止する（MUST）。

本06の外部にnormative decisionが残っている場合、本06を`FROZEN`にしてはならない。

## 1. Gate定義 / acceptance claim

### 目的
3 Familyのnavigation/Stage recomposition後に、project context・Results/Lineage・routing・existing analytical execution/persistenceがcross-familyで一貫することを確立する。

### PASS後に後続Gateが利用できる成果
ENH-E5全体をproduct-level verified contractとして利用・release判断できる。

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
- AC-G05-001: Family切替およびglobal workspace間でもResearch Context/Dataset/Analysis View project contextの整合性を維持する。
- AC-G05-002: Global Results/Lineageは既存cross-family result/lineageのaggregate/navigation機能を維持する。
- AC-G05-003: G02-G04変更後も、すべてのcanonical Family/Stage deep linkとlegacy mappingが併存して機能する。
- AC-G05-004: PASS済みG00-G04のprotected contractを無断変更しない。
- AC-G05-005: DB schema migration、新規analytical engine dependency、Result schema再設計、navigation persistenceを導入していない。
- AC-G05-006: Fixed Trial Candidate上でfull `uv run pytest -q`がPASSする。
- AC-G05-007: 利用可能なbrowser/e2e regression suiteがFamily tab、Stage navigation、direct route、back/forward、代表的Family operationについてPASSする。
- AC-G05-008: requirements/design/traceability docs match the implemented/verified contract and contain no unresolved placeholders except explicitly permitted evidence identities before PASS.

## 3. Execution Mode の決定

Mode: `SINGLE_EXECUTION`.

1つのbounded candidateとして実装し、candidate freeze前にGate-wide self-checkを実施する。

## 4. 必須の実装semantics

実装は、保護対象upstream contractの意味を変えずにGate目的を成立させなければならない（MUST）。このGateで明示的に必要としない限り、現在のanalysis spec、execution plan、result schema、algorithmを保持するadditive/refactoring変更を優先する。

## 5. 許可されるscope

- cross-family context continuity
- Results/Lineage global continuity
- all canonical/legacy route regression
- full automated regression
- browser e2e
- documentation synchronization

## 6. 明示的な禁止scope

- E5 accepted scopeを超える新規product feature
- schema migration
- engine addition
- prior Gate contractの無断緩和

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

- AC-G05-001について自動テストevidenceを実装する: Family切替およびglobal workspace間でもResearch Context/Dataset/Analysis View project contextの整合性を維持する。
- AC-G05-002について自動テストevidenceを実装する: Global Results/Lineageは既存cross-family result/lineageのaggregate/navigation機能を維持する。
- AC-G05-003について自動テストevidenceを実装する: G02-G04変更後も、すべてのcanonical Family/Stage deep linkとlegacy mappingが併存して機能する。
- AC-G05-004について自動テストevidenceを実装する: PASS済みG00-G04のprotected contractを無断変更しない。
- AC-G05-005について自動テストevidenceを実装する: DB schema migration、新規analytical engine dependency、Result schema再設計、navigation persistenceを導入していない。
- AC-G05-006について自動テストevidenceを実装する: Fixed Trial Candidate上でfull `uv run pytest -q`がPASSする。
- AC-G05-007について自動テストevidenceを実装する: 利用可能なbrowser/e2e regression suiteがFamily tab、Stage navigation、direct route、back/forward、代表的Family operationについてPASSする。
- AC-G05-008について自動テストevidenceを実装する: requirements/design/traceability docs match the implemented/verified contract and contain no unresolved placeholders except explicitly permitted evidence identities before PASS.

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
