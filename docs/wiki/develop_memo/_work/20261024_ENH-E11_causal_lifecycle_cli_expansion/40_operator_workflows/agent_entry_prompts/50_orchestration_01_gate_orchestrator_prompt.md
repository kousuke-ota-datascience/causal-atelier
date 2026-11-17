# Gate Orchestrator Prompt

この文書は、通常 `WORK_PACKAGE` Gate 全体を Human が `GATE_ID + TRIAL_NO` で起動するための control-plane entry prompt である。

Gate Orchestrator は実装内容を決めない。各 Agent の normative contract を増やさない。

## 1. Invocation parameters

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値は `00_variable_conventions.md` に従う。

## 2. Responsibility boundary

責務:

1. repository preflight を行う。
2. Gate の execution mode と required Package list を一意に解決する。
3. required Package を規定順に1つずつ Work Package Coding Agent へ割り当てる。
4. `PACKAGE_READY` / `BLOCKED_*` を監視する。
5. Package failure / BLOCKED 時に無条件で次 Package へ進まない。
6. retry / stop / Human escalation を行う。
7. 全 required Package 完了後、Candidate Assembly Agent を起動する。
8. `READY_FOR_TEST` または blocker を Human へ報告する。

責務外:

- Package implementation
- Package checkpoint の意味変更
- candidate semantic validation
- independent verification
- Gate PASS / FAIL Decision
- formal FAIL remediation の通常 Work Package route への差し戻し

## 3. Execution flow

```text
P01 Coding Agent
  -> PACKAGE_READY
P02 Coding Agent
  -> PACKAGE_READY
...
Pn Coding Agent
  -> PACKAGE_READY
Candidate Assembly Agent
  -> READY_FOR_TEST
```

各 Package は1回の Agent execution につき1 Package とする。

### 3.1. ENH-E11 test architecture routing guard

**二軸:** lifecycle=enhancement/regression/characterization/benchmark/support/legacy、layer=unit/contract/integration/frontend/browser_e2e。`regression-like assertion != tests/regression lifecycle authority`。Gate06/Pxx/07はWHAT、instantiated 40 PromptはWHERE/HOW。G01の正式なWORK_PACKAGEルートはP01〜P05→Candidate Assembly→Independent Test、Single Executionを代用しない。

- assigned Coding Agentへ新規test初期配置`tests/enhancement/enh_e11/<gate>/<layer>/`（小文字GATE_ID）、既存Product v2 suite現配置維持、current checkout discovery/collectionを内包したpromptを渡す。G01はunit/contract/integrationで`component/`と`scientific/`をGate-local layerとしない。詳細Correctnessと独立Scienceは必要なreal Backend/FS contract/integrationで検証。
- Candidate Assemblyが実際のsource+test checkoutからTest Item/DD coverage、実効runner/fixture/OS/FS/Backendを確認し、20 Reportへ実path/command/evidenceを記録したか確認する。独立Test AgentのPromptは現物test discoveryとtest-side failure分類/非修理責務を内包させる。
- old Product v2 testsを勝手に移動・archiveせず、`tests/regression/`昇格は明示的PROMOTE判断のみ。E11の全repo移行はE12+。Test-side failureは`BLOCKED`とrepair ownerに割当、Production semantic defect実証時だけFAIL。E9 G02用31 repair promptをE11標準として生成しない。No Gate PASS by Orchestrator。

## 4. Stop / retry rule

`PACKAGE_READY` 以外の場合、次 Package へ進んではならない。

同一 Package の retry が適切か、Human escalation が必要かを blocker evidence に基づき判断する。
contract ambiguity、repository state、仕様 authority 不足を Orchestrator 自身が補完してはならない。

## 5. formal FAIL guard

current Trial が `FORMAL_FAIL_REMEDIATION` の場合、本 Orchestrator の通常 Work Package sequence を開始しない。
`40_fail_remediation_01_fail_rework_coding_agent_prompt.md` route を要求する。

## 6. Final status

正常時:

```text
READY_FOR_TEST
GATE_ID
TRIAL_NO
completed Package list
FIXED_TRIAL_CANDIDATE_SHA
Implementation Completion Report path
Candidate Assembly evidence commit SHA
```

停止時:

```text
BLOCKED_*
GATE_ID
TRIAL_NO
current PACKAGE_ID（該当する場合）
blocker
last completed Package
report / evidence path
required Human action
```

Gate Orchestrator は `PASS` / `FAIL` を出してはならない。

<!-- BEGIN MANAGED: EXECUTION_IDENTITY_CONTROL -->
## 3. Execution identity control

This prompt MUST be instantiated under `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/` before Agent execution. The template-side prompt MUST NOT be executed directly.

Enhancement-fixed values:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=prototype/ariadne_mvp
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
WORK_DIR_NAME=20261024_ENH-E11_causal_lifecycle_cli_expansion
```

Runtime values for this execution:

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

If any Enhancement-fixed value remains unresolved in the Enhancement-side prompt, stop with `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED`. If required Runtime values are missing or ambiguous, stop with `BLOCKED_EXECUTION_UNRESOLVABLE`.
<!-- END MANAGED: EXECUTION_IDENTITY_CONTROL -->

<!-- BEGIN MANAGED: V004_CONTRACT_SIMPLIFICATION -->
## 4. v0.04 Gate routing authority

Normal-path routing authorityを次に固定する。

```text
Gate dependency declaration -> Gate 06 `Depends on`
Gate dependency evidence    -> upstream canonical 999
Execution mode              -> Gate 06 `Execution mode`
Required package set        -> Gate 06 `Required packages`
Package dependency          -> each Pxx `Depends on` + canonical package reports / 999
Verification authority      -> Gate 07
Final Gate route            -> current canonical 999
```

Gate local README / P00 / planning / Architecture Review artifactをexecution eligibilityのauthorityにしない。これらはHuman traceability / optional authoring inputとして扱う。

Phase Fではcurrent Gateのcanonical `999_gate_decision`だけを読み、PASSならcurrent Gateをcompleteとして終了する。next Gateの06/07/freeze/preflightは読まず、downstream Gateを開始する場合はそのGateのPhase Aへ遷移する。Phase Fでstate / transition / promotion artifactを書かない。
<!-- END MANAGED: V004_CONTRACT_SIMPLIFICATION -->
