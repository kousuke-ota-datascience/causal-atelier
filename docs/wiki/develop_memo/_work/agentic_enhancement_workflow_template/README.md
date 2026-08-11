# AI Agent分業型エンハンス開発ワークフローテンプレート

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでworkflow全体の作成・運用原則を理解できること。


## 0. このテンプレートの目的

本テンプレートは、AI Agentを用いてエンハンス開発を計画・実装・独立検証するときに、**どの文書を、どの順序で、何を記載して作成すればよいか**を定義する標準テンプレートである。

実際のエンハンスでは、このdirectoryを作業directoryへコピーし、`{{...}}` placeholderを具体値へ置換して使用する。


### Canonical filename policy

Canonical filename / directory nameは、LLM・shell・Git・自動生成処理で安定して扱えることを優先し、次をMUSTとする。

- filename / directory nameは **ASCII charactersのみ**を使用する。
- semantic suffixは **technical English**を使用する。
- 日本語はcanonical filename / directory nameへ使用しない。
- 日本語はdocument title / body textへ使用してよい。
- `ENHANCE_ID` / `GATE_ID` / `TRIAL_NO` / `PACKAGE_ID`等のcanonical identifierは定義どおり保持する。
- Humanはidentityを指定し、derived filename / pathはschemaから生成する。

例:

```text
06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_implementation_instruction.md
07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction.md
```


## 0.1. Document design principles

本テンプレートの各文書は、**その文書が担う責務について、読者またはLLMが当該文書から直接理解・作成・実行・監査できること**を原則とする。

ただし、自己完結の対象は「すべての情報」ではない。文書内へ保持すべきものと、外部参照してよいものを区別する。

### Document classes

| Document class | 主な対象 | Self-containment rule |
|---|---|---|
| **Authoring Guide** | root / 各directory README、構造・命名ガイド | **MUST** — そのガイドだけで担当artifactの作り方が分かること |
| **Primary Execution Contract** | 06, 07, Pxx, Rxx | **MUST** — Agentが担当責務を実行するためのnormative semanticsを本文内に持つこと |
| **Derived Contract** | 08, 09 | **CONDITIONAL** — 派生理由を保持しつつ、用途に応じてdelta referenceまたはconsolidationを選ぶこと |
| **Planning / Evidence / State / Operator Artifact** | 00, 20, 30, Current State Control Sheet, 40のprompt/result等 | **MUST for own responsibility** — その文書の結論・判断・実行規則は本文内に持ち、fact/evidence/targetは外部参照可 |

### Local normative meaning

以下は原則として**現在の文書内へ記載する**。

- その文書の目的・責務
- 用語または状態の意味
- 必須条件・禁止事項
- 判断基準・completion condition
- authority / precedenceのうち、その文書を正しく使うために必要なもの
- Agentへ直接与えるinstructionの場合、そのAgentが守るべきeffective contract

### Evidence / fact by reference

以下は複製せず外部参照してよい。

- source code / migration / schema / runtime object
- commit SHA / diff / command output
- previous Gate Decision / Test Item evidence
- requirement / designのprovenance
- observation target / execution target
- historical rationale

**外部artifactを参照して事実を取得すること**と、**外部workflow文書を読まなければ現在文書の規則が分からないこと**を混同しない。

### Remediation exception

`08 Trial Remediation Contract`は、original 06 / 07をimmutableに保持するためにformal FAIL後に作成する派生contractである。この存在意義から、次の2 modeを許容する。

- `DELTA` — 06 / 07のstill-valid contractを参照し、remediation固有の変更だけを記載する。
- `CONSOLIDATED` — next Trialに必要なeffective implementation / verification contractを08内へ統合する。

modeはFAIL evidence確定後、**next TrialのLLMへ与えるeffective contextが必要十分・明確・最小になる方**を選ぶ。

Gate semantic claimまたはAcceptance Criteria自体が誤っていた場合は08で再定義せず、09 Gate Contract Amendmentを使用する。


本テンプレートを使用して作成された文書だけから、後から最低限以下を再構成・監査できる状態を作ることを目的とする。

