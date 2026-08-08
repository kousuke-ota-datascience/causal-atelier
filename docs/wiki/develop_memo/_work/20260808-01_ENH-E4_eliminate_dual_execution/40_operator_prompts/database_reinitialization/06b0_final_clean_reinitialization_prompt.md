# 06b0 Final Clean Reinitialization — Human Operator Prompt

## 1. Purpose

これまでのphaseにより、以下が実証された。

* active persistenceを安全に停止・削除できる
* 空DBからProduct migrationのみでschemaを再構築できる
* legacy migrationは不要
* application stackを正常復旧できる
* clean startupではProduct application dataは0件
* clean startupではartifact filesは0件
* isolated Active Product testsはPASSする
* Compose Golden PathはPASSする
* Golden PathによってExecution / Result / Artifact等が実際に生成される
* Result lineage APIは正常なnodes / edgesを返す
* `product_lineage_edge > 0` はGolden Path成功条件ではない

Phase 06aのGolden Pathにより、現在のactive persistenceには一時的なverification dataが存在する。

このphaseでは、それらをすべて破棄し、

> **検証済みだがデータは空である最終稼働状態**

へ戻す。

---

## 2. Final Target State

完了時に以下を満たすこと。

```text
Compose project:
  ariadne-e1a

database:
  running / healthy

api:
  running / healthy

worker:
  running

frontend:
  running

Product migration:
  20260807_product_0006

legacy alembic_version:
  absent

Product application rows:
  0

artifact files:
  0

active metadata volume:
  recreated clean

active artifact volume:
  recreated clean
```

Golden Pathは再実行しない。

---

## 3. Active Persistence Targets

今回再初期化するactive persistenceを以下に固定する。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

---

## 4. Explicit Non-targets

以下には触れない。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

これらはstale Compose project persistenceとして、active environmentの最終検証完了後に別工程で扱う。

また以下にも触れない。

* Docker images
* Git repository
* source code
* migrations
* `.ariadne`
* `.gitignore`
* `deploy/.nfs000000000076202f00000088` のworking-tree差分

---

## 5. Known Working-tree Exception

以下の差分のみ既知の許容差分とする。

```text
D	deploy/.nfs000000000076202f00000088
```

それ以外のruntime-area tracked differenceが存在した場合はABORTする。

このphaseでは当該 `.nfs...` ファイルを復元・変更しない。

---

## 6. Safety Model

このphaseでは以下の順序を固定する。

```text
precondition
    |
    v
temporary verification data record
    |
    v
stop active stack
    |
    v
remove active containers
    |
    v
verify volume consumers = 0
    |
    v
delete active persistence
    |
    v
rebuild database
    |
    v
Product migration
    |
    v
verify empty DB
    |
    v
restore application
    |
    v
verify empty artifact storage
    |
    v
final read-only verification
```

失敗した場合はその時点で停止する。

retryや手動修復は行わない。

---

## 7. Prohibited Operations

以下は禁止する。

* legacy migration
* `alembic.ini` によるupgrade
* manual schema SQL
* manual INSERT / UPDATE / DELETE
* seed投入
* fixture投入
* Golden Path再実行
* test data作成
* source code変更
* migration変更
* configuration変更
* stale `causal-atelier_*` volume削除
* failure後のretry
* failure後の自動修復

---

## 8. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

repository内の任意のdirectoryから実行してよい。

---

## 9. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/06b0_final_clean_reinitialization_result.md'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
RC=$?

if [ "${RC}" -ne 0 ]; then
    printf '%s\n' 'ERROR: current location is not inside a Git worktree.'
    exit 2
fi

RESULT_PATH="${REPO_ROOT}/${RESULT_REL}"
RESULT_DIR="$(dirname "${RESULT_PATH}")"

if [ ! -d "${RESULT_DIR}" ]; then
    printf 'ERROR: result directory does not exist: %s\n' "${RESULT_DIR}"
    exit 3
fi

TMP_RESULT="$(mktemp)"
CMD_OUTPUT="$(mktemp)"

cleanup() {
    rm -f "${TMP_RESULT}" "${CMD_OUTPUT}"
}
trap cleanup EXIT

cd "${REPO_ROOT}" || exit 4

