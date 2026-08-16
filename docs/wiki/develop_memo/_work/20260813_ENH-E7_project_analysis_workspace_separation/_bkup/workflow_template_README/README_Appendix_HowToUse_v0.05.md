# README Appendix — How to Use the Agentic Enhancement Workflow

> Document class: Operator How-To / Runbook Appendix  
> Document version: v0.05  
> Audience: Human operator / workflow maintainer  
> Scope: planning 完了後から Work Package 実装、Gate verification、次 Gate への移行、Enhancement 完了まで  
> Initial reference: ENH-E7 / workflow v0.07  
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

本書の実行手順は、後続の Phase A〜F と1対1で対応する。

各 Phase は「何をするか」だけでなく、**目的**と**Phase完了時にあるべき状態**を先に理解してから実行する。

```text
Planning / Requirements / Design 完了
    ↓
Phase A — Gate を実行可能にする
    目的:
      Gate-level implementation / verification contract を確定し、
      Work Package Coding を安全に開始できる状態にする。
    完了状態:
      upstream prerequisiteが成立し、deferred design questionが解消され、
      Gate 06 / 07がexecution authorityとして利用可能。

    A1 upstream prerequisite を確認
    A2 deferred Architecture / Design question を解消
    A3 Gate 06 implementation contract を確定
    A4 Gate 07 verification contract を確定
    A5 Pxx self-containment を確認
    A6 Gate 06 / 07 を freeze
    ↓
Phase B — Work Package を1本実行する
    目的:
      dependency-readyなPxxを1本ずつ、Minimum Sufficient Contextで実装する。
    完了状態:
      assigned Pxxが PACKAGE_COMPLETE、または継続不能理由が明示的にBLOCKEDとして残る。

    B1 次の PACKAGE_ID を決定
    B2 preflight で execution eligibility を確認
    B3 Coding Agent を起動
    B4 package result を確認
    B5 次 package へ進む
    ↓
    required Pxx がすべて PACKAGE_COMPLETE
    ↓
Phase C — Candidate Assembly: 各Gateにおける複数 Work Package 実装完了時の結果の統合
    目的:
      package単位の実装結果をGate単位で統合し、正式検証対象candidateを確定する。
    完了状態:
      Gate-wide integration self-checkが成立し、Fixed Trial Candidateがfreezeされ、READY_FOR_TEST。
    ↓
Phase D — Independent Verification: Gate Candidate の独立検証
    目的:
      Coding側の判断から独立して、Gate 07をauthorityとしてcandidateを検証する。
    完了状態:
      required Test Itemのevidenceが揃い、999 Gate Decisionを行える。
    ↓
Phase E — 999 Gate Decision: Gate の最終判定
    目的:
      Gateの正式な品質判定を PASS / FAIL / BLOCKED として確定する。
    完了状態:
      canonical 999 reportに最終判定と根拠が記録される。
    ↓
Phase F — Current State promotion と次 Gate: PASS成果の昇格と次工程への移行
    目的:
      PASSしたGateだけをverified current stateへ昇格し、次GateまたはEnhancement完了へ進む。
    完了状態:
      Current Stateがcanonical PASS evidenceを反映し、次工程のprerequisiteが明確。
    ↓
Next Gate の Phase A
    または
Enhancement completion
```

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

v0.07 instanceで実行時に参照する主要状態を一覧化する。

| 対象文書 / Artifact | Field / Result | 主な値 | 意味 | 単独で実行制御するか |
|---|---|---|---|---|
| Pxx contract（fieldが存在する場合） | `Status at issuance` | `DRAFT_NOT_FROZEN` 等 | 発行時点の診断・履歴metadata | **No** |
| Gate 06 | `Contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | implementation contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Gate 07 | `Verification contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | verification / acceptance contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Preflight | result severity | `FAIL`, `WARN`, `INFO` | Coding開始前のreadiness診断 | `FAIL`のみblocking |
| Package execution status report | `State` | `PACKAGE_COMPLETE`, `PACKAGE_BLOCKED` | assigned Pxx実装の完了 / 継続不能 | dependency導出に使用 |
| Coding停止理由 | outcome label | `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`, `PACKAGE_BLOCKED_CONTRACT_CHANGE_REQUIRED` 等 | BLOCKED理由の分類 | BLOCKEDとして扱う |
| Gate implementation completion report | `Candidate state` | `READY_FOR_TEST`, `BLOCKED` | Gate candidateが独立検証可能か | Yes |
| `999_gate_decision` | `Gate decision` | `PASS`, `FAIL`, `BLOCKED` | Gateの最終判定 | **Gate authority** |
| `Current_State_Control_Sheet.md` | verified state | instance依存のhuman-readable state | final PASS済み状態のpromotion結果 | 999 evidenceから更新 |

