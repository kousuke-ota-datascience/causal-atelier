# 21_30_state_models

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`; original ID, level and state retained.  
**Source blob:** `72903b9ad48b5b7edabaa7bb1c2cace42aa46ce7`.

---

## 5. 状態モデル

### 5.1 Project Status

```text
ACTIVE
  │
  └── archive()
        ▼
    ARCHIVED
```

- 初期状態は`ACTIVE`。
- `ARCHIVED -> ACTIVE`をcurrent必須遷移としない。
- ARCHIVED後も過去Resource / Result / Lineageをread-onlyで保持する。

### 5.2 Versioned Resource Status

`ResearchContextVersion`、`AnalysisView`、`AnalysisSpecification`の基本状態:

```text
DRAFT
  │
  └── fix()
        ▼
      FIXED
```

- DRAFTではvalidation可能な範囲で編集できる。
- FIXED後に意味内容を変更する場合は新Versionを作成する。
- FIXED時にcanonical hash / fixed_atを確定する。

`GraphVersion`も`DRAFT -> FIXED`を基本とするが、Graph origin/reference制約を追加で満たす。

### 5.3 Execution Status

```text
QUEUED
  ├── start() ───────────────► RUNNING
  ├── cancel() ──────────────► CANCELLED
  │
RUNNING
  ├── succeed() ─────────────► SUCCEEDED
  ├── fail() ────────────────► FAILED
  └── cancel() ──────────────► CANCELLED
```

- technical Execution statusとResultのscientific statusは独立である。
- `SUCCEEDED`は科学的仮説の成功を意味しない。
- rerun/revisionは既存Executionのstatus巻き戻しではなく新Executionとして表現する。

### 5.4 StageExecution Status

```text
PENDING
   │ prerequisite resolved
   ▼
READY
   │ start
   ▼
RUNNING
 ├──────────────► SUCCEEDED
 ├──────────────► FAILED
 ├──────────────► CANCELLED
 └ prerequisite failure
                 ▼
       SKIPPED_DUE_TO_PREREQUISITE
```

実際の許容状態は次の7つ。

- `PENDING`
- `READY`
- `RUNNING`
- `SUCCEEDED`
- `FAILED`
- `SKIPPED_DUE_TO_PREREQUISITE`
- `CANCELLED`

StageAttemptはこの状態遷移の試行履歴であり、StageExecutionそのものとは分離する。

### 5.5 GraphVersion Status

```text
DRAFT
  │
  └── fix()
        ▼
      FIXED
```

- DRAFTのみ編集可能。
- FIXEDは不変。
- 編集・修正したGraphを保存する場合、parent GraphVersionを参照する新GraphVersionを作成する。

### 5.6 Result Scientific Status

Resultのscientific statusは`result_type`に応じて解釈する。代表的なstatus group:

| Result category | 許容status |
| --- | --- |
| Exploratory generic | `GENERATED`, `GENERATED_WITH_WARNINGS` |
| Discovery Graph | `GENERATED`, `GENERATED_WITH_WARNINGS`, `UNRELIABLE` |
| Identification | `IDENTIFIED`, `NOT_IDENTIFIED`, `PARTIALLY_IDENTIFIED`, `REQUIRES_REVIEW` |
| Eligibility / Diagnostics | `PASS`, `WARN`, `FAIL` |
| Treatment Effect | `ESTIMATED`, `INSUFFICIENT_OVERLAP`, `INSUFFICIENT_SAMPLE`, `ESTIMATION_UNRELIABLE`, `REQUIRES_REVIEW` |
| Refutation | `NO_FAILURE_DETECTED`, `FAILURE_DETECTED`, `INCONCLUSIVE` |
| Sensitivity | `ROBUST`, `FRAGILE`, `INCONCLUSIVE` |
| Split | `PASS` |
| Training | `TRAINED`, `TRAINED_WITH_WARNINGS` |
| Evaluation | `EVALUATED`, `INSUFFICIENT_TEST_SAMPLE` |
| Predictive Explanation | `GENERATED`, `GENERATED_WITH_WARNINGS`, `NOT_APPLICABLE` |

technical `FAILED`をscientific `FAIL`と混同しない。

### 5.7 Workspace Selection State

WorkspaceSelectionはlifecycle Entityではなくmutable selection stateだが、Analysis Contextの整合性に関わるため状態規則を定義する。

```text
Current Project = route project_id
      │
      ├─ Active Research Context  optional
      ├─ Dataset Version          optional
      └─ Analysis View            optional
             │
             └─ Dataset-compatible only
```

Dataset Version変更時:

```text
new Dataset Version selected
        │
        ▼
current Analysis View compatible?
      ├─ yes -> keep
      └─ no  -> clear Analysis View selection
```

有効値がない場合はunselectedを許容し、dummy/default Resourceを作らない。
