# README Appendix — How to Use the Agentic Enhancement Workflow

> Document class: Operator How-To / Runbook Appendix  
> Audience: Human operator / workflow maintainer  
> Scope: planning 完了後から Work Package 実装、Gate verification、次 Gate への移行、Enhancement 完了まで  
> Initial reference: ENH-E7 / workflow v0.07  
> Authority: 各 Enhancement instance の frozen contract / assigned Pxx / Gate 07 が本書より優先する

---

## 0. この文書の目的

Root `README.md` の Quick HowToUse は、1 Work Package を開始する入口だけを説明する。

本書は Human/operator が、workflow 全体について次を迷わず判断できるようにする。

```text
今どの段階か
    ↓
次に何を確認するか
    ↓
どの script / prompt を実行するか
    ↓
PASS / BLOCKED / FAIL をどう解釈するか
    ↓
次の工程へどう進むか
```

基本フロー:

```text
Planning / Design
    ↓
Gate contract freeze
    ↓
Work Package execution
    ↓
Candidate Assembly
    ↓
Independent Verification
    ↓
999 Gate Decision
    ↓
Current State promotion
    ↓
Next Gate / Enhancement completion
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

---

## 1. 最初に理解するべき状態と単位

### 1.1. Gate

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

### 1.2. Work Package

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

### 1.3. Trial

Gate candidate の verification attempt。

Formal FAIL remediation で次 Trial へ進む。

`BLOCKED_PRECHECK` や `PACKAGE_BLOCKED` は、それだけで formal Gate FAIL を意味しない。

### 1.4. 状態値の意味

#### 1.4.1. Package-level `Status at issuance`

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

#### 1.4.2. Gate 06 / 07 readiness

Gate 06 / 07 の未freezeは package-level status と同じ意味ではない。

未freezeの理由が、

- implementation semantics 未確定
- Acceptance Criteria 未確定
- unresolved Architecture / Design decision

である場合、Gate contract はまだ execution authority ではないため Coding を開始しない。

重要なのは `FROZEN` という文字列そのものではなく、**設計・acceptance contract が本当に確定していること**である。

#### 1.4.3. `PACKAGE_COMPLETE`

assigned scope + focused verification + package handoff が完了。

```text
PACKAGE_COMPLETE
    != READY_FOR_TEST
    != Gate PASS
```

#### 1.4.4. `READY_FOR_TEST`

Candidate Assembly が Gate-level integration を確認し、Fixed Trial Candidate を freeze した状態。

#### 1.4.5. Gate PASS

最終 authority は canonical `999_gate_decision` のみ。

```text
Gate decision: PASS
```

---

## 2. 誰が何を読むか

### 2.1. Human/operator

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

### 2.3. Candidate Assembly Agent

全 required Pxx 完了後に Gate-level candidate を組み立てる。

### 2.4. Independent Verification Test Agent

Acceptance authority は frozen Gate 07。

Coding Agent Pxx を Acceptance Criteria 補完に使わない。

---

## 3. Preflight の役割

Preflight は、

> Coding Agent が安全かつ迷わず assigned Work Package を開始できるか

を確認する。

Workflow artifact の形式的完全性を証明するものではない。

### 3.1. Result semantics

```text
FAIL
  -> BLOCKED
  -> 実作業リスクがある

WARN
  -> 実行継続可能
  -> 確認価値はあるが非blocking

INFO
  -> 診断・追跡情報
