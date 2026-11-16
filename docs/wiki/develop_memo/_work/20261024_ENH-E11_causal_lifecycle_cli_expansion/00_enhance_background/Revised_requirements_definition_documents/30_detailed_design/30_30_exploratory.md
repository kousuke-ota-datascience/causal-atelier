# 30_30_exploratory

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `04d83541e55ab0364500afb4b92ef55c10785a0c`.

---

## 13. Exploratory Capability / Stage Contents

### 13.1 Mapping

| Navigation Stage | Current operation / resource | Detailed placement |
| --- | --- | --- |
| Profile | `PROFILE` | profile execution/control/result |
| Data Quality | dedicated operationなし | `PROFILE` resultのread-only projection |
| Distribution | `DISTRIBUTION` | distribution control/result |
| Relationships | `ASSOCIATION` | association control/result |
| Comparison | `GROUP_SUMMARY`, `TIME_TREND` | comparison/grouping controls/results |
| Findings | `CHART`, saved Exploratory Results | chart control/result/artifact + saved results |

### 13.2 Profile

ProfileはDataset/Analysis Viewのdescriptive profileを生成・表示する。

Profile resultはData Quality Stageからもread-only参照され得る。

### 13.3 Data Quality

Data Quality専用backend operationを作らない。

```text
PROFILE result found
  → render read-only data-quality availability/summary

PROFILE result absent
  → NO_PROFILE_RESULT
  → Profileへの導線
  → Execution/resource/backend stateを新規作成しない
```

`DATA_QUALITY` runtime operation、Result Type、persistent stateを追加しない。

### 13.4 Distribution

`DISTRIBUTION` operation/resultを配置する。Navigation Stage名を理由にruntime StageTypeを増設しない。

### 13.5 Relationships

`ASSOCIATION` operation/resultを配置する。

### 13.6 Comparison

`GROUP_SUMMARY`と`TIME_TREND`を同一Navigation Stageへ配置できる。

`TIME_TREND`はcurrent grouping/aggregation semanticsを維持する。

禁止:

- 新しい時系列モデルの導入
- UI Stage都合だけのtime type validation追加
- time orderingをscientific model semanticsとして暗黙導入

### 13.7 Findings

`CHART`はpersistent operationであり、表示専用mechanismへ置換しない。

- `CHART_RESULT`
- `CHART_SPECIFICATION`等のartifact/specification
- saved Exploratory Results

をcurrent contractに従って扱う。

---
