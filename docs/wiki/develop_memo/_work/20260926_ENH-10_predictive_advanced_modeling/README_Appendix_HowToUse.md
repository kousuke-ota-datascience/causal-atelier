# README Appendix — How to Use the Agentic Enhancement Workflow

> Reconstructed template baseline: 00_〜40_ canonical namespaceを統合済み。actual repository未取得のlegacy semantic bodyは `RECONSTRUCTION_NOTES.md` のboundaryに従い推測で補完しない。


> Document class: Operator How-To / Runbook Appendix  
> Document version: v0.13  
> Audience: Human operator / workflow maintainer  
> Scope: planning 完了後から Gate implementation、Gate verification、次 Gate への移行、Enhancement 完了まで  
> Authority: implementation は各 Enhancement instance の assigned execution contract、verification は frozen Gate 07、final Gate decision は canonical 999 Gate Decision が本書より優先する

---

## 1. INTRODUCTION

### 1.1. この文書の目的

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

### 1.2. 基本フロー

本書の実行手順は、後続の Phase A〜F と対応する。

`Planning / Requirements / Design` は **本書のスコープ外** である。必要な設計・source confirmationはGate 06をFROZENにするまでのauthoring inputとして扱い、FROZEN後のnormal runtimeでplanning tree全体を再読しない。

```text
Planning / Requirements / Design
    本書のスコープ外
    ↓
Phase A — Gate Entry Readiness
    read: 06 + 07 + 06-declared upstream 999
    ↓
    06.Execution mode
    ├─ WORK_PACKAGE
    │    ↓
    │  Phase B1 — assigned Pxx execution
    │    ↓ all 06.Required packages = PACKAGE_COMPLETE
    │  Phase C — Candidate Assembly
    │    ↓
    │  Implementation Completion Report
    │
    └─ SINGLE_EXECUTION
         ↓
       Phase B2 — Gate-wide implementation / candidate finalization
         ↓
       Implementation Completion Report

共通
    ↓
Phase D — Independent Verification
    authority = frozen Gate 07
    ↓
Phase E — canonical 999 Gate Decision
    ↓
Phase F — Gate Terminal Routing
    read = current canonical 999 only
    write = none
    ├─ PASS    -> current Gate COMPLETE; downstream Gateを開始するならそのGateのPhase Aへ
    ├─ FAIL    -> formal remediation
    └─ BLOCKED -> blocker resolution
```

**Phase C はWORK_PACKAGE固有。Phase D / E / Fはexecution mode共通。**

Execution modeはGate 06 `Execution mode`をauthorityとして決める。prompt file、Gate local README、P00の存在から推測しない。Gate local READMEはHuman index、P00はoptional authoring/audit artifactである。

### 1.3. 実行前に理解する最小概念

Root `README.md` にも一部同じ概念が記載されている。本セクションは仕様正本を重複させるためではなく、**実行中に最低限参照するためのクイックリファレンス**として残す。

#### 1.3.1. Gate

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

#### 1.3.2. Work Package

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

#### 1.3.3. Trial

Trial は Gate candidate の verification attempt である。

Formal FAIL remediation で次 Trial へ進む。

`BLOCKED_PRECHECK` や `PACKAGE_BLOCKED` は、それだけで formal Gate FAIL を意味しない。

#### 1.3.4. Candidate

Candidate はGate implementationの結果をGate単位で確定し、Independent Verificationの対象として固定したrepository stateである。Work Package modeではrequired Work PackageをCandidate Assemblyで統合し、Single Execution modeではGate-wide implementation完了時にcandidate finalizationを行う。

Fixed Trial Candidate SHAは Work Package 単位ではなく Gate boundary で扱う。

### 1.4. 状態値と実行可否の読み方

状態値はすべて同じ重要度ではない。**実行可否を直接制御する状態、成果物から導出される状態、診断・履歴用metadata**を区別する。

#### 1.4.1. 状態値クイックリファレンス

実行時に参照する主要状態を一覧化する。

| 対象文書 / Artifact | Field / Result | 主な値 | 意味 | 単独で実行制御するか |
|---|---|---|---|---|
| Pxx contract（fieldが存在する場合） | `Status at issuance` | `DRAFT_NOT_FROZEN` 等 | 発行時点の診断・履歴metadata | **No** |
| Gate local README | Human index / navigation | instance依存 | canonical artifactへのHuman向け入口 | **No。execution authorityではない** |
| Gate 06 | `Contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | implementation contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Gate 07 | `Verification contract status` | `FROZEN`, `DRAFT_NOT_FROZEN` | verification / acceptance contractの確定状態 | **Yes。ただし文字列ではなく実質的blocker有無が本質** |
| Preflight | result severity | `FAIL`, `WARN`, `INFO` | Coding開始前のreadiness診断 | `FAIL`のみblocking |
| Package execution status report | `State` | `PACKAGE_COMPLETE`, `PACKAGE_BLOCKED` | assigned Pxx実装の完了 / 継続不能 | dependency導出に使用 |
| Coding停止理由 | outcome label | `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`, `PACKAGE_BLOCKED_CONTRACT_CHANGE_REQUIRED` 等 | BLOCKED理由の分類 | BLOCKEDとして扱う |
| Gate implementation completion report | `Candidate state` | `READY_FOR_TEST`, `BLOCKED` | Gate candidateが独立検証可能か | Yes |
| `999_gate_decision` | `Gate decision` | `PASS`, `FAIL`, `BLOCKED` | Gateの最終判定 | **Gate authority** |

#### 1.4.2. Package-level `Status at issuance`

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

#### 1.4.3. Gate 06 / 07 readiness

Gate 06 / 07 の未freezeは package-level status と同じ意味ではない。

未freezeの理由が、

- implementation semantics 未確定
- Acceptance Criteria 未確定
- unresolved Architecture / Design decision

である場合、Gate contract はまだ execution authority ではないため Coding を開始しない。

重要なのは `FROZEN` という文字列そのものではなく、**設計・acceptance contract が本当に確定していること**である。

#### 1.4.4. Preflight `FAIL / WARN / INFO`

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

#### 1.4.5. Package execution state

正常完了は、canonical package execution status reportの

```text
State: PACKAGE_COMPLETE
```

で表す。

継続不能時は canonical package report の意味論として `PACKAGE_BLOCKED` とし、必要に応じて blocker reason を分類する。

Coding Agent prompt の terminal outcome label が `PACKAGE_READY` 等であっても、それ自体を workflow cursor にしない。assigned Pxx の completion criteria、focused verification、canonical package report の内容から package completion を導出し、canonical report では次の意味論へ正規化する。

```text
PACKAGE_READY (agent outcome; implementation-specific)
    + completion evidence satisfied
    -> State: PACKAGE_COMPLETE (canonical report semantics)

