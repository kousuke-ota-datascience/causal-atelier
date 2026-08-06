# Ariadne ENH-E1a 再実装ならびに再テスト指示書

- 文書ID: `ARIADNE-ENH-E1A-IMPLEMENTATION-INSTRUCTION-20260806`
- 作成日: 2026-08-06
- 文書状態: 実装開始可能
- エンハンス計画名: `ariadne_ENH-E1a`
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 開始元ブランチ: `prototype/ariadne_mvp_e1_scientific_enhance`
- 作業ブランチ推奨名: `prototype/ariadne_mvp_e1a_corrective_enhance`
- 先行計画: `ENH-E1`
- 対象監査報告書: `07_ariadne_ENH-E1_実施状況監査報告書.md`
- 要件正本: `../10_Revised_requirements_definition_documents/10_要件定義.md`
- 実装対象外: ENH-E2以降の機能、主要Entity追加、旧システム互換対応

> **本作業はENH-E1の未達事項および欠陥を閉じる是正実装である。新規プロダクト構想を追加してはならない。**
>
> **要件の唯一の正本は`../10_Revised_requirements_definition_documents/10_要件定義.md`である。実装都合から要件を弱めてはならない。**
>
> **監査IDごとに、実装、Behavior Test、受入証跡を揃えなければ完了としてはならない。**

---

## 1. 目的

### 1.1. ariadne_ENH-E1aの位置付け

`ariadne_ENH-E1a`は、ENH-E1で実装された中核構造を維持したまま、監査報告書で未達または不具合と判定された事項を是正するための補完リリースである。

ENH-E1の再設計または全面的な作り直しではない。

### 1.2. 最上位目標

以下をすべて達成する。

1. ENH-E1のMUST要件をBehavior Testで検証可能な状態にする
2. 科学的負結果と技術的失敗を分離する
3. Estimator compatibility gateを実際のデータ型に対して機能させる
4. Identification判定の科学的妥当性を改善する
5. Analysis Modeの未達要件を実装する
6. Scientific Benchmarkを計画どおり完成させる
7. Browser E2EでE2E-04〜06を完走する
8. 要件―設計―実装―Test―結果のトレーサビリティを完成させる

### 1.3. 完了状態

以下の状態のみを`COMPLETE`とする。

```text
全監査IDがCLOSED
AND 全MUST要件にBehavior Testが存在
AND Scientific Benchmark GateがPASS
AND Browser E2E E2E-04〜06がPASS
AND Full RegressionがPASS
AND Completion Reportに完全な証跡が存在
```

---

## 2. 正本、優先順位および変更統制

### 2.1. 参照優先順位

不一致がある場合は、以下の順で扱う。

1. `../10_Revised_requirements_definition_documents/10_要件定義.md`
2. 承認済み改定設計書
3. `06_Ariadne_ENH-E1_実装指示書.md`
4. `07_ariadne_ENH-E1_実施状況監査報告書.md`
5. 本指示書
6. 現行ソースコード
7. 現行テスト

本指示書は要件を変更せず、監査で明らかになった未達を閉じる実装手順と受入条件を具体化する。

### 2.2. 不一致を発見した場合

要件と設計が矛盾し、実装判断が一意に定まらない場合は、推測で補完してはならない。

```text
該当Work Packageを停止
→ 監査ID、要件ID、設計節、影響範囲を記録
→ 最小の設計修正案を提示
→ 承認後に設計文書を更新
→ トレーサビリティを再確認
→ 実装を再開
```

他の独立Work Packageは継続してよい。

### 2.3. 禁止事項

以下を禁止する。

- 要件をテストが通る範囲へ弱める
- 監査指摘を「既存挙動」として正当化する
- 新しい主要Entityまたは専用Tableを追加する
- Causal Question、Identification、Refutation、Sensitivityを独立Entity化する
- Run／Attemptを復活させる
- 汎用Workflow Engineを追加する
- 汎用Lineage Relation Tableを追加する
- Comparison Tableを追加する
- CPDAG／PAGを暗黙にDAGへ変換する
- `NOT_IDENTIFIED`、Eligibility `FAIL`、`FRAGILE`等を技術的例外へ変換する
- Refutation成功を識別仮定の証明として表示する
- External Library型をProduct Domainへ漏らす
- 未知FieldをSilent Ignoreする
- Browser E2EをFrontend Contract Testで代替する
- Benchmark scenarioをテスト件数だけで完了扱いする
- 失敗するテストをskip、xfailまたはmarker除外して完了扱いする
- ENH-E2以降のEstimator、CATE、DML、IV、DiD等を混入させる

