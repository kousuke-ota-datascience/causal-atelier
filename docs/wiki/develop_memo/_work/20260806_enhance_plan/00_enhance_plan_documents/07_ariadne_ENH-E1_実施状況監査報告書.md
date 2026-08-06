# Ariadne ENH-E1 実施状況監査報告書

- 文書ID: `ARIADNE-ENH-E1-AUDIT-20260806`
- 作成日: 2026-08-06
- 文書状態: E1a是正実装の監査正本
- 対象リポジトリ: `kousuke-ota-datascience/causal-atelier`
- 対象ブランチ: `prototype/ariadne_mvp_e1_scientific_enhance`
- 対象計画: `ENH-E1`
- 後続是正計画: `ariadne_ENH-E1a`
- 対象計画文書: `docs/wiki/develop_memo/_work/20260806_enhance_plan/00_enhance_plan_documents/`
- 監査方式: 計画文書、要件定義、設計文書、実装コード、テストコード、コミット差分および実装報告書に対する静的監査

> 本文書は、`06_Ariadne_ENH-E1_実装指示書.md`に対する実装状況を判定し、後続の`ariadne_ENH-E1a`で解消すべき事項を固定する。
>
> 本文書は要件定義書を変更しない。要件の正本は引き続き`../10_Revised_requirements_definition_documents/10_要件定義.md`である。

---

## 1. エグゼクティブサマリー

### 1.1. 総合判定

> **INCOMPLETE / 条件付き不合格**

ENH-E1で要求された主要アーキテクチャおよび主要ユースケースは広範に実装されている。一方、計画上の完了条件である全MUST要件、科学ベンチマーク、Browser E2Eおよび受入証跡の一部が未達または不足している。

適切な状態表現は次のとおりである。

> **E1主要機能実装済み、科学的・受入検証未完了**

### 1.2. 判定の意味

本判定は、ENH-E1実装が全面的に失敗したことを意味しない。

以下の中核機能は実装済みまたは概ね実装済みである。

- Execution Operationの拡張
- Result Type固有Scientific Status
- Snapshot schema v2
- Graph provenance
- Identification-first
- Data Eligibility
- Treatment EffectとDiagnosticsの分離
- RefutationおよびSensitivity
- LineageおよびComparisonの拡張

一方、ENH-E1の完了定義は「主要コードが存在すること」ではなく、「全MUST要件と受入条件を、妥当なテスト証跡を伴って満たすこと」である。

### 1.3. 基準コミットに関する訂正

当初、計画文書の基準コミットと実作業開始HEADの不一致をWP-0の問題として指摘した。

その後、当該差異は計画文書作成後に文書を含む変更をコミットしたことによる正常な履歴形成であることが確認されたため、以下の指摘を撤回する。

- 基準コミットと実作業開始HEADの不一致
- 上記不一致を根拠としたRequirements Gate違反

修正後のWP-0判定は **実施済み** とする。

`Completed Commit`欄が未更新である点は、実装上の欠陥ではなく、最終報告書の記録整備事項として扱う。

---

## 2. 監査対象

### 2.1. リポジトリおよび実装

- 対象ブランチ: `prototype/ariadne_mvp_e1_scientific_enhance`
- 主要実装コミット: `3750bec0a2ef3236de94fa0cdcd17b8493677c49`
- 実装報告書: `../20_implementation_reports/ENH-E1_completion_report.md`

### 2.2. 計画・要件・設計文書

- `01_Enhance構想・要件改定計画.md`
- `02_Enhance構想承認記録.md`
- `03_要件定義書改定.md`
- `04_設計書改定.md`
- `05_要件・設計整合性およびトレーサビリティ確認.md`
- `06_Ariadne_ENH-E1_実装指示書.md`
- `../10_Revised_requirements_definition_documents/00_プロダクトコンセプトメモ.md`
- `../10_Revised_requirements_definition_documents/10_要件定義.md`
- `../10_Revised_requirements_definition_documents/21_論理データ設計.md`
- `../10_Revised_requirements_definition_documents/22_プロダクト基本設計.md`
- `../10_Revised_requirements_definition_documents/23_API・インターフェース設計.md`
- `../10_Revised_requirements_definition_documents/30_詳細設計.md`

