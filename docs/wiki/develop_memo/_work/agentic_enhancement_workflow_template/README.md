# AI Agent分業型エンハンス開発テンプレート v3

## 0. Purpose

本テンプレートは、AI Agentを用いたエンハンス開発について、Repository上の文書だけから、**contract / execution / verification / verified state** を分離して追跡・再構成・監査できる状態を作るための標準構成である。

最低限、後から以下へ回答できなければならない。

1. なぜエンハンスを行うのか。
2. どの要件・設計を改定したのか。
3. 各Gateが「何が成立した」と主張する契約単位なのか。
4. そのGateの成果は、どの条件を満たしたとき後続工程が依存可能になるのか。
5. 各Trialで、どのFixed Trial Candidateを独立検証へ提出したのか。
6. Work Packageを使った場合、どのexecution unitへ分解し、各packageが何を実行したのか。
7. Package Checkpoint、Fixed Trial Candidate、Gate PASSを混同していないか。
8. Test / Audit Agentが何を観測し、なぜPASS / FAIL / BLOCKEDとしたのか。
9. 現在、何がverified current stateとして確立しているのか。
10. どのpassed-Gate contractが保護対象なのか。
11. どのTransition DebtがOPENで、どのGateで解消される予定なのか。
12. prerequisite / preflightが満たされているか。
13. 人間または別Agentが同じ根拠を再監査・追試できるか。

v3の中心原則は次の8つである。

1. **Gate-local semantic contract**
2. **Gate scope != Agent execution scope**
3. **Trial = candidate-to-independent-verification transaction**
4. **Work Package = bounded Coding Agent execution unit**
5. **Package checkpoint != Fixed Trial Candidate != Gate PASS**
6. **PASS-only verified-state promotion**
7. **Passed-Gate immutability**
8. **Explicit authority / precedence / evidence identity**

v3はv2のverification architectureを維持し、その上へ**execution decomposition architecture**を追加する。

---

## 1. Information layers

```text
TEMPLATE_Current_State_Control_Sheet.md / generated Current State Control Sheet
  = Verified current state control plane
  = final PASS済みevidenceのみから構成する、現在の正へのindex

00_enhance_background
  = Why / design history
  = 背景、要件・設計改定、承認、時点snapshot

10_enhance_instruction
  = What must become true + how execution is bounded
  = Gate contract / Work Package plan / package instruction / remediation

20_implementation_reports
  = What was implemented
  = package checkpoint / Trial candidate assembly / Coding Agent evidence

30_test_report
  = What was independently verified
  = Test Item evidence / Gate Decision / regression evidence

40_operator_workflows
  = Human-controlled orchestration
  = parameterized Agent entry prompt / architecture review / preflight / controlled runbook
```

### 1.1. Authority separation

```text
Gate Coding Contract (06)
  = implementation semantic contract
  = what must become true / allowed implementation scope

Gate Verification Contract (07)
  = Acceptance Criteria authority

Work Package Plan / Package Instruction
  = execution decomposition authority
  = Gate contractを細分化して実行するためのHOW
  = Gate semantic contractを変更できない

Package Checkpoint Report
  = Coding Agentが1 execution unitで観測したimplementation evidence
  = Gate acceptance authorityを持たない

Implementation Completion Report
  = one Trial candidate transaction record
  = Fixed Trial Candidate identity authority
  = Coding Agent authority

Gate-local Implementation Report Detail
  = Active Gateのimplementation ledger
  = 未検証状態を含んでよい

Gate Decision
  = independent verification decision
  = Test / Audit Agent authority

Current State Control Sheet
  = verified state index
  = final PASS済みevidenceのみをpromotion
```

**Coding Agentが実装したこと**、**packageが完了したこと**、**candidateがtest可能になったこと**、**Gate contractが確立したこと**を同一視してはならない。

---

## 2. Requirement levels

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

## 3. Core Workflow Semantics

この節はv3の**normative definition**である。

### 3.1. Gate — Acceptance Contract

