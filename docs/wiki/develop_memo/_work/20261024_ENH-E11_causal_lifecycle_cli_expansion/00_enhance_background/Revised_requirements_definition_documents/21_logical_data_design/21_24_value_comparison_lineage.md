# 21_24_value_comparison_lineage


---

### 4.9 Comparison Projection

Comparisonは複数Result / Executionから導出するread modelであり、比較そのものを正本Entityとして保存することを必須としない。

```text
Comparison Projection
├─ compared execution/result IDs
├─ method / parameter / dataset / graph differences
├─ comparable metrics
├─ warnings
└─ provenance links
```

比較対象の原データはExecution / Result / Artifact / LineageEdgeを正本とする。

### 4.10 Lineage View

Lineage Viewは`LineageEdge`およびEntityのdirect referenceから構成するquery modelである。

```text
Lineage View
Project
  ├─ ResearchContextVersion
  ├─ DatasetVersion
  ├─ AnalysisView
  ├─ AnalysisSpecification
  ├─ ExecutionPlan
  ├─ Execution
  │   ├─ StageExecution
  │   ├─ Result
  │   └─ Artifact
  └─ GraphVersion
```

UI表示時に新しいLineage relationを推測・persistしてはならない。

### 4.11 Graph Candidate View

Graph Candidate ViewはGraphVersionを候補一覧として比較するprojectionである。

主要表示値:

- GraphVersion identity / name / graph_type / origin
- source Result / parent GraphVersion
- designated outcome
- status
- content hash
- selected diagnostics / annotation summary

独立Candidate Entityは作らない。

### 4.12 Graph Comparison View

複数GraphVersionの構造差分を表示するprojection。

```text
Graph Comparison
├─ base graph
├─ compared graph
├─ added / removed nodes
├─ added / removed / reoriented edges
├─ origin / rationale
└─ provenance
```

比較結果を正本Graphとして保存する場合は新しいGraphVersionを明示作成する。

### 4.13 Operation Availability View

現在のAnalysis ContextとResource状態から、Operation実行可否を導出するread model。

```json
{
  "operation": "ESTIMATION",
  "available": false,
  "reasons": [
    {"code": "INPUT_RESULT_REQUIRED"}
  ]
}
```

availabilityはExecution stateそのものではない。context不足時に架空Resourceを生成して`available=true`にしない。

### 4.14 Compatibility / transition read models

`FamilyExecution / FamilyStageExecution / FamilyResult / FamilyArtifact`はhistorical/compatibility read modelである。

- legacy/historical rowを読み出すために保持し得る。
- canonical Product lifecycleの新規write authorityにはしない。
- canonical `Execution / StageExecution / Result / Artifact`との意味を混在させない。

### 4.17 Lineage authority model

Domain上のpolymorphic referenceは次のvalue modelとして解釈する。

```text
ResourceRef
├─ resource_type
├─ resource_id
├─ project_id
├─ schema_version: optional
└─ content_hash: optional
```

Canonical read modelは最低限次のstructural chainを再構成できなければならない。

```text
ResearchContextVersion
  ↓
AnalysisSpecification
  ↓
ExecutionPlan
  ↓
Execution
  ↓
StageExecution
  ↓
Result
  ↓
Artifact
```

さらに`DatasetVersion / AnalysisView / GraphVersion / input Result / base Execution`を接続する。

Lineage authorityはclosed-by-defaultとする。FK、snapshot identity、Execution/Stage/Result/Artifact ownershipからdeterministically導出できるstructural relationをgeneric `LineageEdge`へ二重persistしない。

Structural authorityの代表tuple:

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Result --USED_INPUT--> Execution
Result --DERIVED_FROM--> GraphVersion
Artifact --DERIVED_FROM--> DatasetVersion
Execution --DERIVED_FROM--> Execution
Execution --REVISED_FROM--> Execution
```

Generic `LineageEdge`がauthorityとなる代表tuple:

```text
Artifact --DERIVED_FROM--> Artifact
Result --SUMMARIZES--> Result
Result --SUMMARIZES--> Artifact
Result --MOTIVATED--> Execution
Result --MOTIVATED--> AnalysisSpecification
```

`Result`または`Artifact`をsourceとする`DOCUMENTS / SUPPORTED_BY / EVIDENCE_FOR`、ならびにdecision semanticsである`SELECTED / REJECTED`等は、許可されたsource/target typeの組合せに限ってgeneric persistenceする。

Domain relation typeとして扱う語彙:

```text
USED_INPUT
GENERATED
DERIVED_FROM
REVISED_FROM
SUPPORTED_BY
EVIDENCE_FOR
DOCUMENTS
SUMMARIZES
MOTIVATED
SELECTED
REJECTED
```

API入力として許可するrelation type subsetとdomain authority allowlistは同一contractとは限らない。presentation用の`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION / RELATED_TO`等の表示relation名をcanonical generic LineageEdge typeへ無条件に保存しない。
