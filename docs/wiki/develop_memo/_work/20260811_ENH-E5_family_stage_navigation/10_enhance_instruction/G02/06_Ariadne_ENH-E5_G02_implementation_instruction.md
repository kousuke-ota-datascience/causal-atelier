# Ariadne ENH-E5 G02 実装指示書 — Gate Coding Contract（Gate実装契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G02
- Gate title: Predictive Family Recomposition and Compatibility（Predictive再構成・互換性）
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
current Predictive workspaceをSetup/Train/Predict/Metrics/Explainability/Model Managementへ再配置し、既存設定項目とgenerated spec/execution semanticsの完全互換を成立させる。

### PASS後に後続Gateが利用できる成果
ユーザーとG05が、新navigation下でもcurrent Predictive capabilityがsemantically unchangedで利用できることへ依存できる。

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
- AC-G02-001: Predictiveの6 Navigation Stageすべてへ到達でき、canonical routeを使用する。
- AC-G02-002: 現行visible Predictive controlをすべて保持し、単なる再配置を除いてinput semantics/defaultを変更しない。
- AC-G02-003: 同等inputに対するgenerated `predictive-analysis-spec/1`のhidden/default semanticsを変更しない。
- AC-G02-004: Train actionは既存split/prepare/train/evaluate/(explain) workflowを引き続き起動し、Navigation StageをExecution Stageへ1対1 mappingしない。
- AC-G02-005: Predict Stageではstandalone scoringを導入せず、利用可能な既存prediction-bearing output/artifact/resultだけを表示し、存在しない場合はdeterministicにその旨を示す。
- AC-G02-006: Metricsは既存evaluation/error-analysis semanticsを表示し、Explainabilityはpredictive-not-causalのwarning/meaningを維持する。
- AC-G02-007: E5のModel Managementはread-onlyなfitted-model/model-card/artifact/lineage scopeとする。
- AC-G02-008: active page session中のFamily/Stage切替で、保護対象の未保存Predictive form値を破棄しない。
- AC-G02-009: 既存Predictive regression testと関連full suiteがPASSする。

## 3. Execution Mode の決定

Mode: `WORK_PACKAGE`。

Operator / Planning担当は`06_G02_P00_work_package_plan.md`と計画済みPxxを用いてPackage分解・依存関係・統合順序を管理する。ただしPackage Coding Agentへ渡すnormative inputは**assigned Pxxのみ**とし、06 / P00 / 他Pxxを併読させてscopeや仕様を再合成させてはならない。Package completionはGate PASSを意味しない。

## 4. 必須の実装semantics

実装は、保護対象upstream contractの意味を変えずにGate目的を成立させなければならない（MUST）。このGateで明示的に必要としない限り、現在のanalysis spec、execution plan、result schema、algorithmを保持するadditive/refactoring変更を優先する。

## 5. 許可されるscope

- Predictiveの6つのStage surface
- 既存config fieldの保持
- split/train/eval/explain workflowの保持
- predictionを含むartifact/resultの参照
- metrics/explanation/model-cardの参照surface
- compatibility test

## 6. 明示的な禁止scope

- LightGBM
- new standalone scoring execution/API
- new model registry CRUD/deployment
- predictive-analysis-spec schema change
- hidden preprocessing/model default change

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

- AC-G02-001について自動テストevidenceを実装する: Predictiveの6 Navigation Stageすべてへ到達でき、canonical routeを使用する。
- AC-G02-002について自動テストevidenceを実装する: 現行visible Predictive controlをすべて保持し、単なる再配置を除いてinput semantics/defaultを変更しない。
- AC-G02-003について自動テストevidenceを実装する: 同等inputに対するgenerated `predictive-analysis-spec/1`のhidden/default semanticsを変更しない。
- AC-G02-004について自動テストevidenceを実装する: Train actionは既存split/prepare/train/evaluate/(explain) workflowを引き続き起動し、Navigation StageをExecution Stageへ1対1 mappingしない。
- AC-G02-005について自動テストevidenceを実装する: Predict Stageではstandalone scoringを導入せず、利用可能な既存prediction-bearing output/artifact/resultだけを表示し、存在しない場合はdeterministicにその旨を示す。
- AC-G02-006について自動テストevidenceを実装する: Metricsは既存evaluation/error-analysis semanticsを表示し、Explainabilityはpredictive-not-causalのwarning/meaningを維持する。
- AC-G02-007について自動テストevidenceを実装する: E5のModel Managementはread-onlyなfitted-model/model-card/artifact/lineage scopeとする。
- AC-G02-008について自動テストevidenceを実装する: active page session中のFamily/Stage切替で、保護対象の未保存Predictive form値を破棄しない。
- AC-G02-009について自動テストevidenceを実装する: 既存Predictive regression testと関連full suiteがPASSする。

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
