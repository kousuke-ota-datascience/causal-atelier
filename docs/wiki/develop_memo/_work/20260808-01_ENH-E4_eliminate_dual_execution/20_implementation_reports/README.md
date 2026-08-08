# 20_implementation_reports — Implementation Evidence Specification

# 0. common

## 0.1. Purpose

`20_implementation_reports/` は、Coding Agentが実際に行った実装を、
**人間・Test Agent・将来のLLMが後から再構成できる粒度**で保存する実装証跡ディレクトリである。

ここでは次の2種類の文書を扱う。

```text
implementation completion report
  = 1 Gate / 1 trialの実装結果を固定するtransaction record

implementation report detail
  = enhancement全体の累積実装状態を示すstate ledger
```

## 0.2. Requirement levels

### MUST
常に記載が必要。

### CONDITIONAL MUST
該当条件がある場合に必須。

### SHOULD
監査性・handoff品質・再現性向上のため推奨。

## 0.3. Common recording rules

### 0.3.1. Blank values

必須fieldを空欄にしない。

```text
N/A      : 概念上非該当
NONE     : 該当対象だが存在しない
UNKNOWN  : 取得を試みたが確定不能
NOT_RUN  : test等、予定されていたが未実行
```

### 0.3.2. Commits

commitは可能な限りfull SHA。

以下を区別する。

```text
baseline commit
  = enhancement基準点

starting commit
  = 当該trial開始時点

implementation commit
  = source/test/migration実装を固定したcommit

report commit
  = report文書追加/更新後のcommit
```

`implementation commit` と `report commit` を混同しない。

### 0.3.3. Paths

Repository内pathはrepository root相対path。

### 0.3.4. Facts vs interpretation

reportにはRepository上の観察事実を優先して記録する。

```text
Fact:
  src/x.py を追加
  endpoint /foo を実装
  migration abc123 を追加

Interpretation:
  architectureが改善された
  保守性が高まった
```

後者を記載する場合、前者と区別する。

### 0.3.5. Related identifier format

Implementation report自体はGate IDとTrial IDを使用する。
後続のTest / Audit evidenceでは以下を使用する。

```text
Trial ID      : 2-digit zero-padded decimal (01–99)
Test Item ID  : 3-digit zero-padded decimal (001–998)
Test Item 000 : reserved / do not use
Gate Decision : reserved Test Item ID 999
```

**Test Item IDは常に3桁で記録する。**

例:

```text
G3_01_implementation_completion_report.md
  ↓
G3_01_001_schema_contract.md
G3_01_002_leakage_rejection.md
G3_01_999_gate_decision.md
```

### 0.3.6. Test result boundary

Coding Agentが軽量self-checkを行う運用でも、
独立Gate判定とTest Agent evidenceをimplementation reportへ混在させない。

Coding Agent自身のself-checkは必要なら補足として記録するが、
Gate PASSの根拠にはしない。

---

# 1. implementation completion report

## 1.1. File naming

```text
[GATE]_[trial]_implementation_completion_report.md
```

例:

```text
G3_01_implementation_completion_report.md
G3_02_implementation_completion_report.md
```

### Naming rules

- `[GATE]`: Gate identifier
- `[trial]`: 2桁ゼロ埋め（01–99）
- extension: `.md`

## 1.2. Identifier rules

```text
Gate ID  : project-defined identifier
Trial ID : 2-digit zero-padded decimal (01–99)
```

Implementation Completion ReportではTrial IDを必ず2桁で記録する。

## 1.3. Purpose

Implementation Completion Reportは、
**当該Gate / trialでCoding Agentが何を変更し、どのcommitをTest Agentへ引き渡したか**
を固定するhandoff証跡である。

---

## 1.4. Contents

### 1.4.1. Must

