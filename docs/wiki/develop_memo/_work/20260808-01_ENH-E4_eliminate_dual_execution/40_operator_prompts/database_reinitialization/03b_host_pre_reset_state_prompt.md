# 03b Host Pre-reset State — Human Operator Prompt

## 1. Purpose

Phase 03 / 03a の結果、Agent実行環境からDocker daemonへアクセスできないことが確認された。

そのため、このphaseでは **Dockerへアクセス可能なホスト側terminalで人間が固定Execution Blockを実行する。**

このphaseの目的は、Reset前の実状態をread-onlyで取得し、

* database container
* Docker volumes
* PostgreSQL schema
* Alembic revision
* table row counts
* artifact persistence
* repository-local `.ariadne`

を確定することである。

---

## 2. Execution Environment

このExecution Blockは **Agent環境では実行しない。**

以下を満たすホスト側terminalで実行すること。

* 対象repositoryをcheckoutしている
* branchが `refactor/ariadne_mvp_e4`
* `docker` commandが利用可能
* Docker daemonへアクセス可能
* `docker compose` が利用可能

このphaseではDocker daemonへのアクセスに `sudo` を使用しない。

通常ユーザーでDockerへアクセスできない場合は実行を中止し、そのエラーを記録する。

---

## 3. Safety

このphaseは **read-only inspection** である。

以下を行わない。

* `docker compose up`
* `docker compose down`
* `docker compose start`
* `docker compose stop`
* `docker compose restart`
* container作成
* container削除
* volume作成
* volume削除
* DB作成・削除
* INSERT
* UPDATE
* DELETE
* TRUNCATE
* ALTER
* migration
* Alembic upgrade / downgrade
* source code変更
* configuration変更

database serviceが停止している場合も、このphaseでは起動しない。

---

## 4. Execution Block

repository内の任意のdirectoryから、以下を**変更せず1回だけ実行すること。**

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03b_host_pre_reset_state_result.md'

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
    printf '%s\n\n' '# 03b Host Pre-reset State Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03b_host_pre_reset_state_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Host-side read-only inspection. No reset operation was performed.'
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
    '03b-01 Current branch' \
    'git branch --show-current'

run_command \
    '03b-02 Working tree status' \
    'git status --short'

run_command \
    '03b-03 Effective user' \
    'id'

run_command \
    '03b-04 Docker daemon access' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"'

DOCKER_ACCESS=0

if docker version >/dev/null 2>&1; then
    DOCKER_ACCESS=1
fi