### 2.3. 主な実装確認箇所

- `src/ariadne/product/domain/`
- `src/ariadne/product/application/`
- `src/ariadne/product/persistence/`
- `src/ariadne/scientific/identification/`
- `src/ariadne/scientific/inference/`
- `src/ariadne/scientific/refutation/`
- `src/ariadne/interfaces/web_api/`
- `src/ariadne/interfaces/worker/`
- `src/ariadne/interfaces/cli/`
- `frontend/`
- `tests/product/`
- `tests/scientific_benchmarks/`

---

## 3. 判定基準

| 判定 | 定義 |
|---|---|
| 実施済み | 要件に対応する実装および妥当な検証証跡が確認できる |
| 概ね実施 | 主要部分は実装済みだが、限定的な不足または改善事項がある |
| 部分実施 | 実装は存在するが、MUST要件または受入条件の重要部分が不足する |
| 未達 | 要求された実装、検証または証跡が確認できない |
| 判定不能 | 静的監査のみでは実行結果を確認できない |

---

## 4. Work Package別判定

| WP | 判定 | 要約 |
|---|---|---|
| WP-0 Requirements Gate | **実施済み** | 計画・要件・設計文書は配置されている。基準コミット差異は正常な履歴形成であり問題ではない |
| WP-1 Domain / Persistence | **概ね実施** | Operation、Result Type、Scientific Status、Graph Origin、Graph semanticsを実装 |
| WP-2 Snapshot / API | **概ね実施** | schema v2、未知Field拒否、snapshot hash、upstream result契約を実装 |
| WP-3 Graph Provenance | **概ね実施** | Origin、Parent、Source、CPDAG/PAG endpoint保持、post-hoc制約分離を実装 |
| WP-4 Identification / Eligibility | **部分実施** | RANDOMIZED/BACKDOOR、Eligibilityを実装。ただし異常系と科学判定ロジックに問題がある |
| WP-5 Estimation Gate / Diagnostics | **部分実施** | Identification-first gate、Diagnostics分離は実装。FR-054の型互換性検証が不足する |
| WP-6 Refutation / Sensitivity | **概ね実施** | Placebo、Data Subset、Adjustment Set、Clipping variationを実装 |
| WP-7 UI / CLI / Query | **部分実施** | UI・CLI・lineage・comparisonのコードは存在。Browser E2E未実施、FR-063の根拠不足 |
| WP-8 Scientific Benchmark | **未達** | 要求シナリオ、semi-synthetic benchmark、構造化Artifactが不足する |
| WP-9 Final Verification | **未達** | Browser E2E未実施、MUST要件未達、受入証跡不足 |

---

## 5. 実施を確認できた主要項目

### 5.1. Domain / Snapshot

以下の実装を確認した。

- `DISCOVERY`
- `IDENTIFICATION`
- `ESTIMATION`
- `REFUTATION`
- `SENSITIVITY`
- Operation別Graph／Upstream Input Matrix
- Result Type別Scientific Status Matrix
- `causal-analysis-spec/2`
- 未知Field拒否
- deterministic snapshot hash
- `input_result_id`
- validation overrideのreason、actor、warning_codes

主な確認箇所:

- `src/ariadne/product/application/execution_service.py`
- `src/ariadne/product/domain/analysis_spec.py`

### 5.2. Graph Provenance

以下を確認した。

- `DISCOVERED`
- `CONSTRAINT_ADJUSTED`
- `USER_DEFINED`
- `IMPORTED`
- `USER_EDITED`
- Source Result／Parent Graph制約
- CPDAG／PAG endpoint semantics保持
- post-hoc constraintを別Graph Versionとして保存
- Discovery Backendが制約未対応の場合に未適用であることを明示

主な確認箇所:

- `src/ariadne/product/domain/graph_version.py`
- `src/ariadne/product/application/graph_version_service.py`
- `src/ariadne/scientific/discovery/adapter.py`

### 5.3. Identification-firstおよびDiagnostics分離

以下を確認した。

- Identificationを独立Executionとして実行
- Identification ResultとData Eligibility Resultを生成
- `NOT_IDENTIFIED`のResult保存
- EstimationがIdentification Resultを明示参照
- Project／Dataset／Graph／Causal Question hashの照合
- Eligibility FAIL時の拒否
- Eligibility WARNおよび`REQUIRES_REVIEW`時のoverride要求
- Treatment Effect ResultとDiagnostics Resultの分離

主な確認箇所:

- `src/ariadne/scientific/identification/adapter.py`
- `src/ariadne/product/application/scientific_validation_service.py`
- `src/ariadne/interfaces/worker/execution_processor.py`

### 5.4. Refutation / Sensitivity

以下を確認した。

- Placebo Treatment
- Data Subset
- Adjustment Set Variation
- Propensity Clipping Variation
- Random seed保存
- Base estimateとの比較
- Sign reversal／decision reversal
- 仮定を証明する処理ではない旨の表示

主な確認箇所:

- `src/ariadne/scientific/refutation/adapter.py`
- `src/ariadne/scientific/sensitivity/adapter.py`

---

## 6. 監査指摘一覧

| 監査ID | 優先度 | 対象 | 判定 | 概要 |
|---|---:|---|---|---|
| AUD-E1-001 | P0 | WP-9 | 未達 | Browser E2EおよびE2E-04〜06が未実施 |
| AUD-E1-002 | P0 | FR-054 | 未達 | EstimatorのTreatment Type／Outcome Type互換性を実際に検証していない |
| AUD-E1-003 | P0 | WP-8／NFR-013 | 未達 | Benchmark scenario、semi-synthetic、構造化出力が不足 |
| AUD-E1-004 | P1 | FR-050／FR-064 | 不具合 | Eligibility FAILが例外により技術的FAILEDへ転化し得る |
| AUD-E1-005 | P1 | Identification | 科学的妥当性不足 | Collider判定がindegreeベースで過度に単純化されている |
| AUD-E1-006 | P1 | RANDOMIZED | 要件逸脱の疑い | Adjustment Setが非空であることだけを理由に一律`NOT_IDENTIFIED`とする |
| AUD-E1-007 | P1 | FR-067 | 状態優先順位不備 | CPDAG／PAGの`REQUIRES_REVIEW`が確定的入力不整合を隠し得る |
| AUD-E1-008 | P1 | FR-062 | 実装根拠不足 | 固定後変更を新Executionとし、変更理由を記録する仕組みが不足 |
| AUD-E1-009 | P1 | FR-063 | 未実装の可能性大 | 同一データで探索後に確認的推定する場合の警告が不足 |
| AUD-E1-010 | P2 | NFR-015／報告書 | 証跡不足 | Completion Reportが実際の未達事項と最終コミットを十分に反映していない |

---

## 7. 重大な未達事項

### 7.1. AUD-E1-001: Browser E2E未実施

#### 7.1.1. 事実

`06_Ariadne_ENH-E1_実装指示書.md`では、以下を完了条件としている。

- Browser E2Eを含む最終検証
- E2E-04〜E2E-06の成功
- すべてのMUST要件の実装

`ENH-E1_completion_report.md`は、Firefox／WebDriver環境上の制約によりBrowser E2Eを未実施とし、最終判定を`INCOMPLETE`としている。

#### 7.1.2. 判定

**WP-9は未達である。**

Frontend contract testおよびAPI E2Eは、実ブラウザにおける以下の検証を代替しない。

- フォーム入力
- 画面状態遷移
- 非同期表示更新
- ブラウザ固有のエラーハンドリング
- UI操作とAPI／Worker連携の統合動作

### 7.2. AUD-E1-002: FR-054 Estimator型互換性検証の不足

#### 7.2.1. 要件

FR-054はEstimatorについて、少なくとも以下との互換性検証を要求する。