---

## 3. 作業開始手順

### 3.1. RepositoryおよびBaseline固定

1. 開始元ブランチを取得する
2. 作業開始時HEADの完全なCommit SHAを記録する
3. 作業ブランチを作成する
4. Working Treeがcleanであることを確認する
5. Python 3.12環境を構築する
6. 依存関係を同期する
7. 現行テストを実行しBaselineを保存する
8. 現行Migration headを記録する
9. Browser E2E実行環境の成立性を先に確認する

推奨コマンド:

```bash
git switch prototype/ariadne_mvp_e1_scientific_enhance
git pull --ff-only
git rev-parse HEAD
git status --short

git switch -c prototype/ariadne_mvp_e1a_corrective_enhance

uv sync --all-groups --python 3.12
uv run pytest -q
uv run pytest -q -m scientific_benchmark
python -m compileall -q src tests
git diff --check
```

環境上の理由で一部コマンドを変更した場合、実際に使用した完全なコマンドをCompletion Reportへ記録する。

### 3.2. Baseline Report

実装開始前に以下を記録する。

- Baseline Commit
- Branch
- OS／Architecture
- Python Version
- Package Versions
- Migration Head
- Unit／Component／API／Worker Test結果
- Scientific Benchmark結果
- Browser E2Eの実行可否
- 既知の失敗
- 既知のskip

Baseline失敗をE1a変更による失敗と混同してはならない。

---

## 4. 監査IDとWork Packageの対応

| Work Package | 対象監査ID | 主対象 |
|---|---|---|
| WP-0 | 全件 | Baseline、要件・設計Gate、作業計画 |
| WP-1 | AUD-E1-002 | FR-054 Estimator compatibility |
| WP-2 | AUD-E1-004 | Eligibilityと技術状態の分離 |
| WP-3 | AUD-E1-005〜007 | Collider、RANDOMIZED、Status優先順位 |
| WP-4 | AUD-E1-008〜009 | Analysis Mode、探索後推論警告 |
| WP-5 | AUD-E1-003 | Scientific Benchmark完成 |
| WP-6 | AUD-E1-001 | Browser E2E E2E-04〜06 |
| WP-7 | AUD-E1-010 | Full Regression、Traceability、Completion Report |

依存順序:

```text
WP-0
→ WP-1
→ WP-2
→ WP-3
→ WP-4
→ WP-5
→ WP-6
→ WP-7
```

WP-1〜WP-4は、相互に独立する範囲では並行実施してよい。ただし、各WPの受入条件未達のままWP-7へ進んではならない。

---

## 5. WP-0 Baseline／Requirements Gate

### 5.1. 目的

E1aの開始点、正本および監査対象を固定する。

### 5.2. 必須確認

- `07_ariadne_ENH-E1_実施状況監査報告書.md`の監査IDが全件存在する
- 要件正本が変更されていない
- 7 Entity方針が維持されている
- 現行Snapshot schemaとAPI contractを確認した
- Data Eligibility payloadの現行構造を確認した
- Dataset Versionが保持するschema／column metadataを確認した
- Existing Testの要件ID markerまたは対応表を確認した
- Browser E2E runnerの有無を確認した

### 5.3. 成果物

- Baseline記録
- 監査ID別の変更対象ファイル一覧
- 監査ID別のTest追加計画
- 設計上の不明点一覧

### 5.4. 完了条件

- 全監査IDがいずれかのWPに割り当てられている
- 要件IDと監査IDが対応している
- 実装者が独自判断すべき未決事項が残っていない
- Baseline Test結果が保存されている

---

## 6. WP-1 FR-054 Estimator Compatibility Gate

### 6.1. 対象

- 監査ID: `AUD-E1-002`
- 要件ID: `FR-054`
- 主な変更候補:
  - `src/ariadne/product/application/scientific_validation_service.py`
  - `src/ariadne/scientific/identification/adapter.py`
  - Data Eligibility Resultのpayload生成箇所
  - Estimation submissionのvalidation test
  - API error contract test

### 6.2. 必須実装

Estimator受付時に以下をすべて検証する。

1. Estimand
2. Treatment Type
3. Outcome Type
4. Identification Strategy
5. Estimator固有Parameter
6. 必要なAdjustment契約
7. 必要なOverlap／Diagnostics前提

少なくともFR-054の4軸は必須である。

### 6.3. 型の正規化

Product Domainへpandas dtype、NumPy dtypeまたは外部Library型を保存してはならない。

Scientific Adapterまたは同等の境界で、分析上の型をProduct固有の正規化値へ変換する。

E1で最低限必要な正規化値:

```text
Treatment Type:
- BINARY
- UNSUPPORTED

Outcome Type:
- CONTINUOUS
- BINARY
- UNSUPPORTED
```

追加の型をENH-E2機能として実装してはならない。

Data Eligibility Resultには、少なくとも以下の判定根拠を機械可読に保存する。

```json
{
  "inferred_types": {
    "treatment": {
      "type": "BINARY",
      "evidence": {}
    },
    "outcome": {
      "type": "CONTINUOUS",
      "evidence": {}
    }
  }
}
```

既存payload構造と整合する別表現を使用してよいが、型名と根拠を再利用可能な形で保存すること。

### 6.4. Gateの実行位置

推奨処理順序:

```text
Identification
→ Data Eligibilityで分析上の型を判定・保存
→ Estimation受付
→ Identification ResultとEligibility Resultを取得
→ ESTIMATOR_CAPABILITIESと照合
→ 不一致なら受付拒否
→ 一致した場合のみExecution作成
```

同じ型判定をAPI、Worker、CLIで別々に再実装してはならない。共通Serviceまたは共通Validatorへ集約する。

### 6.5. エラー要件

不一致は技術的Worker失敗ではなく、受付時のScientific Contract違反として拒否する。

Machine-readable error codeを使用する。

最低限、以下を区別する。

```text
ESTIMATOR_ESTIMAND_INCOMPATIBLE
ESTIMATOR_TREATMENT_TYPE_INCOMPATIBLE
ESTIMATOR_OUTCOME_TYPE_INCOMPATIBLE
ESTIMATOR_IDENTIFICATION_STRATEGY_INCOMPATIBLE
ESTIMATOR_PARAMETER_UNSUPPORTED
```

既存のエラー命名規約がある場合は、それに従って同等の識別可能性を保証する。

### 6.6. 必須Test

Registry shape testだけでは不十分である。以下のBehavior Testを追加する。

| Case | 期待結果 |
|---|---|
| 対応Estimand／Treatment Type／Outcome Type／Strategy | Estimation受付成功 |
| 非対応Estimand | 受付拒否 |
| 非対応Treatment Type | 受付拒否 |
| 非対応Outcome Type | 受付拒否 |
| 非対応Strategy | 受付拒否 |
| 未知Estimator | 受付拒否 |
| 未知Parameter | 受付拒否 |
| 同一Identification Resultを互換な複数Estimatorで使用 | 受付成功 |
| API／CLIで同一不一致 | 同一意味のエラー |

### 6.7. 完了条件

- FR-054の4軸を実データ由来の型に対して検証している
- 不一致がWorkerへ到達しない
- Capability Registryの未使用Fieldを放置していない
- Behavior Testが要件IDと紐付いている
- `AUD-E1-002`がCLOSEDである

---

## 7. WP-2 Data Eligibilityと技術状態の分離

### 7.1. 対象

- 監査ID: `AUD-E1-004`
- 要件ID: `FR-050`、`FR-064`、`FR-065`
- 主な変更候補:
  - `src/ariadne/scientific/identification/adapter.py`
  - `src/ariadne/interfaces/worker/execution_processor.py`
  - Identification／Eligibility component test
  - Worker integration test

### 7.2. 必須実装

Eligibility checkは、失敗した検査の後に、その検査が成立することを前提とした処理を実行してはならない。

処理を依存関係順に分離する。

```text
Required Column Check
→ Type Compatibility
→ Treatment Domain Check
→ Constant／Missingness／Sample Size
→ Numeric-only Diagnostics
→ Propensity／Overlap Diagnostics
```

前提を満たさない場合は、依存する後続checkを以下のいずれかとして記録する。

- `NOT_APPLICABLE`
- `SKIPPED_DUE_TO_PREREQUISITE`
- 既存status体系に適合する明示的な根拠付き未実行

Silent Skipは禁止する。

総合Statusの優先順位は以下を維持する。

```text
FAIL > WARN > PASS
```

### 7.3. 技術状態

以下を保証する。

```text
科学的／データ適格性の負結果
→ Result保存成功
→ Execution Status = SUCCEEDED
```

以下の場合のみ技術的`FAILED`とする。

- Dataset Artifactを読めない
- Result永続化に失敗した
- 内部不変条件違反
- 未処理の実装バグ
- Infrastructure障害

### 7.4. 必須Test