`Current_State_Control_Sheet.md` のhuman-readable literalはinstanceごとに異なり得る。verified stateのauthorityは literal 自体ではなく、canonical `999 Gate Decision = PASS` と紐づくevidenceである。

#### 0.4.1. Package-level `Status at issuance`

例:

```text
**Status at issuance:** DRAFT_NOT_FROZEN
```

v0.07 では diagnostic / issuance metadata として扱い、Pxx execution eligibility を直接制御しない。

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

`PASS` のみ verified current state へpromotionできる。

### 0.5. Preflight とは何か

Preflight は、

> Coding Agent が安全かつ迷わず assigned Work Package を開始できるか

を確認するための**実行前readiness check**である。

Workflow artifact の形式的完全性を証明する仕組みではない。

実際の実行手順は Phase B の `Step B2 — preflight` で扱う。本セクションでは概念だけを説明する。

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
- PASS 後の Current State promotion
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

### 1.3. Candidate Assembly Agent

全 required Pxx 完了後に Gate-level candidate を組み立てる。

### 1.4. Independent Verification Test Agent

Acceptance authority は frozen Gate 07。

Coding Agent Pxx を Acceptance Criteria 補完に使わない。

---

## 2. Phase A — Gate を実行可能にする

**主担当:** Human/operator  
LLM / script は source discovery、contract review、preflight などの補助に利用する。最終的に「Gateを開始してよいか」を判断するのは Human/operator である。

**目的:** upstream prerequisite、deferred design question、implementation / verification contractを確定し、Work Package Codingを安全に開始できるGate-level authorityを整える。

**作業後にあるべき状態:** Gate 06 / 07がexecution authorityとして利用可能で、各Pxxがself-contained、P01またはdependency-ready Pxxに対してpreflightを実行できる。

Work Package Coding を開始する前に Gate contract を準備する。

### 2.0. Phase A 最低限クイックチェック

詳細を読む前に、Human/operator は最低限次だけ確認する。

| Step | 最低限見る場所 | 確認する箇所 | 進行可能な状態 | 未達の場合 |
|---|---|---|---|---|
| A1 | `Current_State_Control_Sheet.md`、upstream Gateの `30_test_report/<GATE>/Trial<TRIAL>/..._999_gate_decision.md` | Current Stateのverified state / open prerequisite、`Gate decision` | 必須upstreamが `PASS` evidenceで確認でき、対象Gateを妨げるprerequisiteがない | upstream Gateを完了する。対象GateのCodingへ進まない |
| A2 | `00_enhance_background/04_design_revision.md`、`05_requirements_design_consistency_and_traceability_review.md`、必要ならArchitecture Review artifact | deferred / unresolved事項、Freeze rule | source confirmationにdeferされた項目が解消され、Gateに影響するunresolved itemが0件 | Architecture Discovery / source confirmationを実施する |
| A3 | `10_enhance_instruction/<GATE>/06_Ariadne_<ENH>_<GATE>_implementation_instruction.md` | 冒頭 `Contract status`、特に Gate定義・必須semantics・Allowed/Prohibited scope・Protected contract・API/persistence方針・Stop condition | 内容確定後は `Contract status: FROZEN`。実装上の意味・scopeに未解決事項がない | 06を修正・レビューする |
| A4 | `10_enhance_instruction/<GATE>/07_Ariadne_<ENH>_<GATE>_test_instruction.md` | 冒頭 `Verification contract status`、Acceptance Criteria・Test Item plan・Browser E2E・Decision semantics・Required output | 内容確定後は `Verification contract status: FROZEN`。PASS条件に未解決事項がない | 07を修正・レビューする |
| A5 | `10_enhance_instruction/<GATE>/06_<GATE>_Pxx_*.md` | 冒頭metadata、Entry criteria、Required implementation、Focused verification、handoff、completion / stop rule | `Self-containment: MUST`、`Information isolation: MUST`。assigned Pxx単独で実装判断に必要な情報が揃う | Pxxを補完する。Coding Agentに他文書を探索させない |
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
Pxx self-contained
        ↓
