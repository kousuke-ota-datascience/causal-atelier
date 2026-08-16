# Agentic Enhancement Workflow Template v0.01 — Handoff

> Handoff date: 2026-08-15  
> Scope: `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/`  
> Canonical handoff artifact: `agentic_enhancement_workflow_template_v0.01.zip`  
> SHA-256: `cbbd27283bbd90e7389adbfebd781be1d239fe480e07b97b3f207f86f6d2a0c6`  
> Status: provisional consolidated baseline; actual repository full-tree reconciliation is still required

---

## 1. このhandoffの目的

このチャットで行った `agentic_enhancement_workflow_template` の設計修正を一本化し、次チャットで過去の議論を再構築せずに作業を再開できる状態にする。

次チャットでは、**過去の個別bundleではなく `agentic_enhancement_workflow_template_v0.01.zip` を作業基準にすること。**

ただし、このZIPは実repository checkout全体を取得して再構成したものではない。会話中に取得・materializeできたtemplateファイルを統合したbaselineであるため、actual repositoryとのfull-tree diff / mergeが次工程で必要である。

---

## 2. 引継ぎ時に渡すファイル

必須:

```text
agentic_enhancement_workflow_template_v0.01.zip
agentic_enhancement_workflow_template_v0.01_HANDOFF.md
```

補助的に必要なら:

```text
agentic_enhancement_workflow_template_v0.01_VALIDATION.txt
```

ZIP内のHowToUseは、

```text
README_Appendix_HowToUse.md
```

である。

これは、このチャットでP0修正を反映した `README_Appendix_HowToUse_v0.09.md` の内容をcanonical filenameへ変更して収録したもの。

---

## 3. v0.01 ZIPの構成

現在のZIPには以下が含まれる。

```text
agentic_enhancement_workflow_template/
├─ README.md
├─ README_Appendix_HowToUse.md
├─ README_NAMING_CONVENTION.md
├─ TEMPLATE_STRUCTURE.md
└─ 40_operator_workflows/
    ├─ README_40.md
    ├─ agent_entry_prompts/
    │   ├─ README_40_agent_entry_prompts.md
    │   ├─ 00_variable_conventions.md
    │   ├─ 10_normal_execution_01_single_execution_coding_agent_prompt.md
    │   ├─ 10_normal_execution_02_work_package_coding_agent_prompt.md
    │   ├─ 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md
    │   ├─ 30_independent_verification_01_test_agent_prompt.md
    │   ├─ 40_fail_remediation_01_fail_rework_coding_agent_prompt.md
    │   └─ 50_orchestration_01_gate_orchestrator_prompt.md
    ├─ preflight/
    │   └─ AGENT_EXECUTION_READINESS.md
    └─ tools/
        ├─ instantiate_agent_entry_prompts.py
        ├─ readme_naming.py
        └─ validate_agent_execution_readiness.py
```

---

## 4. ここまでに確定した主要設計

### 4.1. Template-side prompt直接実行は禁止

以下はauthoring sourceであり、Agent executionへ直接指定しない。

```text
agentic_enhancement_workflow_template/
40_operator_workflows/agent_entry_prompts/
```

Enhancement開始時に、

```text
{WORK_ROOT}/40_operator_workflows/agent_entry_prompts/
```

へEnhancement-specific promptをinstance化する。

Human/operatorはinstance側promptだけをAgentへ指定する。

### 4.2. IdentityをEnhancement-fixedとRuntimeに分離

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

Execution時のruntime identity:

```text
GATE_ID
PACKAGE_ID                 # Work Package mode
TRIAL_NO
REMEDIATION_PACKAGE_ID     # remediation
AMENDMENT_ID               # amendment
```

`WORK_ROOT` はdirectory nameではなく、Enhancement work rootへのpathそのもの。

### 4.3. Coding Agent information isolation

Work Package Coding Agentのnormative workflow contractは、

```text
Enhancement-specific Coding prompt
+
assigned Pxx only
```

とする。

仕様補完目的で以下を読ませない。

```text
Gate 06
Gate 07
P00
other Pxx
00 background/planning
20 reports
30 reports
past Enhancement
ADR / issue / external Web
```

current repositoryのsource / tests / config / migrationsはimplementation substrateとして調査可能だが、current behaviorをspecification authorityにはしない。

assigned Pxxがself-containedでなければ探索範囲を広げずBLOCKEDにする。

### 4.4. Human traceabilityとAgent-visible contextを分離

原則:

```text
Human traceability != Agent-visible normative context
```

Human/auditorはPxx ↔ Gate contract ↔ verification contractを追跡できる。

そのtraceabilityをCoding Agentのread dependencyにはしない。

### 4.5. Agent Execution ReadinessをDocument Complianceから分離

最低4軸:

```text
1. Artifact completeness
2. Content completeness
3. Execution resolvability
4. Information isolation
```

template側のmechanical validator:

```text
40_operator_workflows/tools/validate_agent_execution_readiness.py
```

HowToUseでは、これに加えてbranch / dependency / Gate contract semantics等をHuman/operatorが確認するsemantic preflightを区別している。

### 4.6. Mutable Current State Sheetを廃止

以下の考え方を採用した。

```text
Declared mutable state
    ではなく
Canonical evidence
    ↓
Derived state
```

`TEMPLATE_Current_State_Control_Sheet.md` / `Current_State_Control_Sheet.md` は廃止対象。

状態authority:

```text
Pxx dependency
    = upstream package execution evidence

Gate dependency
    = upstream canonical 999 Gate Decision

Gate readiness
    = static routing/dependency declaration
      + Gate 06
      + Gate 07
      + blocking preflightなし

Candidate readiness
    = implementation completion evidence

Final Gate authority
    = canonical 999 Gate Decision
```

**Gate local READMEを新しいmutable state sheetとして使ってはならない。**

Gate local READMEはstatic routing / dependency declaration / canonical artifact indexに限定する。

### 4.7. README postfix naming

Top-levelだけ無印:

```text
README.md
```

nested READMEはpath-derived deterministic naming:

```text
00_enhance_background/
    README_00.md

20_implementation_reports/G01/Trial01/
    README_20_G01_Trial01.md

40_operator_workflows/agent_entry_prompts/
    README_40_agent_entry_prompts.md
```

原則:

```text
README filename = deterministic function(directory path)
```

canonical implementation:

```text
40_operator_workflows/tools/readme_naming.py
```

root以外の無印 `README.md` は禁止。

### 4.8. Markdown heading numbering

```text
#       title: numberなし
##      1. / 2. / 3.
###     1.1. / 1.2.
####    1.1.1.
#####   1.1.1.1.
```

`## 0.` を特例にしない。

### 4.9. Package state

HowToUse側では、Agent terminal outcomeとcanonical report semanticsを区別した。

```text
PACKAGE_READY
    = Coding Agentのterminal outcome label

State: PACKAGE_COMPLETE
    = canonical package report上のcompletion semantics
```

`PACKAGE_READY` 等のliteral自体をworkflow cursorにしない。

package completionは、

```text
assigned Pxx completion criteria
+
focused verification
+
canonical package report evidence
```

から導出する。

### 4.10. Execution modeとGate-level verification

execution modeはprompt fileの存在だけで決めない。

Gate contract / Gate local README等の**static routing**をauthorityとする。

最終workflow骨格:

```text
Phase A — Gate readiness
    ↓
execution mode
    ├─ WORK_PACKAGE
    │    ↓
    │  Pxx execution
    │    ↓
    │  all required Pxx complete
    │    ↓
    │  Phase C — Candidate Assembly
    │    ↓
    │  Fixed Trial Candidate
    │
    └─ SINGLE_EXECUTION
         ↓
       Gate-wide implementation
         ↓
       Candidate finalization
         ↓
       Fixed Trial Candidate

            共通
             ↓
Phase D — Independent Verification
    authority = frozen Gate 07
             ↓
Phase E — canonical 999 Gate Decision
             ↓
PASS / FAIL / BLOCKED
             ↓
Phase F — canonical evidenceから
          Next Gate / Enhancement completion判定
```

**Phase CだけがWork Package固有。Phase Dはexecution mode共通。**

Single ExecutionでもCoding Agent自身がGate PASSを判定してはならない。

---

## 5. Root README Quick HowToUse

root `README.md` には、Human/operatorがcopy/pasteできるexecution entryを掲載済み。

対象:

```text
SINGLE EXECUTION
WORK PACKAGE EXECUTION
CANDIDATE ASSEMBLY
INDEPENDENT VERIFICATION
FORMAL FAIL REMEDIATION
GATE WIDE AUTONOMOUS EXECUTION
```

すべて、

```text
{WORK_ROOT}/40_operator_workflows/agent_entry_prompts/
```

のEnhancement-specific instanceを参照する。

template-side promptを直接参照するcanonical exampleは置かない。

End-to-end procedureは、

```text
README_Appendix_HowToUse.md
```

へ分離している。

---

## 6. v0.01の検証結果