**Gateは作業量や実装難易度を表す単位ではない。**

Gateとは、次を判定する**契約上のacceptance boundary**である。

> そのGateが主張する機能・状態・architecture semanticsが成立し、Gate内の作業から生じた変化・成果物を、後続工程が契約上依存可能な状態になったか。

Gateの境界は、原則として次で決める。

- 何を成立したと主張するのか。
- その主張が独立したsemantic contractとして表現できるか。
- PASS後に後続Gate / subsystem / operatorがその成果へ依存できるか。
- PASS後にprotected contractとしてregression protectionできるか。

次はGate分割理由にならない。

- 実装が大変である。
- ファイル数が多い。
- Coding Agentが一度では処理しづらい。
- commit数が多い。
- 作業時間が長い。

それらは**Work Package分割の理由**にはなり得る。

#### Gate PASSの効果

Final PASSされたGateは、以下を成立させる。

```text
Gate Contract
  ↓ implementation candidate
  ↓ independent verification
Final PASS
  ↓
Gate Contract Established
  ↓
Downstream may rely on the established semantics
```

PASS後は、原則として次が起きる。

- Gateのsemantic contractがestablishedになる。
- Current State Control Sheetへverified stateをpromotionできる。
- downstream Gateが前提として依存できる。
- protected passed-Gate contractになる。
- 後続変更にはmandatory regression obligationが生じる。

### 3.2. Trial — Candidate Verification Attempt

Trialは**Coding Agentを何回起動したか**を数える単位ではない。

Trialとは、同一Gate contractに対して、あるimplementation candidateを生成し、Fixed Trial Candidateとして固定し、Independent Verificationへ提出して正式判定を受ける一連のtransactionである。

```text
Trial
  = Candidate Generation
  + Candidate Assembly
  + Independent Verification Attempt
```

原則としてTrial番号が増えるのは、Independent Verificationによる**formal FAIL**を受け、次candidateを作るときである。

次だけではTrial番号を増やさない。

- Coding Agent interruption
- package implementation failure
- focused self-check failure
- package restart
- same-package correction
- report correction
- package checkpointの作り直し

`BLOCKED`は`FAIL`と同一ではない。Trial identityを変更するかはblocker解消方針で明示する。

### 3.3. Work Package — Coding Execution Unit

Work Packageは、Gate Contractを成立させるための実装作業を、Coding Agentが安全かつ検証可能に実行できる境界へ分解した**operational / execution unit**である。

```text
Gate
  = WHAT must become true
  = semantic / contractual boundary

Work Package
  = HOW implementation work is safely executed
  = operational / execution boundary
```

Work Package completionは以下を意味しない。

- Gate contract established
- Gate PASS
- verified current state promotion
- downstream Gate unlock
- product / architecture acceptance

したがって、v3のMUST invariantは次である。

> **Work Package completion does not establish any product or architecture contract.**

### 3.4. Responsibility matrix

| 観点 | Gate | Trial | Work Package |
|---|---|---|---|
| 主目的 | 成果の成立を契約・判定する | 1 candidateを独立検証へ提出する | 実装作業を安全に実行する |
| 境界 | semantic claim / downstream dependency | candidate verification attempt | execution scope / dependency / failure localization |
| Authority | 06/07 + 999 Gate Decision | Fixed Trial Candidate + Test evidence | package instruction + Coding self-check |
| 完了の意味 | downstreamが依存可能 | PASS/FAIL/BLOCKED decisionが出た | 次のimplementation stepへ進める |
| verified state更新 | PASS時のみ可能 | 直接はしない | しない |
| downstream unlock | PASS時に可能 | 直接はしない | しない |
| protected contract化 | PASS時 | しない | しない |
| failure | formal Gate FAILになり得る | formal FAILで次Trialへ | package failure != Gate FAIL |
| restart | Gate contractは維持 | formal FAILまで同Trial | 同Trial内で可能 |

### 3.5. Gate vs Work Package decision rule

