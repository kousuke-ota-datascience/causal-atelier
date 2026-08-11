# ENH-E5 既存実装・設計整合性レビュー

- 状態: `PHASE_H_UPDATED / REMEDIATION_FROZEN`
- 対象branch: `feature/ariadne_mvp_e5`
- Historical planning pin: `46122c68333df03680b97c253a7b5d32bf9393e7`
- ENH-E4 completion alignment baseline: `a770cc4f38137063cd5f22d8035e91e3c63b7502`
- 詳細evidence:
  - `40_operator_workflows/preflight_analysis/ENH-E5_nonchange_alignment_audit_report.md`
  - `40_operator_workflows/preflight_analysis/ENH-E5_nonchange_requirement_alignment_matrix.csv`
  - `40_operator_workflows/preflight_analysis/ENH-E5_nonchange_design_alignment_matrix.csv`
  - `40_operator_workflows/preflight_analysis/remediation_decision_log.md`
  - `40_operator_workflows/preflight_analysis/remediation_decision_matrix.csv`

## 0. Purpose

本書は詳細source監査を複製するものではない。

役割:

1. ③-1（E4→E5非変更部分）と①（ENH-E4完了実装）のalignment review結果をsummaryする。
2. Case diagnosisとD1/D2/D3 final dispositionをplanning layerへ接続する。
3. 詳細evidenceのindexを提供する。
4. Phase I canonical docs改訂とNFR-019再監査へのtraceを定義する。

## 1. Authority / baseline rule

alignment auditのsource-of-truth baseline:

```text
a770cc4f38137063cd5f22d8035e91e3c63b7502
```

historical planning pin:

```text
46122c68333df03680b97c253a7b5d32bf9393e7
```

この2つを混同しない。

③-1 ↔ ① alignment判定ではENH-E4 completion baselineをauthorityとする。

## 2. Audit question

物件:

- ① ENH-E4完了実装
- ② ENH-E4完了文書
- ③ ENH-E5文書
  - ③-1 E4→E5非変更部分
  - ③-2 E5変更部分

主目的:

> ③-1が①を正確に記述しているか。

②はdiscrepancy diagnosisに利用するがsource of truthではない。

Alignment:

- MATCH
- PARTIAL_MATCH
- MISMATCH
- UNVERIFIED
- TARGET_CHANGE

Case:

- Case A: ②=①, ③-1≠①
- Case B: ②=③-1, ①≠②
- Case C: 全て不一致
- Case D: ③-1=①, ②≠①

今回の非MATCHは基本的にCase Bとしてremediationを裁定した。

## 3. Audit coverage

remediation matrixがcoverする元監査非MATCH集合:

| Source Type | Alignment | Unique Source IDs |
|---|---|---:|
| Requirement | MISMATCH | 24 |
| Requirement | PARTIAL_MATCH | 33 |
| Requirement | UNVERIFIED | 1 |
| Design | MISMATCH | 6 |
| Design | PARTIAL_MATCH | 3 |

Total unique Source IDs: **67**

remediation Decision Item:

| Decision | Rows |
|---|---:|
| D1 | 31 |
| D2 | 35 |
| D3 | 28 |
| Total | 94 |

log ↔ matrix Decision Item/Source/Decision/Substatement/Delivery/TD Refの機械差分は0。

## 4. Final remediation taxonomy

### D1 — CURRENT_IMPLEMENTATION

current implementationをcurrent contractとして採用し、③-1/Requirement/Designをsource-alignedに訂正する。

### D2 — E5_TARGET_CHANGE

current implementationには不足しているが、ENH-E5で実装するtargetとして③-2へ置く。

### D3 — DEFER

要求方向は維持するがENH-E5では実装しない。

Requirement正本では:

```text
Requirement Status = DEFERRED
Delivery = FUTURE
```

詳細は90 ledger。

D1/D2/D3はRequirement Levelとは別軸。

## 5. Formal freeze status

remediation freeze auditでblockerだった次の4件は、2026-08-12にHuman ownerがD3/FUTUREを明示承認した。

- `FR-122`
- `FR-126`
- `D10-006a`
- `D10-006b`

したがってPhase Hではremediation decision baselineを**FROZEN / PASS相当**として扱う。

Repository上の`remediation_decision_freeze_audit.md`と90 ledgerを同期する際は、このapproval traceを反映する。

## 6. D1 current contract correction summary

主なcurrent correction:

### 6.1 Ownership / resources

- `decision_context`はResearchContextVersion責務。
- canonical Executionに独立`execution_plan_id` columnを捏造しない。
- retryはStageAttempt append-only。
- Result/Artifact direct fieldsをcurrent modelへ合わせる。
- Result status matrixをcurrent enumへ合わせる。
- GraphVersion origin/reference invariantをcurrent sourceへ合わせる。
- simple AnnotationとWorkspaceAnnotationを分離する。
- canonicalization / schema registry semanticsをsourceへ合わせる。

### 6.2 Runtime / workflow

- Causal current runtimeはone-operation/one-stage compatibility plan。
- Predictive planは`split -> prepare -> train -> evaluate -> optional explain`。
- Exploratory plannerはoperationごとに1 runtime Stage。
- PlanValidator/StageRunnerRegistry responsibilityをcurrent sourceへ合わせる。
- Worker claim/lease contractをrepository/current fieldsへ合わせる。
- 架空のruntime event contractを除去する。