Phase B の preflight へ進む
```

`Status at issuance: DRAFT_NOT_FROZEN` などの **Pxx package-level status literal は、このクイックチェックの合否条件にしない。**

### 2.1. Step A1 — upstream prerequisite を確認する

**目的:** この Gate を開始するために必要な upstream Gate / artifact が正式に成立していることを確認し、未成立の前提を抱えたまま downstream 実装へ進むことを防ぐ。

**作業後にあるべき状態:** 対象 Gate の全 upstream prerequisite が canonical evidence で満たされており、upstream dependency が Gate開始の blocker ではない。

**最低限これを見る:**

```text
Current_State_Control_Sheet.md
  -> 対象Gateのopen prerequisite

30_test_report/<UPSTREAM_GATE>/Trial<TRIAL>/
  <ENH>_<UPSTREAM_GATE>_Trial<TRIAL>_999_gate_decision.md
  -> Gate decision: PASS
```

upstream Gateを必要としないGateでは、Current State上で開始を妨げるprerequisiteがないことだけ確認する。

Gate README / P00 / Current State を Human/operator が確認する。

例:

```text
G02 depends on G01 final PASS
```

なら、canonical G01 `999_gate_decision` が `PASS` であることを確認する。

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

source confirmation が defer されている場合、Gate freeze 前に解消する。

ENH-E7 例:

```text
Data Quality
TIME_TREND
CHART
```

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
10_enhance_instruction/<GATE>/
  06_Ariadne_<ENH>_<GATE>_implementation_instruction.md

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
10_enhance_instruction/<GATE>/
  07_Ariadne_<ENH>_<GATE>_test_instruction.md

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

### 2.5. Step A5 — Pxx self-containment を確認する

**目的:** Coding Agent が assigned Pxx だけを読めば、不要な横断探索や設計補完なしに実装できる Minimum Sufficient Context を保証する。

**作業後にあるべき状態:** 各 Pxx が scope、変更理由、変更対象、禁止事項、dependency、completion condition、focused verification、handoff contract を自己完結して説明している。

**最低限これを見る:**

```text
10_enhance_instruction/<GATE>/06_<GATE>_Pxx_*.md

冒頭metadata:
  Self-containment: MUST
  Information isolation: MUST
  Gate: <GATE>
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

不足している場合は Gate freeze 前に修正する。

### 2.6. Step A6 — Gate 06 / 07 を freeze

**目的:** implementation contract と verification contract を execution authority として確定し、Gate を Work Package 実行へ移せる状態にする。

**作業後にあるべき状態:** unresolved semantic / acceptance blocker がなく、Gate 06 / 07 が frozen authority として利用可能で、P01 preflight を実行できる。

**最低限これを見る:**

```text
10_enhance_instruction/<GATE>/README.md
  -> Gate contract が利用可能であること

06_Ariadne_<ENH>_<GATE>_implementation_instruction.md
  -> Contract status: FROZEN

07_Ariadne_<ENH>_<GATE>_test_instruction.md
  -> Verification contract status: FROZEN
```

上記3点が成立したら Phase B のpreflightへ進む。

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

## 3. Phase B — Work Package を1本実行する

**目的:** dependency-readyなWork Packageを1本ずつ、assigned Pxxだけをnormative contractとして実装し、不要な探索とworkflow理解コストを抑える。

**作業後にあるべき状態:** 対象Pxxが `PACKAGE_COMPLETE` になり次dependencyのevidenceとして利用可能、または継続不能理由が `PACKAGE_BLOCKED*` として明示される。

### 3.1. Step B1 — 次の PACKAGE_ID を決める

**目的:** dependency graph に従って、現在実行候補となる Work Package を一意に選択する。

**作業後にあるべき状態:** 実行対象の `GATE_ID` / `PACKAGE_ID` / `TRIAL_NO` が明確で、preflight に渡す runtime identity が確定している。

