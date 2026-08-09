# {{ENHANCE_ID}} Current State Control Sheet

- Project: {{PROJECT_NAME}}
- Enhancement: {{ENHANCE_ID}}
- Branch: {{BRANCH}}
- Verified through Gate: {{VERIFIED_THROUGH_GATE}}
- Current Active Gate: {{ACTIVE_GATE}}
- Last updated: {{TIMESTAMP_ISO8601_TZ}}
- Update authority: {{UPDATE_AUTHORITY}}

## 1. Purpose and authority

この文書は、enhancementの**verified current state**を人間とAgentが誤認しないためのcontrol plane / indexである。

MUST:

- final PASS済みGate evidenceだけをverified stateへ反映する。
- FAIL / BLOCKED中の未検証implementationをcurrent truthとして昇格しない。
- 06 / 07 / Gate Decision / approved designをoverrideしない。
- source-of-truth文書へのpath / IDを示す。

## 2. Verified baseline

- Baseline commit: {{BASELINE_COMMIT}}
- Verified implementation commit: {{VERIFIED_IMPLEMENTATION_COMMIT}}
- Migration / schema head: {{VERIFIED_MIGRATION_HEAD_OR_NA}}
- Runtime / deployment baseline: {{VERIFIED_RUNTIME_BASELINE_OR_NA}}

## 3. Verified current architecture / behavior

{{VERIFIED_CURRENT_ARCHITECTURE_OR_BEHAVIOR}}

記載対象例:

- canonical runtime entrypoint
- canonical write/read path
- ownership / authority
- persistence semantics
- API/UI behavior
- lineage semantics

非architecture enhancementでは、検証済みの主要product behaviorを記載してよい。

## 4. Authority map

| Concern | Canonical authority | Temporary authority | Evidence / Contract |
|---|---|---|---|
| {{CONCERN}} | {{CANONICAL_AUTHORITY}} | {{TEMPORARY_AUTHORITY_OR_NONE}} | {{PATH_OR_ID}} |

## 5. Passed-Gate protected contracts

| Gate | Final PASS Decision | Protected invariant / semantic | Mandatory regression trigger |
|---|---|---|---|
| {{GATE_ID}} | {{DECISION_PATH}} | {{PROTECTED_SEMANTIC}} | {{TRIGGER}} |

## 6. OPEN Transition Debt register

| ID | Description | Temporary authority / exception | Introduced | Exit Gate | Exit Criterion | Scope Guard | Owner |
|---|---|---|---|---|---|---|---|
| {{TD_ID}} | {{DESCRIPTION}} | {{TEMP_AUTHORITY}} | {{GATE_ID}} | {{EXIT_GATE}} | {{EXIT_CRITERION}} | {{SCOPE_GUARD}} | {{OWNER}} |

If none: `NONE`.

## 7. Closed Transition Debt

| ID | Closed Gate | Closure evidence | Result |
|---|---|---|---|
| {{TD_ID}} | {{GATE_ID}} | {{EVIDENCE_PATH}} | CLOSED |

If none: `NONE`.

## 8. Prerequisite / Preflight status

| Prerequisite | Status | Evidence | Validity / expiry |
|---|---|---|---|
| {{PREREQUISITE}} | PASS / FAIL / UNKNOWN / N/A | {{PATH}} | {{VALIDITY}} |

## 9. Active Gate control

- Active Gate: {{ACTIVE_GATE}}
- Gate contract 06: {{PATH_06}}
- Gate verification contract 07: {{PATH_07}}
- Current Trial: {{TRIAL_ID}}
- Applicable remediation 08: {{PATH_OR_NONE}}
- Allowed next action: {{ALLOWED_NEXT_ACTION}}
- Explicitly prohibited next action: {{PROHIBITED_NEXT_ACTION}}

## 10. Evidence index

| Evidence type | Path / ID | Authority meaning |
|---|---|---|
| Last PASS Gate Decision | {{PATH}} | verified promotion basis |
| Active implementation completion report | {{PATH_OR_NONE}} | unverified implementation transaction |
| Active Gate detail ledger | {{PATH_OR_NONE}} | Coding-observed implementation state |
| Preflight result | {{PATH_OR_NA}} | execution prerequisite evidence |

## 11. Update log

| Timestamp | Trigger | Changed sections | Evidence |
|---|---|---|---|
| {{TIMESTAMP}} | Initial baseline / Gate PASS / TD close / prerequisite refresh | {{SECTIONS}} | {{PATH}} |

### Update rule

- `Gate PASS`: update verified state, protected contracts, TD status, active Gate.
- `Gate FAIL`: do **not** promote failed implementation semantics.
- `Gate BLOCKED`: do **not** promote product semantics; prerequisite status may be updated.
- Contract amendment: record only after explicit human approval and link amendment evidence.
