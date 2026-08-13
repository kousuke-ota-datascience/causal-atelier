# Contract Amendment Log — ENH-E6 append-only ledger

**Document class:** Planning / Evidence / Governance Artifact  
**Self-containment:** MUST for own responsibility.

## 1. Purpose

freeze/approval後のformal contract amendmentをappend-onlyで追跡する。Gate-local contract change decisionは09で承認し、affected primary contractsをexplicitly re-baselineする。本ledger自体はexecution authorityではない。

## 2. Invariants

- existing entryを削除/上書きしない。
- historical BLOCKED/FAIL/Test/Gate Decision evidenceを改変しない。
- failed implementationに合わせてACを緩めない。
- amendment identityを一意にする。
- application commit SHAを同じcommitへ自己参照で事前記載しない。
- Coding-agent information isolation/template compliance correctionとsemantic contract amendmentを区別する。

## 3. Canonical entry schema

Future amendmentはtemplate schemaのStatus/Trigger/Evidence/Gate/Trial/Type/09/Approval/Affected documents/Semantic impact/Downstream convergence/Evidence preservation/Git traceability/Notesを全て記載する。

### `<AMENDMENT_ID>` — `<TITLE>`

Future amendment entryは以下を全て埋める。

- Status: PROPOSED / APPROVED / REJECTED / APPLIED
- Trigger
- Trigger evidence
- Gate(s)
- Trial(s)
- Amendment type
- Gate-local 09 path
- Human / architecture owner approval

#### Affected normative documents

| Artifact | Before identity | Required action | After identity / path |
|---|---|---|---|
| `<path>` | `<sha/version>` | REBASELINE / REPLACE / NONE | `<path/sha>` |

#### Semantic impact

Before/AfterでGate semantic contract / AC / implementation semanticsへの影響を記載する。

#### Downstream convergence

- invalidated P00/Pxx/Rxx
- invalidated candidate(s)
- required new Trial
- required operator route
- Current State impact

#### Evidence preservation

- historical blocker/FAIL evidence preserved: YES/NO
- immutable evidence paths

#### Git traceability

- amendment authoring/approval commit
- re-baseline/application commit
- follow-up traceability commit if needed

#### Notes

N/Aなら`NONE`/`N/A`を明記する。

## Current ledger

### DOC-REBASELINE-001 — Template compliance and Coding-Agent information-isolation correction

- Status: `APPROVED / APPLICATION_COMMIT_PENDING`
- Trigger: Human owner instructed that all ENH-E6 artifacts must retain every applicable workflow-template field/section; Coding Agent must not read Gate 07 and must be entered only through the canonical Work Package operator prompt.
- Trigger evidence: ENH-E6 planning conversation / uploaded current workflow template audit bundle on 2026-08-13
- Gate(s): `G01`
- Trial(s): `N/A — before Trial01 Coding execution`
- Amendment type: `OTHER — DOCUMENTATION / GOVERNANCE REBASELINE, NON-SEMANTIC`
- Gate-local 09: `N/A` — Gate objective, required product behavior, presentation mappings, and AC-E6-G01-001..011 are not changed/relaxed.
- Human / architecture owner approval: Human owner explicit instruction to perform this template-compliance correction.

#### Affected normative documents

| Artifact | Before identity | Required action | After identity / path |
|---|---|---|---|
| Root / Current State / 00 planning artifacts | branch commit `42df32d...` state | COMPLETE TEMPLATE SCHEMA / AUDITABILITY | same canonical paths in this re-baseline |
| G01 Gate 06 | `42df32d...` frozen copy | NON-SEMANTIC DOCUMENTATION REBASELINE; retain implementation semantics | same path |
| G01 Gate 07 | `42df32d...` frozen copy | NON-SEMANTIC DOCUMENTATION REBASELINE; retain AC set and blocking journeys | same path |
| G01 P00 | `42df32d...` abbreviated copy | COMPLETE HUMAN ORCHESTRATION FIELDS | same path |
| G01 P01-P03 | `42df32d...` abbreviated/insufficiently isolated copies | MAKE EACH Pxx SELF-CONTAINED; REMOVE INSTRUCTION TO READ 07/PLANNING | same paths |
| 00/10/20/30/40 governance namespaces | incomplete/not instantiated | ADD APPLICABLE GUIDES/EVIDENCE NAMESPACES | new paths listed by compliance audit |

#### Semantic impact

`NONE` on product/Gate acceptance semantics. The correction makes already-approved ENH-E6 intent explicit in the template-required schema and fixes execution-context isolation. It does not loosen or redefine the Family/Stage routes, legacy targets, stage-aware presentation mapping, fail-closed behavior, or AC-E6-G01-001..011.

#### Downstream convergence

- Invalidated P00 / Pxx / Rxx: prior abbreviated P00/P01-P03 should no longer be used after this re-baseline; same canonical paths are replaced by template-compliant effective versions.
- Invalidated candidate(s): `NONE` — Coding execution has not started and no Fixed Trial Candidate exists.
- Required new Trial: `NO`.
- Required operator route: start Trial01 P01 only after Human commits/applies the re-baseline; use canonical Work Package Coding Agent prompt with `GATE_ID=G01`, `PACKAGE_ID=P01`, `TRIAL_NO=01`.
- Current State Control Sheet impact: record governance re-baseline as non-product/non-PASS update; actual P01 START_SHA is runtime-derived after application commit.

#### Evidence preservation

- Historical blocker / FAIL evidence preserved: `YES`.
- Immutable evidence paths: all ENH-E5 frozen contracts/reports/test decisions; pre-fix runtime negative-control facts remain unchanged.

#### Git traceability

- Amendment authoring / approval evidence commit: `PENDING — Human will commit local artifact bundle`.
- Re-baseline / application commit: `PENDING`.
- Traceability follow-up commit: `N/A unless Human records application SHA later`.

#### Notes

This entry prevents the post-freeze documentation rewrite from becoming a silent rewrite. Because semantic Gate/AC behavior is unchanged, no G01 09 semantic amendment is created.

No Human-approved **semantic** Gate Contract Amendment exists as of this re-baseline.