```

### 3.2. Hard Fail にすべき代表例

- WORK_ROOT が解決不能
- assigned Pxx が一意でない
- Gate / Package / Trial が不明
- wrong branch
- Gate contract に実質的 unresolved blocker がある
- required dependency completion evidence がない
- prompt が Coding Agent information isolation を破る

### 3.3. 原則 WARN / INFO にすべき代表例

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

## 4. Phase A — Gate を実行可能にする

Work Package Coding を開始する前に Gate contract を準備する。

### 4.1. Step A1 — upstream prerequisite を確認する

Gate README / P00 / Current State を Human/operator が確認する。

例:

```text
G02 depends on G01 final PASS
```

なら、canonical G01 `999_gate_decision` が `PASS` であることを確認する。

### 4.2. Step A2 — deferred Architecture / Design question を解消する

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

### 4.3. Step A3 — Gate 06 を確定する

少なくとも次を確認する。

- Gate objective / claim
- allowed / prohibited scope
- protected passed-Gate contract
- API / persistence / domain semantic policy
- Work Package decomposition との整合
- unresolved implementation semantic blocker がない

### 4.4. Step A4 — Gate 07 を確定する

少なくとも次を確認する。

- Acceptance Criteria
- Test Item mapping
- candidate identity rule
- protected regression
- Browser E2E obligation
- PASS / FAIL / BLOCKED semantics
- canonical test report / 999 output contract

### 4.5. Step A5 — Pxx self-containment を確認する

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

### 4.6. Step A6 — Gate 06 / 07 を freeze

unresolved semantic blocker がゼロになった時点で freeze する。

**Pxx の `Status at issuance` を `READY_TO_EXECUTE` に変更する必要はない。**

### 4.7. Gate freeze finalization を LLM に依頼する場合

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

## 5. Phase B — Work Package を1本実行する

### 5.1. Step B1 — 次の PACKAGE_ID を決める

Human/operator は Gate README / P00 の dependency graph を見る。

実行可否の最終判定は preflight が evidence から導出する。

### 5.2. Step B2 — preflight

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

### 5.3. Step B3 — Coding Agent 起動

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

### 5.4. Step B4 — package result 確認

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

### 5.5. Step B5 — 次 package

次 Pxx document の status を変更しない。

次 Pxx に対して再度 preflight を実行する。

preflight が completion evidence から eligibility を導出する。

---

## 6. BLOCKED の扱い

### 6.1. `BLOCKED_PRECHECK`

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

### 6.2. `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`

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

### 6.3. `PACKAGE_BLOCKED`

runtime / implementation / environment 等で completion 不能。

これは formal Gate FAIL ではない。

原因を分類する。

```text
Product/code
Contract
Dependency
Environment/harness
```

### 6.4. Trial を増やすか

`PACKAGE_BLOCKED` / `BLOCKED_PRECHECK` だけでは自動的に Trial を増やさない。

Formal Gate FAIL 後の approved remediation では next Trial を使う。

---

## 7. Phase C — Candidate Assembly

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

## 8. Phase D — Independent Verification

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

## 9. Phase E — 999 Gate Decision

### 9.1. PASS

```text
Gate decision: PASS
```

なら Gate は正式 PASS。

次に Current State promotion。

### 9.2. FAIL

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

### 9.3. BLOCKED

identity / environment / harness / prerequisite / verification contract ambiguity 等で Product 判定不能。

`BLOCKED` を Product FAIL と解釈しない。

---

## 10. Phase F — Current State promotion と次 Gate

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

### 10.1. 次 Gate がある場合

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

## 11. Browser E2E / environment blocker

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

## 12. Artifact authority map

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

## 13. Operator prompt / script quick reference

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

## 14. やってはいけないこと

### 14.1. Package status を workflow cursor にする

```text
DRAFT_NOT_FROZEN
    ↓ manual edit
READY_TO_EXECUTE
```

で次 package を unlock しない。

### 14.2. Coding Agent に workflow 全体を探索させる

Pxx が不足しているなら Design側を修正する。

### 14.3. `PACKAGE_COMPLETE` を Gate PASS とみなす

Gate PASS は 999 のみ。

### 14.4. Work Package ごとに Gate級 SHA / acceptance を要求する

Fixed Candidate は Candidate Assembly で Gate単位に固定する。

### 14.5. SHA / placeholder / naming の表記差だけで止める

実害がなければ WARN / INFO を優先する。

### 14.6. Gate 06 / 07 の未freezeを status 問題として無視する

unresolved semantic / acceptance blocker があるなら実質的 blocker。

### 14.7. environment BLOCKED を Product FAIL にする

Product violation が verified された場合だけ FAIL。

---

## 15. End-to-End operator flow

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

## 16. Operator checklist

### 16.1. Gate開始前

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

### 16.2. Work Package完了後

- [ ] assigned scope のみ変更
- [ ] focused verification PASS
- [ ] unresolved blocker なし
- [ ] canonical package status report 作成
- [ ] `State: PACKAGE_COMPLETE`
- [ ] 次 Pxx status を手動変更していない
- [ ] 次 Pxx は preflight で再判定

### 16.3. Gate PASS後

- [ ] canonical 999 = PASS
- [ ] Fixed Trial Candidate SHA 記録
- [ ] Current State promotion
- [ ] protected contract set 更新
- [ ] downstream Gate prerequisite 確認
- [ ] deferred design があれば next Gate freeze を先に実行
- [ ] final Gateなら cross-gate integration / regression の不足確認
- [ ] Enhancement完了後、必要な Canonical Requirements 更新

---

## 17. README 本文との役割分担

### 17.1. Root `README.md`

- workflow instance 概要
- Gate一覧
- Quick Start
- 最重要 execution principles
- 本Appendixへのリンク

### 17.2. `README_Appendix_HowToUse.md`

- end-to-end operator procedure
- Gate freeze / transition
- Work Package execution
- BLOCKED / FAIL handling
- Candidate Assembly
- Independent Verification
- Current State promotion
- status / evidence semantics

### 17.3. Subdirectory README

各 layer 固有の詳細 contract / canonical path / artifact semantics。

本Appendixは各READMEを置き換えず、**「どの順番で何を見るか」**を説明する。

---

## 18. Workflow Template 次版への反映

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