```text
# {{GATE}} Trial {{TRIAL}} Implementation Completion Report

- Project: {{PROJECT_NAME:
  MUST.
  project正式名称。}}

- Enhancement: {{ENHANCE_ID:
  MUST.
  enhancement ID。}}

- Gate: {{GATE:
  MUST.
  filenameの[GATE]と一致。}}

- Trial: {{TRIAL:
  MUST.
  filenameの[trial]と一致する2桁番号。}}

- Status: {{STATUS:
  MUST.
  許容値は原則:
    READY_FOR_TEST
    DESIGN_BLOCKED
  READY_FOR_TEST:
    06で定義されたCoding completion conditionを満たし、
    Test Agentへ独立検証を引き渡せる。
  DESIGN_BLOCKED:
    06だけでは実装判断不能な仕様矛盾・設計不足を検出し停止した。
  Gate PASS/FAIL/BLOCKEDをここで判定しない。}}

- Branch: {{BRANCH:
  MUST.
  実装branch。}}

- Baseline commit: {{BASELINE_COMMIT:
  MUST.
  06で定義されたbaseline full SHA。}}

- Starting commit: {{STARTING_COMMIT:
  MUST.
  当該trial開始時のfull SHA。}}

- Implementation commit: {{IMPLEMENTATION_COMMIT:
  MUST for READY_FOR_TEST.
  Test Agentへ引き渡すsource/test/migration実装commitのfull SHA。
  DESIGN_BLOCKEDで実装commitを作らない場合は N/A。}}

- Report commit: {{REPORT_COMMIT:
  CONDITIONAL MUST.
  reportをcommitした場合のfull SHA。
  report作成時点で未commitなら UNKNOWN とし、
  後続運用で更新可能かをREADME/06規約に従う。}}

- Migration head: {{MIGRATION_HEAD:
  CONDITIONAL MUST.
  migration管理対象projectではimplementation commit時点のactual head。
  非該当なら N/A。}}

- Started at: {{STARTED_AT:
  MUST.
  timezone付きISO 8601。}}

- Finished at: {{FINISHED_AT:
  MUST.
  timezone付きISO 8601。}}

## 1. Input

- Implementation instruction: {{IMPLEMENTATION_INSTRUCTION_PATH:
  MUST.
  当該trialで使用した06のrepository-relative path。}}

- Previous Gate Decision report: {{PREVIOUS_GATE_DECISION_REPORT:
  CONDITIONAL MUST.
  FAIL後の修正trialでは入力となったprevious Gate Decision report path。
  初回trialでは N/A。}}

## 2. Scope Implemented

{{SCOPE_IMPLEMENTED:
  MUST.
  当該trialで実際に実装したscopeを、06のGate contractと対応づけて列挙する。
  「G3を実装した」だけでは不十分。
  capability、endpoint、schema、state transition、UI等の具体単位で記載する。}}

## 3. Files Changed

### Added
{{FILES_ADDED:
  MUST.
  added fileをrepository-relative pathで列挙。
  なしなら NONE。}}

### Modified
{{FILES_MODIFIED:
  MUST.
  modified fileをrepository-relative pathで列挙。
  なしなら NONE。}}

### Deleted
{{FILES_DELETED:
  MUST.
  deleted fileを列挙。
  なしなら NONE。
  destructive deletionがある場合はImplementation Detailsで理由を説明する。}}

## 4. Implementation Details

{{IMPLEMENTATION_DETAILS:
  MUST.
  主要変更ごとに以下を追えるよう記載する。
    - changed component
    - implemented behavior
    - 06のどのcontractに対応するか
    - important interface/schema/state transition
    - compatibility impact
  code全文を転載しない。
  「リファクタリングした」のような抽象記述だけにしない。}}

## 5. Automated Test Code Added / Changed

{{AUTOMATED_TEST_CODE_CHANGES:
  MUST.
  Coding Agentが追加・変更したautomated test codeをpath単位で列挙し、
  何の契約を検証するtestかを記載する。
  test code変更なしなら NONE。
  Test Agentの独立テスト実行結果はここへ書かない。}}

## 6. Migration

- Added migration: {{ADDED_MIGRATION:
  CONDITIONAL MUST.
  migration追加時はrevision/path。
  なしなら NONE / 非該当なら N/A。}}

- Previous head: {{PREVIOUS_MIGRATION_HEAD:
  CONDITIONAL MUST.
  migration変更時のprevious head。
  非該当なら N/A。}}

- New head: {{NEW_MIGRATION_HEAD:
  CONDITIONAL MUST.
  migration変更後のhead。
  非該当なら N/A。}}

- Destructive change: {{DESTRUCTIVE_CHANGE:
  CONDITIONAL MUST.
  destructive schema/data changeの有無と内容。
  ない場合は NONE。}}

- Data migration: {{DATA_MIGRATION:
  CONDITIONAL MUST.
  data migration有無と内容。
  ない場合は NONE / 非該当なら N/A。}}

## 7. Changes to Already-Passed Gates

{{CHANGES_TO_PASSED_GATES:
  MUST.
  PASS済みGate領域への変更がなければ NONE。
  ある場合は少なくとも:
    - affected Gate
    - changed file/component
    - why unavoidable
    - preserved contract
    - required regression
  を記載する。
  「影響なし」とだけ書かず、変更事実と分離する。}}

## 8. Known Limitations / Unresolved Items

{{KNOWN_LIMITATIONS:
  MUST.
  READY_FOR_TESTでも残るknown limitation、未解決事項、Test Agentへの注意点を列挙。
  なしなら NONE。
  DESIGN_BLOCKEDの場合はblock内容と重複してもよいが、実装上の未完了scopeを明確にする。}}

## 9. Out-of-Scope Work

{{OUT_OF_SCOPE_WORK:
  MUST.
  06で対象外とされた領域について、今回実装していないことを確認できるよう記載する。
  特にfuture-Gate draftや便乗refactorが存在する場合、その扱いを記録する。}}

## 10. Git Evidence

- `git rev-parse HEAD`: {{GIT_HEAD:
  MUST.
  report作成時点のactual HEAD。}}

- `git status --short`: {{GIT_STATUS_SHORT:
  MUST.
  report作成時点のworking tree状態。
  cleanなら CLEAN 等、定義した表現で明示。}}

- Diff stat: {{GIT_DIFF_STAT:
  MUST.
  starting commitからimplementation commitまでのdiff stat、
  または同等の変更量証拠。}}

## 11. Handoff to Test Agent

- Test target implementation commit: {{TEST_TARGET_IMPLEMENTATION_COMMIT:
  MUST for READY_FOR_TEST.
  Test Agentが固定すべきfull SHA。
  Implementation commitと一致すること。}}

- Active Gate: {{ACTIVE_GATE:
  MUST.
  Test Agentが判定すべきGate。}}

- Implementation report path: {{IMPLEMENTATION_REPORT_PATH:
  MUST.
  本report自身のrepository-relative path。}}

- Coding Agent test execution: {{CODING_AGENT_TEST_EXECUTION:
  MUST.
  原則 NOT_PERFORMED または self-checkのみの事実。
  Coding Agentが独立Gate testを実行したかのように見せない。}}

- Ready for independent test: {{READY_FOR_INDEPENDENT_TEST:
  MUST.
  YES / NO。
  Statusと整合すること。
  READY_FOR_TESTなら通常YES。
  DESIGN_BLOCKEDならNO。}}

## 12. Design Block

- Contradiction: {{DESIGN_BLOCK_CONTRADICTION:
  CONDITIONAL MUST for DESIGN_BLOCKED.
  06内の矛盾・不足を具体化。
  READY_FOR_TESTなら N/A。}}

- Observed facts: {{DESIGN_BLOCK_FACTS:
  CONDITIONAL MUST for DESIGN_BLOCKED.
  contradictionの根拠となる事実。}}

- Impact: {{DESIGN_BLOCK_IMPACT:
  CONDITIONAL MUST for DESIGN_BLOCKED.
  どのGate/contract/componentが判断不能か。}}

- Minimal choices: {{DESIGN_BLOCK_CHOICES:
  SHOULD for DESIGN_BLOCKED.
  作業指示者が決定できる最小選択肢。}}

- Decision required: {{DESIGN_BLOCK_DECISION_REQUIRED:
  CONDITIONAL MUST for DESIGN_BLOCKED.
  作業指示者に必要な具体決定。}}
```