| Case | Identification Result | Eligibility Result | Execution |
|---|---|---|---|
| 文字列Treatment | Result保存 | `FAIL` | `SUCCEEDED` |
| 非数値Outcome | Result保存 | `FAIL` | `SUCCEEDED` |
| 必須列欠落 | 非識別理由保存 | `FAIL` | `SUCCEEDED` |
| Treatment armが1種類 | Result保存 | `FAIL` | `SUCCEEDED` |
| 小標本 | Result保存 | `WARN`または`FAIL` | `SUCCEEDED` |
| Propensity推定不能 | Result保存 | 根拠付き`WARN`または`FAIL` | `SUCCEEDED` |
| Artifact読取不能 | 未保存または失敗証跡 | 該当なし | `FAILED` |

### 7.5. 完了条件

- 型不一致で例外が送出されない
- Eligibility Resultが必ず保存される
- 負結果と技術的失敗が分離されている
- EstimationがEligibility `FAIL`を拒否する
- `AUD-E1-004`がCLOSEDである

---

## 8. WP-3 Identification科学判定の是正

### 8.1. 対象

- 監査ID: `AUD-E1-005`、`AUD-E1-006`、`AUD-E1-007`
- 要件ID: `FR-038`、`FR-039`、`FR-064`〜`FR-067`
- 主な変更候補:
  - `src/ariadne/scientific/identification/adapter.py`
  - Graph semantics utility
  - Identification benchmark／component test

### 8.2. Collider判定

次の実装を禁止する。

```text
親が2つ以上存在する
→ 対象因果効果に対するColliderと断定
```

ColliderはTreatment–Outcome間の対象経路に対する役割として判定する。

以下のいずれかの方法を使用する。

1. path-relativeなCollider／descendant-of-collider判定
2. d-separationまたは同等のBack-door criterion判定
3. ancestral moral graph等、科学的に同値な判定

既存のBack-door blocking判定を利用してよいが、`COLLIDER_ADJUSTMENT`という理由を付与する場合は、そのノードが対象経路でColliderまたはColliderの子孫として作用する根拠を保存する。

判定不能な場合に誤ってColliderと断定してはならない。より一般的な`OPEN_BACKDOOR_PATH`等の理由を使用する。

### 8.3. Collider必須Test

最低限、以下を独立Testとして実装する。

| Graph／Adjustment | 期待 |
|---|---|
| `T -> C <- Y`で`C`を調整 | 拒否または警告 |
| Collider descendantを調整 | path openingを検出 |
| 親が2つあるが対象T–Y経路上のColliderではない変数 | Colliderとして誤拒否しない |
| 非Collider confounderを調整 | 有効 |
| Post-treatment mediatorを調整 | `POST_TREATMENT_ADJUSTMENT` |
| 有効Adjustment Setで全Back-door pathをblock | `IDENTIFIED` |

### 8.4. RANDOMIZED strategy

Adjustment Setが非空であることのみを理由に`NOT_IDENTIFIED`としてはならない。

E1aでは以下を是正方針とする。

- Randomization assumptionが宣言されている場合、識別はRandomizationに基づく
- pre-treatment covariate adjustmentを許可する
- Treatment、Outcomeの混入を拒否する
- post-treatment variableを拒否する
- Dataset columnおよびGraph nodeとの整合性を検証する
- Estimator側の`required_adjustment`契約はWP-1で検証する
- 調整の有無をIdentification成立そのものと混同しない

`difference_in_means`のようにAdjustmentを使用しないEstimatorは、Estimator compatibility gateで不一致を拒否する。Identification段階でRandomized design全体を非識別にしてはならない。

### 8.5. Status優先順位

Status決定を理由収集後の明示的な優先順位関数へ分離する。

推奨優先順位:

```text
確定的入力不整合
または DAG cycle
または 必須対象不在
→ NOT_IDENTIFIED

DAGで決定的な識別条件違反
→ NOT_IDENTIFIED

CPDAG／PAGで、入力は整合するが方向不確実性により自動判定不能
→ REQUIRES_REVIEW

全必須条件成立
→ IDENTIFIED
```

`REQUIRES_REVIEW`は、明確な入力欠損または確定的違反を上書きしてはならない。

Reasonは失わず、すべてpayloadへ保存する。

### 8.6. Status必須Test

| Case | 期待Status |
|---|---|
| CPDAG + Treatment node不在 | `NOT_IDENTIFIED` |
| PAG + Outcome column不在 | `NOT_IDENTIFIED` |
| CPDAG + 入力整合 + orientationのみ未確定 | `REQUIRES_REVIEW` |
| DAG + cycle | `NOT_IDENTIFIED` |
| DAG + valid back-door | `IDENTIFIED` |
| RANDOMIZED + valid pre-treatment adjustment | `IDENTIFIED` |
| RANDOMIZED + post-treatment adjustment | `NOT_IDENTIFIED` |

