# Ariadne ENH-E1 実装指示書

- 作成日: 2026-08-06
- 文書状態: 実装開始可能
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 対象ブランチ: `prototype/ariadne_mvp`
- 基準コミット: `f5e6e5ad5774a3951af5af65b724c4b53aada56a`
- 対象要件: `ENH-E1`
- 実装対象外: ENH-E2以降

> **`../10_Revised_requirements_definition_documents/10_要件定義.md`を唯一の要件正本として実装すること。**
>
> **実装、既存コード、テスト結果または実装上の都合から要件定義書を更新してはならない。**

## 1. 実装開始条件

### 1.1. 必須文書

以下が承認済みであること。

1. `01_Enhance構想・要件改定計画.md`
2. `02_Enhance構想承認記録.md`
3. `03_要件定義書改定.md`
4. `04_設計書改定.md`
5. `05_要件・設計整合性およびトレーサビリティ確認.md`
6. `../10_Revised_requirements_definition_documents/00_プロダクトコンセプトメモ.md`
7. `../10_Revised_requirements_definition_documents/10_要件定義.md`
8. `../10_Revised_requirements_definition_documents/21_論理データ設計.md`
9. `../10_Revised_requirements_definition_documents/22_プロダクト基本設計.md`
10. `../10_Revised_requirements_definition_documents/23_API・インターフェース設計.md`
11. `../10_Revised_requirements_definition_documents/30_詳細設計.md`

### 1.2. 開始判定

以下をすべて満たすこと。

- 承認済み要件定義書がリポジトリへ格納されている
- 承認済み設計書がリポジトリへ格納されている
- 要件・設計トレーサビリティ確認が`PASS`である
- 実装者が独自判断すべき仕様が残っていない
- 基準コミットが固定されている
- 現行Test Baselineが記録されている

## 2. Coding Agentへの最上位指示

### 2.1. 要件正本原則

要件定義書を唯一の正本として実装すること。

既存コードと要件が矛盾する場合、原則としてコードを修正すること。

### 2.2. 未決事項の処理

要件不足または設計矛盾を検出した場合、推測で補完してはならない。

以下の手順とする。

```text
実装停止
→ 問題点の記録
→ 影響する要件ID・設計節の特定
→ 変更提案
→ 承認
→ 要件定義書更新
→ 設計書更新
→ トレーサビリティ再確認
→ 実装指示書更新
→ 実装再開
```

### 2.3. 禁止事項

以下を禁止する。

- 旧Enhance Coding Instructionを直接実行する
- Causal Question専用Entityを追加する
- Identification専用Entityを追加する
- Refutation専用Entityを追加する
- Sensitivity専用Entityを追加する
- Run／Attemptを復活させる
- 旧Control Planeを復活させる
- 汎用Workflow Engineを追加する
- 汎用Lineage Relation Tableを追加する
- Comparison Tableを追加する
- 詳細RBACを追加する
- 旧DBデータ互換のための複雑なMigrationを作る
- CPDAG／PAGを暗黙にDAGへ変換する
- Refutation成功を識別仮定の証明として扱う
- `NOT_IDENTIFIED`を例外へ変換する
- External Library型をProduct DomainへImportする
- 未使用FieldをSilent Ignoreする
- 既存コードの挙動を要件へ昇格する
- Coding Agentが要件または設計を独自に変更する

## 3. 作業開始手順

1. Repositoryを取得する
2. 対象BranchをCheckoutする
3. 作業開始時の完全なCommit SHAを記録する
4. 基準Commitとの差分を確認する
5. 承認済み要件・設計書が格納済みであることを確認する
6. 現行Testを実行しBaselineを記録する
7. Product DB Schemaを確認する
8. Scientific Core PortとWorker Dispatchを確認する
9. 作業Branchを作成する
10. Work Package単位で実装する

## 4. Work Package依存順序

```text
WP-0 Requirements Gate
→ WP-1 Domain / Persistence Contract
→ WP-2 Snapshot / API Contract
→ WP-3 Graph Provenance
→ WP-4 Identification / Eligibility
→ WP-5 Estimation Gate / Diagnostics
→ WP-6 Refutation / Sensitivity
→ WP-7 UI / CLI / Query
→ WP-8 Scientific Benchmark
→ WP-9 Final Verification
```

