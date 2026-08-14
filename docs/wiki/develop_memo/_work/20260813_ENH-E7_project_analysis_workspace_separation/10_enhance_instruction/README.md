# ENH-E7 Enhance Instruction

**Execution Mode:** G01 / G02ともにWORK_PACKAGE。

## Gate / Work Package / Trial

- **Gate**: semantic acceptance / formal quality boundary。
- **Work Package**: bounded Coding Agent implementation unit。
- **Trial**: 1つのGate-level Fixed Trial CandidateをIndependent Verificationへ渡すcandidate transaction。
- `PACKAGE_COMPLETE` はGate PASSではない。

## Gate順序

```text
G01 final PASS
    ↓
G02 execution eligible
```

## Execution readiness discipline

Execution readinessはpackage status literalから決めない。

Human/operatorはGate-level Architecture / implementation / verification contractを確認し、
preflightは以下から実行可否を導出する。

1. execution targetが一意
2. runtime identityが有効
3. current branchが正しい
4. Architecture / Gate contractに明示的blocking stateがない
5. required dependency completion evidenceが揃っている

Pxxの `READY_TO_EXECUTE` / `DRAFT_NOT_FROZEN` 等のdeclared statusはworkflow cursorにしない。

G01はArchitecture Review承認済み、Gate 06/07確認済みのpre-P01 baselineである。
G02はGate contractに明示的draft stateが残るため、freeze前はpreflightでBLOCKする。

## Work Package completion

Work PackageはGate級quality boundaryではない。

Package completionに必要なのは、

- assigned scope実装
- focused verification PASS
- unresolved blockerなし
- package execution status report

である。

package単位のFixed Candidate SHA / checkpoint reportは必須にしない。
Gate-level Fixed Trial CandidateはCandidate Assemblyで固定する。

## Information isolation

Coding Agentはassigned Pxxをnormative implementation contractとする。
P00 / 06 / 07 / other Pxxを仕様補完目的で読まない。

## Remediation

各Gateの08 / 09は`TEMPLATE_ONLY`。
formal FAILまたは明示的contract amendment triggerまでactive contractではない。