Human/operator は Gate README / P00 の dependency graph を見る。

実行可否の最終判定は preflight が evidence から導出する。

### 3.2. Step B2 — preflight

**目的:** Coding Agent を起動する前に、誤対象・未成立dependency・未確定Gate contractなど、実作業へ影響する blocker がないことを確認する。

**作業後にあるべき状態:** Hard `FAIL` がなく、`WARN` / `INFO` がある場合も意味を把握したうえで、Coding Agent を安全に開始できる。

ENH-E7 例:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . \
  --gate G01 \
  --package P01 \
  --trial 01
```

```text
FAILあり      -> Coding Agentを開始しない
WARN/INFOのみ -> 実行継続可能
```

### 3.3. Step B3 — Coding Agent 起動

**目的:** assigned Pxx の self-contained contract に限定して実装と focused verification を行い、不要な仕様探索を避ける。

**作業後にあるべき状態:** assigned scope の実装・局所検証・handoff report 作成までが完了するか、継続不能なら理由が `PACKAGE_BLOCKED*` として明示されている。

```text
下記ファイルを実行せよ

- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01

プロンプトの際の基本言語は日本語とする
```

### 3.4. Step B4 — package result 確認

**目的:** Coding Agent の作業結果が assigned Pxx の completion condition を満たし、次のdependency判定に利用できる正式なhandoffになっていることを確認する。

**作業後にあるべき状態:** 正常時は canonical package report が存在し `State: PACKAGE_COMPLETE` であり、scope外変更・未解決blockerがない。

正常完了:

```text
State: PACKAGE_COMPLETE
```

Canonical report:

```text
20_implementation_reports/<GATE>/Trial<TRIAL>/packages/
ENH-E7_<GATE>_<PACKAGE>_Trial<TRIAL>_package_execution_status.md
```

確認事項:

- assigned scope 完了
- focused verification PASS
- unresolved blocker なし
- scope外変更なし
- package report あり

### 3.5. Step B5 — 次 package

**目的:** package status の手動書換えではなく、実際の completion evidence と dependency から次の実行可否を導出し、同じ手順で後続Pxxへ進む。

**作業後にあるべき状態:** 次候補 Pxx に対して preflight を再実行できる。全 required Pxx 完了時は Phase C — Candidate Assembly へ移行できる。

次 Pxx document の status を変更しない。

次 Pxx に対して再度 preflight を実行する。

preflight が completion evidence から eligibility を導出する。

---

## 4. Phase C — Candidate Assembly: 各Gateにおける複数 Work Package 実装完了時の結果の統合

**目的:** 各 Work Package の実装結果をGate単位で統合し、Independent Verificationへ渡す1つのFixed Trial Candidateを確定する。

**作業後にあるべき状態:** required Pxx がすべて完了し、Gate-wide integration / regression self-checkに重大なblockerがなく、Fixed Trial Candidateがfreezeされ `READY_FOR_TEST` になっている。

全 required Pxx が `PACKAGE_COMPLETE` になったら実行する。

Prompt:

```text
40_operator_workflows/agent_entry_prompts/
20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md
```

Human input:

```text
GATE_ID=<Gxx>
TRIAL_NO=<NN>
```

Candidate Assembly では Gate 全体を確認する。

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
20_implementation_reports/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_implementation_completion_report.md

20_implementation_reports/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_implementation_report_detail.md
```

Fixed Trial Candidate SHA を package 単位で freeze しない。

---

## 5. Phase D — Independent Verification: Gate Candidate の独立検証

**目的:** Coding側の実装判断から独立して、frozen Gate 07をAcceptance authorityとしてFixed Trial Candidateを検証する。

**作業後にあるべき状態:** Gate 07で要求されたTest Itemのevidenceが揃い、Product判定可能な場合はPASS/FAIL、判定不能ならBLOCKEDとして999 Gate Decisionへ進める。

`READY_FOR_TEST` 後に Test Agent を実行する。

Prompt:

```text
40_operator_workflows/agent_entry_prompts/
30_independent_verification_01_test_agent_prompt.md
```

Human input:

```text
GATE_ID=<Gxx>
TRIAL_NO=<NN>
```

Execution:

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

