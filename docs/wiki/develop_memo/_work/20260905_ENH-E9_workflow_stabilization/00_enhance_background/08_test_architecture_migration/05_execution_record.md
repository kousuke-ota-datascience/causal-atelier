# Test Migration Execution Record

**Status:** `NOT_STARTED`  
**Purpose:** append-only evidence of physical test-code migration batches

## 1. Execution policy

Each migration batch must record:

- batch ID;
- execution date/time;
- before SHA;
- after SHA;
- changed paths;
- manifest rows implemented;
- commands executed;
- collection/test results;
- deviations from manifest;
- blocker/failure classification;
- rollback or follow-up action if needed.

Do not use this document to rewrite design decisions; update `04_migration_decision_log.md` for new decisions and reference the decision ID here.

## 2. Current state

No physical test migration has been executed under this workstream yet.

```text
Migration batch count: 0
Source-code/test-code moves: NONE
Product semantic changes: NONE
G02 Fixed Trial Candidate changes: NONE
```

## 3. Batch template

### Batch Mxx — <title>

**Status:** `PLANNED | RUNNING | PASS | FAIL | BLOCKED | ROLLED_BACK`

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

#### Follow-up

- ...
