# ENH-E11 — GitHub Issue Register / Scope-to-Contract Map

**Document class:** Planning / Evidence Artifact  
**Status:** ISSUES REGISTERED / SCOPE-TO-GATE MAPPING PROVISIONAL  
**Repository:** https://github.com/kousuke-ota-datascience/causal-atelier  
**Reference Issue format:** [#11](https://github.com/kousuke-ota-datascience/causal-atelier/issues/11) — all E11 issues use `Problem / Goal / Proposed Design / Acceptance Criteria / Related / Result / Memo` and scientifically specific acceptance evidence.

## 1. Issue index

| Issue | Phase | Description | Proposed Gate | Disposition |
|---|---|---|---|---|
| [#13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13) | Program | All-Phase CLI-first scope, authority and child tracking | All / pre-Gate | Planning |
| [#14](https://github.com/kousuke-ota-datascience/causal-atelier/issues/14) | Planning | Historical 8/4 × Sep E11 × current baseline reconciliation, architecture review | Pre-Gate | A/B/C/D/E classification |
| [#15](https://github.com/kousuke-ota-datascience/causal-atelier/issues/15) | Phase 1 | Question/Design versions, identification/eligibility residuals | G01, G02 | Reuse / conditional gap |
| [#16](https://github.com/kousuke-ota-datascience/causal-atelier/issues/16) | Phase 1 | DoWhy, frontdoor/IV, refutation, sensitivity extension | G02, G03 | New optional backend |
| [#17](https://github.com/kousuke-ota-datascience/causal-atelier/issues/17) | Phase 1 | FCI/PAG/latent and endpoint fidelity | G01 | New discovery algorithm |
| [#19](https://github.com/kousuke-ota-datascience/causal-atelier/issues/19) | Phase 1 | Existing IPTW/AIPW inference and diagnostics integrity | G03 | Reuse / quality validation |
| [#18](https://github.com/kousuke-ota-datascience/causal-atelier/issues/18) | Phase 2 | EconML CATE/HTE, DML/DR/meta/IV+ML, support and artifacts | G04, G05 | New (Sep Notion excluded) |
| [#20](https://github.com/kousuke-ota-datascience/causal-atelier/issues/20) | Phase 3 | Tigramite PCMCI/PCMCI+/LPCMCI and temporal graphs | G06 | New (Sep Notion excluded) |
| [#21](https://github.com/kousuke-ota-datascience/causal-atelier/issues/21) | Phase 3 | DiD, Event Study, Interrupted Time Series | G07 | New (Sep Notion excluded) |
| [#22](https://github.com/kousuke-ota-datascience/causal-atelier/issues/22) | Phase 3 | RDD sharp/fuzzy, IV/LATE | G08 | New (Sep Notion excluded) |
| [#23](https://github.com/kousuke-ota-datascience/causal-atelier/issues/23) | Phase 3 | Synthetic Control, Synthetic DiD | G09 | New (Sep Notion excluded) |
| [#24](https://github.com/kousuke-ota-datascience/causal-atelier/issues/24) | Cross | CLI schema, manifest, local artifacts and scientific acceptance | G05/G10 and all | Shared enablement/verification |

## 2. Planned dependency order

1. **#14** must resolve current architecture/requirements and owner's full
   approval; it is a blocking **planning** prerequisite, not a Gate itself.
2. **#15, #17** stabilize CausalContext/Graph and uncertain endpoint identity.
3. **#16, #19** close Phase 1 identification/refutation/inference scientific
   foundation based on the approved design.
4. **#18** adds distinct CATE/HTE estimands and optional EconML capabilities.
5. **#20** creates temporal graph/design semantics; **#21–#23** add quasi-
   experimental method families that may be parallel Work Packages only after
   approved shared contracts, not by assumption of independent Gate PASS.
6. **#24** is cross-cutting: input/file artifact contract must be agreed **before**
   method implementation, while final scientific acceptance is tested after each
   method and the program-level integration.

The dependency sequence is a proposal and does not substitute approved 06
`Depends on` or canonical 999 evidence. Do not mistake issue checkboxes for
runtime workflow cursor.

## 3. Issue content contract — matches Issue #11

Every Issue contains the following full sections, not only a short task title:

1. `# Problem` — current code baseline, historical scope and why gap matters.
2. `# Goal` — scientifically meaningful target outcomes.
3. `# Proposed Design` — design, assumptions, method parameters, artifacts,
   compatibility, negative results and local CLI ownership.
4. `# Acceptance Criteria` — evidence-based checklists, not only launch tests.
5. `# Related` — canonical requirements, 8/4 sources, parent and workflow docs.
6. `# Result` — initially unimplemented/planning; later real implementation
   evidence summary, **not** a substitute for 999 Gate Decision.
7. `# Memo` — explicit out-of-scope, risk and governance boundaries.

The narrower child Issues need not reproduce Issue #11's entire repository-wide
test migration inventory. Their depth is measured by coverage of method-specific
assumptions, invariants and objective scientific acceptance.

## 4. Issue / Requirement / Gate / verification governance

- **Issue:** operational tracking. Opening an Issue does not approve requirement
  changes or a backend dependency. Closing does not certify scientific validity.
- **03 Requirements Revision:** proposed FR/NFR/AR semantic delta and approval.
- **04 Design Revision:** ownership, adapter, CLI artifact, migration decisions.
- **05 Traceability:** provisional requirements→design→Gate→AC→Issue mapping.
- **Gate 06/07:** frozen coding and verification authority **only after review**.
- **20 / 30 / 999:** implementation evidence, independent tests and Gate decision.

## 5. Explicit exclusions and existing backlog interaction

- New Web UI, Web API, Worker and DB integration for Phase 1–3 **do not** belong
  to these E11 implementation Issues; future Enhancement Issue(s) may be opened
  once design integration is proposed. Do not open artificial future implementation
  tickets before that work is authorized.
- Policy Evaluation, monitoring, off-policy evaluation and automated decision
  workflow remain Phase 4/out of scope.
- [#11](https://github.com/kousuke-ota-datascience/causal-atelier/issues/11)
  repository-wide test architecture migration remains independent/nonblocking;
  E11 produces only tests needed for its own approved scientific acceptance.
