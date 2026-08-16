# ENH-E7 Handoff — Workflow Execution / G01 Work Package Readiness

## 0. このhandoffの目的

別チャットで ENH-E7 の workflow execution を継続するための引き継ぎ。

対象 Enhancement:

```text
Project: Ariadne
Enhancement: ENH-E7
Branch: feature/ariadne_mvp_e7
Remote: causal-atelier
Work root:
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation
```

基準断面:

```text
Baseline full SHA:
1beea1c9eb3ffa5d01f7c266b826e52136d01e8f
```

ENH-E6 upstream protected evidence:

```text
ENH-E6 G01 PASS Fixed Trial Candidate:
575cdd139aea09d4f19b46ab6a6d38545f645c71
```

---

# 1. ENH-E7 Product / IA baseline

ENH-E7 の target IA は以下で固定。

```text
Projects
│
├─ Project List / Register
│
└─ Selected Project
     │
     ├─ Project Management
     │    ├─ Overview / Project Info
     │    ├─ Research Context
     │    ├─ Data
     │    └─ Results / Lineage
     │
     └─ Analysis Workspace
          ├─ Analysis Context
          │    ├─ Current Project
          │    ├─ Active Research Context
          │    ├─ Dataset Version
          │    └─ Analysis View
          │
          ├─ Exploratory
          ├─ Causal
          └─ Predictive
```

Responsibility boundary:

```text
Project Management
    = Project resource を管理する場所

Analysis Workspace
    = Project context の下で分析する場所

Family
    = Analysis paradigm

Stage
    = Family 内の workflow / presentation view

Operation
    = Stage 内の処理
```

Canonical Project routes:

```text
/projects
/projects/new
/projects/{project_id}/overview
/projects/{project_id}/context
/projects/{project_id}/data
/projects/{project_id}/results
```

Short route:

```text
/projects/{project_id}
```

は:

```text
/projects/{project_id}/overview
```

へ normalize。

Canonical Analysis route は ENH-E6 contract を維持:

```text
/projects/{project_id}/analysis/{family}/{stage}
```

---

# 2. Gate構成

2 Gate構成を維持。

## G01 — Project Management Surface Contract

Work Packages:

```text
P01 Project Navigation Authority
P02 Projects / New Project Surface
P03 Overview / Project Lifecycle
P04 Research Context Surface
P05 Data / Analysis View Surface
P06 Results / Lineage Surface
P07 Project Integration / Regression
```

Dependency概略:

```text
P01
├─ P02
│  └─ P03
│     ├─ P04
│     ├─ P05
│     └─ P06
└───────────────┐
                ↓
               P07
```

## G02 — Analysis Workspace Contract

Work Packages:

```text
P01 Analysis Shell / Analysis Context
P02 Project <-> Analysis Routing
P03 Causal Stage Surface Migration
P04 Exploratory Stage Surface Migration
P05 Predictive Stage Surface Migration
P06 Legacy Cutover / Integration / Regression
```

G02 は G01 final PASS 後。

---

# 3. Workflow execution policy

Coding Agent の normative workflow contract:

```text
Enhancement-specific operator prompt
    +
assigned Pxx only
```

Coding Agent は仕様補完目的で以下を読まない。

```text
Gate 06
Gate 07
P00
other Pxx
00 background
20 reports
30 reports
previous Enhancement workflow artifacts
ADR / issue / external Web
```

source / tests / config / migrations は implementation substrate として調査可能。

重要:

```text
PACKAGE_COMPLETE
    != READY_FOR_TEST
    != Gate PASS
```

Gate PASS authority は Independent Verification の:

```text
999 Gate Decision
```

のみ。

---

# 4. Language / runtime policy

以下配下の Markdown は日本語主体。

```text
00_enhance_background
10_enhance_instruction
```

technical term / identifier / route / status token は英語維持可。

Python command は全workflowで:

```text
python3
```

をcanonicalとする。

`python` command は使用しない。

---

# 5. Execution identity / approval state

Human により以下は承認済み。

```text
REMOTE_NAME=causal-atelier
BRANCH_NAME=feature/ariadne_mvp_e7
BASELINE_FULL_SHA=1beea1c9eb3ffa5d01f7c266b826e52136d01e8f
```

Architecture Review:

```text
APPROVED
```

G01 Gate contract:

```text
G01 06 = FROZEN
G01 07 = FROZEN
```

G01 P01:

```text
READY_TO_EXECUTE
```

G02-specific:

```text
Data Quality / TIME_TREND / CHART
```

の最終配置は G02 freeze 前の source confirmation に defer。

これは G01/P01 blocker ではない。

---

# 6. Preflight policy

Canonical command:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . \
  --gate G01 \
  --package P01 \
  --trial 01
```

主な check:

```text
PRE-01 prompts exists
PRE-02 unresolved placeholders == 0
PRE-03 WORK_ROOT exists
PRE-04 root identity
PRE-05 assigned Pxx exactly one
PRE-06 prompt information isolation
PRE-07 Pxx self-contained / information isolation
PRE-08 GATE_ID
PRE-09 PACKAGE_ID
PRE-10 TRIAL_NO
PRE-11 branch
PRE-12 remote
PRE-13 Architecture Review approved
PRE-14 Gate 06/07 frozen
PRE-15 Pxx executable status
PRE-16 Pxx reporting contract
```

PRE-02:

```text
00_enhance_background/provenance/
Enhancement root直下の _work/
```

は placeholder scan 対象外。

PRE-07 は自然言語完全一致ではなく固定metadataを使用。

```text
**Self-containment:** MUST
**Information isolation:** MUST
```

PRE-16 は Pxx 内に self-contained reporting contract があることを要求。

---

# 7. 発生した問題 1 — P01 reporting contract ambiguity

G01/P01 を実行したところ、Agentは実装・focused verificationまで進んだ。

一度目の報告:

```text
PACKAGE_BLOCKED_CONTRACT_AMBIGUITY
```

理由:

```text
P01 §9 が
- implementation checkpoint report
- package execution status report
を要求するが、
保存先・filename・必須内容がP01内にない。
```

Agentは information isolation rule により 20-layer template 等から補完できず停止。

これは正しい停止。

---

# 8. v0.05で意図した修正

v0.05 では全13 Pxxに以下を追加する設計にした。

```text
**Reporting contract:** SELF_CONTAINED
```

各Pxx内で以下を完全定義する方針。

## Package Execution Status Report

Canonical path:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/packages/
ENH-E7_<GATE_ID>_<PACKAGE_ID>_Trial<TRIAL_NO>_package_execution_status.md
```

## Implementation Checkpoint Report

Canonical path:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/packages/
ENH-E7_<GATE_ID>_<PACKAGE_ID>_Trial<TRIAL_NO>_implementation_checkpoint_report.md
```

また、SHA自己参照を避けるため順序を固定。

```text
candidate-affecting implementation
    ↓
focused verification
    ↓
implementation commit
    ↓
Implementation checkpoint full SHA freeze
    ↓
report作成
    ↓
evidence-only report commit
```

report自身のcommit SHAをreport本文へ自己記録しない。

Candidate Assembly / Gate 07 についても同様に canonical output path / filename / required content を self-contained化する方針。

---

# 9. 重要な現状問題 — v0.05修正先が正規rootではない可能性

G01/P01 を再実行したが、Agentは再び:

```text
PACKAGE_BLOCKED_CONTRACT_AMBIGUITY
```

となった。

Agentが確認した正規P01:

```text
docs/wiki/develop_memo/_work/
20260813_ENH-E7_project_analysis_workspace_separation/
10_enhance_instruction/G01/
06_G01_P01_project_navigation_authority.md
```

には、依然として以下の抽象記述しかなかった。

```text
implementation checkpoint reportと
package execution status reportを作成する。
```

一方、以下にも同名fileが存在。

```text
docs/wiki/develop_memo/_work/
20260813_ENH-E7_project_analysis_workspace_separation/
_work/
20260813_ENH-E7_project_analysis_workspace_separation/
10_enhance_instruction/G01/
06_G01_P01_project_navigation_authority.md
```

したがって、**v0.05 patchが正規work rootではなく `_work/` 配下のcopyへ反映された可能性が高い。**

これは最優先で修正すること。

## 次チャットで必ず確認すること

実repositoryで:

```bash
git status --short

find docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation \
  -path '*/10_enhance_instruction/G01/06_G01_P01_project_navigation_authority.md' \
  -print

sed -n '1,220p' \
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/10_enhance_instruction/G01/06_G01_P01_project_navigation_authority.md