PACKAGE_COMPLETE
    != READY_FOR_TEST
    != Gate PASS
```

#### 1.4.6. `READY_FOR_TEST`

Gate-level candidate finalizationが完了し、Fixed Trial Candidateをfreezeした状態。Work Package modeではCandidate Assembly、Single Execution modeではPhase B2のcandidate finalizationがこれを担う。

Work Package完了とは異なり、Independent Verificationへ進めるGate-level stateである。

#### 1.4.7. Gate `PASS / FAIL / BLOCKED`

最終 authority は canonical `999_gate_decision` のみ。

```text
Gate decision: PASS
Gate decision: FAIL
Gate decision: BLOCKED
```

`PASS` のみ downstream Gate dependency を正式に満たす。Gate間dependencyのauthorityは canonical `999_gate_decision` である。


#### 1.4.8. Mutable state sheet は持たない

Workflow の進行状態を集約する mutable state sheet は作成しない。

必要な状態は、用途ごとに既存の canonical artifact から導出する。

| 判定したいこと | Authority |
|---|---|
| Pxx dependency | upstream package の `package execution status report` |
| Gate dependency | upstream Gate の canonical `999_gate_decision` |
| Gate readiness | Gate `06` + Gate `07` + 06-declared upstream canonical evidence + blocking preflightなし |
| Candidate readiness | Gate の `implementation completion report` |

```text
Declared mutable state
    ではなく
Canonical evidence
    ↓
Derived state
```

同じ状態を別ファイルへ転記して同期対象を増やさない。

### 1.5. Preflight とは何か

Preflight は、

> Coding Agent が安全かつ迷わず assigned Work Package を開始できるか

を確認するための**実行前readiness check**である。

Preflight は2層に分ける。

1. **Mechanical Agent Execution Readiness** — `validate_agent_execution_readiness.py` が artifact completeness / content completeness / execution resolvability / information isolation を検査する。
2. **Semantic operator check** — Human/operator が current branch、Gate 06/07の実質的blocker、dependency evidence、environment等を確認する。

mechanical validator の `OVERALL: BLOCKED` はblockingである。semantic checkでは具体的な誤実装・誤対象につながる条件を `FAIL`、非blockingな差異を `WARN / INFO` として扱う。

Workflow artifact の形式的完全性だけを証明する仕組みではない。

実際の実行手順は、Work Package modeでは Phase B1 の `Step B1-2 — preflight`、Work Packageなしでは各instanceのsingle-execution readiness contractで扱う。本セクションでは概念だけを説明する。

#### 1.5.1. Hard Fail にすべき代表例

- WORK_ROOT が解決不能
- assigned Pxx が一意でない
- Gate / Package / Trial が不明
- wrong branch
- Gate contract に実質的 unresolved blocker がある
- required dependency completion evidence がない
- prompt が Coding Agent information isolation を破る

#### 1.5.2. 原則 WARN / INFO にすべき代表例

- package status literal の差異
- traceability 用 SHA の単純な差異
- repository identity を誤らせない remote alias 差異
- explanatory placeholder
- optional metadata 欠落
- cosmetic naming mismatch

判断基準:

> これは誤ったコードを書くこと、または誤った対象を検証することを具体的に防ぐために Hard Fail である必要があるか？

No なら WARN / INFO を優先する。

#### 1.5.3. Metadata parser — format tolerance / semantic strictness

preflightはworkflow metadataの**意味**を検査し、Markdown decoration自体をexecution contractにしてはならない。

最低限、以下は同値として解釈する。

```text
**Depends on:** G02 PASS
Depends on: G02 PASS
- Depends on: G02 PASS
```

同じ原則を、意味が一意な以下のmetadataへ適用する。

```text
Contract status
Verification contract status
Self-containment
Information isolation
Reporting contract
Gate
Package
Depends on
Status at issuance
```

境界は次のとおり。

| Case | Severity | Reason |
|---|---|---|
| bold / bullet / cosmetic decoration差 | `INFO` または無通知 | 意味不変 |
| required fieldは存在し値も一意に解釈可能 | PASS | semantic requirement成立 |
| required field欠落 | `FAIL` | execution authority不足 |
| required fieldが空 | `FAIL` | execution authority不足 |
| dependency valueがworkflow grammarとして解釈不能 | `FAIL` | semantic guessing禁止 |
| required dependency evidenceが不存在 | `FAIL` | 未依存実行防止 |

```text
format tolerance   = YES
semantic guessing  = NO
```

共通parserは `40_operator_workflows/tools/workflow_metadata.py` を使用する。個別preflightで `bold_field()` のような特定Markdown装飾専用parserを再実装しない。

なお、dependency grammarの完全形はEnhancement instanceのstatic dependency contractとrepository artifactsをauthorityとして解決する。protocol側で `G01/G02/P01/P02` のようなinstance値のallow-listをhard-codeしない。

---

## 2. 実行主体と参照範囲

### 2.1. Human/operator

Human/operator はroutingを実行するが、routing semanticsのauthorityはGate 06 / 07 / canonical evidenceに置く。

主な仕事:

- runtime identity の指定
- Architecture / Design blocker の解消
- Gate 06 / 07 freeze
- 次 Pxx の選択
- preflight 確認
- Coding / Candidate Assembly / Test Agent 起動
- Gate PASS 後の次 Gate / Enhancement completion 判定
- formal FAIL / amendment の分岐判断

### 2.2. Work Package Coding Agent

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

### 2.3. Single Execution Coding Agent

Work Packageを持たないGateで、Gate全体を1 execution unitとして扱う場合に使用する。

具体的な実行契約・成果物・verification handoffは各workflow instanceのsingle-execution contractに従う。

Execution modeはGate 06 `Execution mode`から一意に決定する。prompt file、Gate local README、P00の存在をmode enablementの根拠にしない。modeが一意に決まらない場合は実行を開始しない。

### 2.4. Candidate Assembly Agent

Phase B1（Work Package mode）で全 required Pxx 完了後に Gate-level candidate を組み立てる。

### 2.5. Independent Verification Test Agent

Work Package mode / Single Execution modeのいずれでも、Gate-level formal verificationのAcceptance authorityは frozen Gate 07。

Coding Agentのimplementation contractをAcceptance Criteria補完に使わない。

---

## 3. Phase A — Gate Entry Readiness

**主担当:** Human/operator

**目的:** 対象Gateのcanonical implementation / verification contractとupstream dependencyを解決し、選択されたexecution modeを安全に開始できる状態にする。

**原則:** Phase Aの通常read-setは `Gate 06 + Gate 07 + 06が宣言するupstream 999 evidence` に限定する。Gate local README / P00 / planning artifacts / architecture artifactsを通常read dependencyにしない。

### 3.0. Phase A クイックリファレンス

通常のGate開始では、まずこの表だけを上から順に確認する。詳細な理由・例外・authorityの説明が必要な場合だけ、対応するA1〜A5本文を読む。

| Step | 最初に見るartifact / field | 進行可能条件 | 条件を満たさない場合 | 次 |
|---|---|---|---|---|
| A1 | current Gateのcanonical `06` | exactly one / `Gate`一致 / `Contract status: FROZEN` / routing metadata解釈可能 | `BLOCKED`。06を一意化・freeze・修正する | A2 |
| A2 | `06` の `Depends on` | `NONE`、または宣言された各upstream Gateのlatest canonical `999`が`PASS` | current Gateを開始しない。missing / non-PASS / ambiguityを解消する | A3 |
| A3 | current Gateのcanonical `07` | exactly one / `Verification contract status: FROZEN` | `BLOCKED`。Acceptance contractを確定する | A4 |
| A4 | `06.Execution mode` / `06.Required packages`、WORK_PACKAGEならrequired Pxx | mode/package contractが整合し、required Pxxを一意に解決可能 | `BLOCKED`。routing contractまたはPxxを修正する | A5 |
| A5 | mechanical preflight | `OVERALL: READY_FOR_AGENT_EXECUTION` | `OVERALL: BLOCKED`なら実行開始しない | Phase B1 / B2 |

最短経路:

```text
A1: 06 exactly one + FROZEN
    ↓