---

### 1.4.2. Should

```text
## 13. Supplemental Implementation Evidence

- Key symbols / interfaces: {{KEY_SYMBOLS_INTERFACES:
  SHOULD.
  主要class/function/endpoint/schema名。}}

- Dependency changes: {{DEPENDENCY_CHANGES:
  SHOULD.
  package dependency変更がある場合のbefore/after。}}

- Self-check commands: {{SELF_CHECK_COMMANDS:
  SHOULD.
  Coding Agentが06で許可された軽量self-checkを実行した場合のexact commandと結果。
  Gate evidenceとは区別する。}}

- Risk notes: {{RISK_NOTES:
  SHOULD.
  Test Agentが重点監査すべきrisk。}}

- Related issue / PR: {{RELATED_REFERENCES:
  SHOULD.
  issue/PR/operator decision等。}}
```

---

# 2. implementation report detail

## 2.1. File naming

```text
{{ENHANCE_ID}}_implementation_report_detail.md
```

例:

```text
ENH-E3_implementation_report_detail.md
```

## 2.2. Purpose

Implementation Report Detailは、
**enhancement全体の累積状態を示すstate ledger**である。

trial単位の詳細証拠はImplementation Completion Reportへ保持し、
Detail Reportでは現在地点、Gate状態、trial履歴、未完了作業、evidence indexを集約する。

