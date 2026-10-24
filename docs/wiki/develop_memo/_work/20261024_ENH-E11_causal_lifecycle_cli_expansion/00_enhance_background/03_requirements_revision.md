# ENH-E11 — 要件定義書改定案

**Document class:** Planning / Decision Artifact  
**Status:** DRAFT REQUIREMENT SEMANTIC DELTA / NOT APPROVED  
**Rule:** Temporary `E11-REQ-*` identifiers are planning references **only**;
no official FR/NFR/AR numbers are assigned until canonical approval.

## 1. Source documents

- `docs/wiki/requirement_definition/00_product_concept_memo.md`
- `docs/wiki/requirement_definition/10_requirements_definition.md` (canonical
  implementation-status correction at `84c5a624389b233fcb97c656f1c94d177f459c5a`)
- `docs/wiki/requirement_definition/{21,22,23,30}_*.md`
- Historical `20260804_causal_lifecycle_enhancement/03_01..03_03` (proposals)
- [ENH-E11 Notion handoff](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5) (HANDOFF_DRAFT)
- `06_three_source_reconciliation_matrix.md` and Issue #13.

## 2. Proposed semantic deltas (Before → After)

| Planning ID | Current canonical before | Proposed E11 after | Why / Issue |
|---|---|---|---|
| E11-REQ-P1Q | FR-040/041 fix Question/Design semantics; FR-054 and NFR-002 partial lineage | Version/content-hash aware Question/Design/Graph identity in standalone CLI file contract; model may reuse existing Product versions | Reuse/close residuals #15 |
| E11-REQ-P1I | FR-042/043/046 and AR-005/023 have current randomized/backdoor identification | Pluggable optional backdoor/frontdoor/IV backend and explicit unsupported/nonidentified status, with untestable assumptions recorded | DoWhy semantic addition #16 |
| E11-REQ-P1G | FR-035/037 include multi-algorithm discovery and endpoint schema | FCI optional discovery retaining PAG circles/latent warnings; never orient to DAG silently | New algorithm #17 |
| E11-REQ-P1R | FR-049 covers Placebo and Data Subset | Add Random Common Cause and Bootstrap refutation and canonical refuter provenance | New methods #16 |
| E11-REQ-P1S | FR-050 covers adjustment-set and clipping sensitivity | Include scientific confounding scenarios/method applicability where approved; keep existing sensitivities | New scope #16 |
| E11-REQ-P1W | FR-047/048 cover ATE/ATT interval and applicable diagnostics; existing IPW | Define normalized Hájek/IPTW weights, ATE/ATT, inference uncertainty quality, balance/ESS/overlap applicability | Quality/inference #19 |
| E11-REQ-P2 | No current FR for first-class CATE/HTE, EconML and heterogeneous inference | CATE/HTE specification/result, approved estimators, effect modifier vs confounder, inference and subgroup support | Phase2 newly adopted #18 |
| E11-REQ-P2A | No current canonical CATE artifact requirement | Policy-ready **file** Parquet/JSON CATE and aggregate summaries with privacy limit, seeds, splits and versions | Phase2 artifacts #18/#24 |
| E11-REQ-P3T | No dedicated time-series graph/discovery FR | TemporalDesign, TIME_SERIES_GRAPH lag semantics, PCMCI/PCMCI+/LPCMCI, applicable CI tests and fidelity | Phase3 new #20 |
| E11-REQ-P3D | No dedicated causal DiD/Event/ITS FR | QuasiExperimentalDesign with DiD, Event Study, ITS, pre-trend/event-time and cluster validation | Phase3 new #21 |
| E11-REQ-P3I | Current randomized/backdoor Identification not equivalent to design-specific IV | Sharp/fuzzy RDD local estimand and IV/LATE first-stage/weak-IV, relevance/exclusion/monotonicity declarations | Phase3 new #22 |
| E11-REQ-P3S | No donor-panel Synthetic Control/SDID FR | Donor eligibility, pre-fit, treatment timing, placebo, donor weights and negative result contracts | Phase3 new #23 |
| E11-REQ-CLI | Existing NFR-001b/002 partial; NFR-025 and NFR-028 implemented for current surface | Local only versioned spec, hash/manifest, backend/runtime/dependency version, deterministic seed/split, durable artifacts, typed scientific outcome | Cross-cutting #24 |