1. なぜエンハンスを行うのか。
2. どの要件・設計を改定したのか。
3. 各Gateは何を成立させる契約なのか。
4. Gate PASSにより、どの成果を後続工程が利用可能になるのか。
5. Gateを成立させるために、どの実装作業を行ったのか。
6. Work Packageを使用した場合、どのexecution unitへ分解したのか。
7. どのimplementation candidateをIndependent Verificationへ提出したのか。
8. Test / Audit Agentは何を観測し、なぜPASS / FAIL / BLOCKEDと判定したのか。
9. 現在、何がverified current stateとして確立しているのか。
10. どのpassed-Gate contractが保護対象なのか。
11. OPENなTransition Debtと、その解消条件は何か。
12. prerequisite / preflightが成立しているか。
13. 人間または別Agentが同じ根拠を再監査・追試できるか。

---

## 1. 最初に理解すべきworkflow semantics

このテンプレートでは、**契約単位・検証単位・実行単位を分離する**。

### 1.1. Gate — Acceptance Contract

Gateは作業量や実装難易度を表す単位ではない。

Gateとは、次を判定する**契約上のacceptance boundary**である。

> そのGateが主張する機能・状態・architecture semanticsが成立し、Gate内の作業から生じた変化・成果物を、後続工程が契約上依存可能な状態になったか。

Gateの境界は原則として次で決める。

- 何を成立したと主張するのか。
- その主張が独立したsemantic contractとして表現できるか。
- PASS後に後続Gate / subsystem / operatorがその成果へ依存できるか。
- PASS後にprotected contractとしてregression protectionする意味があるか。

次はGate分割理由にならない。

- 実装が大変である。
- ファイル数が多い。
- Coding Agentが一度では処理しづらい。
- commit数が多い。
- 作業時間が長い。

これらはWork Package分割の理由にはなり得る。

### 1.2. Trial — Candidate Verification Attempt

TrialはCoding Agentを何回起動したかを数える単位ではない。

Trialとは、同一Gate contractに対してimplementation candidateを生成し、Fixed Trial Candidateとして固定し、Independent Verificationへ提出して正式判定を受ける一連のtransactionである。

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

`BLOCKED`は`FAIL`と同一ではない。

### 1.3. Work Package — Coding Execution Unit

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

### 1.4. Responsibility matrix

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

### 1.5. Workflow invariants

すべてのエンハンス文書は、以下の不変条件を満たすように作成する。

1. **Gate-local semantic contract** — Gateごとに06/07でsemantic contractを固定する。
2. **Gate scope != Agent execution scope** — Gate境界をAgent実行量で決めない。
3. **Trial = candidate-to-independent-verification transaction** — TrialはAgent起動回数ではない。
4. **Work Package = bounded Coding Agent execution unit** — Work Packageはexecution boundaryである。
5. **Package checkpoint != Fixed Trial Candidate != Gate PASS** — 各evidence identityを分離する。
6. **PASS-only verified-state promotion** — verified stateはfinal PASS時だけ昇格させる。
7. **Passed-Gate immutability** — PASS済みcontractは後続作業から保護する。
8. **Explicit authority / precedence / evidence identity** — 文書authorityとevidence identityを明示する。

---

## 2. 作成するdocument layers

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

### 2.1. Document authority

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

## 3. エンハンス文書を作成する順序

### Step 1 — Background / requirements / designを作成する

`00_enhance_background/`を使用する。

最低限、以下を明らかにする。

- enhancement objective
- current problem / motivation
- affected requirements
- affected architecture / design
- constraints / invariants
- approval record
- traceability

architecture / ownership / persistence等を変更する場合は、必要に応じて`40_operator_workflows/architecture_review/`を先に実行する。

### Step 2 — Gate decompositionを決める

各Gateについて次を一文で書けることを確認する。

> このGateがPASSすると、何が成立し、後続工程は何へ依存できるようになるか。

分割理由が単に実装量である場合はGateを増やさず、Work Packageを使用する。

