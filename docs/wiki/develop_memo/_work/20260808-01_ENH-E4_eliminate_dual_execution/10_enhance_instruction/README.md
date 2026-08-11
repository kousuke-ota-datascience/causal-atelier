# 10_enhance_instruction — Agent Execution Contract Specification

# 0. common

## 0.1. Purpose

`10_enhance_instruction/` は、エンハンス実行時にCoding AgentおよびTest / Audit Agentへ渡す
**実行契約の唯一の正本**を保存する。

ここに置く06/07は、上位の背景資料・要件定義書・設計書をAgent自身に再探索させずに済むよう、
必要な差分仕様・制約・Acceptance Criteria・Gate運用を具体化した完成指示書である。

```text
00_enhance_background
        ↓ 作業設計者が差分を抽出・統合
10_enhance_instruction
        ↓
Agent execution
```

## 0.2. Requirement levels

### MUST

Agentが迷わず作業するため常に定義が必要。

### CONDITIONAL MUST

該当機能・Gate・architecture条件が存在する場合に必須。

### SHOULD

実装・テストの探索空間削減、監査性、handoff品質を高めるため推奨。

## 0.3. General rules

### 0.3.1. No unresolved meta variables

Agentへ渡す時点で、06/07内に未解決の `{{...}}` を残さない。

### 0.3.2. Self-contained execution contract

06/07だけでAgentが作業判断できる状態を目標とする。

背景資料、要件定義書、設計書、旧指示書を「必要に応じて参照」として残さない。

### 0.3.3. Explicit precedence

複数文書を参照可能にする例外を設ける場合、優先順位とoverride範囲を明記する。

### 0.3.4. Gate localization

Agentへ同時に考慮させるGateを必要最小限にする。

- PASS済みGate
- Active Gate
- 後続Gate

の状態を明示し、Active Gate以外の便乗実装を禁止する。

### 0.3.5. Identifier format

Gate / Trial / Test Itemの識別子は以下で統一する。

```text
Gate ID       : project-defined identifier (例: G1, G2, G3)
Trial ID      : 2-digit zero-padded decimal (01–99)
Test Item ID  : 3-digit zero-padded decimal (001–998)
Test Item 000 : reserved / do not use
Gate Decision : reserved Test Item ID 999
```

**Test Item IDは常に3桁で記録する。**
`1`、`01`、`item1` のような省略表記は使用しない。

例:

```text
G3_01_implementation_completion_report.md
G3_01_001_schema_contract.md
G3_01_002_leakage_rejection.md
G3_01_999_gate_decision.md
```

Trial IDとTest Item IDは桁数自体を構文上の識別に使用する。

### 0.3.6. Negative constraints

禁止事項は曖昧にせず、少なくとも以下を具体化する。

- 変更禁止領域
- 再設計禁止事項
- 次Gateへの先行着手禁止
- Test Agentによるsource modification禁止
- Coding AgentによるGate判定禁止

---

# 1. implementation instruction

## 1.1. File naming

```text
06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_実装指示書.md
```

例:

```text
06_Ariadne_ENH-E4_実装指示書.md
```

## 1.2. Purpose

06はCoding Agentが従う唯一の実装契約である。

06には少なくとも以下を含める。

- 現在地点
- Gate状態
- Active Gate
- 実装対象
- 実装禁止事項
- change boundary
- Gate別実装契約
- trial規約
- 完了条件
- required outputs
- stop condition

---

## 1.3. Contents

### 1.3.1. Must

