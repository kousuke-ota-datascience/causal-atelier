# NFR-019 Documentation Self-Containment Re-Audit — Phase J

- **Audit baseline commit SHA:** `9008078d6d9e8d1f86e4ec2e77c8074c00cc4d28`
- **Audit date:** 2026-08-12 (Asia/Tokyo)
- **Normative input:** `10_requirements_definition.md`, `21_logical_data_design.md`, `22_product_basic_design.md`, `23_api_interface_design.md`, `30_detailed_design.md`
- **Reference planning evidence:** `remediation_decision_matrix.csv`, `d2_planning_decision_freeze.md`, `90_technical_debt_and_future_enhancements.md`
- **Normative status:** This document is non-normative audit evidence.

## 1. Overall verdict

**FAIL / REMEDIATION REQUIRED**

Phase I significantly improved self-containment and removed the former G00/G01/Architecture Review delegation blockers. However, `10_requirements_definition.md` still contains stale cross-cutting prose that contradicts its own Requirement table and the canonical `21/22/23/30` contract.

The blockers are localized and should be corrected before declaring NFR-019 PASS.

## 2. DOC-019 acceptance result

| ID | Result | Finding |
|---|---|---|
| DOC-019-01 | FAIL | The canonical set is broadly self-contained, but contradictory authorization, audit/retention, and StageExecution lifecycle statements prevent a single unambiguous contract from being derived. |
| DOC-019-02 | PASS | No normative statement was found that delegates required contract content only to ENH-E4/source/existing-contract references. Historical Change Log references do not act as normative delegation. |
| DOC-019-03 | PASS | No target design statement was found that requires ADR / 06 / Pxx / repository inspection to determine the design. |
| DOC-019-04 | PASS | No remaining Architecture Review / Human Review / Gate freeze / TBD decision was found in the canonical five-document set. |
| DOC-019-05 | FAIL | D1 StageExecution cancellation is reflected in 21/23/30 but omitted from `10 §8.4`, producing a stale current-contract statement. |
| DOC-019-06 | PASS | D2 target contracts are concretized, including typed filter validation, exploratory handoff, subgroup uncertainty, comparability, idempotency, authorization, lineage, reproducibility, deep navigation/accessibility, and navigation architecture. |
| DOC-019-07 | FAIL | `10 §9` and `10 §10` leak D3 system/operator authorization and general audit/retention contracts back into current normative prose; `10 §12` also requires verification evidence for all NFRs, including D3/FUTURE items. |
| DOC-019-08 | FAIL | `10` contradicts `21/22/23/30` on StageExecution `CANCELLED`, Project authorization terminology, and D3 audit/retention boundary. |

## 3. Blocking findings

### PJ-B01 — StageExecution lifecycle contradiction

`10 §8.4` currently defines:

```text
PENDING -> READY -> RUNNING -> SUCCEEDED
                       -> FAILED
PENDING / READY -> SKIPPED_DUE_TO_PREREQUISITE
```

but omits `CANCELLED`.

Canonical `21`, `23`, and `30` include `CANCELLED` in the StageExecution lifecycle/status contract.

Required remediation:

```text
PENDING -> READY -> RUNNING -> SUCCEEDED
                       -> FAILED
PENDING / READY -> SKIPPED_DUE_TO_PREREQUISITE
PENDING / READY / RUNNING -> CANCELLED
```

### PJ-B02 — Authorization terminology contradicts frozen role model

`10 §7.1` correctly freezes persisted Project roles to:

```text
OWNER
EDITOR
VIEWER
```

and explicitly prohibits an independent `EXECUTE` role.

However, `10 §9` still states:

- `execute権限` is required for Plan submit/cancel/retry.
- `Operator権限` is required for system configuration/retention/health detail.

This conflicts with the Phase G authorization contract:

- Execution mutation is authorized by `OWNER / EDITOR`.
- No independent `EXECUTE` role is introduced.
- system/operator-level authorization is D3/FUTURE.

Required remediation:

- Replace generic `execute権限` wording with the explicit `OWNER / EDITOR` rule.
- Remove current-E5 normative `Operator権限`.
- State that system/operator-level authorization is `DEFERRED / FUTURE`.

### PJ-B03 — D3 Audit / retention leaked into current normative prose

