# README Appendix — How to Use the Agentic Enhancement Workflow

> Document class: Operator How-To / Runbook Appendix  
> Document version: v0.08  
> Audience: Human operator / workflow maintainer  
> Scope: planning 完了後から Gate implementation、Gate verification、次 Gate への移行、Enhancement 完了まで  
> Authority: 各 Enhancement instance の frozen contract / assigned Pxx / Gate 07 が本書より優先する

---

## 0. INTRODUCTION

### 0.1. この文書の目的

Root `README.md` の Quick HowToUse は、1 Work Package を開始する入口と最重要原則を簡潔に説明する。

本書は Human/operator が、workflow 全体について次を迷わず判断できるようにするための **クイックリファレンス** である。

```text
今どの段階か
    ↓
この段階で何を達成するのか
    ↓
次に何を確認するか
    ↓
どの script / prompt を実行するか
    ↓
作業後にどの状態になっていればよいか
    ↓
PASS / BLOCKED / FAIL をどう解釈するか
    ↓
次の工程へどう進むか
```

Workflow の目的は workflow protocol 自体を厳密に証明することではない。

優先するものは、

- Separation of Concerns
- Minimum Sufficient Context
- No Unnecessary Exploration
- Artifact-based Handoff
- Gate-level Quality Assurance
- Derived State over Declared State
- Semantic Validation over String Validation
- FAIL / WARN / INFO separation

である。

本書内では見出しレベルを次の用語で統一する。

| Markdown | 呼称 | 番号形式 |
|---|---|---|
| `##` | チャプタ | `X.` |
| `###` | セクション | `X.Y.` |
| `####` | サブセクション | `X.Y.Z.` |
| `#####` | サブサブセクション | `X.Y.Z.A.` |

### 0.2. 基本フロー

本書の実行手順は、後続の Phase A〜F と対応する。

各 Phase は「何をするか」だけでなく、**目的**と**Phase完了時にあるべき状態**を先に理解してから実行する。

`Planning / Requirements / Design` は **本書のスコープ外** である。本書は、それらの成果物が作成・レビュー済みで、対象Gateの実行準備へ移れる状態から開始する。

```text
Planning / Requirements / Design
    本書のスコープ外
    ↓
    成果物が利用可能になったら本書の運用開始
    ↓
Phase A — Gate を実行可能にする
    目的:
      Gate-level implementation / verification contract を確定し、
      implementation execution を安全に開始できる状態にする。
    完了状態:
      upstream prerequisiteが成立し、deferred design questionが解消され、
      Gate 06 / 07がexecution authorityとして利用可能。

    A1 upstream prerequisite を確認
    A2 deferred Architecture / Design question を解消
    A3 Gate 06 implementation contract を確定
    A4 Gate 07 verification contract を確定
    A5 実行モードに応じたimplementation contractを確認
       - Work Packageあり: Pxx self-containment
       - Work Packageなし: Gate-wide single execution contract
    A6 Gate 06 / 07 を freeze
    ↓
    Gateの実行モードを確認
    ├─ Work Packageあり
    │    ↓
    │  Phase B1 — Work Package を実行する
    │    目的:
    │      dependency-readyなPxxを1本ずつ、Minimum Sufficient Contextで実装する。
    │    完了状態:
    │      required PxxがすべてPACKAGE_COMPLETE、または継続不能理由がBLOCKEDとして明示される。
    │    ↓
    │  required Pxx がすべて PACKAGE_COMPLETE
    │    ↓
    │  Phase C — Candidate Assembly
    │    Work Package mode固有:
    │      複数Work Packageの実装結果をGate Candidateへ統合する。
    │    ↓
    │  Phase D — Independent Verification
    │    Work Package mode固有:
    │      統合済みFixed Trial Candidateを独立検証する。
    │    ↓
    │  Phase E — 999 Gate Decision
    │
    └─ Work Packageなし
         ↓
       Phase B2 — Gate 全体を実行する
         目的:
           Gate-wide single execution contractに従い、Gate全体を1 execution unitとして実装・検証する。
         完了状態:
           Gate-level final decisionに必要なimplementation / verification evidenceが揃う。
         ↓
       Phase E — 999 Gate Decision

Phase E — 999 Gate Decision: Gate の最終判定
    目的:
      Gateの正式な品質判定を PASS / FAIL / BLOCKED として確定する。
    完了状態:
      canonical 999 reportに最終判定と根拠が記録される。
    ↓
Phase F — 次 Gate への遷移 / Enhancement completion
    目的:
      canonical Gate PASS evidenceを基に、次Gate dependency成立またはEnhancement完了を判断し、
      mutable state sheetを介さず次工程へ進む。
    完了状態:
      downstream Gate dependencyはcanonical 999 Gate Decisionから判定でき、
      次Gateがある場合はREADME + Gate 06 + Gate 07からreadinessを確認できる。
    ↓
Next Gate の Phase A
    または
Enhancement completion
```

**Phase C / Phase D は Phase B1（Work Package mode）の場合にのみ実施する。**

Work Packageを持たないGateでは Phase B2 を使用する。具体的な single-execution prompt / artifact contract は各workflow instanceの定義に従う。

実際に Phase B1 / B2 のどちらを使用するかは、対象workflow instanceのGate decompositionとoperator prompt routingをauthorityとして判断する。single execution promptがdisabledならPhase B2は使用しない。

### 0.3. 実行前に理解する最小概念

Root `README.md` にも一部同じ概念が記載されている。本セクションは仕様正本を重複させるためではなく、**実行中に最低限参照するためのクイックリファレンス**として残す。

#### 0.3.1. Gate

Gate は**意味のあるコード変更成果の正式な品質保証境界**である。

```text
Gate
├─ Implementation Contract (06)
├─ Verification Contract (07)
├─ Work Package(s)
├─ Gate-level Candidate
├─ Independent Verification
└─ 999 Gate Decision
```

#### 0.3.2. Work Package

Work Package は Coding Agent が迷わず実装できるサイズへ Gate を分割したもの。

```text
Work Package
    ↓
bounded implementation + focused verification

Gate
    ↓
integration + formal independent verification
```

Work Package は Gate と同じ acceptance boundary ではない。

#### 0.3.3. Trial

Trial は Gate candidate の verification attempt である。

Formal FAIL remediation で次 Trial へ進む。

`BLOCKED_PRECHECK` や `PACKAGE_BLOCKED` は、それだけで formal Gate FAIL を意味しない。

#### 0.3.4. Candidate

Candidate は required Work Package の結果をGate単位で統合し、Independent Verificationの対象として固定したrepository stateである。

Fixed Trial Candidate SHAは Work Package 単位ではなく Gate boundary で扱う。

### 0.4. 状態値と実行可否の読み方

状態値はすべて同じ重要度ではない。**実行可否を直接制御する状態、成果物から導出される状態、診断・履歴用metadata**を区別する。