sed -n '1,220p' \
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/_work/20260813_ENH-E7_project_analysis_workspace_separation/10_enhance_instruction/G01/06_G01_P01_project_navigation_authority.md
```

正規root側に以下が存在するか確認。

```text
**Reporting contract:** SELF_CONTAINED

## 9. Reporting artifact contract

Canonical保存先 / filename

Package Execution Status Report

Implementation Checkpoint Report

Commit / SHA順序
```

存在しなければ、nested `_work/` copyの正しい修正を**正規rootへ反映**する。

---

# 10. nested `_work/` について

Enhancement root直下に:

```text
_work/
```

が存在している。

これは execution contract authorityではない。

preflight PRE-02からは除外済み。

ただし、今回のようにpatch先を誤る原因になるため、次チャットでは以下を検討する。

### 推奨

nested `_work/` が不要なartifact copyなら削除する。

ただし削除前に:

```bash
git status
git ls-files
diff -ru
```

等で、正規rootに未反映の有効修正がないか確認する。

**正規 authorityは常に:**

```text
docs/wiki/develop_memo/_work/
20260813_ENH-E7_project_analysis_workspace_separation/
```

直下。

---

# 11. P01 現在の実装状態

Agent報告ではP01 implementationは一度完了している。

実装済み（当時未commit）:

```text
frontend/navigation_state.js
frontend/app.js
tests/product/test_enh_e7_g01_p01_project_navigation_authority.py
```

内容:

- `ProjectNavigation`追加
- `/projects`
- `/projects/new`
- `/projects/<id>/overview|context|data|results`
  parse / serialize
- `/projects/<id>` → `/overview`
  replaceState normalization
- Project select / create / archive後のhistory transition
- focused test追加

検証履歴:

最初の実行:

```text
8 passed in 2.37s
node --check PASS
git diff --check PASS
```

後の再実行:

```text
Preflight PASS
P01 focused test: 2 passed
JavaScript syntax PASS
diff whitespace PASS
```

ただしreport contract ambiguityにより:

```text
Implementation checkpoint SHA freeze
report作成
PACKAGE_COMPLETE
```

までは到達していない。

**formal Gate FAILではない。Trialは01のまま。**

---

# 12. P02で発生した問題

HumanがG01/P02/Trial01を開始しようとした。

実行:

```text
GATE_ID=G01
PACKAGE_ID=P02
TRIAL_NO=01
```

preflight結果:

```text
PRE-01〜PRE-14: PASS
PRE-15 Pxx executable status: FAIL
```

P02:

```text
06_G01_P02_projects_new_project_surface.md
```

が:

```text
READY_TO_EXECUTE
```

ではないため `BLOCKED_PRECHECK`。

これはworkflow設計上は正しい。

---

# 13. P02をREADY_TO_EXECUTEにするタイミング

G01 package dependency上:

```text
P02 depends on P01
```

したがって、P01がまだ:

```text
PACKAGE_COMPLETE
```

になっていない現状でP02をREADY_TO_EXECUTEへ昇格させてはいけない。

正しい順序:

```text
1. 正規P01へv0.05 reporting contractを反映
2. G01/P01/Trial01を再開
3. implementation checkpoint SHA固定
4. 2 report作成
5. P01 = PACKAGE_COMPLETE
6. P01 completion evidenceをHuman/operatorが確認
7. G01 P02 を READY_TO_EXECUTEへ昇格
8. P02 preflight PASS
9. P02開始
```

P02 PRE-15 FAILは現時点では修正対象ではなく、**dependency gateとして意図したblock**。

---

# 14. 次チャットの最優先タスク

## Task 1 — 正規work rootへのreporting contract反映確認

全13 Pxxについて正規root側を監査。

```text
G01 P01-P07
G02 P01-P06
```

最低限以下を確認。

```text
**Self-containment:** MUST
**Information isolation:** MUST
**Reporting contract:** SELF_CONTAINED
```

さらに§9で:

```text
canonical report path
canonical filename
required content
Commit / SHA順序
```

が定義されていること。

nested `_work/` copyだけにある場合は正規rootへ移す。

---

## Task 2 — Candidate Assembly / 07も正規root確認

以下もnested copyだけにpatchされていないか確認。

```text
40_operator_workflows/agent_entry_prompts/
20_candidate_assembly_01_work_package_candidate_assembly_agent_prompt.md

