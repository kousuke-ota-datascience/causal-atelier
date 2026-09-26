# ENH-E10 Approved Requirement / Design Snapshot

> **Document class:** Approved Snapshot Manifest  
> **Status:** `APPROVED / CANONICAL_APPLIED`  
> **Enhancement:** `ENH-E10`

## 1. Snapshot identity

Canonical application commit:

`3e22d09e7e68e65aceb54d1a3a32cab697d7b480`

Human approval source:

- `02_enhancement_concept_approval_record.md`
- approval timestamp: `2026-09-26T14:58:00+09:00`

Architecture decision authority:

- `40_operator_workflows/architecture_review/02_target_architecture_decision_record.md`

## 2. Canonical files

| Canonical document | Git blob SHA at snapshot |
|---|---|
| `docs/wiki/requirement_definition/10_requirements_definition.md` | `9e1389c077487f14db5a2e1d32166627bb75679f` |
| `docs/wiki/requirement_definition/22_product_basic_design.md` | `87196f2f03a7f3367724bc05fb254d1a4d98109e` |
| `docs/wiki/requirement_definition/23_api_interface_design.md` | `131467f02222f105a49e6dfdbcec0f49cadb0f41` |
| `docs/wiki/requirement_definition/30_detailed_design.md` | `04d83541e55ab0364500afb4b92ef55c10785a0c` |

## 3. Applied requirement delta

Applied existing requirement revisions:

- FR-061
- FR-068
- FR-069
- FR-071
- FR-161

Applied new IDs after collision check:

- FR-178 through FR-184
- NFR-028
- AR-027

No collision was found at application time.

## 4. Applied architecture essentials

- optional extra `predictive-advanced`
- LightGBM classifier/regressor model IDs and bounded parameter contract
- core import isolation / no silent fallback
- provider-neutral `fitted-model/2` new-write contract with v1 read compatibility
- `SHAP_TREE` LightGBM global/local raw-output semantics
- `LIME_TABULAR` local-only deterministic TRAIN reference semantics
- additive `predictive-capabilities/1`
- unchanged `predictive-analysis-spec/1`
- capability-driven Train / Explainability / Model Management
- G03 two critical Browser journeys

## 5. Use

This manifest freezes the requirement/design source snapshot used to finalize ENH-E10 traceability and Gate contracts.

It is not an implementation-completion record and does not authorize Coding Agent execution by itself. Gate execution still requires:

1. Gate-local 06/07/Pxx FROZEN
2. upstream prerequisite evidence
3. Agent Execution Readiness = READY
