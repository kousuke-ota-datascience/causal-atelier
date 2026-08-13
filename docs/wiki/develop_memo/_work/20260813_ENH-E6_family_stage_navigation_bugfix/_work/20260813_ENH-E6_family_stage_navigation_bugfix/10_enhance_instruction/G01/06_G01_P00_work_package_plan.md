# ENH-E6 G01 P00 Work Package Plan

**Document class:** Planning / Orchestration Artifact  
**Self-containment:** MUST for decomposition responsibility.  
**Audience:** Human/operator; **not Coding Agent normative input**.

- Status: `APPROVED`
- Gate: `G01`
- Trial next: `Trial01`
- Execution Mode: `WORK_PACKAGE`

## 1. Why Work Package Mode is required

G01 is one semantic Gate, but implementation has three dependency/failure-localization boundaries: transition authority, presentation/legacy binding, and browser regression/harness. A single Coding execution would mix root-cause structural work with presentation mapping and test-infrastructure failure modes. Work Package Mode preserves one Gate while making checkpoints/restarts/focused verification bounded.

## 2. Effective Gate semantic boundary for decomposition

Decomposition must collectively establish: all supported Analysis navigation entries apply canonical Family/Stage context through one authority; shell/history/presentation stay synchronized; legacy analytical entries are compatibility shortcuts; Causal stage maps to correct existing surface; real browser critical journeys prove observable behavior.

No package may silently alter that semantic claim.

## 3. Package map

| Package | Purpose | Entry | Exit/checkpoint meaning |
|---|---|---|---|
| P01 | Navigation transition authority/lifecycle convergence | Trial01 repo clean; assigned P01 contract | transition seam exists; required entries converge within P01 scope; focused tests pass |
| P02 | Stage-aware presentation + legacy compatibility | P01 required checkpoint available | deterministic stage mapping/legacy targets integrated; focused tests pass |
| P03 | Browser regression/test strengthening | required P01/P02 behavior available | ENH-E6 real-browser runner + required static/regression support ready and focused browser suite green |

## 4. Execution DAG

```text
P01
  -> P02
  -> P03
P01 --------> P03 (P03 may reuse P01 seam, but blocking B02 requires P02 semantics)
```

Operational order: `P01 -> P02 -> P03` unless Human/operator explicitly determines a non-semantic test-infrastructure preparation can occur without violating dependency/prohibition rules. Coding Agents do not self-select next package.

## 5. Shared package rules

- assigned Pxx only is Coding Agent normative implementation contract.
- Coding Agent must not read Gate06/07/P00/other Pxx/00-30/ADR/past ENH/issues/Web for specification completion.
- source/test/config may be inspected as implementation substrate.
- canonical `docs/wiki/requirement_definition/**` and ENH-E5 historical evidence are protected.
- package cannot claim Gate PASS or close ANOM-E5-001.
- no unrelated refactor, fallback, test weakening.
- runtime-derived START/checkpoint/evidence SHAs must be reported, not guessed in planning docs.

## 6. Package completion semantics

`PACKAGE_READY` means assigned implementation and focused verification complete, checkpoint/evidence recorded. It does **not** mean:

- G01 PASS
- Fixed Trial Candidate assembled
- verified state promotion
- downstream Gate unlock
- `ANOM-E5-001` resolved

## 7. Interruption / restart rule

Wrong branch/dirty tree/ambiguous Pxx -> block before implementation. Same-package implementation/test correction stays Trial01. Package interruption does not create Trial02. Formal Independent Verification FAIL is required before Trial increment.

## 8. Checkpoint policy

Each package creates a package checkpoint commit only after its required implementation/focused verification succeed. Evidence/report commit may be separate. Reported `PACKAGE_CHECKPOINT_SHA` is implementation checkpoint identity, not evidence commit and not Fixed Candidate SHA.

## 9. Candidate Assembly

After required P01-P03 checkpoints are ready, Candidate Assembly verifies package identities/dependencies/diff, creates a Fixed Trial Candidate identity, and writes Trial completion/implementation completion record. Candidate Assembly does not make Gate PASS decision.

## 10. Trial completion condition

Trial01 candidate generation phase completes only when:

- all required packages are PACKAGE_READY,
- Candidate Assembly succeeds,
- one Fixed Trial Candidate SHA is fixed,
- implementation completion report/evidence references exact package checkpoint identities,
- candidate is ready for Independent Verification.

Trial01 itself ends with independent PASS/FAIL/BLOCKED decision.

## 11. Remediation rule

- Package/local failure before Fixed Candidate: same Trial01/package correction or BLOCKED; no 08.
- Independent formal FAIL: evaluate contract validity, then Trial02 + 08 (or 09 if contract defect).
- Do not return directly to normal Pxx route after formal FAIL.