後続Work Packageを、先行Work Packageの受入条件未達のまま開始してはならない。

## 5. WP-0 Requirements Gate

### 5.1. 目的

実装開始前に、正本となる要件および設計を固定する。

### 5.2. 作業

- 更新済み要件定義書を確認する
- 更新済み論理データ設計書を確認する
- 更新済みプロダクト基本設計書を確認する
- 更新済みAPI・インターフェース設計書を確認する
- 更新済み詳細設計書を確認する
- 要件IDと設計節の対応表を確認する
- 現行実装との差分一覧を作成する

### 5.3. 完了条件

- すべての実装項目に要件IDがある
- 設計未決事項がない
- 既存コード由来の追加要件がない
- 実装者が独自判断すべき仕様が残っていない

## 6. WP-1 Domain／Persistence Contract

### 6.1. 変更対象

```text
src/ariadne/product/domain/enums.py
src/ariadne/product/domain/execution.py
src/ariadne/product/domain/result.py
src/ariadne/product/domain/graph_version.py
src/ariadne/product/domain/graph_semantics.py
src/ariadne/product/persistence/orm_models.py
src/ariadne/product/persistence/repositories.py
product_migrations/versions/
```

### 6.2. Enum追加

Execution Operation:

```text
IDENTIFICATION
REFUTATION
SENSITIVITY
```

Result Type:

```text
DATA_ELIGIBILITY_RESULT
DIAGNOSTICS_RESULT
REFUTATION_RESULT
SENSITIVITY_RESULT
```

Graph Origin:

```text
DISCOVERED
CONSTRAINT_ADJUSTED
USER_DEFINED
IMPORTED
USER_EDITED
```

Scientific Statusを要件定義書で定義した和集合へ更新する。

ENH-E1で新規追加するResultへ`VALID`を書き込まない。

### 6.3. Execution変更

```python
input_result_id: str | None
snapshot_schema_version: str
```

Operation別の入力契約をDomain層またはApplication層で検証する。

### 6.4. Result変更

Result TypeとScientific Statusの組合せを検証する。

不正な組合せを永続化前に拒否する。

### 6.5. Graph Version変更

```python
graph_origin: GraphOrigin
provenance_json: dict[str, Any]
```

`source_result_id`をNullableに変更する。

Graph Origin別の参照制約を実装する。

### 6.6. Migration

- 空DBへのUpgradeを保証する
- 現Product DBデータの保持を実装要件としない
- Repository規約に従ってDowngradeを用意する
- Check Constraintを更新する
- FKへIndexを付与する

### 6.7. Test

- Enum Test
- Operation Matrix Test
- Result Status Matrix Test
- Graph Origin Test
- Project Boundary Test
- ORM Round-trip Test
- Migration Upgrade Test

### 6.8. 完了条件

- 7 EntityのままSchema拡張が完了している
- 不正なOperation／Input組合せを作成できない
- 不正なResult Type／Statusを保存できない
- Graph Originと参照関係が整合している

## 7. WP-2 Snapshot／API Contract

### 7.1. 変更対象

```text
src/ariadne/product/application/execution_service.py
src/ariadne/interfaces/web_api/schemas/
src/ariadne/interfaces/web_api/routers/executions.py
src/ariadne/interfaces/web_api/error_handlers.py
```

### 7.2. Snapshot Schema

`causal-analysis-spec/2`を実装する。

未知FieldをRejectする。

Operation別SchemaをDiscriminated Unionまたは同等方式でValidationする。

### 7.3. Canonicalization対象

以下をHash対象とする。

- Research Context
- Causal Question
- Causal Design
- Operation Spec
- Dataset Version ID／Hash
- Graph Version ID／Hash
- Input Result ID
- Method
- Parameters
- Random Seed
- Code Version
- Runtime Versions
- Override情報

### 7.4. API変更

Execution Batch Create Requestへ`input_result_id`を追加する。