以下を満たす作業単位はGate候補である。

1. 独立したsemantic claimを持つ。
2. その単位だけPASSしたとき、後続が成果へ安全に依存できる。
3. protected contractとして保存する意味がある。

以下の場合はWork Package候補である。

1. 単独完了してもdownstream利用可能性を確立しない。
2. Gate Contract成立のための途中実装である。
3. 分割理由がexecution size / dependency / failure localization / Agent restart resilienceである。

**実装難易度だけを理由にGateを細分化してはならない。**

### 3.6. Anti-patterns

禁止例:

```text
「G06は大変だから G06-A / G06-B / G06-C に分ける」
```

それぞれが独立したacceptance contractを持たないなら、GateではなくWork Packageへ分解する。

```text
P03 COMPLETE → G06 partially PASS
```

この状態は存在しない。正しくは:

```text
P03 = PACKAGE_COMPLETE
G06 = IN_PROGRESS
```

---

## 4. Execution Modes

Gate Coding Contractは、Gate開始前にexecution modeを明示する。

```text
SINGLE_EXECUTION
WORK_PACKAGE
```

### 4.1. SINGLE_EXECUTION

小規模Gateでは従来どおり、1 Trial candidateを1つのbounded Coding executionで生成してよい。

### 4.2. WORK_PACKAGE — CONDITIONAL MUST

以下のいずれかに該当する場合、Work Package Modeを使用する。

- 一度のAgent executionにはscopeが大きすぎる。
- 意味的に独立した複数implementation boundaryがある。
- dependency DAG / execution orderがある。
- intermediate checkpointがないとfailure localizationが困難。
- 複数subsystem / authority boundaryを跨ぐ。
- packageごとのfocused verificationが必要。
- Agent interruption / restart resilienceが必要。

Work Package Modeでは、P00 Work Package Planを作成し、各package scope / dependency / entry / exit / checkpoint ruleを固定する。

---

## 5. Canonical identifiers and naming

project-wide invariantとして以下を使用する。

```text
Enhancement ID       : project-defined identifier (e.g. ENH-E4)
Enhancement Short ID : artifact naming用short form (e.g. E4)
Gate ID              : G + 2-digit zero-padded decimal (G00-G99)
Trial No             : 2-digit zero-padded decimal (01-99)
Package Plan ID      : P00 reserved
Planned Package ID   : P01-P99
Remediation Package  : R01-R99
Test Item ID         : 001-998
Test Item 000        : reserved / do not use
Gate Decision        : reserved Test Item ID 999
Amendment ID         : A + 2-digit zero-padded decimal (A01-A99)
Transition Debt ID   : <ENHANCE_ID>-TD-<3 digits>
```

`P00`はWork Package Plan / execution control用reserved IDであり、production implementation packageとして扱わない。

標準例:

```text
E4-G06_01_P03_implementation_checkpoint_report.md
E4-G06_01_P03_in_progress.md
ENH-E4_G06_01_implementation_completion_report.md
ENH-E4_G06_01_001_contract_verification.md
ENH-E4_G06_01_999_gate_decision.md
ENH-E4_G06_02_Remediation_Instruction.md
```

`G6`, `Gate6`, `trial1`, `P3`, `item01` 等の表記揺れは使用しない。

### 5.1. Human-supplied vs derived variables

Operator promptでは、Humanが**identity variables**を指定し、path / filenameはschemaから導出する。

Human-supplied例:

```text
ENHANCE_ID
ENHANCE_SHORT_ID
GATE_ID
TRIAL_NO
PACKAGE_ID        # Work Package Coding時のみ
WORK_DIR_NAME
PROJECT_NAME
BRANCH_NAME
REMOTE_NAME
```

Derived variables例:

```text
WORK_ROOT
IMPLEMENTATION_INSTRUCTION_ID
TEST_INSTRUCTION_ID
INSTRUCTION_DIR
IMPLEMENTATION_REPORT_DIR
TEST_REPORT_DIR
IN_PROGRESS_REPORT_FILE
```

