# 06a1 Lineage Semantics Assessment Result

## Metadata

- Prompt: `06a1_lineage_semantics_assessment_prompt.md`
- Started at: `2026-08-08T07:12:20+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `a738004fdbfc651e603215127a9214f5511560b8`
- Golden Path root result: `9203bd6d-abbc-47a4-9bc2-bc5ea061f98c`

> Read-only assessment. No Product state was modified.

## 06a1-01 Current branch

### Command

````bash
git branch --show-current
````

### Exit Code

````text
0
````

### Output

````text
refactor/ariadne_mvp_e4
````

## 06a1-02 Application service states

### Command

````bash
docker ps --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"
````

### Exit Code

````text
0
````

### Output

````text
NAMES                    STATUS                    service
ariadne-e1a-frontend-1   Up 14 minutes             frontend
ariadne-e1a-api-1        Up 14 minutes (healthy)   api
ariadne-e1a-worker-1     Up 14 minutes             worker
ariadne-e1a-database-1   Up 21 minutes (healthy)   database
````

## 06a1-03 Golden Path root Result presence

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT result_id, execution_id, result_type, scientific_status FROM product_result WHERE result_id = '9203bd6d-abbc-47a4-9bc2-bc5ea061f98c';"
````

### Exit Code

````text
0
````

### Output

````text
              result_id               |             execution_id             |       result_type       | scientific_status 
--------------------------------------+--------------------------------------+-------------------------+-------------------
 9203bd6d-abbc-47a4-9bc2-bc5ea061f98c | b8f73f99-cbb0-49e4-8c8b-9d13042e071d | TREATMENT_EFFECT_RESULT | ESTIMATED
(1 row)

````

## 06a1-04 Persisted product_lineage_edge count

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT count(*) AS product_lineage_edge_count FROM product_lineage_edge;"
````

### Exit Code

````text
0
````

### Output

````text
 product_lineage_edge_count 
----------------------------
                          0
(1 row)

````

## 06a1-05 Lineage API request

### Command

````bash
curl --fail --silent --show-error http://127.0.0.1:18000/api/v1/results/9203bd6d-abbc-47a4-9bc2-bc5ea061f98c/lineage
````

### Exit Code

````text
0
````

### Error Output

````text
````

## 06a1-07 Golden Path lineage assertions in source

### Command

````bash
sed -n "221,236p" tests/product/compose_golden_path_smoke.py
````

### Exit Code

````text
0
````

### Output

````text
                )["items"]
                if result["result_type"] == "TREATMENT_EFFECT_RESULT"
            )
            for execution_id in estimation_ids
        ]
        assert all(result["scientific_status"] == "ESTIMATED" for result in estimation_results)
        assert all(result["artifact_ids"] for result in estimation_results)
        _require(client.post("/comparisons/query", json={
            "project_id": project_id,
            "result_ids": [result["result_id"] for result in estimation_results],
        }))

        selected = estimation_results[0]
        _require(client.post(f"/projects/{project_id}/annotations", json={
            "target_result_id": selected["result_id"], "target_graph_version_id": None,
            "statement": "retain the OLS estimate", "rationale": "estimator agreement",
````

## 06a1-08 LineageQueryService construction logic

### Command

````bash
grep -nE "def get_lineage|def add_edge|add_edge\\(|uow\\.|return LineageView" src/ariadne/product/application/lineage_query_service.py
````

### Exit Code

````text
0
````

### Output

````text
29:    def get_lineage(self, result_id: str) -> LineageView:
31:            result = uow.results.get(result_id)
45:            def add_edge(source: str, target: str) -> None:
55:                        uow.artifacts.list_by_execution(execution_id)
56:                        + uow.artifacts.list_by_result(target_result_id)
64:                    add_edge(target_result_id, artifact.artifact_id)
68:                annotations = uow.annotations.list_by_target(
79:                    add_edge(target_id, annotation.annotation_id)
82:                dataset = uow.dataset_versions.get(dataset_version_id)
90:                add_edge(dataset.dataset_version_id, execution_id)
91:                source_artifact = uow.artifacts.get(dataset.source_artifact_id)
97:                    add_edge(source_artifact.artifact_id, dataset.dataset_version_id)
113:                generating = uow.executions.get(current.execution_id)
118:                project = uow.projects.get(generating.project_id)
123:                    add_edge(project.project_id, generating.execution_id)
135:                add_edge(generating.execution_id, current.result_id)
138:                    base = uow.executions.get(revision.get("base_execution_id", ""))
154:                    add_edge(base.execution_id, generating.execution_id)
159:                    upstream = uow.results.get(generating.input_result_id)
162:                        add_edge(upstream.result_id, generating.execution_id)
164:                    graph = uow.graph_versions.get(generating.input_graph_version_id)
182:                add_edge(graph.graph_version_id, consumer_id)
185:                    source = uow.results.get(graph.source_result_id)
188:                        add_edge(source.result_id, graph.graph_version_id)
190:                    parent = uow.graph_versions.get(graph.parent_graph_version_id)
195:            root_execution = uow.executions.get(result.execution_id)
199:        return LineageView(nodes=nodes, edges=edges)
````

## 06a1-09 Persistent LineageEdge ORM definition

### Command

````bash
grep -nA30 -B3 "class LineageEdgeOrm" src/ariadne/product/persistence/orm_models.py
````

### Exit Code

````text
0
````

### Output

````text
539-    )
540-
541-
542:class LineageEdgeOrm(ProductBase):
543-    __tablename__ = "product_lineage_edge"
544-
545-    lineage_edge_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
546-    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
547-    source_type: Mapped[str] = mapped_column(String(100), nullable=False)
548-    source_id: Mapped[str] = mapped_column(String(100), nullable=False)
549-    relation_type: Mapped[str] = mapped_column(String(100), nullable=False)
550-    target_type: Mapped[str] = mapped_column(String(100), nullable=False)
551-    target_id: Mapped[str] = mapped_column(String(100), nullable=False)
552-    evidence_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
553-    created_by: Mapped[str] = mapped_column(String(200), nullable=False)
554-    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
555-
556-    __table_args__ = (
557-        UniqueConstraint("source_type", "source_id", "relation_type", "target_type", "target_id", name="uq_product_lineage_edge"),
558-    )
559-
560-
561-class ProjectMembershipOrm(ProductBase):
562-    __tablename__ = "product_project_membership"
563-
564-    membership_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
565-    project_id: Mapped[str] = mapped_column(ForeignKey("product_project.project_id", ondelete="RESTRICT"), nullable=False, index=True)
566-    user_id: Mapped[str] = mapped_column(String(200), nullable=False)
567-    role: Mapped[str] = mapped_column(String(20), nullable=False)
568-    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
569-
570-    __table_args__ = (
571-        UniqueConstraint("project_id", "user_id", name="uq_product_project_membership"),
572-        CheckConstraint("role IN ('OWNER','EDITOR','VIEWER')", name="ck_product_project_membership_role"),
````

## 06a1-10 Product source references to LineageEdge persistence

### Command

````bash
git grep -n -E "LineageEdgeOrm|product_lineage_edge" -- src/ariadne/product || true
````

### Exit Code

````text
0
````

### Output

````text
src/ariadne/product/application/exploratory_service.py:43:    LineageEdgeOrm,
src/ariadne/product/application/exploratory_service.py:538:        session.add(LineageEdgeOrm(
src/ariadne/product/application/predictive_split_service.py:31:    LineageEdgeOrm,
src/ariadne/product/application/predictive_split_service.py:273:        session.add(LineageEdgeOrm(
src/ariadne/product/application/predictive_workflow_service.py:53:    LineageEdgeOrm,
src/ariadne/product/application/predictive_workflow_service.py:603:            rows = session.scalars(select(LineageEdgeOrm).where(
src/ariadne/product/application/predictive_workflow_service.py:604:                LineageEdgeOrm.project_id == project_id,
src/ariadne/product/application/predictive_workflow_service.py:606:                    LineageEdgeOrm.source_id.in_(owned_ids)
src/ariadne/product/application/predictive_workflow_service.py:607:                    | LineageEdgeOrm.target_id.in_(owned_ids)
src/ariadne/product/application/predictive_workflow_service.py:609:            ).order_by(LineageEdgeOrm.created_at, LineageEdgeOrm.lineage_edge_id))
src/ariadne/product/application/predictive_workflow_service.py:645:                for edge in session.scalars(select(LineageEdgeOrm).where(
src/ariadne/product/application/predictive_workflow_service.py:646:                    (LineageEdgeOrm.source_id.in_(owned_ids))
src/ariadne/product/application/predictive_workflow_service.py:647:                    | (LineageEdgeOrm.target_id.in_(owned_ids))
src/ariadne/product/application/predictive_workflow_service.py:1038:    def _lineage_response(row: LineageEdgeOrm) -> dict[str, Any]:
src/ariadne/product/application/predictive_workflow_service.py:1086:        session.add(LineageEdgeOrm(
src/ariadne/product/application/product_closure_service.py:35:    LineageEdgeOrm,
src/ariadne/product/application/product_closure_service.py:383:            explicit_rows = list(session.scalars(select(LineageEdgeOrm).where(LineageEdgeOrm.project_id == project_id)))
src/ariadne/product/application/product_closure_service.py:448:            row = LineageEdgeOrm(
src/ariadne/product/application/product_closure_service.py:460:                row = session.scalar(select(LineageEdgeOrm).where(
src/ariadne/product/application/product_closure_service.py:461:                    LineageEdgeOrm.source_type == source_type,
src/ariadne/product/application/product_closure_service.py:462:                    LineageEdgeOrm.source_id == source_id,
src/ariadne/product/application/product_closure_service.py:463:                    LineageEdgeOrm.relation_type == relation,
src/ariadne/product/application/product_closure_service.py:464:                    LineageEdgeOrm.target_type == target_type,
src/ariadne/product/application/product_closure_service.py:465:                    LineageEdgeOrm.target_id == target_id,
src/ariadne/product/application/product_closure_service.py:497:                session.add(LineageEdgeOrm(
src/ariadne/product/application/product_closure_service.py:583:            explicit = list(session.scalars(select(LineageEdgeOrm).where(
src/ariadne/product/application/product_closure_service.py:584:                LineageEdgeOrm.project_id == project_id,
src/ariadne/product/application/product_closure_service.py:779:    def _lineage_edge_value(row: LineageEdgeOrm) -> dict[str, Any]:
src/ariadne/product/persistence/orm_models.py:542:class LineageEdgeOrm(ProductBase):
src/ariadne/product/persistence/orm_models.py:543:    __tablename__ = "product_lineage_edge"
src/ariadne/product/persistence/orm_models.py:557:        UniqueConstraint("source_type", "source_id", "relation_type", "target_type", "target_id", name="uq_product_lineage_edge"),
````

## 06a1-11 Product repository references to lineage

### Command

````bash
grep -nEi "lineage|LineageEdge" src/ariadne/product/persistence/repositories.py || true
````

### Exit Code

````text
0
````

### Output

````text
````

## Completion

- Finished at: `2026-08-08T07:12:21+00:00`
- Phase execution: `COMPLETED`
- Product state modified: `NO`
- Final clean reinitialization: `NOT EXECUTED`
