# 10_enhance_instruction — Gate Execution Contract Specification v2

## 0. Purpose

`10_enhance_instruction/`は、Coding AgentおよびTest / Audit Agentが従う**Gate-local execution contract**を保存する。

```text
{{GATE_ID}}/
  06 = Coding Contract
  07 = Verification Contract
  08 = retry Trial remediation delta (conditional)
  09 = explicit Gate Contract Amendment record (exceptional)
```

## 1. Common rules

### 1.1. No unresolved meta variables — MUST
Agentへ渡す時点で`{{...}}`を残さない。

### 1.2. Gate localization — MUST
Active Gate以外の便乗実装を禁止する。

### 1.3. Immutable Gate contract — MUST
06/07はGate開始前にfreezeする。FAILを理由に意味論を変更しない。

### 1.4. Remediation delta — CONDITIONAL MUST
FAIL後の次Trialでは08を追加する。08は06/07をoverrideしない。

### 1.5. Passed-Gate protection — MUST when previous PASS exists
previous PASS Gateのprotected semanticsとmandatory regressionを明示する。

### 1.6. Transition Debt — CONDITIONAL MUST
temporary authority / exceptional behaviorが存在する場合、IDとexit criterionを明示する。

### 1.7. Explicit precedence — MUST when multiple documents are readable
各文書のauthority domainを明記する。

## 2. 06 Coding Contract

MUST include:

- Project / Enhancement / Branch / Baseline / Active Gate
- Source of Truth / precedence
- Current verified state reference
- Coding Agent role
- prohibited work
- protected passed-Gate contracts
- implementation scope and change boundary
- Gate-specific implementation contract
- Transition Debt rules
- required automated checks
- required outputs
- completion / stop condition

## 3. 07 Verification Contract

MUST include:

- exact implementation commit selection rule
- Acceptance Criteria
- test item plan
- authority / precedence
- mutation prohibition
- protected passed-Gate regression requirements
- Transition Debt scope / exit audit where applicable
- PASS / FAIL / BLOCKED semantics
- required evidence format

07 is the Acceptance Criteria authority.
06 may be read as implementation/scope context but may not relax or override 07.

## 4. 08 Remediation Contract

08 is created for a retry Trial after FAIL.

MUST include:

- failed Trial / Gate Decision path
- observed failure facts
- required correction delta
- files / areas allowed to change
- explicit non-solutions
- unchanged 06/07 statement
- regression / retest obligations
- stop condition

MUST NOT:

- weaken Acceptance Criteria
- redefine target architecture without explicit amendment
- silently broaden Gate scope
- convert environment/preflight problems into product-code changes

## 5. Contract amendment

06/07 itself is wrong -> Human-approved Gate Contract Amendment (`09_*_Gate_Contract_Amendment.md`).
Retry implementation is wrong -> 08 Remediation Delta.
These paths must not be conflated.