A2: 06.Depends on -> upstream canonical 999 PASS
    ↓
A3: 07 exactly one + FROZEN
    ↓
A4: 06.Execution mode / Required packages / required Pxx整合
    ↓
A5: mechanical preflight PASS
    ↓
WORK_PACKAGE -> Phase B1
SINGLE_EXECUTION -> Phase B2
```

Phase Aでは、Gate local README / P00 / Architecture Reviewの存在を通常のexecution authorityとして要求しない。06が未freezeの場合に限り、06本文に明示されたauthoring inputへ戻る。

### 3.1. A1 — Gate 06を解決する

#### 3.1.0. A1クイックリファレンス

| 項目 | 見る場所 / 値 | Operator action |
|---|---|---|
| 対象artifact | `10_enhance_instruction/<GATE_ID>/` のcanonical Gate 06 | Gate-level `06`をexactly oneへ解決する。Pxxの`06_<GATE>_<Pxx>_*.md`はここではGate 06として数えない |
| resolver count | `1` | 続行 |
| resolver count | `0` または `2+` | **BLOCKED**。Gate 06を作成 / 重複解消してから再開 |
| `Gate` | runtime `GATE_ID` と一致 | 続行。不一致なら**BLOCKED** |
| `Contract status` | `FROZEN` | 続行。その他は実装開始せず、06に明示されたfreeze input / open itemだけを解決 |
| `Depends on` | fieldが存在しworkflow grammarで解釈可能 | 値の成立確認はA2で行う。欠落 / 空 / 解釈不能なら**BLOCKED** |
| `Execution mode` | `SINGLE_EXECUTION` または `WORK_PACKAGE` | mode/package整合の詳細確認はA4で行う。その他は**BLOCKED** |
| `Required packages` | `NONE` または `Pxx[, Pyy...]` | mode/package整合の詳細確認はA4で行う。欠落 / 空 / grammar不正は**BLOCKED** |
| A1正常終了 | 上記をすべて満たす | **A2へ進む** |

```text
Gate 06 exactly one?
    ├─ No  -> BLOCKED
    └─ Yes
         ↓
Gate == GATE_ID?
    ├─ No  -> BLOCKED
    └─ Yes
         ↓
Contract status == FROZEN?
    ├─ No  -> 06明示のfreeze input / open itemを解決
    └─ Yes -> routing metadata確認 -> A2
```

`10_enhance_instruction/<GATE_ID>/` からcanonical 06をexactly oneへ解決する。

必須metadata:

```text
Gate
Contract status
Depends on
Execution mode
Required packages
```

進行条件:

- `Gate == GATE_ID`
- `Contract status == FROZEN`
- `Depends on`が存在しworkflow grammarで解釈可能
- `Execution mode`が一意
- `Required packages`が解釈可能

06がFROZENでない場合だけ、06本文に明示されたfreeze input / open itemを解決する。Planning / Design tree全体を毎回探索しない。Architecture Reviewはこのauthoring過程で必要な場合だけ使用する。

A1ではdependency evidenceやrequired Pxx completionを先回りして検証しない。`Depends on`の成立確認はA2、mode/package routingの整合確認はA4、実行時dependency evidenceの最終機械判定はA5で行う。

### 3.2. A2 — Gate dependencyをcanonical 999から検証する

#### 3.2.0. A2クイックリファレンス

| `06.Depends on` | 追加で見るartifact | 判定 | Operator action |
|---|---|---|---|
| `NONE` | なし | dependency satisfied | **A3へ進む** |
| `Gxx PASS` | upstream `Gxx`のlatest canonical `999_gate_decision` | `Gate decision: PASS` | dependency satisfied。**A3へ進む** |
| 複数の`Gxx PASS` | 各upstream Gateのlatest canonical `999_gate_decision` | **すべて**`PASS` | dependency satisfied。**A3へ進む** |
| `Gxx PASS` | canonical 999 missing / latest resolver ambiguous | 判定不能 | **BLOCKED**。current Gateを開始しない |
| `Gxx PASS` | latest canonical 999 = `FAIL` | dependency未成立 | current Gateを開始しない。upstream FAIL routeを優先 |
| `Gxx PASS` | latest canonical 999 = `BLOCKED` | dependency未成立 | current Gateを開始しない。upstream blockerを解消 |
| grammar不正 / 空 / fieldなし | 06自身 | semantic authority不足 | **BLOCKED**。推測でdependencyを補完しない |

```text
06.Depends on
    │
    ├─ NONE
    │    -> A3
    │
    └─ Gxx PASS [, Gyy PASS ...]
          ↓
       各upstream latest canonical 999
          │
          ├─ all PASS -> A3
          └─ missing / ambiguous / FAIL / BLOCKED -> STOP / BLOCKED
