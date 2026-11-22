# DEC-G01-EXEC-01 — G01 implementation-entry evidence rephasing (Owner adopted)

**Decision date:** 2026-11-23 JST (Owner reply following the 2026-11-22 discussion).
**Owner decision:** 「採用する。引き続き実行せよ」 in direct response to proposal **DEC-G01-EXEC-01: move unavailable pre-execution validation and independent S09/B05 scientific review to mandatory post-implementation acceptance; permit an Owner-approved provisional G01-S10 contract freeze and a separately Owner-approved limited G01-S11 coding authorization**.
**Status:** `OWNER_ADOPTED_CONTROL_PLANE_EXCEPTION_FOR_G01_ONLY`. **NOT** `S09_PASS`, **NOT** `S10_FROZEN`, **NOT** `S11_AUTHORIZED`, **NOT** `G01_999_PASS`.
**Scope:** Overrides the *timing/dependency* rules of `173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md` **for G01 only**. `DEC-PREPCODE-01=B` still governs Gate-specific approval and downstream Gate999 prerequisites. No Method, privacy, scientific-validity, CLI/ABI, fs-atomicity or security acceptance is removed.

## 1. Exact revised workflow

| Stage | Authoritative outcome | Requirements / blocked truth |
| --- | --- | --- |
| Author contract reconciliation | `AUTHOR_READY_FOR_PROVISIONAL_S10_REVIEW` after meaningful G01/common 06/Pxx/07, wire/Port/Method, privacy, Publisher/Reader, Protected Product v2, known fail-closed hazards are coherent | Author inspection is **not independent S09**; unresolved material implementation-contract contradictions remain true blockers |
| **G01 S10 (provisional)** | **Separate explicit Owner action** freezes **implementation WHAT and independent 07 acceptance obligations** at a full 40-hex source commit with exception ledger | No representation that S09, Python3.12 B02/B04 or MAG/PAG/BK B05 is PASS. Unresolved science reference specifications can be completed after code as a required 07/999 deliverable, but coding must not invent new scientific target/acceptance threshold |
| **G01 S11 (limited)** | **Separate explicit Owner action** grants only G01/P01–P05 coding and bounded developer tests on the frozen contract, named source/lock/ref/path boundary | No other Gate/Method authorization, no public/production science-release authorization, no unilateral contract change. No Agent execution merely from this policy adoption |
| After S11 | Candidate coding, read-only effective B02 Draft202012, B04 Python3.12 ENV-BASE `fisherz/chisq/gsq`, B03 actual Reader/OS, independent G01-common S09 review, independent B05 MAG/PAG/BK oracle, preregistered T2→T3, Product v2 regression, independent 07, G01_999 | `EXTERNAL_PENDING` if independent reviewer or VM unavailable. **G01_999 BLOCKED** without real independent acceptance and runtime evidence; cannot silently replace by Author Probe, mocks or source reading |
| Dependency closure | Only independently verified `G01_999=PASS` releases G01-dependent later Gates | Future Gate S09/S10/S11 policy unchanged by this one-Gate exception |

## 2. Explicit risk and fail-closed rule

- Source-level evidence that tagged `causal-learn 0.1.4.8` mishandles non-null BackgroundKnowledge (PAG over-orientation and stdout printing) is already known. All non-null BK, including structurally empty BK objects, remains `BACKEND_SEMANTICS_UNVERIFIED` / exit 4 **before FCI** until an independently verified scientifically valid remedy exists. Never weaken G01-07-10 or claim BK-positive science PASS. The positive-BK scientific acceptance obligation stays required before `G01_999 PASS`.
- No `fisherz/chisq/gsq` fit, Python3.12 validator, MAG/PAG compelled-endpoint oracle, T2/T3 statistical result, privacy-safe Reader, filesystem behavior or compatibility regression may be marked PASS without real evidence. Incompatible actual Backend API or a missing scientific Oracle is a post-S11 implementation/test blocker, not permission to substitute PC, impute, relabel, change estimand or relax AC.
- Frozen G01 06/07/Method semantics, G01 common contracts, relevant tests, actual Source ABI and protected v2 must not silently change under independent-review findings. A material discrepancy invokes formal 09 Contract Defect/change impact, Owner re-approval and revised frozen full SHA as required. Do not backfill an independent S09 PASS for the earlier provisional S10.
- The existing scientific scope (41 Methods, 68 dispositions, 10 UCs, full-real AR confidence sets in G08), cross-Gate DAG, accepted E11 Local Scientific CLI security/Privacy, no false Gate PASS, and independent `999` remain intact.

## 3. Evidence status and operational boundary

- `B02/B04` approved-target Linux Python3.12 execution: `EXTERNAL_PENDING / NOT_RUN`.
- `S09` truly separate independent G01/common document review: `EXTERNAL_PENDING / NOT_RUN`; it must occur **after S11 but before G01_999** under this exception.
- `B05` independent MAG/PAG and BK scientific reference acceptance: `EXTERNAL_PENDING / NOT_ACCEPTED`, required before `G01_999`.
- G01 S10 provisional Freeze: `AWAITING_SEPARATE_OWNER_DECISION`. G01 S11 limited coding authorization: `AWAITING_SEPARATE_OWNER_DECISION_AFTER_S10`.
- The present ChatGPT session cannot execute the Owner Linux VM or start an independent reviewer; do not schedule those as if this session could execute them. Continue only accessible Author contract/authorization preparation and actual downstream coding **after** distinct S11.
- Approved decision is a phase/timing exception; it does not authorize agents, Linux shell, any changes to `src/`, `tests/`, `pyproject.toml`, `uv.lock`, or a test PASS.

## 4. Documents to propagate

`172` (phase assignment), `173` (older per-Gate policy), `174` (G01 readiness), `165` (independent audit instructions as post-S11 required reviewer), G01 `06/P00/07`, shared `40` operator authorization controls, G01 blockers/exception register and later S10/S11 decision docket. Apply this decision **only** where G01 pre-code dependency rules are affected; do not change stock design scientific semantics or future Gate approval procedure.