if [ "${DOCKER_ACCESS}" -eq 1 ]; then

    run_command \
        '03b-05 Compose container state' \
        'docker compose -f compose.yaml ps -a'

    run_command \
        '03b-06 Compose container state JSON' \
        'docker compose -f compose.yaml ps -a --format json'

    run_command \
        '03b-07 Metadata volume candidates' \
        'docker volume ls --filter label=com.docker.compose.volume=metadata-data --format "{{.Name}}" | sort'

    run_command \
        '03b-08 Metadata volume details' \
        'for v in $(docker volume ls --filter label=com.docker.compose.volume=metadata-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done'

    run_command \
        '03b-09 Artifact volume candidates' \
        'docker volume ls --filter label=com.docker.compose.volume=artifact-data --format "{{.Name}}" | sort'

    run_command \
        '03b-10 Artifact volume details' \
        'for v in $(docker volume ls --filter label=com.docker.compose.volume=artifact-data -q | sort); do docker volume inspect "$v" --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Labels={{json .Labels}}"; done'

    run_command \
        '03b-11 Database container mount mapping' \
        'CID="$(docker compose -f compose.yaml ps -aq database | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: database container"; fi'

    run_command \
        '03b-12 API container mount mapping' \
        'CID="$(docker compose -f compose.yaml ps -aq api | head -n 1)"; if [ -n "$CID" ]; then docker inspect "$CID" --format "{{json .Mounts}}"; else printf "%s\n" "ABSENT: api container"; fi'

    run_command \
        '03b-13 Database service running state' \
        'if docker compose -f compose.yaml ps --status running --services | grep -qx "database"; then printf "%s\n" "RUNNING"; else printf "%s\n" "NOT_RUNNING"; fi'

    DB_RUNNING=0

    if docker compose -f compose.yaml ps --status running --services | grep -qx 'database'; then
        DB_RUNNING=1
    fi

    if [ "${DB_RUNNING}" -eq 1 ]; then

        run_command \
            '03b-14 PostgreSQL identity' \
            'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT current_database() AS database_name, current_user AS database_user, current_schema() AS current_schema;"'

        run_command \
            '03b-15 PostgreSQL database size' \
            'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"'

        run_command \
            '03b-16 Public schema tables' \
            'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT tablename FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename;"'

        run_command \
            '03b-17 Alembic version table presence' \
            'docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT to_regclass('\''public.alembic_version'\'') AS legacy_version_table, to_regclass('\''public.alembic_version_product'\'') AS product_version_table;"'

        run_command \
            '03b-18 Legacy Alembic revision' \
            'if [ "$(docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'') IS NOT NULL;")" = "t" ]; then docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version"; fi'

        run_command \
            '03b-19 Product Alembic revision' \
            'if [ "$(docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version_product'\'') IS NOT NULL;")" = "t" ]; then docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off -c "SELECT version_num FROM alembic_version_product ORDER BY version_num;"; else printf "%s\n" "ABSENT: alembic_version_product"; fi'

        run_command \
            '03b-20 Exact row counts for all public tables' \
            'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker compose -f compose.yaml exec -T database psql -X -U ariadne -d ariadne -P pager=off'

    else

        {
            printf '\n## 03b-14 through 03b-20 Database inspection\n\n'
            printf '%s\n' '### Status'
            printf '\n'
            printf '%s\n' '````text'
            printf '%s\n' 'SKIPPED: database service was not running.'
            printf '%s\n' 'The database service was not started by this phase.'
            printf '%s\n' '````'
        } >> "${TMP_RESULT}"

    fi

else

    {
        printf '\n## 03b-05 through 03b-20 Docker inspection\n\n'
        printf '%s\n' '### Status'
        printf '\n'
        printf '%s\n' '````text'
        printf '%s\n' 'SKIPPED: Docker daemon was not accessible from this host terminal.'
        printf '%s\n' 'No permission change or sudo operation was attempted.'
        printf '%s\n' '````'
    } >> "${TMP_RESULT}"

fi

run_command \
    '03b-21 Repository-local .ariadne tree' \
    'if [ -e .ariadne ]; then find .ariadne -maxdepth 4 -printf "%y %p\n" | sort; else printf "%s\n" "ABSENT: .ariadne"; fi'

run_command \
    '03b-22 Repository-local .ariadne size' \
    'if [ -e .ariadne ]; then du -sh .ariadne; else printf "%s\n" "ABSENT: .ariadne"; fi'

run_command \
    '03b-23 Repository-local .ariadne file count' \
    'if [ -e .ariadne ]; then find .ariadne -type f | wc -l; else printf "%s\n" "ABSENT: .ariadne"; fi'

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

## 5. Important

このスクリプトでは `run_command` 内を

```bash
bash -o pipefail -lc
```

で実行する。

これは Phase 03 で発生した、

```text
docker command failure
        |
        v
pipelineの後段が0を返す
        |
        v
resultにexit code 0と記録される
```

という問題を防止するためである。

---

## 6. Result

実行後、以下が生成される。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03b_host_pre_reset_state_result.md
```

このファイルをGit管理対象として保存する。

---

## 7. Stop Condition

`03b_host_pre_reset_state_result.md` が生成されたら停止する。

このphaseではResetを行わない。

結果を確認するまで `04_reset` へ進まない。