```

06 `Depends on` が `NONE` ならGate dependency checkは終了する。

`Gxx PASS` が宣言されている場合、そのGateのlatest canonical `999_gate_decision`を一意に解決し、`Gate decision: PASS`であることを確認する。複数dependencyが宣言されている場合はすべて満たす必要がある。

Gate dependencyの成立可否をREADME、state sheet、P00、status literalから推測しない。`999_gate_decision`以外のartifactにPASS相当の記述があってもdependency evidenceへ昇格させない。

### 3.3. A3 — Gate 07を解決する

#### 3.3.0. A3クイックリファレンス

| 項目 | 見る場所 / 値 | Operator action |
|---|---|---|
| 対象artifact | `10_enhance_instruction/<GATE_ID>/` のcanonical Gate 07 | exactly oneへ解決 |
| resolver count | `1` | 続行 |
| resolver count | `0` または `2+` | **BLOCKED**。07を作成 / 重複解消 |
| `Verification contract status` | `FROZEN` | 続行 |
| `Verification contract status` | `FROZEN`以外 / 欠落 / 空 | **BLOCKED**。Acceptance contractを確定し、Codingを開始しない |
| Acceptance authority | frozen Gate 07 | Test Item / ACを06から補完しない |
| A3正常終了 | 07 exactly one + FROZEN | **A4へ進む** |

canonical 07をexactly oneへ解決し、`Verification contract status: FROZEN`を確認する。

07はAcceptance Criteria authorityであり、06のimplementation semanticsと役割を混同しない。07にacceptance semanticsの未確定事項がある場合、実装を先に進めて後から実装へ合わせて07を書き換えない。

### 3.4. A4 — Execution mode固有contractを検証する

#### 3.4.0. A4クイックリファレンス

まずGate 06のrouting metadataだけでmodeを決める。

| `06.Execution mode` | `06.Required packages` | 必須確認 | Operator action |
|---|---|---|---|
| `SINGLE_EXECUTION` | `NONE` | single-execution routeが一意に解決可能 | 正常なら**A5へ** |
| `SINGLE_EXECUTION` | Pxxあり | mode/package矛盾 | **BLOCKED**。06を修正 |
| `WORK_PACKAGE` | Pxx 1件以上 | listed Pxxが各ID exactly one存在 | 正常ならPxx metadata確認後**A5へ** |
| `WORK_PACKAGE` | `NONE` | mode/package矛盾 | **BLOCKED**。06を修正 |
| その他 | 任意 | unsupported mode | **BLOCKED**。modeを推測しない |

WORK_PACKAGEでは各required Pxxについて最低限次を確認する。

| Pxx field / condition | 正常 | 異常時 |
|---|---|---|
| file resolver | exactly one | **BLOCKED** |
| `Self-containment` | `MUST` | **BLOCKED** |
| `Information isolation` | `MUST` | **BLOCKED** |
| `Depends on` | 存在しworkflow grammarで解釈可能 | **BLOCKED** |
| P00 | **参照不要** | missingでもそれだけではblockしない |
| Gate local README | **参照不要** | missing/staleでもそれだけではblockしない |

`SINGLE_EXECUTION`:

- `Required packages: NONE`
- single-execution routeが一意に解決可能

`WORK_PACKAGE`:

- `Required packages`に1件以上のPxxがある
- required Pxx fileが各IDについてexactly one存在する
- 各Pxxは`Self-containment: MUST` / `Information isolation: MUST`
- package dependencyは各Pxx `Depends on`から解決する
- P00の有無はreadiness blocking conditionにしない

Coding AgentへはGate 06 / 07を読ませず、Enhancement-specific Coding prompt + assigned Pxxだけを渡す。Human/operator / preflightがroutingを解決した結果を、Coding Agentのnormative context拡大で代替しない。

### 3.5. A5 — Mechanical preflight

#### 3.5.0. A5クイックリファレンス

Mechanical preflightは、A1〜A4でHuman/operatorが確認したrouting / authority / dependencyをrepository artifactから再解決し、誤対象実行を防ぐ最後のblocking checkである。

**WORK_PACKAGE:**

```bash
python3 <WORK_ROOT>/40_operator_workflows/tools/validate_agent_execution_readiness.py \
  --work-root <WORK_ROOT> \
  --mode package \
  --gate-id <GATE_ID> \
  --package-id <PACKAGE_ID> \
  --trial-no <TRIAL_NO>
```

**SINGLE_EXECUTION:**

```bash
python3 <WORK_ROOT>/40_operator_workflows/tools/validate_agent_execution_readiness.py \
  --work-root <WORK_ROOT> \
  --mode single \
  --gate-id <GATE_ID> \
  --trial-no <TRIAL_NO>
```

| preflight output / condition | 意味 | Operator action |
|---|---|---|
| `OVERALL: READY_FOR_AGENT_EXECUTION` | blocking failureなし | modeに応じてPhase B1 / B2へ |
| `OVERALL: BLOCKED` | authority / target / dependency / isolation等を解決不能 | **実行開始しない**。FAIL evidenceを修正後、同じruntime identityで再実行 |
| `[WARN]`のみ | 非blocking diagnostic | 内容を確認し、原則継続可能 |
| `[INFO]` | trace / diagnostic | 継続可能 |
| Gate local README missing/stale | runtime authorityではない | それ単独ではHard FAILにしない |
| P00 missing | runtime authorityではない | それ単独ではHard FAILにしない |
| Architecture Review artifact missing | normal runtime authorityではない | それ単独ではHard FAILにしない |
| Markdown bold / bullet等のcosmetic差 | semantic fieldが一意なら意味不変 | それ単独ではHard FAILにしない |

```text
preflight
    ├─ BLOCKED -> STOP -> blocker修正 -> preflight再実行
    └─ READY_FOR_AGENT_EXECUTION
          ├─ 06.Execution mode = WORK_PACKAGE     -> Phase B1
          └─ 06.Execution mode = SINGLE_EXECUTION -> Phase B2
