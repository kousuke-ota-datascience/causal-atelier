# ENH-E11 — 要件・設計整合性およびトレーサビリティ確認（計画版）

**Document class:** Planning / Decision Artifact  
**Status:** DRAFT / CHECKS PENDING / NO GATE APPROVAL

## 1. Traceability matrix

`E11-REQ-*` and AC IDs below are **temporary planning aliases**, not approved
FR/NFR/AR or frozen 07 Test Items. Issue closure is not Gate PASS.

| Requirement / invariant (draft) | Design realization | Proposed Gate | Proposed AC | GitHub Issue |
|---|---|---|---|---|
| E11-REQ-P1Q; FR-040/041/054, NFR-002 | Versioned local Question/Design/Graph + eligibility and lineage | G01/G02 | AC-01 identity, invalid-design rejection | #15 |
| E11-REQ-P1G; FR-035/037 | FCI registry, PAG circle endpoints, latent warning | G01 | AC-02 endpoint roundtrip / known latent synthetic | #17 |
| E11-REQ-P1I; FR-042/046, AR-023 | Optional DoWhy normalization, separated identification | G02 | AC-03 backdoor/frontdoor/IV identifiable vs nonidentified | #16 |
| E11-REQ-P1R/P1S; FR-049/050 | Additional refuters and sensitivity result protocol | G03 | AC-04 refutation/sensitivity known-truth and seed replay | #16 |
| E11-REQ-P1W; FR-047/048, NFR-016 | IPW/AIPW weighting/inference + existing E9 diagnostic reuse | G03 | AC-05 effect accuracy, coverage, overlap/balance/ESS | #19 |
| E11-REQ-P2 | CATE/HTE protocol, capability-aware EconML estimators | G04 | AC-06 CATE known-truth/compatibility | #18 |
| E11-REQ-P2A | Per-unit Parquet + subgroup/uncertainty/artifact diagnostics | G05 | AC-07 local artifact, support, calibration, privacy | #18, #24 |
| E11-REQ-P3T | TemporalDesign + PCMCI/PCMCI+/LPCMCI | G06 | AC-08 known lags and orientation/CI assumptions | #20 |
| E11-REQ-P3D | QuasiExperimentalDesign + DiD/Event Study/ITS | G07 | AC-09 pretrend, timing, cluster and known effect | #21 |
| E11-REQ-P3I | RD sharp/fuzzy and IV/LATE method-specific estimands | G08 | AC-10 cutoff/manipulation and first-stage/weak-IV | #22 |
| E11-REQ-P3S | Synthetic Control/SDID donor pool and placebo | G09 | AC-11 known effect, RMSPE, donor/contamination | #23 |
| E11-REQ-CLI; NFR-001b/002/025/028 | CLI schema, file manifest, checksum and dependency isolation | G10 (and local all Gate ACs) | AC-12 replay/version/dependency/negative outcomes | #24 |
| 8/4/9月末/current baseline reconciliation | No redundant work; A/B/C/D/E classification and approved delta | Pre-Gate | AC-00 item-level decision/evidence completeness | #14 |

## 2. Current consistency checks

| Check | Current result | Reason |
|---|---|---|
| Requirement vs design | **PENDING** | New FR/NFR/AR semantics, CLI schema and versioning not approved |
| Design vs Gate decomposition | **PENDING** | Architecture Review has not fixed authority or Gate semantics |
| Gate boundaries mutually coherent | **PENDING** | G01–G10 are proposed claims, not 06/07 contracts |
| Transition Debt exits defined | **PARTIAL / PENDING** | Draft future API/DB boundary is explicit, but owner/change plan unapproved |
| Current implementation vs canonical requirements | **PARTIAL COVERAGE** | Previous source audit exists; full item-by-item evidence and fixed-SHA reruns incomplete |

## 3. Unresolved issues and decision blockers

1. Confirm 8/4 mandatory Phase 1–3 algorithms and acceptable replacements
   when a library version does not provide a historical named estimator.
2. Resolve canonical §11 engine exclusion via approved semantic change.
3. Decide question/design/graph identity and versions for DB-free CLI runs.
4. Freeze method-specific inference/coverage benchmark protocols and tolerances.
5. Resolve privacy/default storage and atomic write behavior for CATE Parquet.
6. Review proposed G01–G10 boundaries; dependency and Issue→Gate mappings
   must be regenerated if claims are merged/split.
7. Formal owner approval and later independent fixed-SHA scientific acceptance
   evidence remain absent.

## 4. Conclusion

**NOT READY FOR 06/07 FREEZE OR CODING.** The traceability structure is present,
but unknowns are explicit. Proceed with #14 Architecture Review and owner
approval, then revise 03/04/05 and populate the approved canonical snapshots.