未解決`{{...}}`をAgent executionへ持ち込んではならない。

---

## 6. Gate contract model

### 6.1. 06 = Gate Coding Contract

- Active Gateのimplementation semanticsを固定する。
- `WHAT must become true`を定義する。
- execution modeを固定する。
- Gate PASSまでは原則immutable。
- FAILになっても実装失敗を理由に06を書き換えない。
- Work Package Plan / package instructionより上位である。

### 6.2. P00 = Work Package Plan — conditional

- `HOW implementation is decomposed`を固定する。
- package DAG / sequence / entry / exit / checkpoint / candidate assemblyを定義する。
- Gate semantic contractを変更できない。
- P00自体はimplementation packageではない。

### 6.3. P01-P99 = Planned Work Package

- 1 bounded Coding Agent execution unit。
- focused implementation + focused verification + checkpoint reportを生成する。
- package completeはGate acceptanceではない。

### 6.4. 07 = Gate Verification Contract

- Acceptance CriteriaとIndependent Verification contractを固定する。
- Gate PASSまでは原則immutable。
- 07がAcceptance Criteria authorityである。
- Test targetは原則**Fixed Trial Candidate**である。

### 6.5. 08 = Trial Remediation Delta

- formal FAIL evidenceに対する次Trialの差分修正契約。
- 06/07を再定義しない。
- Acceptance Criteriaを緩和しない。
- Work Package Modeでは必要に応じR01-R99 remediation packageへ分解する。
- original Pxxを「再実行」した体裁にせず、FAIL起因修正をRxxで区別する。

### 6.6. 09 = Gate Contract Amendment

06/07自体が誤っていることが判明した場合、それはTrial remediationではない。Human / architecture ownerへ戻し、`A01...`のAmendment recordで再承認する。

AmendmentがP00 / package instructionをinvalidateする場合、それらもversioned re-baselineする。

「テストに落ちたためACを変更してPASS」する運用は禁止する。

---

## 7. Candidate Assembly and evidence identity

### 7.1. Candidate hierarchy

v3ではcommit / evidence identityを最低3階層に分ける。

```text
Package Checkpoint SHA
  = 1 Work Packageのimplementation checkpoint

Fixed Trial Candidate SHA
  = 全package統合後、Gate-wide self-verificationを終え
    Independent Testへ渡す唯一のcandidate

Tested Repository State
  = Test Agentが実際にcheckout / observeしたrepository state
```

Acceptance判定の主対象は**Fixed Trial Candidate**である。

### 7.2. Package checkpoint != Fixed Trial Candidate

package checkpointは途中evidenceであり、単独でGate test targetへ昇格しない。

### 7.3. Documentation-only post-candidate changes

Fixed Trial Candidate固定後にreport-only commit等が生じる場合、production / test / migration / dependency semanticsが変わっていないことを明示する。

Tested Repository StateがFixed Trial Candidate SHAと異なる場合、Test / Audit Agentは差分を監査し、candidate semanticsが不変であることをevidence化する。確認不能なら`BLOCKED`または`FAIL`とする。

### 7.4. Candidate Assembly

Work Package Modeでは、package完了後にCandidate Assemblyを行う。

最低限:

- package chain completeness audit
- unresolved package blocker確認
- integration / Gate-wide regression
- protected passed-Gate regressionのCoding-side self-check
- candidate-affecting uncommitted changeなし
- Fixed Trial Candidate SHA固定
- Implementation Completion Report作成

Candidate AssemblyはGate PASSではない。完了状態は`READY_FOR_TEST`である。

---

## 8. State transition invariants

標準state:

```text
Gate
  IN_PROGRESS

Trial Candidate Generation
  PACKAGE_IN_PROGRESS
  PACKAGE_BLOCKED
  PACKAGE_COMPLETE

Candidate Assembly
  CANDIDATE_ASSEMBLY_IN_PROGRESS
  READY_FOR_TEST

Independent Verification
  PASS
  FAIL
  BLOCKED
```