Operation Enumを拡張する。

既存DISCOVERY／ESTIMATION Requestとの意味互換を維持する。

ただし、不正または曖昧な旧Fieldを要件へ昇格させてはならない。

### 7.5. Test

- Schema Version Missing
- Unknown Field
- Invalid Operation Spec
- Deterministic Snapshot Hash
- Input Result Mismatch
- Override Reason Missing

### 7.6. 完了条件

- 同一入力から同一Hashが得られる
- Operationに無関係なFieldをRejectする
- Submit後のSnapshotを変更できない
- Snapshot Versionを保存できる

## 8. WP-3 Graph Provenance

### 8.1. 変更対象

```text
src/ariadne/product/application/graph_version_service.py
src/ariadne/interfaces/web_api/routers/graph_versions.py
src/ariadne/product/domain/graph_semantics.py
src/ariadne/scientific/discovery/adapter.py
frontend/
```

### 8.2. 必須実装

- Source ResultなしのUSER_DEFINED Graph
- Source ResultなしのIMPORTED Graph
- Source Result由来のDISCOVERED Graph
- Parent Graph由来のUSER_EDITED Graph
- Post-hoc Constraint適用時のCONSTRAINT_ADJUSTED Graph
- Origin、Parent、Sourceの表示
- Graph TypeとEndpoint Semanticsの保持

### 8.3. Discovery Adapter修正

現在のPost-hoc Edge削除・追加を、制約付き探索Resultとして表示してはならない。

1. BackendがBackground Knowledgeを正式にサポートする場合、Algorithm Inputとして渡す
2. サポートしない場合、Algorithm Outputをそのまま保存する
3. 別Graph VersionとしてConstraint Adjustmentを適用する
4. Provenanceへ`constraint_mode=POST_HOC`を保存する

### 8.4. CPDAG／PAG

以下を保持する。

- Circle Endpoint
- Bidirected Edge
- Unresolved Orientation
- Graph Type
- Latent Confounding Warning

DAG専用処理へ渡す前にGraph Typeを検証する。

暗黙DAG化を禁止する。

### 8.5. Test

- Graph Origin Matrix
- Source／Parent Constraint
- Algorithm OutputとEdited GraphのHash差
- Endpoint Round-trip
- Post-hoc Provenance

### 8.6. 完了条件

- Algorithm Outputと編集結果を識別できる
- User-defined Graphから下流処理へ進める
- CPDAG／PAGを意味損失なく保存できる
- Post-hoc ConstraintをAlgorithm Constraintと誤表示しない

## 9. WP-4 Identification／Data Eligibility

### 9.1. 変更対象

```text
src/ariadne/product/ports/scientific_core.py
src/ariadne/scientific/core_adapter.py
src/ariadne/scientific/identification/
src/ariadne/scientific/validation/
src/ariadne/interfaces/worker/execution_processor.py
```

### 9.2. Scientific Core Port

```python
def run_identification(...) -> list[ScientificResultDescriptor]:
    ...
```

以下の2 Resultを返す。

- `IDENTIFICATION_RESULT`
- `DATA_ELIGIBILITY_RESULT`

### 9.3. ENH-E1 Identification Strategy

必須:

```text
RANDOMIZED
BACKDOOR
```

追加候補:

```text
USER_ASSERTED
```

`USER_ASSERTED`を許可する場合、Scientific Statusを`REQUIRES_REVIEW`とし、AssumptionsおよびReasonを必須とする。

### 9.4. Back-door Validation

- GraphがDAGである
- Treatment Nodeが存在する
- Outcome Nodeが存在する
- TreatmentとOutcomeが異なる
- Adjustment Setが観測列に存在する
- Adjustment SetにTreatmentを含まない
- Adjustment SetにOutcomeを含まない
- Treatment Descendantを含まない
- 既知Colliderを含まない
- Back-door PathをBlockする

一意に判断できないGraph Typeでは`REQUIRES_REVIEW`とする。

### 9.5. Data Eligibility

検査結果ごとに以下を返す。