The Requirement table correctly marks:

- `FR-122` general operational audit trail = `DEFERRED / NOT_IMPLEMENTED / FUTURE`
- `FR-126` configurable retention/deletion policy = `DEFERRED / NOT_IMPLEMENTED / FUTURE`

However `10 §10` currently requires:

- physical Artifact deletion metadata/reason to be retained as audit records
- Audit fields `actor / action / resource / project / request id / timestamp / outcome`

These are effectively the deferred general Audit/retention contracts.

Required remediation:

Keep current/baseline data-lifecycle facts only, and explicitly separate:

```text
FR-122 general operational audit trail -> DEFERRED / FUTURE
FR-126 configurable retention/deletion policy -> DEFERRED / FUTURE
```

### PJ-B04 — Definition of Done mixes D3 NFRs into ENH-E5 acceptance

`10 §12` currently requires verification evidence for `NFR-001〜NFR-027`.

This range includes D3/FUTURE requirements such as:

- `NFR-004`
- `NFR-007`
- `NFR-008c`
- `NFR-009b`
- `NFR-010b`
- `NFR-011b`
- `NFR-017`
- `NFR-020b`

The detailed/basic design explicitly says D3 verification targets must not be mixed into ENH-E5 acceptance.

Required remediation:

Replace blanket NFR/AR ranges with lifecycle-aware acceptance wording, e.g.:

> `Requirement Status=ACTIVE` and `Delivery=BASELINE or ENH-E5` items shall have the verification evidence required by their Level/design verification contract. `DEFERRED / FUTURE` items are excluded from ENH-E5 mandatory acceptance.

## 4. Non-blocking terminology clarification

### PJ-N01 — `Operator` actor label

`10 §2 Actor` and `22 System Context` use `Operator` as an actor/persona. This can be retained only if it is explicitly distinguished from a persisted Project role or ENH-E5 authorization role.

Recommended wording:

> `Infrastructure Operator`: deployment/operations persona; not a persisted ProjectMembership role. Product-level system/operator authorization policy is DEFERRED/FUTURE.

This prevents confusion with the D3 system/operator authorization decision.

## 5. Verified convergence points

The following contracts were verified as mutually aligned across the canonical documents:

- Analysis Family values: `EXPLORATORY / CAUSAL / PREDICTIVE`
- canonical navigation endpoint: `GET /api/v1/navigation/analysis`
- navigation schema: `analysis-navigation/1`
- canonical route: `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`
- default stages: exploratory/profile, predictive/setup, causal/setup
- exact Family-local Navigation Stage catalogs
- Navigation Stage is not persisted to AnalysisSpecification / ExecutionPlan / Execution / StageExecution
- `FILTER_TYPE_MISMATCH`
- `EXPLORATORY_REUSE_SAME_DATA`
- idempotency scope `(project_id, command_scope, idempotency_key)`
- `IDEMPOTENCY_KEY_REQUIRED`
- HTTP 409 `IDEMPOTENCY_CONFLICT`
- persisted roles `OWNER / EDITOR / VIEWER`
- no independent persisted `EXECUTE` role
- canonical lineage chain
- `StageAttempt.effective_random_seed`
- async presentation states `IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`
- D3 exclusion in `22` and `30`

## 6. D1 / D2 / D3 trace check

Machine comparison of Requirement-type remediation rows against the `10` Requirement table:

- Requirement decision rows checked: **77**
- lifecycle/status mismatch: **0**, excluding the special documentation verification representation for `NFR-019`
- D3 Decision Items: **28**
- D3 items traceable in `90_technical_debt_and_future_enhancements.md`: **28 / 28**

The remaining failures are therefore not the main Requirement table classification itself; they are stale prose outside the table.

## 7. Required sequence

```text
Phase J initial re-audit = FAIL
        |
        v
Remediate 10 (and clarify 22 Operator persona if retained)
        |
        v
Re-run DOC-019-01..08
        |
        +-- all PASS -> update NFR-019 Implementation Status to IMPLEMENTED
        |             -> Phase J PASS / FROZEN
        |             -> proceed to Phase K 06/Pxx/07 convergence
        |
        +-- any FAIL -> remain in Phase J remediation loop
```

## 8. Current gate

**Phase K remains BLOCKED.**
