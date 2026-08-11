# 06a Post-reset Functional Verification Result

## Metadata

- Prompt: `06a_post_reset_functional_verification_prompt.md`
- Started at: `2026-08-08T07:06:01+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `47d34e96256c5b65e57e2b7c1585c2bd6afdf0f5`
- Target Compose project: `ariadne-e1a`

> Functional verification after clean database reinitialization.
> Golden Path intentionally writes temporary verification data.

## 06a-01 Current branch precondition

### Command

````bash
CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"
````

### Exit Code

````text
0
````

### Output

````text
refactor/ariadne_mvp_e4
````

## 06a-02 Verify known runtime diff only

### Command

````bash
ACTUAL="$(git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy)"; EXPECTED="$(printf "D\tdeploy/.nfs000000000076202f00000088")"; printf "%s\n" "$ACTUAL"; test "$ACTUAL" = "$EXPECTED"
````

### Exit Code

````text
0
````

### Output

````text
D	deploy/.nfs000000000076202f00000088
````

## 06a-03 UV availability

### Command

````bash
uv --version
````

### Exit Code

````text
0
````

### Output

````text
uv 0.11.8 (x86_64-unknown-linux-gnu)
````

## 06a-04 Database health precondition

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"
````

### Exit Code

````text
0
````

### Output

````text
running/healthy
````

## 06a-05 API health precondition

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-api-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"
````

### Exit Code

````text
0
````

### Output

````text
running/healthy
````

## 06a-06 Worker state precondition

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"
````

### Exit Code

````text
0
````

### Output

````text
running
````

## 06a-07 Frontend state precondition

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"
````

### Exit Code

````text
0
````

### Output

````text
running
````

## 06a-08 API readiness precondition

### Command

````bash
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:18000/health/ready
````

### Exit Code

````text
0
````

### Output

````text
{"status":"ok"}
````

## 06a-09 Verify Product database is clean before tests

### Command

````bash
COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT COALESCE(SUM(n_live_tup),0) FROM pg_stat_user_tables WHERE relname LIKE 'product_%' AND relname <> 'alembic_version_product';")"; printf "estimated_product_rows=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
estimated_product_rows=0
````

## 06a-10 Verify artifact storage is clean before tests

### Command

````bash
COUNT="$(docker exec ariadne-e1a-api-1 sh -lc 'find /state -type f | wc -l')"; printf "artifact_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
artifact_file_count=0
````

## 06a-11 Run isolated Active Product tests

### Command

````bash
env -u ARIADNE_PRODUCT_DATABASE_URL -u ARIADNE_PRODUCT_TEST_DATABASE_URL -u ARIADNE_ARTIFACT_ROOT uv run --frozen pytest -q tests/product --ignore=tests/product/test_postgres_contract.py
````

### Exit Code

````text
0
````

### Output

````text
........................................................................ [ 54%]
...........................................................              [100%]
131 passed in 60.07s (0:01:00)
````

## 06a-12 Verify active database unchanged by isolated tests

### Command

````bash
COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT COALESCE(SUM(n_live_tup),0) FROM pg_stat_user_tables WHERE relname LIKE 'product_%';")"; printf "estimated_product_rows=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
estimated_product_rows=0
````

## 06a-13 Verify active artifact storage unchanged by isolated tests

### Command

````bash
COUNT="$(docker exec ariadne-e1a-api-1 sh -lc 'find /state -type f | wc -l')"; printf "artifact_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
artifact_file_count=0
````

## 06a-14 Run Compose Product Golden Path

### Command

````bash
timeout 300 env ARIADNE_GOLDEN_PATH_BASE_URL=http://127.0.0.1:18000/api/v1 uv run --frozen python tests/product/compose_golden_path_smoke.py
````

### Exit Code

````text
0
````

### Output

````text
{'project_id': 'bf6ade7b-ae94-457c-b921-ed70e04fedba', 'dataset_version_id': 'f7eee1e3-b6b0-40f1-8abe-d4eaed558c49', 'discovery_results': 3, 'estimation_results': 3, 'root_result_id': '9203bd6d-abbc-47a4-9bc2-bc5ea061f98c', 'status': 'PASS'}
````

## 06a-15 API health after Golden Path

### Command

````bash
curl --fail --silent --show-error --include --max-time 10 http://127.0.0.1:18000/health/ready
````

### Exit Code

````text
0
````

### Output

````text
HTTP/1.1 200 OK
date: Sat, 08 Aug 2026 07:07:24 GMT
server: uvicorn
content-length: 15
content-type: application/json
x-request-id: c81fa45b-5032-48e0-9127-adf4fc311707

{"status":"ok"}
````

## 06a-16 Worker state after Golden Path

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"
````

### Exit Code

````text
0
````

### Output

````text
status=running
````

## 06a-17 Verify Golden Path created execution data

### Command

````bash
COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_execution;")"; printf "product_execution=%s\n" "$COUNT"; test "$COUNT" -gt 0
````

### Exit Code

````text
0
````

### Output

````text
product_execution=7
````

## 06a-18 Verify Golden Path created result data

### Command

````bash
COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_result;")"; printf "product_result=%s\n" "$COUNT"; test "$COUNT" -gt 0
````

### Exit Code

````text
0
````

### Output

````text
product_result=11
````

## 06a-19 Verify Golden Path created lineage data

### Command

````bash
COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_lineage_edge;")"; printf "product_lineage_edge=%s\n" "$COUNT"; test "$COUNT" -gt 0
````

### Exit Code

````text
1
````

### Output

````text
product_lineage_edge=0
````

## Completion

- Finished at: `2026-08-08T07:07:25+00:00`
- Phase execution: `ABORTED`
- Reason: `Golden Path produced no lineage edges`
- Final clean reinitialization: `NOT EXECUTED`
