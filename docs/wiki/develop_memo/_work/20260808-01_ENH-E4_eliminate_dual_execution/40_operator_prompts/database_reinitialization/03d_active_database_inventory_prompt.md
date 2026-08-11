# 03d Active Database Inventory — Human Operator Prompt

## 1. Purpose

Phase 03c により、現在実際に使用されているdatabase containerが以下であることが確定した。

```text
ariadne-e1a-database-1
```

このphaseでは、Reset直前のDB内部状態をread-onlyで記録する。

確認対象:

* PostgreSQL identity
* database size
* public schema table一覧
* legacy Alembic version table
* product Alembic version table
* migration revision
* 全public tableのrecord count

この結果をもって、Reset前DB状態の記録を完了する。

---

## 2. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

---

## 3. Target

対象containerを以下に固定する。

```text
ariadne-e1a-database-1
```

対象database:

```text
ariadne
```

対象database user:

```text
ariadne
```

Agentまたは人間が別containerを選択してはならない。

---

## 4. Safety

このphaseは **read-only** である。

SQLは `SELECT` のみ実行する。

以下は禁止する。

* INSERT
* UPDATE
* DELETE
* TRUNCATE
* DROP
* ALTER
* CREATE
* migration
* Alembic upgrade
* Alembic downgrade
* database restart
* container restart
* container stop
* volume操作

---

## 5. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03d_active_database_inventory_result.md'

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
    printf '%s\n\n' '# 03d Active Database Inventory Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03d_active_database_inventory_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target container: `ariadne-e1a-database-1`'
    printf '%s\n' '- Target database: `ariadne`'
    printf '\n'
    printf '%s\n' '> Read-only database inventory. No database state was modified.'
} > "${TMP_RESULT}"

run_command() {
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
}

run_command \
    '03d-01 Target container state' \
    'docker ps --filter name="^/ariadne-e1a-database-1$" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03d-02 PostgreSQL identity' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT current_database() AS database_name, current_user AS database_user, current_schema() AS current_schema;"'

run_command \
    '03d-03 PostgreSQL database size' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"'

run_command \
    '03d-04 Public schema tables' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT tablename FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename;"'

run_command \
    '03d-05 Alembic version table presence' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT to_regclass('\''public.alembic_version'\'') AS legacy_version_table, to_regclass('\''public.alembic_version_product'\'') AS product_version_table;"'

run_command \
    '03d-06 Legacy Alembic revision' \
    'if [ "$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'') IS NOT NULL;")" = "t" ]; then docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version"; fi'

run_command \
    '03d-07 Product Alembic revision' \
    'if [ "$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version_product'\'') IS NOT NULL;")" = "t" ]; then docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version_product"; fi'

run_command \
    '03d-08 Exact row counts for all public tables' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off'

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 6. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03d_active_database_inventory_result.md
```

---

## 7. Stop Condition

`03d_active_database_inventory_result.md` が生成されたら停止する。

Resetは行わない。

追加調査も行わない。