**External-engine conflict:** canonical requirement §11 excludes DoWhy/EconML
as unapproved engines for the prior baseline. Adoption by ENH-E11 requires a
documented change from exclusion to *approved optional capability*, not a
silent assertion that current FR already requires these packages. Tigramite and
other additional libraries require the same explicit dependency policy.

## 3. Proposed invariants and constraints

1. **Identifiability first:** Estimation/CATE/causal-design execution only on an
   identified estimand, applicable design, and eligible sample. Diagnostic
   failure is not a technical execution failure.
2. **Graph fidelity:** PAG/CPDAG uncertainty and temporal lag orientation are
   preserved; no forced conversion for downstream compatibility.
3. **Estimator semantics:** ATE/ATT/CATE/LATE/local RD estimands are not treated
   as interchangeable; predictive subgroup scores are not CATE.
4. **Weight semantics:** IPW estimator analysis weights versus AIPW propensity
   components are distinct. Normalized Hájek weights, stabilized numerator and
   clipping/trimming policy must be identified separately.
5. **Quasi-experimental assumptions:** staggered adoption, pretrend, exclusion,
   weak IV, RD density and donor contamination produce explicit scientific
   diagnostics; assumptions cannot be proven by software.
6. **Optional engines:** Domain/Spec/Result never contain raw DoWhy/EconML/
   Tigramite objects. Missing extras fail only selected capability and report
   actionable error and version provenance (NFR-028).
7. **Local execution:** No new E11 API/Worker/DB/UI. Legacy Product behavior,
   schema `causal-analysis-spec/2`, current standalone CLI configurations and
   previously accepted Result readers remain compatible or have approved version
   transitions.
8. **Privacy/reproducibility:** Row-level CATE is explicit opt-in or under a
   documented minimization policy; no arbitrary pickle/code import. Manifest
   records inputs, version, seeds/splits, outputs, checksum and scientific status.

## 4. Removed or deprecated requirements

None approved. Historical September E11 **scope exclusions** for Phase 2/3 are
proposed to be superseded **for ENH-E11 only** by the owner's later direction.
This does not remove any current Product FR. Proposal to rename the Enhancement
requires human confirmation.

## 5. Acceptance implications (DRAFT)

| Method group | Primary scientific proof | Negative / edge proof |
|---|---|---|
| Backdoor/frontdoor/IV and FCI | Known-truth DAG/PAG identification; endpoint round-trip | Nonidentifiable graph, unavailable library, latent ambiguity |
| IPTW/AIPW | Known-truth ATE/ATT and interval coverage; E9 diagnostics regression | Poor overlap, extreme weights, clipping, score uncertainty |
| EconML CATE/HTE | Known heterogeneous-effect synthetic benchmarks and estimand compatibility | Poor subgroup support, invalid treatment type, crossfit leakage |
| PCMCI family | Known-lag time-series graph tests with seed/CI versions | Irregular time, wrong lag, latent warnings |
| DiD/Event/ITS | Known intervention effects and pretrend/cluster diagnostics | Pretrend violations, staggered adoption hazards, autocorrelation |
| RDD/IV/LATE | Local effect/strong-IV known truth and bandwidth/first-stage reporting | Manipulation, weak/invalid instrument, fuzzy configuration |
| Synthetic Control/SDID | Known donor-panel effect, RMSPE and placebo diagnostics | Poor prefit, donor contamination, weak support |
| CLI/provenance | Fixed-seed rerun, artifact/manifest checksums, method contracts | Missing optional extra, invalid spec, negative scientific status |

Exact dataset generators, tolerances, resample counts, clustering rules and
confidence coverage thresholds must be fixed in approved 07 before coding.

## 6. Open decision blockers

- Which new official FR/NFR/AR IDs and Product concept changes are approved?
- What are scientifically defensible default SE/inference and trimming options?
- Which IV+ML estimator is the approved Phase 2 equivalent (DRIV vs alternative)?
- How are per-unit CATE artifacts minimized, encrypted or restricted locally?
- What local spec and manifest schema/version boundary preserves backward reads?
