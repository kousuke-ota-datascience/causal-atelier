# ENH-E11 — Causal Lifecycle CLI-first Expansion

**State:** PLANNING / architecture and full requirement approval pending (2026-10-24)

This is the ENH-E11 workflow instance. It follows
`../agentic_enhancement_workflow_template/README.md` and
`../agentic_enhancement_workflow_template/README_Appendix_HowToUse.md`. This
directory deliberately does **not** claim that
any Gate 06/07 is frozen, any coding has started, or any canonical 999 Gate Decision exists.

## Current decisions

- Deliver all mandatory causal method families in the historical 2026-08-04 Phase 1–3
  instructions, reusing capabilities that are already implemented.
- New functionality stops at Scientific Core, local CLI and durable local file artifacts.
  New Web UI, Web API, Worker and DB integration is deferred.
- Phase 4 Policy Evaluation, automated decision making, operations monitoring and drift
  remain excluded.
- [GitHub tracking Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)
  indexes the work; an Issue marked done is **not** a Gate PASS.

## Documents — 00 planning layer

| Artifact | State / responsibility |
|---|---|
| `00_enhance_background/README_00.md` | Planning layer index and authority |
| `00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md` | Draft concept, scope, risks, proposed Gates |
| `00_enhance_background/02_enhancement_concept_approval_record.md` | **PENDING** human approval record; retains chat scope decisions as provenance |
| `00_enhance_background/03_requirements_revision.md` | Draft semantic changes, no new FR/NFR/AR IDs assigned yet |
| `00_enhance_background/04_design_revision.md` | Draft architecture deltas, review decisions pending |
| `00_enhance_background/05_requirements_design_consistency_and_traceability_review.md` | Provisional requirement→Gate→AC coverage, not PASS |
| `00_enhance_background/06_three_source_reconciliation_matrix.md` | Aug 4 × Sep handoff × current code/requirement reconciliation |
| `00_enhance_background/07_github_issue_register.md` | Registered GitHub issues, coverage and execution boundaries |
| `00_enhance_background/80_contract_amendment_log.md` | Empty append-only ledger; no approved contract amended |
| `00_enhance_background/Revised_requirements_definition_documents/README_00_Revised_requirements_definition_documents.md` | Approved-snapshot gate; snapshot **not yet frozen** |

## Deferred workflow layers

1. Finish full Reconciliation Matrix and Architecture Discovery; independently verify
   current code, test and prior acceptance evidence at fixed SHA.
2. Record human concept approval and resolve architecture decisions.
3. Approve requirement changes and update canonical `docs/wiki/requirement_definition/`
   documents; create approved Revised Requirements snapshots and freeze a baseline SHA.
4. Finalize semantic Gate decomposition; only then instantiate and freeze Gate-local
   `10_enhance_instruction/<GATE>/06_*` and `07_*` and Work Package contracts.
5. During actual execution, create `20_implementation_reports/`, `30_test_report/`,
   and run operator procedures under `40_operator_workflows/`, preserving independent
   verification and canonical 999 decisions.

Do not invent approval/Gate PASS evidence or create unapproved 06/07 contracts solely
because the original template contains placeholders.