### 6.3 Interface / architecture

- current role taxonomyはOWNER/EDITOR/VIEWER。
- Bearer/OIDCをcurrent common contractとして捏造しない。
- current CLIをgeneric Product orchestration CLIと誤記しない。
- API route/filter/idempotency coverageをendpoint実装に合わせる。
- current Port setだけを記述する。
- current architectureから未実装Outboxを除去する。
- object-storage adapterをcurrent implementationとしない。

### 6.4 Result / Artifact / Lineage

- Result/Artifact responsibilityをcanonical modelへ合わせる。
- Predictive metric/error等をすべてArtifactとしない。
- lineage relation authorityをcurrent classifierへ合わせる。

## 7. D2 target summary

D2 35 Decision ItemはPhase Gで11 freeze packageへ完全収束した。

```text
PF-D2-01 Typed Filter Validation
PF-D2-02 Exploratory Handoff & Provenance
PF-D2-03 Predictive Subgroup Evaluation
PF-D2-04 Scientific Comparability & Exploratory-Reuse Guard
PF-D2-05 Command Idempotency & Retry-safe Artifact Commit
PF-D2-06 Project Authorization & Sensitive Output Boundary
PF-D2-07 Canonical Lineage Completion
PF-D2-08 Reproducibility Metadata Completion
PF-D2-09 Frontend Deep Navigation, Action State & Accessibility
PF-D2-10 Derived E5 Test Architecture
PF-D2-11 Documentation Self-containment & Navigation Architecture Freeze
```

Remaining unresolved planning decision: **0**

D2は「current implementationに存在しない」ことを理由に削除しない。

## 8. Navigation target is intentionally not current-aligned

次はENH-E5 targetであり、current sourceに存在しないこと自体はalignment failureではない。

- Family top tabs
- Family-local Navigation Stage sidebar
- FamilyNavigationDescriptor / NavigationStageDescriptor
- backend Navigation catalog endpoint
- exact Family/Stage route
- default Stage
- legacy route normalization
- resource deep route
- frontend Family/Stage renderer binding

ただし既存runtime contractを壊してはならない。

Frozen boundary:

```text
Navigation Stage != Execution Stage
Navigation state authority = URL/Application
No Navigation persistence to AnalysisSpecification/Execution
No Navigation-driven runtime Stage generation
```

## 9. D3 isolation summary

D3はcurrent/E5 targetへ復活させない。

主要group:

- audit / retention
- system operator authorization
- sensitive metadata/configurable governance
- Exploratory surface expansion
- automated hyperparameter selection
- Product orchestration CLI
- component readiness
- resource hard limits
- p95 performance gate
- object storage
- cross-store compensation
- production auth/security hardening
- restart/resume semantics
- observability overhaul
- schema-example synchronization

Human approval済みD3 blocker:

`FR-122 / FR-126 / D10-006a / D10-006b`

## 10. Preflight detail index

本書へ詳細source evidenceを複製しない。

| Detail | Preflight artifact |
|---|---|
| ③-1 ↔ ① overall audit | `ENH-E5_nonchange_alignment_audit_report.md` |
| Requirement per-ID evidence | `ENH-E5_nonchange_requirement_alignment_matrix.csv` |
| Design per-ID evidence | `ENH-E5_nonchange_design_alignment_matrix.csv` |
| D1/D2/D3 human-readable decision | `remediation_decision_log.md` |
| machine-readable decision | `remediation_decision_matrix.csv` |
| freeze audit | `remediation_decision_freeze_audit.md` |
| D2 exact planning decisions | `d2_planning_decision_freeze.md` / `.csv` |
| NFR-019 documentation audit | `nfr_019_documentation_self_containment_audit.md` |
| D3 future ledger | `90_technical_debt_and_future_enhancements.md` |

## 11. Phase I obligations

Phase Iでは次を実施する。

### 11.1 10 Requirements

- D1 current wording correction
- D2 ACTIVE / ENH-E5
- D3 DEFERRED / FUTURE
- Area / Requirement Status / Implementation Status / Delivery
- timing-dependent wording除去

### 11.2 21/22/23/30 Design

- D1 current correction
- Phase G D2 exact contract
- D3 current target exclusion
- Navigation architecture exact freeze
- `StageAttempt.effective_random_seed` migration
- D2-derived test architecture

## 12. NFR-019 trace

current v5 documentation audit:

`PARTIAL_MATCH / FAIL`

理由:

- current/targetのself-contained性不足
- G00/G01等へのnormative delegation
- Navigation exact decisionの未freeze記述
- D1/D2/D3未反映

Phase GでNavigation planning decisionはfreeze済み。

Phase Iでcanonical docsへ反映した後:

1. cross-document consistency review
2. `DOC-019-01〜08` re-audit
3. all PASS
4. その後にのみ`06/Pxx/07` final freeze

## 13. Final verdict

**PHASE H ALIGNMENT DISPOSITION: FROZEN**

意味:

- alignment evidence collectionは完了。
- Case diagnosisは完了。
- D1/D2/D3裁定は完了。
- formal D3 approval blockerは解消。
- D2 planning decisionはFROZEN。
- 次に必要なのはPhase I canonical docs改訂であり、追加source再監査ではない。

ただし、Phase Lでは③-1 ↔ ① final re-auditを再実施する。