### 8.7. 完了条件

- indegree heuristicをCollider判定として使用していない
- Randomized designをAdjustment非空だけで拒否しない
- Status優先順位が独立Testで固定されている
- non-identification reasonとreview reasonを区別できる
- `AUD-E1-005`〜`AUD-E1-007`がCLOSEDである

---

## 9. WP-4 Analysis Modeおよび探索後推論警告

### 9.1. 対象

- 監査ID: `AUD-E1-008`、`AUD-E1-009`
- 要件ID: `FR-060`〜`FR-063`
- 主な変更候補:
  - `src/ariadne/product/domain/analysis_spec.py`
  - `src/ariadne/product/application/execution_service.py`
  - Query／Repository
  - Web API schema
  - Frontend
  - CLI manifest
  - Lineage表示
  - Analysis Mode contract／E2E test

### 9.2. FR-062 改訂Execution

Submitted ExecutionのSnapshotを変更してはならない。

固定済み条件を変更する場合は、新しいExecutionを作成する。

新しい主要EntityまたはTableを追加せず、既存Snapshot、Execution参照またはAnnotationを使用して以下を保存する。

- 基準となるExecution
- 変更理由
- 変更されたdimension
- Actor
- 変更日時またはExecution作成日時
- 旧値と新値を復元可能にする参照

具体的なField名と配置は既存設計との整合を確認して決定する。

Snapshot schemaを変更する場合は、以下を満たす。

- schema version運用方針を明示する
- 旧`causal-analysis-spec/2`の取扱いを明示する
- Unknown Field rejectを維持する
- canonical hash対象を更新する
- API／CLI／UIで同一contractを使用する
- Migrationが必要かを明示する

要件を満たす表現が既存設計に存在しない場合、独断でEntityを追加せず、最小の設計追補を記録してから実装する。

### 9.3. FR-062 必須Behavior

- 既存Executionを直接更新できない
- Revised Execution作成時に基準Executionを参照できる
- 条件差分がある場合、変更理由を必須とする
- 変更理由なしの改訂受付を拒否する
- Lineageまたは詳細画面から基準Executionへ遡れる
- 同一Snapshotを単純再実行する場合と、条件変更を伴う改訂を区別する

### 9.4. FR-063 探索後推論警告

以下の条件をすべて満たす場合、探索後推論警告を生成する。

```text
Analysis Mode = CONFIRMATORY
AND Operation = ESTIMATION
AND 同一Project内
AND 同一Dataset Versionを使用した先行DISCOVERYが存在
```

Graph Versionが先行Discovery Result由来である場合は必ず警告する。

User-defined／Imported Graphであっても、同一Dataset Versionに対する先行Discoveryを利用者が実施済みである場合は警告対象とする。

警告には最低限以下を含める。

```text
warning_code
message
source_discovery_execution_ids
dataset_version_id
rationale
```

推奨warning code:

```text
POST_SELECTION_INFERENCE_RISK
```

### 9.5. 警告の扱い

- 警告はIdentification成立またはEstimation実行を自動的に否定しない
- 警告をScientific Statusと混同しない
- UI、CLI、API responseまたは保存済みSnapshot／Resultから再確認可能にする
- 同じ条件から同じ警告が決定論的に生成される
- 警告を消すために履歴を無視してはならない

### 9.6. 必須Test

| Case | 期待 |
|---|---|
| EXPLORATORY Estimation + 先行Discovery | FR-063警告なし |
| CONFIRMATORY Estimation + 同一Datasetの先行Discovery | 警告あり |
| CONFIRMATORY Estimation + 別DatasetのDiscovery | 警告なし |
| CONFIRMATORY Estimation + Discovery由来Graph | 警告あり |
| 条件変更 + change reasonなし | 受付拒否 |
| 条件変更 + change reasonあり | 新Execution作成 |
| Submitted Executionの更新 | 拒否 |
| API／CLI／UI | 同じwarning semantics |

### 9.7. 完了条件

- FR-062の改訂Executionと変更理由が実装されている
- FR-063の探索後推論警告が実装されている
- Snapshot不変性を維持している
- 専用Behavior TestおよびBrowser E2Eが存在する
- `AUD-E1-008`および`AUD-E1-009`がCLOSEDである

---

## 10. WP-5 Scientific Benchmark完成

### 10.1. 対象

- 監査ID: `AUD-E1-003`
- 要件ID: `NFR-010`、`NFR-011`、`NFR-013`、`NFR-014`
- 主な変更候補:
  - `tests/scientific_benchmarks/`
  - Benchmark scenario manifest
  - Benchmark result serializer
  - CI Artifact設定
  - Scientific package version capture