```text
# {{PROJECT_NAME}} {{ENHANCE_ID}} 実装指示書

- Project: {{PROJECT_NAME:
  MUST.
  対象projectの正式名称。}}

- Enhancement: {{ENHANCE_ID:
  MUST.
  対象enhancement ID。
  例: ENH-E3}}

- Branch: {{BRANCH:
  MUST.
  Coding Agentが作業するbranch名。}}

- Baseline commit: {{BASELINE_COMMIT:
  MUST.
  enhancement開始時または再開時に基準とするfull commit SHA。
  current HEADと異なる場合、その関係をCurrent Stateで説明する。}}

- Active Gate: {{ACTIVE_GATE:
  MUST.
  Coding Agentが今回実装してよい唯一のGate。
  例: G3}}

- Migration head: {{MIGRATION_HEAD:
  CONDITIONAL MUST.
  DB migration管理対象projectでは、開始時点のexpected migration head。
  非該当なら N/A。}}

## 1. Source of Truth

{{CODING_SOURCE_OF_TRUTH:
  MUST.
  06自身が唯一の作業指示であることを明示する。
  Coding Agentが参照してよい情報源を列挙する。
  通常許可:
    - 本書
    - current source code
    - current automated test code
    - current migration
    - Git status/diff/log
    - 同一Gateの前trial Gate Decision report（FAIL修正時）
    - 自身のimplementation report
  通常禁止:
    - 旧実装指示書
    - 旧テスト指示書
    - 00_enhance_background
    - revised requirements snapshot
    - 上位要件定義書・設計書
  例外を許す場合は文書path・参照目的・優先順位を限定する。}}

## 2. Coding Agent Role

{{CODING_AGENT_ROLE:
  MUST.
  Coding Agentが実施する責務を列挙する。
  最低限:
    - Active Gateのproduction code実装
    - Active Gateに必要なautomated test code作成/修正
    - 必要なmigration作成
    - 必要なschema/API/domain/persistence/UI整合
    - implementation commit作成
    - implementation completion report作成
    - implementation report detail更新
    - READY_FOR_TESTで停止
  「必要に応じて設計を見直す」等の広い裁量を与えない。}}

## 3. Prohibited Work

{{CODING_PROHIBITIONS:
  MUST.
  Coding Agentに禁止する作業を明示する。
  最低限検討:
    - Gate判定
    - 独立監査
    - 本格E2E
    - scientific benchmark
    - 上位設計の再探索
    - product architecture再設計
    - Active Gate外の便乗refactor
    - PASS済みGateの再設計
    - 次Gateへの先行着手
    - skip/xfail追加による回避
    - assertion緩和
    - failing test削除
    - git add .
  project固有の禁止事項を追加する。}}

## 4. Current State

{{CURRENT_STATE:
  MUST.
  Agent再開時点の事実を記載する。
  最低限:
    - current HEAD
    - working tree clean/dirty
    - uncommitted implementation files
    - future-Gate draftの有無
    - current migration head
    - 既知の環境block
    - 前Gateまでの確定状態
  「途中まで実装済み」のような曖昧記述だけにしない。}}

## 5. Gate Status

{{GATE_TABLE:
  MUST.
  全Gateまたは少なくともPASS済み/Active/後続Gateを表形式で示す。
  推奨列:
    - Gate
    - Purpose
    - Status
    - Latest Trial
    - Evidence
  Statusの許容値を06内で固定する。
  例:
    NOT_STARTED
    IN_PROGRESS
    READY_FOR_TEST
    PASS
    FAIL
    BLOCKED
    DESIGN_BLOCKED
  Active Gateと表の状態が矛盾しないこと。}}

## 6. Trial Rules

{{TRIAL_RULES:
  MUST.
  trial numberingと再実装規約を定義する。
  最低限:
    - 2桁ゼロ埋め
    - 同一trial番号を再利用しない
    - FAIL後は同一Gateの次trial
    - PASS後のみ次Gateへ進める
    - BLOCKED時にproduct code変更で迂回しない
    - 1 Coding execution = 1 Gate / 1 trial
  既存trialから再開する場合はnext trialを具体的に示す。}}

## 7. Gate Implementation Contracts

{{GATE_IMPLEMENTATION_CONTRACTS:
  MUST.
  Active Gateの実装を、Coding Agentが設計判断せず実装できる粒度で定義する。
  各Gateについて最低限:
    - Purpose
    - In scope
    - Out of scope
    - Input contract
    - Output contract
    - State transition
    - API/schema/domain contract
    - Persistence contract
    - UI contract（該当時）
    - migration contract（該当時）
    - scientific/statistical/analytical invariant（該当時）
    - rejection/failure conditions
    - backward compatibility policy
    - implementation completion criteria
  sequencingが重要ならstage順序を固定する。
  例:
    SPLIT -> PREPARE -> TRAIN -> EVALUATE -> EXPLAIN
  禁止partition/access等がある場合は構造契約として明記する。}}

## 8. Allowed / Forbidden Change Areas

{{CHANGE_BOUNDARIES:
  MUST.
  変更可能領域と変更禁止領域をpathまたはcomponent単位で具体化する。
  最低限:
    - allowed directories/files
    - conditionally allowed directories/files
    - forbidden directories/files
    - PASS済みGate領域を変更できる条件
    - future-Gate draftの扱い
  「必要な範囲のみ変更」のような抽象表現だけにしない。}}

## 9. Completion Conditions

{{IMPLEMENTATION_COMPLETION_CRITERIA:
  MUST.
  Coding AgentがREADY_FOR_TESTへ移行できる条件。
  実装上の完了条件であり、Test AgentによるPASSとは区別する。
  例:
    - Active Gate契約の実装が完了
    - required automated test codeが追加済み
    - required migrationが追加済み
    - forbidden scopeへ変更していない
    - implementation commit作成済み
    - report作成済み
  Coding Agent自身のfull test passを必須にするか否かも明示する。}}

## 10. Required Outputs

{{IMPLEMENTATION_OUTPUTS:
  MUST.
  Coding Agentが生成・更新する成果物をpathと命名規則まで具体化する。
  最低限:
    - implementation commit
    - 20_implementation_reports/[GATE]_[trial]_implementation_completion_report.md
    - 20_implementation_reports/{{ENHANCE_ID}}_implementation_report_detail.md
  report template pathも指定する。
  source code以外の不要な文書生成を要求しない。}}

## 11. Stop Conditions

{{CODING_STOP_CONDITIONS:
  MUST.
  Coding Agentが停止すべき条件を定義する。
  最低限:
    - READY_FOR_TEST
    - DESIGN_BLOCKED
    - current Gate以外へ進む前
  DESIGN_BLOCKED時にreportへ何を残すかを明示する。
  Coding AgentがそのままTest Agent作業を開始しないことを明示する。}}
```

