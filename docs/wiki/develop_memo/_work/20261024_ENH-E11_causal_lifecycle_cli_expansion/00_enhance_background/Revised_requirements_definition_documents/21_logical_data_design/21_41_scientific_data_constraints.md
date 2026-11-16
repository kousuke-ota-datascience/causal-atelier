# 21_41_scientific_data_constraints

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

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


## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.AR-004. AR-004（SPLIT）

- 元要件（設計上の拘束を含む）：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する
- RD改訂後の要求：同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない
- Trace：`AR-004`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.AR-008. AR-008（SPLIT）

- 元要件（設計上の拘束を含む）：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
- RD改訂後の要求：推定に必要な変数型が適格かを識別できなければならない
- Trace：`AR-008`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.AR-009. AR-009（MOVE_BD）

- 元要件（設計上の拘束を含む）：外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Trace：`AR-009`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../96_rd04_nfr_ar_application_review.md)