```

Hard FAILは、execution target / authority / dependency / isolationを一意に解決できない場合に限定する。

代表例:

- Gate 06 / 07をexactly oneへ解決できない
- Gate 06 / 07がFROZENでない
- Gate 06 `Depends on` / `Execution mode` / `Required packages` がsemantic grammarとして不正
- required upstream canonical 999がmissing / ambiguous / non-PASS
- runtime modeとGate 06 `Execution mode`が矛盾
- WORK_PACKAGEでassigned Pxxを一意に解決できない
- assigned Pxxがself-contained / information-isolatedでない
- Pxx dependency declarationまたはcanonical evidenceが不足
- runtime identity / repository branch / targetが矛盾

Gate local README missing/stale、P00 missing、Architecture Review artifact missing、cosmetic Markdown差だけではHard FAILにしない。

PASS後、execution modeに応じてPhase Bへ進む。

## 4. Phase B1 — Work Package を実行する: Work Package がある Gate の実装

**目的:** dependency-readyなWork Packageを1本ずつ、assigned Pxxだけをnormative contractとして実装し、不要な探索とworkflow理解コストを抑える。

**作業後にあるべき状態:** 対象Pxxが `PACKAGE_COMPLETE` になり次dependencyのevidenceとして利用可能、または継続不能理由が `PACKAGE_BLOCKED*` として明示される。

### 4.1. Step B1-1 — 次の PACKAGE_ID を決める

**目的:** dependency graph に従って、現在実行候補となる Work Package を一意に選択する。

**作業後にあるべき状態:** 実行対象の `GATE_ID` / `PACKAGE_ID` / `TRIAL_NO` が明確で、preflight に渡す runtime identity が確定している。

Human/operator はGate 06 `Required packages` と各Pxx `Depends on` を見る。Gate local README / P00はruntime dependency graph authorityとして参照しない。

実行可否の最終判定は preflight が evidence から導出する。

### 4.2. Step B1-2 — preflight

**目的:** Coding Agent を起動する前に、誤対象・未成立dependency・未確定Gate contractなど、実作業へ影響する blocker がないことを確認する。

**作業後にあるべき状態:** Hard `FAIL` がなく、`WARN` / `INFO` がある場合も意味を把握したうえで、Coding Agent を安全に開始できる。

基本形:

```bash
python3 <WORK_ROOT>/40_operator_workflows/tools/validate_agent_execution_readiness.py \
  --work-root <WORK_ROOT> \
  --mode package \
  --gate-id <GATE_ID> \
  --package-id <PACKAGE_ID> \
  --trial-no <TRIAL_NO>
```

Mechanical validator:

```text
OVERALL: BLOCKED                    -> Coding Agentを開始しない
OVERALL: READY_FOR_AGENT_EXECUTION  -> semantic operator checkへ進む
```

Semantic operator check:

```text
FAILあり      -> Coding Agentを開始しない
WARN/INFOのみ -> 実行継続可能
```

### 4.3. Step B1-3 — Coding Agent 起動

**目的:** assigned Pxx の self-contained contract に限定して実装と focused verification を行い、不要な仕様探索を避ける。

**作業後にあるべき状態:** assigned scope の実装・局所検証・handoff report 作成までが完了するか、継続不能なら理由が `PACKAGE_BLOCKED*` として明示されている。

```text
下記ファイルを実行せよ

- <WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- PACKAGE_ID=<PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

### 4.4. Step B1-4 — package result 確認

**目的:** Coding Agent の作業結果が assigned Pxx の completion condition を満たし、次のdependency判定に利用できる正式なhandoffになっていることを確認する。

**作業後にあるべき状態:** 正常時は canonical package report が存在し `State: PACKAGE_COMPLETE` であり、scope外変更・未解決blockerがない。

正常完了:

```text
State: PACKAGE_COMPLETE
```

Canonical report:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/packages/
<ENHANCE_SHORT_ID>-<GATE_ID>_<TRIAL_NO>_<PACKAGE_ID>__status.md
```

確認事項:

- assigned scope 完了
- focused verification PASS
- unresolved blocker なし
- scope外変更なし
- package report あり

### 4.5. Step B1-5 — 次 package

**目的:** package status の手動書換えではなく、実際の completion evidence と dependency から次の実行可否を導出し、同じ手順で後続Pxxへ進む。

**作業後にあるべき状態:** 次候補 Pxx に対して preflight を再実行できる。全 required Pxx 完了時は Phase C — Candidate Assembly へ移行できる。Phase CはこのPhase B1固有だが、Phase Dは全execution mode共通である。

次 Pxx document の status を変更しない。

次 Pxx に対して再度 preflight を実行する。

preflight が completion evidence から eligibility を導出する。

---

## 5. Phase B2 — Gate 全体を実行する: Work Package がない Gate の実装

**適用条件:** Gate 06が `Execution mode: SINGLE_EXECUTION` かつ `Required packages: NONE` を一意に宣言する場合のみ使用する。

**目的:** Gate全体を1 execution unitとして実装し、Work Package分割を前提とせずFixed Trial Candidateを確定できるimplementation evidenceを作成する。formal Independent VerificationはこのPhaseでは行わない。

**作業後にあるべき状態:** instance-specific single execution contractで要求された実装・focused/self verification・handoffが完了し、Fixed Trial Candidate identityがfreezeされ `READY_FOR_TEST` としてPhase Dへ渡せる。

### 5.1. Phase B2 最低限クイックチェック

| 確認対象 | 最低限見る場所 | 進行可能な状態 |
|---|---|---|
| execution mode | Gate 06 `Execution mode` | `SINGLE_EXECUTION` が一意に解決できる |
| Gate 06 / 07 | role-based resolverでexactly oneへ解決 | 両contractがFROZEN authorityとして利用可能 |
| single execution prompt | `40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md` | Enhancement-specific instanceとして解決済み |
| candidate finalization contract | instance-specific single execution contract | Fixed Trial Candidate identity / `READY_FOR_TEST` handoffが明示されている |

### 5.2. Step B2-1 — Gate-wide single execution contract を確認する

**目的:** Work Packageを使わないGateで、実装範囲・完了条件・candidate finalization・verification handoffを1つのcontractとして確定する。

**作業後にあるべき状態:** Human/operatorが、どのpromptを起動し、何をもってGate-wide implementation完了およびFixed Trial Candidate確定とするかを一意に判断できる。

contractにcandidate identity / freeze rule / Phase D handoffが不足している場合は `BLOCKED_CONTRACT_AMBIGUITY` 相当として開始しない。

### 5.3. Step B2-2 — Single Execution Coding Agent を起動する

Human/operatorはEnhancement-specific entry promptへ runtime identity を渡す。

Template上の基本形:

```text
下記ファイルを実行せよ

- <WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_01_single_execution_coding_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

