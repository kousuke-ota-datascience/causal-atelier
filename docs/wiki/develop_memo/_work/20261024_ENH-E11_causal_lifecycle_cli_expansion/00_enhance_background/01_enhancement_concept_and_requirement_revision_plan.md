# ENH-E11 — Enhance構想・要件改定計画

**Document class:** Planning / Decision Artifact  
**Status:** DRAFT / OWNER SCOPE DIRECTION RECORDED / FULL APPROVAL PENDING  
**Date:** 2026-10-24 (Asia/Tokyo)  
**Tracking Issue:** https://github.com/kousuke-ota-datascience/causal-atelier/issues/13

## 1. Problem statement

Historical 2026-08-04 causal lifecycle proposal includes identification, refutation,
sensitivity, heterogeneous treatment effect, time-series causal discovery and
quasi-experimental designs, but the current accepted product implements only a
subset. The 2026-09 ENH-E11 *Foundation Gap Completion* handoff deliberately reduced
scope to residual foundation gaps, excluding Phase 2 CATE and Phase 3 advanced
designs. Subsequent owner direction restored **all mandatory Phase 1–3 capability
families** to ENH-E11, with a narrower execution surface: Scientific Core + local
CLI + durable files. Without explicit reconciliation, already implemented code
would be duplicated and previously excluded new engines could enter the product
without an approved requirement/design contract.

## 2. Why now

- ENH-E7 separated Project / Analysis workspaces; do not couple scientific CLI to
  navigation/page state.
- ENH-E8 separated Causal Identification, Estimation, Effects, Diagnostics and
  Sensitivity stage responsibilities; Navigation Stage is not an Execution Stage.
- ENH-E9 delivered structured weight, balance, overlap and ESS diagnostic records
  and improved workflow; re-use these, do not rewrite them as a new algorithm.
- ENH-E10 established an optional analytical-engine isolation pattern and its
  advanced predictive implementation must not be mistaken for causal CATE.
- Previous Browser E2E cycles were disproportionately costly; a CLI-only boundary
  permits statistical proof primarily through scientific benchmarks.

## 3. Current-state problem and baseline

Reference code/requirements branch: `prototype/ariadne_mvp`; audited source SHA
`84c5a624389b233fcb97c656f1c94d177f459c5a` (current planning reference,
not yet frozen as an ENH-E11 accepted Gate baseline). The local scientific core
already supports DAG/CPDAG/PAG document semantics, Graph/Question/Design,
identification for randomized/backdoor, ATE/ATT estimation including IPW/AIPW,
and placebo/subset refutation and adjustment/clipping sensitivity. E9 persists
IPW diagnostics. Missing or incomplete scope includes DoWhy, FCI, extended
refutation/sensitivity, CATE/HTE estimators, Tigramite and quasi-experimental
design families. FR-051/054 and associated lineage aspects remain partially
implemented. Implementation existence, testing, historical acceptance and fresh
fixed-SHA execution must not be conflated.

The canonical requirement's external-engine exclusion (§11) and the Notion E11
future-phase disposition are **not automatically superseded** by code or this
draft. Requirement semantic changes and scope approval must make that transition
explicit before implementation contracts freeze.

## 4. Target outcome

1. Every mandatory 8/4 Phase 1–3 method is either demonstrably reused, improved,
   newly implemented with scientific verification, or subject to an explicit
   approved equivalent/substitution decision.
2. Users can run supported analysis locally through a strict CLI, with typed
   specification, scientific result state, diagnostics, artifact checksums and
   executable provenance without needing Web UI/API, Worker or DB.
3. Requirements, design decisions, Issues, Gates, independent tests and canonical
   999 PASS evidence can be traced without ambiguous implementation-status claims.

## 5. Scope

### In scope

- **Phase 1:** question/design/graph/versioning/eligibility residuals, optional
  DoWhy identification and refuters, FCI/PAG fidelity, extended refutation and
  sensitivity, current ATE/ATT/IPTW/AIPW scientific quality/diagnostics.
- **Phase 2:** EconML-compatible LinearDML, CausalForestDML, DRLearner,
  ForestDRLearner, S-/T-/X-Learner, and DRIV or scientifically compatible
  IV+ML option; first-class CATE/HTE; cross-fitting, uncertainty, calibration,
  support and policy-ready **file** artifacts (not policy execution).
- **Phase 3:** Tigramite PCMCI, PCMCI+, LPCMCI and CI-test registry;
  DiD, Event Study, RDD sharp/fuzzy, IV/LATE, Synthetic Control, Synthetic DiD,
  Interrupted Time Series with design-specific assumptions, diagnostics and
  known-truth tests.
- Local-only scientific entrypoints, manifest, version/hash/seed/split records,
  result taxonomy, capability/dependency-isolation diagnostics and benchmark
  packages. Existing verified capability is reused wherever scientifically valid.

### Out of scope

- New functionality's Web UI, Web API, Worker and DB integrations;
  Browser E2E as blocking correctness proof for CLI-only methods.
- Phase 4 policy learning/evaluation and automated business decisions,
  capacity/cost constraints, drift monitoring, production approval workflows.
- Nonmandatory 8/4 extension points RPCMCI/J-PCMCI+ and all-library wrapper
  enumeration; broad master lifecycle concept items beyond explicit Phase 1–3
  coding instructions require separate requirement approval.
