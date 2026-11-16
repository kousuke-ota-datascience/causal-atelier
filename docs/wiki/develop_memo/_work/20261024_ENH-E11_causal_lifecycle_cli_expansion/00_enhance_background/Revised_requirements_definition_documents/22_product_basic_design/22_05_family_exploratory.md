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

**当該機能に適用する設計制約（関連Requirement）**

- **`FR-029`**：Chart Specificationを保存し、同じDataset Versionで再実行できる
- **`FR-032`**：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- **`FR-034`**：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- **`FR-147`**：Visualizationは各分析Stageの表現手段とし、独立Navigation Stageを設けない
- **`FR-148`**：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
