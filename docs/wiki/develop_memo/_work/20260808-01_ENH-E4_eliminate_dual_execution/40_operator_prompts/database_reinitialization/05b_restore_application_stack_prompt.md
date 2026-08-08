# 05b Restore Application Stack — Human Operator Prompt

## 1. Purpose

Phase 05a により、空の永続領域から以下が正常に再構築された。

```text
ariadne-e1a_metadata-data
PostgreSQL database
Product migration schema
```

Product migrationは正常終了し、application dataは0件である。

このphaseでは、残りのapplication serviceを起動する。

対象:

```text
api
worker
frontend
```

また、API / worker が利用する以下のartifact volumeが空の状態から再作成されることを確認する。

```text
ariadne-e1a_artifact-data
```

---

## 2. Goals

このphaseでは以下を確認する。

1. APIが正常起動する
2. API healthcheckがhealthyになる
3. workerが正常稼働する
4. frontendが正常起動する
5. E1a host endpointからAPIへ到達できる
6. E1a host endpointからfrontendへ到達できる
7. artifact volumeが新規作成される
8. artifact storageが初期状態で空である
9. application起動だけではProduct application dataが作成されない
10. legacy schemaが依然として存在しない

---

## 3. Confirmed Starting State

Compose project:

```text
ariadne-e1a
```

現在存在するservice:

```text
database
migrate
```

期待状態:

```text
database:
  running / healthy

migrate:
  exited / exit code 0
```

現在のProduct migration revision:

```text
20260807_product_0006
```

現在のProduct application record count:

```text
all tables = 0
```

---

## 4. Compose Configuration

使用するCompose filesを以下に固定する。

```text
compose.yaml
compose.e1a.yaml
```

host endpoint:

```text
API:
  http://127.0.0.1:18000

Frontend:
  http://127.0.0.1:18080
```

API readiness endpoint:

```text
http://127.0.0.1:18000/health/ready
```

---

## 5. Prohibited Operations

以下は禁止する。

* legacy migration
* 手動SQLによるschema変更
* INSERT
* UPDATE
* DELETE
* seed投入
* test fixture投入
* artifactの手動作成
* artifactの手動削除
* stale `causal-atelier_*` volume操作
* source code変更
* migration file変更
* configuration変更
* failure後のretry
* failure原因の自動修正

起動に失敗した場合はresultを保存して停止する。

---

## 6. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

---

