# Ariadne ENH-E5 G00 テスト指示書 — Gate Verification Contract（Gate検証契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G00
- Planning baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- Gate title: Family / Navigation Stage Domain Contract（Family / Navigation Stageドメイン契約）
- 検証契約状態: **DRAFT_FOR_REVIEW**（レビュー前ドラフト）


## 0. 検証時の参照ポリシー — 単一normative verification contract

本GateのAcceptance / verification semanticsについて、**本07文書を唯一のnormative authority**とする。

Test / Audit Agentは、本07だけから「何を観測するか」「何をPASS/FAILとするか」「何を禁止するか」を判断する（MUST）。

### 0.1 規範的仕様として参照してはならないもの
Acceptance Criteriaを補完・修正する目的で、06、Pxx、00〜30、ADR、Gate decomposition、他Gate文書、過去Enhancement、issue、commit message、外部Webを参照してはならない（MUST NOT）。

### 0.2 Evidenceとして参照してよいもの
- Implementation Completion Report: Fixed Trial Candidate identity取得
- repository state/diff: 実際のtest target確認
- source code / automated tests / runtime output: evidence取得
- freeze済み本07内に具体的に列挙されたprotected contract identity/evidence

これらはAcceptance Criteriaを追加・変更するauthorityではない。

### 0.3 Repositoryの扱い
repositoryから観測方法・test command・implementation factを発見してよいが、期待仕様を発見してはならない。

### 0.4 Contract ambiguity
本07だけではAcceptance Criteriaの意味を一意に決定できない場合、06や上流資料を読んで推測せず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。

### 0.5 Freeze condition
Test Agentが本07以外の設計文書を読まなければPASS/FAILを判定できない場合、本07を`FROZEN`にしてはならない。

## 1. Acceptance の権威情報

freeze後は、この07をAcceptance Criteriaの権威情報とする。Package完了、Coding self-check、`READY_FOR_TEST`はacceptance evidenceではない。

## 2. Gate目的 / acceptance claim

FamilyとNavigation Stageのapplication contractをExecution Stageから独立して成立させ、capability-owned canonical stage catalogとread APIを提供する。

PASS後にdownstreamが依存可能になるcontract:
G01以降が、stable Family ID / stage ID / order / default Stage / catalog APIへ依存できる。

## 3. 検証時に有効な前提

- test対象は、正確なFixed Trial Candidateである。
- Navigation StageとExecution Stageは別概念である。
- このGateが明示的に変更しない限り、既存analytical algorithm/persistenceはregression保護対象である。
- deferred/out-of-scope featureを偶発的に実装してはならない。
- environment/prerequisiteにより観測不能な場合は`BLOCKED`とし、preflight失敗を自動的にproduct `FAIL`へ変換しない。

## 4. 検証入力

必須:
- current Trialのimplementation completion report
- Fixed Trial Candidate SHA
- repository status/diff
- 該当する場合はPackage checkpoint chain
- 本07へfreeze時に列挙されたprotected regression identity/evidence

identityが欠落または曖昧な場合は`BLOCKED_CANDIDATE_IDENTITY`とする。

### Existing / current semantics の比較基準

本07で「existing」「current」「既存」と記載する挙動・control・schema・operationは、原則として本書metadataの`Planning baseline SHA`で観測できるproduct factを比較基準とする。先行Gateが意図的に変更した範囲は、FROZEN時に本07へ具体的に転記されたprotected contract/evidenceを優先する。

Test Agentはbaseline checkout/source/testsを**evidence取得のため**に観測してよいが、そこから新しいAcceptance Criteriaを導出してはならない。baselineとcandidateの差が本07だけでは許容変更か判定できない場合は、06や設計書を読んで推測せず`BLOCKED_CONTRACT_AMBIGUITY`とする。

## 4.1 FROZEN時のexpected canonical catalog

FROZEN版07には、expected catalogを以下の一意な値として保持する。DRAFT段階でHuman Architecture Reviewにより変更された場合は、本節も同時amendする。Test Agentが06/ADRを読んで期待値を補完してはならない。

