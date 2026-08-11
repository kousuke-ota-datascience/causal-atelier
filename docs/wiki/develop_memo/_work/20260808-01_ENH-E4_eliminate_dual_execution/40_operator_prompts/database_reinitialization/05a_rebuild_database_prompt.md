# 05a Rebuild Database — Human Operator Prompt

## 1. Purpose

Phase 04c により、active environment `ariadne-e1a` の以下の永続領域が完全に削除された。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

このphaseでは、空の状態から以下だけを再構築する。

1. PostgreSQL database
2. Product migration schema

API、worker、frontendはまだ起動しない。

このphaseの目的は、

> 現行Compose定義と現行Product migrationsだけで、空DBから正しいschemaを再構築できること

を独立して検証することである。

---

## 2. Target Environment

Git branch:

```text
refactor/ariadne_mvp_e4
```

Compose project:

```text
ariadne-e1a
```

Compose files:

```text
compose.yaml
compose.e1a.yaml
```

対象database:

```text
ariadne
```

対象database user:

```text
ariadne
```

migration configuration:

```text
alembic_product.ini
```

---

## 3. Scope

このphaseで起動してよいserviceは以下のみ。

```text
database
migrate
```

以下は起動しない。

```text
api
worker
frontend
browser-e2e
```

したがって、このphaseではapplicationによる通常データ書き込みを発生させない。

---

## 4. Expected Rebuild Path

現行Compose定義に従い、

```text
empty metadata persistence
        |
        v
PostgreSQL initialization
        |
        v
database healthy
        |
        v
alembic -c alembic_product.ini upgrade head
        |
        v
Product schema
```

の経路だけでDBを構築する。

手動SQLでschemaを作成してはならない。

legacy migrationを実行してはならない。

---

## 5. Prohibited Operations

以下は禁止する。

* legacy `alembic.ini` によるmigration
* `migrations/` のmigration実行
* 手動 `CREATE TABLE`
* 手動 `ALTER TABLE`
* 手動 `INSERT`
* seed投入
* API起動
* worker起動
* frontend起動
* stale `causal-atelier_*` volume操作
* database volume手動作成
* artifact volume内容の手動作成
* migration failure後の手動修正
* retry
* source code変更
* migration file変更

migrationが失敗した場合はその状態を記録して停止する。

---

## 6. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

repository内の任意のdirectoryから実行してよい。

---

