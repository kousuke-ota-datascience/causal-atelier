# テストMigration Execution Record

**状態:** `NOT_STARTED`  
**目的:** physical test-code migration batchの追記型実行証跡

## 1. 実行policy

各migration batchは以下を記録する。

- batch ID
- execution date/time
- before SHA
- after SHA
- changed paths
- 実装したmanifest row
- 実行command
- collection / test result
- manifestからのdeviation
- blocker / failure classification
- 必要なrollback / follow-up

Design decisionの変更は本書で行わず、`04_migration_decision_log.md` を更新してdecision IDを参照する。

## 2. 現在状態

本workstreamにおけるphysical test migrationは未開始。

```text
Migration batch count: 0
Source-code/test-code moves: NONE
Product semantic changes: NONE
Gate contract/candidate remediation: NONE
```

## 3. Batch template

### Batch Mxx — <title>

**状態:** `PLANNED | RUNNING | PASS | FAIL | BLOCKED | ROLLED_BACK`

```text
Executed at:
Before SHA:
After SHA:
Related decisions:
Related manifest rows:
```

#### Scope

- ...

#### Files changed

```text
source -> target
```

#### Commands

```text
...
```

#### Results

| Verification | Result | Evidence |
|---|---|---|
| pytest collection | | |
| targeted tests | | |
| regression tests | | |
| enhancement tests | | |
| Browser/CI path validation | | |

#### Deviations

- NONE / ...

#### Classification

```text
PRODUCT_DEFECT | TEST_IMPLEMENTATION_DEFECT | TEST_ORCHESTRATION_DEFECT |
TEST_ENVIRONMENT_DEFECT | MIGRATION_MANIFEST_DEFECT | NONE
```

#### Gate / Enhancement impact

```text
Affected Gate(s): NONE | Gxx ...
Product candidate impact: NONE | <explicit route reference>
Frozen contract impact: NONE | <explicit amendment reference>
```

Migration自体を理由としてGate candidateやfrozen contractを変更してはならない。影響が生じる場合は、test migrationとは別の正式なGate routeとして記録する。

#### Follow-up

- ...