1. Estimand
2. Treatment Type
3. Outcome Type
4. Identification Strategy

#### 7.2.2. 実装確認

`ESTIMATOR_CAPABILITIES`には以下が定義されている。

- `estimands`
- `strategies`
- `treatment_types`
- `outcome_types`
- `required_adjustment`
- `uncertainty_support`
- `overlap_requirement`
- `produced_diagnostics`

一方、`ScientificValidationService._validate_estimation()`で確認できる受付検証は主として以下である。

- Estimand
- Identification Strategy
- Parameter名

Treatment TypeおよびOutcome Typeについて、Data Eligibility Result、Dataset schemaまたは実データから導出した型との照合処理は確認できない。

FR-054対応とされるテストもRegistry内のキー存在確認が中心であり、型不一致入力を拒否する振る舞いを検証していない。

#### 7.2.3. 判定

**FR-054は未達である。**

Capability Registryの定義と、Registryに基づく受付可否判定は別の実装責務である。

### 7.3. AUD-E1-003: Scientific Benchmarkの不足

#### 7.3.1. 計画上の要求シナリオ

実装指示書は以下の10シナリオを要求する。

1. Randomized ATE
2. Observed Confounding
3. Missing Confounder
4. Collider Adjustment
5. Post-treatment Adjustment
6. Poor Overlap
7. Placebo
8. Adjustment Variation
9. Propensity Clipping
10. Unresolved CPDAG／PAG

さらに以下の出力を要求する。

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

#### 7.3.2. 実装確認

Benchmarkコードでは主に以下を確認した。

- Back-door成功
- 未調整による非識別
- Post-treatment adjustment
- CPDAG／PAG
- Poor overlap
- 複数seedのRandomized ATE bias／coverage
- Placebo再現性
- Propensity clipping variation

#### 7.3.3. 不足

少なくとも以下が不足する。

- Collider Adjustmentを明確に表す独立Benchmark
- Adjustment Set Variationの独立Benchmark
- Semi-synthetic Benchmark
- DGP version、RMSE、runtime、package versions等を含む構造化出力
- Benchmark設定と結果をCI Artifactまたは同等の証跡として保存する仕組み

#### 7.3.4. 判定

**WP-8およびNFR-013は未達である。**

テスト件数の成功は、計画上要求された科学シナリオおよび評価指標の網羅を意味しない。

### 7.4. AUD-E1-004: Data Eligibility FAILが技術的FAILEDへ転化し得る

#### 7.4.1. 実装上の問題

Eligibility処理は非数値列を検出した場合、`TYPE_COMPATIBILITY = FAIL`を生成する。

一方、その後の処理でTreatment列の型にかかわらず平均値を計算する。

```python
prevalence = float(frame[treatment].dropna().mean())
```

文字列Treatment等では例外が発生し得る。

WorkerはScientific Adapterから例外が送出された場合、Execution全体を`FAILED`へ遷移させる。

#### 7.4.2. 期待動作

```text
非対応Treatment型
→ Data Eligibility Result = FAIL
→ Identification Execution = SUCCEEDED
→ Estimation受付を拒否
```

#### 7.4.3. 発生し得る動作

```text
非対応Treatment型
→ TYPE_COMPATIBILITY FAILを生成
→ 型依存診断で例外
→ Result未保存
→ Execution = FAILED
```

#### 7.4.4. 判定

以下に対する実装不備である。

- FR-050
- FR-064
- 科学的負結果と技術的失敗を分離する設計原則

---

## 8. 科学的妥当性に関する問題

### 8.1. AUD-E1-005: Collider判定の過度な単純化

現在の実装は、Adjustment Set内で親を2つ以上持つノードをColliderとして扱う。

```python
colliders = sorted(
    node for node in adjustment
    if len(parents.get(node, set())) >= 2
)
```

この条件は、Treatment–Outcome間の対象経路においてColliderとして作用するかを判定していない。

#### 8.1.1. 想定される影響