---

### 1.3.2. Should

```text
## Supplemental Implementation Context

- Target architecture summary: {{TARGET_ARCHITECTURE_SUMMARY:
  SHOULD.
  Active Gateに直接関係するarchitectureだけを簡潔に要約する。}}

- Dependency / package constraints: {{DEPENDENCY_CONSTRAINTS:
  SHOULD.
  新規dependency禁止、version固定、許可package等。}}

- Performance constraints: {{PERFORMANCE_CONSTRAINTS:
  SHOULD.
  Active Gateに性能要件がある場合のthreshold。}}

- Security / privacy constraints: {{SECURITY_PRIVACY_CONSTRAINTS:
  SHOULD.
  Active Gateにsecurity/privacy契約がある場合。}}

- Known non-goals: {{KNOWN_NON_GOALS:
  SHOULD.
  Agentが「ついでに改善」しそうな領域を明示する。}}
```

---

# 2. test / audit instruction

## 2.1. File naming

```text
07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_テスト指示書.md
```

## 2.2. Purpose

07はTest / Audit Agentが従う唯一のテスト・監査契約である。

Test Agentへは07に加え、作業指示者が
**今回対象の具体的なimplementation completion report path**を外側プロンプトで指定する。

---

## 2.3. Contents

### 2.3.1. Must

