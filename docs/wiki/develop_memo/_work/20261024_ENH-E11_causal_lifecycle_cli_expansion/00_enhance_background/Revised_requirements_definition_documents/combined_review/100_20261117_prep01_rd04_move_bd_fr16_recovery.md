# PREP-01 RD04 MOVE_BD recovery — 16 FR source text relocation

- Date: 2026-11-17 JST
- Classification: FLOW / SOURCE-INTEGRITY EVIDENCE
- Ledger: `doc01_review/rd04_review/95_rd04_fr_application_review.md`
- Scope: 16 FR `MOVE_BD` entries whose Revised RD stock text still contained the old design-specific predicate
- Before: full RD04 FR88 exact match = 72/88; these 16 were text mismatches; Status/Implementation/Delivery already matched for all.

## 1. Preconditions verified
1. RD row exactly matched the ledger's **original requirement text** and all Status/Implementation/Delivery metadata before editing.
2. The full original design predicate for each of these 16 FRs was present **verbatim** in each target 21/22/23/30 stock file named by the RD04 migration record (checked at branch HEAD; all applicable target files contained both exact original text and source ID).
3. Owner-approved RD04 disposition was `MOVE_BD` and prescribed the replacement `【設計制約移管・Legacy Trace】…` in the working-copy RD; no canonical `docs/wiki/requirement_definition/` edit is authorized.

## 2. Stock RD recovery

| ID | Revised RD document | Migration predicate |
|---|---|---|
| FR-045 | `10_13_fr_causal.md` | `MOVE_BD` |
| FR-075 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-077 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-079 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-080 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-089 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-143 | `10_14_fr_workflow_execution.md` | `MOVE_BD` |
| FR-133 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-140 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-141 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-144 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-145 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-157 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-158 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-160 | `10_16_fr_navigation_ui.md` | `MOVE_BD` |
| FR-128a | `10_18_fr_security_operations.md` | `MOVE_BD` |

Only Requirement text cells were changed. IDs, Area, Level, Requirement Status, Implementation Status, Delivery and order were preserved. The Source-oriented original predicate remains in design stock and historical RD04 ledger/migration records.

## 3. Remaining

`NFR-018`, `AR-022`, and `AR-009` are the remaining 3 `MOVE_BD` text mismatches. Their lower-design destination IDs are present, but full original predicate was not found verbatim. They must be checked or restored in design stock **before** overwriting the RD capability with a Legacy Trace.

The 16-row fix is **transcription+stock-preservation**, not a semantic/independent review PASS. This does not waive Product API negative tests, Method science acceptance or PREP02 Freeze.
