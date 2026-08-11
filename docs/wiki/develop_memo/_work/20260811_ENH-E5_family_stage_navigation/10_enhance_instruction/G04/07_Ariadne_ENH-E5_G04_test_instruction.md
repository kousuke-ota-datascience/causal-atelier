# Ariadne ENH-E5 G04 テスト指示書 — Gate Verification Contract（Gate検証契約）

文書区分: Primary Execution Contract（主要実行契約）
自己完結性: MUST（必須）

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: G04
- Planning baseline SHA: `46122c68333df03680b97c253a7b5d32bf9393e7`
- Gate title: Exploratory Family Recomposition
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

current Explore & Visualize capabilityをProfile/Data Quality/Distribution/Relationships/Comparison/Findingsへ再配置し、visualizationをanalytical Stageではなく各Stageの表現手段として位置づける。

PASS後にdownstreamが依存可能になるcontract:
ユーザーとG05が、EDAを探索観点別にnavigationしつつ既存exploratory resultsを失わず利用できる。

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

## 5. Candidate identity audit — 最初に必ず実行

1. 意図したcandidateをcheckout/観測する;
2. `git rev-parse HEAD`を記録する;
3. `git status --short`を記録する;
4. test対象repository stateとFixed Trial Candidate SHAを比較する;
5. 異なる場合はdiffをauditし、documentation-only/non-semanticであることを証明する。証明できなければ状況に応じてBLOCKED/FAILとする。

## 6. Acceptance Criteria（受入基準）

| AC | 基準 | レベル | 必要evidence |
|---|---|---|---|
| AC-G04-001 | Exploratoryの6 Navigation Stageすべてへ到達でき、canonical routeを使用する。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-002 | Profileは既存dataset/profile contextを表示し、explorationに必要なAnalysis View accessを保持する。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-003 | Data Qualityは既存data/profile capabilityから導出可能なquality factだけを表示し、未support metricを捏造しない。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-004 | Distribution、Relationships、Comparisonは既存exploratory operationをanalytical semanticsを変えずにmappingする。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-005 | Visualization/Chart controlは関連Stage内部へ配置し、VisualizationというNavigation Stageは設けない。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-006 | Findingsは既存saved exploratory Result/annotation/linkage semanticsを再利用し、新規persistent Findings modelは作成しない。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-007 | Exploratory outputでは、該当箇所のnon-causal interpretation warningを維持する。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |
| AC-G04-008 | 既存exploratory regression testがPASSする。 | 必須（Mandatory） | Fixed Trial Candidateのbehavior/code/test evidence |

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
