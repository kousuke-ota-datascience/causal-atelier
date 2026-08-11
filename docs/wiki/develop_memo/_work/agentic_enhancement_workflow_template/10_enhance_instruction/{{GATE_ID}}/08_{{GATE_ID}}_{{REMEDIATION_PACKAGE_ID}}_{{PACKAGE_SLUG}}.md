# {{ENHANCE_ID}} {{GATE_ID}} {{REMEDIATION_PACKAGE_ID}} — {{PACKAGE_TITLE}}

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでremediation packageのnormative responsibilityを理解できること。

- Gate: {{GATE_ID}}
- Trial: {{TRIAL_NO}}
- Remediation Package: {{REMEDIATION_PACKAGE_ID}}
- Parent 08 (traceability): {{PATH_08}}
- Failed evidence (fact source): {{FAILED_EVIDENCE}}
- Depends on: {{DEPENDENCIES_OR_NONE}}

## 1. Verified failure context relevant to this package
{{FAILURE_CONTEXT}}

## 2. Correction objective
{{OBJECTIVE}}

## 3. Effective Gate / remediation constraints

Parent 08のmodeにかかわらず、このRxxを実行するために必要なconstraintを本文内に記載する。

{{EFFECTIVE_REMEDIATION_CONSTRAINTS}}

## 4. In scope
{{IN_SCOPE}}

## 5. Explicitly out of scope / forbidden workaround
{{FORBIDDEN}}

## 6. Entry criteria
{{ENTRY_CRITERIA}}

## 7. Required implementation
{{IMPLEMENTATION}}

## 8. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| {{CHECK}} | `{{COMMAND}}` | {{RESULT}} |

## 9. Protected contract / Transition Debt constraints
{{PROTECTED_AND_TD}}

## 10. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. implementation checkpoint reportを作成する。
4. execution status reportを作成・更新する。
5. report-only commitが別ならcheckpoint SHAと区別する。

Package completionはGate PASSではない。

## 11. Completion criteria
{{EXIT_CRITERIA}}

## 12. Stop rule

- scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next remediation packageへ勝手に進まない。