## 7. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/05b_restore_application_stack_result.md'

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
    printf '%s\n\n' '# 05b Restore Application Stack Result'

    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`05b_restore_application_stack_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '%s\n' '- Restore scope: `api + worker + frontend + artifact persistence`'
    printf '\n'
    printf '%s\n' '> Application services are restored on top of the clean Product database created in Phase 05a.'
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
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"

    trap - EXIT
    rm -f "${CMD_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit "${EXIT_CODE}"
}

record_command \
    '05b-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '05b-02 Runtime configuration working-tree precondition' \
    'git diff --exit-code HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy' \
    || abort_phase 'runtime application files contain uncommitted changes' 11

record_command \
    '05b-03 Database health precondition' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'database is not running and healthy' 12

record_command \
    '05b-04 Migration completion precondition' \
    'EXIT_CODE="$(docker inspect ariadne-e1a-migrate-1 --format "{{.State.ExitCode}}")"; printf "migration_exit_code=%s\n" "$EXIT_CODE"; test "$EXIT_CODE" -eq 0' \
    || abort_phase 'Product migration container is not successfully completed' 13

record_command \
    '05b-05 Product revision precondition' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'unexpected Product migration revision' 14

record_command \
    '05b-06 Verify artifact volume absent before application restore' \
    'if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi' \
    || abort_phase 'artifact volume already exists before application restore' 15

record_command \
    '05b-07 Verify application services absent before restore' \
    'for service in api worker frontend; do COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --filter label=com.docker.compose.service="$service" -q | wc -l)"; printf "%s_container_count=%s\n" "$service" "$COUNT"; test "$COUNT" -eq 0 || exit 1; done' \
    || abort_phase 'one or more application containers already exist' 16

record_command \
    '05b-08 Restore application services' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build api worker frontend' \
    || abort_phase 'application Compose startup failed' 20

record_command \
    '05b-09 Wait for API health' \
    'timeout 120 sh -c '\''until [ "$(docker inspect ariadne-e1a-api-1 --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}" 2>/dev/null)" = "healthy" ]; do sleep 2; done'\''' \
    || abort_phase 'API did not become healthy within fixed wait' 21

record_command \
    '05b-10 API container state' \
    'docker inspect ariadne-e1a-api-1 --format "status={{.State.Status}} health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}"' \
    || abort_phase 'unable to inspect API container' 22

record_command \
    '05b-11 Worker container state' \
    'STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'worker is not running' 23

record_command \
    '05b-12 Frontend container state' \
    'STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'frontend is not running' 24

record_command \
    '05b-13 Active Compose project inventory' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect restored Compose project' 25

record_command \
    '05b-14 Host API readiness request' \
    'curl --fail --silent --show-error --include --max-time 10 http://127.0.0.1:18000/health/ready' \
    || abort_phase 'host API readiness endpoint failed' 30

record_command \
    '05b-15 Host frontend request' \
    'STATUS="$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" --max-time 10 http://127.0.0.1:18080/)"; printf "http_status=%s\n" "$STATUS"; test "$STATUS" -ge 200 -a "$STATUS" -lt 400' \
    || abort_phase 'host frontend endpoint failed' 31

record_command \
    '05b-16 Recreated artifact volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'artifact volume was not recreated correctly' 32

record_command \
    '05b-17 API artifact volume mount' \
    'VOLUME="$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'API artifact mount mismatch' 33

record_command \
    '05b-18 Worker artifact volume mount' \
    'VOLUME="$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'worker artifact mount mismatch' 34

record_command \
    '05b-19 Artifact storage initial state' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; du -sh /state /state/objects'\''' \
    || abort_phase 'unable to inspect recreated artifact storage' 35

record_command \
    '05b-20 Verify legacy Alembic table remains absent' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table appeared after application startup' 36

record_command \
    '05b-21 Product revision after application startup' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'Product revision changed unexpectedly during application startup' 37

record_command \
    '05b-22 Exact row counts after application startup' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to inspect Product table row counts after startup' 38

record_command \
    '05b-23 Verify stale non-target volumes remain untouched' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify stale non-target volumes' 39

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Database: `RUNNING / HEALTHY`'
    printf '%s\n' '- API: `RUNNING / HEALTHY`'
    printf '%s\n' '- Worker: `RUNNING`'
    printf '%s\n' '- Frontend: `RUNNING`'
    printf '%s\n' '- Artifact persistence: `RECREATED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 8. Success Criteria

このphaseでは以下をすべて満たすこと。

```text
database:
  running / healthy

migrate:
  exit code 0

api:
  running / healthy

worker:
  running

frontend:
  running

http://127.0.0.1:18000/health/ready:
  success

http://127.0.0.1:18080/:
  HTTP 2xx or 3xx

ariadne-e1a_artifact-data:
  recreated
  mounted by api and worker

legacy alembic_version:
  absent

product revision:
  20260807_product_0006
```

---

## 9. Important Observation

`05b-19` と `05b-22` は単に記録する。

Agent自身は、

* artifact storageが本当に「空」と言えるか
* application startupでDB rowが増えたことが正常か異常か

を判断しない。

その解釈は人間側で行う。

---

## 10. Failure Semantics

失敗した場合、

* retryしない
* serviceをrestartしない
* source codeを修正しない
* migrationを再実行しない
* DBを変更しない
* artifactを変更しない

その時点のresultを保存して停止する。

---

## 11. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
05b_restore_application_stack_result.md
```

---

## 12. Stop Condition

result生成後は停止する。

test dataの作成や分析実行にはまだ進まない。

次phaseで最終verificationを行う。