```json
{
  "check_code": "LIMITED_OVERLAP",
  "status": "WARN",
  "message": "Estimated propensity scores show limited overlap.",
  "evidence": {}
}
```

総合Statusは以下の優先順位で決定する。

```text
FAIL > WARN > PASS
```

### 9.6. Worker

Identificationで科学的負結果が出ても、Result保存に成功した場合、Executionを`SUCCEEDED`とする。

### 9.7. Test

- Randomized Strategy
- Valid Back-door
- Missing Adjustment Set
- Invalid Adjustment Set
- Post-treatment Variable
- Collider
- Missing Node
- CPDAG Review
- PAG Review
- Poor Overlap
- Missing Column
- Duplicate Analysis Unit

### 9.8. 完了条件

- `NOT_IDENTIFIED`を正常なResultとして保存できる
- IdentificationとEligibilityを同一Executionから保存できる
- Data Eligibilityが`FAIL`の場合、下流Estimationを拒否できる
- 非識別理由を保存できる

## 10. WP-5 Estimation Gate／Diagnostics

### 10.1. 変更対象

```text
src/ariadne/product/application/execution_service.py
src/ariadne/scientific/inference/adapter.py
src/ariadne/interfaces/worker/execution_processor.py
```

### 10.2. Estimation受付条件

- `input_result_id`がIdentification Resultである
- 同一Projectである
- 同一Datasetである
- 同一Graphである
- Causal Question Hashが一致する
- Identification Statusが`IDENTIFIED`または許可済み`REQUIRES_REVIEW`である
- Data Eligibilityが`PASS`またはOverride済み`WARN`である
- Data Eligibilityが`FAIL`ではない
- EstimatorがEstimandと互換である

### 10.3. Estimator Capability Registry

各Estimatorについて以下を定義する。

- Supported Estimands
- Treatment Types
- Outcome Types
- Required Adjustment
- Uncertainty Support
- Overlap Requirement
- Produced Diagnostics

未対応FieldをSilent Ignoreしてはならない。

### 10.4. Diagnostics Result

Treatment Effect Resultとは別Resultとして保存する。

推定値が生成されても、Diagnosticsが`FAIL`となることを許容する。

### 10.5. Test

- Non-identified Gate
- Eligibility Fail Gate
- Warn Override
- Incompatible Estimator
- Multiple Estimators Reuse
- Diagnostics Failure with Technical Success

### 10.6. 完了条件

- 数値計算可能性を識別可能性と混同していない
- 同一Identification Resultを複数Estimatorが参照できる
- Diagnosticsを独立Resultとして表示できる
- 未対応Optionを拒否できる

## 11. WP-6 Refutation／Sensitivity

### 11.1. 変更対象

```text
src/ariadne/scientific/refutation/
src/ariadne/scientific/sensitivity/
src/ariadne/scientific/core_adapter.py
src/ariadne/interfaces/worker/execution_processor.py
```

### 11.2. Refutation

必須Method:

- Placebo Treatment
- Data Subset

Resultへ以下を保存する。

- Method
- Random Seed
- Perturbation
- Base Estimate
- Refutation Estimate
- Metric
- Severity
- Interpretation

### 11.3. Sensitivity

必須Method:

- Adjustment Set Variation
- Propensity Clipping Threshold Variation

Resultへ以下を保存する。

- Base Specification
- Variation
- Effect Range
- Sign Reversal
- Decision Reversal
- Warning

### 11.4. 表示文言

Refutation Result:

```text
特定の破綻を検出しなかった。
識別仮定の正しさを証明するものではない。
```

Sensitivity Result:

```text
指定した変動範囲に対する結論依存性を示す。
因果仮定の真実性を保証するものではない。
```

### 11.5. Test

- Deterministic Seed
- Placebo Near Zero
- Subset Stability
- Adjustment Variation
- Clipping Variation
- Incompatible Estimator
- Upstream Result Mismatch

### 11.6. 完了条件

- Resultを再実行できる
- Upstream Treatment Effect Resultへ遡れる
- 科学的解釈を過大表示しない
- Base Specificationとの差を保存できる

## 12. WP-7 UI／CLI／Query

