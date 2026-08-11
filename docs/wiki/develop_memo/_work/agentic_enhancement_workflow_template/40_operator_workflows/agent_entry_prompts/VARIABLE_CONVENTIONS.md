# Agent Entry Prompt Variable Conventions — Authoring Reference

**Document class:** Authoring Reference  
**Self-containment:** SHOULD; execution prompts must not depend on this file at runtime.


> **Supplemental authoring reference**: 各execution promptは必要なvariable / expansion ruleを自身に持つ。本書はprompt authorが命名を揃えるためのreferenceであり、Agent execution時の必須入力ではない。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。


## 1. Principle

Humanはexecution identityを指定し、path / filenameはderived variableで構成する。

**Humanがderived filenameを毎回手入力して二重管理しない**ことを原則とする。

## 2. Human-supplied variables

| Variable | Meaning | Example form |
|---|---|---|
| `PROJECT_NAME` | project / product name | `{{PROJECT_NAME}}` |
| `ENHANCE_ID` | enhancement canonical ID | `ENH-XX` |
| `ENHANCE_SHORT_ID` | artifact prefix用short ID | `EXX` |
| `GATE_ID` | Gate acceptance boundary | `G03` |
| `TRIAL_NO` | verification attempt | `01` |
| `PACKAGE_ID` | Coding execution unit; Work Package時のみ | `P02` |
| `WORK_DIR_NAME` | enhancement work directory | `YYYYMMDD-NN_<enhancement_slug>` |
| `REMOTE_NAME` | git remote | `origin` |
| `BRANCH_NAME` | git branch | `refactor/<enhancement_slug>` |

## 3. Derived variable examples

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
ARTIFACT_PREFIX={{ENHANCE_SHORT_ID}}-{{GATE_ID}}
IMPLEMENTATION_INSTRUCTION_ID=06_{{GATE_ID}}_{{PACKAGE_ID}}
IN_PROGRESS_REPORT_FILE={{ARTIFACT_PREFIX}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
CHECKPOINT_REPORT_FILE={{ARTIFACT_PREFIX}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
TEST_INSTRUCTION_ID=07_{{PROJECT_NAME}}_{{ENHANCE_ID}}_{{GATE_ID}}_test_instruction
TEST_REPORT_DIR={{WORK_ROOT}}/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}
```

## 4. Expansion rule

- `{{VARIABLE}}`は再帰的に展開する。
- 未定義variableが残った場合はexecutionを開始しない。
- derived valueをHumanが手入力で二重管理しない。
- globが複数fileへ一致した場合は曖昧性を解消するまで停止する。
- variable nameはUPPER_SNAKE_CASEを使用する。
