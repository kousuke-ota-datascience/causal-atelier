# Agentic Enhancement Workflow Template 修正申し送り事項

- 起票元: Ariadne ENH-E6 — Family / Stage Navigation Observable UI Bugfix
- 対象: `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/`
- 作成日: 2026-08-13
- 種別: Workflow / Operator Control / Agent Context Isolation 改善
- 優先度: High
- ENH-E6 product semanticsへの影響: なし

---

## 1. 申し送りの目的

ENH-E6のPlanning〜Coding Agent起動準備で、workflow templateの使い方に関して次の問題が顕在化した。

1. template側の `agent_entry_prompts/` をHumanが直接指定すると、Enhancement identityを一意に解決できない。
2. Work Package Coding Agentへ過剰なworkflow文書を読ませやすい構造・運用になっている。
3. Human向けtraceabilityとCoding Agent向けinformation isolationを混同しやすい。
4. document/template complianceを満たしていても、Agent execution readinessが成立していないケースを検出できない。
5. `agent_entry_prompts/` のEnhancement-specific instantiationが必須であることが、operatorが誤用できない程度には強制されていない。

このため、templateを「文書雛形」だけでなく「実行時control plane」として誤用しにくい形へ修正する必要がある。

---

## 2. ENH-E6で実際に発生した問題

### 2.1. template側operator promptを直接Coding Agentへ指定してしまった

誤ったHuman entry例:

```text
下記文書に記載の指示を実行すること。

- docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

今回の指示は

- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01

である。
```

`G01 / P01 / Trial01` はEnhancement固有identifierではないため、これだけではENH-E6を一意に決定できない。

本来は少なくとも以下のEnhancement-fixed valuesが事前確定している必要がある。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E6
ENHANCE_SHORT_ID=E6
BRANCH_NAME=bugfix/ariadne_mvp_e6
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix
WORK_DIR_NAME=20260813_ENH-E6_family_stage_navigation_bugfix
```

### 2.2. Coding Agentへ07等を参照させる誤りが発生した

一時的にP01からGate 07やPlanning documentを参照可能とする記述を置いてしまった。

これはWork Package Coding Agentのinformation isolationに反する。

Coding Agentのnormative implementation sourceはassigned Pxxのみであるべきで、以下を仕様補完目的で読ませない。

- Gate-level 06
- Gate-level 07
- P00
- 他Pxx
- 00 / 20 / 30 planning/evidence artifacts
- 過去Enhancement
- ADR / issue / external Web

一方でHuman/auditorはPxx ↔ 06 ↔ 07のtraceabilityを追跡できる必要がある。

つまり、

```text
Human traceability != Agent-visible normative context
```

をtemplate上でより強く分離する必要がある。

### 2.3. template compliance PASSとAgent execution readiness PASSを混同した

artifactのheading、placeholder、required section等を検査しても、次の問題は検出できなかった。

- `agent_entry_prompts/` がEnhancement側にinstance化されていない
- Human entryだけではEnhancement identityが解決できない
- Coding Agentが不要なworkflow文書へ到達可能

したがって、document complianceだけではAgent execution可否を判定できない。

---

## 3. 根本原因

### 3.1. Templateの二重の責務が明確に分離されていない

workflow templateには少なくとも次の2責務がある。

1. **Artifact schema**
   - README / 00 / 06 / 07 / P00 / Pxx / 20 / 30等に何を書くか。
2. **Execution protocol**
   - Humanがどのpromptを渡すか。
   - どのvariableをいつ固定するか。
   - Agentがどのdocumentを読めるか。
   - WORK_ROOT等をどう解決するか。
   - Coding Agent / Test Agentのinformation boundaryをどう保持するか。

現状は1が強く、2がoperatorの解釈に依存しやすい。

### 3.2. Presence validationだけでは不足

「存在するENH artifactにplaceholderが残っていない」ことだけを検査しても、template-required artifactそのものがENH側に存在しないケースを検出できない。

最初に次を検査する必要がある。

```text
Required instantiated artifact set
-
Actual enhancement artifact set
```

### 3.3. Syntax validationとsemantic execution validationの混同

以下は別物である。

```text
unresolved {{...}} == 0
```

と

```text
Human entryからEnhancement / Gate / Package / Trialを一意に解決できる
```

後者はexecution resolvability validationとして独立させる必要がある。

---

## 4. Template修正要求

### 4.1. Enhancement-specific `agent_entry_prompts/` のinstance化をMUST化する

root README / operator workflow README / variable conventionsで明示する。

要求:

- template directory上の `agent_entry_prompts/` をAgent executionへ直接使用してはならない。
- Enhancement開始時に、Enhancement work root配下へ `40_operator_workflows/agent_entry_prompts/` をinstance化する。
- Enhancement-fixed variablesはinstance化時に具体値へ展開する。
- 未解決Enhancement-fixed variableが1件でも残る場合はAgent executionを開始しない。

例:

```text
{{WORK_ROOT}}
  /40_operator_workflows/
    agent_entry_prompts/