### 10.2. 必須Scenario

以下を独立scenarioとして実装する。

| Scenario ID | Scenario |
|---|---|
| SB-E1A-001 | Randomized ATE |
| SB-E1A-002 | Observed Confounding |
| SB-E1A-003 | Missing Confounder |
| SB-E1A-004 | Collider Adjustment |
| SB-E1A-005 | Post-treatment Adjustment |
| SB-E1A-006 | Poor Overlap |
| SB-E1A-007 | Placebo |
| SB-E1A-008 | Adjustment Variation |
| SB-E1A-009 | Propensity Clipping |
| SB-E1A-010 | Unresolved CPDAG／PAG |
| SB-E1A-011 | Semi-synthetic ATE／ATT |

既存Testを再利用してよいが、各scenarioを個別に識別できなければならない。

### 10.3. Semi-synthetic Benchmark

Semi-synthetic Benchmarkは以下を満たす。

- Covariate分布は固定された実データ由来または実データ相当の公開fixtureを使用する
- TreatmentおよびOutcomeの生成機構は既知とする
- Ground Truthを計算可能にする
- Test時に外部Networkへ依存しない
- Datasetの出典、ライセンス、前処理を記録する
- 単一seedで合否を判定しない

リポジトリに適切なfixtureが存在しない場合、ライセンス上問題のない小規模fixtureを追加する。無断転載または出典不明データを追加してはならない。

### 10.4. Benchmark出力

実行ごとに構造化結果を出力する。

最低限のschema:

```json
{
  "benchmark_id": "ariadne_ENH-E1a",
  "code_commit": "<full-sha>",
  "environment": {},
  "scenarios": [
    {
      "scenario_id": "SB-E1A-001",
      "scenario": "Randomized ATE",
      "dgp_version": "v1",
      "seed": 1,
      "ground_truth": 0.0,
      "estimate": 0.0,
      "bias": 0.0,
      "rmse": 0.0,
      "ci_coverage": 0.95,
      "expected_status": "IDENTIFIED",
      "actual_status": "IDENTIFIED",
      "runtime_seconds": 0.0,
      "package_versions": {}
    }
  ],
  "gate_result": "PASS"
}
```

該当しないmetricは`null`としてよいが、Field自体をSilentに欠落させてはならない。

### 10.5. Gate

最低限、ENH-E1指示書のGateを満たす。

- Deterministic Status一致率: 100%
- Post-treatment拒否率: 100%
- Non-identification検出率: 100%
- Fixed Poor-overlap検出率: 100%
- Standardized Absolute Bias: 0.10以下
- Empirical 95% CI Coverage: 0.90以上0.98以下
- 単一seedだけで合格判定しない
- Backend Versionを記録する
- Threshold違反時にCIが失敗する

### 10.6. Artifact

Benchmark結果をCI Artifactまたは同等の再取得可能な出力として保存する。

推奨出力先:

```text
test-results/scientific_benchmarks/ariadne_ENH-E1a.json
```

出力先が異なる場合はCompletion Reportへ記録する。

### 10.7. 必須Test

- Scenario manifest completeness
- 全Scenario ID重複なし
- 必須Field completeness
- Seed再現性
- 複数seed集計
- Threshold境界
- Threshold違反時のprocess failure
- Package／backend version記録
- Semi-synthetic fixtureのoffline実行

### 10.8. 完了条件

- 全11scenarioが独立識別可能
- SyntheticとSemi-syntheticの双方が存在
- 構造化Artifactを生成する
- Gate違反でTest／CIが失敗する
- `AUD-E1-003`がCLOSEDである

---

## 11. WP-6 Browser E2Eおよび受入シナリオ

### 11.1. 対象

- 監査ID: `AUD-E1-001`
- 要件ID: E2E-04、E2E-05、E2E-06
- 対象:
  - Frontend
  - Web API
  - Worker
  - PostgreSQL
  - Artifact Store
  - Browser automation runner

### 11.2. 実行環境

HostのFirefox snap制約を完了不能の理由としてはならない。

以下のいずれかで再現可能なBrowser E2E環境を構築する。

- Chromium + Playwright
- Firefox／Chromium + Selenium
- Containerized browser runner
- CIが公式に提供するbrowser runner

推奨は、host固有mount namespaceへ依存しないcontainerized Chromium／Playwrightである。

Browser E2E用依存関係はdev/test scopeに限定する。

### 11.3. E2E-04 Identification-first

Browserから以下を実行する。

