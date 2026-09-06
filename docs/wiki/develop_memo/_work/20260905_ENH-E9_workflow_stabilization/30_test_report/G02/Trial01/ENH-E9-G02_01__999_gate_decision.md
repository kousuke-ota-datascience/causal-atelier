# ENH-E9 G02 Trial 01 Gate Decision

> **Document class:** Decision / Evidence Artifact

- Project / Enhancement / Gate / Trial: Ariadne / ENH-E9 / G02 / 01
- Reserved Test Item ID / Status: 999 / BLOCKED
- Fixed Trial Candidate SHA: `8cf70523093efa53b59a7de2c655f9755dbceb8d`
- Tested Repository State: `6355ce9252a896c5907ac465b102e959c5b481f7`
- 07 Contract: `10_enhance_instruction/G02/07_Ariadne_ENH-E9_G02_test_instruction.md` (FROZEN)
- Completion report: `20_implementation_reports/G02/Trial01/ENH-E9-G02_01__implementation_completion.md`
- Applicable 08: NONE
- Decision timestamp: 2026-09-06T01:13:54Z

## Decision summary

**BLOCKED — PROMOTION_NOT_ALLOWED.** Candidate identity and all non-browser blocking checks passed, but the frozen contract requires a final Browser E2E. The available runner stopped before its first scenario because its initial navigation selector is obsolete. This is `TEST_IMPLEMENTATION_DEFECT`, not a verified product violation; it cannot support either product FAIL or Gate PASS.

## Candidate identity and package provenance

- Fixed candidate established by Completion Report: YES.
- Tested state equals candidate: NO; post-candidate range classification: DOCUMENTATION_ONLY.
- Candidate identity valid for acceptance: YES (item 001).
- Previous failed candidate / remediation comparison: N/A.

| Package | Checkpoint present | Report present | Required | Provenance |
|---|---|---|---|---|
| P01 | YES | YES | YES | COMPLETE |
| P02 | YES | YES | YES | COMPLETE |
| P03 | YES | YES | YES | COMPLETE |

## Test Item evidence index

| Item | Name | Status | AC | Evidence path |
|---|---|---|---|---|
| 001 | Candidate identity and provenance audit | PASS | prerequisite AC1–AC8 | `ENH-E9-G02_01__001_candidate_identity_and_provenance_audit.md` |
| 002 | Non-browser interaction and contract regression | PASS | AC1–AC8 primary proof | `ENH-E9-G02_01__002_non_browser_contract_regression.md` |
| 003 | Browser cross-layer connectivity | BLOCKED | mandatory final connectivity AC1–AC8 | `ENH-E9-G02_01__003_browser_cross_layer_connectivity.md` |

## Acceptance Criteria and protected regression

| Requirement | Result | Evidence |
|---|---|---|
| AC1–AC8 non-browser primary proof | PASS | Item 002: 11 passed |
| Graph Candidate identity / GraphVersion lineage / DRAFT-FIXED / FIXED immutability / designated Outcome | PASS | Item 002 E2/E7 regression contracts |
| Mandatory Browser cross-layer connectivity | BLOCKED | Item 003: zero scenarios reached |

Browser diagnostic: `TEST_IMPLEMENTATION_DEFECT`; product judgment possible: **NO**. Trace/screenshot/video are listed in item 003. No Transition Debt audit is defined by frozen 07.

## Established contract and promotion consequence

N/A — this decision is BLOCKED. This canonical 999 is the Gate state authority; no mutable promotion artifact or Phase F write-set was produced.

## Failure remediation input

N/A — this is BLOCKED, not FAIL.

## Blocker record

- Blocker class: test implementation.
- Facts: `run_enh_e1a.py` requires `nav button[data-workspace="management"]`, while the current initial UI has `#new-project` and no matching selector. It stops before project registration, Discovery, comparison, adoption, or fix; `evidence.json` records empty scenarios and no console error.
- Required owner/action: update or provide the authoritative G02 Browser E2E runner to use current Project List → New Project navigation, then rerun Discovery → candidate review/comparison → adopt/fix.
- Trial identity handling: SAME_TRIAL. Candidate identity remains valid and no product defect is established.

## Final rationale

Frozen 07 is unambiguous. The candidate is valid and its package provenance complete. The 11 mandatory non-browser tests pass, covering AC1–AC8 and the protected lifecycle/lineage semantics. The contract nevertheless explicitly requires Browser E2E as the final item. Its failure is prior to any G02 product assertion and is attributable to a stale test locator, so product correctness cannot be determined. The only valid final state is `BLOCKED`, with `PROMOTION_NOT_ALLOWED`.