過去trialの事実を消して「最新状態だけ」にしない。

---

## 2.3. Contents

### 2.3.1. Must

```text
# {{PROJECT_NAME}} {{ENHANCE_ID}} Implementation Report Detail

## 1. Baseline

- Branch: {{BRANCH:
  MUST.
  enhancement対象branch。}}

- Baseline commit: {{BASELINE_COMMIT:
  MUST.
  enhancement基準full SHA。}}

- Initial migration head: {{INITIAL_MIGRATION_HEAD:
  CONDITIONAL MUST.
  migration管理対象なら開始時head。
  非該当なら N/A。}}

- Enhancement root: {{ENHANCE_ROOT:
  MUST.
  repository内enhancement root path。}}

## 2. Gate Status

| Gate | Status | Latest Trial | Implementation Commit | Gate Decision Report |
|---|---|---:|---|---|
{{GATE_STATUS_ROWS:
  MUST.
  Gateごとにcurrent statusを1行。
  Statusは06/07と同じ列挙値体系を使用する。
  Latest Trial:
    未着手なら N/A。
  Implementation Commit:
    latest READY_FOR_TEST/PASS対象commit。
  Gate Decision Report:
    PASS/FAIL/BLOCKED判定がある場合のlatest report path。
  PASS済みGateを後からIN_PROGRESSへ黙って戻さない。}}

## 3. Trial History

| Gate | Trial | Coding Status | Implementation Commit | Test Decision | Evidence |
|---|---:|---|---|---|---|
{{TRIAL_HISTORY_ROWS:
  MUST.
  実施済み全trialを時系列またはGate順で保持する。
  Coding Status:
    READY_FOR_TEST / DESIGN_BLOCKED等。
  Test Decision:
    PASS / FAIL / BLOCKED / NOT_TESTED。
  Evidence:
    implementation completion reportおよびGate Decision report path。
  過去FAIL trialを削除しない。}}

## 4. Current Working State

- Current active Gate: {{CURRENT_ACTIVE_GATE:
  MUST.
  現在作業対象Gate。
  enhancement完了済みなら COMPLETE 等、06規約に合わせる。}}

- Current HEAD: {{CURRENT_HEAD:
  MUST.
  report更新時点full SHA。}}

- Working tree: {{WORKING_TREE:
  MUST.
  clean/dirtyと主要uncommitted状態を要約。}}

- Migration head: {{MIGRATION_HEAD:
  CONDITIONAL MUST.
  actual current migration head。
  非該当なら N/A。}}

- Uncommitted implementation files: {{UNCOMMITTED_IMPLEMENTATION_FILES:
  MUST.
  なしなら NONE。}}

- Saved future-Gate drafts: {{FUTURE_GATE_DRAFTS:
  MUST.
  future-Gate draftを保存している場合path/扱い。
  なしなら NONE。}}

- Known environmental blocks: {{KNOWN_ENVIRONMENTAL_BLOCKS:
  MUST.
  current workに影響するenvironment/infrastructure block。
  なしなら NONE。}}

## 5. Completed Implementation

{{COMPLETED_IMPLEMENTATION:
  MUST.
  PASSまたは少なくともREADY_FOR_TESTまで到達した実装をGate単位で要約。
  詳細はcompletion reportへリンクする。
  「何が実装済みか」を人間が一目で理解できる粒度。}}

## 6. Outstanding Work

{{OUTSTANDING_WORK:
  MUST.
  Active Gateおよび後続Gateの未完了作業を列挙。
  completed項目と重複しない。
  unknownなものを推測で補完しない。}}

## 7. Cross-Gate Changes

{{CROSS_GATE_CHANGES:
  MUST.
  PASS済みGate領域へ後続Gate都合で変更した履歴。
  なしなら NONE。
  各変更についてaffected Gate / trial / commit / evidenceを追えるようにする。}}

## 8. Known Deviations

{{KNOWN_DEVIATIONS:
  MUST.
  06/07契約、予定architecture、migration plan等からの既知偏差。
  なしなら NONE。
  deviationを「仕様変更済み」と無断で正当化しない。}}

## 9. Evidence Index

{{EVIDENCE_INDEX:
  MUST.
  主要implementation completion report、Gate Decision report、migration evidence等への索引。
  trial履歴と整合させる。}}
```