#### 0.4.0. 状態値クイックリファレンス

実行時に参照する主要状態を一覧化する。

| 対象文書 / Artifact | Field / Result | 主な値 | 意味 | 単独で実行制御するか |
|---|---|---|---|---|
| Pxx contract（fieldが存在する場合） | `Status at issuance` | `DRAFT_NOT_FROZEN` 等 | 発行時点の診断・履歴metadata | **No** |
| Gate README | Gate-level readiness / prerequisite summary | instance依存 | Gateの実行前提・06/07参照・実行モードの入口 | Gate readiness確認に使用 |
| Gate 06 | `Contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | implementation contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Gate 07 | `Verification contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | verification / acceptance contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Preflight | result severity | `FAIL`, `WARN`, `INFO` | Coding開始前のreadiness診断 | `FAIL`のみblocking |
| Package execution status report | `State` | `PACKAGE_COMPLETE`, `PACKAGE_BLOCKED` | assigned Pxx実装の完了 / 継続不能 | dependency導出に使用 |
| Coding停止理由 | outcome label | `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`, `PACKAGE_BLOCKED_CONTRACT_CHANGE_REQUIRED` 等 | BLOCKED理由の分類 | BLOCKEDとして扱う |
| Gate implementation completion report | `Candidate state` | `READY_FOR_TEST`, `BLOCKED` | Gate candidateが独立検証可能か | Yes |
| `999_gate_decision` | `Gate decision` | `PASS`, `FAIL`, `BLOCKED` | Gateの最終判定 | **Gate authority** |

#### 0.4.1. Package-level `Status at issuance`

例:

```text
**Status at issuance:** DRAFT_NOT_FROZEN
```

本HowToUseでは diagnostic / issuance metadata として扱い、Pxx execution eligibility を直接制御しない。

したがって、

```text
Status at issuance = DRAFT_NOT_FROZEN
+
Gate contract ready
+
dependencies complete
+
preflight FAILなし
    ↓
execution eligible
```

は成立し得る。

Pxx status を `READY_TO_EXECUTE` へ手動変更して workflow cursor にしない。

#### 0.4.2. Gate 06 / 07 readiness

Gate 06 / 07 の未freezeは package-level status と同じ意味ではない。

未freezeの理由が、

- implementation semantics 未確定
- Acceptance Criteria 未確定
- unresolved Architecture / Design decision

である場合、Gate contract はまだ execution authority ではないため Coding を開始しない。

重要なのは `FROZEN` という文字列そのものではなく、**設計・acceptance contract が本当に確定していること**である。

#### 0.4.3. Preflight `FAIL / WARN / INFO`

```text
FAIL
  -> BLOCKED
  -> 誤実装・誤対象・未依存実行につながり得るため停止

WARN
  -> 実行継続可能
  -> 確認価値はあるが非blocking

INFO
  -> 診断・追跡情報
```

#### 0.4.4. Package execution state

正常完了は、canonical package execution status reportの

```text
State: PACKAGE_COMPLETE
```

で表す。

継続不能時は `PACKAGE_BLOCKED` とし、必要に応じて `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY` 等で理由を分類する。

```text
PACKAGE_COMPLETE
    != READY_FOR_TEST
    != Gate PASS
```

#### 0.4.5. `READY_FOR_TEST`

Candidate Assembly が Gate-level integration を確認し、Fixed Trial Candidate を freeze した状態。

Work Package完了とは異なり、Independent Verificationへ進めるGate-level stateである。

#### 0.4.6. Gate `PASS / FAIL / BLOCKED`

最終 authority は canonical `999_gate_decision` のみ。

```text
Gate decision: PASS
Gate decision: FAIL
Gate decision: BLOCKED
```

`PASS` のみ downstream Gate dependency を正式に満たす。Gate間dependencyのauthorityは canonical `999_gate_decision` である。


#### 0.4.7. Mutable state sheet は持たない

Workflow の進行状態を集約する mutable state sheet は作成しない。

必要な状態は、用途ごとに既存の canonical artifact から導出する。

| 判定したいこと | Authority |
|---|---|
| Pxx dependency | upstream package の `package execution status report` |
| Gate dependency | upstream Gate の canonical `999_gate_decision` |
| Gate readiness | 対象 Gate の `README` + Gate `06` + Gate `07` |
| Candidate readiness | Gate の `implementation completion report` |

```text
Declared mutable state
    ではなく
Canonical evidence
    ↓
Derived state
```

同じ状態を別ファイルへ転記して同期対象を増やさない。

### 0.5. Preflight とは何か

Preflight は、

> Coding Agent が安全かつ迷わず assigned Work Package を開始できるか

を確認するための**実行前readiness check**である。

Workflow artifact の形式的完全性を証明する仕組みではない。

実際の実行手順は、Work Package modeでは Phase B1 の `Step B1-2 — preflight`、Work Packageなしでは各instanceのsingle-execution readiness contractで扱う。本セクションでは概念だけを説明する。

#### 0.5.1. Hard Fail にすべき代表例

- WORK_ROOT が解決不能
- assigned Pxx が一意でない
- Gate / Package / Trial が不明
- wrong branch
- Gate contract に実質的 unresolved blocker がある
- required dependency completion evidence がない
- prompt が Coding Agent information isolation を破る

#### 0.5.2. 原則 WARN / INFO にすべき代表例

- package status literal の差異
- traceability 用 SHA の単純な差異
- repository identity を誤らせない remote alias 差異
- explanatory placeholder
- optional metadata 欠落
- cosmetic naming mismatch

判断基準:

> これは誤ったコードを書くこと、または誤った対象を検証することを具体的に防ぐために Hard Fail である必要があるか？

No なら WARN / INFO を優先する。

---

## 1. 実行主体と参照範囲

### 1.1. Human/operator

Human/operator は routing authority。

主な仕事:

- runtime identity の指定
- Architecture / Design blocker の解消
- Gate 06 / 07 freeze
- 次 Pxx の選択
- preflight 確認
- Coding / Candidate Assembly / Test Agent 起動
- Gate PASS 後の次 Gate / Enhancement completion 判定
- formal FAIL / amendment の分岐判断

### 1.2. Work Package Coding Agent

Normative workflow contract:

```text
Enhancement-specific Coding prompt
+
assigned Pxx only
```

仕様補完目的で以下を読ませない。

```text
Gate 06 / 07
P00
other Pxx
00 background
20 reports
30 reports
previous Enhancement artifacts
ADR / issue / external Web
```

source / tests / config / migrations / runtime facts は assigned Pxx scope の implementation substrate として調査可。

Pxx が不足しているなら Agent に探索させず、Design/operator 側で Pxx を直す。

### 1.3. Single Execution Coding Agent

Work Packageを持たないGateで、Gate全体を1 execution unitとして扱う場合に使用する。

