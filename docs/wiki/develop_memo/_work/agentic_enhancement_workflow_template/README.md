# AI Agent分業型エンハンス開発テンプレート v2

## 0. Purpose

本テンプレートは、AI Agentを用いたエンハンス開発について、Repository上の文書だけから以下を追跡・再構成・監査できる状態を作るための標準構成である。

1. なぜエンハンスを行うのか。
2. どの要件・設計を改定したのか。
3. 各Gateで何を実装・検証する契約だったのか。
4. 各Trialで実際に何を変更したのか。
5. Test / Audit Agentが何を観測し、なぜPASS / FAIL / BLOCKEDとしたのか。
6. 現在、何がverified current stateとして確立しているのか。
7. どのpassed-Gate contractが保護対象なのか。
8. どのTransition DebtがOPENで、どのGateで解消される予定なのか。
9. prerequisite / preflightが満たされているか。
10. 人間または別Agentが同じ根拠を再監査・追試できるか。

v2の中心原則は次の5つである。

- **Gate-local contract**
- **Trial-local remediation delta**
- **PASS-only verified-state promotion**
- **Passed-Gate immutability**
- **Explicit document authority / precedence**

---

## 1. Information layers

```text
TEMPLATE_Current_State_Control_Sheet.md / generated Current State Control Sheet
  = Verified current state control plane
  = PASS済みevidenceのみから構成する、現在の正へのindex

00_enhance_background
  = Why / design history
  = 背景、要件・設計改定、承認、時点snapshot

10_enhance_instruction
  = Gate contract
  = Coding Agent / Test Agentが従うGate-local実行契約

20_implementation_reports
  = What was implemented
  = Coding Agentが各Gate / Trialで実際に行った変更の証跡

30_test_report
  = What was verified
  = Test / Audit Agentの独立検証、Gate Decision、regression evidence

40_operator_workflows
  = Human-controlled orchestration
  = Agent起動prompt、architecture review、preflight、controlled runbook
```

### 1.1. Authority separation

```text
Implementation Completion Report
  = one Trial transaction record
  = Coding Agent authority

Gate-local Implementation Report Detail
  = Active Gateの実装ledger
  = Coding Agent authority
  = 未検証状態を含んでよい

Gate Decision
  = independent verification decision
  = Test / Audit Agent authority

Current State Control Sheet
  = verified state index
  = final PASS済みevidenceのみを昇格
  = FAIL / BLOCKED中の未検証実装をcurrent truthとして扱わない
```

**Coding Agentが実装したこと**と、**システムの現在の正として確立したこと**を同一視してはならない。

---

## 2. Requirement levels

各READMEでは以下を使用する。

- `MUST`: 常に必要。
- `CONDITIONAL MUST`: 条件該当時に必要。
- `SHOULD`: 再現性・監査性・保守性向上のため推奨。

空欄は避け、必要に応じて以下を使用する。

```text
N/A       : 概念上非該当
NONE      : 該当対象だが存在しない
NOT_RUN   : 実行予定だが未実行
UNKNOWN   : 取得を試みたが確定不能
```

---

## 3. Canonical identifiers

project-wide invariantとして以下を使用する。

```text
Enhancement ID : project-defined identifier (e.g. ENH-E4)
Gate ID        : G + 2-digit zero-padded decimal (G00-G99)
Trial ID       : 2-digit zero-padded decimal (01-99)
Test Item ID   : 3-digit zero-padded decimal (001-998)
Test Item 000  : reserved / do not use
Gate Decision  : reserved Test Item ID 999
Transition Debt ID : <ENHANCE_ID>-TD-<3 digits> (e.g. ENH-E4-TD-001)
```

標準例:

```text
ENH-E4_G03_01_implementation_completion_report.md
ENH-E4_G03_01_001_schema_contract.md
ENH-E4_G03_01_999_gate_decision.md
ENH-E4_G03_02_Remediation_Instruction.md
```

`G3`, `Gate3`, `trial1`, `item01` 等の表記揺れは使用しない。

---

## 4. Gate contract model

### 4.1. 06 = Gate Coding Contract

- Active Gateの実装意味論を固定する。
- Gate PASSまでは原則immutable。
- FAILになっても、実装失敗を理由として06を書き換えない。

### 4.2. 07 = Gate Verification Contract

- Acceptance Criteriaと独立検証契約を固定する。
- Gate PASSまでは原則immutable。
- 07がAcceptance Criteria authorityである。

### 4.3. 08 = Trial Remediation Delta

- FAIL evidenceに対する次Trialの差分修正契約。
- 06/07を再定義しない。
- Acceptance Criteriaを緩和しない。
- FAIL理由、required correction、禁止回避策、再検証対象を固定する。

### 4.4. Gate Contract Amendment

06/07自体が誤っていることが判明した場合、それはTrial remediationではない。
Human / architecture ownerへ戻し、契約改定理由・影響・再承認を明示したうえで06/07をversioned amendmentする。
「テストに落ちたためACを変更してPASS」する運用は禁止する。

---

## 5. Passed-Gate immutability

Final PASSしたGateの以下はprotected contractとなる。

- 06 / 07のsemantic contract
- PASSを成立させたproduction semantics
- acceptance evidence
- established authority / ownership / schema / API contract

後続Gateがprotected contractに影響する場合、後続06/07に必ず以下を記録する。

1. affected passed Gate
2. protected invariant
3. 変更が必要な理由
4. preserved semantic / explicit amendment
5. mandatory regression test

既存PASSを暗黙に破壊してはならない。

---