{
    printf '%s\n\n' '# 06b0 Final Clean Reinitialization Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`06b0_final_clean_reinitialization_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '\n'
    printf '%s\n' '> Final removal of temporary functional-verification data followed by clean rebuild.'
} > "${TMP_RESULT}"

record_command() {
    LABEL="$1"
    COMMAND="$2"

    : > "${CMD_OUTPUT}"

    bash -o pipefail -lc "${COMMAND}" > "${CMD_OUTPUT}" 2>&1
    EXIT_CODE=$?

    {
        printf '\n## %s\n\n' "${LABEL}"

        printf '%s\n\n' '### Command'
        printf '%s\n' '````bash'
        printf '%s\n' "${COMMAND}"
        printf '%s\n\n' '````'

        printf '%s\n\n' '### Exit Code'
        printf '%s\n' '````text'
        printf '%s\n' "${EXIT_CODE}"
        printf '%s\n\n' '````'

        printf '%s\n\n' '### Output'
        printf '%s\n' '````text'
        cat "${CMD_OUTPUT}"

        if [ -s "${CMD_OUTPUT}" ]; then
            LAST_BYTE="$(tail -c 1 "${CMD_OUTPUT}" | od -An -t uC | tr -d ' ')"
            if [ "${LAST_BYTE}" != "10" ]; then
                printf '\n'
            fi
        fi

        printf '%s\n' '````'
    } >> "${TMP_RESULT}"

    return "${EXIT_CODE}"
}

