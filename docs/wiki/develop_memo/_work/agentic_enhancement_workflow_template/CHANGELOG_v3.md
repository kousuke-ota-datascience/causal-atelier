# CHANGELOG v3

## Summary

v3はv2のGate-local verification architectureを維持し、ENH-E4 G06で実証された**execution decomposition architecture**を追加するbreaking schema updateである。

## Breaking semantic changes

1. `Gate scope != Agent execution scope`をnormative invariant化。
2. Gateを**acceptance contract / downstream依存可能性の判定単位**として明文化。
3. TrialをAgent runではなく**candidate-to-independent-verification transaction**として再定義。
4. Work Packageをbounded Coding Agent execution unitとしてfirst-class化。
5. `P00` Work Package Plan、`P01-P99` planned package、`R01-R99` remediation packageを導入。
6. `Package Checkpoint SHA -> Fixed Trial Candidate SHA -> Tested Repository State`のevidence identity hierarchyを導入。
7. Candidate Assemblyを明示的state / responsibilityとして導入。
8. `20 / 30`を`Gate -> Trial` directory hierarchyへ変更。
9. package execution status reportとimplementation checkpoint reportを追加。
10. Test / Audit Agentのacceptance targetをFixed Trial Candidateとして明文化。
11. Agent entry promptをparameterized operator prompt方式へ変更。
12. Human-supplied identity variablesとDerived filename/path variablesを分離。
13. Amendment ID `A01-A99`をcanonical identifierへ追加。

## Preserved v2 invariants

- Gate-local 06 / 07 contract
- Trial-local 08 remediation delta
- PASS-only verified-state promotion
- Passed-Gate immutability
- Explicit document authority / precedence
- Transition Debt traceability
- Independent Test / Audit authority

## Compatibility

`SINGLE_EXECUTION` modeを保持するため、小規模GateはWork Packageを作成せずv2相当の運用を継続できる。
Work Package artifactは条件付きである。
