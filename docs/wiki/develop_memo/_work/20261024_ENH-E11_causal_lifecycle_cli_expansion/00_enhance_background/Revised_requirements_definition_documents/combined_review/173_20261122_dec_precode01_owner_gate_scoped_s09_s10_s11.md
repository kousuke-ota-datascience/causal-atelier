# DEC-PREPCODE-01 — Gate-scoped independent review, Contract Freeze and Coding Authorization

**Date:** 2026-11-22 JST  
**Authority:** Human Owner's explicit current message: `B案を採用する。引き続き進めよ`.  
**Decision:** `B / OWNER_ADOPTED / CONTROL_PLANE_CHANGED`.  
**Current execution status:** `G01_S09_NOT_RUN / G01_S10_NOT_FROZEN / G01_S11_NOT_AUTHORIZED`. This is an authoritative **workflow policy change**, **not** human approval of the scientific algorithm, the 06/07 contents, S09, Freeze, source change, or Coding Agent execution.

## 1. Exact adopted policy

Replace the historical global order `all-Gate S09 → one global S10 Freeze → individual Gate S11` with:

1. Maintain a **global versioned inventory of active E11 contracts** (latest 402 unique sources; additional source/provenance and direct dependency references must be discovered). This is for coverage, changed-closure analysis, downstream QA and regressions; **402/402 SHA equality is not 402/402 independent semantic review**.
2. **First independently review and freeze the common contract baseline** together with G01: E11 local wire/Study, ContentRef, strict versioning/JCS/hash domains, shared Ports/Class boundaries, root/privacy, atomic publisher/Reader, Operation status/bundle semantics, Method registry dispatch and protected Product v2 invariants. Do not falsely claim common baseline has been approved before S09/S10.
3. For each Gate `Gnn`, conduct **scope-limited independent S09 review** of the common baseline and *every* source file affecting `Gnn` or its scientifically/technically transitive upstream dependency closure: 06, P00/Pxx, 07, operator entry prompts, Method/Output/Inference Profiles, applicable design/requirement stock, true Source ABI, reference and negative acceptance specification. Review outside-scope Gate documents only as needed to determine coupling/contradictions; mark unreviewed ones `NOT_REVIEWED`, not `PASS`.
4. Each Gate then receives its **own explicit Owner S10 Contract Freeze** referencing exactly one immutable reviewed Source commit/full SHA and itemized contract+independent S09 verdict+pre-code science/Backend/Schema evidence. No automatic approval from an Author's notes or from another Gate. Any change of shared/frozen material invalidates impacted closure until independently re-audited and re-frozen; do not change protected v2 or silently inherit a previous Gate verdict.
5. Only **after** its S10, an independent **Owner S11 Coding Authorization** names the exact Gate/Pxx, reviewed source+lock, affected paths and applicable 06/07. For `G02+`, prerequisites include **actual upstream Gate999 PASS** and confirmed immutable dependency integrity; a frozen-but-not-completed upstream Gate is insufficient. No coding permission for unrelated Gates or Methods.
6. Execute Coding Agent → fixed candidate Trial → Independent Test Agent → Gate999 under the approved Gate's frozen 06/07. Actual E11 FS/Reader, numeric T2/T3 and production Adapter regression belong here; never replace these with pre-code design-only assertions.
7. G10 confirms **all 41** Method independently accepted science evidence and all required upstream 999; changed/unknown closure is rerun or BLOCKED under Owner DEC-S02-04. No science, safety, reproducibility or Product v2 guarantee is removed.

**Revision boundary:** This changes **when** S09/S10/S11 apply, not approved 41 Method targets, 68 Scope dispositions, 10 E11 UC, method allocation, shared security invariants, T2/T3 rigor, 07 independence, G10 integration, or mandatory weak-IV full-real AR confidence sets. An unresolved G08-specific AR exact algorithm is a blocker **for G08**, not automatically for G01. Likewise optional DoWhy/EconML/Tigramite research remains assigned to relevant Gates.

## 2. Gate plan and real upstream closure

Preserve prior PREP-03 approved Gate DAG and individual 06/P00 packages:

| Gate | Earlier Gate999 prerequisite | Method count or cross-cutting | Gate-specific pre-code work |
| --- | --- | --- | --- |
| G01 | none | P1-M06 FCI | Common E11 v1 baseline, P1-M06 strict FCI Config/Question/Design, ENV-BASE/causal-learn, MAG/PAG oracle, JCS/Publisher/Reader and Privacy contracts |
| G02 | G01 | P1-M01..05, P1-M07 (6) | identification/IV target, strict profiles, DoWhy feasibility and independent graph/identification proof |
| G03 | G02 | P1-M08..20 (13) | effect/refutation/sensitivity/diagnostics plus native/optional Backend and independent oracles |
| G04 | G02 and G03 | P2-M01..08 (8) | EconML/CATE/conditional-IV structural slope, vector output, inference restrictions |
| G05 | G04 | cross-cutting row export | row authorization, bounded Parquet writer, Method allowlist and original G01 Reader |
| G06 | G01 | P3-M01..03 (3) | temporal/lag semantics, Tigramite, independent temporal oracle |
| G07 | G01 and G02 | P3-M04..06 (3) | DID_2X2 vs STAGGERED deferred, event-time, ITS level/slope HAC |
| G08 | G01 and G02 | P3-M07..11 (5) | RDD/IV, full-real weak-IV AR set and independently authorized exact algorithm |
| G09 | G01 | P3-M12..13 (2) | SCM/SDID non-scalar outputs and SDID inference |
| G10 | all G01..G09 | 41 scientific Method evidence | repository-wide integrated closure, bounded affected-only reruns, protected Product regression |

**G01 is the first Gate.** Its S09 excludes 40 later-Method schemas from G01 *acceptance* but does not exclude common-dispatch unknown Method fail-closed tests. Its `G01_999` must eventually independently PASS before G02/G06/G09, and G07/G08 have their own additional G02 dependency. No unreviewed later-Gate artifact is assumed frozen.

## 3. Required independent S09 evidence under adopted B

For `Gnn`, the reviewer must include an **exact-file source manifest** with classification `COMMON_SHARED / OWN_GATE / UPSTREAM_DEPENDENCY / IMPACT_SAMPLE / DEFERRED_OTHER_GATE`. The last classification is `NOT_REVIEWED` scientifically, though path/version are inventoried. Every actual read must cite full Source SHA+path+line/byte/hash. Reviewer returns:

- For each common and owned file: **reviewed** or `BLOCKED`, precise contradiction/semantics, source SHA and criterion.
- For any shared mutation: impact graph across all frozen downstream consumers; outdated Gate Freeze is stale until impact is re-reviewed.
- S05 pre-code vs future Gate 07/999 evidence distinction, including P1-M06 strict schema, review-only effective ENV-BASE feasibility and independently reviewed MAG/PAG truth/negative scenarios.
- **No** fictitious (T2/T3) PASS, backend-installed claim, actual Reader/FS evidence or independent reference whose code/hash does not exist.
- Separate formal independent reviewer verdict; Author corrections trigger new target commit and **re-review**.

A review of 402 SHA-index entries is **only the inventory**. The B decision eliminates the need to independently *semantically* approve every later Gate before G01. It does not authorize skipping changes in global common/Source ABI that affect G01.

## 4. PREP-04 phase-specific closure

Before G01 S10, G01's contract must be independently reviewable and pre-code feasibility established: specific FCI/Study/Graph strict Schema validation; actual Python3.12 `ENV-BASE` package/API positive/negative feasibility; independently specified executable-oracle route for FCI and independent PAG/MAG truth references, acceptance/negative/pre-registration protocol; secure Publication/Reader type/atomic/root contract; G01 06/Pxx/07 consistency and scoped independent S09 PASS. Actual G01 implementation, true `LocalManifestReader`, full candidate FCI integration/Monte Carlo/T2/T3, real ext4/XFS process tests and v2 regression are **mandatory post-S11 07/999**, not pre-code victories.

For G02+ repeat gate-specific profile/backend/reference preparations and independent scoped S09 before their own S10. No global requirement that all 41 Method post-implementation quantitative slots are populated before G01, and no waiver for later Method G10 science.

## 5. Explicit no-go and next action

**No G01 independent review has run.** No S10 Freeze, no S11 Authorization and no Source/Test/Lock change. Immediate next work: revise independent S09 reviewer scope/Operator controls; pin G01 candidate source+impact inventory; complete G01-specific pre-code blocker/evidence checklist; arrange genuinely independent S09 and Python3.12 review evidence. If a material mathematical choice or changed protected contract needs Owner judgment, present alternatives; do not self-approve.