- Repository-wide unrelated test architecture migration (GitHub Issue #11).

## 6. Requirement changes expected

- Retain implemented FR-035–050/FR-153–156 status for their **existing** semantics;
  do not reinterpret those as proof of DoWhy/FCI/CATE/Phase 3 completion.
- Draft new explicit FR semantics for optional-backend identification/refutation,
  uncertainty-preserving graph discovery, CATE/HTE result, temporal graph,
  quasi-experimental design and local artifact/CLI behaviors.
- Extend NFR-001b/NFR-002 (version/provenance/lineage), NFR-025 (CLI independent
  of navigation), NFR-028 (optional engine isolation) and NFR-015/016
  (testability/scientific transparency) with method-specific acceptance rules.
- Extend AR-005/010/023 and new design-specific integrity constraints: no
  unapproved identification, no DAG fabrication from PAG, no CATE inferred from
  predictive subgroup performance, no weak-IV or invalid RD claims.
- Any new FR/NFR/AR numbering and normative edits are **proposed**, pending
  approval; details in `03_requirements_revision.md`.

## 7. Design changes expected

- Add capability-declared optional Scientific Core adapters, registries and
  method-specific validation, keeping Domain independent from external types.
- Add first-class local Causal/Temporal/Quasi-experimental Design records and
  structured Results with explicit positive/warn/negative/nonidentifiable states.
- Use versioned local specs, Parquet/JSON/Markdown results and manifest fields
  sufficient to reproduce a run without introducing DB models in ENH-E11.
- Keep current Product lifecycle and all current API/Worker/UI behavior intact;
  no silent reinterpretation of stored `causal-analysis-spec/2`.

## 8. Risk / migration / compatibility

- **Scope/size:** Phase 2/3 were explicitly excluded by the old Notion handoff;
  this is a substantive owner-directed expansion, not mere foundation closure.
- **Statistical validity:** estimand heterogeneity, identifiability, time-series
  leakage, staggered DiD, weak instruments, overlap and interval coverage.
- **External engines:** dependency solver/platform/version changes. Optional
  install groups, controlled import and actionable unavailability are required.
- **Backward compatibility:** preserve current CLI aliases (`ipw` etc.),
  manifest readers, existing FR meanings and accepted E9 diagnostic applicability.
- **Security/privacy:** avoid arbitrary dynamic Python imports/pickles and
  unbounded personally identifiable per-unit CATE output by default.
- **Test authority:** fixed-SHA unit/contract/scientific benchmark/integration;
  previously accepted historical 999 PASS is not a substitute for re-execution.

## 9. Architecture-review applicability

- **Required: YES.** New Scientific Core entrypoints, spec/result ownership,
  adapters, graph types/temporal schema, file-based persistence and lineage,
  estimator compatibility and versioning cross current authority boundaries.
- Must decide design metadata identity, file artifact retention/atomicity,
  optional dependency matrix, local CLI execution isolation, and Gate boundaries
  before drafting frozen 06/07.

## 10. Proposed Gate decomposition (DRAFT, acceptance boundaries)

| Gate | Provisional semantic acceptance claim | Issue mapping |
|---|---|---|
| G01 | Versioned local causal context and uncertainty-preserving Graph/FCI identity | #15, #17 |
| G02 | Approved identification and eligibility produce scientifically typed results | #15, #16 |
| G03 | Refutation/sensitivity and IPTW inference/diagnostics independently verifiable | #16, #19 |
| G04 | CATE/HTE estimand and estimator protocol operate with optional EconML | #18 |
| G05 | CATE support, uncertainty and persisted policy-ready files are validated | #18, #24 |
| G06 | Temporal discovery preserves lag/endpoint/assumption semantics | #20 |
| G07 | DiD/Event Study/ITS estimation and pre-trend/time validation contract | #21 |
| G08 | RDD and IV/LATE design-specific identification, local effects and diagnostics | #22 |
| G09 | Synthetic Control/SDID and placebo/donor diagnostics accepted | #23 |
| G10 | Local CLI manifest/provenance/reproducibility and regression/benchmark closure | #24 |

These are provisional *semantic claims*, not fixed Gate count/order. The
Architecture Review may merge/split, recording reasons beyond implementation
workload. Implementation Work Packages are separately determined per Gate.

## 11. Approval required before implementation

- Confirm expansion from the Foundation-only Notion handoff to Phase 1–3 all
  methods and the revised name/CLI-only boundary in `02`.
- Approve precise mandatory method list, equivalence decisions, statistical
  inference methods and acceptable scientific thresholds.
- Approve requirement semantic delta, design ownership, optional package
  policy, CLI artifact contract, privacy policy and proposed Gates.
- Freeze appropriate source SHA and verified evidence; produce 06/07 and 999
  decisions only in their respective workflow stages.

## 12. Provenance

- Historical Phase 1/2/3 instructions: `../20260804_causal_lifecycle_enhancement/03_01...` etc.
- Notion: https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5 (`HANDOFF_DRAFT`).
- Canonical baseline: `docs/wiki/requirement_definition/` at `84c5a624389b233fcb97c656f1c94d177f459c5a`.
- Planning analysis: `06_three_source_reconciliation_matrix.md`;
  Issue index: `07_github_issue_register.md`.
