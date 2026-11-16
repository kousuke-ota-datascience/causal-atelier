# 21_41_scientific_data_constraints


---

### 6.6 Result type / scientific status matrix

`Result.result_type`と`scientific_status`は任意組合せではない。少なくとも次を満たす。

| Result Type | Allowed Scientific Status |
| --- | --- |
| `DATA_PROFILE_RESULT`, `DISTRIBUTION_RESULT`, `ASSOCIATION_RESULT`, `GROUP_SUMMARY_RESULT`, `CHART_RESULT`, `ERROR_ANALYSIS_RESULT`, `MODEL_CARD_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS` |
| `SPLIT_RESULT` | `PASS` |
| `TRAINING_RESULT` | `TRAINED`, `TRAINED_WITH_WARNINGS` |
| `EVALUATION_RESULT` | `EVALUATED`, `INSUFFICIENT_TEST_SAMPLE` |
| `PREDICTIVE_EXPLANATION_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS`, `NOT_APPLICABLE` |
| `DISCOVERY_GRAPH_RESULT` | `GENERATED`, `GENERATED_WITH_WARNINGS`, `UNRELIABLE` |
| `IDENTIFICATION_RESULT` | `IDENTIFIED`, `NOT_IDENTIFIED`, `PARTIALLY_IDENTIFIED`, `REQUIRES_REVIEW` |
| `DATA_ELIGIBILITY_RESULT`, `DIAGNOSTICS_RESULT` | `PASS`, `WARN`, `FAIL` |
| `TREATMENT_EFFECT_RESULT` | `ESTIMATED`, `INSUFFICIENT_OVERLAP`, `INSUFFICIENT_SAMPLE`, `ESTIMATION_UNRELIABLE`, `REQUIRES_REVIEW` |
| `REFUTATION_RESULT` | `NO_FAILURE_DETECTED`, `FAILURE_DETECTED`, `INCONCLUSIVE` |
| `SENSITIVITY_RESULT` | `ROBUST`, `FRAGILE`, `INCONCLUSIVE` |

### 6.8 GraphVersion整合性

`graph_origin`とsource/parent referenceの整合を保証する。

- `DISCOVERED`: `source_result_id`必須。
- `CONSTRAINT_ADJUSTED`: source Resultまたはparent GraphVersionの少なくとも一方を要求。
- `USER_DEFINED / IMPORTED`: source Resultとparent GraphVersionを持たない。
- `USER_EDITED`: parent GraphVersion必須、source Resultは持たない。
- 自己parentを禁止する。
- Graph lineageでcycleを許容する設計にしてはならない。cycle検出の実装方式は詳細設計で定める。

**適用する論理データ制約（関連Requirement）**

- **`AR-004`**：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する
- **`AR-008`**：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
- **`AR-009`**：外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない
