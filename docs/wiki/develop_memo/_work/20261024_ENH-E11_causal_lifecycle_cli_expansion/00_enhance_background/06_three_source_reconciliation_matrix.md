# ENH-E11 — Three-source Reconciliation Matrix（暫定）

**Document class:** Planning / Evidence Artifact  
**Status:** PRELIMINARY SOURCE-AND-CODE INVENTORY / NO NEW FIXED-SHA RERUN  
**Reference:** `prototype/ariadne_mvp` code; canonical requirements at `84c5a624389b233fcb97c656f1c94d177f459c5a`.

## 1. Comparison axes and authority

- **Historical A (2026-08-04):** Phase 1–3 coding instruction method list,
  architecture proposal and synthetic-test ideas; **not** authoritative current FR.
- **Historical B (2026-09/Notion):** `ENH-E11 Causal Lifecycle Foundation Gap
  Completion`, `HANDOFF_DRAFT`; foundation residuals only; Phase 2/3 excluded.
- **Current C:** canonical FR/NFR/AR Implementation Status, current source and
  auto-test existence, past Gate acceptance (when actually traceable), and later
  fresh execution as **separate** evidence axes.
- **Current owner direction:** all mandatory historical P1–3 methods inside
  ENH-E11, with Scientific Core/local CLI/local file only. This is a planned
  scope expansion relative to Historical B, not retrospective 9月 approval.

Taxonomy: `A_CURRENT_REQUIREMENT_GAP` (current requirement unmet),
`B_NEW_CAPABILITY_CANDIDATE` (new requirement needed), `C_SUPERSEDED`
(baseline already solves equivalent), `D_FUTURE_PHASE` (explicitly deferred),
`E_REJECT` (conflicts with intended product). Mixed rows give primary and
residual separate dispositions rather than treating partial as a single boolean.

## 2. Foundation / Phase 1

| 8/4 item | 9月 Notion E11 | Current FR/implementation evidence | Residual / E11 disposition | Issue |
|---|---|---|---|---|
| Causal Question and version | In-scope residual | FR-040 implemented; canonical spec/model exists | Verify content/version/CLI identity; A if current lineage gap, otherwise C | #15 |
| Causal Design extension | In-scope residual | FR-041 implemented | New CLI-file role/time/assumption semantics only if real gap; C / A? | #15 |
| DAG/CPDAG/PAG and endpoint | In-scope residual | FR-037 implemented, `graph_semantics` preserves endpoint vocabulary | Base graph C; FCI output new B | #17 |
| Identification and negative outcomes | In-scope residual | FR-042/043/046, AR-005/023 implemented for native methods | Existing backdoor C; frontdoor/IV/DoWhy B | #15, #16 |
| Data Eligibility / gate | In-scope residual | FR-044/045 implemented; sample/overlap/typing guards | Existing baseline C; new method-specific checks B | #15, #18–#23 |
| ATE/ATT estimators | In-scope residual | FR-047; diff/OLS/IPW/AIPW adapter and estimator engine | Existing baseline C; inference adequacy VERIFY / A-QUALITY | #19 |
| IPW/IPTW diagnostics | In-scope residual | FR-048; E9 actual weights, arm ESS, balance/overlap tests | Existing weight math C; normalized vs stabilized label / CI quality corrective | #19 |
| Refutation: placebo, subset | In-scope residual | FR-049 implemented with 2 native methods | C (reuse) | #16 |
| Refutation: random common cause, bootstrap | Optional approved adapter | No method in current refutation adapter | B, require approved DoWhy or equivalent | #16 |
| Sensitivity: adjustment/clipping | In-scope residual | FR-050 implemented; two dimensions | C (reuse); confounding sensitivity B | #16 |
| Scientific validation | In-scope residual | FR-044–046 and tests | Extend per new method, B; verify remaining current coverage | #15, #24 |
| FCI / latent confounder | Candidate; no automatic adoption | Discovery algorithms PC/GES/LiNGAM/NOTEARS; no FCI | B; preserve PAG circle endpoints | #17 |
| DoWhy identification | Candidate, not approved mandatory | No active DoWhy backend | B after requirement approval | #16 |
| Provenance/artifacts/lineage | In-scope residual | FR-054 / NFR-001b/002 PARTIAL; local manifest exists | A for current unfilled claims, B for E11 richer local metadata | #15, #24 |
| API/Worker/DB integration | 9月 candidate residual | Existing Product paths available for baseline | **D** for new E11 features by owner decision | #13, #24 |

## 3. HTE / Phase 2 — 9月 Notion explicitly OUT; now adopted

| 8/4 item | 9月 Notion | Current evidence | Residual / E11 disposition | Issue |
|---|---|---|---|---|
| First-class CATE/HTE estimand | Future Enhancement | Current `analysis_spec` and estimation accept ATE/ATT, not CATE | **B**, first-class semantic extension | #18 |
| LinearDML / CausalForestDML | Future Enhancement | Not in current core estimator registry | **B**, optional EconML | #18 |
| DRLearner / ForestDRLearner | Future Enhancement | AIPW is implemented, but not DRLearner | **B**, distinct estimator contract | #18 |
| S-/T-/X-Learner | Future Enhancement | Not first-class causal estimators | **B** | #18 |
| DRIV or compatible IV+ML | Future Enhancement | No approved IV+ML adapter | **B**; separate from P1 identification/P3 LATE | #18 |
| Cross-fitting, nuisance/final model/split evidence | Future Enhancement | Existing AIPW uses optional crossfit; not EconML spec | Reuse portions C; new contract B | #18, #24 |
| CATE support/overlap/calibration/stability and uncertainty | Future Enhancement | Generic E9 overlap/ESS reusable; CATE-specific no | **B** | #18, #24 |
| Per-unit CATE Parquet and policy-ready artifact | Future Enhancement | No CATE artifact in active CLI | **B**; not policy execution | #18, #24 |

## 4. Temporal and quasi-experimental / Phase 3 — 9月 Notion OUT; now adopted

| 8/4 item | 9月 Notion | Current evidence | Residual / E11 disposition | Issue |
|---|---|---|---|---|
| PCMCI / PCMCI+ / LPCMCI and CI registry | Future Enhancement | No Tigramite methods in scientific discovery registry | **B** | #20 |
| TemporalDesign / TIME_SERIES_GRAPH | Future Enhancement | Current graph enum lacks time-series graph type | **B** | #20 |
| DiD / Event Study | Future Enhancement | Not causal CLI design estimator | **B** | #21 |
| Interrupted Time Series | Future Enhancement | Not causal CLI design estimator | **B** | #21 |
| RDD sharp / fuzzy | Future Enhancement | Not causal CLI design estimator | **B** | #22 |
| IV / LATE / weak-IV contract | Future Enhancement | No design-specific estimator; current backdoor is not IV | **B** | #22 |
| Synthetic Control / Synthetic DiD | Future Enhancement | No native donor estimator or placebo workflow | **B** | #23 |
| Design-specific validity and benchmark artifacts | Future Enhancement | Existing generic diagnostics not sufficient | **B** | #21–#24 |
| RPCMCI/J-PCMCI+ extension | Extension only in 8/4, not required P3 | Not implemented | **D**, extension point only | #13 |
| Policy evaluation, monitoring, drift | Future/Phase 4 | Not E11 CLI methods | **D**, explicitly excluded | #13 |

## 5. Evidence and completion discipline

These rows are **not** fixed-SHA test certification. To complete Issue #14,
expand each row with the exact FR/NFR/AR citation, code function/path, unit/
component/integration/scientific benchmark path, prior 999 Gate evidence when
available, and fresh execution status. Missing historical PASS must be `NOT
LOCATED`, not assumed. Correctly separate `IMPLEMENTED`, `PARTIAL`, `ABSENT`,
`TEST_EXISTS`, `HISTORICAL_ACCEPTED`, `RERUN_PASS/FAIL/BLOCKED`.

## 6. Design conflicts requiring approved resolution

1. Current canonical requirements §11 excludes unapproved DoWhy/EconML;
   new optional backend adoption requires explicit requirement change.
2. Notion `HANDOFF_DRAFT` excludes P2/P3; owner has subsequently expanded scope;
   update concept approval and nomenclature without rewriting history.
3. Current `causal-analysis-spec/2` only supports ATE/ATT and particular methods;
   use versioned additive contracts, not silently widened legacy enums.
4. Product metadata/DB lineage and E11 DB-free file manifest cannot be treated
   as the same identity without Architecture Review.
5. Phase 1 identification IV, Phase 2 IV+ML and Phase 3 LATE have different
   causal and statistical contracts. They require separate tests and result tags.