```text
# {{PROJECT_NAME}} {{ENHANCE_ID}} テスト・監査指示書

- Project: {{PROJECT_NAME:
  MUST.
  対象project正式名称。}}

- Enhancement: {{ENHANCE_ID:
  MUST.
  enhancement ID。}}

- Branch: {{BRANCH:
  MUST.
  検証対象branch。}}

- Active Gate: {{ACTIVE_GATE:
  MUST.
  Test Agentが今回判定する唯一のGate。}}

## 1. Source of Truth

{{TEST_SOURCE_OF_TRUTH:
  MUST.
  07自身が唯一のテスト・監査指示であることを明示する。
  通常許可:
    - 本書
    - 作業指示者が指定したimplementation completion report
    - 対象source/test/migration
    - Git status/diff/log
    - 過去test report（履歴確認目的のみ）
    - 実行生成evidence
  通常禁止:
    - 06実装指示書
    - 旧07
    - 00 background
    - revised requirements snapshot
    - 上位設計書
  Test Agent自身にAcceptance Criteriaを再設計させない。}}

## 2. Test / Audit Agent Role

{{TEST_AGENT_ROLE:
  MUST.
  Test Agentの責務を列挙する。
  最低限:
    - implementation commit固定
    - required test実行
    - architecture/schema/static監査
    - integration/migration/scientific/E2E等の必要試験
    - exact command記録
    - test item report作成
    - Gate Decision作成
    - PASS/FAIL/BLOCKED判定
  source修正は責務に含めない。}}

## 3. Prohibited Work

{{TEST_PROHIBITIONS:
  MUST.
  最低限:
    - production code変更
    - automated test code変更
    - migration変更
    - dependency変更
    - formatterによるsource書換え
    - bug fix
    - assertion緩和
    - skip/xfail追加
    - failing test削除
    - product design再設計
    - Coding Agent report改竄
    - FAIL/BLOCKED Gateを越えた次Gate監査
  read-only inspection用temporary scriptを許可する場合は場所を限定する。}}

## 4. Gate Decision Rules

{{GATE_DECISION_RULES:
  MUST.
  Gate Statusの許容値と条件を定義する。
  通常:
    PASS
    FAIL
    BLOCKED
  PASS:
    当該trialに要求された全MUST test itemが完了しAcceptance Criteriaを満たす。
  FAIL:
    implementation/test coverageにGate通過不能な欠陥がある。
  BLOCKED:
    environment/infrastructure等によりimplementation defectか判断不能。
  partial pass等の独自状態を禁止する。}}

## 5. Trial Rules

{{TEST_TRIAL_RULES:
  MUST.
  最低限:
    - 2桁trial
    - current trialだけを判定
    - 過去trialのPASSを寄せ集めない
    - deterministic product failureを無意味に再実行しない
    - transient environment failure再試行回数
    - retry理由と初回結果を証跡化
    - user interruption/timeout時の扱い
  PASSを宣言するtrialでは全MUST項目を完走する。}}

## 6. Implementation Commit Fixing Rules

{{IMPLEMENTATION_COMMIT_RULES:
  MUST.
  implementation completion reportに記載されたimplementation commitを
  test targetとして固定する規則。
  最低限:
    - full SHA記録
    - handoff後にsourceが変わっていないことの確認方法
    - report-only commitをcurrent HEADでtestしてよい条件
    - source差分がある場合のBLOCKED条件
    - test item report間で同一commitを使用すること
  「最新HEADをテスト」など曖昧な運用を禁止する。}}

## 7. Test Execution Order

{{TEST_EXECUTION_ORDER:
  MUST.
  fail-fastの実行順序を具体化する。
  例:
    1. static/architecture/schema
    2. unit/contract
    3. targeted integration
    4. migration/database
    5. scientific/analytical benchmark
    6. full regression
    7. browser/UI E2E
    8. Gate Decision
  Gate固有で不要な層を明示する。
  blocking failure後に継続する/停止する条件も定義する。}}

## 8. Gate Test Plans

{{GATE_TEST_PLANS:
  MUST.
  Active Gateのtest item一覧をitem番号単位で定義する。
  各itemについて最低限:
    - item number
      - Test Item IDは3-digit zero-padded decimal
      - allowed range: 001–998
      - 000はreserved / do not use
      - 999はGate Decision専用でtest itemとして使用しない
    - report filename
    - purpose
    - Acceptance Criteria
    - test type
    - target component
    - required commandまたはcommand導出規則
    - PASS condition
    - FAIL condition
    - BLOCKED condition
    - regression scope
    - scientific/analytical invariant（該当時）
    - evidence requirement
  Test Agentに「何をテストすべきか」を設計させない。}}

## 9. Evidence Requirements

{{TEST_EVIDENCE_REQUIREMENTS:
  MUST.
  30_test_report READMEに従うことを明示し、
  最低限:
    - tested commit
    - working directory
    - environment
    - exact commands
    - exit code
    - test counts
    - logs
    - reproduction procedure
    - Gate evidence mapping
  を要求する。
  commandはコピー&ペースト可能な完全形とする。}}

## 10. Completion Conditions

{{TEST_COMPLETION_CRITERIA:
  MUST.
  Test AgentがGate Decisionを確定できる条件。
  PASS/FAIL/BLOCKEDごとに必要なevidence completionを定義する。
  PASS時:
    - 全MUST item report存在
    - 全criterion satisfied
    - regression/scientific/E2E等の必須項目完了
  FAIL時:
    - 少なくとも1つの具体的failure evidence
  BLOCKED時:
    - block原因と影響itemの証跡
  を最低限含める。}}

## 11. Required Outputs

{{TEST_OUTPUTS:
  MUST.
  出力path・命名規則を明記する。
  最低限:
    - 30_test_report/[GATE]_[trial:2-digit]_[item:3-digit]_[test_name].md
    - 30_test_report/[GATE]_[trial:2-digit]_999_gate_decision.md
  Test Item IDは常に3桁（001–998）とし、000は予約、999はGate Decision専用とする。
  使用template pathも示す。}}

## 12. Stop Conditions

{{TEST_STOP_CONDITIONS:
  MUST.
  Gate Decision report作成後に停止することを明示する。
  PASSでもTest Agent自身が次Gateへ進まない。
  FAILでもTest Agent自身が修正実装しない。
  BLOCKEDでもproduct codeを変更して回避しない。}}
```

