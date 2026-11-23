# 40_operator_workflows — Human-controlled orchestrationの作成・使用ガイド

**2026-11-23 実行時Authority更新（Owner）:** 対象GitHub repositoryは `kousuke-ota-datascience/causal-atelier`（変更なし）、唯一の現行作業/実装/push先branchは `feature/ariadne_mvp_e11`。40のinstantiated `BRANCH_NAME` と `git push` 指示は変更済み。`REMOTE_NAME=causal-atelier` はローカルremote alias（要実環境照合）でありリポジトリ名・branch名とは別。G01 S10/S11は[179](../00_enhance_background/Revised_requirements_definition_documents/combined_review/179_20261123_g01_provisional_s10_owner_approved.md)・[180](../00_enhance_background/Revised_requirements_definition_documents/combined_review/180_20261123_g01_limited_s11_owner_coding_authorization.md)で限定承認済み。詳細は[182 branch migration](../00_enhance_background/Revised_requirements_definition_documents/combined_review/182_20261123_e11_execution_branch_retargeting.md)。本ガイド中の「S10/S11全Gate未承認」記載は策定時点の履歴であり現在のG01状態ではない。G01_999はBLOCKED、実Coding Agent起動は未観測。

**ENH-E11 DEC-PREPCODE-01=B（Owner 2026-11-22採用）：Gate別独立監査・Freeze・Coding Authorization。** 全402のsource SHA索引は変更影響の全体発見用であり、全Gateの科学・契約独立PASSではない。最初に共通E11契約とG01の実依存閉包について独立S09審査、Owner G01-S10 Freeze、別個のOwner G01-S11 Coding Authorizationを得る。G02以降は当該Gate固有のS09→S10→S11と必要な先行Gate999の**実PASS**を当該GateのS11前に確認する。S09文書監査準備は先行Gateのcoding中でも可能。S11がない場合Agentを起動せず、`BLOCKED_CODING_AUTHORIZATION`を記録する。対象外GateはSHA索引には保持するが`NOT_REVIEWED`、実際のMethod別07/999・T2/T3・FS/Reader・旧Product回帰を省略しない。Owner決定記録は`combined_review/173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md`。**現時点S10/S11は全Gate未承認。**

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけで40層の用途・各workflowの責務・operator artifactのself-containment ruleが分かること。

## 1. Purpose

`40_operator_workflows/`は、product acceptance contractとは別に、HumanがAgentの起動・architecture discovery・preflight・destructive operation等をbounded executionとして制御する層である。

40層のresultは、明示的に30層へ取り込まれない限りGate PASS authorityを持たない。

## 2. Sub-workflows

### `agent_entry_prompts/`
Single Execution Coding / Work Package Coding / Candidate Assembly / FAIL rework / Independent Test / Gate Orchestratorを起動するparameterized prompt。各prompt自身にhuman-supplied variables、derived-variable rule、target path、required output、stop conditionを含める。

### `architecture_review/`
current architecture discovery、target architecture decision、Gate decompositionを行う。product codeを実装するworkflowではない。

### `preflight/`
DB / migration / service / toolchain等のexecution prerequisiteを検証する。preflight FAILとproduct implementation FAILを区別する。Gate blocking Browser E2Eではstale service / image / fixtureに依存しないhermetic execution prerequisiteを確認する。

### `BROWSER_E2E_GATE_POLICY.md`
Browser E2Eを少数のcritical user journeyへ限定し、test-layer allocation、hermetic environment、semantic synchronization、observable assertion、failure evidence / classificationを定義する共通authoring / operational policy。個別GateのAcceptance authorityではなく、必要なGate固有ruleはfrozen 07へ具体化する。

### `controlled_runbook/`
破壊的・不可逆・infrastructure-sensitive operationをstep単位で実行し、各step後にHuman decision boundaryを置く。

## 3. Operator Artifact self-containment

Agentへ直接渡すprompt / instructionは、そのexecutionのために必要な以下を本文内に持つ。

- required variables / expansion rule
- exact target / allowed action
- prohibited action
- output schema / output path
- completion / abort / stop condition

共通ガイドを別ファイルに保持してよいが、**実行時に別のvariable conventionやresult templateを読まなければpromptを実行できない構造にしない。**

external source / commit / DB / previous result等はexecution target / precondition evidenceとして参照してよい。

<!-- BEGIN MANAGED: WORKFLOW_EXECUTION_CONTROL -->
## 2. Workflow Execution Control

### 2.1. Template-side prompt direct execution prohibition

`agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/` はauthoring sourceであり、Agent executionへ直接指定してはならない。

Enhancement開始時にEnhancement-specific prompt instanceを以下へ生成する。

