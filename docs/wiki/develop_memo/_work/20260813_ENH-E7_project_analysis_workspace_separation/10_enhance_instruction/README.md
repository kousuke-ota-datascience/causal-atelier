# ENH-E7 Enhance Instruction

**Execution Mode:** G01 / G02ともにWORK_PACKAGE。

## Gate / Work Package / Trial

- **Gate**: semantic acceptance boundary。
- **Work Package**: bounded Coding Agent execution unit。
- **Trial**: 1つのFixed Trial CandidateをIndependent Verificationへ渡すcandidate transaction。
- `PACKAGE_COMPLETE` はGate PASSではない。

## Gate順序

```text
G01 final PASS
    ↓
G02 execution eligible
```

## Freeze discipline

生成時点の06 / 07 / P00 / Pxxは `DRAFT_NOT_FROZEN`。

Execution前にHuman/operatorが以下を行う。

1. Architecture Reviewをconfirmする。
2. local repository identityを解決する。
3. Gate 06 / 07をreviewしてFROZENにする。
4. Pxxがself-containedであることを確認する。
5. Agent Execution Readiness preflightをPASSさせる。

## Information isolation

Pxx内のP00 / parent 06/07 pathはHuman traceability用である。
Coding AgentはP00 / 06 / 07 / other Pxxを仕様補完目的で読まない。

## Remediation

各Gateの08 / 09は`TEMPLATE_ONLY`。
formal FAILまたは明示的contract amendment triggerまでactive contractではない。
