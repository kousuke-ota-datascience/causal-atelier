# ENH-E7 Agent Execution Readiness Preflight

Preflightの目的は、**Coding Agentが安全かつ迷わずassigned Work Packageを開始できるか**を確認することである。

Workflow protocolの完全性を証明するものではない。

## Result semantics

```text
FAIL
  -> BLOCKED_PRECHECK
  -> 誤対象、未依存、必須入力不足など実作業リスクがある

WARN
  -> 実行継続可能
  -> 非本質的metadata差異やdiagnostic information

INFO
  -> 追跡・説明用
```

`WARN` / `INFO`だけではCoding executionを停止しない。

## Canonical command

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . --gate G01 --package P01 --trial 01
```

## Derived execution eligibility

Pxx execution eligibilityは `READY_TO_EXECUTE` 等のdeclared status literalから決めない。

PRE-15はassigned Pxxの、

```text
**Depends on:** ...
```

を読み、必要なdependency completion evidenceから実行可否を導出する。

### Package dependency

例:

```text
**Depends on:** P01,P02
```

の場合、同一Gate / Trialのcanonical package execution status reportを確認する。

```text
20_implementation_reports/<GATE>/Trial<TRIAL>/packages/
ENH-E7_<GATE>_<PACKAGE>_Trial<TRIAL>_package_execution_status.md
```

最低限、

- Gate
- Trial
- Package
- State

のidentityが一致し、Stateがcompleteを意味する場合にdependency satisfiedとする。

package単位のcheckpoint SHA完全一致はdependency unlock条件にしない。

### Gate PASS dependency

`G01 PASS` のようなdependencyは、canonical `999_gate_decision` のPASS evidenceから導出する。

## Non-blocking diagnostics

以下は原則WARN / INFOであり、それ単独ではHard Failにしない。

- package declared status literal
- 説明・template用途のplaceholder表記
- local remote alias差異
- self-containment等の補助metadata literal欠落
- package単位のSHA未記録

## Blocking checks

Hard Failは、少なくとも以下のような実害を防ぐものに限定する。

- WORK_ROOTが存在しない
- assigned Pxxが一意に解決しない
- runtime Gate / Package / Trialが解決できない
- current branchが対象branchではない
- Architecture / Gate contractに明示的blocking stateがある
- required dependency completion evidenceがない
- Coding promptがcontext isolationを破るpositive read directiveを持つ

## Package evidence

Work Package Coding Agentは1 packageにつき1本のstatus reportを作る。

```text
..._package_execution_status.md
```

Work PackageはGate-level quality boundaryではないため、package単位のFixed Candidate SHA / checkpoint reportは必須にしない。

Gate-level Fixed Trial CandidateはCandidate Assemblyで初めてfreezeする。

## Regression self-test

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/selftest_check_agent_execution_readiness.py
```

このself-testはP01開始前からP07までのdependency chain、status literal非依存、SHA非依存、identity mismatch等を検証する。
