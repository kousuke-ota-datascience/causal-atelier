# 23_18_api_annotation_artifact

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

### 5.9 Annotation / Artifact API

#### 5.9.1 Canonical/simple Annotation

Current routes:

| Method | Path | 用途 |
| --- | --- | --- |
| POST | `/projects/{project_id}/annotations` | ResultまたはGraphVersion向けAnnotation作成 |
| GET | `/annotations/{annotation_id}` | 取得 |
| PATCH | `/annotations/{annotation_id}` | 更新 |

Response field:

```text
annotation_id
project_id
target_result_id
target_graph_version_id
statement
rationale
assumptions
limitations
created_by
created_at
updated_at
```

exactly one target constraintを持つ。

#### 5.9.2 WorkspaceAnnotation

Product Closureには別のProject-scoped annotation APIがある。

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/projects/{project_id}/workspace-annotations` | list/filter |
| POST | `/projects/{project_id}/workspace-annotations` | create |
| PATCH | `/projects/{project_id}/workspace-annotations/{annotation_id}` | update |

Allowed target:

```text
Project
ResearchContextVersion
AnalysisView
AnalysisSpecification
Execution
Result
GraphVersion
```

追加fieldとして`decision: SELECTED / REJECTED / DEFERRED / null`、`next_actions`を扱い、persistenceではrevision historyも保持する。

#### 5.9.3 Canonical Artifact

Current unscoped-by-project routes:

| Method | Path | 用途 |
| --- | --- | --- |
| GET | `/artifacts/{artifact_id}` | metadata |
| GET | `/artifacts/{artifact_id}/download` | SHA-256検証済みdownload |

Metadata response:

```text
artifact_id
project_id
execution_id
result_id
artifact_type
object_key
content_hash
media_type
size_bytes
metadata
created_at
```

Canonical persistenceにはさらに`stage_execution_id / artifact_scope`が存在するが、current `ArtifactResponse`では公開していない。

Project Closureにも`GET /projects/{project_id}/artifacts/{artifact_id}`および`.../download`があり、membership / Project境界を付加して同じartifact contentを扱う。

Current contractではunscoped legacy routeもArtifactからProjectをresolveして同じmembership authorizationを適用する。Explicit sensitive Artifact/output detailはOWNER/EDITORのみ。

Canonical `ArtifactType`はfixed enumであり、Predictive関連では`PARTITION_INDEX / FITTED_PREPROCESSOR / FITTED_MODEL / PREDICTION / PREDICTIVE_EXPLANATION / MODEL_CARD`等を含む。

#### 5.9.4 Findings / Model Management

`Findings`はcanonical Result、simple AnnotationまたはWorkspaceAnnotation、Artifact、Lineage projectionを組み合わせて構成する。decision/next actionが必要な場合はWorkspaceAnnotationの既存責務を利用する。

`Model Management`は`TRAINING_RESULT / EVALUATION_RESULT / MODEL_CARD_RESULT`と`FITTED_PREPROCESSOR / FITTED_MODEL / MODEL_CARD`等をreadするsurfaceとして構成できる。ENH-E10ではmodel/task/effective parameters、provider/library version、seed/determinism、feature/preprocessor identity、fitted-model schema/artifact identity、explanation method metadata、lineage/runtime provenanceを同じread surfaceから提示する。

これらのNavigation Stageのために重複Result/Annotation/Artifact Resourceを新設しない。


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-124a（SPLIT）

- 旧要件に含まれるIF固有情報：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- RDの要求核／Legacy Trace：成果物の情報・取得をProject境界内で安全に利用できる
- `FR-124a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-124b（SPLIT）

- 旧要件に含まれるIF固有情報：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- RDの要求核／Legacy Trace：旧経路を含む成果物取得に同じProject権限を適用する
- `FR-124b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. AR-020（SPLIT）

- 旧要件に含まれるIF固有情報：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する
- RDの要求核／Legacy Trace：個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する
- `AR-020`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)
