# 30_12_context_analysis_view


---

## 7. Research Context detailed contract

Research ContextはProject-scoped、versioned、immutable/fixed snapshotとして扱う。

主な責務:

- research question / hypothesis / assumptions等の分析文脈
- version history
- current active selection
- downstream AnalysisSpecification / Result lineageへの参照

Analysis Workspaceではexisting Research Contextをselectする。create/revise/history管理はProject Management / Research Context surfaceが担う。

Navigation Stage切替でResearch Context selectionを失わせない。

---

## 8. Analysis View detailed contract

### 8.1 Persistent contract

Analysis ViewはDataset Versionから派生するversioned logical viewである。

```text
AnalysisView
├─ analysis_view_id
├─ project_id
├─ source_dataset_version_id
├─ view_key
├─ version_number
├─ name
├─ status: DRAFT | FIXED
├─ schema_version: analysis-view/1
├─ spec_json
├─ content_hash
├─ manifest_json
├─ created_by / created_at
└─ fixed_at
```

logical specは少なくとも次のconcernを持ち得る。

```text
source_dataset_version_id
row_filter
selected_columns
derived_columns
missing_value_policy
time_cutoff
sampling
```

### 8.2 Ownership

- create/edit/version/fix/delete等のlifecycle ownership: Project Management / Data
- current input selection: Analysis Context
- execution input: existing fixed/supported Analysis View reference

Analysis ViewをExploratory専用resourceとして扱わない。

### 8.3 Filter validation contract

`row_filter` validationはsource `DatasetVersion`のlogical column typeをresolveし、create/update/validate/fixで同一ruleを適用する。

| logical type | allowed operators | value contract |
| --- | --- | --- |
| BOOLEAN | EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL | bool |
| INTEGER | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | boolを除くinteger |
| REAL | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | finite int/float、bool除外 |
| DATETIME | EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL | ISO-8601 string |
| TEXT | EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL | string |
| OTHER | IS_NULL, NOT_NULL | valueなし |

Invariant:

- `IS_NULL / NOT_NULL`はvalueを受け取らない。
- `IN / NOT_IN`はnon-empty list。
- `TEXT`へlexical LT/LTE/GT/GTEを許可しない。
- `time_cutoff`はDATETIME column + `LT / LTE`。
- source logical typeを決定できない場合はvalidation successにしない。
- type/operator/value incompatibilityはstable code `FILTER_TYPE_MISMATCH`。
- current operator taxonomy自体は変更しない。
- このvalidationは`analysis-view/1` persistent schemaを変更しない。

---
