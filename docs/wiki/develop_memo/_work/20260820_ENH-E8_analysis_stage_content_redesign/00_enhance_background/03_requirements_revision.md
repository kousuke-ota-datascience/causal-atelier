# ENH-E8 Requirement Revision

- Status: `APPROVED`
**Decision:** `NO_REQUIREMENT_SEMANTIC_DELTA`

## 1. 新規・変更・廃止Requirement

- New FR: `NONE`
- Revised FR semantics: `NONE`
- Retired FR: `NONE`
- New NFR: `NONE`
- Revised NFR semantics: `NONE`
- New/Revised AR: `NONE`

## 2. E8がconformance対象とする既存authority

| Area | Existing authority |
|---|---|
| Predictive task / feature-set semantics | `FR-055`, `FR-057` 等 |
| Predictive Stage catalog/responsibility | `FR-149`–`FR-152` |
| Causal Stage catalog/responsibility | `FR-153`–`FR-156` |
| canonical Project navigation | `FR-163` |
| Selected Project local navigation | `FR-166` |
| Stage Contentsへのexisting capability配置 | `FR-174` |
| Predictive Navigation Stage != runtime execution model | `FR-176` |
| UI/IA-only変更でAPI/persistence/backend semanticsを変えない | `FR-177` |
| navigation determinism / history | `NFR-022` 等 |
| draft/state continuity / current-stage presentation | `NFR-026` 等 |

## 3. Predictive feature selector

カンマ区切りfeature-column入力をDataset-schema-backed popup/checkbox selectorへ変更することは、新しいanalytical requirementではない。

維持するもの:

- `predictive-analysis-spec/1 -> feature_spec.feature_columns`
- feature availability
- target / excluded-column validation
- split semantics
- model behavior
- execution behavior

新規API、persistent resource、runtime Stage、analysis operationは導入しない。

## 4. E8固有の新規Requirement-level invariant

`NONE`

current-stage heading、presentation-only grouping、vertical layout、feature-selector interactionはDesign Invariantとして扱う。

## 5. Acceptance上の含意

Gate Acceptance Criteriaは、既存Requirement + E8 Design Invariantへtraceする。UI acceptanceをtraceするためだけに新しいRequirement IDを作らない。

## 6. Deferred capability

以下はENH-E8外とし、別EnhancementでRequirement semantic deltaを再評価する。

- LightGBM
- LIME
- SHAP
- `20260804_causal_lifecycle_enhancement` を起点とするcausal capability expansion
