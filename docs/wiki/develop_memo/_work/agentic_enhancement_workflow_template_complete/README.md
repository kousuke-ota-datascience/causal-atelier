# AI Agent分業型エンハンス開発テンプレート

## 0. Purpose

本テンプレートは、AI Agentを用いたエンハンス開発について、以下をRepository上の文書として追跡可能にするための標準構成である。

1. なぜエンハンスを行ったか
2. どの要件・設計を改定したか
3. Agentへ何を実装・検証するよう指示したか
4. Coding Agentが実際に何を変更したか
5. Test / Audit Agentが実際に何を検証したか
6. GateをなぜPASS / FAIL / BLOCKEDと判定したか
7. 人間が後から実装差分とテストを再監査・追試できるか

## 1. Information layers

```text
00_enhance_background
  = Why
  = 背景・課題意識・要件/設計改定・承認・時点snapshot

10_enhance_instruction
  = What / How
  = Coding Agent / Test Agentが従う実行契約

20_implementation_reports
  = What was implemented
  = Coding Agentが実際に行った変更の証跡

30_test_report
  = What was verified
  = Test / Audit Agentが実際に行った検証とGate判定の証跡

40_operator_prompts
  = Entry point
  = 作業指示者がAgent起動時に渡す最小プロンプト
```

## 2. Core design principle

各ディレクトリでは、以下を分離する。

```text
README.md
  = 文書スキーマ仕様書
  = 何を書くか / どう解釈するか / 必須性 / 整合条件

TEMPLATE_*.md または skeleton文書
  = 完成文書の構造
  = 固定見出し + 固定field + meta-syntax variable

実際の生成物
  = meta-syntax variableを具体値へ置換した文書
```

`TEMPLATE_*.md` には原則として作業instructionを書かない。

## 3. Requirement levels

各READMEでは以下を使用する。

- `MUST`: 常に必要
- `CONDITIONAL MUST`: 条件該当時に必要
- `SHOULD`: 再現性・監査性・保守性向上のため推奨

空欄は避け、必要に応じて以下を使用する。

```text
N/A
NONE
NOT_RUN
UNKNOWN
```

## 4. Identifier format

以下をproject-wide invariantとして使用する。

```text
Gate ID       : project-defined identifier (e.g. G1, G2, G3)
Trial ID      : 2-digit zero-padded decimal (01–99)
Test Item ID  : 3-digit zero-padded decimal (001–998)
Test Item 000 : reserved / do not use
Gate Decision : reserved Test Item ID 999
```

標準file naming:

```text
G3_01_implementation_completion_report.md
G3_01_001_schema_contract.md
G3_01_002_leakage_rejection.md
G3_01_999_gate_decision.md
```

Trial IDとTest Item IDは桁数そのものを構文上の識別にも使用する。

## 5. Agent boundary

### Coding Agent

- `10_enhance_instruction/06_..._実装指示書.md` のみを実装契約として使用する
- 実装、必要なautomated test code、必要なmigration、実装報告だけを行う
- Gate判定、本格的な独立テスト、上位設計の再探索を行わない

### Test / Audit Agent

- `10_enhance_instruction/07_..._テスト指示書.md`
- 作業指示者が明示指定したimplementation completion report

のみを検証入力として使用する。

Test Agentはproduction code、automated test code、migration、dependencyを変更しない。

## 6. Gate / Trial flow

```text
作業指示者
  ↓ 06
Coding Agent
  ↓ implementation commit
  ↓ implementation completion report
  ↓ READY_FOR_TEST
  STOP
  ↓
作業指示者
  ↓ 07 + specific implementation completion report
Test / Audit Agent
  ↓ test item reports
  ↓ gate decision report
  ↓ PASS / FAIL / BLOCKED
  STOP

FAIL
  ↓ same Gate next trial

PASS
  ↓ next Gate
```

## 7. Human auditability

最終的にRepository上の文書から、少なくとも以下へ回答できることを目標とする。

```text
Q1. なぜこのエンハンスを行ったか？
Q2. どの要件・設計を変更したか？
Q3. Coding Agentには何を実装するよう指示したか？
Q4. 実際にどのfileを変更したか？
Q5. どのimplementation commitをTest Agentへ渡したか？
Q6. Test Agentはどのcommitを検証したか？
Q7. 何のcommandを実行したか？
Q8. どのAcceptance Criterionに対する証拠か？
Q9. Gate判定の根拠は何か？
Q10. 人間が同じtestを再実行できるか？
```