---

### 2.3.2. Should

```text
## Supplemental Test Context

- Expected environment matrix: {{EXPECTED_ENVIRONMENT_MATRIX:
  SHOULD.
  複数runtime/browser/DB versionを要求する場合のmatrix。}}

- Performance test policy: {{PERFORMANCE_TEST_POLICY:
  SHOULD.
  性能Gateがある場合のwarm-up、回数、threshold、ノイズ扱い。}}

- Stochastic test policy: {{STOCHASTIC_TEST_POLICY:
  SHOULD.
  seed、repeat count、confidence interval、failure threshold等。}}

- Artifact retention policy: {{ARTIFACT_RETENTION_POLICY:
  SHOULD.
  screenshot/log/coverage/benchmark artifactの保存先・保持期間。}}

- Known flaky tests: {{KNOWN_FLAKY_TESTS:
  SHOULD.
  既知flaky testが存在する場合、retry許容条件を明確化する。
  flakyだからPASS扱い、は不可。}}
```

---

# 3. Cross-document consistency

## 3.1. 06 -> 20

06の以下がimplementation reportへ追跡できること。

```text
Gate contract
  ↓
implemented scope
  ↓
changed files
  ↓
implementation commit
```

## 3.2. 07 -> 30

07の以下がtest evidenceへ追跡できること。

```text
Gate Acceptance Criteria
  ↓
test item
  ↓
exact command
  ↓
actual result
  ↓
Gate Decision
```

## 3.3. 06 and 07 alignment

06と07で以下が一致すること。

- Project
- Enhancement
- Branch
- Gate definition
- Active Gate
- trial numbering
- Acceptance boundary
- implementation report naming
- Gate progression rules