```

### 4.2. Variableを「Enhancement-fixed」と「Runtime」に明確分離する

#### Enhancement-fixed

例:

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
BRANCH_NAME
REMOTE_NAME
WORK_ROOT
WORK_DIR_NAME
```

これらはEnhancement-specific prompt生成時に確定する。

#### Runtime

例:

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

これらのみHuman operatorが各execution時に指定する。

### 4.3. Work Package Coding Agent promptを「resolver + guardrail」へ縮小する

Coding Agent用operator promptは長いworkflow説明書にせず、次だけに限定する。

1. Enhancement identity
2. Runtime variables
3. Assigned Pxxの解決規則
4. Assigned Pxxのみがnormative implementation contractであること
5. 読んではならないworkflow artifacts
6. source / tests / config / migrationをimplementation substrateとして調査可能であること
7. report/checkpoint出力先
8. BLOCKED / stop rule

Coding Agentにworkflow全体を理解させない。

### 4.4. Human Quick HowToUseはinstance-specific pathを使用する

悪い例:

```text
.../agentic_enhancement_workflow_template/.../10_normal_execution_02_...
```

良い例:

```text
.../{{WORK_DIR_NAME}}/40_operator_workflows/agent_entry_prompts/
10_normal_execution_02_work_package_coding_agent_prompt.md
```

Humanはruntime variablesのみ渡す。

### 4.5. Information isolation ruleを視覚的・構造的に強化する

Work Package Coding Agentについて、次を強制する。

```text
Normative workflow document reachable by Coding Agent = assigned Pxx only
```

Pxxの本文はself-containedにする。

Human/auditor用traceability linkが必要な場合も、Coding Agentに別workflow documentを読ませる指示として書かない。

### 4.6. Test Agentとの情報分離を維持する

Gate 07はIndependent Verification authorityであり、Coding Agentへacceptance-answer keyとして露出させない。

Coding Agentのfocused testはpackage completion用であり、Gate PASS判定ではない。

### 4.7. Agent Execution Readiness validationを新設する

Document complianceとは別に、execution前に最低4軸を検証する。

| Validation axis | Required check |
|---|---|
| Artifact completeness | 必須instance artifactが存在するか |
| Content completeness | required sections/fieldsを省略していないか |
| Execution resolvability | Human entryだけでEnhancement/Gate/Package/Trialを一意に解決できるか |
| Information isolation | Agentが許可されたnormative sourceだけで実行できるか |

### 4.8. Agent execution前のmechanical checksを定義する

最低限次を自動検査可能にする。

```text
1. Enhancement-side agent_entry_prompts directory exists
2. Enhancement-fixed placeholders == 0
3. WORK_ROOT exists and points to exactly one enhancement root
4. Assigned Pxx glob resolves to exactly one file
5. Coding Agent prompt does not direct-read 06/07/P00/other Pxx
6. Coding Agent Pxx does not require 06/07/P00 to complete specification
7. Runtime identifiers are present
8. Branch/remote identity is explicit
```

不成立なら `BLOCKED` とし、Agent実装を開始しない。

---

## 5. 推奨するCoding Agent entry topology

```text
Human operator
    |
    | short entry instruction
    v
Enhancement-specific instantiated operator prompt
    |
    | resolver + guardrail
    v
Assigned Pxx
    |
    | self-contained implementation contract
    v
source / tests / config / migrations
```

読ませるworkflow文書は実質2つにする。

1. instantiated operator prompt
2. assigned Pxx

06 / 07 / P00 / README / 00 / 20 / 30はHuman/operator/test/audit側の責務に残す。

---

## 6. さらに検討可能な改善

