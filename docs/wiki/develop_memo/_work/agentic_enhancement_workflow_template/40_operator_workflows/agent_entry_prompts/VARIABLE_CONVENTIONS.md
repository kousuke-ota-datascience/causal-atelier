# Agent Entry Prompt Variable Conventions — v3

## 1. Principle

Humanはidentityを指定し、path / filenameはderived variableで構成する。

## 2. Human-supplied variables

| Variable | Meaning | Example |
|---|---|---|
| `PROJECT_NAME` | project / product name | `Ariadne` |
| `ENHANCE_ID` | enhancement canonical ID | `ENH-E4` |
| `ENHANCE_SHORT_ID` | artifact prefix用short ID | `E4` |
| `GATE_ID` | Gate acceptance boundary | `G08` |
| `TRIAL_NO` | verification attempt | `01` |
| `PACKAGE_ID` | Coding execution unit; WP mode only | `P04` |
| `WORK_DIR_NAME` | enhancement work directory | `20260808-01_ENH-E4_eliminate_dual_execution` |
| `REMOTE_NAME` | git remote | `causal-atelier` |
| `BRANCH_NAME` | git branch | `refactor/ariadne_mvp_e4` |

## 3. Derived variable examples

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
ARTIFACT_PREFIX={{ENHANCE_SHORT_ID}}-{{GATE_ID}}
IMPLEMENTATION_INSTRUCTION_ID=06_{{GATE_ID}}_{{PACKAGE_ID}}
IN_PROGRESS_REPORT_FILE={{ARTIFACT_PREFIX}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
CHECKPOINT_REPORT_FILE={{ARTIFACT_PREFIX}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
TEST_INSTRUCTION_ID=07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_テスト指示書
TEST_REPORT_DIR={{WORK_ROOT}}/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}
```

## 4. Expansion rule

- `{{VARIABLE}}`は再帰的に展開する。
- 未定義variableが残った場合はexecutionを開始しない。
- derived valueをHumanが手入力で二重管理しない。
- globが複数fileへ一致した場合は曖昧性を解消するまで停止する。
- variable nameはUPPER_SNAKE_CASEを使用する。
