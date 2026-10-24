# ENH-E11 Gate Decomposition (Provisional)

**Document class:** Planning / Operator Artifact  
**Status:** DRAFT / Architecture Review and human approval pending

## 1. Decomposition principle

Each Gate is a **semantic acceptance boundary** on which a downstream method
or user can rely. Execution workload, the number of files/Issues or Agent
context size only determines Work Package splitting, not new Gates. Formal
authority is the eventual frozen Gate-local 06/07 and independent 999 decision.

## 2. Proposed Gates

| Gate | Acceptance claim | Entry prerequisites | Protected on PASS | Issue(s) |
|---|---|---|---|---|
| G01 | Local causal context/Graph uncertainty and FCI endpoints are reproducible | Approved local context/Graph schema | Typed spec/hash + PAG fidelity | #15, #17 |
| G02 | Identification/eligibility with optional DoWhy safely gates estimation | G01 semantics as applicable | Native/DoWhy normalized identification and scientific negatives | #15, #16 |
| G03 | Refutation, sensitivity and existing IPTW/AIPW diagnostics/inference are scientifically accepted | G02 compatible identification | Effect/refuter/sensitivity scientific integrity | #16, #19 |
| G04 | First-class CATE/HTE estimand plus EconML estimator capabilities run | G02 identification, G03 diagnostic reuse | CATE result model + approved estimator families | #18 |
| G05 | CATE support/calibration/uncertainty and privacy-preserving files are accepted | G04 estimator result | Policy-ready file artifact and HTE diagnostics | #18, #24 |
| G06 | Temporal graphs/discovery preserve lag and uncertainty | G01 GraphSchema decisions | TIME_SERIES_GRAPH and PCMCI-family validation | #20 |
| G07 | DiD/Event Study/ITS design-specific estimates and diagnostics accepted | Approved quasi-experimental design | Timing/pretrend/cluster/ITS result contract | #21 |
| G08 | RDD and IV/LATE local estimands with design validation accepted | Approved design & identification semantics | RD/IV result and weak-identification safeguards | #22 |
| G09 | Synthetic Control/SDID donor/counterfactual/placebo semantics accepted | Approved donor design | Synthetic methods/result diagnostics | #23 |
| G10 | Method CLI/manifest/benchmark regression achieves end-to-end local reproducibility | Accepted method Gate results | All approved method files replayable with checksums | #24 |

## 3. Ordering rationale

G01–G03 establish portable context, identification and baseline inference;
G04–G05 build HTE/CATE. Temporal G06 and quasi-experimental G07–G09 may have
different dependencies once design schema is reviewed. The cross-cutting CLI
artifact contract is needed **early** but its end-to-end program acceptance
cannot be PASS before required method results are accepted. Gate ordering
and split may therefore change at Architecture Review.

## 4. Final convergence condition

All mandatory P1–3 methods are either already verified/traceably reused or
accepted via a method-specific 999 PASS, and G10 proves local file results,
manifest provenance and reproducibility at fixed SHA. Accepted requirements
and design own the method inventory; Issue closure never replaces Gate PASS.

## 5. Forbidden parallelization

- Do not implement P2 CATE against an unidentified or schema-ambiguous estimand.
- Do not implement LPCMCI temporal endpoints before graph semantics are agreed.
- Do not freeze RDD/IV/Synth result semantics before design-specific assumptions
  and negative-result contracts are approved.
- Do not treat multiple Issues as independent Gates when they only partition
  execution workload; use Work Packages instead.

## 6. Outstanding review questions

- Whether G04/G05 are truly separate acceptance claims or one Gate plus Pxx.
- Whether G07–G09 should be grouped by common design authority with independent
  Work Packages and subtests.
- Whether G10 manifest acceptance should be incorporated into each Gate before
  final program integration rather than a single downstream blocker.

**All Gate identities and the dependency table are PROPOSED, not frozen.**