具体的な実行契約・成果物・verification handoffは各workflow instanceのsingle-execution contractに従う。

対象workflow instanceでsingle execution promptがdisabledの場合は使用しない。

### 1.4. Candidate Assembly Agent

Phase B1（Work Package mode）で全 required Pxx 完了後に Gate-level candidate を組み立てる。

### 1.5. Independent Verification Test Agent

Phase B1（Work Package mode）では、Acceptance authority は frozen Gate 07。

Coding Agent Pxx を Acceptance Criteria 補完に使わない。

---

## 2. Phase A — Gate を実行可能にする

**主担当:** Human/operator  
LLM / script は source discovery、contract review、preflight などの補助に利用する。最終的に「Gateを開始してよいか」を判断するのは Human/operator である。

**目的:** upstream prerequisite、deferred design question、implementation / verification contractを確定し、Gateのimplementation executionを安全に開始できるGate-level authorityを整える。

**作業後にあるべき状態:** Gate 06 / 07がexecution authorityとして利用可能で、Work Package modeなら各Pxxがself-contained、Work PackageなしならGate-wide single execution contractが利用可能である。

Implementation execution を開始する前に Gate contract を準備する。

### 2.0. Phase A 最低限クイックチェック

詳細を読む前に、Human/operator は最低限次だけ確認する。

| Step | 最低限見る場所 | 確認する箇所 | 進行可能な状態 | 未達の場合 |
|---|---|---|---|---|
| A1 | 対象GateのREADME / P00等のdependency declaration、upstream Gateの `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/..._999_gate_decision.md` | 必須upstream Gate、`Gate decision` | 必須upstreamが canonical `999 Gate Decision = PASS` で確認できる | upstream Gateを完了する。対象GateのCodingへ進まない |
| A2 | `00_enhance_background/04_design_revision.md`、`05_requirements_design_consistency_and_traceability_review.md`、必要ならArchitecture Review artifact | deferred / unresolved事項、Freeze rule | source confirmationにdeferされた項目が解消され、Gateに影響するunresolved itemが0件 | Architecture Discovery / source confirmationを実施する |
| A3 | `10_enhance_instruction/<GATE_ID>/06_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_implementation_instruction.md` | 冒頭 `Contract status`、特に Gate定義・必須semantics・Allowed/Prohibited scope・Protected contract・API/persistence方針・Stop condition | 内容確定後は `Contract status: FROZEN`。実装上の意味・scopeに未解決事項がない | 06を修正・レビューする |
| A4 | `10_enhance_instruction/<GATE_ID>/07_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_test_instruction.md` | 冒頭 `Verification contract status`、Acceptance Criteria・Test Item plan・Browser E2E・Decision semantics・Required output | 内容確定後は `Verification contract status: FROZEN`。PASS条件に未解決事項がない | 07を修正・レビューする |
| A5 | Work Packageあり: `10_enhance_instruction/<GATE_ID>/06_<GATE_ID>_Pxx_*.md` / Work Packageなし: instance-specific single execution contract | Work Package mode: Pxx metadata・Entry criteria・Required implementation・Focused verification・handoff・completion / stop rule。Single execution mode: Gate-wide scope・completion・verification handoff | 選択した実行モードだけで必要十分な実装判断ができる | 不足contractを補完する。Coding Agentにworkflow全体を探索させない |
| A6 | Gate README、06、07 | Gate-level readiness | READMEがGate contract利用可能状態を示し、06 / 07がともにFROZEN。Pxx `Status at issuance` は判定材料にしない | freeze finalizationを行う |

**最短判定:**

```text
upstream PASS / prerequisite OK
    +
deferred / unresolved design item = 0
    +
Gate 06 = FROZEN
    +
Gate 07 = FROZEN
    +
execution mode contract ready
        ↓
Work Packageあり  -> Phase B1
Work Packageなし  -> Phase B2
```

`Status at issuance: DRAFT_NOT_FROZEN` などの **Pxx package-level status literal は、このクイックチェックの合否条件にしない。**

### 2.1. Step A1 — upstream prerequisite を確認する

**目的:** この Gate を開始するために必要な upstream Gate / artifact が正式に成立していることを確認し、未成立の前提を抱えたまま downstream 実装へ進むことを防ぐ。

**作業後にあるべき状態:** 対象 Gate の全 upstream prerequisite が canonical evidence で満たされており、upstream dependency が Gate開始の blocker ではない。

**最低限これを見る:**

```text
対象Gateの README / P00 等
  -> upstream Gate dependency の宣言

30_test_report/<UPSTREAM_GATE>/Trial<TRIAL_NO>/
  <ENHANCEMENT_ID>_<UPSTREAM_GATE>_Trial<TRIAL_NO>_999_gate_decision.md
  -> Gate decision: PASS
```

upstream Gateを必要としないGateでは、Gate dependency evidenceの確認は不要。

Human/operator は、dependency の定義を対象Gateのplan / READMEから確認し、
**dependencyが満たされたかどうかは canonical 999 Gate Decisionだけで判定する。**

例:

```text
<NEXT_GATE_ID> depends on <UPSTREAM_GATE_ID> final PASS
```

なら、canonical `<UPSTREAM_GATE_ID>` `999_gate_decision` が `PASS` であることを確認する。

### 2.2. Step A2 — deferred Architecture / Design question を解消する

**目的:** Planning 時点で source confirmation に defer された設計判断を実コード・tests・config・runtime factsから確定し、Coding Agent に再設計や推測をさせない。

**作業後にあるべき状態:** Gate 06 / 07 および Pxx を確定するために必要な source fact と design decision が明示され、未解決の deferred question が残っていない。

**最低限これを見る:**

```text
00_enhance_background/04_design_revision.md
  -> source confirmationへdeferされた記述が残っていないか

00_enhance_background/05_requirements_design_consistency_and_traceability_review.md
  -> Freeze rule
  -> Gateに影響するArchitecture unresolved item = 0
```

deferred itemがある場合のみArchitecture Discovery / source inspectionへ進む。最初から全sourceを再探索しない。

source confirmation が defer されている場合、Gate freeze 前に解消する。対象項目はそのEnhancementのPlanning / Design artifactに記録されたdeferred questionをauthorityとし、このHowToUse側へ個別テーマをハードコードしない。

Architecture Discovery prompt がある場合:

```text
40_operator_workflows/architecture_review/
01_architecture_discovery_prompt.md
```

Discovery では Product code を変更しない。

Facts と Design recommendation を分離する。

### 2.3. Step A3 — Gate 06 を確定する

**目的:** Gate が何を実装し、どこまでを変更可能範囲とするかを implementation authority として確定する。

**作業後にあるべき状態:** Gate objective、scope、protected contract、実装上の主要semanticsが一意であり、Coding側が Gate-level 方針を再構築する必要がない。

**最低限これを見る:**