- Family order: `EXPLORATORY -> PREDICTIVE -> CAUSAL`
- Family slug: `exploratory`, `predictive`, `causal`
- proposed defaults: Exploratory=`profile`, Predictive=`setup`, Causal=`setup`
- Exploratory stages: `profile`, `data-quality`, `distribution`, `relationships`, `comparison`, `findings`
- Predictive stages: `setup`, `train`, `predict`, `metrics`, `explainability`, `model-management`
- Causal stages: `setup`, `discovery`, `identification`, `estimation`, `effects`, `diagnostics`, `sensitivity`
- target read interface: `GET /api/v1/navigation/analysis`
- target response schema: `analysis-navigation/1`

Test AgentはFamily/Stage order、default、slug、schemaを上記値と直接比較する。FROZEN版に`proposed`/未承認表現が残っている場合は`BLOCKED_CONTRACT_AMBIGUITY`とする。

## 5. Candidate identity audit — 最初に必ず実行

1. 意図したcandidateをcheckout/観測する;
2. `git rev-parse HEAD`を記録する;
3. `git status --short`を記録する;
4. test対象repository stateとFixed Trial Candidate SHAを比較する;
5. 異なる場合はdiffをauditし、documentation-only/non-semanticであることを証明する。証明できなければ状況に応じてBLOCKED/FAILとする。

## 6. Acceptance Criteria（受入基準）

| AC | 基準 | レベル | 必要evidence |
|---|---|---|---|
| AC-G00-001 | Family identityとして既存AnalysisFamily値EXPLORATORY/CAUSAL/PREDICTIVEを用いる。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-002 | Navigation descriptor typeは、execution StageType/StageDefinition/StageExecutionから構造上・semantics上独立している。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-003 | 各capabilityが自身のStage ID、label、order、default Stageを正確に所有する。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-004 | Generic aggregationはduplicate Family/Stage、空Stage list、不正default Stageをrejectする。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-005 | `GET /api/v1/navigation/analysis`が3 Familyすべてについてdeterministicな`analysis-navigation/1` schemaを返す。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-006 | DB migrationまたはnavigation-state persistenceを導入しない。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-007 | 既存workflow/execution testがgreenを維持する。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G00-008 | CLI/library/backend use case/runtime executionがNavigation Stageを必須inputとして要求しない。 | 必須（Mandatory） | direct-call regression / signature dependency audit |
| AC-G00-009 | Navigation StageとExecution Stageの1:1 mappingを要求するcontract/dependencyを導入していない。 | 必須（Mandatory） | code dependency audit + focused test |
| AC-G00-010 | 既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family enum/fieldを導入していない。 | 必須（Mandatory） | schema/type/code audit |
| AC-G00-011 | AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加していない。 | 必須（Mandatory） | schema/domain/runtime dependency audit |

Gate PASSには、すべてのMandatory ACがPASSしなければならない。

## 7. Test Item 計画

- `001_candidate_identity` — candidate/repository-state audit
- 各AC clusterをカバーする1つ以上のfocused item
- protected regression item
- transition-debt audit item
- `999_gate_decision` — 最終Gate Decision専用

各test itemにcommand/input、observed output、evidence path、PASS/FAIL/BLOCKED結果を記録する。

## 8. 保護対象regression

current diffが影響し得る、過去のfinal-PASS Gate contractをすべて検証する。影響があるのに明示的なregression itemがない場合、それ自体をverification defectとする。

## 9. Transition Debt audit

このGateで想定するOPEN debtは`NONE`。文書化されていない一時的authority/exceptionが導入されていないことを確認する。

## 10. Test / Audit Agent の禁止作業

以下を変更してはならない（MUST NOT）:
- production code
- automated test code
- migration/dependency定義
- Package実装
- Acceptance Criteria

## 11. Evidence 要件

Evidenceは再現可能で、正確なcandidate identityに紐付いていなければならない。自動assertionが実用的な箇所では、screenshot/manual observationはautomationの補足には使えるが代替にはできない。

## 12. PASS の意味

PASSとは、Fixed Trial CandidateについてこのGateのsemantic claimが成立し、すべてのmandatory ACとprotected regressionがPASSし、未承認scope/migration/debtが存在せず、evidence identityをaudit可能であることを意味する。

FAILはproduct/contract挙動が有効なACに違反していることを意味する。BLOCKEDはprerequisite/candidate/contractの曖昧さが残り、acceptanceを判定できないことを意味する。