06にない要件を07で突然追加しない。
07にないテスト責務をTest Agentへ暗黙要求しない。

---

# 4. Authoring checklist

Agentへ06/07を渡す前に、人間または作業設計LLMが以下を確認する。

```text
[ ] 未解決{{...}}がない
[ ] 旧文書参照が残っていない
[ ] Active Gateが一意
[ ] Gate StatusとCurrent Stateが矛盾しない
[ ] change boundaryが具体的
[ ] Coding Agentの禁止事項が明確
[ ] Test Agentの禁止事項が明確
[ ] implementation contractが設計判断不要な粒度
[ ] test planがテスト設計不要な粒度
[ ] PASS/FAIL/BLOCKED条件が明確
[ ] required report pathが具体的
[ ] Coding AgentとTest Agentの責務が混ざっていない
```
---

# 5. Addendum

## Gate-localized execution contract policy

ENH-E4以降、本Enhanceの06/07はGate単位で管理する。

```text
10_enhance_instruction/
├── README.md
├── 06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_実装指示書.md
├── 07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_テスト指示書.md
├── G02/
│   ├── 06_Ariadne_ENH-E4_実装指示書.md
│   └── 07_Ariadne_ENH-E4_テスト指示書.md
├── G03/
│   ├── 06_Ariadne_ENH-E4_実装指示書.md
│   └── 07_Ariadne_ENH-E4_テスト指示書.md
...
└── G08/
    ├── 06_Ariadne_ENH-E4_実装指示書.md
    └── 07_Ariadne_ENH-E4_テスト指示書.md
```

### Contract authority

root直下の

```text
06_{{PROJECT_NAME}}_{{ENHANCE_ID}}_実装指示書.md
07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_テスト指示書.md
```

はauthoring templateであり、Coding Agent / Test Agentへ直接渡す実行契約ではない。

実際のAgent executionでは、Active Gate directory配下の06/07だけを正本とする。

例:

```text
Active Gate = E4-G02

Coding Agent Source of Truth:
10_enhance_instruction/G02/06_Ariadne_ENH-E4_実装指示書.md

Test / Audit Agent Source of Truth:
10_enhance_instruction/G02/07_Ariadne_ENH-E4_テスト指示書.md
```

### Gate isolation

一回のAgent executionで扱ってよいGateは一つだけとする。

```text
PASS済みGate
    = immutable baselineとして扱う

Active Gate
    = 今回変更・検証してよい唯一のGate

Future Gate
    = implementation / testへの先行着手禁止
```

後続Gateの最終architectureを知っていることは、Active Gateを越境して先行実装してよい理由にはならない。

temporary coexistenceまたはtransition debtがGate decompositionで明示されている場合、Active Gateではそのtemporary stateを契約どおり維持する。

### Gate contract immutability

GateがPASSした後、そのGateの06/07は原則として変更しない。

後続GateでPASS済みGateのcontract自体に問題が見つかった場合は、既存06/07をsilent rewriteせず、

* affected Gate
* conflict
* reason
* approved correction
* required regression

を新しいdecision evidenceとして記録する。

### Report localization

Implementation / Test evidenceはGate IDとTrial IDで対応付ける。

```text
20_implementation_reports/
E4-G02_01_implementation_completion_report.md

30_test_report/
E4-G02_01_001_*.md
E4-G02_01_002_*.md
...
E4-G02_01_999_gate_decision.md
```

Trial IDは2桁、Test Item IDは3桁とする。

`999` はGate Decision専用であり、通常Test Itemには使用しない。

### Gate progression

```text
Gate N / Coding Trial
        ↓
READY_FOR_TEST
        ↓
Gate N / Independent Test Trial
        ↓
PASS
        ↓
Gate N+1 contract authoring / execution
```

FAILの場合は同一Gateの次Trialへ進む。

BLOCKEDの場合、別Gateのimplementationで迂回してはならない。

PASSしていないGateを前提として次Gateへ進んではならない。