- 対象因果効果に対して問題のない共変量をColliderとして拒否する
- 真のColliderまたはCollider descendantによるpath openingを適切に表現できない
- Graph全体のindegreeと、対象因果効果に対するCollider biasを混同する

#### 8.1.2. 判定

Colliderに関する拒否処理は存在するが、科学的妥当性の観点では要修正である。

### 8.2. AUD-E1-006: RANDOMIZEDでAdjustment Setを一律禁止

Identification Adapterは、`RANDOMIZED`かつAdjustment Setが空でない場合に`NOT_IDENTIFIED`とする。

一方、要件文書はRANDOMIZED strategyのサポートを規定しているが、Adjustment Setを必ず空にする制約を明示していない。

#### 8.2.1. 代替仮説

- 要件記載漏れ
- 実装者による独自仕様追加
- 科学的に不要に強い制約

#### 8.2.2. 判定

Adjustment Setが非空であることのみを理由に`NOT_IDENTIFIED`とする実装は、要件上の根拠が不足する。

### 8.3. AUD-E1-007: CPDAG／PAGと確定的異常条件のStatus優先順位

Identification AdapterはTreatment nodeまたはOutcome node不在等の理由を生成した後、Graph TypeがCPDAG／PAGである場合に`REQUIRES_REVIEW`を設定する。

そのため以下が同時に成立する場合でも、最終Statusが`REQUIRES_REVIEW`になり得る。

- Graph TypeがCPDAGまたはPAG
- Treatment node不在
- Outcome node不在
- 必須データ列不在

#### 8.3.1. 問題

- 「方向未確定」と「分析対象不在」が同一Statusに隠れる
- 明確な入力不整合が、専門家レビューで解決可能な不確実性として扱われる
- 利用者が修正すべき原因を誤認する

#### 8.3.2. 判定

Graph orientation不確実性より、確定的入力不整合および非識別条件を優先する必要がある。

---

## 9. Analysis Mode要件の評価

### 9.1. 確認できた実装

- `analysis_mode`が`EXPLORATORY`または`CONFIRMATORY`であることのValidation
- UIからAnalysis ModeをSnapshotへ含める処理

### 9.2. AUD-E1-008: FR-062の実装根拠不足

FR-062は以下を要求する。

- 固定後の条件変更は新しいExecutionとする
- 変更理由を記録する

Execution Snapshotの不変性は確認できるが、以下の実装根拠が不足する。

- 既存Executionを基準とした改訂Executionの明示
- 変更理由の必須化
- 変更された条件の記録
- API／UI／Lineage上の確認手段
- 専用Behavior Test

### 9.3. AUD-E1-009: FR-063の実装不足

FR-063は、同一データでGraph探索と確認的推定を行う場合、探索後推論の警告を表示することを要求する。

以下の処理を確認できない。

- 同一Project／Dataset Versionに先行Discoveryが存在するかの判定
- `CONFIRMATORY` Estimationとの組合せ検出
- 探索後推論警告の生成
- 警告の保存または再現
- UI／CLI表示
- 専用Behavior Test

### 9.4. 判定

| 要件 | 判定 |
|---|---|
| FR-060 | 実施済み |
| FR-061 | SHOULD。明確な実装根拠不足 |
| FR-062 | 部分実施または実装根拠不足 |
| FR-063 | 未実装の可能性が高い |

---

## 10. 受入証跡の評価

### 10.1. 問題ではない事項

以下は問題なしと判定する。

- 計画文書作成後のコミットによる基準コミットと作業開始HEADの差異

### 10.2. AUD-E1-010: 更新が必要な事項

`ENH-E1_completion_report.md`について以下の更新または後続報告での是正が必要である。

- 完了コミットの記録
- Browser E2E未実施の明示
- FR-054、Benchmark、Eligibility異常系、FR-062、FR-063等の未達反映
- 「既知の未完了項目はBrowser E2Eのみ」という記述の是正
- 要件ID、設計節、実装箇所、Test Case、実行結果の対応更新

### 10.3. 判定