```text
10_enhance_instruction/<GATE_ID>/
  06_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_implementation_instruction.md

冒頭:
  Contract status: FROZEN       <- A6完了時の期待値

最低限確認するセクション:
  Gate定義 / Acceptance claim
  必須implementation semantics
  Allowed scope
  Explicitly prohibited scope
  Protected passed-Gate contract
  API / persistence / migration方針
  Stop condition
```

`FROZEN` への文字列変更だけを行わない。上記セクションの意味が確定した結果としてFROZENにする。

少なくとも次を確認する。

- Gate objective / claim
- allowed / prohibited scope
- protected passed-Gate contract
- API / persistence / domain semantic policy
- Work Package decomposition との整合
- unresolved implementation semantic blocker がない

### 2.4. Step A4 — Gate 07 を確定する

**目的:** Gate が何を満たせば PASS かを independent verification authority として確定し、実装結果に合わせてAcceptance Criteriaが後付けで変わることを防ぐ。

**作業後にあるべき状態:** Acceptance Criteria、Test Item、candidate identity、regression / Browser E2E obligation、PASS / FAIL / BLOCKED semantics が明確である。

**最低限これを見る:**

```text
10_enhance_instruction/<GATE_ID>/
  07_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_test_instruction.md

冒頭:
  Verification contract status: FROZEN   <- A6完了時の期待値

最低限確認するセクション:
  Acceptance Criteria
  Test Item plan
  Browser E2E
  Protected passed-Gate regression
  Decision semantics
  Required output artifact contract
```

実装結果を見てからAcceptance Criteriaを作り替えない。

少なくとも次を確認する。

- Acceptance Criteria
- Test Item mapping
- candidate identity rule
- protected regression
- Browser E2E obligation
- PASS / FAIL / BLOCKED semantics
- canonical test report / 999 output contract

### 2.5. Step A5 — 実行モードに応じた contract completeness を確認する

**目的:** 選択した実行モードだけを読めば、Coding Agent が不要な横断探索や設計補完なしに実装できる Minimum Sufficient Context を保証する。

**作業後にあるべき状態:** Work Package modeでは各Pxxがself-contained、Work PackageなしではGate-wide single execution contractがself-containedである。

#### 2.5.1. Work Package がある場合

**最低限これを見る:**

```text
10_enhance_instruction/<GATE_ID>/06_<GATE_ID>_Pxx_*.md

冒頭metadata:
  Self-containment: MUST
  Information isolation: MUST
  Gate: <GATE_ID>
  Package: <Pxx>
  Depends on: <dependency>

本文:
  Entry criteria
  Required implementation
  Focused verification
  Package handoff artifact contract
  Package completion criteria
  Stop rule
```

`Status at issuance` はここでの実行可否判定には使用しない。

Coding Agent が assigned Pxx だけで以下を理解できること。

- 何を変更するか
- なぜ変更するか
- どこを変更するか
- 何を変更してはいけないか
- dependency
- completion condition
- focused verification
- package handoff report path / required content

#### 2.5.2. Work Package がない場合

Gate全体を1 execution unitとして扱う single-execution contract を確認する。

最低限、次が一意であること。

- Gate-wide implementation scope
- prohibited scope
- completion condition
- required verification / evidence
- Gate 07へのhandoff方法
- stop / BLOCKED condition

具体prompt / artifact contractはworkflow instance側をauthorityとする。single execution promptがdisabledなら、この分岐は使用しない。

不足している場合は Gate freeze 前に修正する。

### 2.6. Step A6 — Gate 06 / 07 を freeze

**目的:** implementation contract と verification contract を execution authority として確定し、Gate を Work Package 実行へ移せる状態にする。

**作業後にあるべき状態:** unresolved semantic / acceptance blocker がなく、Gate 06 / 07 が frozen authority として利用可能で、P01 preflight を実行できる。

**最低限これを見る:**

```text
10_enhance_instruction/<GATE_ID>/README.md
  -> Gate contract が利用可能であること

06_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_implementation_instruction.md
  -> Contract status: FROZEN

07_<SYSTEM_ID>_<ENHANCEMENT_ID>_<GATE_ID>_test_instruction.md
  -> Verification contract status: FROZEN
```

上記3点が成立したら実行モードを確認し、Work Packageありなら Phase B1、Work Packageなしなら Phase B2 へ進む。

unresolved semantic blocker がゼロになった時点で freeze する。

**Pxx の `Status at issuance` を `READY_TO_EXECUTE` に変更する必要はない。**

### 2.7. Gate freeze finalization を LLM に依頼する場合

専用 prompt がない場合は次の趣旨で依頼する。

```text
対象Gateのfreeze作業を実施せよ。

source discoveryで確認されたFactsを基礎として、
Coding Agentがassigned Pxxだけを読んで再設計せず実装でき、
Test Agentが07だけをAcceptance authorityとして検証できる状態へcontractを確定する。

確認事項:
- unresolved design decisionの解消
- Requirements / Design / Pxx / AC / Test Itemの整合
- Pxx self-containment
- 06 implementation semanticsの確定
- 07 acceptance semanticsの確定
- protected passed-Gate contractの明示
- API / persistence / domain semantic変更の許可範囲

unresolved semantic blockerがゼロの場合のみGate 06/07をfreezeする。
Product code / test codeは変更しない。
```

単なる status literal の置換作業にしてはならない。

---

## 3. Phase B1 — Work Package を実行する: Work Package がある Gate の実装

**目的:** dependency-readyなWork Packageを1本ずつ、assigned Pxxだけをnormative contractとして実装し、不要な探索とworkflow理解コストを抑える。

**作業後にあるべき状態:** 対象Pxxが `PACKAGE_COMPLETE` になり次dependencyのevidenceとして利用可能、または継続不能理由が `PACKAGE_BLOCKED*` として明示される。

### 3.1. Step B1-1 — 次の PACKAGE_ID を決める

**目的:** dependency graph に従って、現在実行候補となる Work Package を一意に選択する。

**作業後にあるべき状態:** 実行対象の `GATE_ID` / `PACKAGE_ID` / `TRIAL_NO` が明確で、preflight に渡す runtime identity が確定している。

Human/operator は Gate README / P00 の dependency graph を見る。

実行可否の最終判定は preflight が evidence から導出する。

### 3.2. Step B1-2 — preflight

**目的:** Coding Agent を起動する前に、誤対象・未成立dependency・未確定Gate contractなど、実作業へ影響する blocker がないことを確認する。

**作業後にあるべき状態:** Hard `FAIL` がなく、`WARN` / `INFO` がある場合も意味を把握したうえで、Coding Agent を安全に開始できる。

基本形:

```bash
python3 docs/wiki/develop_memo/_work/<WORK_ROOT>/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . \
  --gate <GATE_ID> \
  --package <PACKAGE_ID> \
  --trial <TRIAL_NO>
```

