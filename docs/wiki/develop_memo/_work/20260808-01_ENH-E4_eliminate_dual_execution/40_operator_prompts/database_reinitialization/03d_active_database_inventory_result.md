# 03d Active Database Inventory Result

## Metadata

- Prompt: `03d_active_database_inventory_prompt.md`
- Started at: `2026-08-08T06:34:55+00:00`
- Repository root: `/loc0/bigbrother/repositories/causal-atelier`
- Git commit: `b458c9dfe7592db347cb20ebe34e0891ddcd3bf2`
- Target container: `ariadne-e1a-database-1`
- Target database: `ariadne`

> Read-only database inventory. No database state was modified.

## 03d-01 Target container state

### Command

````bash
docker ps --filter name="^/ariadne-e1a-database-1$" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
````

### Exit Code

````text
0
````

### Output

````text
CONTAINER ID   NAMES                    STATUS
df5f53878ef7   ariadne-e1a-database-1   Up 47 hours (healthy)
````

## 03d-02 PostgreSQL identity

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

## 03d-03 PostgreSQL database size

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"
````

### Exit Code

````text
0
````

### Output

````text
 database_size 
---------------
 13 MB
(1 row)

````

## 03d-04 Public schema tables

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

## 03d-05 Alembic version table presence

### Command

````bash
docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT to_regclass('public.alembic_version') AS legacy_version_table, to_regclass('public.alembic_version_product') AS product_version_table;"
````

### Exit Code

````text
0
````

### Output

````text
 legacy_version_table |  product_version_table  
----------------------+-------------------------
                      | alembic_version_product
(1 row)

````

## 03d-06 Legacy Alembic revision

### Command

````bash
if [ "$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('public.alembic_version') IS NOT NULL;")" = "t" ]; then docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version"; fi
````

### Exit Code

````text
0
````

### Output

````text
ABSENT: alembic_version
````

## 03d-07 Product Alembic revision

### Command

````bash
if [ "$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('public.alembic_version_product') IS NOT NULL;")" = "t" ]; then docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version_product"; fi
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

## 03d-08 Exact row counts for all public tables

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
 product_analysis_specification |         5
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_analysis_view |         7
(1 row)

     table_name     | row_count 
--------------------+-----------
 product_annotation |        59
(1 row)

    table_name    | row_count 
------------------+-----------
 product_artifact |       422
(1 row)

       table_name        | row_count 
-------------------------+-----------
 product_dataset_version |        52
(1 row)

    table_name     | row_count 
-------------------+-----------
 product_execution |       300
(1 row)

       table_name       | row_count 
------------------------+-----------
 product_execution_plan |        17
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_export_bundle |         1
(1 row)

       table_name        | row_count 
-------------------------+-----------
 product_family_artifact |        35
(1 row)

        table_name        | row_count 
--------------------------+-----------
 product_family_execution |        17
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_family_result |        37
(1 row)

           table_name           | row_count 
--------------------------------+-----------
 product_family_stage_execution |        37
(1 row)

      table_name       | row_count 
-----------------------+-----------
 product_graph_version |       108
(1 row)

     table_name      | row_count 
---------------------+-----------
 product_idempotency |       353
(1 row)

      table_name      | row_count 
----------------------+-----------
 product_lineage_edge |       229
(1 row)

   table_name    | row_count 
-----------------+-----------
 product_project |        40
(1 row)

         table_name         | row_count 
----------------------------+-----------
 product_project_membership |        40
(1 row)

            table_name            | row_count 
----------------------------------+-----------
 product_research_context_version |         3
(1 row)

   table_name   | row_count 
----------------+-----------
 product_result |       458
(1 row)

          table_name          | row_count 
------------------------------+-----------
 product_workspace_annotation |         3
(1 row)

         table_name          | row_count 
-----------------------------+-----------
 product_workspace_selection |         4
(1 row)

````

## Completion

- Finished at: `2026-08-08T06:34:56+00:00`
- Phase execution: `COMPLETED`