---

### 2.3.2. Should

```text
## 10. Supplemental State

- Last updated at: {{LAST_UPDATED_AT:
  SHOULD.
  timezone付きISO 8601。}}

- Last updated by: {{LAST_UPDATED_BY:
  SHOULD.
  Coding Agent / operator等の識別。}}

- Current risk summary: {{CURRENT_RISK_SUMMARY:
  SHOULD.
  Active Gateに関する主要risk。}}

- Next expected handoff: {{NEXT_EXPECTED_HANDOFF:
  SHOULD.
  次に生成されるべきreportまたはAgent handoff。}}
```

---

# 3. Consistency rules

## 3.1. Completion Report -> Detail Report

trial終了時、Detail Reportへ最低限以下を反映する。

```text
Gate Status
Trial History
Current Working State
Completed Implementation / Outstanding Work
Evidence Index
```

Completion Reportの具体file/commitとDetail Reportが矛盾しないこと。

## 3.2. Implementation Commit -> Test Handoff

```text
Implementation Completion Report
  Implementation commit
        =
  Test target implementation commit
        =
Test Item Report
  Tested implementation commit
        =
Gate Decision Report
  Tested implementation commit
```

この一致が崩れた場合、Test Agentは07のcommit fixing rulesに従う。

## 3.3. FAIL rework

FAIL後の次trialでは:

```text
Previous Gate Decision Report
       ↓
next trial Implementation Completion Report / Input
```

を明示する。

どのfailureを修正対象としたか追跡可能にする。

---

# 4. Human implementation audit checklist

```text
Q1. enhancement baselineは何か？
Q2. このtrialはどのcommitから始まったか？
Q3. どのGateを実装したか？
Q4. 06のどのcontractを実装したか？
Q5. どのfileを追加・変更・削除したか？
Q6. migrationはどう変わったか？
Q7. PASS済みGateへ影響したか？
Q8. Test Agentへ渡したimplementation commitは何か？
Q9. known limitationは何か？
Q10. 過去trialを含む全履歴をDetail Reportから追えるか？
```