標準flow:

```text
Human / workflow owner
  ↓ freeze 06 + 07
  ↓ select execution mode

Trial 01 Candidate Generation
  ├─ SINGLE_EXECUTION
  │    └─ implementation
  └─ WORK_PACKAGE
       ├─ P01 ... checkpoint
       ├─ P02 ... checkpoint
       └─ PNN ... checkpoint

Candidate Assembly
  ↓ Fixed Trial Candidate SHA
  ↓ Implementation Completion Report
  ↓ READY_FOR_TEST

Test / Audit Agent
  ↓ Test Item Reports
  ↓ 999 Gate Decision

FAIL
  ↓ 08 Trial 02 Remediation Delta
  ↓ optional R01-RNN remediation packages
  ↓ same Gate / next Trial

BLOCKED
  ↓ prerequisite / environment / contract ambiguity等を解消
  ↓ Trial identityの扱いを明示

PASS
  ↓ Gate Contract established
  ↓ Current State Control Sheetへverified state promotion
  ↓ passed-Gate contract protected
  ↓ next Gate may proceed
```

**Package failureだけでTrialをFAIL扱いしてはならない。**

---

## 9. Passed-Gate immutability

Final PASSしたGateの以下はprotected contractとなる。

- 06 / 07 semantic contract
- PASSを成立させたproduction semantics
- acceptance evidence
- established authority / ownership / schema / API contract

後続Gateがprotected contractに影響する場合、後続06/07に必ず以下を記録する。

1. affected passed Gate
2. protected invariant
3. 変更が必要な理由
4. preserved semantic / explicit amendment
5. mandatory regression test

Work Packageの都合でprevious Gate semantic contractを暗黙に変更してはならない。

---

## 10. Transition Debt

Transition Debtは単なるTODOではなく、期限付きarchitectural / operational exceptionとして管理する。

最低限:

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

06 / 07 / Work Package Plan / relevant package report / Implementation Completion Report / Test Item / Gate Decision / Current State Control Sheetからtraceableであること。

---

## 11. Document authority and precedence

標準precedence:

```text
1. Explicit Human-approved Gate Contract Amendment
2. 07 Gate Verification Contract
     -> Acceptance Criteria authority
3. 06 Gate Coding Contract
     -> Gate implementation semantics / allowed scope
4. Applicable 08 Remediation Delta
     -> current Trial correction delta only
5. P00 Work Package Plan / package instruction
     -> execution decomposition only; 06/07をoverrideしない
6. Final PASS previous Gate Decision
     -> established previous contract evidence
7. Current State Control Sheet
     -> verified-state index; upper contractをoverrideしない
8. Implementation Completion Report
     -> Fixed Trial Candidate identity / implementation facts
9. Package Checkpoint Report
     -> package-local implementation facts
10. Current source/test/migration
     -> observable implementation facts
```

矛盾を検出したAgentは勝手に統合解釈せず、`BLOCKED`またはhuman escalationとする。

---

## 12. Agent boundaries

### 12.1. Coding Agent

MUST:

- Active Gate / assigned Work Package scopeのみ実装する。
- package instructionがある場合、そのscopeを越えない。
- focused verificationを実行する。
- package checkpointまたはsingle-execution candidate checkpointを固定する。
- execution completion / interruption時にstatus reportを記録する。
- Work Package Modeではpackage checkpoint reportを作成する。
- Candidate Assembly担当時のみFixed Trial Candidateを固定する。
- `READY_FOR_TEST`または明示的な`BLOCKED_*`で停止する。

MUST NOT:

- Gate判定する。
- Work Package completionをGate PASSと表現する。
- Acceptance Criteriaを変更する。
- PASS済みGateを無断再設計する。
- next Gateへ先行着手する。
- assertion緩和 / test削除 / skip/xfail追加だけでFAILを回避する。

### 12.2. Test / Audit Agent

MUST:

- 07をAcceptance Criteria authorityとして使用する。
- Fixed Trial Candidate identityを最初に確認する。
- package checkpointではなくFixed Trial CandidateをGate acceptance対象とする。
- test itemごとのraw evidenceを保存する。
- candidate identity / repository state差分を監査する。
- 999 Gate Decisionを出す。

MUST NOT:

- production codeを変更する。
- automated test codeを変更する。
- migration / dependencyを変更する。
- package implementationを修正する。
- Work Package completionをPASS evidenceへ読み替える。

---

## 13. Parameterized operator prompt rules

Agent起動promptは、Humanが少数のidentity variablesを宣言し、derived variableを展開してpath / filenameを決定する形式を標準とする。

MUST:

- UPPER_SNAKE_CASE variableを使用する。
- Human-supplied / Derivedを分離する。
- `{{VARIABLE}}`を再帰展開する。
- execution開始前に未解決placeholderがないことを確認する。
- globが複数instructionに一致する場合、任意選択せず停止する。

Work Package Coding AgentおよびTest / Audit Agentの標準promptは`40_operator_workflows/agent_entry_prompts/`を参照する。

---

## 14. Preflight / prerequisite

product Gate判定とexecution prerequisiteを混同しない。

環境、DB、migration baseline、外部service、credential、test fixture等がGate execution前提の場合、`40_operator_workflows/preflight/`で独立確認する。

- Preflight failure = product acceptance FAILではない。
- prerequisite未成立時はGateを`BLOCKED`扱いにできる。
- destructive reset等はcontrolled runbookを使用する。

---

## 15. Architecture discovery conditional workflow

以下ではimplementation Gate開始前のarchitecture reviewを`CONDITIONAL MUST`とする。

- runtime entrypoint / execution lifecycle変更
- authority / ownership変更
- persistence / schema / lineage変更
- legacy path除去・統合
- migration strategy変更
- canonical source-of-truth変更

推奨順序:

```text
Current architecture inventory
  ↓
Target architecture / ADR / invariant set
  ↓
Gate decomposition
  ↓
Gate-local 06 / 07
  ↓
Execution Mode selection
  ↓
(optional) Work Package decomposition
```

Gate decompositionとWork Package decompositionを混同してはならない。

---

## 16. Human auditability

Repository上の文書だけから最低限以下に回答できること。

1. なぜこのenhancementを行ったか。
2. 現在のverified stateは何か。
3. Active Gateは何か。
4. Gateが成立を主張するsemantic contractは何か。
5. Gate PASSによって何がdownstream利用可能になるか。
6. Execution Modeは何か。
7. Work Package Modeなら、なぜ分割が必要だったか。
8. package dependency / execution orderは何か。
9. 各packageはどのcheckpoint SHAを生成したか。
10. package interruption / restartは発生したか。
11. Fixed Trial Candidate SHAは何か。
12. Test Agentはどのcandidateを検証したか。
13. Tested Repository Stateとの差分はあるか。
14. 各Acceptance Criterionのevidenceは何か。
15. Gate判定の根拠は何か。
16. 今回のTrialに08 / Rxx remediationが適用されたか。
17. どのpassed-Gate contractがprotectedか。
18. どのregressionを確認したか。
19. OPEN Transition Debtは何か。
20. prerequisite / preflightは成立しているか。
21. 次に進んでよいGateは何か。
22. 人間が同じtestを再実行できるか。

---

## 17. Instantiation rule

このdirectoryはテンプレートである。実enhancementへコピー後:

1. `{{...}}`を具体値へ置換する。
2. 不要なconditional workflow skeletonを削除または`N/A`化する。
3. Gateごとに`{{GATE_ID}}` directoryを作成する。
4. Gate開始前に06/07をfreezeする。
5. Execution Modeを選択する。
6. Work Package ModeではP00を作成してからP01+ instructionを作る。
7. Trial開始時にTrial directoryを作る。
8. Current State Control Sheetの初期verified baselineを作る。
9. 未解決meta variableをAgentへ渡さない。