## 7. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/05a_rebuild_database_result.md'

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
    printf '%s\n\n' '# 05a Rebuild Database Result'

    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`05a_rebuild_database_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '%s\n' '- Rebuild scope: `database + product migration only`'
    printf '\n'
    printf '%s\n' '> This phase rebuilds database persistence from the current Product migration chain.'
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
        printf '%s\n' '- Full application startup: `NOT EXECUTED`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"

    trap - EXIT
    rm -f "${CMD_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit "${EXIT_CODE}"
}

record_command \
    '05a-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '05a-02 Runtime configuration working-tree precondition' \
    'git diff --exit-code HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations' \
    || abort_phase 'runtime or Product migration files contain uncommitted changes' 11

record_command \
    '05a-03 Docker daemon access precondition' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"' \
    || abort_phase 'Docker daemon inaccessible' 12

record_command \
    '05a-04 Verify active-project containers absent before rebuild' \
    'COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'ariadne-e1a containers unexpectedly exist before rebuild' 13

record_command \
    '05a-05 Verify old metadata volume absent' \
    'if docker volume inspect ariadne-e1a_metadata-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_metadata-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_metadata-data"; fi' \
    || abort_phase 'old metadata volume exists before rebuild' 14

record_command \
    '05a-06 Verify old artifact volume absent' \
    'if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi' \
    || abort_phase 'old artifact volume exists before rebuild' 15

record_command \
    '05a-07 Verify stale non-target volumes remain untouched before rebuild' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to inspect stale non-target volumes' 16

record_command \
    '05a-08 Rebuild database and run Product migration' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build database migrate' \
    || abort_phase 'database/migrate Compose startup failed' 20

record_command \
    '05a-09 Wait for Product migration container completion' \
    'timeout 120 docker wait ariadne-e1a-migrate-1' \
    || abort_phase 'migration container did not complete successfully within fixed wait' 21

record_command \
    '05a-10 Verify Product migration exit code' \
    'EXIT_CODE="$(docker inspect ariadne-e1a-migrate-1 --format "{{.State.ExitCode}}")"; printf "migration_exit_code=%s\n" "$EXIT_CODE"; test "$EXIT_CODE" -eq 0' \
    || abort_phase 'Product migration container exited non-zero' 22

record_command \
    '05a-11 Record Product migration logs' \
    'docker logs ariadne-e1a-migrate-1' \
    || abort_phase 'unable to record Product migration logs' 23

record_command \
    '05a-12 Verify database container health' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'database container is not running and healthy' 24

record_command \
    '05a-13 Active project containers after database rebuild' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect rebuilt containers' 25

record_command \
    '05a-14 Recreated Compose volumes' \
    'docker volume ls --filter label=com.docker.compose.project=ariadne-e1a --format "{{.Name}}" | sort' \
    || abort_phase 'unable to inspect recreated Compose volumes' 26

record_command \
    '05a-15 Recreated metadata volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_metadata-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/metadata-data"' \
    || abort_phase 'recreated metadata volume identity mismatch' 27

record_command \
    '05a-16 PostgreSQL identity after rebuild' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT current_database() AS database_name, current_user AS database_user, current_schema() AS current_schema;"' \
    || abort_phase 'unable to query rebuilt database' 30

record_command \
    '05a-17 Public tables after Product migration' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT tablename FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename;"' \
    || abort_phase 'unable to inspect rebuilt public schema' 31

record_command \
    '05a-18 Verify legacy Alembic version table absent' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic version table exists after Product-only rebuild' 32

record_command \
    '05a-19 Verify Product Alembic version table present' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version_product'\'');")"; printf "product_version_table=%s\n" "$VALUE"; test "$VALUE" = "alembic_version_product"' \
    || abort_phase 'Product Alembic version table missing after rebuild' 33

record_command \
    '05a-20 Product Alembic revision after rebuild' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"' \
    || abort_phase 'unable to read Product Alembic revision' 34

record_command \
    '05a-21 Exact row counts after migration and before application startup' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to count rows in rebuilt database' 35

record_command \
    '05a-22 Verify API worker and frontend were not started' \
    'for service in api worker frontend; do COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --filter label=com.docker.compose.service="$service" -q | wc -l)"; printf "%s_container_count=%s\n" "$service" "$COUNT"; test "$COUNT" -eq 0 || exit 1; done' \
    || abort_phase 'application service unexpectedly started during database-only rebuild' 36

record_command \
    '05a-23 Verify stale non-target volumes after rebuild' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify stale non-target volumes after rebuild' 37

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Database persistence: `RECREATED`'
    printf '%s\n' '- Product migration: `COMPLETED`'
    printf '%s\n' '- Legacy migration: `NOT EXECUTED`'
    printf '%s\n' '- Application services: `NOT STARTED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 8. Expected State

このphaseが成功した場合、

```text
ariadne-e1a-database-1
    running / healthy

ariadne-e1a-migrate-1
    exited / exit code 0
```

となる。

DBにはProduct migrationによって生成されたschemaが存在する。

API、worker、frontendはまだ存在しない。

---

## 9. Interpretation Rule

このphaseの重要な判定対象は以下である。

### A. Product migration単独で空DBから再構築できたか

成功条件:

* migration exit code = 0
* database healthy
* Product Alembic version tableが存在する

### B. Legacy schemaが混入していないか

成功条件:

```text
alembic_version
    absent

alembic_version_product
    present
```

### C. Application起動前のDBがクリーンか

全public tableのrow countを記録する。

migration framework自身の管理データを除き、application dataが投入されていないことを次の人間レビューで確認する。

Agent自身はrow countの意味を解釈しない。

---

## 10. Failure Semantics

migrationが失敗した場合、

* legacy migrationを試さない
* 手動SQLを実行しない
* migration fileを変更しない
* retryしない
* applicationを起動しない

resultを保存して停止する。

これは、

> 現行Product migration chainだけでは空DBから再構築できない

可能性を示す重要な検証結果として扱う。

---

## 11. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
05a_rebuild_database_result.md
```

---

## 12. Stop Condition

`05a_rebuild_database_result.md` が生成されたら停止する。

API / worker / frontendはまだ起動しない。

次phaseへ自動的に進まない。
