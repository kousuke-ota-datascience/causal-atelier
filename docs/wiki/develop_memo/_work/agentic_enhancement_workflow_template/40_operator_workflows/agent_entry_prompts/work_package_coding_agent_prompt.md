# Coding Agent 作業開始プロンプト — WORK_PACKAGE

**Document class:** Operator Artifact / Agent Entry Prompt  
**Self-containment:** MUST for routing — このpromptだけで変数展開、Pxx/Rxx instruction特定、report path、stop ruleを理解できること。実装normative semanticsは特定されたPxx/Rxx primary contractに含まれる。

以下の変数をexecution parametersとする。

```text
PROJECT_NAME={{PROJECT_NAME}}
ENHANCE_ID={{ENHANCE_ID}}
ENHANCE_SHORT_ID={{ENHANCE_SHORT_ID}}
GATE_ID={{GATE_ID}}
PACKAGE_ID={{PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
WORK_DIR_NAME={{WORK_DIR_NAME}}
REMOTE_NAME={{REMOTE_NAME}}
BRANCH_NAME={{BRANCH_NAME}}
```

## 1. Variable / package-kind rule

- `PACKAGE_ID=P01-P99` -> planned package; instruction prefix=`06`
- `PACKAGE_ID=R01-R99` -> remediation package; instruction prefix=`08`
- その他 -> STOP
- `{{VARIABLE}}`は再帰展開し、未解決placeholderが残ればSTOP。

Derived variables:

```text
WORK_ROOT=docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}
INSTRUCTION_DIR={{WORK_ROOT}}/10_enhance_instruction/{{GATE_ID}}
IMPLEMENTATION_REPORT_DIR={{WORK_ROOT}}/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages
IN_PROGRESS_REPORT_FILE={{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_in_progress.md
CHECKPOINT_REPORT_FILE={{ENHANCE_SHORT_ID}}-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}_implementation_checkpoint_report.md
```

Instruction pattern:

```text
if PACKAGE_ID starts with P:
  06_{{GATE_ID}}_{{PACKAGE_ID}}_*.md
if PACKAGE_ID starts with R:
  08_{{GATE_ID}}_{{PACKAGE_ID}}_*.md
```

## 2. Execution

上記patternに一致する**1ファイルだけ**を特定し、そのprimary execution contractを実行せよ。複数一致 / 0件なら任意選択せず停止せよ。

Assigned Package scopeを越えて実装してはならない。

## 3. Execution status report

完了、中断、継続不能のいずれでも以下へ記録する。

```text
{{IMPLEMENTATION_REPORT_DIR}}/{{IN_PROGRESS_REPORT_FILE}}
```

最低限:

- Gate / Trial / Package
- execution status
- completed work / remaining work
- observed failures / blockers
- executed verification
- relevant commit SHA
- next action required

## 4. Checkpoint report

`PACKAGE_COMPLETE`を主張する場合:

```text
{{IMPLEMENTATION_REPORT_DIR}}/{{CHECKPOINT_REPORT_FILE}}
```

に、starting SHA、implementation checkpoint full SHA、changed files、focused verification、dependency state、limitationsを記載する。report-only commit SHAはcheckpoint SHAと区別する。

Package completionをGate PASS / verified current stateとして表現しない。

## 5. Repository recording

```bash
git add docs/wiki/develop_memo/_work/{{WORK_DIR_NAME}}/;\
git status;\
git commit -m "{{ENHANCE_ID}} Gate {{GATE_ID}} Trial {{TRIAL_NO}} Package {{PACKAGE_ID}} implementation checkpoint";\
git push -u {{REMOTE_NAME}} {{BRANCH_NAME}};\
git log -1
```

最後にexecution statusとrelevant SHAを明示して停止する。next packageへ勝手に進まない。
