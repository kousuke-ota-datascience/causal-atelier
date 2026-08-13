# ENH-E6 Current State Control Sheet

**Document class:** State / Control Artifact  
**Self-containment:** MUST for verified-current-state responsibility.

## 1. Purpose and authority

本書はENH-E6のverified current state control planeである。final PASS済みevidence、またはGate execution prerequisiteとして独立に確認済みのbaseline factのみを記録する。planned implementation、package progress、post-fix expectationをverified stateへpromotionしない。

## 2. Verified baseline

- Branch: `bugfix/ariadne_mvp_e6`
- Production behavior baseline: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
- Template-compliance audit input / frozen instruction commit: `42df32decaa67b9de8c6cab518d441cf0a2f8fe4`
- Source anomaly: `ENH-E5 / ANOM-E5-001`
- Canonical product requirements/design: `docs/wiki/requirement_definition/**` — READ ONLY for ENH-E6

## 3. Verified current architecture / behavior

| ID | Verified fact | Evidence / provenance |
|---|---|---|
| E6-CS-001 | ENH-E5 G01 historical Gate Decision is PASS; its evidence chain is immutable | ENH-E5 frozen 06/07 + final Gate Decision |
| E6-CS-002 | ENH-E5 closeout records `ANOM-E5-001` as follow-up bugfix anomaly | ENH-E5 technical-debt ledger |
| E6-CS-003 | Family tab / Stage sidebar DOM and renderer code exist | `frontend/index.html`, `frontend/app.js` source inspection |
| E6-CS-004 | canonical analysis route restore invokes analysis navigation rendering | `frontend/app.js` source inspection |
| E6-CS-005 | normal workspace activation can update navigation/history without converging on same shell-render lifecycle | `frontend/app.js` source inspection |
| E6-CS-006 | baseline has Family-only `causal -> discovery` presentation mapping | `frontend/app.js` source inspection |
| E6-CS-007 | existing browser harness is Playwright Python / Chromium through `browser-e2e` compose service | Dockerfile/compose/runner inspection |
| E6-CS-008 | API READY clean Project context reaches canonical `.../analysis/exploratory/profile` on normal Explore entry | 2026-08-13 preflight probe |
| E6-CS-009 | same clean baseline has Family tab container=1 but Family buttons=0 and Stage buttons=0 | 2026-08-13 preflight probe |

Post-fix Family/Stage correctness is not yet verified.

## 4. Authority map

| Concern | Authority |
|---|---|
| Canonical product requirement/design | `docs/wiki/requirement_definition/**` (read-only upstream) |
| ENH-E6 planning/design rationale | `00_enhance_background/**` |
| Gate-wide implementation semantics | frozen G01 `06` |
| Independent acceptance semantics | frozen G01 `07` |
| Work Package decomposition | G01 `P00` (Human/operator only) |
| Assigned Coding execution | assigned `Pxx` only |
| Package implementation evidence | `20_implementation_reports/**` |
| Gate verification / decision | `30_test_report/**` |
| Operator routing/preflight/architecture evidence | `40_operator_workflows/**` |
| Verified current-state index | this document |

## 5. Passed-Gate protected contracts

- ENH-E5 frozen Gate contracts, implementation reports, test reports, Gate Decision are immutable historical evidence.
- ENH-E5 canonical Family/Stage semantics preserved by ENH-E6: Family values, backend catalog authority, canonical route model, `Navigation Stage != Execution Stage`, Navigation Context non-persistence, affected operation-availability semantics.
- G01 has not yet PASSed; ENH-E6 post-fix behavior is not protected/verified state yet.

## 6. OPEN Transition Debt register

| Debt / anomaly | Status | Exit condition |
|---|---|---|
| `ANOM-E5-001` Family Tab Observable UI Gap | OPEN / IN_SCOPE | ENH-E6 G01 final PASS with blocking real-browser evidence |
| Legacy analysis left navigation retained as compatibility surface | ACCEPTED TEMPORARY / E6 boundary | E6 requires compatibility-only authority; complete IA removal is future scope |

## 7. Closed Transition Debt

None in ENH-E6 at this point. Do not mark `ANOM-E5-001` closed before G01 final PASS.

## 8. Prerequisite / Preflight status

- Status: `PASS_FOR_G01_EXECUTION`
- API health: `API READY`
- Project fixture: UI-created/selected successfully
- Canonical Explore entry: `/projects/<id>/analysis/exploratory/profile`
- Negative control: Family buttons=0, Stage buttons=0
- Browser framework: Playwright Python / Chromium
- Canonical invocation pattern: existing `browser-e2e` compose service confirmed
- Detailed preflight artifact: `40_operator_workflows/preflight/`

## 9. Active Gate control

- Gate: `G01`
- 06: `APPROVED / FROZEN`
- 07: `APPROVED / FROZEN`
- Execution Mode: `WORK_PACKAGE`
- Trial: `Trial01` not yet started by Coding Agent after template-compliance update
- Next package: `P01`
- P02: waits for P01 checkpoint
- P03: waits for required P01/P02 checkpoints
- Candidate: not assembled
- Gate Decision: not executed

Coding Agent entry must use the canonical Work Package operator prompt with `GATE_ID=G01`, `PACKAGE_ID=P01`, `TRIAL_NO=01`. Coding Agent must not read G01 07/P00/06/other Pxx for specification completion.

## 10. Evidence index

| Evidence | Identity / path | Meaning |
|---|---|---|
| Production baseline | `5a5ced9bd6a0e62027c4058eb66ec487719bde23` | source/behavior baseline under investigation |
| Frozen docs audit input | `42df32decaa67b9de8c6cab518d441cf0a2f8fe4` | pre-template-compliance instruction state |
| ENH-E5 anomaly provenance | ENH-E5 `90_technical_debt_and_future_enhancements.md` | source anomaly |
| Source alignment review | `00_enhance_background/06_existing_implementation_design_alignment_review.md` | implementation facts/root-cause classification |
| Architecture review | `40_operator_workflows/architecture_review/**` | lifecycle/authority decision provenance |
| Preflight | `40_operator_workflows/preflight/**` | clean negative-control/runtime prerequisite evidence |
| G01 contracts | `10_enhance_instruction/G01/06_*`, `07_*` | frozen Gate semantics |

## 11. Update log

| Timestamp | Update | Promotion class |
|---|---|---|
| 2026-08-13 | Initial ENH-E6 baseline and ENH-E5 anomaly inheritance recorded | baseline fact |
| 2026-08-13 | API READY clean browser negative control reproduced | prerequisite/runtime fact |
| 2026-08-13 | G01 06/07 frozen after Human review | contract state, not Gate PASS |
| 2026-08-13 | Template-compliance/auditability remediation prepared; Pxx normative-source isolation corrected | governance/documentation, not product verification |

### Update rule

Only final independent PASS may promote ENH-E6 implementation behavior to verified current state. Package checkpoint, Coding Agent self-check, candidate assembly, or browser preflight alone must not be described as G01 PASS.