```text
FAILあり      -> Coding Agentを開始しない
WARN/INFOのみ -> 実行継続可能
```

### 3.3. Step B1-3 — Coding Agent 起動

**目的:** assigned Pxx の self-contained contract に限定して実装と focused verification を行い、不要な仕様探索を避ける。

**作業後にあるべき状態:** assigned scope の実装・局所検証・handoff report 作成までが完了するか、継続不能なら理由が `PACKAGE_BLOCKED*` として明示されている。

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/<WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- PACKAGE_ID=<PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

### 3.4. Step B1-4 — package result 確認

**目的:** Coding Agent の作業結果が assigned Pxx の completion condition を満たし、次のdependency判定に利用できる正式なhandoffになっていることを確認する。

**作業後にあるべき状態:** 正常時は canonical package report が存在し `State: PACKAGE_COMPLETE` であり、scope外変更・未解決blockerがない。

正常完了:

```text
State: PACKAGE_COMPLETE
```

Canonical report:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/packages/
<ENHANCEMENT_ID>_<GATE_ID>_<PACKAGE_ID>_Trial<TRIAL_NO>_package_execution_status.md
```

確認事項:

- assigned scope 完了
- focused verification PASS
- unresolved blocker なし
- scope外変更なし
- package report あり

### 3.5. Step B1-5 — 次 package

**目的:** package status の手動書換えではなく、実際の completion evidence と dependency から次の実行可否を導出し、同じ手順で後続Pxxへ進む。

**作業後にあるべき状態:** 次候補 Pxx に対して preflight を再実行できる。全 required Pxx 完了時は Phase C — Candidate Assembly へ移行できる。Phase C / D はこの Phase B1 を使用した場合にのみ実施する。

次 Pxx document の status を変更しない。

次 Pxx に対して再度 preflight を実行する。

preflight が completion evidence から eligibility を導出する。

---

## 4. Phase B2 — Gate 全体を実行する: Work Package がない Gate の実装

**適用条件:** 対象GateにWork Packageが定義されておらず、workflow instanceがGate-wide single execution modeを明示的に有効化している場合のみ使用する。

**目的:** Gate全体を1 execution unitとして実装し、Work Package分割を前提とせずGate-level final decisionに必要なimplementation / verification evidenceを作成する。

**作業後にあるべき状態:** instance-specific single execution contractで要求された実装・検証・handoffが完了し、Phase E — 999 Gate Decisionへ進めるだけのcanonical evidenceが揃っている。

Phase B2を使用できるのは、対象workflow instanceでsingle execution promptが明示的に有効な場合だけである。disabledまたは未定義ならPhase B2へ進まない。

### 4.0. Phase B2 最低限クイックチェック

| 確認対象 | 最低限見る場所 | 進行可能な状態 |
|---|---|---|
| execution mode | Gate decomposition / operator prompt routing | Work Packageなし、かつ single execution が明示的に有効 |
| Gate 06 / 07 | `10_enhance_instruction/<GATE_ID>/06...`, `07...` | 両contractがexecution / verification authorityとして利用可能 |
| single execution prompt | `40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md` | instanceでdisabledではない |
| completion / verification handoff | instance-specific single execution contract | Phase Eへ進むためのrequired evidenceが明示されている |

### 4.1. Step B2-1 — Gate-wide single execution contract を確認する

**目的:** Work Packageを使わないGateで、実装範囲・完了条件・verification handoffを1つのcontractとして確定する。

**作業後にあるべき状態:** Human/operatorが、どのpromptを起動し、何をもってGate-wide execution完了とするかを一意に判断できる。

### 4.2. Step B2-2 — Single Execution Coding Agent を起動する

instanceでsingle execution promptが有効な場合、Human/operatorはinstance-specific entry promptへ runtime identity を渡す。

Template上の基本形:

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/<WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_01_single_execution_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

対象workflow instanceでsingle execution promptがdisabledなら、この実行例は使用しない。

### 4.3. Step B2-3 — Gate-wide result を確認する

**目的:** single execution contractで要求された実装・検証・handoff evidenceが揃い、formal Gate Decisionへ進めることを確認する。

**作業後にあるべき状態:** Candidate Assembly / Work Package-specific Independent Verificationを経由せず、instance-specific contractに従ってPhase Eへ進める。

Phase C / Phase D は Phase B1 固有の処理であり、Phase B2では実施しない。

---

## 5. Phase C — Candidate Assembly: 各Gateにおける複数 Work Package 実装完了時の結果の統合

**適用条件:** Phase B1（Work Package mode）を使用したGateのみ。Phase B2では実施しない。

**目的:** 各 Work Package の実装結果をGate単位で統合し、Independent Verificationへ渡す1つのFixed Trial Candidateを確定する。

**作業後にあるべき状態:** required Pxx がすべて完了し、Gate-wide integration / regression self-checkに重大なblockerがなく、Fixed Trial Candidateがfreezeされ `READY_FOR_TEST` になっている。

全 required Pxx が `PACKAGE_COMPLETE` になったら実行する。

### 5.1. Candidate Assembly Agent 実行プロンプト

Human/operatorは次の形式で実行する。

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/<WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

`GATE_ID` / `TRIAL_NO` は実行対象に置換する。

### 5.2. Candidate Assembly で確認すること

- required package set complete
- unresolved package blocker なし
- Gate-wide integration self-check
- protected regression
- applicable Browser E2E self-check
- candidate-affecting diff audit
- Fixed Trial Candidate SHA freeze

正常完了:

```text
Candidate state: READY_FOR_TEST
```

Gate-level reports:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
<ENHANCEMENT_ID>_<GATE_ID>_Trial<TRIAL_NO>_implementation_completion_report.md

20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
<ENHANCEMENT_ID>_<GATE_ID>_Trial<TRIAL_NO>_implementation_report_detail.md
```

Fixed Trial Candidate SHA を package 単位で freeze しない。

---

## 6. Phase D — Independent Verification: Gate Candidate の独立検証

**適用条件:** Phase B1（Work Package mode）を使用し、Phase Cで `READY_FOR_TEST` のFixed Trial Candidateを作成したGateのみ。Phase B2では実施しない。

**目的:** Coding側の実装判断から独立して、frozen Gate 07をAcceptance authorityとしてFixed Trial Candidateを検証する。

**作業後にあるべき状態:** Gate 07で要求されたTest Itemのevidenceが揃い、Product判定可能な場合はPASS/FAIL、判定不能ならBLOCKEDとして999 Gate Decisionへ進める。

`READY_FOR_TEST` 後に Test Agent を実行する。

### 6.1. Independent Verification Agent 実行プロンプト

Human/operatorは次の形式で実行する。

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/<WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 30_independent_verification_01_test_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

`GATE_ID` / `TRIAL_NO` は実行対象に置換する。

### 6.2. Independent Verification の実行内容