### 12.1. UI

Inference Workspaceへ以下を追加する。

- Causal Question Form
- Identification Execution
- Eligibility Table
- Gate Status
- Override Form
- Estimator Compatibility
- Refutation Section
- Sensitivity Section

Results Workspaceへ以下を追加する。

- Result Type Filter
- Scientific Status
- Upstream Result
- Graph Origin
- Stage Lineage

### 12.2. Comparison

同一Result Typeかつ同一Estimandの場合のみ数値比較する。

条件が一致しない場合、Warningを表示する。

### 12.3. Lineage

`input_result_id`を再帰的に追跡する。

### 12.4. CLI

```text
ariadne-identify
ariadne-refute
ariadne-sensitivity
```

CLIはWeb Execution IDを使用しない。

### 12.5. 完了条件

- UIからE2E-04〜E2E-06を実行できる
- CLI ManifestがSnapshotおよびBackend Versionを保持する
- ComparisonとLineageをEntity追加なしで生成できる

## 13. WP-8 Scientific Benchmark

### 13.1. 配置

```text
tests/scientific_benchmarks/
```

通常のUnit TestとMarkerを分離する。

```python
@pytest.mark.scientific_benchmark
def test_known_truth_scenario() -> None:
    ...
```

### 13.2. Benchmark Scenario

- Randomized ATE
- Observed Confounding
- Missing Confounder
- Collider Adjustment
- Post-treatment Adjustment
- Poor Overlap
- Placebo
- Adjustment Variation
- Propensity Clipping
- Unresolved CPDAG／PAG

### 13.3. Benchmark出力

- Scenario
- Data-generating Process Version
- Random Seed
- Ground Truth
- Estimate
- Bias
- RMSE
- CI Coverage
- Expected Status
- Actual Status
- Runtime
- Package Versions

### 13.4. Benchmark Gate

- Deterministic Status一致率: 100%
- Post-treatment拒否率: 100%
- Non-identification検出率: 100%
- Fixed Poor-overlap検出率: 100%
- Standardized Absolute Bias: 0.10以下
- Empirical 95% CI Coverage: 0.90以上0.98以下

### 13.5. 完了条件

- Benchmark設定をArtifactまたはTest Outputとして保存する
- Threshold違反時にCIが失敗する
- 単一Seedだけで合格判定しない
- Backend Versionを記録する

## 14. WP-9 Final Verification

### 14.1. 必須検証

- Unit Test
- Component Test
- API Test
- Worker Test
- Migration Test
- Frontend Contract Test
- Browser E2E
- Scientific Benchmark
- Compose Golden Path
- Backup／Restore
- Static Analysis

### 14.2. 受入れ証跡

- Baseline Commit
- Completed Commit
- Test Command
- Test Result
- Environment
- Package Versions
- Migration Version
- Benchmark Result
- Known Limitations
- 未完了項目

### 14.3. 完了定義

以下をすべて満たした場合のみ実装完了とする。

1. すべてのMUST要件を実装している
2. 要件IDとTestの対応が存在する
3. E2E-04〜E2E-06が成功する
4. Scientific Benchmarkが成功する
5. 既存MVP Golden Pathが成功する
6. 新しい主要Entityを追加していない
7. 旧Run／Attemptを追加していない
8. CPDAG／PAGを暗黙DAG化していない
9. `NOT_IDENTIFIED`を技術的失敗として扱っていない
10. Refutationを仮定の証明として表示していない
11. 実装から要件定義書を変更していない
12. Coding Agentが未決事項を独断で補完していない
13. 要件、設計、実装およびTestのトレーサビリティが成立している

## 15. Work Package完了報告形式

```markdown
## WP-X Completion Report

### Requirements

- FR-xxx
- NFR-xxx

### Changed Files

- `path/to/file.py`

### Design Compliance

- 対応する設計書:
- 対応する節:
- 適合内容:

### Tests

- Command:
- Result:
- Evidence:

### Deviations

- None

### Unresolved Issues

- None
```

要件または設計からの逸脱がある場合、次のWork Packageへ進んではならない。
