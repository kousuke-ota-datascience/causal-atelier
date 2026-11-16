# 22_05_family_exploratory

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

## 10. Family別Workflow / Capability

この章で扱う`Workflow`はruntime execution semanticsであり、5章のNavigation Stage一覧とは別概念である。

### 10.1 Exploratory

現行実装の`ExploratoryPlanner`は、`exploratory-analysis-spec/1`のoperationを次のruntime Stageへ写像し、**1 Execution Planにつき1 runtime Stage**を生成する。

| family_spec.operation | runtime stage_key | StageType |
| --- | --- | --- |
| `PROFILE` | `profile` | `exploratory.profile.v1` |
| `DISTRIBUTION` | `distribution` | `exploratory.distribution.v1` |
| `ASSOCIATION` | `association` | `exploratory.association.v1` |
| `GROUP_SUMMARY` | `aggregate` | `exploratory.aggregate.v1` |
| `TIME_TREND` | `time_trend` | `exploratory.time_trend.v1` |
| `CHART` | `chart` | `exploratory.chart.v1` |

Navigation Stage:

```text
Profile / Data Quality / Distribution / Relationships / Comparison / Findings
```

は上記runtime operationと同一taxonomyではない。例えば`Data Quality`や`Findings`に同名runtime Stageは存在しなくてよく、保存済みDataset/Result/Annotation/Artifactのreadで成立してよい。Navigation Stageを開いたことだけを理由にpersistent Executionを作らない。


## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-029（SPLIT）

- 既存要件の設計情報を含む原文：Chart Specificationを保存し、同じDataset Versionで再実行できる
- RDに残る能力／Legacy Trace：可視化の条件を保存し同じデータ版で再実行できる
- Original Requirement：`FR-029`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-032（SPLIT）

- 既存要件の設計情報を含む原文：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- RDに残る能力／Legacy Trace：探索結果から因果・予測分析の草案を生成し由来を追跡できる。本人の確定・実行を必要とする
- Original Requirement：`FR-032`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-034（SPLIT）

- 既存要件の設計情報を含む原文：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- RDに残る能力／Legacy Trace：探索に用いたデータ選択・分析設定・実行環境および成果物の由来を再構成できる
- Original Requirement：`FR-034`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-147（SPLIT）

- 既存要件の設計情報を含む原文：Visualizationは各分析Stageの表現手段とし、独立Navigation Stageを設けない
- RDに残る能力／Legacy Trace：可視化は探索の各目的に即して利用できる
- Original Requirement：`FR-147`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-148（SPLIT）

- 既存要件の設計情報を含む原文：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
- RDに残る能力／Legacy Trace：探索上のFindingで既存の結果・注釈・来歴を利用できる
- Original Requirement：`FR-148`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)