```text
Candidate identity audit
    ↓
Gate 07 Test Items
    ↓
protected regression / Browser E2E
    ↓
999 Gate Decision
```

Test Agent は production / test implementation を修復しない。

---

## 7. Phase E — 999 Gate Decision: Gate の最終判定

**目的:** Gate-level verification evidenceを基に、Gateの正式な最終判定をcanonical artifactとして確定する。

**作業後にあるべき状態:** `999_gate_decision` に `PASS / FAIL / BLOCKED` のいずれかと根拠が記録され、次のoperator actionが一意に決まる。

### 7.0. Phase E 最低限クイックチェック

Human/operatorは、詳細なtest reportを最初から読み直す前に最低限次を確認する。

| 最低限見る場所 | 確認する箇所 | 期待する状態 / 判断 |
|---|---|---|
| Phase B1の場合: `20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/..._implementation_completion_report.md` | `Candidate state`、Fixed Trial Candidate identity | `READY_FOR_TEST` とcandidate identityが確定済み |
| Phase B1の場合: `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/` | Gate 07でrequiredなTest Item report | required Test Itemのevidenceが揃っている |
| Phase B2の場合: instance-specific Gate-wide execution / verification evidence | Gate 07が要求するevidence | Phase Eの判定に必要なevidenceが揃っている |
| `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/<ENHANCEMENT_ID>_<GATE_ID>_Trial<TRIAL_NO>_999_gate_decision.md` | `Gate decision` | `PASS` / `FAIL` / `BLOCKED` のいずれかが明示されている |
| 同999 report | candidate / tested repository identity、根拠evidence | 判定対象と根拠が追跡可能 |

**最低限の読み方:**

```text
Gate decision: PASS
    -> Phase Fへ進む

Gate decision: FAIL
    -> formal FAIL remediationへ進む

Gate decision: BLOCKED
    -> Product FAILと決めつけずblockerを解消する
```

### 7.1. PASS

```text
Gate decision: PASS
```

なら Gate は正式 PASS。

次に Phase F へ進む。

### 7.2. FAIL

Formal FAIL。

```text
FAIL evidence
    ↓
approved 08 remediation contract
    ↓
next Trial
    ↓
40_fail_remediation_01_fail_rework_coding_agent_prompt.md
```

Acceptance Criteria を実装に合わせて書き換えない。

Gate semantic claim 自体が誤りなら 09 Gate Contract Amendment が必要。

### 7.3. BLOCKED

identity / environment / harness / prerequisite / verification contract ambiguity 等で Product 判定不能。

`BLOCKED` を Product FAIL と解釈しない。

---

## 8. Phase F — 次 Gate への遷移 / Enhancement completion: canonical evidenceから次工程を決定する

**目的:** final PASSを新しいmutable stateへ転記せず、canonical evidenceから downstream dependency と次工程を判断する。

**作業後にあるべき状態:** 次Gateがある場合は upstream `999 Gate Decision = PASS` によりGate dependencyが満たされ、対象Gateの `README + Gate 06 + Gate 07` からreadinessを確認できる。次GateがなければEnhancement completionへ進める。

**重要:** 廃止したstate sheetの代替となる mutable state sheet は作成しない。

### 8.0. Phase F 最低限クイックチェック

| 判定対象 | 最低限見るartifact | 進行可能な状態 |
|---|---|---|
| 前Gateの正式完了 | canonical `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/..._999_gate_decision.md` | `Gate decision: PASS` |
| downstream Gate dependency | upstream Gateのcanonical `999_gate_decision` | 必須upstream Gateがすべて `PASS` |
| 次Gate readiness | 次Gate `README` + Gate `06` + Gate `07` | unresolved blockerなし、06/07がexecution authorityとして利用可能 |
| Candidate readiness | `20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/..._implementation_completion_report.md` | instance contractで定義されたtest-ready state |
| Pxx dependency | upstream Pxxの `package execution status report` | required upstream Pxxが `PACKAGE_COMPLETE` |

```text
状態を1枚のsheetへ集約しない
        ↓
用途ごとのcanonical artifactを直接見る
```

### 8.1. 次 Gate がある場合

前 Gate PASS 後、次 Gate Coding を即開始できるとは限らない。

まず前Gateのcanonical `999_gate_decision` を downstream dependency evidence として扱う。
その上で、次Gateの `README + Gate 06 + Gate 07` から Gate readiness を確認する。

次 Gate に deferred design / source confirmation が残っていれば先に freeze 作業を行う。

```text
Previous Gate canonical 999 = PASS
    ↓
Next Gate dependency satisfied
    ↓
Next Gate README + Gate 06 + Gate 07
    ↓
deferred itemあり?
    ├─ Yes -> source/design confirmation -> Gate 06 / 07 freeze
    └─ No  -> Gate readiness確認
    ↓
Next Gate implementation execution
```

Gate contract readiness で preflight が止まる場合、package status literal ではなく、
**Gate-level contract に実質的 unresolved blocker が残っていないか**を最初に確認する。

次GateにPlanning時点のdeferred source confirmationが残る場合は、以下の2段階を正式な遷移として扱う。

### 8.2. Next Gate freeze前の source confirmation をLLMに実施させる

**目的:** 次Gate contractをfreezeする前に、Planning / Designでdeferされたsource factをcurrent source / tests / config / runtime factsから確定する。

**作業後にあるべき状態:** 次Gate implementation / verification contractを確定するために必要なsource factsとdesign recommendationが分離され、freezeをBLOCKする未解決事項の有無が明示されている。

#### 8.2.1. 汎用実行プロンプト

Human/operatorは、対象workflow instanceのArchitecture Discovery promptを次の形式で実行する。

```text
下記ファイルを実行せよ。

docs/wiki/develop_memo/_work/<WORK_ROOT>/
40_operator_workflows/architecture_review/
01_architecture_discovery_prompt.md

目的は <NEXT_GATE_ID> Gate contract freeze 前の source confirmation である。

特に、Planning / Requirements / Design artifactで
source confirmationへdeferされた項目を列挙し、各項目について以下を確定すること。

- current source / tests / config / runtime factsから確認できる事実
- 現行実装のsemantics / route / operation / persistence / API等、対象項目に必要なactual behavior
- Gate implementationに追加変更が必要か否か
- factから導かれるDesign recommendation
- freezeをBLOCKする未解決事項が残るか

制約:

- Product codeは変更しない
- test codeも変更しない
- Facts と Design recommendationを明確に分離する
- sourceに存在しない仕様・operation・behaviorを補完目的で捏造しない
- current source / tests / config / runtime factを根拠とする
- 対象Enhancementに記録されたdeferred questionだけを扱い、無関係な探索へ広げない
- 基本言語は日本語とする

最後に、<NEXT_GATE_ID> freezeをBLOCKする未解決事項が残っているかを明示すること。
```