## 6. Phase E — 999 Gate Decision: Gate の最終判定

**目的:** Gate-level verification evidenceを基に、Gateの正式な最終判定をcanonical artifactとして確定する。

**作業後にあるべき状態:** `999_gate_decision` に `PASS / FAIL / BLOCKED` のいずれかと根拠が記録され、次のoperator actionが一意に決まる。

### 6.1. PASS

```text
Gate decision: PASS
```

なら Gate は正式 PASS。

次に Current State promotion。

### 6.2. FAIL

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

### 6.3. BLOCKED

identity / environment / harness / prerequisite / verification contract ambiguity 等で Product 判定不能。

`BLOCKED` を Product FAIL と解釈しない。

---

## 7. Phase F — Current State promotion と次 Gate: PASS成果の昇格と次工程への移行

**目的:** final PASSで検証済みとなったGate成果だけをverified current stateへ昇格し、次GateまたはEnhancement completionへ安全に遷移する。

**作業後にあるべき状態:** `Current_State_Control_Sheet.md` がcanonical PASS evidenceとFixed Trial Candidate identityを反映し、downstream GateのprerequisiteまたはEnhancement完了条件が明確になっている。

Gate PASS 後だけ `Current_State_Control_Sheet.md` を更新する。

最低限:

- Gate decision = PASS
- Fixed Trial Candidate SHA
- canonical 999 evidence path
- Gate で成立した protected semantics

```text
PACKAGE_COMPLETE
READY_FOR_TEST
```

では promotion しない。

### 7.1. 次 Gate がある場合

前 Gate PASS 後、次 Gate Coding を即開始できるとは限らない。

次 Gate に deferred design / source confirmation が残っていれば先に freeze 作業を行う。

```text
Previous Gate 999 PASS
    ↓
Current State promotion
    ↓
Next Gate source/design confirmation
    ↓
Next Gate 06 / 07 freeze
    ↓
Next Gate P01 preflight
    ↓
Coding
```

Gate contract readiness で preflight が止まる場合、これは package status literal の問題ではなく、**Gate-level contract が未確定である可能性を最初に確認する**。

---

## 8. Cross-Phase Exception Handling — BLOCKED / environment 問題

Phase A〜F の途中で発生する `BLOCKED` は、独立した工程ではなく、各 Phase を横断する例外状態として扱う。

原則として、`BLOCKED` は formal Product FAIL と同義ではない。原因を分類し、blocker を解消したうえで、同じ Phase / Gate / Package / Trial の適切な地点から再開する。

### 8.1. `BLOCKED_PRECHECK`

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

### 8.2. `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`

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

### 8.3. `PACKAGE_BLOCKED`

runtime / implementation / environment 等で completion 不能。

これは formal Gate FAIL ではない。

原因を分類する。

```text
Product/code
Contract
Dependency
Environment/harness
```

### 8.4. Browser E2E / environment blocker

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

### 8.5. Trial を増やすか

`PACKAGE_BLOCKED` / `BLOCKED_PRECHECK` だけでは自動的に Trial を増やさない。

Formal Gate FAIL 後の approved remediation では next Trial を使う。

---

## 9. Artifact authority map

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

## 10. Operator prompt / script quick reference

| Goal | Entry point |
|---|---|
| Architecture / source discovery | `40_operator_workflows/architecture_review/01_architecture_discovery_prompt.md` |
| Preflight | `40_operator_workflows/preflight/check_agent_execution_readiness.py` |
| Work Package Coding | `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` |
| Candidate Assembly | `40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| Independent Verification | `40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md` |
| Formal FAIL remediation | `40_operator_workflows/agent_entry_prompts/40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Gate orchestration | `40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md` |
| Preflight regression self-test | `40_operator_workflows/preflight/selftest_check_agent_execution_readiness.py` |

Manual mode では Human/operator が各段階を明示的に起動する。

Gate Orchestrator を使っても Coding Agent isolation / 999 authority は変更しない。

---

## 11. やってはいけないこと

### 11.1. Package status を workflow cursor にする

```text
DRAFT_NOT_FROZEN
    ↓ manual edit
READY_TO_EXECUTE
```

で次 package を unlock しない。

### 11.2. Coding Agent に workflow 全体を探索させる