### 6.1. Execution-specific fully-resolved prompt生成

必要なら、executionごとに完全展開済みpromptを生成する方式を検討する。

例:

```text
40_operator_workflows/agent_entry_prompts/runtime/
  G01_P01_Trial01_coding_agent_prompt.md
```

この場合Human instructionは1 pathだけで済み、runtime variable解決エラーもなくせる。

利点:

- Enhancement/Gate/Package/Trial identityが完全一意
- Human instructionが最小
- 実行prompt自体がaudit evidenceになる
- Agentが推測する余地を減らせる

欠点:

- execution単位でprompt artifactが増える

これはMUSTではなくtemplate design optionとして検討する。

---

## 7. README / template documentationへの反映箇所

最低限以下を修正対象とする。

- root `README.md`
- `40_operator_workflows/README.md`
- `40_operator_workflows/agent_entry_prompts/README.md`
- `40_operator_workflows/agent_entry_prompts/00_variable_conventions.md`
- `10_normal_execution_01_single_execution_coding_agent_prompt.md`
- `10_normal_execution_02_work_package_coding_agent_prompt.md`
- Candidate Assembly / Test / Remediation / Orchestration prompts（固定値/runtime値の同一規則を適用）
- preflight / controlled runbook（Agent Execution Readiness checkを組み込む場合）
- `TEMPLATE_STRUCTURE.md`
- `MANIFEST.json`（required instantiated artifact metadataを持たせる場合）

---

## 8. Acceptance Criteria — workflow template修正

Template改修完了条件として、最低限次を満たすこと。

### AC-WF-01
Enhancement-specific `agent_entry_prompts/` を作成せず、template directory上のpromptを直接指定した場合、execution readinessがFAIL/BLOCKEDになる。

### AC-WF-02
Enhancement-fixed valuesに未解決placeholderが残る場合、Coding Agent executionを開始しない。

### AC-WF-03
Work Package Coding AgentのHuman entryから、Enhancement / Gate / Package / Trialを一意に決定できる。

### AC-WF-04
Assigned Pxx globが0件または2件以上の場合、Coding Agent executionを開始しない。

### AC-WF-05
Coding Agentが仕様補完目的でGate 06 / 07 / P00 / other Pxxへ誘導されない。

### AC-WF-06
Assigned Pxx単独で、Coding Agentがimplementation scope / constraints / completion criteria / stop conditionを判断できる。

### AC-WF-07
Human/auditorはPxx ↔ Gate contract ↔ verification contractのtraceabilityを維持できるが、そのtraceabilityがCoding Agentのread dependencyにならない。

### AC-WF-08
Document template complianceとAgent execution readinessが独立したvalidation結果として出力される。

### AC-WF-09
Human Quick HowToUseのcanonical exampleはEnhancement-specific instantiated promptを参照する。

### AC-WF-10
Coding Agent operator promptはworkflow全体の説明書ではなく、resolver + guardrailとして最小化されている。

---

## 9. 非目的

今回のtemplate修正で次は変更しない。

- ENH-E6 product requirements
- ENH-E6 G01 acceptance semantics
- Ariadne Family/Stage navigation design
- production code
- Gate 06 / 07の一般的な責務分離そのもの

対象はworkflow templateのinstance化、Agent routing、information isolation、execution readiness validationである。

---

## 10. 優先順位

### P0 — 先に修正すべきもの

1. Enhancement-specific operator prompt instantiation MUST化
2. Enhancement-fixed / Runtime variable分離
3. template-side prompt直接実行禁止
4. Coding Agent information isolation明文化
5. Execution resolvability preflight

### P1 — 続けて修正

6. Coding Agent operator promptの小型化
7. artifact completeness vs execution readinessの別判定
8. Quick HowToUse全面更新

### P2 — Optional

9. execution-specific fully-resolved runtime prompt生成方式
10. MANIFESTを使ったrequired instantiated artifact自動検査

---

## 11. 一言での申し送り

> `agentic_enhancement_workflow_template` は、artifact schemaだけでなくAgent execution controlまでtemplate自身が強制できる構造へ修正すること。特に、template側operator promptを直接Agentへ渡さず、Enhancement-specific promptをinstance化して固定identityを事前展開すること、Coding Agentのnormative contextをassigned Pxxへ限定すること、document complianceとは別にexecution resolvability / information isolationを機械検証することをMUST化する。