### 5.4. Step B2-3 — Gate-wide implementation result を確認する

**目的:** single execution contractで要求されたimplementation scope、focused/self verification、handoff evidenceが揃っていることを確認する。

**作業後にあるべき状態:** implementation blockerがなく、candidate finalizationへ進める。

### 5.5. Step B2-4 — Fixed Trial Candidate を確定する

**目的:** Single Executionの実装結果からGate boundaryのFixed Trial Candidate identityをfreezeし、Independent Verification対象を一意にする。

**作業後にあるべき状態:** candidate identityがcanonical implementation completion evidenceに記録され、`Candidate state: READY_FOR_TEST` としてPhase Dへ渡せる。

```text
Single Execution implementation complete
    ↓
Gate-boundary candidate identity freeze
    ↓
Candidate state: READY_FOR_TEST
    ↓
Phase D — Independent Verification
```

Candidate finalizationをCoding Agent自身のGate PASS判定にしてはならない。Gate PASS authorityはPhase D/E側に残す。

---

## 6. Phase C — Candidate Assembly: 各Gateにおける複数 Work Package 実装完了時の結果の統合

**適用条件:** Phase B1（Work Package mode）を使用したGateのみ。Phase B2ではPhase Cを実施せず、Phase B2内でFixed Trial Candidateを確定する。

**目的:** 各 Work Package の実装結果をGate単位で統合し、Independent Verificationへ渡す1つのFixed Trial Candidateを確定する。

**作業後にあるべき状態:** required Pxx がすべて完了し、Gate-wide integration / regression self-checkに重大なblockerがなく、Fixed Trial Candidateがfreezeされ `READY_FOR_TEST` になっている。

全 required Pxx が `PACKAGE_COMPLETE` になったら実行する。

### 6.1. Candidate Assembly Agent 実行プロンプト

Human/operatorは次の形式で実行する。

```text
下記ファイルを実行せよ

- <WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

`GATE_ID` / `TRIAL_NO` は実行対象に置換する。

### 6.2. Candidate Assembly で確認すること

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
<ENHANCE_ID>_<GATE_ID>_Trial<TRIAL_NO>_implementation_completion_report.md

20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
<ENHANCE_ID>_<GATE_ID>_Trial<TRIAL_NO>_implementation_report_detail.md
```

Fixed Trial Candidate SHA を package 単位で freeze しない。

---

## 7. Phase D — Independent Verification: Gate Candidate の独立検証

**適用条件:** execution modeにかかわらず、Gate boundaryで `READY_FOR_TEST` のFixed Trial Candidateが確定したすべてのGate。Work Package modeではPhase C、Single Execution modeではPhase B2-4から到達する。

**目的:** Coding側の実装判断から独立して、frozen Gate 07をAcceptance authorityとしてFixed Trial Candidateを検証する。

**作業後にあるべき状態:** Gate 07で要求されたTest Itemのevidenceが揃い、Product判定可能な場合はPASS/FAIL、判定不能ならBLOCKEDとして999 Gate Decisionへ進める。

`READY_FOR_TEST` 後に、execution modeにかかわらず Test Agent を実行する。

### 7.1. Independent Verification Agent 実行プロンプト

Human/operatorは次の形式で実行する。

```text
下記ファイルを実行せよ

- <WORK_ROOT>/40_operator_workflows/agent_entry_prompts/
    - 30_independent_verification_01_test_agent_prompt.md

Runtime identityは以下の通り

- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>

プロンプトの際の基本言語は日本語とする
```

`GATE_ID` / `TRIAL_NO` は実行対象に置換する。

### 7.2. Independent Verification の実行内容

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

## 8. Phase E — 999 Gate Decision: Gate の最終判定

**目的:** Gate-level verification evidenceを基に、Gateの正式な最終判定をcanonical artifactとして確定する。

**作業後にあるべき状態:** `999_gate_decision` に `PASS / FAIL / BLOCKED` のいずれかと根拠が記録され、次のoperator actionが一意に決まる。

### 8.1. Phase E 最低限クイックチェック

Human/operatorは、詳細なtest reportを最初から読み直す前に最低限次を確認する。

| 最低限見る場所 | 確認する箇所 | 期待する状態 / 判断 |
|---|---|---|
| Phase B1の場合: `20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/..._implementation_completion_report.md` | `Candidate state`、Fixed Trial Candidate identity | `READY_FOR_TEST` とcandidate identityが確定済み |
| Phase D output: `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/` | Gate 07でrequiredなTest Item report | execution modeにかかわらずrequired Test Itemのevidenceが揃っている |
| Phase B2の場合: Gate-wide implementation completion evidence | `Candidate state`、Fixed Trial Candidate identity | `READY_FOR_TEST` とcandidate identityが確定済み |
| `30_test_report/<GATE_ID>/Trial<TRIAL_NO>/<ENHANCE_ID>_<GATE_ID>_Trial<TRIAL_NO>_999_gate_decision.md` | `Gate decision` | `PASS` / `FAIL` / `BLOCKED` のいずれかが明示されている |
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

### 8.2. PASS

```text
Gate decision: PASS
```

なら Gate は正式 PASS。

次に Phase F へ進む。

### 8.3. FAIL

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

### 8.4. BLOCKED

identity / environment / harness / prerequisite / verification contract ambiguity 等で Product 判定不能。

`BLOCKED` を Product FAIL と解釈しない。

---

## 9. Phase F — Gate Terminal Routing

**目的:** current Gateのcanonical final decisionだけから、このGateのterminal routeを確定する。

**read-set:** current Gateのlatest canonical `999_gate_decision`のみ。

**write-set:** なし。

Phase Fでは以下を読まない。

- next Gate local README
- next Gate 06 / 07
- P00 / Pxx
- package execution reports
- Implementation Completion Report
- Architecture Review
- planning / design / traceability artifacts
- preflight result

これらはcurrent Gate final decisionのauthorityではなく、next Gate readinessはNext Gate Phase Aの責務である。

### 9.0. Gate Terminal Routing クイックリファレンス

Phase Fはこの表だけで通常のterminal routingを完了できる。次Gateの準備情報を先読みしない。