abort_phase() {
    REASON="$1"
    EXIT_CODE="$2"

    {
        printf '\n## Completion\n\n'
        printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
        printf '%s\n' '- Phase execution: `ABORTED`'
        printf '%s\n' "- Reason: \`${REASON}\`"
        printf '%s\n' '- Operator action required: `YES`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"

    trap - EXIT
    rm -f "${CMD_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit "${EXIT_CODE}"
}

# ------------------------------------------------------------
# A. Preconditions
# ------------------------------------------------------------

record_command \
    '06b0-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '06b0-02 Verify known runtime diff only' \
    'ACTUAL="$(git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy)"; EXPECTED="$(printf "D\tdeploy/.nfs000000000076202f00000088")"; printf "%s\n" "$ACTUAL"; test "$ACTUAL" = "$EXPECTED"' \
    || abort_phase 'unexpected runtime-area working-tree difference' 11

record_command \
    '06b0-03 Docker daemon access' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"' \
    || abort_phase 'Docker daemon inaccessible' 12

record_command \
    '06b0-04 Active project state before final reset' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect active project' 13

record_command \
    '06b0-05 Verify active metadata volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_metadata-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/metadata-data"' \
    || abort_phase 'active metadata volume identity mismatch' 14

record_command \
    '06b0-06 Verify active artifact volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'active artifact volume identity mismatch' 15

# ------------------------------------------------------------
# B. Record temporary verification state before deletion
# ------------------------------------------------------------

record_command \
    '06b0-07 Temporary Product row counts before final reset' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to record temporary Product data before deletion' 16

record_command \
    '06b0-08 Temporary artifact state before final reset' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; du -sh /state /state/objects'\''' \
    || abort_phase 'unable to record temporary artifact data before deletion' 17

# ------------------------------------------------------------
# C. Quiesce
# ------------------------------------------------------------

record_command \
    '06b0-09 Stop active Compose stack' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml stop' \
    || abort_phase 'active stack stop failed' 20

record_command \
    '06b0-10 Verify no active-project container is running' \
    'COUNT="$(docker ps --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "running_container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'one or more active-project containers remain running' 21

# ------------------------------------------------------------
# D. Remove containers, preserve persistence temporarily
# ------------------------------------------------------------

record_command \
    '06b0-11 Remove stopped active Compose containers' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml rm -f -s' \
    || abort_phase 'active container removal failed' 22

record_command \
    '06b0-12 Verify active-project containers absent' \
    'COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'active-project containers remain after removal' 23

record_command \
    '06b0-13 Verify metadata volume has zero consumers' \
    'COUNT="$(docker ps -a --filter volume=ariadne-e1a_metadata-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'metadata volume still has consumers' 24

record_command \
    '06b0-14 Verify artifact volume has zero consumers' \
    'COUNT="$(docker ps -a --filter volume=ariadne-e1a_artifact-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'artifact volume still has consumers' 25

# ------------------------------------------------------------
# E. Irreversible active persistence deletion
# ------------------------------------------------------------

record_command \
    '06b0-15 Delete active metadata volume' \
    'docker volume rm ariadne-e1a_metadata-data' \
    || abort_phase 'active metadata volume deletion failed' 30

record_command \
    '06b0-16 Delete active artifact volume' \
    'docker volume rm ariadne-e1a_artifact-data' \
    || abort_phase 'active artifact volume deletion failed' 31

record_command \
    '06b0-17 Verify active persistence absent' \
    'for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESENT: %s\n" "$v"; exit 1; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'one or more active volumes remain after deletion' 32

# ------------------------------------------------------------
# F. Rebuild database + Product migration
# ------------------------------------------------------------

record_command \
    '06b0-18 Rebuild database and Product migration' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build database migrate' \
    || abort_phase 'database/Product migration rebuild failed' 40

record_command \
    '06b0-19 Wait for Product migration completion' \
    'timeout 120 docker wait ariadne-e1a-migrate-1' \
    || abort_phase 'Product migration did not complete within fixed wait' 41

record_command \
    '06b0-20 Verify Product migration exit code' \
    'EXIT_CODE="$(docker inspect ariadne-e1a-migrate-1 --format "{{.State.ExitCode}}")"; printf "migration_exit_code=%s\n" "$EXIT_CODE"; test "$EXIT_CODE" -eq 0' \
    || abort_phase 'Product migration exited non-zero' 42

record_command \
    '06b0-21 Record Product migration logs' \
    'docker logs ariadne-e1a-migrate-1' \
    || abort_phase 'unable to record Product migration logs' 43

record_command \
    '06b0-22 Verify rebuilt database health' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'rebuilt database is not running/healthy' 44

record_command \
    '06b0-23 Verify Product revision' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'unexpected Product migration revision' 45

record_command \
    '06b0-24 Verify legacy Alembic table absent after rebuild' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table exists after clean rebuild' 46

record_command \
    '06b0-25 Verify no unexpected public tables after rebuild' \
    'UNEXPECTED="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='\''public'\'' AND tablename <> '\''alembic_version_product'\'' AND tablename NOT LIKE '\''product_%'\'' ORDER BY tablename;")"; printf "%s\n" "$UNEXPECTED"; test -z "$UNEXPECTED"' \
    || abort_phase 'unexpected non-Product public table exists after rebuild' 47

record_command \
    '06b0-26 Exact row counts before application startup' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to record clean database row counts' 48

record_command \
    '06b0-27 Assert Product application row total is zero before startup' \
    'TOTAL=0; while IFS= read -r table; do COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM public.${table};")"; TOTAL=$((TOTAL + COUNT)); done < <(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='\''public'\'' AND tablename LIKE '\''product_%'\'' ORDER BY tablename;"); printf "product_application_row_total=%s\n" "$TOTAL"; test "$TOTAL" -eq 0' \
    || abort_phase 'Product application data exists immediately after migration' 49

# ------------------------------------------------------------
# G. Restore application stack
# ------------------------------------------------------------

record_command \
    '06b0-28 Verify artifact volume absent before application restore' \
    'if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi' \
    || abort_phase 'artifact volume unexpectedly exists before application restore' 50

record_command \
    '06b0-29 Restore API worker and frontend' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build api worker frontend' \
    || abort_phase 'application stack restore failed' 51

record_command \
    '06b0-30 Wait for API health' \
    'timeout 120 sh -c '\''until [ "$(docker inspect ariadne-e1a-api-1 --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}" 2>/dev/null)" = "healthy" ]; do sleep 2; done'\''' \
    || abort_phase 'API did not become healthy within fixed wait' 52

# ------------------------------------------------------------
# H. Final read-only verification
# ------------------------------------------------------------

record_command \
    '06b0-31 Final Compose project state' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect final Compose state' 60

record_command \
    '06b0-32 Final database health' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'final database state is not running/healthy' 61

record_command \
    '06b0-33 Final API health' \
    'STATUS="$(docker inspect ariadne-e1a-api-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'final API state is not running/healthy' 62

record_command \
    '06b0-34 Final worker state' \
    'STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'final worker state is not running' 63

record_command \
    '06b0-35 Final frontend state' \
    'STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'final frontend state is not running' 64

record_command \
    '06b0-36 Final API readiness endpoint' \
    'curl --fail --silent --show-error --include --max-time 10 http://127.0.0.1:18000/health/ready' \
    || abort_phase 'final API readiness request failed' 65

record_command \
    '06b0-37 Final frontend endpoint' \
    'STATUS="$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" --max-time 10 http://127.0.0.1:18080/)"; printf "http_status=%s\n" "$STATUS"; test "$STATUS" -ge 200 -a "$STATUS" -lt 400' \
    || abort_phase 'final frontend endpoint failed' 66

record_command \
    '06b0-38 Final artifact volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'final artifact volume identity mismatch' 67

record_command \
    '06b0-39 Final API artifact mount' \
    'VOLUME="$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'final API artifact mount mismatch' 68

record_command \
    '06b0-40 Final worker artifact mount' \
    'VOLUME="$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'final worker artifact mount mismatch' 69

record_command \
    '06b0-41 Final artifact storage emptiness' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; STATE_FILES="$(find /state -type f | wc -l)"; OBJECT_FILES="$(find /state/objects -type f | wc -l)"; printf "state_files=%s\n" "$STATE_FILES"; printf "object_files=%s\n" "$OBJECT_FILES"; test "$STATE_FILES" -eq 0; test "$OBJECT_FILES" -eq 0; du -sh /state /state/objects'\''' \
    || abort_phase 'final artifact storage is not empty' 70

record_command \
    '06b0-42 Final Product application row total' \
    'TOTAL=0; while IFS= read -r table; do COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM public.${table};")"; TOTAL=$((TOTAL + COUNT)); done < <(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT tablename FROM pg_tables WHERE schemaname='\''public'\'' AND tablename LIKE '\''product_%'\'' ORDER BY tablename;"); printf "product_application_row_total=%s\n" "$TOTAL"; test "$TOTAL" -eq 0' \
    || abort_phase 'final Product database is not empty' 71

record_command \
    '06b0-43 Final exact table row counts' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to record final exact row counts' 72

record_command \
    '06b0-44 Final legacy Alembic absence' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table exists in final state' 73

record_command \
    '06b0-45 Final Product revision' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'unexpected final Product migration revision' 74

record_command \
    '06b0-46 Verify stale non-target volumes remain untouched' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify stale non-target volumes' 75

record_command \
    '06b0-47 Verify repository-local .ariadne has no files' \
    'if [ -e .ariadne ]; then COUNT="$(find .ariadne -type f | wc -l)"; printf "ariadne_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0; else printf "%s\n" "ABSENT: .ariadne"; fi' \
    || abort_phase 'repository-local .ariadne contains files' 76

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Temporary Golden Path data: `DELETED`'
    printf '%s\n' '- Active database persistence: `RECREATED CLEAN`'
    printf '%s\n' '- Active artifact persistence: `RECREATED CLEAN`'
    printf '%s\n' '- Product application rows: `0`'
    printf '%s\n' '- Artifact files: `0`'
    printf '%s\n' '- Product migration: `20260807_product_0006`'
    printf '%s\n' '- Legacy migration state: `ABSENT`'
    printf '%s\n' '- Database: `RUNNING / HEALTHY`'
    printf '%s\n' '- API: `RUNNING / HEALTHY`'
    printf '%s\n' '- Worker: `RUNNING`'
    printf '%s\n' '- Frontend: `RUNNING`'
    printf '%s\n' '- Final clean state: `VERIFIED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 10. Success Criteria

以下がすべて成立した場合のみ完了とする。

```text
temporary Golden Path data:
  deleted

Product application row total:
  0

artifact file count:
  0

legacy alembic_version:
  absent

alembic_version_product:
  20260807_product_0006

database:
  running / healthy

api:
  running / healthy

worker:
  running

frontend:
  running

API readiness:
  HTTP success

Frontend:
  HTTP 2xx / 3xx
```

---

## 11. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
06b0_final_clean_reinitialization_result.md
```

---

## 12. Stop Condition

result生成後は停止する。

Golden Pathやその他のwrite testは再実行しない。

最終clean stateを維持する。