1. Dataset Versionを登録する
2. FIXED Graph Versionを選択する
3. Causal QuestionおよびCausal Designを入力する
4. Identification Executionを作成する
5. Identification ResultとData Eligibility Resultを確認する
6. `IDENTIFIED`の場合のみEstimationへ進む
7. 同一Identification Resultを2種類以上の互換Estimatorで使用する
8. Diagnosticsを比較する
9. Refutationを実行する
10. Sensitivityを実行する
11. Annotationへ採用理由、Assumptions、Limitationsを記録する
12. Resultからすべての上流条件へ遡る
13. Analysis Modeおよび必要な警告を確認する

### 11.4. E2E-05 非識別結果

Browserから以下を実行する。

1. 識別不能なGraph／Causal Questionを指定する
2. Identification Executionが技術的に`SUCCEEDED`になることを確認する
3. Identification Resultが`NOT_IDENTIFIED`になることを確認する
4. 非識別理由を確認する
5. 通常Estimationの作成が拒否されることを確認する
6. Result比較およびLineage確認が可能であることを確認する

### 11.5. E2E-06 Graph Provenance

Browserから以下を実行する。

1. Discovery ResultからGraph Versionを作成する
2. Constraint適用Graphを別Versionとして作成する
3. User Editを別Versionとして作成する
4. 各VersionのOrigin、Parent、Source、理由を確認する
5. Algorithm Outputを人為編集結果として表示しないことを確認する
6. CPDAG／PAG endpoint semanticsを表示上も失わないことを確認する

### 11.6. E1a追加Browser Test

以下もBrowserで確認する。

- Estimator Type不一致を送信前または受付時に明示する
- Eligibility `FAIL`を技術的エラー画面として表示しない
- CONFIRMATORY + 先行Discoveryで探索後推論警告を表示する
- Revised Execution作成時に変更理由を要求する
- RANDOMIZED + valid pre-treatment adjustmentを不当に非識別扱いしない

### 11.7. 証跡

各scenarioについて以下を保存する。

- Test command
- Browser／Driver version
- Start／End time
- PASS／FAIL
- Screenshot
- Failure時trace／video／console log
- API／Worker logへの参照
- 作成されたProject／Execution／Result ID

秘密情報、tokenまたは個人情報をArtifactへ含めてはならない。

### 11.8. 完了条件

- E2E-04〜06が実ブラウザでPASSする
- E1a追加Browser TestがPASSする
- skipなし
- host固有手動操作なしで再実行できる
- `AUD-E1-001`がCLOSEDである

---

## 12. WP-7 Full Regression、Traceabilityおよび完了報告

### 12.1. 対象

- 監査ID: `AUD-E1-010`
- 要件ID: `NFR-015`
- 全Work Package

### 12.2. 必須Regression

最低限、以下を実行する。

```bash
uv run pytest -q
uv run pytest -q -m scientific_benchmark
python -m compileall -q src tests
git diff --check
```

加えて、リポジトリ既存手順に従い以下を実行する。

- PostgreSQL contract test
- Migration upgrade
- Migration downgrade
- Migration re-upgrade
- API integration test
- Worker integration test
- CLI contract test
- Frontend contract test
- Browser E2E
- Docker Compose golden path
- Backup／Restore
- Architecture／Import boundary test

### 12.3. skipの扱い

skipが存在する場合、以下をCompletion Reportへ記録する。

- Test名
- skip理由
- 要件への影響
- 完了判定への影響

MUST要件、Browser E2EまたはScientific Benchmarkに対応するTestをskipした状態で`COMPLETE`としてはならない。

### 12.4. Traceability Matrix

以下の列を持つ表を作成する。

| 監査ID | 要件ID | 設計文書・節 | 実装ファイル | Test Case | Test Command | 結果 | Evidence |
|---|---|---|---|---|---|---|---|

最低限、`AUD-E1-001`〜`AUD-E1-010`を全件含める。

「Registryが存在する」等の構造確認だけをBehavior要件の証跡としてはならない。

### 12.5. Completion Report

新規に以下を作成する。

```text
../20_implementation_reports/ENH-E1a_completion_report.md
```

過去の`ENH-E1_completion_report.md`を履歴抹消目的で上書きしてはならない。

Completion Reportには以下を含める。

- Baseline Commit
- Completed Commit
- Branch
- Changed Files
- Requirement／Audit Closure Matrix
- Work Package別Completion Report
- Test Commands
- Test Results
- Browser／Driver Versions
- Benchmark Artifact Path
- Benchmark Summary
- Migration Version
- Environment
- Package Versions
- Known Limitations
- Remaining Issues
- Final Decision