| 項目 | 見る場所 / 値 | Operator action |
|---|---|---|
| 読むartifact | current Gate / current Trialのcanonical `999_gate_decision` | exactly oneへ解決する |
| resolver count | `1` | `Gate decision`を読む |
| resolver count | `0` または `2+` | **BLOCKED**。terminal routeを推測しない |
| `Gate decision: PASS` | canonical 999 | current Gateを`COMPLETE`として扱う。downstream Gateを開始するなら**そのGateのPhase Aへ** |
| `Gate decision: FAIL` | canonical 999 | formal FAIL remediation routeへ |
| `Gate decision: BLOCKED` | canonical 999 | blocker resolutionへ。Product FAILへ読み替えない |
| その他 / field欠落 / 空 | canonical 999 | **BLOCKED**。canonical decisionを修正 / 確定する |
| Next Gate 06 / 07 | **Phase Fでは見ない** | Next Gate Phase Aで解決する |
| Next Gate readiness | **Phase Fでは判定しない** | Next Gate Phase Aへ責務移管 |
| state / transition / promotion artifact | **作成しない** | canonical 999自体をterminal authorityとする |

```text
current canonical 999
    │
    ├─ PASS
    │    -> current Gate COMPLETE
    │    -> downstream Gateを開始するなら、そのGateのPhase A
    │
    ├─ FAIL
    │    -> Formal FAIL Remediation
    │
    └─ BLOCKED
         -> Blocker Resolution
```

Phase Fの判定に必要なのはcurrent canonical 999だけである。Enhancement completion判定が必要な場合も、Phase Fへnext-Gate contract readを追加せず、Enhancement orchestration側でrequired Gate集合のcanonical 999を評価する。

### 9.1. F1 — canonical 999を解決する

current Gate / current Trialのcanonical `999_gate_decision`をexactly oneへ解決する。

0件または複数の場合はterminal routeを推測せず`BLOCKED`として扱う。README、test report本文、implementation report等から`PASS / FAIL / BLOCKED`を再構成して999の代替authorityにしない。

### 9.2. F2 — terminal route

```text
Gate decision = PASS
    -> current Gate COMPLETE
    -> downstream Gateを開始する場合、そのGateのPhase Aへ入る
    -> Phase F自身はnext Gate readinessを判定しない

Gate decision = FAIL
    -> formal FAIL remediation route
    -> 08 / Rxx等のexception contractへ遷移

Gate decision = BLOCKED
    -> blocker resolution
    -> product FAILへ読み替えない
```

### 9.3. F3 — Enhancement completion

current GateがPASSしたことだけではEnhancement completionを自動推測しない。

Enhancement-level required Gate集合がすべてPASSしたかの判定はEnhancement orchestration responsibilityとし、個々のGate Phase Fへnext-Gate contract readを持ち込まない。

Phase Fは新しいstate file / transition report / promotion recordを作成しない。canonical `999_gate_decision`自体がcurrent Gate terminal authorityである。

## 10. Cross-Phase Exception Handling — BLOCKED / environment 問題

Phase A〜F の途中で発生する `BLOCKED` は、独立した工程ではなく、各 Phase を横断する例外状態として扱う。

原則として、`BLOCKED` は formal Product FAIL と同義ではない。原因を分類し、blocker を解消したうえで、同じ Phase / Gate / Package / Trial の適切な地点から再開する。

### 10.1. `BLOCKED_PRECHECK`

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

### 10.2. `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`

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

### 10.3. `PACKAGE_BLOCKED`

runtime / implementation / environment 等で completion 不能。

これは formal Gate FAIL ではない。

原因を分類する。

```text
Product/code
Contract
Dependency
Environment/harness
```

### 10.4. Browser E2E / environment blocker

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

### 10.5. Trial を増やすか

`PACKAGE_BLOCKED` / `BLOCKED_PRECHECK` だけでは自動的に Trial を増やさない。

Formal Gate FAIL 後の approved remediation では next Trial を使う。

---

## 11. Artifact authority map

### 11.1. Workflow state authority quick reference

Workflow の進行状態は集約sheetへ転記せず、次のcanonical artifactから直接導出する。

| 判定対象 | Authority |
|---|---|
| Pxx dependency | upstream package の `package execution status report` |
| Gate dependency | upstream Gate の canonical `999_gate_decision` |
| Gate readiness | Gate `06` + Gate `07` + 06-declared upstream canonical evidence + blocking preflightなし |
| Candidate readiness | Gate の `implementation completion report` |

この4系統を別のmutable state fileへ再集約しない。

### 11.2. Agent別 artifact authority

| Artifact | Human/operator | Coding Agent | Candidate Assembly | Test Agent |
|---|---:|---:|---:|---:|
| `00_enhance_background/*` | Yes | No | Reference | No |
| Gate `06` | Yes | No | **Required package / routing authority** | No acceptance use |
| Gate `07` | Yes | No | Reference | **Authority** |
| `P00` | Optional | No | authoring rationale / audit only | No |
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

## 12. Operator prompt / script quick reference

| Goal | Entry point |
|---|---|
| Architecture / source discovery（06 freeze前に必要な場合のみ） | `40_operator_workflows/architecture_review/01_architecture_discovery_prompt.md` |
| Preflight | `40_operator_workflows/tools/validate_agent_execution_readiness.py` |
| Work Package Coding | `40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md` |
| Gate-wide Single Execution（Work Packageなし / instanceで有効な場合） | `40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md` |
| Candidate Assembly | `40_operator_workflows/agent_entry_prompts/20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md` |
| Independent Verification | `40_operator_workflows/agent_entry_prompts/30_independent_verification_01_test_agent_prompt.md` |
| Formal FAIL remediation | `40_operator_workflows/agent_entry_prompts/40_fail_remediation_01_fail_rework_coding_agent_prompt.md` |
| Gate orchestration | `40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md` |

Manual mode では Human/operator が各段階を明示的に起動する。

Gate Orchestrator を使っても Coding Agent isolation / 999 authority は変更しない。

---

## 13. やってはいけないこと

### 13.1. Package status を workflow cursor にする

```text
DRAFT_NOT_FROZEN
    ↓ manual edit
READY_TO_EXECUTE
```

で次 package を unlock しない。

### 13.2. Coding Agent に workflow 全体を探索させる

Pxx が不足しているなら Design側を修正する。

### 13.3. `PACKAGE_COMPLETE` を Gate PASS とみなす

Gate PASS は 999 のみ。

### 13.4. Work Package ごとに Gate級 SHA / acceptance を要求する

Fixed Trial Candidate は Gate単位に固定する。Work Package modeではCandidate Assembly、Single Execution modeではPhase B2のcandidate finalizationで固定する。

### 13.5. SHA / placeholder / naming の表記差だけで止める

実害がなければ WARN / INFO を優先する。

