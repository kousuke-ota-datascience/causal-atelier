# 10_enhance_instruction — Gate Execution Contract Specification v3

## 0. Purpose

`10_enhance_instruction/`は、Gateのsemantic contractと、それを実行するためのexecution decompositionを保存する。

```text
{{GATE_ID}}/
  06 = Gate Coding Contract
  P00 = Work Package Plan (conditional)
  06_Gxx_Pxx = planned Coding execution package (conditional)
  07 = Gate Verification Contract
  08 = retry Trial remediation delta
  08_Gxx_Rxx = remediation Coding execution package (conditional)
  09 = explicit Gate Contract Amendment record
```

## 1. Normative responsibility

### Gate

Gateはacceptance contractであり、**作業結果が後続工程から依存可能になったか**を判定する単位である。

### Work Package

Work PackageはGate Contractを成立させるためのbounded Coding execution unitである。package completionはproduct / architecture acceptanceを成立させない。

### Trial

TrialはFixed Trial CandidateをIndependent Verificationへ提出して正式判定を受けるattemptである。Agent起動回数ではない。

## 2. Common rules

### 2.1. No unresolved meta variables — MUST
Agentへ渡す時点で`{{...}}`を残さない。

### 2.2. Gate localization — MUST
Active Gate以外の便乗実装を禁止する。

### 2.3. Immutable Gate contract — MUST
06/07はGate開始前にfreezeする。FAILやpackage都合を理由に意味論を変更しない。

### 2.4. Execution Mode — MUST
06で`SINGLE_EXECUTION`または`WORK_PACKAGE`を固定する。

### 2.5. Work Package decomposition — CONDITIONAL MUST
Work Package ModeではP00を先に固定し、その後P01+ instructionを作成する。

### 2.6. Remediation delta — CONDITIONAL MUST
formal FAIL後の次Trialでは08を追加する。08は06/07をoverrideしない。

### 2.7. Passed-Gate protection — MUST when previous PASS exists
previous PASS Gateのprotected semanticsとmandatory regressionを明示する。

### 2.8. Transition Debt — CONDITIONAL MUST
temporary authority / exceptionが存在する場合、IDとexit criterionを明示する。

## 3. 06 Gate Coding Contract MUST include

- Project / Enhancement / Branch / Baseline / Active Gate
- Gate definition / objective
- **Gate acceptance claim: PASS後に何がdownstream利用可能になるか**
- Execution Mode
- allowed scope / prohibited scope
- protected passed-Gate contracts
- required implementation semantics
- schema / migration / API / runtime policy
- automated test obligations
- Transition Debt constraints
- candidate assembly requirement
- required reports / stop condition

06はpackage instructionより上位である。

## 4. P00 Work Package Plan — conditional

MUST include:

- why Work Package Mode is required
- package list
- package semantic scope
- dependency / execution DAG
- entry criteria
- exit criteria
- focused verification
- checkpoint rule
- restart / interruption rule
- package report path
- Candidate Assembly owner / package
- Fixed Trial Candidate fixation rule

P00自体をimplementation packageとして実行しない。

## 5. Package instruction P01-P99

MUST include:

- Gate / Trial / Package identity
- parent 06 / P00
- exact scope
- explicit out-of-scope
- dependencies
- required implementation
- focused verification
- checkpoint commit rule
- status report rule
- checkpoint report rule
- stop condition

Package AgentはGate-wide PASS/FAILを判定しない。

## 6. 07 Verification Contract

MUST include:

- Acceptance Criteria
- Fixed Trial Candidate identity rule
- Test Item plan
- candidate identity audit
- protected passed-Gate regression
- Transition Debt audit
- FAIL / BLOCKED distinction
- Gate Decision semantics

07がAcceptance Criteria authorityである。

## 7. 08 Remediation Delta

formal FAIL後にHuman / workflow ownerが作成する。

MUST include:

- failed Trial
- failed Gate Decision path
- immutable 06 / 07 references
- failure facts
- required correction
- forbidden workaround
- re-verification requirements
- next Trial identity
- Work Package Modeの場合のRxx decomposition方針

## 8. Remediation Package R01-R99

Rxxはformal FAILによって生じたcorrection execution unitである。
Original Pxxと区別し、FAIL前のplanned implementationとFAIL後のremediationをtraceableにする。

## 9. 09 Gate Contract Amendment

Contract defect時のみ使用する。Amendment IDは`A01-A99`。

- amendment reason
- affected 06 / 07
- affected P00 / package instructions
- protected passed-Gate impact
- re-approval
- re-baseline requirement
- Trial handling

## 10. Precedence

```text
Amendment > 07 > 06 > 08 > P00/package instruction > evidence/report
```

ただし08は06/07をoverrideせず、P00/package instructionはexecution HOWのみを支配する。