`Completed Commit`未更新は軽微な文書整備事項であり、コード品質またはRequirements Gate違反ではない。

一方、未達事項を網羅していないCompletion Reportは、最終受入証跡として不十分である。

---

## 11. 総合判定表

| 評価対象 | 判定 |
|---|---|
| 主要アーキテクチャ実装 | 実施済み |
| 主要E1ユースケース | 概ね実施 |
| Domain／Snapshot／Provenance | 概ね実施 |
| Identification-first | 実施済み |
| Diagnostics分離 | 実施済み |
| Estimator型互換性 | 未達 |
| Eligibility異常系 | 不具合あり |
| Refutation／Sensitivity | 概ね実施 |
| Analysis Mode | 部分実施 |
| Scientific Benchmark | 未達 |
| Semi-synthetic Benchmark | 未達 |
| Benchmark Artifact | 不足 |
| Browser E2E | 未実施 |
| 最終受入証跡 | 不足 |
| WP-0 Requirements Gate | 実施済み |
| ENH-E1総合完了 | **未達** |

---

## 12. ariadne_ENH-E1aへの引継ぎ

### 12.1. P0: 完了判定を阻止する項目

1. `AUD-E1-001`: Browser E2EおよびE2E-04〜06を実行する
2. `AUD-E1-002`: FR-054のTreatment Type／Outcome Type互換性検証を実装する
3. `AUD-E1-003`: Benchmark scenario、semi-synthetic、構造化出力を完成させる

### 12.2. P1: 科学的・機能的欠陥

1. `AUD-E1-004`: 非対応型をEligibility FAILとして正常保存する
2. `AUD-E1-005`: Collider判定を対象経路または同等のd-separation基準に基づく判定へ変更する
3. `AUD-E1-006`: RANDOMIZEDのAdjustment Set一律禁止を撤廃し、pre-treatment covariate adjustmentを妥当に扱う
4. `AUD-E1-007`: 確定的異常条件を`REQUIRES_REVIEW`より優先する
5. `AUD-E1-008`: FR-062の改訂Executionと変更理由記録を実装する
6. `AUD-E1-009`: FR-063の探索後推論警告を実装する

### 12.3. P2: Test／Traceability

1. `AUD-E1-010`: E1a Completion Reportで最終コミットと全未達解消証跡を記録する
2. FR-054をRegistry shape testからbehavior testへ変更する
3. FR-062およびFR-063の専用テストを追加する
4. 各Benchmark scenarioを独立した名称と要件IDで管理する
5. 要件ID―設計節―実装箇所―Test Case―実行結果を機械可読または表形式で管理する

---

## 13. 最終結論

ENH-E1は、中核ドメイン、Graph provenance、Identification-first、Diagnostics分離、RefutationおよびSensitivityについて相当程度実装されている。

しかし以下が残存する。

- Estimator型互換性検証の不足
- Eligibility異常系の技術的失敗化
- Collider判定の科学的妥当性不足
- RANDOMIZED adjustmentの過剰制約
- CPDAG／PAG時のStatus優先順位不備
- Analysis Mode関連要件の不足
- 科学ベンチマークのシナリオ不足
- semi-synthetic benchmark未実施
- 構造化Benchmark Artifact不足
- Browser E2E未実施
- Completion Reportの証跡不足

よって、現時点のコードベースを **ENH-E1完了** と判定することはできない。

> **最終判定: INCOMPLETE / 条件付き不合格**

上記指摘を閉じる後続是正計画を`ariadne_ENH-E1a`とする。

---

## 14. 監査上の制約

本報告はGitHub上のソースコードおよび文書に対する静的監査である。

以下は独立再実行していない。

- 実装報告書記載のテスト成功件数
- PostgreSQLを用いた統合テスト
- Docker Compose golden path
- backup／restore
- Browser E2E
- 実運用相当データに対する科学計算結果

したがって、実行結果については、実装報告書の記載とコード上の証跡を区別して扱う。

静的監査で確認できた事実と、実行環境を必要とする未検証事項は同一視しない。
