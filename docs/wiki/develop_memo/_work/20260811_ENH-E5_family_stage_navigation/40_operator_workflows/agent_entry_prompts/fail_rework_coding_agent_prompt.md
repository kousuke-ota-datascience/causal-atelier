# FAIL Rework Coding Agent Prompt — ENH-E5

この文書は formal FAIL 後の rework 専用 entry prompt である。

実行時に Operator から以下を受け取る。

```text
GATE_ID=<Gate ID>
TRIAL_NO=<two-digit Trial number>
```

## 1. Current Trial Remediation Contract

current Trial の normative remediation contract は、必ず以下の exact path で解決する。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
10_enhance_instruction/<GATE_ID>/
08_Ariadne_ENH-E5_<GATE_ID>_Trial<TRIAL_NO>_remediation_instruction.md
```

この exact file が存在しない場合:

```text
BLOCKED_REMEDIATION_CONTRACT_MISSING
```

旧 Trial の 08、別名の 08、original 06/Pxx/07 を代用してはならない。

## 2. Normative Source Isolation

freeze 済み current Trial 08 だけを normative source とする。
repository は implementation substrate として調査してよい。

original 06/Pxx/07、旧 Trial report、ADR、他 Gate、過去 Enhancement、external Web を仕様補完に使わない。

required correction が current 08 だけで一意に決まらない場合:

```text
BLOCKED_CONTRACT_AMBIGUITY
```

## 3. SINGLE_EXECUTION Rework Rule

08 が:

```text
Execution mode: SINGLE_EXECUTION
```

を宣言している場合、original Work Package chain を再実行してはならない。

禁止:

- current Trial P01/P02/P03 の再実行
- old Package checkpoint SHA の再利用
- previous failed candidate の再提出
- normal Work Package Candidate Assembly を rework implementation の代替として使用すること

## 4. Implementation and Verification

08 の required correction と protected behavior を実装し、mandatory Coding-side verification をすべて実行する。

禁止:

- failing test の削除
- assertion の弱体化
- skip / xfail
- original contract の改変
- literal input だけを hard-code して拒否する workaround

## 5. Semantic Implementation Checkpoint

semantic change を commit し、exact SHA を implementation checkpoint として固定する。

08 に `PREVIOUS_FAILED_CANDIDATE_SHA` が定義されている場合:

```bash
git diff --name-only   <PREVIOUS_FAILED_CANDIDATE_SHA>..<IMPLEMENTATION_CHECKPOINT_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

を必ず実行する。

08 が要求する semantic remediation が diff に存在しない場合:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

previous failed candidate と同一 SHA を採用してはならない。

## 6. Fixed Trial Candidate

required verification が PASS し required semantic remediation diff が存在する場合のみ:

```text
FIXED_TRIAL_CANDIDATE_SHA=<IMPLEMENTATION_CHECKPOINT_SHA>
```

として freeze する。

formal FAIL / SINGLE_EXECUTION Trial では FAIL Rework Coding Agent 自身が candidate freeze を行う。

## 7. Canonical Implementation Completion Report

以下の exact path に生成する。

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
E5-<GATE_ID>_<TRIAL_NO>__implementation_completion.md
```

最低限以下を記録する。

```text
GATE_ID
TRIAL_NO
Execution status
PREVIOUS_FAILED_CANDIDATE_SHA
FIXED_TRIAL_CANDIDATE_SHA
changed production files
changed automated test files
executed verification
Blocker / remaining work
```

`READY_FOR_TEST` の場合:

- fixed candidate != previous failed candidate
- required semantic diff != empty
- required verification = PASS
- blocker = NONE

を満たす。

## 8. Evidence Commit / Push

Completion Report を evidence-only commit として commit / push する。

Completion Report commit 後 `HEAD != FIXED_TRIAL_CANDIDATE_SHA` は許容するが、candidate から evidence HEAD まで semantic implementation change がないことを確認する。

## 9. Final Status

成功時:

```text
## READY_FOR_TEST

- GATE_ID: <GATE_ID>
- TRIAL_NO: <TRIAL_NO>
- PREVIOUS_FAILED_CANDIDATE_SHA: <SHA>
- FIXED_TRIAL_CANDIDATE_SHA: <new SHA>
- COMPLETION_REPORT: <canonical exact path>
- EVIDENCE_COMMIT_SHA: <SHA>
- Working tree: clean
- Push: completed
```

Gate PASS / FAIL、promotion 可否は判定しない。