### 8.3. discovery結果を Next Gate contractへ反映する

**目的:** source confirmationで確定したFactsをGate contract / Design / 必要なPxxへ反映し、Coding Agentがassigned contractだけで再設計せず実装できる状態にする。

**作業後にあるべき状態:** unresolved semantic blockerが0件で、次Gate 06 / 07がfrozen authorityとして利用でき、次Gate implementation executionへ進める。

#### 8.3.1. 汎用実行プロンプト

```text
<NEXT_GATE_ID> Gate contract freeze作業を実施せよ。

前工程で実施したArchitecture Discovery / source confirmationの結果を
source factとして使用すること。

目的:
<NEXT_GATE_ID> Coding Agentがassigned execution contractだけを読んで、
設計判断を再構築せず実装できる状態までcontractを確定する。

最低限の対象候補:

1.
40_operator_workflows/architecture_review/
02_target_architecture_decision_record.md

2.
00_enhance_background/
04_design_revision.md

3.
00_enhance_background/
05_requirements_design_consistency_and_traceability_review.md

4.
10_enhance_instruction/<NEXT_GATE_ID>/
06_<SYSTEM_ID>_<ENHANCEMENT_ID>_<NEXT_GATE_ID>_implementation_instruction.md

5.
10_enhance_instruction/<NEXT_GATE_ID>/
07_<SYSTEM_ID>_<ENHANCEMENT_ID>_<NEXT_GATE_ID>_test_instruction.md

6.
10_enhance_instruction/<NEXT_GATE_ID>/
README.md

7.
Discovery結果の影響を受けるPxx contractのみ。
影響しないPxxは変更しない。

実施事項:

- deferred confirmationをsource factで解消する
- source factから確定したDesign decisionを記録する
- Requirement変更が必要な場合だけRequirements artifactを変更する
- 影響を受けるPxxをself-containedにし、Coding AgentがArchitecture Reviewや背景文書を仕様補完目的で読まなくてよい状態にする
- Gate 06 implementation contractとGate 07 verification contractの内容が矛盾しないことを確認する
- Requirements → Design → Pxx / Gate execution contract → AC/Testのtraceabilityを再確認する
- unresolved semantic blockerがゼロの場合のみ、
  <NEXT_GATE_ID> Gate 06 Contract statusをFROZEN、
  <NEXT_GATE_ID> Gate 07 Verification contract statusをFROZEN
  とする
- 単なるstatus literalを合わせる目的でfreezeしてはならない
- Product code / test codeは変更しない

基本言語は日本語とする。

最後に以下を報告すること。

- source facts
- freeze時に確定したdesign decisions
- 変更ファイル
- unresolved blockers
- <NEXT_GATE_ID> の最初のexecution unitに対してpreflightを実行可能か
```

個別のdeferred question、影響Pxx、ファイル名は各Enhancement instanceのPlanning / Design artifactをauthorityとして決める。本HowToUseには特定Enhancement固有のテーマを埋め込まない。

---

## 9. Cross-Phase Exception Handling — BLOCKED / environment 問題

Phase A〜F の途中で発生する `BLOCKED` は、独立した工程ではなく、各 Phase を横断する例外状態として扱う。

原則として、`BLOCKED` は formal Product FAIL と同義ではない。原因を分類し、blocker を解消したうえで、同じ Phase / Gate / Package / Trial の適切な地点から再開する。

### 9.1. `BLOCKED_PRECHECK`

Coding 前の blocker。

代表例:

- dependency 未完了
- Gate contract 未freeze
- wrong branch
- assigned Pxx 不明

対応:

```text
blocker解消
    ↓
同じ Gate / Package / Trial でpreflight再実行
```

status literal を合わせるだけの修正は原則行わない。

### 9.2. `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`

Pxx が必要十分でない。

```text
Coding Agent停止
    ↓
Design/operatorがPxx修正
    ↓
preflight
    ↓
同じpackageを再実行
```

Coding Agent に P00 / 06 / 07 / other Pxx を読ませて補完させない。

### 9.3. `PACKAGE_BLOCKED`

runtime / implementation / environment 等で completion 不能。

これは formal Gate FAIL ではない。

原因を分類する。

```text
Product/code
Contract
Dependency
Environment/harness
```

### 9.4. Browser E2E / environment blocker

Browser E2E の environment defect と Product defect を区別する。

例:

```text
Docker disk full
Chromium launch failure
Browser harness timeout
service unavailable
```

Product 判定不能なら `PACKAGE_BLOCKED` / verification `BLOCKED` として扱う。

```text
環境問題を解消
    ↓
同一scopeを再実行
    ↓
新しいevidenceを取得
```

旧candidate / 旧scenario の evidence を、新変更の証拠として流用しない。

---

### 9.5. Trial を増やすか

`PACKAGE_BLOCKED` / `BLOCKED_PRECHECK` だけでは自動的に Trial を増やさない。

Formal Gate FAIL 後の approved remediation では next Trial を使う。

---

## 10. Artifact authority map

### 10.0. Workflow state authority quick reference

Workflow の進行状態は集約sheetへ転記せず、次のcanonical artifactから直接導出する。

| 判定対象 | Authority |
|---|---|
| Pxx dependency | upstream package の `package execution status report` |
| Gate dependency | upstream Gate の canonical `999_gate_decision` |
| Gate readiness | 対象 Gate の `README` + Gate `06` + Gate `07` |
| Candidate readiness | Gate の `implementation completion report` |

この4系統を別のmutable state fileへ再集約しない。

### 10.1. Agent別 artifact authority

| Artifact | Human/operator | Coding Agent | Candidate Assembly | Test Agent |
|---|---:|---:|---:|---:|
| `00_enhance_background/*` | Yes | No | Reference | No |
| Gate `06` | Yes | No | Gate context | No acceptance use |
| Gate `07` | Yes | No | Reference | **Authority** |
| `P00` | **Yes** | No | package set | No |
| assigned `Pxx` | Yes | **Authority** | evidence context | No acceptance use |
| other `Pxx` | Yes | **No** | package audit | No |
| package status reports | Yes | No | **Input** | No acceptance use |
| implementation completion report | Yes | No | Output | candidate identity input |
| test reports / `999` | Yes | No | No | Output |
| source / tests / config | Yes | scope内でYes | Yes | independent evidenceとしてYes |

原則:

```text
Coding Agent authority = assigned Pxx
Test Agent authority   = frozen 07
Final Gate authority   = canonical 999
```

---

## 11. Operator prompt / script quick reference