Pxx が不足しているなら Design側を修正する。

### 11.3. `PACKAGE_COMPLETE` を Gate PASS とみなす

Gate PASS は 999 のみ。

### 11.4. Work Package ごとに Gate級 SHA / acceptance を要求する

Fixed Candidate は Candidate Assembly で Gate単位に固定する。

### 11.5. SHA / placeholder / naming の表記差だけで止める

実害がなければ WARN / INFO を優先する。

### 11.6. Gate 06 / 07 の未freezeを status 問題として無視する

unresolved semantic / acceptance blocker があるなら実質的 blocker。

### 11.7. environment BLOCKED を Product FAIL にする

Product violation が verified された場合だけ FAIL。

---

## 12. End-to-End operator flow

```text
[0] Planning / Requirements / Design
        ↓
[1] Architecture Review / source confirmation
        ↓
[2] Gate 06 / 07 freeze
        ↓
[3] P01 preflight
        ↓
[4] P01 Coding → PACKAGE_COMPLETE
        ↓
[5] dependency-ready Pxxを順次 preflight → Coding
        ↓
    all required Pxx complete
        ↓
[6] Candidate Assembly
        ↓
    READY_FOR_TEST + Fixed Trial Candidate
        ↓
[7] Independent Verification
        ↓
[8] 999 Gate Decision
     ├─ PASS
     │    ↓
     │  Current State promotion
     │    ↓
     │  Next Gate freeze / execution
     │
     ├─ FAIL
     │    ↓
     │  approved remediation / next Trial
     │
     └─ BLOCKED
          ↓
        prerequisite / environment / contract blocker解消
```

---

## 13. Operator checklist

### 13.1. Gate開始前

- [ ] upstream Gate dependency がある場合、canonical 999 が PASS
- [ ] Current State が最新 PASS evidence を反映
- [ ] Architecture / source confirmation の unresolved blocker なし
- [ ] Gate 06 implementation semantics 確定
- [ ] Gate 07 Acceptance Criteria / Test Item 確定
- [ ] Pxx self-contained
- [ ] Pxx dependency 明示
- [ ] package handoff contract が Pxx 内で理解可能
- [ ] current branch 正常
- [ ] preflight FAILなし

Package-level `Status at issuance` の文字列一致は本質条件ではない。

### 13.2. Work Package完了後

- [ ] assigned scope のみ変更
- [ ] focused verification PASS
- [ ] unresolved blocker なし
- [ ] canonical package status report 作成
- [ ] `State: PACKAGE_COMPLETE`
- [ ] 次 Pxx status を手動変更していない
- [ ] 次 Pxx は preflight で再判定

### 13.3. Gate PASS後

- [ ] canonical 999 = PASS
- [ ] Fixed Trial Candidate SHA 記録
- [ ] Current State promotion
- [ ] protected contract set 更新
- [ ] downstream Gate prerequisite 確認
- [ ] deferred design があれば next Gate freeze を先に実行
- [ ] final Gateなら cross-gate integration / regression の不足確認
- [ ] Enhancement完了後、必要な Canonical Requirements 更新

---

## 14. README 本文との役割分担

### 14.1. Root `README.md`

- workflow instance 概要
- Gate一覧
- Quick Start
- 最重要 execution principles
- 本Appendixへのリンク

### 14.2. `README_Appendix_HowToUse_v0.05.md`

- end-to-end operator procedure
- Gate freeze / transition
- Work Package execution
- BLOCKED / FAIL handling
- Candidate Assembly
- Independent Verification
- Current State promotion
- status / evidence semantics

### 14.3. Subdirectory README

各 layer 固有の詳細 contract / canonical path / artifact semantics。

本Appendixは各READMEを置き換えず、**「どの順番で何を見るか」**を説明する。

Root READMEと重複する最小概念は、実行中に参照するクイックリファレンスとしてINTRODUCTIONへ意図的に残す。詳細仕様のauthorityは各contract / artifact側に置く。

---

## 15. Workflow Template 次版への反映

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
Work Package != Gate quality boundary
```

本書の成功条件は、Human/operator が workflow 内部protocolを推測せず、

> **今どの段階で、次にどの prompt / script を実行し、何を確認すべきか**

を README 体系だけから判断できることである。
