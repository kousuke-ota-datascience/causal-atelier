# ENH-E11 G01 AMD-E11-G01-P01-002 — Scientific Graph-negative reason contract amendment

**Document class:** Derived Contract; formal 09 decision candidate (self-contained)
**Amendment ID/type:** AMD-E11-G01-P01-002 / CONTRACT_DEFECT
**Gate/Trial:** G01 / P01 / Trial01
**Date:** 2026-11-23 JST
**Status:** PROPOSED; formal 09 Owner approval not yet issued; amended S10/S11 not yet issued
**Prior approved S10:** 707f6aaac1df5393dbf762448c41db2f1c9dbf35
**Prior approved S11:** record 187; no longer authorizes changed normative WHAT
**Third agent stop START_SHA:** f33a6a614881f69cc8db4216ce295072ff87b58c
**Provisional norm-content amendment commit:** f7492a58109fab4fd3050d63c32e89007ee2469d
**Frozen uv.lock Git blob (unchanged):** 2b83110e86b26b7969fbddf8f98a727370ae19f7

Affected G01 primary instructions: 06_G01_P01_local_contract_codec.md (§6.5.1a, §6.5.3, §7, §10); 06_G01_P04_fci_backend_oracle.md (producer); 06_G01_P05_cli_use_case_privacy.md (UseCase source verification); 07_Ariadne_ENH-E11_G01_test_instruction.md (existing MAN04/05 and G01-07-06/07/11 cases). Stock design: 30_62_local_execution_publication.md and 23_42_local_result_manifest_artifact.md. Ledger: 80_contract_amendment_log.md. Supporting Author review: combined_review/189_20261123_g01_p01_negative_reason_contract_defect_impact.md.

## 1. Contract defect

Previous P01 defined graph_negative_reason_codes as tuple[str,...] and required it to be nonempty with elements in Status reason_codes. Public e11-local-status/1 Schema constrains only uppercase text, not semantic categories. Therefore a technical failure duplicated in both fields (e.g. BACKEND_API_MISMATCH) met the previous explicit consistency checks. This contradicted P01's prose prohibition on technical failures as scientific-negative.

G01/P01/Trial01 third Coding Agent correctly stopped at BLOCKED_CONTRACT_AMBIGUITY before implementation. No actual focused tests, code changes, Package checkpoint or formal G01 FAIL; old two blocked reports preserved.

## 2. Why 08 remediation is inapplicable

No fixed candidate, G01_999 FAIL, approved 08 or defective production implementation exists. This is a frozen primary WHAT defect and must follow 09 -> new S10 freeze -> separate S11 authorization. Keep normal Trial01 absent a real formal Trial transition.

## 3. Before/after normative meaning

| Subject | Before | New meaning |
| --- | --- | --- |
| G01 science-negative code | Any nonempty strings matching Status | Closed singleton SCI_NO_ADMISSIBLE_PAG only |
| Exact G01 negative fields | Nonempty tuple and Status containing its codes | graph_negative_reason_codes == ("SCI_NO_ADMISSIBLE_PAG",) and status_payload.reason_codes == ["SCI_NO_ADMISSIBLE_PAG"] |
| Graph-positive fields | Negative tuple empty | Negative tuple empty and Status reason_codes == [] |
| Technical-error mixing | Not explicitly testable | All technical, unknown SCI_*, mixed, extra or duplicate codes rejected as SCHEMA_INVALID, even if tuple and Status both carry the identical bad text |
| Science semantic/provenance | Code equality could masquerade as legitimate result | SCI_NO_ADMISSIBLE_PAG means scientifically validated absence of any admissible PAG after eligible successful Method; **reserved** and no real P04 producer/proof currently established |
| P04/P05 | Generic typed legitimate negative | P04 only emits a scientifically proved discriminated negative; P05 checks actual P04 outcome and diagnostics and aborts on technical errors/absent proof, regardless of matching reason strings |
| Pure versus physical/semantic proof | Not fully explicit | P01 pure candidate classification only; P04/P05 actual Method proof and P02 independent physical checks; synthetic P01 fixture is not a scientific result |
| Public schema | Generic code format | Unchanged; G01 semantic validation is Method-specific |

A valid empty-edge PAG or uncertain PAG is still Graph-positive; an unavailable/malformed returned Graph, ineligible data, unsupported BK, API/runtime exception, incompatible model or inadequate support is never relabeled a scientific negative. If valid nonexistence proof is unavailable in P04, **do not produce any real G01 scientific-negative run**. This is not a claim that current causal-learn FCI can legitimately generate this outcome.

## 4. Acceptance criteria impact (no relaxation)

- G01-07-06/07 / DD-E11-MAN04/05: retain Graph-positive and scientifically justified negative structural variants; add closed-code negative test against same technical string, unknown SCI, duplicate/mixed, contaminated positive and bogus provenance. Pure synthetic negative tests are not an independent scientific proof.
- G01-07-08/09/10/11: real FCI/BK/SCI oracle/backend fail-closed and exit4 obligations unchanged.
- G01-07-05: atomic P02 publication/Reader and real FS unchanged.
- G01_999: independent S09/B02/B03/B04/B05/T2/T3/07/Product v2 regression requirements unchanged. Unproved real P04 negative scenarios remain BLOCKED, not fabricated PASS.

## 5. Protected previously passed Gates

No G01_999 PASS or fixed candidate exists. P01 checkpoint absent. G02-G10, Product v2, P02 real FD/readback, P03 PAG Graph semantics, lockfile and public wire schemas are untouched.

## 6. Execution invalidation

- P00 dependency DAG unaffected: P01 -> P02/P03 -> P04 -> P05.
- G01/P01 requires revised WHAT. G01/P04 and G01/P05 need aligned contracts; P02/P03 unchanged.
- Existing candidate invalidated: N/A (none).
- 185/186/187 Owner authorization applies to earlier freeze **only** and cannot be silently carried over.

## 7. Required rebaseline

Use the actual committed amendment full SHA (not a predicted SHA), diff it against previous S10, confirm changed path/blob list and uv.lock unchanged. Owner must explicitly approve this formal 09 and issue a new provisional G01-S10 full-SHA freeze. Only then a second, separate Owner approval can grant limited G01-S11 coding. Do not manufacture or claim those approvals from the request to amend documents. Re-run actual clean branch/lock/Trial preflight after approval.

## 8. Trial

Preserve all three pre-code BLOCKED Agent reports and Trial01. No automatic 02 or 08 remediation without a genuine formal Gate FAIL or owner state change.

## 9. Owner approval evidence

Owner requested immediate documentation correction of third blocked defect. **Owner formal 09 approval of this exact amended contract: PENDING. Revised S10: PENDING. Distinct revised S11: PENDING.** Independent S09/Science/OS and G01_999 not proven.

## 10. Ledger / traceability

See 80_contract_amendment_log.md, combined_review/189_20261123_g01_p01_negative_reason_contract_defect_impact.md, amended 06/07/23_42/30_62 at f7492a58109fab4fd3050d63c32e89007ee2469d. The later commit containing this 09 and ledger is a separate administrative source revision; actual freeze SHA must be obtained and approved after this commit.

## 11. Guardrail

No scientific truth manufactured from code text, no S09 PASS substituted, no public Schema changes, no Product v2 regression bypass, no acceptance weakening, no unauthorized coding before revised 09/S10/S11 approvals.
