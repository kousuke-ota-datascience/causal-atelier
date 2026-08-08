# 06b0 Final Clean Reinitialization Result

## Metadata

- Prompt: `06b0_final_clean_reinitialization_prompt.md`
- Started at: `2026-08-08T07:22:49+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `b3a1d4786fed42d401cbfd55ad6ad12c318bdaea`
- Target Compose project: `ariadne-e1a`

> Final removal of temporary functional-verification data followed by clean rebuild.

## 06b0-01 Current branch precondition

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

## 06b0-02 Verify known runtime diff only

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

## 06b0-03 Docker daemon access

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

## 06b0-04 Active project state before final reset

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
1ee441b739cf   ariadne-e1a-frontend-1   Up 24 minutes               frontend
5a07b9279add   ariadne-e1a-api-1        Up 24 minutes (healthy)     api
93b71e3e01d2   ariadne-e1a-worker-1     Up 24 minutes               worker
189944a5d65b   ariadne-e1a-migrate-1    Exited (0) 24 minutes ago   migrate
965f98f75c79   ariadne-e1a-database-1   Up 31 minutes (healthy)     database
````

## 06b0-05 Verify active metadata volume identity

### Command

````bash
IDENTITY="$(docker volume inspect ariadne-e1a_metadata-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/metadata-data"
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a/metadata-data
````

## 06b0-06 Verify active artifact volume identity

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

## 06b0-07 Temporary Product row counts before final reset

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
 product_annotation |         1
(1 row)

    table_name    | row_count 
------------------+-----------
 product_artifact |        13
(1 row)

       table_name        | row_count 
-------------------------+-----------
 product_dataset_version |         1
(1 row)

    table_name     | row_count 
-------------------+-----------
 product_execution |         7
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
 product_graph_version |         2
(1 row)

     table_name      | row_count 
---------------------+-----------
 product_idempotency |         6
(1 row)

      table_name      | row_count 
----------------------+-----------
 product_lineage_edge |         0
(1 row)

   table_name    | row_count 
-----------------+-----------
 product_project |         1
(1 row)

         table_name         | row_count 
----------------------------+-----------
 product_project_membership |         1
(1 row)

            table_name            | row_count 
----------------------------------+-----------
 product_research_context_version |         0
(1 row)

   table_name   | row_count 
----------------+-----------
 product_result |        11
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

## 06b0-08 Temporary artifact state before final reset

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; du -sh /state /state/objects'
````

### Exit Code

````text
0
````

### Output

````text
state_files=13
object_files=13
152K	/state
````

## 06b0-09 Stop active Compose stack

### Command

````bash
docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml stop
````

### Exit Code

````text
0
````

### Output

````text
 Container ariadne-e1a-frontend-1 Stopping 
 Container ariadne-e1a-worker-1 Stopping 
 Container ariadne-e1a-frontend-1 Stopped 
 Container ariadne-e1a-api-1 Stopping 
 Container ariadne-e1a-api-1 Stopped 
 Container ariadne-e1a-worker-1 Stopped 
 Container ariadne-e1a-migrate-1 Stopping 
 Container ariadne-e1a-migrate-1 Stopped 
 Container ariadne-e1a-database-1 Stopping 
 Container ariadne-e1a-database-1 Stopped 
````

## 06b0-10 Verify no active-project container is running

### Command

````bash
COUNT="$(docker ps --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "running_container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
running_container_count=0
````

## 06b0-11 Remove stopped active Compose containers

### Command

````bash
docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml rm -f -s
````

### Exit Code

````text
0
````

### Output

````text
 Container ariadne-e1a-frontend-1 Stopping 
 Container ariadne-e1a-worker-1 Stopping 
 Container ariadne-e1a-worker-1 Stopped 
 Container ariadne-e1a-frontend-1 Stopped 
 Container ariadne-e1a-api-1 Stopping 
 Container ariadne-e1a-api-1 Stopped 
 Container ariadne-e1a-migrate-1 Stopping 
 Container ariadne-e1a-migrate-1 Stopped 
 Container ariadne-e1a-database-1 Stopping 
 Container ariadne-e1a-database-1 Stopped 
Going to remove ariadne-e1a-frontend-1, ariadne-e1a-api-1, ariadne-e1a-worker-1, ariadne-e1a-migrate-1, ariadne-e1a-database-1
 Container ariadne-e1a-api-1 Removing 
 Container ariadne-e1a-frontend-1 Removing 
 Container ariadne-e1a-worker-1 Removing 
 Container ariadne-e1a-migrate-1 Removing 
 Container ariadne-e1a-database-1 Removing 
 Container ariadne-e1a-frontend-1 Removed 
 Container ariadne-e1a-worker-1 Removed 
 Container ariadne-e1a-database-1 Removed 
 Container ariadne-e1a-api-1 Removed 
 Container ariadne-e1a-migrate-1 Removed 
````

## 06b0-12 Verify active-project containers absent

### Command

````bash
COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
container_count=0
````

## 06b0-13 Verify metadata volume has zero consumers

### Command

````bash
COUNT="$(docker ps -a --filter volume=ariadne-e1a_metadata-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
consumer_count=0
````

## 06b0-14 Verify artifact volume has zero consumers

### Command

````bash
COUNT="$(docker ps -a --filter volume=ariadne-e1a_artifact-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
consumer_count=0
````

## 06b0-15 Delete active metadata volume

### Command

````bash
docker volume rm ariadne-e1a_metadata-data
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_metadata-data
````

## 06b0-16 Delete active artifact volume

### Command

````bash
docker volume rm ariadne-e1a_artifact-data
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_artifact-data
````

## 06b0-17 Verify active persistence absent

### Command

````bash
for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESENT: %s\n" "$v"; exit 1; else printf "ABSENT: %s\n" "$v"; fi; done
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: ariadne-e1a_metadata-data
ABSENT: ariadne-e1a_artifact-data
````

## 06b0-18 Rebuild database and Product migration

### Command

````bash
docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build database migrate
````

### Exit Code

````text
0
````

### Output

````text
 Image ariadne-e1a-migrate Building 
#1 [internal] load local bake definitions
#1 reading from stdin 552B done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 132B
#2 transferring dockerfile: 957B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.12-slim
#3 DONE 1.6s

#4 [internal] load .dockerignore
#4 transferring context: 843B done
#4 DONE 0.0s

#5 [ 1/11] FROM docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
#5 resolve docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36 0.0s done
#5 DONE 0.0s

#6 [internal] load build context
#6 transferring context: 42.31kB 0.1s done
#6 DONE 0.1s

#7 [10/11] COPY --chmod=0755 product_migrations ./product_migrations
#7 CACHED

#8 [ 2/11] RUN pip install --no-cache-dir uv==0.8.3
#8 CACHED

#9 [ 3/11] WORKDIR /app
#9 CACHED

#10 [ 4/11] RUN groupadd --system causal && useradd --system --gid causal --home /app causal
#10 CACHED

#11 [ 9/11] COPY --chmod=0644 alembic_product.ini ./
#11 CACHED

#12 [ 5/11] COPY --chmod=0644 pyproject.toml uv.lock README.md ./
#12 CACHED

#13 [ 6/11] RUN uv sync --frozen --no-dev --no-install-project --no-cache
#13 CACHED

#14 [ 7/11] COPY --chmod=0755 src ./src
#14 CACHED

#15 [ 8/11] RUN uv sync --frozen --no-dev --no-cache
#15 CACHED

#16 [11/11] RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state
#16 CACHED

#17 exporting to image
#17 exporting layers done
#17 exporting manifest sha256:3535c84957a72e97520d6d2d46f6f4bf73289c72c567b99d28f1534320a15517 done
#17 exporting config sha256:8098ac2610ff57065e9732280e0bfb13cd8e521185ae1c37530dff7679a8d6c7 done
#17 exporting attestation manifest sha256:0a400a66701e3f6a96f98e72dc184321d8b6c6ab4291d15b42008eb9b9f85d05 0.0s done
#17 exporting manifest list sha256:4e5fefb9bbe2048b72652f47a7e9549735e36463647a18d6c578914ee25acf16 0.0s done
#17 naming to docker.io/library/ariadne-e1a-migrate:latest
#17 naming to docker.io/library/ariadne-e1a-migrate:latest done
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest 0.0s done
#17 DONE 0.2s

#18 resolving provenance for metadata file
#18 DONE 0.0s
 Image ariadne-e1a-migrate Built 
 Volume ariadne-e1a_metadata-data Creating 
 Volume ariadne-e1a_metadata-data Created 
 Container ariadne-e1a-database-1 Creating 
 Container ariadne-e1a-database-1 Created 
 Container ariadne-e1a-migrate-1 Creating 
 Container ariadne-e1a-migrate-1 Created 
 Container ariadne-e1a-database-1 Starting 
 Container ariadne-e1a-database-1 Started 
 Container ariadne-e1a-database-1 Waiting 
 Container ariadne-e1a-database-1 Healthy 
 Container ariadne-e1a-migrate-1 Starting 
 Container ariadne-e1a-migrate-1 Started 
````

## 06b0-19 Wait for Product migration completion

### Command

````bash
timeout 120 docker wait ariadne-e1a-migrate-1
````

### Exit Code

````text
0
````

### Output

````text
0
````

## 06b0-20 Verify Product migration exit code

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

## 06b0-21 Record Product migration logs

### Command

````bash
docker logs ariadne-e1a-migrate-1
````

### Exit Code

````text
0
````

### Output

````text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 20260805_product_0001, 20260805_0001_product_domain_baseline
INFO  [alembic.runtime.migration] Running upgrade 20260805_product_0001 -> 20260806_product_0002, ENH-E1 scientific validity foundation.
INFO  [alembic.runtime.migration] Running upgrade 20260806_product_0002 -> 20260806_product_0003, ENH-E2 outcome inheritance for Graph Version.
INFO  [alembic.runtime.migration] Running upgrade 20260806_product_0003 -> 20260807_product_0004, ENH-E3 generic workspace and exploratory persistence.
INFO  [alembic.runtime.migration] Running upgrade 20260807_product_0004 -> 20260807_product_0005, ENH-E3 G4 Research Context, Analysis Specification, and predictive references.
INFO  [alembic.runtime.migration] Running upgrade 20260807_product_0005 -> 20260807_product_0006, ENH-E3 G6 workspace closure, annotations, access, and export bundles.
````

## 06b0-22 Verify rebuilt database health

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

## 06b0-23 Verify Product revision

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

## 06b0-24 Verify legacy Alembic table absent after rebuild

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

## 06b0-25 Verify no unexpected public tables after rebuild

### Command

````bash
UNEXPECTED="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename <> 'alembic_version_product' AND tablename NOT LIKE 'product_%' ORDER BY tablename;")"; printf "%s\n" "$UNEXPECTED"; test -z "$UNEXPECTED"
````

### Exit Code

````text
0
````

### Output

````text

````

## 06b0-26 Exact row counts before application startup

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

## 06b0-27 Assert Product application row total is zero before startup

### Command

````bash
TOTAL=0; while IFS= read -r table; do COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM public.${table};")"; TOTAL=$((TOTAL + COUNT)); done < <(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'product_%' ORDER BY tablename;"); printf "product_application_row_total=%s\n" "$TOTAL"; test "$TOTAL" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
product_application_row_total=0
````

## 06b0-28 Verify artifact volume absent before application restore

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

## 06b0-29 Restore API worker and frontend

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
 Image ariadne-e1a-migrate Building 
 Image ariadne-e1a-api Building 
 Image ariadne-e1a-worker Building 
#1 [internal] load local bake definitions
#1 reading from stdin 1.46kB done
#1 DONE 0.0s

#2 [worker internal] load build definition from Dockerfile
#2 transferring dockerfile: 957B 0.0s done
#2 DONE 0.0s

#3 [migrate internal] load metadata for docker.io/library/python:3.12-slim
#3 DONE 0.3s

#4 [migrate internal] load .dockerignore
#4 transferring context: 843B 0.0s done
#4 DONE 0.0s

#5 [api internal] load build context
#5 DONE 0.0s

#6 [api  1/11] FROM docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
#6 resolve docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36 0.0s done
#6 DONE 0.1s

#5 [migrate internal] load build context
#5 transferring context: 42.31kB 0.1s done
#5 transferring context: 42.31kB 0.1s done
#5 DONE 0.1s

#7 [worker  5/11] COPY --chmod=0644 pyproject.toml uv.lock README.md ./
#7 CACHED

#8 [worker  7/11] COPY --chmod=0755 src ./src
#8 CACHED

#9 [worker  6/11] RUN uv sync --frozen --no-dev --no-install-project --no-cache
#9 CACHED

#10 [worker 10/11] COPY --chmod=0755 product_migrations ./product_migrations
#10 CACHED

#11 [worker  3/11] WORKDIR /app
#11 CACHED

#12 [worker  4/11] RUN groupadd --system causal && useradd --system --gid causal --home /app causal
#12 CACHED

#13 [worker  8/11] RUN uv sync --frozen --no-dev --no-cache
#13 CACHED

#14 [worker  9/11] COPY --chmod=0644 alembic_product.ini ./
#14 CACHED

#15 [worker  2/11] RUN pip install --no-cache-dir uv==0.8.3
#15 CACHED

#16 [worker 11/11] RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state
#16 CACHED

#17 [migrate] exporting to image
#17 exporting layers 0.0s done
#17 exporting manifest sha256:3535c84957a72e97520d6d2d46f6f4bf73289c72c567b99d28f1534320a15517 0.0s done
#17 exporting config sha256:8098ac2610ff57065e9732280e0bfb13cd8e521185ae1c37530dff7679a8d6c7 done
#17 exporting attestation manifest sha256:3b3ff07d9da7daf0396c842653195ead66618eb138ea601737aa86dbfe079934
#17 exporting attestation manifest sha256:3b3ff07d9da7daf0396c842653195ead66618eb138ea601737aa86dbfe079934 0.1s done
#17 exporting manifest list sha256:536513258b6d0750149356d12ad4cf073c33bd3039de017c297ddbe31bf04ae4
#17 exporting manifest list sha256:536513258b6d0750149356d12ad4cf073c33bd3039de017c297ddbe31bf04ae4 0.1s done
#17 naming to docker.io/library/ariadne-e1a-migrate:latest 0.0s done
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest 0.0s done
#17 DONE 0.4s

#18 [api] exporting to image
#18 exporting layers done
#18 exporting manifest sha256:33d384c70354985940c2b9133ee1643cfcf3a958f7a232b468800e923febb786 done
#18 exporting config sha256:0595f75a6b16d5c88515c547b5f7db124dcc7ae25fc2192835deeb84336559de done
#18 exporting attestation manifest sha256:be255d9b380db86754f98eed2bec37acab9c0ac471dba079f7cd0cd23b7afac0 0.1s done
#18 exporting manifest list sha256:1eceec47dbc1a033fd010935bdf3e766bbd0f9bebeddf3c7b3444b5ec3dcd341 0.1s done
#18 naming to docker.io/library/ariadne-e1a-api:latest 0.0s done
#18 unpacking to docker.io/library/ariadne-e1a-api:latest 0.1s done
#18 DONE 0.4s

#19 [worker] exporting to image
#19 exporting layers 0.0s done
#19 exporting manifest sha256:75ace132be83a262c1a97ba9fccfa0adda2e92ae7689c63f3ce50c48eb00b343 0.0s done
#19 exporting config sha256:2ce3b9967ccee967f046e8f9be89ef0b9ef7eec34f53cf0469617c26f45f199d 0.0s done
#19 exporting attestation manifest sha256:dbfb3ac908522413b3626c3e024edab08c276887e6c12a6be04dee5257c9dfe2 0.1s done
#19 exporting manifest list sha256:073eb03e8a6eb15f52241ab9928dc81b54b9af22ed32499fd24f7c2ea005a5ba 0.0s done
#19 naming to docker.io/library/ariadne-e1a-worker:latest 0.0s done
#19 unpacking to docker.io/library/ariadne-e1a-worker:latest 0.0s done
#19 DONE 0.5s

#20 [api] resolving provenance for metadata file
#20 DONE 0.1s

#21 [migrate] resolving provenance for metadata file
#21 DONE 0.1s

#22 [worker] resolving provenance for metadata file
#22 DONE 0.0s
 Image ariadne-e1a-migrate Built 
 Image ariadne-e1a-api Built 
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
 Container ariadne-e1a-worker-1 Starting 
 Container ariadne-e1a-migrate-1 Exited 
 Container ariadne-e1a-api-1 Starting 
 Container ariadne-e1a-worker-1 Started 
 Container ariadne-e1a-api-1 Started 
 Container ariadne-e1a-api-1 Waiting 
 Container ariadne-e1a-api-1 Healthy 
 Container ariadne-e1a-frontend-1 Starting 
 Container ariadne-e1a-frontend-1 Started 
````

## 06b0-30 Wait for API health

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

## 06b0-31 Final Compose project state

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
c13e8ed52c38   ariadne-e1a-frontend-1   Up Less than a second       frontend
dc225749a393   ariadne-e1a-api-1        Up 11 seconds (healthy)     api
556c6c87ddaa   ariadne-e1a-worker-1     Up 11 seconds               worker
b50c826a3837   ariadne-e1a-migrate-1    Exited (0) 12 seconds ago   migrate
33bde72e228c   ariadne-e1a-database-1   Up 29 seconds (healthy)     database
````

## 06b0-32 Final database health

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

## 06b0-33 Final API health

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

## 06b0-34 Final worker state

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

## 06b0-35 Final frontend state

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

## 06b0-36 Final API readiness endpoint

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
date: Sat, 08 Aug 2026 07:23:25 GMT
server: uvicorn
content-length: 15
content-type: application/json
x-request-id: e1b16a6c-6355-45b0-a35f-cbad2c5ce819

{"status":"ok"}
````

## 06b0-37 Final frontend endpoint

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

## 06b0-38 Final artifact volume identity

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

## 06b0-39 Final API artifact mount

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

## 06b0-40 Final worker artifact mount

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

## 06b0-41 Final artifact storage emptiness

### Command

````bash
docker exec ariadne-e1a-api-1 sh -lc 'set -eu; STATE_FILES="$(find /state -type f | wc -l)"; OBJECT_FILES="$(find /state/objects -type f | wc -l)"; printf "state_files=%s\n" "$STATE_FILES"; printf "object_files=%s\n" "$OBJECT_FILES"; test "$STATE_FILES" -eq 0; test "$OBJECT_FILES" -eq 0; du -sh /state /state/objects'
````

### Exit Code

````text
0
````

### Output

````text
state_files=0
object_files=0
12K	/state
````

## 06b0-42 Final Product application row total

### Command

````bash
TOTAL=0; while IFS= read -r table; do COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM public.${table};")"; TOTAL=$((TOTAL + COUNT)); done < <(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE 'product_%' ORDER BY tablename;"); printf "product_application_row_total=%s\n" "$TOTAL"; test "$TOTAL" -eq 0
````

### Exit Code

````text
0
````

### Output

````text
product_application_row_total=0
````

## 06b0-43 Final exact table row counts

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

## 06b0-44 Final legacy Alembic absence

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

## 06b0-45 Final Product revision

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

## 06b0-46 Verify stale non-target volumes remain untouched

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

## 06b0-47 Verify repository-local .ariadne has no files

### Command

````bash
if [ -e .ariadne ]; then COUNT="$(find .ariadne -type f | wc -l)"; printf "ariadne_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0; else printf "%s\n" "ABSENT: .ariadne"; fi
````

### Exit Code

````text
0
````

### Output

````text
ariadne_file_count=0
````

## Completion

- Finished at: `2026-08-08T07:23:28+00:00`
- Phase execution: `COMPLETED`
- Temporary Golden Path data: `DELETED`
- Active database persistence: `RECREATED CLEAN`
- Active artifact persistence: `RECREATED CLEAN`
- Product application rows: `0`
- Artifact files: `0`
- Product migration: `20260807_product_0006`
- Legacy migration state: `ABSENT`
- Database: `RUNNING / HEALTHY`
- API: `RUNNING / HEALTHY`
- Worker: `RUNNING`
- Frontend: `RUNNING`
- Final clean state: `VERIFIED`