### 13.6. Gate 06 / 07 の未freezeを status 問題として無視する

unresolved semantic / acceptance blocker があるなら実質的 blocker。

### 13.7. environment BLOCKED を Product FAIL にする

Product violation が verified された場合だけ FAIL。

---

## 14. End-to-End operator flow

```text
[0] Planning / Requirements / Design
        本書のスコープ外
        ↓
[1] Phase A: Gate 06 / 07 + 06-declared dependency evidenceを解決
        ↓
    06.Execution modeを解決
        ├─ WORK_PACKAGE
        │    ↓
        │  [2A] Phase B1: Pxx preflight → Coding → package completion evidence
        │    ↓
        │  dependency-ready Pxxを順次実行
        │    ↓
        │  all required Pxx complete
        │    ↓
        │  [3] Phase C: Candidate Assembly
        │    ↓
        │  READY_FOR_TEST + Fixed Trial Candidate
        │
        └─ SINGLE_EXECUTION
             ↓
           [2B] Phase B2: Gate-wide implementation
             ↓
           Fixed Trial Candidate finalization
             ↓
           READY_FOR_TEST

             [共通]
                ↓
           [4] Phase D: Independent Verification
                ↓
           [5] Phase E: 999 Gate Decision

[5] Phase E: 999 Gate Decision
     ├─ PASS
     │    ↓
     │  [6] Phase F: current canonical 999だけでterminal route
     │    ↓
     │  current Gate COMPLETE
     │    ↓
     │  downstream Gateを開始する場合は、そのGateのPhase Aへ
     │  （Next Gate readiness / freeze / preflightはPhase Fでは読まない）
     │
     ├─ FAIL
     │    ↓
     │  approved remediation / next Trial
     │
     └─ BLOCKED
          ↓
        prerequisite / environment / contract blocker解消
```

Phase C は Work Package mode固有である。Phase D は execution mode共通のGate-level Independent Verificationである。

## 15. Operator checklist

### 15.1. Gate開始前

- [ ] Gate 06がexactly one、`Contract status: FROZEN`
- [ ] Gate 06 `Depends on` のupstream canonical 999 evidenceがPASS
- [ ] Gate 07がexactly one、`Verification contract status: FROZEN`
- [ ] Gate 06 `Execution mode` / `Required packages` が整合
- [ ] WORK_PACKAGEならrequired Pxxが存在し、assigned Pxxがself-contained / information-isolated
- [ ] Pxx dependencyが明示されcanonical evidenceで解決可能
- [ ] Gate local README / P00 / Architecture Review artifactの有無をruntime blocking条件にしていない
- [ ] current branch 正常
- [ ] preflight FAILなし

Package-level `Status at issuance` の文字列一致は本質条件ではない。

### 15.2. Work Package完了後

- [ ] assigned scope のみ変更
- [ ] focused verification PASS
- [ ] unresolved blocker なし
- [ ] canonical package status report 作成
- [ ] `State: PACKAGE_COMPLETE`
- [ ] 次 Pxx status を手動変更していない
- [ ] 次 Pxx は preflight で再判定

### 15.3. Work PackageなしのGate-wide execution完了後

- [ ] single execution modeがinstanceで正式に有効
- [ ] Gate-wide implementation scope完了
- [ ] Fixed Trial Candidate identityをGate boundaryでfreeze
- [ ] `Candidate state: READY_FOR_TEST` のcanonical handoffが存在
- [ ] Phase DのIndependent Verificationへ渡した
- [ ] execution modeはGate 06 `Execution mode`から一意に解決済み

### 15.4. Gate PASS後

- [ ] current canonical 999 = PASS
- [ ] Phase Fで新しいstate / transition / promotion artifactを書いていない
- [ ] Phase FでNext Gate README / 06 / 07 / preflightを読んでいない
- [ ] downstream Gateを開始する場合、そのGateのPhase Aへ入る
- [ ] Next Gate Phase Aで06-declared dependency evidence / 06 / 07 / preflightを解決する
- [ ] Enhancement completionはEnhancement-level required Gate集合のcanonical 999からorchestration responsibilityとして判定する

---

## 16. README 本文との役割分担

### 16.1. Root `README.md`

- workflow instance 概要
- Gate一覧
- Quick Start
- 最重要 execution principles
- 本Appendixへのリンク

### 16.2. `README_Appendix_HowToUse.md`

- end-to-end operator procedure
- Gate freeze / transition
- Work Package execution
- BLOCKED / FAIL handling
- Candidate Assembly
- Independent Verification
- Gate PASS後の次Gate遷移 / Enhancement completion判定
- status / evidence semantics

### 16.3. Subdirectory README

各 layer 固有の詳細 contract / canonical path / artifact semantics。

本Appendixは各READMEを置き換えず、**「どの順番で何を見るか」**を説明する。

Root READMEと重複する最小概念は、実行中に参照するクイックリファレンスとしてINTRODUCTIONへ意図的に残す。詳細仕様のauthorityは各contract / artifact側に置く。

---

## 17. Workflow Template 次版への反映

次版では本Appendix相当を標準生成対象にすることを推奨する。

Enhancement instantiation時に解決するidentity:

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
WORK_ROOT
WORK_DIR_NAME
BRANCH_NAME
REMOTE_NAME
```

Execution時にHuman/operatorが指定するruntime identity:

```text
GATE_ID
PACKAGE_ID                 # Work Package modeのみ
TRIAL_NO
REMEDIATION_PACKAGE_ID     # remediation時のみ
AMENDMENT_ID               # amendment時のみ
```

`WORK_ROOT` は `docs/wiki/develop_memo/_work/` 配下のdirectory名ではなく、Enhancement work rootへのpathそのものとして扱う。Gate 06 / 07のfilenameは未定義の `<SYSTEM_ID>` を前提に組み立てず、role-based resolverから一意に解決する。

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
Gate readiness = Gate 06 + Gate 07 + 06-declared upstream canonical evidence + blocking preflightなし
Candidate readiness = implementation completion report
Phase F read-set = canonical 999 only
Phase F write-set = none
Gate local README = Human index only
P00 = optional authoring/audit only
Work Package != Gate quality boundary
Execution mode = Gate 06 `Execution mode`; prompt / README / P00 existence alone is not authority
Independent Verification = common Gate-level phase for all execution modes
```

本書の成功条件は、Human/operator が workflow 内部protocolを推測せず、

> **今どの段階で、次にどの prompt / script を実行し、何を確認すべきか**

を README 体系だけから判断できることである。
