# 189 — G01 P01 Trial01 third BLOCKED contract defect: scientific-negative reason taxonomy

**Date:** 2026-11-23 JST
**State:** AUTHOR_IMPACT_REVIEW_RECORDED / OWNER_09_S10_S11_PENDING
**Amendment:** AMD-E11-G01-P01-002 / CONTRACT_DEFECT
**Observed start:** f33a6a614881f69cc8db4216ce295072ff87b58c / BLOCKED_CONTRACT_AMBIGUITY
**Old frozen S10:** 707f6aaac1df5393dbf762448c41db2f1c9dbf35

## 1. Direct documentary evidence

The e11_local_status_v1.schema.json reason_codes array allows uppercase strings with no science/technical taxonomy. Previous P01 only checked nonempty graph_negative_reason_codes also present in Status, while P04 described a typed legitimate scientific-negative with no closed code set. Thus ("BACKEND_API_MISMATCH",) and ["BACKEND_API_MISMATCH"] satisfy the value join despite a real technical cause. This third stop was pre-implementation, without focused tests/checkpoint.

## 2. Chosen author correction and limits

G01-specific closed P01 code vocabulary: only SCI_NO_ADMISSIBLE_PAG, exactly once and identically in the tuple and Status list for the negative structural variant; both must be empty for a positive. Reject all other technical, mixed, unknown or duplicate codes. P01 pure tests may use a synthetic SCI_NO_ADMISSIBLE_PAG candidate, but no science proof exists by that fact.

The phrase means that a method-specific, otherwise eligible and successfully executed procedure **scientifically proves** no admissible PAG. Present P04 evidence does not establish an actual G01/FCI producer of that condition; do not manufacture one. P04 disallows negative emission without that real proof; P05 must check actual discriminated P04 outcome and diagnostics independently and refuse technical failure relabeling. Existing uncertainty or empty-edge PAG is not a valid no-Graph negative.

## 3. Impact

| Normative family | Affected portion | Change type |
| --- | --- | --- |
| G01 P01 §6.5.1a/§6.5.3, §7/§10 | Exact closed grammar, negative tests and DoD | Primary coding WHAT completion |
| G01 P04 / P05 | Strict scientific producer and UseCase provenance | Fail-closed boundary alignment |
| 23_42 / 30_62 | Operation-specific classification and stock semantics | Design alignment |
| G01 07 | Pure fake-error negatives, distinct real scientific proof | No test weakening |
| P02/P03, P00, G02-G10, schemas, code, uv.lock | Unchanged | No scope expansion |

Unchanged mandatory G01_999 obligations: independent S09, real Python/Backend/FD/FS checks B02-B04, independent MAG/PAG/BK B05, T2/T3, real 07/999, Product v2 regression, privacy, BK fail-closed. No real tests or independent audit were executed by the document Author.

## 4. Owner gates, blocked reports and source

Normative change commit f7492a58109fab4fd3050d63c32e89007ee2469d. This 09/189/Ledger/Handoff administrative commit must be inspected and its complete SHA explicitly pinned by a subsequent Owner-approved new provisional S10; then separate Owner S11 is required. Historical records 185-188 and previous failed preflight reports are not rewritten; prior S10/S11 no longer authorizes the changed WHAT. Trial 01 is retained unless a real formal Fail/08 evidence changes it.
