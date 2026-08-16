# ENH-E7 Work Package Coding Agent Prompt

**Role:** bounded implementation agent  
**Enhancement:** ENH-E7  
**Branch:** feature/ariadne_mvp_e7  
**Work root:** docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation

Human provides exactly:

```text
GATE_ID=<Gxx>
PACKAGE_ID=<Pxx>
TRIAL_NO=<NN>
```

## 1. Preflight first

Run:

```bash
python3 docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/40_operator_workflows/preflight/check_agent_execution_readiness.py \
  --repo-root . --gate <GATE_ID> --package <PACKAGE_ID> --trial <TRIAL_NO>
```

`FAIL` が1件でもある場合のみ `BLOCKED_PRECHECK` として停止する。  
`WARN` / `INFO` は診断情報であり、それ単独では実装を停止しない。

実行可否は `READY_TO_EXECUTE` 等のdeclared status literalではなく、必須入力・実行対象・Gate contract readiness・dependency completionからpreflightが導出する。

## 2. Resolve assigned Pxx

Coding executionの唯一のnormative implementation contractは、exactly-oneで解決される以下のassigned Pxxである。

```text
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/10_enhance_instruction/<GATE_ID>/06_<GATE_ID>_<PACKAGE_ID>_*.md
```

P00はimplementation Work Packageではない。

## 3. Information isolation — MUST

Read the assigned Pxx.

仕様補完のために Gate 06 / Gate 07 / P00 / other Pxx / 00 background / 20 reports / 30 reports / previous Enhancement workflow artifacts / ADR / issue / external Web を読まない。

source code / tests / config / migrations / runtime facts は、assigned Pxx scope内のimplementation substrateとして調査してよい。

Pxxが実装に必要十分でない、またはverified source factと矛盾する場合は、推測で補完せず `PACKAGE_BLOCKED_CONTRACT_AMBIGUITY` とする。

## 4. Execute

assigned Pxxだけを実装する。  
Pxxで指定されたfocused verificationを実行する。  
別packageへ自動継続しない。

Work PackageはGate-level quality boundaryではないため、package単位のFixed Candidate SHAやGate級acceptanceを作らない。

## 5. Package handoff report

完了または中断時、次の**1ファイル**を作成する。

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/packages/
ENH-E7_<GATE_ID>_<PACKAGE_ID>_Trial<TRIAL_NO>_package_execution_status.md
```

最低限、以下を記録する。

```text
# ENH-E7 <GATE_ID> <PACKAGE_ID> Package Execution Status

- Enhancement: ENH-E7
- Gate: <GATE_ID>
- Trial: <TRIAL_NO>
- Package: <PACKAGE_ID>
- State: PACKAGE_COMPLETE | PACKAGE_BLOCKED
- Branch: feature/ariadne_mvp_e7
- Implementation HEAD full SHA: <40-hex SHA or NOT_RECORDED>

## 実施したscope
## Changed files / responsibility
## Focused verification
  - exact command / method
  - exit code / result
## Remaining / blocker
## Scope guard確認
## Facts
## Interpretation
```

`Implementation HEAD full SHA` はtraceability用であり、package completionを成立させるためのSHA lockではない。  
report作成後にreport自身のcommit SHAを自己参照させない。

`PACKAGE_COMPLETE` は以下を意味する。

- assigned scopeの実装が完了した
- required focused verificationがPASSした
- unresolved blockerがない
- 上記status reportを作成した

これは `READY_FOR_TEST` / Gate PASS を意味しない。

## 6. Stop rule

- package scope完了 → `PACKAGE_COMPLETE`
- 安全に継続不能 → `PACKAGE_BLOCKED`
- Gate PASS/FAILを宣言しない
- 別packageへ自動継続しない
