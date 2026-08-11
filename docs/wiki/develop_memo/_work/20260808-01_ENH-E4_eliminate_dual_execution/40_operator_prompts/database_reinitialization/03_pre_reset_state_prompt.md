# 03 Pre-reset State — Operator Prompt

## 1. Task

DB完全初期化作業の Phase 03 として、破壊操作前の実際の永続状態を記録する。

このphaseでは以下を確認する。

* 現在のCompose container状態
* `metadata-data` の実Docker volume
* `artifact-data` の実Docker volume
* database containerのmount
* 現在のPostgreSQL database
* public schema内のtable一覧
* legacy / product Alembic version tableの存在
* migration revision
* 各public tableのrecord count
* repository直下 `.ariadne` の存在

このphaseは **persistent dataに対してread-only** である。

Agent自身で追加調査・判断・retryを行わないこと。

---

## 2. Important Rule

database service が現在起動している場合のみ、固定されたSELECTを実行する。

database service が起動していない場合は、**起動してはならない。**

その場合はDB内部確認を `SKIPPED` と記録して、このphaseを終了する。

---

## 3. Prohibited Operations

以下を実行してはならない。

* `docker compose up`
* `docker compose down`
* `docker compose start`
* `docker compose stop`
* `docker compose restart`
* container作成
* container削除
* volume作成
* volume削除
* database作成
* database削除
* table作成
* table削除
* INSERT
* UPDATE
* DELETE
* TRUNCATE
* ALTER
* migration実行
* Alembic upgrade / downgrade
* seed
* application起動
* test実行
* `.env` 内容表示
* source code変更
* configuration変更
* promptにない追加コマンド
* retry
* エラー修正

---

## 4. Execution

以下のExecution Blockを**変更せず1回だけ実行すること。**

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03_pre_reset_state_result.md'

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
    printf '%s\n\n' '# 03 Pre-reset State Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03_pre_reset_state_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Persistent application data was inspected read-only. No reset operation was performed.'
} > "${TMP_RESULT}"

run_command() {
    LABEL="$1"
    COMMAND="$2"

    : > "${CMD_OUTPUT}"

    bash -lc "${COMMAND}" > "${CMD_OUTPUT}" 2>&1
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
    '03-01 Current branch' \
    'git branch --show-current'

run_command \
    '03-02 Working tree status before inspection' \
    'git status --short'

run_command \
    '03-03 Compose container state' \
    'docker compose -f compose.yaml ps -a'

run_command \
    '03-04 Compose container state as JSON' \
    'docker compose -f compose.yaml ps -a --format json'

run_command \
    '03-05 Metadata volume candidates' \
    'docker volume ls --filter label=com.docker.compose.volume=metadata-data --format "{{.Name}}" | sort'

run_command \
    '03-06 Metadata volume details' \
    'for v in $(docker volume ls --filter label=com.docker.compose.volume=metadata-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done'

run_command \
    '03-07 Artifact volume candidates' \
    'docker volume ls --filter label=com.docker.compose.volume=artifact-data --format "{{.Name}}" | sort'

run_command \
    '03-08 Artifact volume details' \
    'for v in $(docker volume ls --filter label=com.docker.compose.volume=artifact-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done'

run_command \
    '03-09 Database container mount mapping' \
    'CID="$(docker compose -f compose.yaml ps -aq database | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: database container"; fi'

run_command \
    '03-10 API container mount mapping' \
    'CID="$(docker compose -f compose.yaml ps -aq api | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: api container"; fi'

run_command \
    '03-11 Repository-local .ariadne state' \
    'if [ -e .ariadne ]; then find .ariadne -maxdepth 3 -printf "%y %p\n" | sort; else printf "%s\n" "ABSENT: .ariadne"; fi'

run_command \
    '03-12 Database service running state' \
    'if docker compose -f compose.yaml ps --status running --services | grep -qx "database"; then printf "%s\n" "RUNNING"; else printf "%s\n" "NOT_RUNNING"; fi'

DB_RUNNING=0

if docker compose -f compose.yaml ps --status running --services | grep -qx 'database'; then
    DB_RUNNING=1
fi

if [ "${DB_RUNNING}" -eq 1 ]; then

    run_command \
        '03-13 PostgreSQL identity' \
        'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT current_database() AS database_name, current_user AS database_user, current_schema() AS current_schema;"'

    run_command \
        '03-14 PostgreSQL database size' \
        'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"'

    run_command \
        '03-15 Public schema tables' \
        'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT tablename FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename;"'

    run_command \
        '03-16 Alembic version table presence' \
        'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT to_regclass('\''public.alembic_version'\'') AS legacy_version_table, to_regclass('\''public.alembic_version_product'\'') AS product_version_table;"'

    run_command \
        '03-17 Legacy Alembic revision' \
        'if [ "$(docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'') IS NOT NULL;")" = "t" ]; then docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version"; fi'

    run_command \
        '03-18 Product Alembic revision' \
        'if [ "$(docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version_product'\'') IS NOT NULL;")" = "t" ]; then docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version_product"; fi'

    run_command \
        '03-19 Exact row counts for all public tables' \
        'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off'

else

    {
        printf '\n## 03-13 through 03-19 Database inspection\n\n'
        printf '%s\n' '### Status'
        printf '\n'
        printf '%s\n' '````text'
        printf '%s\n' 'SKIPPED: database service was not running.'
        printf '%s\n' 'No container was started by this phase.'
        printf '%s\n' '````'
    } >> "${TMP_RESULT}"

fi

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

## 5. Interpretation Prohibited

Agentは結果について以下を判断しないこと。

* legacy schemaを削除すべきか
* product schemaを削除すべきか
* どのvolumeを削除すべきか
* artifact-dataを削除すべきか
* databaseを再起動すべきか
* migrationをどう再適用すべきか

これらはresult確認後に人間側で決定する。

---

## 6. Result

Execution Blockは以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03_pre_reset_state_result.md
```

resultを生成したら、それ以上のコマンドを実行しないこと。

---

## 7. Response

成功時の最終応答は以下だけとする。

```text
03_pre_reset_state_result.md を生成しました。
Phase 03 completed.
```

Execution Block自体が失敗しresultが生成されなかった場合は、Execution Blockのエラー出力だけを返すこと。

エラー原因を推論・修正しないこと。

---

## 8. Stop Condition

以下のいずれかで直ちに停止する。

1. `03_pre_reset_state_result.md` が生成された
2. Execution Blockがエラー終了した

どちらの場合も、それ以上の操作を行わないこと。