### 12.6. 最終判定

以下をすべて満たす場合のみ`COMPLETE`とする。

1. `AUD-E1-001`〜`AUD-E1-010`が全件CLOSED
2. 全MUST要件を実装している
3. 要件IDとBehavior Testの対応が存在する
4. E2E-04〜E2E-06が成功する
5. E1a追加Browser Testが成功する
6. Scientific Benchmarkが成功する
7. SyntheticとSemi-synthetic Benchmarkが存在する
8. Benchmark Artifactが保存される
9. 既存MVP Golden Pathが成功する
10. 新しい主要Entityを追加していない
11. CPDAG／PAGを暗黙DAG化していない
12. 科学的負結果を技術的失敗として扱っていない
13. Refutationを仮定の証明として表示していない
14. 実装から要件定義書を変更していない
15. 要件、設計、実装、Testおよび結果のトレーサビリティが成立する
16. Completed Commitが記録されている
17. MUST要件に関するskipがない

1項目でも満たさない場合は`INCOMPLETE`とする。

---

## 13. Test設計原則

### 13.1. Test Pyramid

以下を区別する。

- Unit: 型分類、Status優先順位、Graph判定utility
- Component: Scientific Adapter、Validation Service
- API: 受付拒否、Error Code、Snapshot
- Worker: 科学的負結果と技術状態
- CLI: APIと同一contract
- Frontend Contract: 表示要素とpayload
- Browser E2E: 実利用経路
- Scientific Benchmark: 統計的受入

### 13.2. False-positive Testの禁止

次のようなTestを要件証跡としてはならない。

- Registryにkeyが存在するだけ
- 関数が例外なく呼べるだけ
- DOMに文字列が存在するだけ
- Scenario名がTest名に含まれるだけ
- 単一seedで推定値が近いだけ
- Mockが期待値を返すだけで実装経路を通らないTest

### 13.3. Regression Test

各監査指摘について、修正前コードでは失敗し、修正後コードで成功するTestを追加する。

可能な限り以下の順で実施する。

```text
Failing Test追加
→ 失敗を確認
→ 最小実装
→ Test成功
→ 関連Regression実行
```

---

## 14. Work Package完了報告形式

各WP完了時、以下の形式で記録する。

```markdown
## WP-X Completion Report

### Requirements

- FR-xxx
- NFR-xxx

### Audit Findings

- AUD-E1-xxx

### Changed Files

- `path/to/file.py`

### Design Compliance

- 対応する設計書:
- 対応する節:
- 適合内容:
- Entity追加: None

### Tests

- Test Case:
- Command:
- Result:
- Evidence:

### Scientific Rationale

- 判定根拠:
- 反対仮説:
- 採用しなかった実装:
- 理由:

### Deviations

- None

### Unresolved Issues

- None

### Closure Decision

- CLOSED / OPEN
```

監査IDが`OPEN`のまま次の依存WPへ進んではならない。

---

## 15. Coding Agentへの最終指示

1. 最初に監査報告書と要件正本を読むこと
2. 現行コードを正本とみなさないこと
3. 監査ID単位でFailing Testを作成すること
4. 実装変更を最小化すること
5. 科学的判定理由をmachine-readableに保存すること
6. UI、CLI、API、Workerで同一の科学的意味を使用すること
7. 環境制約を理由にMUST Testを省略しないこと
8. Browser E2E環境を再現可能に構築すること
9. Benchmarkを単一seedまたはテスト件数で評価しないこと
10. Completion Reportに完全なCommit SHAと実行証跡を残すこと
11. 不明な仕様を独断で補完しないこと
12. 全完了条件を満たすまで`COMPLETE`と報告しないこと

---

## 16. 最終成果物

E1a完了時に最低限、以下が存在すること。

```text
docs/wiki/develop_memo/_work/20260806_enhance_plan/
├── 00_enhance_plan_documents/
│   ├── 07_ariadne_ENH-E1_実施状況監査報告書.md
│   └── 08_ariadne_ENH-E1a_再実装ならびに再テスト指示書.md
├── 20_implementation_reports/
│   └── ENH-E1a_completion_report.md
└── 30_test_evidence/
    ├── scientific_benchmarks/
    │   └── ariadne_ENH-E1a.json
    └── browser_e2e/
        ├── E2E-04/
        ├── E2E-05/
        └── E2E-06/
```

実行環境上、Test Evidenceをリポジトリへ格納せずCI Artifactとして保存する場合、`30_test_evidence/`にはArtifact URL、Run ID、Commit SHAおよびchecksumを記載したmanifestを置くこと。
