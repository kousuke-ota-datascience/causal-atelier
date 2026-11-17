# PREP-01 RD04 MOVE_BD recovery — remaining NFR/AR 3 clauses

- Date: 2026-11-17 JST
- Type: FLOW / exact-text and destination-preservation evidence
- Baseline: 7f3ccfa1617e897ab1800180fcd2c5be6a1f8046
- Prior 97 text audit at older SHA detected 3 NFR/AR mismatches
- Corrected checking method: NFR/AR ledger has original text in **column 3**, revised text in **column 4** (unlike FR ledger which has RD file in column 3). An exploratory check had incorrectly searched for the revised text as the original; that false negative was corrected.

## 1. Requirements and design preservation

| ID | RD working file | Destination stock with exact original design constraint | Action |
|---|---|---|---|
| NFR-018 | `10_22_nfr_security_compatibility.md` | `22_00_overall_BD.md` + `30_51_security.md` | Replace original RD design clause with the RD04-approved Legacy Trace; preserve ID/status |
| AR-022 | `10_30_ar_scientific_integrity.md` | `22_03_navigation_application.md` | Replace original RD design clause with the RD04-approved Legacy Trace; preserve ID/status |
| AR-009 | `10_31_ar_estimand_inference.md` | `21_41_scientific_data_constraints.md` + `22_08_validation_architecture.md` | Replace original RD design clause with the RD04-approved Legacy Trace; preserve ID/status |

Each original source predicate was located *verbatim* with its ID in every listed destination **stock** file; this is stronger than confirming historical migration records only. RD Requirement Status and Implementation Status were compared with the ledger before edit; they were not changed. The prior 16 FR MOVE_BD fixes are tracked separately in [FR16 recovery](100_20261117_prep01_rd04_move_bd_fr16_recovery.md).

## 2. Scope and decision

- The 19 MOVE_BD revised texts are now applied to the RD working copy (FR 16 + NFR/AR 3). Design-level original predicates remain in their designated stock locations.
- No change to original canonical `docs/wiki/requirement_definition/`.
- No broad requirement redefinition: this re-applies the existing RD04 approved disposition to previously unmodified working-copy cells.
- A subsequent complete 122-row exact text/status recheck is required; semantic/independent review remains distinct from literal equality.