### Step 3 — Current State Control Sheetを初期化する

`TEMPLATE_Current_State_Control_Sheet.md`をコピーし、開始時点で既にverifiedな状態だけを記載する。

未検証の実装予定やpackage進捗をverified current stateへ書かない。

### Step 4 — Gateごとの06 / 07を作成してfreezeする

`10_enhance_instruction/{{GATE_ID}}/`へ以下を作成する。

- `06_*` — Gate Coding Contract
- `07_*` — Gate Verification Contract

06には「何を実装上成立させるか」、07には「何を満たせばGate PASSか」を記載する。

Gate実行開始後に、implementation都合やtest failureを理由として06/07の意味論を書き換えない。

### Step 5 — Execution Modeを選択する

06で以下のいずれかを指定する。

```text
SINGLE_EXECUTION
WORK_PACKAGE
```

`WORK_PACKAGE`を使用する条件の目安:

- 一度のAgent executionにはscopeが大きすぎる。
- 複数のimplementation boundaryがある。
- dependency DAG / execution orderがある。
- intermediate checkpointがないとfailure localizationが困難。
- 複数subsystem / authority boundaryを跨ぐ。
- packageごとのfocused verificationが必要。
- Agent interruption / restart resilienceが必要。

### Step 6 — Work Packageを使う場合はP00 / Pxxを作成する

`WORK_PACKAGE` modeでは以下を作る。

- `P00` — Work Package Plan / execution control
- `P01-P99` — planned implementation package

P00にはpackage list、dependency、entry / exit criteria、focused verification、checkpoint rule、Candidate Assembly方法を記載する。

Pxxは1回のbounded Coding Agent executionとして実行可能なscopeにする。

### Step 7 — Coding Agentを起動する

`40_operator_workflows/agent_entry_prompts/`を使用する。

HumanはGate / Trial / Package等のidentityだけを入力し、path / filenameはderived variablesで組み立てる。

Coding Agentはassigned scopeを越えず、execution completion / interruption時にはstatus reportを残す。

Work Packageごとにcheckpointを作成しても、それをGate PASSと表現してはならない。

### Step 8 — Candidate Assemblyを行う

すべての必要なimplementation scopeが完了したらTrial candidateを組み立てる。

最低限確認する。

- package chain completeness
- unresolved blocker
- integration / Gate-wide regression
- protected passed-Gate regressionのCoding-side self-check
- candidate-affecting uncommitted changeなし
- Fixed Trial Candidate SHA
- Implementation Completion Report

完了状態は`READY_FOR_TEST`であり、Gate PASSではない。

### Step 9 — Independent Test / Auditを実行する

Test / Audit Agentは07をAcceptance Criteria authorityとして、Fixed Trial Candidateを独立検証する。

`30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/`へTest Item reportを作成し、最後に`999_gate_decision`を作成する。

### Step 10 — Gate Decisionに従って遷移する

```text
PASS
  -> Gate Contract established
  -> Current State Control Sheetへverified stateをpromotion
  -> passed-Gate contractをprotected化
  -> next Gateへ進行可能

FAIL
  -> Gate contract validityを確認
  -> validなら08 Trial Remediation ContractをDELTA / CONSOLIDATEDで作成
  -> invalidなら09 Gate Contract Amendmentへ移行
  -> next Trial candidateを作る

BLOCKED
  -> prerequisite / environment / contract ambiguity等を解消
  -> Trial identityの扱いを明示
```

---

## 4. Gate vs Work Packageの判定規則

以下を満たす作業単位はGate候補である。

1. 独立したsemantic claimを持つ。
2. その単位だけPASSしたとき、後続が成果へ安全に依存できる。
3. protected contractとして保存する意味がある。

以下の場合はWork Package候補である。

1. 単独完了してもdownstream利用可能性を確立しない。
2. Gate Contract成立のための途中実装である。
3. 分割理由がexecution size / dependency / failure localization / Agent restart resilienceである。

**実装難易度だけを理由にGateを細分化してはならない。**

禁止例:

```text
「このGateは大きいので Gate-A / Gate-B / Gate-C に分ける」
```

それぞれが独立したacceptance contractを持たないなら、GateではなくWork Packageへ分解する。

同様に、次の状態は存在しない。

```text
P02 COMPLETE -> Gate partially PASS
```

正しくは:

```text
P02 = PACKAGE_COMPLETE
Gate = IN_PROGRESS
```

---

## 5. Canonical identifiers and naming

project-wide invariantとして以下を使用する。

```text
Enhancement ID       : project-defined canonical identifier
Enhancement Short ID : artifact naming用short form
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

標準pattern:

```text
{{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
{{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_implementation_completion_report.md
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_{{TEST_ITEM_ID}}_test_item.md
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_999_gate_decision.md
{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
```

表記揺れを避け、IDはtemplate内で一貫して使用する。

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

### 6.5. 08 = Trial Remediation Contract

- Independent Verificationのformal FAIL後にのみ作成する。
- original 06 / 07をimmutable historical contractとして保持する。
- FAIL evidence確定後に`DELTA / CONSOLIDATED`を選択する。
- `DELTA`: still-valid 06 / 07の必要sectionだけを参照し、failure-specific correction / re-verification deltaを記載する。
- `CONSOLIDATED`: next Trialに必要なeffective implementation / verification contextを08内へ統合する。
- どちらのmodeでもGate semantic claim / Acceptance Criteriaをsilent changeしない。
- Work Package remediationでは必要に応じR01-R99へ分解し、Rxx自体はself-contained Primary Execution Contractとする。
- failed candidate / failed evidenceを上書きしない。

### 6.6. 09 = Gate Contract Amendment

06/07自体が誤っていることが判明した場合、それはTrial remediationではない。Human / architecture ownerへ戻し、`A01...` Amendment recordで再承認する。

AmendmentがP00 / package instructionをinvalidateする場合、それらもversioned re-baselineする。

「テストに落ちたためACを変更してPASS」する運用は禁止する。

---

## 7. Candidate Assembly and evidence identity

### 7.1. Evidence hierarchy

commit / evidence identityを最低3階層に分ける。

```text
Package Checkpoint SHA
  = 1 Work Packageのimplementation checkpoint

Fixed Trial Candidate SHA
  = 全implementation scope統合後、Gate-wide self-verificationを終え
    Independent Testへ渡す唯一のcandidate

Tested Repository State
  = Test Agentが実際にcheckout / observeしたrepository state
```

Acceptance判定の主対象は**Fixed Trial Candidate**である。

### 7.2. Documentation-only post-candidate changes

Fixed Trial Candidate固定後にreport-only commit等が生じる場合、production / test / migration / dependency semanticsが変わっていないことを明示する。

Tested Repository StateがFixed Trial Candidate SHAと異なる場合、Test / Audit Agentは差分を監査し、candidate semanticsが不変であることをevidence化する。確認不能なら`BLOCKED`または`FAIL`とする。

---

## 8. Passed-Gate immutability

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

## 9. Transition Debt

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

## 10. Document authority domains and conflict rule

文書を単一のtotal precedenceだけで理解せず、**authority domain**を分離する。Primary Execution Contractは自分のdomainのnormative meaningを本文内に持つ。

```text
06 Gate Coding Contract
  -> Gate implementation semantic authority

07 Gate Verification Contract
  -> Gate acceptance / AC authority

Pxx / Rxx Primary Execution Contract
  -> assigned bounded Coding execution authority
  -> effective constraintsを自身に保持

08 Trial Remediation Contract
  -> specific next-Trial remediation authority
  -> DELTA / CONSOLIDATED
  -> Gate semantic claim / ACは変更不可

09 Gate Contract Amendment
  -> explicit Human-approved contract-change decision
  -> approval後に06 / 07 / affected plansをre-baseline

Implementation / Test / State artifacts
  -> observed fact / evidence / decision / verified-state indexの各domainのみ
```

### Conflict rule

- Primary contract同士にsemantic conflictを検出した場合、Agentは勝手にprecedence解釈で修復せず`BLOCKED_CONTRACT_AMBIGUITY`とする。
- approved 09が存在する場合、どのprimary contractをre-baselineしたかを明示し、過去Trial contractを上書きしない。
- 08 DELTAが参照するparent sectionsは08内で一意に列挙する。
- 08 CONSOLIDATEDはnext Trialのremediation contextを統合するが、original Gate claim / ACをsilent overrideしない。
- evidence / source / Control Sheetはnormative contractを暗黙変更するauthorityを持たない。

## 11. Agent boundaries

### 11.1. Coding Agent

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

### 11.2. Test / Audit Agent

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

## 12. Parameterized operator prompt rules

Agent起動promptは、Humanが少数のidentity variablesを宣言し、derived variableを展開してpath / filenameを決定する形式を標準とする。

MUST:

- UPPER_SNAKE_CASE variableを使用する。
- Human-supplied / Derivedを分離する。
- `{{VARIABLE}}`を再帰展開する。
- execution開始前に未解決placeholderがないことを確認する。
- globが複数instructionに一致する場合、任意選択せず停止する。

標準promptは`40_operator_workflows/agent_entry_prompts/`に配置する。各prompt自身に、必要な変数規則・対象path導出・停止条件・記録方法を含めるため、実行時に別のvariable guideを必須参照させない。

---

## 13. Preflight / prerequisite

product Gate判定とexecution prerequisiteを混同しない。

環境、DB、migration baseline、外部service、credential、test fixture等がGate execution前提の場合、`40_operator_workflows/preflight/`で独立確認する。

- Preflight failure = product acceptance FAILではない。
- prerequisite未成立時はGateを`BLOCKED`扱いにできる。
- destructive reset等はcontrolled runbookを使用する。

---

## 14. Architecture discovery — conditional workflow

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

## 15. Requirement levels

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

## 16. Instantiation checklist

このdirectoryを実enhancementへコピーした後、以下を順に行う。

1. `{{...}}`を具体値へ置換する。
2. 不要なconditional workflow skeletonを削除または`N/A`化する。
3. enhancement background / requirements / designを作成する。
4. Gate decompositionを確定する。
5. Current State Control Sheetの初期verified baselineを作る。
6. Gateごとに`{{GATE_ID}}` directoryを作る。
7. Gate開始前に06/07をfreezeする。
8. Execution Modeを選択する。
9. Work Package ModeならP00を作成し、P01+ instructionを作る。
10. Trial開始時に`20/30`のTrial directoryを作る。
11. parameterized operator promptのidentity variablesを設定する。
12. 未解決meta variableがないことを確認してAgentを起動する。
13. Candidate Assembly後にFixed Trial Candidateを固定する。
14. Independent Verification後、Gate Decisionに従ってControl Sheetを更新する。

---

## 17. Human audit checklist

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

## 18. 更新履歴

この節はテンプレート利用方法ではなく、schemaの変更履歴を確認するための情報である。詳細は`90_change_history/`を参照する。

### Schema v11

- canonical filename / directory nameをASCII characters + technical Englishへ統一。
- 06 / 07 primary contractおよび00 planning / requirement / design artifactから日本語filenameを除去。
- TEMPLATE_STRUCTURE / MANIFEST / operator promptのderived naming ruleを同期。

### Schema v3

- GateとAgent execution scopeを明示的に分離。
- Trialをcandidate-to-independent-verification transactionとして定義。
- Work Package / Candidate Assembly / package checkpointをfirst-class artifact化。
- Fixed Trial CandidateをIndependent Verificationの標準targetとして明文化。
- parameterized operator promptとderived naming ruleを標準化。

### Schema v2

- Gate-local 06 / 07 contractを導入。
- Trial remediation contract、PASS-only verified-state promotion、Passed-Gate immutabilityを導入。
- Current State Control Sheet、Transition Debt、document authority / precedenceを整備。

過去schemaとの差分は通常のエンハンス計画作成時に読む必要はない。workflowのmigration、template保守、historical audit時のみ参照する。