| Goal | Entry point |
|---|---|
| Architecture / source discovery | `40_operator_workflows/architecture_review/01_architecture_discovery_prompt.md` |
| Preflight | `40_operator_workflows/preflight/check_agent_execution_readiness.py` |
| Work Package Coding | `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` |
| Gate-wide Single Execution（Work Packageなし / instanceで有効な場合） | `40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md` |
| Candidate Assembly | `40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| Independent Verification | `40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md` |
| Formal FAIL remediation | `40_operator_workflows/agent_entry_prompts/40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Gate orchestration | `40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md` |
| Preflight regression self-test | `40_operator_workflows/preflight/selftest_check_agent_execution_readiness.py` |

Manual mode では Human/operator が各段階を明示的に起動する。

Gate Orchestrator を使っても Coding Agent isolation / 999 authority は変更しない。

---

## 12. やってはいけないこと

### 12.1. Package status を workflow cursor にする

```text
DRAFT_NOT_FROZEN
    ↓ manual edit
READY_TO_EXECUTE
```

で次 package を unlock しない。

### 12.2. Coding Agent に workflow 全体を探索させる

Pxx が不足しているなら Design側を修正する。

### 12.3. `PACKAGE_COMPLETE` を Gate PASS とみなす

Gate PASS は 999 のみ。

### 12.4. Work Package ごとに Gate級 SHA / acceptance を要求する

Fixed Candidate は Candidate Assembly で Gate単位に固定する。

### 12.5. SHA / placeholder / naming の表記差だけで止める

実害がなければ WARN / INFO を優先する。

### 12.6. Gate 06 / 07 の未freezeを status 問題として無視する

unresolved semantic / acceptance blocker があるなら実質的 blocker。

### 12.7. environment BLOCKED を Product FAIL にする

Product violation が verified された場合だけ FAIL。

---

## 13. End-to-End operator flow

```text
[0] Planning / Requirements / Design
        本書のスコープ外
        ↓
[1] Phase A: Architecture Review / source confirmation / Gate 06・07 freeze
        ↓
    Work Packageはあるか?
        ├─ Yes
        │    ↓
        │  [2A] Phase B1: Pxx preflight → Coding → PACKAGE_COMPLETE
        │    ↓
        │  dependency-ready Pxxを順次実行
        │    ↓
        │  all required Pxx complete
        │    ↓
        │  [3] Phase C: Candidate Assembly
        │    ↓
        │  READY_FOR_TEST + Fixed Trial Candidate
        │    ↓
        │  [4] Phase D: Independent Verification
        │    ↓
        │  [5] Phase E: 999 Gate Decision
        │
        └─ No
             ↓
           [2B] Phase B2: Gate-wide Single Execution
             ↓
           instance-specific required evidence complete
             ↓
           [5] Phase E: 999 Gate Decision

[5] Phase E: 999 Gate Decision
     ├─ PASS
     │    ↓
     │  [6] Phase F: canonical evidenceから次工程を判定
     │    ↓
     │  upstream 999 PASSでGate dependency成立
     │    ↓
     │  Next Gate README + 06 + 07 readiness確認
     │    ↓
     │  必要ならsource confirmation / contract freeze
     │    ↓
     │  Next Gate Phase A
     │
     ├─ FAIL
     │    ↓
     │  approved remediation / next Trial
     │
     └─ BLOCKED
          ↓
        prerequisite / environment / contract blocker解消
```

Phase C / D は Work Package mode（Phase B1）固有である。

## 14. Operator checklist

### 14.1. Gate開始前

- [ ] upstream Gate dependency がある場合、canonical 999 が PASS
- [ ] Architecture / source confirmation の unresolved blocker なし
- [ ] Gate 06 implementation semantics 確定
- [ ] Gate 07 Acceptance Criteria / Test Item 確定
- [ ] Pxx self-contained
- [ ] Pxx dependency 明示
- [ ] package handoff contract が Pxx 内で理解可能
- [ ] current branch 正常
- [ ] preflight FAILなし

Package-level `Status at issuance` の文字列一致は本質条件ではない。

### 14.2. Work Package完了後

- [ ] assigned scope のみ変更
- [ ] focused verification PASS
- [ ] unresolved blocker なし
- [ ] canonical package status report 作成
- [ ] `State: PACKAGE_COMPLETE`
- [ ] 次 Pxx status を手動変更していない
- [ ] 次 Pxx は preflight で再判定

### 14.3. Work PackageなしのGate-wide execution完了後

- [ ] single execution modeがinstanceで正式に有効
- [ ] Gate-wide implementation scope完了
- [ ] Gate 07が要求するverification evidenceが揃う
- [ ] Phase Eへ進むためのcanonical handoffが存在
- [ ] 対象workflow instanceでsingle execution modeが有効であることを確認

### 14.4. Gate PASS後

- [ ] canonical 999 = PASS
- [ ] Fixed Trial Candidate SHA 記録
- [ ] downstream Gate dependency は canonical 999 PASS から確認
- [ ] 次Gate readiness は README + Gate 06 + Gate 07 から確認
- [ ] deferred design があれば next Gate freeze を先に実行
- [ ] final Gateなら cross-gate integration / regression の不足確認
- [ ] Enhancement完了後、必要な Canonical Requirements 更新

---

## 15. README 本文との役割分担

### 15.1. Root `README.md`

- workflow instance 概要
- Gate一覧
- Quick Start
- 最重要 execution principles
- 本Appendixへのリンク

### 15.2. `README_Appendix_HowToUse_v0.08.md`

- end-to-end operator procedure
- Gate freeze / transition
- Work Package execution
- BLOCKED / FAIL handling
- Candidate Assembly
- Independent Verification
- Gate PASS後の次Gate遷移 / Enhancement completion判定
- status / evidence semantics

### 15.3. Subdirectory README

各 layer 固有の詳細 contract / canonical path / artifact semantics。

本Appendixは各READMEを置き換えず、**「どの順番で何を見るか」**を説明する。

Root READMEと重複する最小概念は、実行中に参照するクイックリファレンスとしてINTRODUCTIONへ意図的に残す。詳細仕様のauthorityは各contract / artifact側に置く。

---

## 16. Workflow Template 次版への反映

次版では本Appendix相当を標準生成対象にすることを推奨する。

Instance-specific に置換するもの:

```text
<ENHANCEMENT_ID>
<WORK_ROOT>
<BRANCH_NAME>
<GATE_ID>
<PACKAGE_ID>
<TRIAL_NO>
```

Template 原則として固定するもの:

```text
Derived State over Declared State
Semantic Validation over String Validation
FAIL / WARN / INFO separation
Coding Agent authority = assigned Pxx
Test Agent authority = frozen 07
Gate PASS authority = canonical 999
No mutable workflow state sheet
Pxx dependency = package execution status report
Gate dependency = canonical 999_gate_decision
Gate readiness = README + Gate 06 + Gate 07
Candidate readiness = implementation completion report
Work Package != Gate quality boundary
```

本書の成功条件は、Human/operator が workflow 内部protocolを推測せず、

> **今どの段階で、次にどの prompt / script を実行し、何を確認すべきか**

を README 体系だけから判断できることである。