consolidated ZIPに対するvalidation:

```text
WORKFLOW TEMPLATE REVISION VALIDATION
PASS prompt inventory / instantiation rule
PASS Operator Quick HowToUse coverage
PASS Work Package context isolation
PASS Agent Execution Readiness policy
PASS hierarchical heading numbering
PASS deterministic nested README naming
PASS README reference migration / tooling integration
OVERALL: PASS
```

追加確認済み:

```text
root以外の無印 README.md              = 0
version付き README_Appendix_HowToUse = 0
Current_State_Control_Sheet参照       = 0
ZIP root                              = 1
ZIP integrity                         = PASS
```

SHA-256:

```text
cbbd27283bbd90e7389adbfebd781be1d239fe480e07b97b3f207f86f6d2a0c6
```

---

## 7. 重要: v0.01は「actual repository完全版」ではない

ここを次チャットで誤認しないこと。

v0.01 ZIPは、このチャットで取得できたtemplate materializationを一本化したもの。

**actual repositoryの `agentic_enhancement_workflow_template/` 全ファイルを取得してbyte-for-byteで再構築したものではない。**

したがって、validation PASSは、

> 「このZIPに含まれる既知範囲で、実装したmechanical invariantがPASS」

を意味する。

以下までは証明していない。

```text
actual repository全体のlink/reference整合
全Pxx templateのsemantic self-containment
actual MANIFEST schemaとの整合
全instantiation artifactのcompleteness
actual architecture_review / planning / report template群との整合
```

---

## 8. 次チャットで最優先に確認・修正する事項

### P0-1. actual repositoryとのfull-tree reconciliation

最優先。

次チャットではactual repository/templateの全treeを取得し、

```text
actual template
vs
agentic_enhancement_workflow_template_v0.01
```

を比較する。

**未知の既存本文をv0.01のstubで上書きしないこと。**

v0.01側の確定規約をactual repositoryへ移植し、actual側の既存semantic bodyを保持する。

### P0-2. Single Execution prompt本体をHowToUseと同期

現在v0.01 ZIPの

```text
10_normal_execution_01_single_execution_coding_agent_prompt.md
```

は、取得できたsource bodyが不足していたため、minimalなmanaged identity controlを追加したmaterialized skeletonである。

HowToUse v0.09ではSingle Executionについて、

```text
Gate-wide implementation
    ↓
candidate finalization
    ↓
Fixed Trial Candidate
    ↓
READY_FOR_TEST
    ↓
Phase D Independent Verification
```

をP0仕様として確定した。

**prompt本体がこのcontractを実装しているかactual repositoryで確認し、不足なら修正すること。**

### P0-3. Candidate Assembly / Test / Remediation / Orchestrator promptのactual body確認

以下もsource bodyを完全取得できていなかった。

```text
20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md
30_independent_verification_01_test_agent_prompt.md
40_fail_remediation_01_fail_rework_coding_agent_prompt.md
50_orchestration_01_gate_orchestrator_prompt.md
```

v0.01にあるものを完全なproduction contractとみなさない。

actual repositoryの既存semantic bodyとmergeすること。

### P0-4. package canonical report semanticsをprompt/toolingへ同期

HowToUseでは、

```text
PACKAGE_READY
    -> canonical report State: PACKAGE_COMPLETE
```

と定義した。

しかしv0.01のWork Package promptは、reportへ「Package status」を要求しているだけで、

```text
State: PACKAGE_COMPLETE
```

をcanonical fieldとして明示的に強制していない。

actual template側で、

```text
Coding prompt
dependency resolver
Candidate Assembly
preflight
HowToUse
```

が同じpackage completion semanticsを使用するよう同期すること。

### P0-5. Architecture Review entry point実在性

HowToUseは、

```text
40_operator_workflows/architecture_review/
01_architecture_discovery_prompt.md
```

を参照している。

しかしv0.01 ZIPには `architecture_review/` 自体が含まれていない。

actual repositoryで、

- 実在するか
- filenameが正しいか
- HowToUseのsource confirmation contractと一致するか

を確認する。

存在しないならHowToUseを合わせるか、canonical promptをtemplateへ追加する。

### P0-6. Current State Sheet廃止をactual repositoryへ完全適用

v0.01 ZIP内には `Current_State_Control_Sheet` は残っていない。

しかしactual repositoryについては未確認。

最低限、

```text
TEMPLATE_Current_State_Control_Sheet.md
instantiation logic
TEMPLATE_STRUCTURE.md
MANIFEST.json
README links
validator / preflight
operator prompt
compliance checklist
```

からの参照・生成を削除する。

別名のmutable state sheetを新設しない。

### P0-7. MANIFEST / structure / instantiationのactual schema確認

v0.01 ZIPにはactual repository由来の完全な `MANIFEST.json` は含まれていない。

actual repositoryに存在する場合は、

- README postfix
- Current State Sheet廃止
- required prompt instantiation
- required artifact set

へ同期する。

---

## 9. 次チャットでの推奨作業順序

### Step 1 — source of truthを固定

次チャットへ、

```text
agentic_enhancement_workflow_template_v0.01.zip
agentic_enhancement_workflow_template_v0.01_HANDOFF.md
```

を渡す。

次チャットではv0.01を**設計baseline**として扱う。

### Step 2 — actual repository treeを取得

```text
docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/
```

の完全inventoryを取得する。

まずread-onlyで構造と既存semantic bodyを確認する。

### Step 3 — full diff

分類する。

```text
A. actualのみ存在
B. v0.01のみ存在
C. 両方存在・内容一致
D. 両方存在・内容差
```

### Step 4 — schema/control-plane変更をactualへ適用

優先:

```text
1. Current State Sheet廃止
2. README postfix deterministic naming
3. Enhancement-specific prompt instantiation
4. fixed/runtime identity分離
5. Coding Agent information isolation
6. readiness validation
7. HowToUse v0.09 semantics
8. Single Execution / Independent Verification flow
9. package report semantics
```

### Step 5 — unknown semantic bodyを保護したmerge

既存prompt本文を不用意に短縮・置換しない。

特に、

```text
Single Execution
Candidate Assembly
Independent Verification
Remediation
Orchestrator
Architecture Review
```

はactual bodyを確認してからmanaged ruleをmergeする。

### Step 6 — full validation

最低限:

```text
- template-side prompt direct execution reference = 0
- Enhancement-side required prompt instantiation complete
- Enhancement-fixed unresolved placeholders = 0
- runtime identity resolution unique
- assigned Pxx resolution exactly one
- Coding Agent prohibited read dependency = 0
- root以外の README.md = 0
- stale README path reference = 0
- Current_State_Control_Sheet reference/generation = 0
- Markdown heading numbering = PASS
- Single Execution -> Fixed Trial Candidate -> Independent Verification = reachable
- Work Package -> Candidate Assembly -> Independent Verification = reachable
- package completion evidence semantics consistent
- actual MANIFEST / structure / tooling consistency
- Markdown link/path consistency
- git diff --check
```

---

## 10. 次チャットで変更してはいけないもの

このworkflow template作業の範囲では、

```text
Product requirements
Ariadne production code
ENH-E6 / ENH-E7固有product semantics
```

を変更しない。

今回の対象は、

```text
workflow template
operator control
agent routing
artifact authority
information isolation
execution readiness
README / documentation schema
```

である。

---

## 11. 次チャット冒頭に与える推奨instruction

```text
添付の以下2ファイルを引継ぎsourceとして使用せよ。

- agentic_enhancement_workflow_template_v0.01.zip
- agentic_enhancement_workflow_template_v0.01_HANDOFF.md

handoffに記載された確定済み設計を維持しつつ、
actual repositoryの
docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/
とのfull-tree reconciliationを行う。

重要:
- v0.01 ZIPは設計baselineだがactual repository完全コピーではない。
- actual repositoryにしか存在しない既存semantic bodyを推測で上書きしない。
- まずinventory / diffを取得し、その後に修正計画を提示する。
- Current State Sheetは廃止方針を維持する。
- Coding Agent normative context = assigned Pxx only を維持する。
- Independent Verificationは全execution mode共通のGate-level phaseとする。
- root以外のREADMEはdeterministic postfix namingとする。
- README_Appendix_HowToUse.md をoperator runbookのbaselineとする。

最初にhandoffとZIPを読み、
未解決事項・actualとの差分・修正計画・完了条件を整理せよ。
```

---

## 12. 最終状態

現時点の位置づけ:

```text
Design principles        : largely fixed
Operator HowToUse        : v0.09 P0 alignment completed
Consolidated baseline    : v0.01 created
Mechanical validation    : PASS on materialized scope
Actual repo reconciliation: NOT YET DONE
Production-ready template : NOT YET CLAIMED
```

次工程の本質は、**設計をさらに増やすことではなく、v0.01で確定したcontrol-plane設計をactual repositoryの全semantic bodyへ安全にmergeし、full-treeで検証すること**である。