## 6. Transition Debt

Transition Debtは単なるTODOではなく、期限付きarchitectural / operational exceptionとして管理する。

各Transition Debtには最低限以下を持たせる。

- ID
- description
- temporary authority / exceptional behavior
- why temporary
- introduced Gate
- owner
- exit Gate
- exit criterion
- scope guard
- status: `OPEN / CLOSED / CANCELLED`

06 / 07 / implementation report / test item / Gate Decision / Current State Control Sheetからtraceableであること。

---

## 7. Document authority and precedence

Test Agentの独立性は「読める文書を極端に減らす」ことではなく、各文書のauthority domainを固定することで確保する。

標準precedence:

```text
1. Explicit Human-approved Gate Contract Amendment
2. 07 Gate Verification Contract      -> Acceptance Criteria authority
3. 06 Gate Coding Contract            -> implementation intent / allowed scope
4. Applicable 08 Remediation Delta    -> current Trial correction delta only
5. Final PASS previous Gate Decision  -> established previous contract evidence
6. Current State Control Sheet        -> verified-state index; upper contractをoverrideしない
7. Implementation Completion Report   -> tested implementation commit / implementation facts
8. Current source/test/migration      -> observable implementation facts
```

矛盾を検出したAgentは勝手に解釈統合せず、`BLOCKED`またはhuman escalationとする。

---

## 8. Agent boundaries

### 8.1. Coding Agent

MUST:

- Active Gateのみ実装する。
- 必要なproduction code / automated test / migrationを変更する。
- implementation commitを固定する。
- completion reportとGate-local detailを更新する。
- `READY_FOR_TEST`で停止する。

MUST NOT:

- Gate判定する。
- Acceptance Criteriaを変更する。
- PASS済みGateを無断再設計する。
- next Gateへ先行着手する。
- assertion緩和、test削除、skip/xfail追加だけでFAILを回避する。

### 8.2. Test / Audit Agent

MUST:

- 07をAcceptance Criteria authorityとして使用する。
- 指定implementation commitを検証する。
- test itemごとのraw evidenceを保存する。
- 最終Gate Decisionを出す。

MUST NOT:

- production codeを変更する。
- automated test codeを変更する。
- migration / dependencyを変更する。
- 実装を修正してからPASSにする。

---

## 9. Gate / Trial state transition

```text
Human / workflow owner
  ↓ Gate-local 06 + 07をfreeze
Coding Agent Trial 01
  ↓ implementation commit
  ↓ implementation completion report
  ↓ READY_FOR_TEST
Test / Audit Agent
  ↓ test item reports
  ↓ 999 Gate Decision

FAIL
  ↓ 08 Trial 02 Remediation Deltaを作成
  ↓ 06/07は原則immutable
  ↓ same Gate / next Trial

BLOCKED
  ↓ prerequisite / contract ambiguity / environment issueを解消
  ↓ same Gate / same or next Trial as explicitly decided

PASS
  ↓ Current State Control Sheetへverified stateをpromotion
  ↓ passed-Gate contractをprotected化
  ↓ next Gate
```

**FAIL中のimplementation stateをCurrent State Control Sheetへ昇格してはならない。**

---

## 10. Preflight / prerequisite

product Gate判定とexecution prerequisiteを混同しない。

環境、DB、migration baseline、外部service、credential、test fixture等がGate execution前提である場合、`40_operator_workflows/preflight/`で独立確認する。

- Preflight failure = product acceptance FAILではない。
- prerequisite未成立時はGateを`BLOCKED`扱いにできる。
- destructive reset等が必要な場合はcontrolled runbookを使用する。

---

## 11. Architecture discovery conditional workflow

以下に該当するenhancementでは、implementation Gate開始前にarchitecture reviewを`CONDITIONAL MUST`とする。

- runtime entrypoint / execution lifecycleを変更する
- authority / ownershipを変更する
- persistence / schema / lineageを変更する
- legacy path除去・統合を行う
- migration strategyを変更する
- 複数subsystemを跨ぐcanonical source-of-truth変更を行う

推奨順序:

```text
Current architecture inventory
  ↓
Target architecture / ADR / invariant set
  ↓
Gate decomposition
  ↓
Gate-local 06 / 07
```

---

## 12. Human auditability

Repository上の文書だけから最低限以下に回答できること。

1. なぜこのenhancementを行ったか。
2. どの要件・設計を変更したか。
3. 現在のverified stateは何か。
4. Active Gateは何か。
5. そのGateの06/07 contractは何か。
6. 今回のTrialに08 remediationが適用されたか。
7. Coding Agentはどのcommitを生成したか。
8. Test Agentはどのcommitを検証したか。
9. どのcommandを実行したか。
10. 各Acceptance Criterionのevidenceは何か。
11. Gate判定の根拠は何か。
12. どのpassed-Gate contractがprotectedか。
13. どのregressionを確認したか。
14. OPEN Transition Debtは何か。
15. prerequisite / preflightは成立しているか。
16. 次に進んでよいGateは何か。
17. 人間が同じtestを再実行できるか。

---

## 13. Instantiation rule

このdirectoryはテンプレートである。実enhancementへコピーした後、以下を行う。

1. `{{...}}` を具体値へ置換する。
2. 不要なconditional workflow skeletonを削除または`N/A`化する。
3. `{{GATE_ID}}` directoryを実Gateごとに作成する。
4. Gate開始前に06/07をfreezeする。
5. Current State Control Sheetの初期verified baselineを作る。
6. 未解決meta variableをAgentへ渡さない。