```text
{{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
```

### 2.2. Variable lifecycle

Enhancement-fixed variablesはinstance化時に確定する。

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
BRANCH_NAME
REMOTE_NAME
WORK_ROOT
WORK_DIR_NAME
```

Runtime variablesだけをexecution時にHuman operator / Orchestratorが与える。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

### 2.3. Coding Agent context isolation

Work Package Coding Agentのnormative contextはassigned Pxxだけとする。

Human/auditor traceabilityとAgent-visible normative contextを分離する。

```text
Human traceability != Agent-visible normative context
```

### 2.4. Execution readiness

Document complianceとAgent Execution Readinessを独立判定する。readinessがFAILならAgentを起動しない。

最低4軸:

1. Artifact completeness
2. Content completeness
3. Execution resolvability
4. Information isolation

Metadata parsingはMarkdown decorationに依存させない。`**Field:** value` / `Field: value` / `- Field: value` のような意味的に同一の表記差は許容し、field欠落・空値・解釈不能なdependency・evidence欠落のみをblocking対象とする。共通実装は `40_operator_workflows/tools/workflow_metadata.py` を使用する。

### 2.5. Runtime authority minimization

Normal-path preflight / orchestrationのrouting authorityはGate 06 / 07へ集約する。

- Gate dependency declaration: 06 `Depends on`
- execution mode: 06 `Execution mode`
- required package set: 06 `Required packages`
- package dependency: each Pxx `Depends on`
- Gate dependency evidence: canonical 999

Gate local README / P00 / Architecture Review artifactはnormal runtime authorityにしない。
<!-- END MANAGED: WORKFLOW_EXECUTION_CONTROL -->

<!-- BEGIN MANAGED: OPERATOR_QUICK_HOWTOUSE -->
## 3. Operator Quick HowToUse

### 3.1. Prerequisite

以下のentry instructionは、**Enhancement-specificにinstance化済みの** `{{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/` を参照する。

template directory上の `agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/` をAgentへ直接指定してはならない。

### 3.2. SINGLE EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_01_single_execution_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.3. WORK PACKAGE EXECUTION — STEP by STEP

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- PACKAGE_ID=<PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.4. CANDIDATE ASSEMBLY

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.5. INDEPENDENT VERIFICATION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 30_independent_verification_01_test_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.6. FORMAL FAIL REMEDIATION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 40_fail_remediation_01_fail_rework_coding_agent_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- REMEDIATION_PACKAGE_ID=<REMEDIATION_PACKAGE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```

### 3.7. GATE WIDE AUTONOMOUS EXECUTION

```text
下記文書に記載の指示を実行すること。

- {{WORK_ROOT}}/40_operator_workflows/agent_entry_prompts/
    - 50_orchestration_01_gate_orchestrator_prompt.md

今回の指示は
- GATE_ID=<GATE_ID>
- TRIAL_NO=<TRIAL_NO>
である。
```


### 3.8. SUPPORTING DOCUMENTS — NOT DIRECT EXECUTION ENTRY POINTS

以下もEnhancement-specific `agent_entry_prompts/` instanceへ含めるが、Human operatorがAgentへ直接指定するexecution promptではない。

- `README_40_agent_entry_prompts.md`
- `00_variable_conventions.md`

Agent起動前にtemplate-side readiness validatorを実行し、`OVERALL: READY_FOR_AGENT_EXECUTION` の場合のみ上記entry instructionを使用する。
<!-- END MANAGED: OPERATOR_QUICK_HOWTOUSE -->

<!-- BEGIN MANAGED: README_NAMING_CONVENTION -->
## 4. README Naming Convention

### 4.1. Rule

Enhancement work root / workflow template rootのtop-level READMEだけを無印 `README.md` とする。

nested directoryのlocal READMEは、directory pathから機械的に導出した `PATH_ID` をpostfixとして付与する。

```text
README filename = deterministic function(directory path)
```

```text
root/
  README.md

root/00_enhance_background/
  README_00.md

root/20_implementation_reports/G01/Trial01/
  README_20_G01_Trial01.md

root/40_operator_workflows/agent_entry_prompts/
  README_40_agent_entry_prompts.md
```

### 4.2. PATH_ID generation

Enhancement/template rootからREADME配置directoryまでのrelative pathを左から処理する。

1. `NN_<semantic_name>` 形式のworkflow namespace directoryは `NN` に短縮する。
2. `G01`, `P01`, `Trial01` 等のruntime identity directoryはそのまま保持する。
3. `agent_entry_prompts`, `preflight` 等の非numbered semantic directoryは名前を保持する。
4. tokenを `_` で連結する。
5. `README_<PATH_ID>.md` とする。

例:

```text
00_enhance_background
  -> 00
  -> README_00.md

20_implementation_reports/G01/Trial01
  -> 20_G01_Trial01
  -> README_20_G01_Trial01.md

40_operator_workflows/agent_entry_prompts
  -> 40_agent_entry_prompts
  -> README_40_agent_entry_prompts.md
```

### 4.3. Invariants

- root以外に無印 `README.md` を置いてはならない。
- 同一directoryに複数のlocal READMEを置いてはならない。
- 手作業でpostfixを決めてはならない。必ずpath-derived naming functionを使用する。
- rename時はMarkdown links、plain path references、operator prompts、structure/manifest、validator/instantiation toolingを同時更新する。
- target filename collisionが発生した場合は自動上書きせず `BLOCKED_README_NAMING_COLLISION` とする。

### 4.4. Canonical implementation

canonical naming functionは以下とする。

```text
40_operator_workflows/tools/readme_naming.py
```

Template migration/apply tooling、instantiation tooling、validatorは同一規則を使用し、別々の命名ロジックを持たない。
<!-- END MANAGED: README_NAMING_CONVENTION -->

## 5. ENH-E11 G01〜G10共通 Test Architecture — 40 Operatorの責務

**根拠:** [ENH-E9 → ENH-E11 test architecture handoff](../../20260905_ENH-E9_workflow_stabilization/00_enhance_background/08_test_architecture_migration/09_handoff_to_enh_e11.md)。本`5は**正式Gate G01〜G10すべて**に適用する実行規約であり、各Gate 06/Pxx/07の検証要求を代替しない。

`GATE_ID`は実行時変数。40は全Gate共通の **WHERE / HOW**（Test配置・発見・実行・Evidence・Test-side障害処理）を規定し、各Gateの06/Pxx/07が **WHAT**（実装対象、受入条件、保護するInvariant、必要なVerification layer、Browser E2E要否）を定める。G01固有のFCI/PAG科学契約をG02〜G10へ一般化してはならない。一方、ENH-E11の採用済み実装Scopeは全GateでLocal Scientific CLIであり、新規Web/API/Worker/DB/UI統合を含まない。Gate固有の実行・科学契約はそれぞれの06/Pxx/07が所有する。

### 5.1. 直交する二つのTest分類軸

| 軸 | 分類 | 規定する内容 |
| --- | --- | --- |
| Lifecycle / authority | `regression`, `enhancement`, `characterization`, `benchmark`, `support`, `legacy` | Provenance・長期保護対象・昇格/廃止のAuthority |
| Verification layer | `unit`, `contract`, `integration`, `frontend`, `browser_e2e` | 何をどの境界・実環境で実証するか |

`regression-like assertion != tests/regression lifecycle authority`。既存Product behaviorの不変条件を検証する新規E11テストであっても、最初のLifecycleはenhancementでよい。回帰観点があるだけで物理的な`tests/regression/`移動を命じてはならない。

### 5.2. G01〜G10の共通配置・発見ルール

1. **新規またはmaterially rebuiltしたGate固有Test**は原則 `tests/enhancement/enh_e11/<gate>/<layer>/` に置く。`<gate>` は実行時`GATE_ID`のlowercase（G01→g01、G10→g10）、`<layer>` は`5.1の5種から、そのGateのPxx/06/07が要求する証明レイヤーを選ぶ。`component/`と`scientific/`を新しいGate-local標準レイヤーとして追加しない。
2. **ENH-E11 G01〜G10のLocal CLI Scope:** 新規Web UI/Frontend機能を対象外とするため、新規Browser E2E blocking journeyは全Gateで**N/A**。各Gateの主要な証明レイヤーはunit/contract/実CLI・Linux FS integration/独立Scientific Reference。既存Productを変更した影響がある場合は、既存Browser E2Eを含むaffected regression suiteを実施しうる。将来Web/UIをE11へ追加する場合はOwnerの正式scope amendment、06/07再Freeze、Browser test契約の具体化を先行させる。G01固有PAG/FCI検証は他Gateに無差別適用しない。
3. **既存Testの共存:** `tests/product/`、`tests/integration/`、`tests/scientific/`、`tests/browser_e2e/` 等の既存Suiteはcurrent invariantが有効なら現配置のまま利用する。対象Gateに必要でないという理由だけでは移動・archiveしない。事実上obsoleteと判断した場合だけ`legacy_archive`を検討する。
4. **`tests/regression/`への昇格:** 将来のProduct invariantを継続的に守るという個別のsemantic promotion decisionがあるときに限る。E11完了時のDisposition候補は `PROMOTE/REWRITE/MERGE/SPLIT/RETIRE/ARCHIVE/KEEP_ENHANCEMENT`。`tests/characterization/scientific/`、`tests/benchmarks/scientific/`、`tests/support/`の採用も用途と再利用根拠がある場合だけ。ENH-E11中のrepository-wide移行は必須ではなく、包括的再構成はENH-E12以降。
5. **Gate existence/readiness:** `GATE_ID`はG01〜G10の範囲で指定する。対応する06/07/Pxx/08が未作成・未Freeze・一意でない・Coding Authorizationがない場合、該当実行フェーズは`BLOCKED_*`で停止する。後続Gateの文書をG01の06/07から推測生成してはならない。

### 5.3. 実体化済み40 Promptへの共通実行規則

**Coding Agent:** Assigned 06/Pxxを唯一の実装WHATにして、new/rebuiltテストのinitial lifecycleとverification layerを判断。current checkoutでfile存在、collection、fixture/conftest、dependency、runner適格性を確認してfocused verificationを実行。Agent-visible entry prompt内にこの規則を直接持ち、READMEの再参照を必須にしない。

**Candidate Assembly:** Gate06のrequired package/実行modeを確認し、current checkoutのTest/Runnerと既存Protected Suiteを発見。Gate-wide self-verificationとProduct Candidate SHAの固定のみ行い、独立07/999のPASSを代行しない。

**Independent Test Agent:** まず当該Gateの`tests/enhancement/enh_e11/<gate>/`、次に関連既存Suiteをcurrent candidate SHAから発見。存在・pytest collection・runner/environmentを確認して実行し、`Gate Item / DD ID / lifecycle / layer / actual path / command / source SHA / fixture SHA / result`をEvidenceに保存。テスト不具合の診断は行えるがtest/production codeを修復しない。

**Failure classification:** `PRODUCT_DEFECT / TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN`。Product違反未実証でTest側が評価不能なら`BLOCKED`。Repairを別責務へ切り出し、ENH-E9 G02専用31を無条件コピーしない。

**Fixed Candidate:** Test-side-onlyの変更でProduct Candidateを無条件に再Freezeせず、`PRODUCT_SEMANTIC_CHANGE / TEST_IMPLEMENTATION_CHANGE / TEST_ORCHESTRATION_CHANGE / TEST_INFRASTRUCTURE_CHANGE / DOCUMENTATION_ONLY`を分類する。Product意味変更の可能性を除外できないときだけCandidate identity BLOCKED。

**Atomic move:** Test移動が承認された場合はpath/import/fixture/conftest/pytest marker/CI/Dockerfile COPY/.dockerignore/compose/Browser build context/evidence pathを同一Batchで整合させる。`Path(__file__).parents[N]`などの階層固定依存を避け、07のACをRunner不調のために緩和しない。

### 5.4. 正本と実行状況

- 実体化された6種のAgent Promptと変数規約は`40_operator_workflows/agent_entry_prompts/`に存在し、**G01〜G10共通で使用する**。Gate別実装契約は`10_enhance_instruction/<GATE_ID>/`側に存在する場合だけ有効。
- **文書実在状況（2026-11-17）：G01〜G10に06/07が存在し、G02〜G10には各P00と計36件のPxxを作成済み。** いずれもPREP-03 Review DRAFTであり、承認・Freeze・Coding Authorization・Gate999 PASSを意味しない。存在と実行可能性を混同しない。
- G01はWORK_PACKAGE方式の草案で、Coding Authorization未発行。Promptの存在はOwner承認・06/07 Freeze・readiness validator・実装着手権限を意味しない。



## 2026-11-22 S02 Owner決定反映と40 Operatorの責務境界

G01〜G10のGate-level 06/07 20件、P00/Pxx 51件が現存するが、現段階ではDraftであり、各GateのFreeze/Owner Coding Authorizationは別の明示承認事項。40 Operatorの実行Prompt 7文書は共通してS02 8項目の遵守、Method別Registry/strict overlay、Study単独row opt-inとOS/Method必須guard、G10の全41独立Science証拠の完全性と影響閉包に基づく選択再実行、旧Product ABIへの変更影響回帰、G01 FS有界試験、Local Graph content hash/非Product Version、NFR-034 DEFERREDと社内OSS遵守を実行前の検証条件とする。40はTest WHERE/HOWとAgent実行/候補SHA/独立性を所有するが、06/Pxx Coding WHATと07 Test WHAT、Owner判断や999 Gate Decisionを創作しない。S05 Backend/Scienceの実環境試験は未実施であり、指示書だけをもってScience PASS/Coding Authorizationとは扱わない。
