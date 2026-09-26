# Agent Execution Readiness

## 1. Purpose

Preflightはtarget Agent executionを一意かつ安全に開始できるかを検証する。

Document compliance / planning completeness / audit completenessを毎回再検証する場ではない。

## 2. Validation axes

| Axis | PASS condition |
|---|---|
| Artifact completeness | normal runtimeにrequiredなinstantiated artifactが存在する |
| Content completeness | required contract metadata / semantic bodyが存在する |
| Execution resolvability | Human entryからexecution identity / routing / dependencyが一意に解決できる |
| Information isolation | Agentが許可されたnormative sourceだけで実行できる |

## 3. Normal read-set

Common:

```text
Enhancement-specific Agent prompt
Gate 06
Gate 07
repository identity / branch
```

Gate dependencyがある場合のみ:

```text
upstream canonical 999 Gate Decision
```

WORK_PACKAGEの場合のみ:

```text
assigned Pxx
assigned Pxxが宣言するupstream package reports / Gate 999
```

Preflightが通常読まないもの:

```text
Gate local README
P00
00 background / planning / design
Architecture Review artifacts
Implementation Detail Ledger
other Pxx
mutable state sheet
```

## 4. Blocking checks

1. WORK_ROOT / branch / runtime identityが正しい。
2. GATE_ID / PACKAGE_ID / TRIAL_NOがprotocol grammarに適合する。
3. Gate directoryがrepository artifactとして存在する。
4. canonical 06 / 07がexactly oneへ解決する。
5. 06 `Gate`がruntime GATE_IDと一致する。
6. 06 `Contract status == FROZEN`。
7. 07 `Verification contract status == FROZEN`。
8. 06 `Depends on`がGate dependency grammarとして解釈可能。
9. required upstream Gateのlatest canonical 999がPASS。
10. 06 `Execution mode`がvalid。
11. modeと06 `Required packages`が整合する。
12. WORK_PACKAGEではassigned Pxxがrequired package集合に含まれexactly oneへ解決する。
13. assigned Pxxが`Self-containment: MUST` / `Information isolation: MUST`。
14. assigned Pxx dependencyがsemantic grammarとして解釈可能でcanonical evidenceを満たす。
15. Coding promptがassigned-Pxx-only authorityを破っていない。

## 5. Metadata parsing contract

Metadata parserは **format tolerance / semantic strictness** を分離する。

```text
format tolerance   = YES
semantic guessing  = NO
```

以下は同値として受理する。

```text
**Depends on:** G02 PASS
Depends on: G02 PASS
- Depends on: G02 PASS
```

同じtoleranceを `Contract status`, `Verification contract status`, `Execution mode`, `Required packages`, `Gate`, `Package`, `Self-containment`, `Information isolation` 等へ適用する。

field欠落、空値、conflicting duplicate、workflow grammarとして解釈不能な値、required evidence欠落はblockingとする。Markdown boldやbulletの有無だけをblocking理由にしてはならない。

共通parser implementationは `40_operator_workflows/tools/workflow_metadata.py` を使用し、個別preflightが `bold_field()` 等の独自decorator-specific parserを持たない。

Regression self-test:

```bash
python3 40_operator_workflows/tools/test_workflow_metadata.py
```

## 6. Non-blocking conditions

以下はHard FAILにしない。

- Gate local README missing / stale
- P00 missing
- optional audit ledger missing
- Architecture Review artifactの存在そのもの
- Markdown bold / bullet / spacing差
- `Status at issuance` literal
- optional remote diagnostic

ただし06がFROZENでない場合はHard FAILとし、freeze authoring workflowへ戻す。

## 7. Severity boundary

### 7.1. Hard FAIL

execution target / authority / prerequisite / isolationを一意に解決できない場合に限定する。

### 7.2. WARN

execution semanticsを変えないが、運用上の確認価値がある非blocking conditionに用いる。

### 7.3. INFO

workflow controlに使用しない宣言値・diagnostic evidenceを表示する。例: Pxx `Status at issuance`。

### 7.4. Cosmetic differences

Markdown bold、bullet、空白等のcosmetic decoration差だけをWARN / FAIL理由にしない。

## 8. Decision

全blocking checkがPASSした場合のみ `READY_FOR_AGENT_EXECUTION` とする。

1件でもFAILならAgentを起動せず、failed axis / conditionを報告する。

## 9. Separation from freeze authoring

Architecture / planning / design factの解決は06を`FROZEN`にするまでのauthoring responsibilityである。

runtime preflightでplanning treeやArchitecture Reviewを再読してfreeze品質を再構成しない。FROZEN 06が必要なsemantic conclusionを自身に保持する。
