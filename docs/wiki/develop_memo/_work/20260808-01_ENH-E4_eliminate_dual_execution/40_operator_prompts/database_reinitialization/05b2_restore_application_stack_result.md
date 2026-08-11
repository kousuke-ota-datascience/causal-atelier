# 05b2 Restore Application Stack Result

## Metadata

- Prompt: `05b2_restore_application_stack_prompt.md`
- Started at: `2026-08-08T06:57:50+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `d7fcae7c06f07f0045765a0aee0c05eaaad26fd5`
- Target Compose project: `ariadne-e1a`
- Restore scope: `api + worker + frontend + artifact persistence`
- Known allowed diff: `D deploy/.nfs000000000076202f00000088`

> Application restore retry after explicit assessment of the known NFS temporary-file diff.

## 05b2-01 Current branch precondition

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

## 05b2-02 Runtime-area tracked differences

### Command

````bash
git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy
````

### Exit Code

````text
0
````

### Output

````text
D	deploy/.nfs000000000076202f00000088
````

## 05b2-03 Verify only known NFS deletion is present

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

## 05b2-04 Verify assessed NFS blob still matches nginx.conf

### Command

````bash
git show HEAD:deploy/.nfs000000000076202f00000088 | cmp - deploy/nginx.conf
````

### Exit Code

````text
0
````

### Output

````text
````

## 05b2-05 Docker daemon access

### Command

````bash
docker version --format "client={{.Client.Version}} server={{.Server.Version}}"
````

### Exit Code

````text
0
````

### Output

````text
client=29.6.2 server=29.6.2
````

## 05b2-06 Database health precondition

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"
````

### Exit Code

````text
0
````

### Output

````text
running/healthy
````

## 05b2-07 Migration completion precondition

### Command

````bash
EXIT_CODE="$(docker inspect ariadne-e1a-migrate-1 --format "{{.State.ExitCode}}")"; printf "migration_exit_code=%s\n" "$EXIT_CODE"; test "$EXIT_CODE" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
migration_exit_code=0
````

## 05b2-08 Product revision precondition

### Command

````bash
REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"
````

### Exit Code

````text
0
````

### Output

````text
product_revision=20260807_product_0006
````

## 05b2-09 Verify legacy Alembic table absent before restore

### Command

````bash
VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('public.alembic_version');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"
````

### Exit Code

````text
0
````

### Output

````text
legacy_version_table=NULL
````

## 05b2-10 Verify artifact volume absent before restore

### Command

````bash
if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: ariadne-e1a_artifact-data
````

## 05b2-11 Verify application services absent before restore

### Command

````bash
for service in api worker frontend; do COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --filter label=com.docker.compose.service="$service" -q | wc -l)"; printf "%s_container_count=%s\n" "$service" "$COUNT"; test "$COUNT" -eq 0 || exit 1; done
````

### Exit Code

````text
0
````

### Output

````text
api_container_count=0
worker_container_count=0
frontend_container_count=0
````

## 05b2-12 Restore application services

### Command

````bash
docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build api worker frontend
````

### Exit Code

````text
0
````

### Output

````text
 Image ariadne-e1a-worker Building 
 Image ariadne-e1a-migrate Building 
 Image ariadne-e1a-api Building 
#1 [internal] load local bake definitions
#1 reading from stdin 1.46kB done
#1 DONE 0.0s

#2 [migrate internal] load build definition from Dockerfile
#2 DONE 0.0s

#2 [migrate internal] load build definition from Dockerfile
#2 transferring dockerfile: 957B done
#2 DONE 0.0s

#3 [migrate internal] load metadata for docker.io/library/python:3.12-slim
#3 DONE 1.3s

#4 [api internal] load .dockerignore
#4 transferring context: 843B 0.0s done
#4 DONE 0.0s

#5 [api  1/11] FROM docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
#5 resolve docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36 0.0s done
#5 DONE 0.1s

#6 [migrate internal] load build context
#6 transferring context: 42.31kB 0.0s done
#6 DONE 0.1s

#7 [api  3/11] WORKDIR /app
#7 CACHED

#8 [api  4/11] RUN groupadd --system causal && useradd --system --gid causal --home /app causal
#8 CACHED

#9 [api  8/11] RUN uv sync --frozen --no-dev --no-cache
#9 CACHED

#10 [api  5/11] COPY --chmod=0644 pyproject.toml uv.lock README.md ./
#10 CACHED

#11 [api  7/11] COPY --chmod=0755 src ./src
#11 CACHED

#12 [api  9/11] COPY --chmod=0644 alembic_product.ini ./
#12 CACHED

#13 [api  2/11] RUN pip install --no-cache-dir uv==0.8.3
#13 CACHED

#14 [api  6/11] RUN uv sync --frozen --no-dev --no-install-project --no-cache
#14 CACHED

#15 [api 10/11] COPY --chmod=0755 product_migrations ./product_migrations
#15 CACHED

#16 [api 11/11] RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state
#16 CACHED

#17 [migrate] exporting to image
#17 exporting layers 0.0s done
#17 exporting manifest sha256:3535c84957a72e97520d6d2d46f6f4bf73289c72c567b99d28f1534320a15517 0.0s done
#17 exporting config sha256:8098ac2610ff57065e9732280e0bfb13cd8e521185ae1c37530dff7679a8d6c7 0.0s done
#17 exporting attestation manifest sha256:7438a732c66f7b04f0c3b69055533246f48a1e1f78120f7f1df75b3f949d0c92
#17 exporting attestation manifest sha256:7438a732c66f7b04f0c3b69055533246f48a1e1f78120f7f1df75b3f949d0c92 0.2s done
#17 exporting manifest list sha256:c83e9bb60fac84159337f6360b34f34d6c112879adc896ef337aef224f3cc738 0.1s done
#17 naming to docker.io/library/ariadne-e1a-migrate:latest
#17 naming to docker.io/library/ariadne-e1a-migrate:latest 0.0s done
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest 0.1s done
#17 DONE 0.7s

#18 [worker] exporting to image
#18 exporting layers 0.0s done
#18 exporting manifest sha256:75ace132be83a262c1a97ba9fccfa0adda2e92ae7689c63f3ce50c48eb00b343 0.0s done
#18 exporting config sha256:2ce3b9967ccee967f046e8f9be89ef0b9ef7eec34f53cf0469617c26f45f199d 0.1s done
#18 exporting attestation manifest sha256:5865ed9bf2ee5b4cc872945ce84134fb6f52aba285ff8aafdec9b854d86d8443 0.2s done
#18 exporting manifest list sha256:75842de19ee84f3c66f14bfd38cb35cffe85687e45d552664f84ae294eb80b00 0.1s done
#18 naming to docker.io/library/ariadne-e1a-worker:latest 0.0s done
#18 unpacking to docker.io/library/ariadne-e1a-worker:latest 0.0s done
#18 DONE 0.8s

#19 [api] exporting to image
#19 exporting layers done
#19 exporting manifest sha256:33d384c70354985940c2b9133ee1643cfcf3a958f7a232b468800e923febb786 0.0s done
#19 exporting config sha256:0595f75a6b16d5c88515c547b5f7db124dcc7ae25fc2192835deeb84336559de 0.1s done
#19 exporting attestation manifest sha256:7537bfc95d78d52d78ccb2c9fbdbb69c6d36e74bd948725d4fb27696c8e839a9 0.2s done
#19 exporting manifest list sha256:26960380de462af291cbcec4048b15975acd7f48d028e4f727cd143647b54898 0.1s done
#19 naming to docker.io/library/ariadne-e1a-api:latest 0.0s done
#19 unpacking to docker.io/library/ariadne-e1a-api:latest 0.1s done
#19 DONE 0.8s

#20 [migrate] resolving provenance for metadata file
#20 DONE 0.2s

#21 [worker] resolving provenance for metadata file
#21 DONE 0.1s

#22 [api] resolving provenance for metadata file
#22 DONE 0.0s
 Image ariadne-e1a-api Built 
 Image ariadne-e1a-migrate Built 
 Image ariadne-e1a-worker Built 
 Volume ariadne-e1a_artifact-data Creating 
 Volume ariadne-e1a_artifact-data Created 
 Container ariadne-e1a-database-1 Running 
 Container ariadne-e1a-migrate-1 Recreate 
 Container ariadne-e1a-migrate-1 Recreated 
 Container ariadne-e1a-worker-1 Creating 
 Container ariadne-e1a-api-1 Creating 
 Container ariadne-e1a-worker-1 Created 
 Container ariadne-e1a-api-1 Created 
 Container ariadne-e1a-frontend-1 Creating 
 Container ariadne-e1a-frontend-1 Created 
 Container ariadne-e1a-database-1 Waiting 
 Container ariadne-e1a-database-1 Healthy 
 Container ariadne-e1a-migrate-1 Starting 
 Container ariadne-e1a-migrate-1 Started 
 Container ariadne-e1a-migrate-1 Waiting 
 Container ariadne-e1a-migrate-1 Waiting 
 Container ariadne-e1a-migrate-1 Exited 
 Container ariadne-e1a-api-1 Starting 
 Container ariadne-e1a-migrate-1 Exited 
 Container ariadne-e1a-worker-1 Starting 
 Container ariadne-e1a-api-1 Started 
 Container ariadne-e1a-api-1 Waiting 
 Container ariadne-e1a-worker-1 Started 
 Container ariadne-e1a-api-1 Healthy 
 Container ariadne-e1a-frontend-1 Starting 
 Container ariadne-e1a-frontend-1 Started 
````

## 05b2-13 Wait for API health

### Command

````bash
timeout 120 sh -c 'until [ "$(docker inspect ariadne-e1a-api-1 --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}" 2>/dev/null)" = "healthy" ]; do sleep 2; done'
````

### Exit Code

````text
0
````

### Output

````text
````

## 05b2-14 API container state

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

## 05b2-15 Worker container state

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

## 05b2-16 Frontend container state

### Command

````bash
STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"
````

### Exit Code

````text
0
````

### Output

````text
status=running
````

## 05b2-17 Active Compose project inventory

### Command

````bash
docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES                    STATUS                      service
1ee441b739cf   ariadne-e1a-frontend-1   Up Less than a second       frontend
5a07b9279add   ariadne-e1a-api-1        Up 12 seconds (healthy)     api
93b71e3e01d2   ariadne-e1a-worker-1     Up 12 seconds               worker
189944a5d65b   ariadne-e1a-migrate-1    Exited (0) 13 seconds ago   migrate
965f98f75c79   ariadne-e1a-database-1   Up 7 minutes (healthy)      database
````

## 05b2-18 Host API readiness request

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
date: Sat, 08 Aug 2026 06:58:10 GMT
server: uvicorn
content-length: 15
content-type: application/json
x-request-id: 7c85076b-a749-4654-9907-9f2d44e92015

{"status":"ok"}
````

## 05b2-19 Host frontend request

### Command

````bash
STATUS="$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" --max-time 10 http://127.0.0.1:18080/)"; printf "http_status=%s\n" "$STATUS"; test "$STATUS" -ge 200 -a "$STATUS" -lt 400
````

### Exit Code

````text
0
````

### Output

````text
http_status=200
````

## 05b2-20 Recreated artifact volume identity

### Command

````bash
IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a/artifact-data
````

## 05b2-21 API artifact volume mount

### Command

````bash
VOLUME="$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_artifact-data
````

## 05b2-22 Worker artifact volume mount

### Command

````bash
VOLUME="$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_artifact-data
````

## 05b2-23 Artifact storage initial state

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; printf "state_dirs="; find /state -type d | wc -l; du -sh /state /state/objects'
````

### Exit Code

````text
0
````

### Output

````text
state_files=0
object_files=0
state_dirs=3
12K	/state
````

## 05b2-24 Verify legacy Alembic table remains absent

### Command

````bash
VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('public.alembic_version');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"
````

### Exit Code

````text
0
````

### Output

````text
legacy_version_table=NULL
````

## 05b2-25 Product revision after application startup

### Command

````bash
REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"
````

### Exit Code

````text
0
````

### Output

````text
product_revision=20260807_product_0006
````

## 05b2-26 Exact row counts after application startup

### Command

````bash
printf "%s\n" "SELECT format('SELECT %L AS table_name, count(*) AS row_count FROM public.%I;', tablename, tablename) FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off
````

### Exit Code

````text
0
````

### Output

````text
       table_name        | row_count 
-------------------------+-----------
 alembic_version_product |         1
(1 row)

           table_name           | row_count 
--------------------------------+-----------
 product_analysis_specification |         0
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_analysis_view |         0
(1 row)

     table_name     | row_count 
--------------------+-----------
 product_annotation |         0
(1 row)

    table_name    | row_count 
------------------+-----------
 product_artifact |         0
(1 row)

       table_name        | row_count 
-------------------------+-----------
 product_dataset_version |         0
(1 row)

    table_name     | row_count 
-------------------+-----------
 product_execution |         0
(1 row)

       table_name       | row_count 
------------------------+-----------
 product_execution_plan |         0
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_export_bundle |         0
(1 row)

       table_name        | row_count 
-------------------------+-----------
 product_family_artifact |         0
(1 row)

        table_name        | row_count 
--------------------------+-----------
 product_family_execution |         0
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_family_result |         0
(1 row)

           table_name           | row_count 
--------------------------------+-----------
 product_family_stage_execution |         0
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_graph_version |         0
(1 row)

     table_name      | row_count 
---------------------+-----------
 product_idempotency |         0
(1 row)

      table_name      | row_count 
----------------------+-----------
 product_lineage_edge |         0
(1 row)

   table_name    | row_count 
-----------------+-----------
 product_project |         0
(1 row)

         table_name         | row_count 
----------------------------+-----------
 product_project_membership |         0
(1 row)

            table_name            | row_count 
----------------------------------+-----------
 product_research_context_version |         0
(1 row)

   table_name   | row_count 
----------------+-----------
 product_result |         0
(1 row)

          table_name          | row_count 
------------------------------+-----------
 product_workspace_annotation |         0
(1 row)

         table_name          | row_count 
-----------------------------+-----------
 product_workspace_selection |         0
(1 row)

````

## 05b2-27 Verify stale non-target volumes remain untouched

### Command

````bash
for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done
````

### Exit Code

````text
0
````

### Output

````text
PRESERVED: causal-atelier_metadata-data
PRESERVED: causal-atelier_artifact-data
````

## Completion

- Finished at: `2026-08-08T06:58:12+00:00`
- Phase execution: `COMPLETED`
- Database: `RUNNING / HEALTHY`
- API: `RUNNING / HEALTHY`
- Worker: `RUNNING`
- Frontend: `RUNNING`
- Artifact persistence: `RECREATED`
- Known NFS deletion diff: `PRESERVED / NOT MODIFIED`
