# 05a Rebuild Database Result

## Metadata

- Prompt: `05a_rebuild_database_prompt.md`
- Started at: `2026-08-08T06:50:40+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `efc982a8a95130747cda10d4404388e00b074cb9`
- Target Compose project: `ariadne-e1a`
- Rebuild scope: `database + product migration only`

> This phase rebuilds database persistence from the current Product migration chain.

## 05a-01 Current branch precondition

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

## 05a-02 Runtime configuration working-tree precondition

### Command

````bash
git diff --exit-code HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations
````

### Exit Code

````text
0
````

### Output

````text
````

## 05a-03 Docker daemon access precondition

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

## 05a-04 Verify active-project containers absent before rebuild

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

## 05a-05 Verify old metadata volume absent

### Command

````bash
if docker volume inspect ariadne-e1a_metadata-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_metadata-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_metadata-data"; fi
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: ariadne-e1a_metadata-data
````

## 05a-06 Verify old artifact volume absent

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

## 05a-07 Verify stale non-target volumes remain untouched before rebuild

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

## 05a-08 Rebuild database and run Product migration

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
#2 transferring dockerfile: 957B 0.0s done
#2 DONE 0.1s

#3 [internal] load metadata for docker.io/library/python:3.12-slim
#3 DONE 1.7s

#4 [internal] load .dockerignore
#4 transferring context: 843B done
#4 DONE 0.0s

#5 [internal] load build context
#5 DONE 0.0s

#6 [ 1/11] FROM docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36
#6 resolve docker.io/library/python:3.12-slim@sha256:229a2c5bfa27522db7815ea81f9bed70af17ccb9de9fc7ad142b1877b5830d36 0.1s done
#6 DONE 0.1s

#5 [internal] load build context
#5 transferring context: 1.31MB 0.3s done
#5 DONE 0.3s

#7 [ 2/11] RUN pip install --no-cache-dir uv==0.8.3
#7 CACHED

#8 [ 3/11] WORKDIR /app
#8 CACHED

#9 [ 4/11] RUN groupadd --system causal && useradd --system --gid causal --home /app causal
#9 CACHED

#10 [ 5/11] COPY --chmod=0644 pyproject.toml uv.lock README.md ./
#10 CACHED

#11 [ 6/11] RUN uv sync --frozen --no-dev --no-install-project --no-cache
#11 CACHED

#12 [ 7/11] COPY --chmod=0755 src ./src
#12 DONE 0.2s

#13 [ 8/11] RUN uv sync --frozen --no-dev --no-cache
#13 3.137    Building ariadne @ file:///app
#13 4.594       Built ariadne @ file:///app
#13 4.596 Prepared 1 package in 1.47s
#13 4.602 Installed 1 package in 5ms
#13 4.602  + ariadne==0.1.0 (from file:///app)
#13 DONE 4.7s

#14 [ 9/11] COPY --chmod=0644 alembic_product.ini ./
#14 DONE 0.1s

#15 [10/11] COPY --chmod=0755 product_migrations ./product_migrations
#15 DONE 0.1s

#16 [11/11] RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state
#16 DONE 0.3s

#17 exporting to image
#17 exporting layers
#17 exporting layers 0.5s done
#17 exporting manifest sha256:3535c84957a72e97520d6d2d46f6f4bf73289c72c567b99d28f1534320a15517 0.0s done
#17 exporting config sha256:8098ac2610ff57065e9732280e0bfb13cd8e521185ae1c37530dff7679a8d6c7 0.0s done
#17 exporting attestation manifest sha256:334ae81f0f6b461a8f49810c18a7ae02827747b204037043d2bacf354fca0e8c 0.1s done
#17 exporting manifest list sha256:8209ee616b76f90855f213629e9240bb4e51f8d98af34e454b2a403a51c0443d
#17 exporting manifest list sha256:8209ee616b76f90855f213629e9240bb4e51f8d98af34e454b2a403a51c0443d 0.0s done
#17 naming to docker.io/library/ariadne-e1a-migrate:latest done
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest
#17 unpacking to docker.io/library/ariadne-e1a-migrate:latest 0.3s done
#17 DONE 1.1s

#18 resolving provenance for metadata file
#18 DONE 0.1s
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

## 05a-09 Wait for Product migration container completion

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

## 05a-10 Verify Product migration exit code

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

## 05a-11 Record Product migration logs

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

## 05a-12 Verify database container health

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

## 05a-13 Active project containers after database rebuild

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
CONTAINER ID   NAMES                    STATUS                              service
d494b4be5172   ariadne-e1a-migrate-1    Exited (0) Less than a second ago   migrate
965f98f75c79   ariadne-e1a-database-1   Up 8 seconds (healthy)              database
````

## 05a-14 Recreated Compose volumes

### Command

````bash
docker volume ls --filter label=com.docker.compose.project=ariadne-e1a --format "{{.Name}}" | sort
````

### Exit Code

````text
0
````

### Output

````text
ariadne-e1a_metadata-data
````

## 05a-15 Recreated metadata volume identity

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

## 05a-16 PostgreSQL identity after rebuild

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT current_database() AS database_name, current_user AS database_user, current_schema() AS current_schema;"
````

### Exit Code

````text
0
````

### Output

````text
 database_name | database_user | current_schema 
---------------+---------------+----------------
 ariadne       | ariadne       | public
(1 row)

````

## 05a-17 Public tables after Product migration

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
````

### Exit Code

````text
0
````

### Output

````text
            tablename             
----------------------------------
 alembic_version_product
 product_analysis_specification
 product_analysis_view
 product_annotation
 product_artifact
 product_dataset_version
 product_execution
 product_execution_plan
 product_export_bundle
 product_family_artifact
 product_family_execution
 product_family_result
 product_family_stage_execution
 product_graph_version
 product_idempotency
 product_lineage_edge
 product_project
 product_project_membership
 product_research_context_version
 product_result
 product_workspace_annotation
 product_workspace_selection
(22 rows)

````

## 05a-18 Verify legacy Alembic version table absent

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

## 05a-19 Verify Product Alembic version table present

### Command

````bash
VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('public.alembic_version_product');")"; printf "product_version_table=%s\n" "$VALUE"; test "$VALUE" = "alembic_version_product"
````

### Exit Code

````text
0
````

### Output

````text
product_version_table=alembic_version_product
````

## 05a-20 Product Alembic revision after rebuild

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"
````

### Exit Code

````text
0
````

### Output

````text
      version_num      
-----------------------
 20260807_product_0006
(1 row)

````

## 05a-21 Exact row counts after migration and before application startup

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

## 05a-22 Verify API worker and frontend were not started

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

## 05a-23 Verify stale non-target volumes after rebuild

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

- Finished at: `2026-08-08T06:51:00+00:00`
- Phase execution: `COMPLETED`
- Database persistence: `RECREATED`
- Product migration: `COMPLETED`
- Legacy migration: `NOT EXECUTED`
- Application services: `NOT STARTED`
