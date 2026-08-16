# ENH-E7 Enhance Instruction

Execution Mode: G01 / G02 / G03 / G04 ともに `WORK_PACKAGE`。

## Gate / Work Package / Trial

- Gate: semantic acceptance / formal quality boundary。
- Work Package: bounded Coding Agent implementation unit。
- Trial: 1つのGate-level Fixed Trial CandidateをIndependent Verificationへ渡すcandidate transaction。
- `PACKAGE_COMPLETE` はGate PASSではない。

## Gate順序

```text
G01 final PASS
    ↓
G02 final PASS
    ↓
Post-Gate UI inspection:
presentation architecture acceptance escape detected
    ↓
G03 — UI Surface Architecture Correction
    ↓
G04 — Navigation / State Reintegration & Full Regression
    ↓
ENH-E7 corrected Product completion
```

G01/G02のPASS evidenceは履歴として保持する。G03/G04はG01/G02を「なかったこと」にする再実行ではなく、
G01/G02のnormative requirementsに適合していなかったpresentation implementationを是正する追加Gateである。

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

## Work Package completion

Work PackageはGate級quality boundaryではない。

Package completionに必要なのは、

- assigned scope実装
- focused verification PASS
- required invariantのdirect verification
- unresolved blockerなし
- package execution status report

である。

package単位のFixed Candidate SHA / checkpoint reportは必須にしない。
Gate-level Fixed Trial CandidateはCandidate Assemblyで固定する。

## Information isolation

Coding Agentはassigned Pxxをnormative implementation contractとする。
P00 / Gate 06 / Gate 07 / other Pxxを仕様補完目的で読まない。

そのためG03/G04では、担当Pxxに必要なpositive invariant / negative invariant / verification predicateを
self-containedに転写する。Gate→Pxxの意味損失をCoding Agent側の探索で補完させない。

## G03 correction rule

G03はcurrent E7 presentation architectureへの追加patchではない。

- reuse: routing / domain state / resource ownership / analysis operation semantics
- replace: top-level presentation shell / navigation ownership / DOM containment / layout topology
- remove: obsolete global sidebar / duplicate navigation / global common-context placement / dead presentation selectors
- prohibit: obsolete architectureをDOMに残したままCSSだけで隠す恒久対応

## G04 reintegration rule

G04はG03で成立したsurface architectureへ既存route/state/history/operation semanticsを再結合する。
G04でpresentation architectureを旧global shellへ戻してはならない。

## Verification discipline for UI architecture

UI architecture ACは以下のevidenceを必要とする。

- DOM containment / runtime visibility
- computed layoutまたはbounding-box relationship
- route/state behavior
- negative invariant（存在してはいけないnavigation / shellのabsence）
- Browser E2Eでのsuccess evidence

element ID / label文字列がsourceに存在するだけでは、surface separation / orientation / ownershipをPASSとしない。

## Remediation

各Gateの08 / 09は`TEMPLATE_ONLY`。

- 08: formal FAIL後のfailure-specific remediation
- 09: semantic Gate contract自体を変更する場合だけ使用