10_enhance_instruction/G01/
07_Ariadne_ENH-E7_G01_test_instruction.md

10_enhance_instruction/G02/
07_Ariadne_ENH-E7_G02_test_instruction.md

40_operator_workflows/agent_entry_prompts/
30_independent_verification_01_test_agent_prompt.md
```

必要なself-contained artifact contract:

### Candidate Assembly

```text
20_implementation_reports/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_implementation_completion_report.md

20_implementation_reports/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_implementation_report_detail.md
```

### Test Item report

```text
30_test_report/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_<TEST_ID>_<TEST_NAME>.md
```

### Gate Decision

```text
30_test_report/<GATE>/Trial<TRIAL>/
ENH-E7_<GATE>_Trial<TRIAL>_999_gate_decision.md
```

---

## Task 3 — preflight PRE-16正規root確認

正規:

```text
40_operator_workflows/preflight/check_agent_execution_readiness.py
```

に:

```text
PRE-16 Pxx reporting contract
```

が実装されていること。

PRE-16で最低限:

```text
**Reporting contract:** SELF_CONTAINED
20_implementation_reports/
_package_execution_status.md
_implementation_checkpoint_report.md
Commit / SHA順序
```

を検査。

---

## Task 4 — P01再開

正規P01修正後:

```text
GATE_ID=G01
PACKAGE_ID=P01
TRIAL_NO=01
```

を同一Trialで再開。

formal FAILではないのでTrial02へ進めない。

P01が `PACKAGE_COMPLETE` になるまでP02をunlockしない。

---

## Task 5 — P01完了後にP02 unlock

P01 completion evidence確認後、正規:

```text
10_enhance_instruction/G01/
06_G01_P02_projects_new_project_surface.md
```

の:

```text
**Status at issuance:** DRAFT_NOT_FROZEN
```

を:

```text
**Status at issuance:** READY_TO_EXECUTE
```

へ変更する。

その後:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . \
  --gate G01 \
  --package P02 \
  --trial 01
```

を実行。

PASS後にP02 Coding Agentを開始。

---

# 15. workflow version履歴

これまで配布したzip:

```text
v0.01
- 日本語基本言語ポリシー前の初期instance

v0.02
- remote / baseline
- Architecture Review APPROVED
- G01 06/07 FROZEN
- G01 P01 READY_TO_EXECUTE

v0.03
- python command → python3

v0.04
- PRE-02 _work除外
- PRE-07 fixed metadata化
- **Information isolation:** MUST

v0.05
- intended:
  - 全13 Pxx reporting self-contained
  - PRE-16
  - Candidate Assembly output contract
  - Test Agent / Gate07 output contract
```

ただし **v0.05の修正が実repository正規rootではなくnested `_work/` copyへ入った可能性が高い**。

次チャットでは「zipを再生成する」より先に、**actual repository上の正規pathとnested copyを比較して正規authorityを修復すること。**

---

# 16. やってはいけないこと

- P01未完了のままP02を強制的にREADY_TO_EXECUTEへする。
- P02 PRE-15を単なるbugとして無条件解除する。
- nested `_work/` copyをnormative contractとしてAgentに読ませる。
- Coding Agentに20-layer templateを読ませてreport仕様を補完させる。
- `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`をformal Gate FAILとしてTrial02へ進める。
- reporting contractの不足をAgentの推測で埋める。
- checkpoint SHAとreport commit SHAを同一identityとして自己参照させる。
- `python` commandへ戻す。

---

# 17. 次チャット開始時の推奨依頼文

以下をそのまま使用可能。

```text
ENH-E7 handoffに基づき作業を継続せよ。

最優先でactual repository上の

docs/wiki/develop_memo/_work/
20260813_ENH-E7_project_analysis_workspace_separation/

を正規authorityとして監査すること。

特に、
1. nested _work/ copyと正規rootの差分
2. 全13 PxxのReporting contract self-contained化
3. Candidate Assembly output contract
4. G01/G02 07のTest report / 999 output contract
5. PRE-16
を確認し、v0.05 intended changeが正規rootへ反映されていなければ修正せよ。

その後G01/P01/Trial01を再開可能か判定せよ。
P01がPACKAGE_COMPLETEになるまでP02をREADY_TO_EXECUTEにしてはならない。
```
