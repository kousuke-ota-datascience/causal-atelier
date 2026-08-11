# ENH-E5 Gate / Work Package Contracts

## Authority model

### SINGLE_EXECUTION Coding
対象Gateのfreeze済み06が唯一のnormative implementation contract。

### WORK_PACKAGE Coding
Gate-level semanticsは06で定義するが、実際のPackage Agentへはassigned Pxxだけを渡す。Pxxは必要なGate制約を自己完結的に保持する。

### Independent Verification
対象Gateのfreeze済み07が唯一のnormative verification contract。

## 禁止する運用

- Coding Agentへ06 + 07 + ADR + requirementsをまとめて渡す
- Package Agentへ06 + P00 + Pxxを渡して自分でeffective scopeを合成させる
- Test Agentへ06を読ませて期待挙動を逆算させる
- contract ambiguityを過去文書/issue/Web探索で補完させる

## Freeze quality gate

Execution Agentが単一contractだけで担当責務を一意に実行できない場合、そのcontractはfreezeしてはならない。
