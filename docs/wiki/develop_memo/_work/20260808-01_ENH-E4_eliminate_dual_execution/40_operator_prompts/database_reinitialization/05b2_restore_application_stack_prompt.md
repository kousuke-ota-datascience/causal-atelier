# 05b2 Restore Application Stack — Human Operator Prompt

## 1. Purpose

Phase 05b は、application startup前のworking-tree preconditionによってABORTした。

Phase 05b1 のread-only assessmentにより、検出された差分

```text
D deploy/.nfs000000000076202f00000088
```

について以下が確認された。

* runtime-areaのtracked差分はこの1件のみ
* HEAD上の当該ファイルと `deploy/nginx.conf` の内容は完全一致
* runtime codeから当該 `.nfs...` filenameへの参照はない
* frontend runtimeが使用するのは `deploy/nginx.conf`
* 当該差分は今回のapplication restoreに影響しない

したがって、このphaseでは上記1件だけを**既知の許容差分**として扱い、application stackのrestoreを再実行する。

既知差分以外のruntime差分が存在する場合はABORTする。

---

## 2. Restore Target

Compose project:

```text
ariadne-e1a
```

Compose files:

```text
compose.yaml
compose.e1a.yaml
```

restore対象:

```text
api
worker
frontend
```

既に再構築済み:

```text
database
migrate
```

再生成対象persistent volume:

```text
ariadne-e1a_artifact-data
```

---

## 3. Known Allowed Working-tree Difference

以下の削除差分のみを許容する。

```text
D	deploy/.nfs000000000076202f00000088
```

このファイルを復元してはならない。

削除差分を修正してはならない。

`.gitignore` も変更しない。

このファイルのGit管理上の整理はdatabase reinitializationとは別作業とする。

---

## 4. Preconditions

application startup前に以下を確認する。

1. branchが `refactor/ariadne_mvp_e4`
2. runtime-areaのtracked差分が許容された `.nfs...` 削除1件だけ
3. HEAD上の `.nfs...` と現在の `deploy/nginx.conf` が同一内容
4. databaseが running / healthy
5. Product migrationが exit code 0
6. Product revisionが `20260807_product_0006`
7. legacy `alembic_version` が存在しない
8. artifact volumeがまだ存在しない
9. api / worker / frontend containerがまだ存在しない

1つでも成立しない場合はABORTする。

---

## 5. Prohibited Operations

以下は禁止する。

* `.nfs...` の復元
* `.nfs...` の追加削除操作
* `.gitignore` 変更
* legacy migration
* manual SQL schema変更
* INSERT
* UPDATE
* DELETE
* seed投入
* fixture投入
* source code変更
* migration file変更
* configuration変更
* stale `causal-atelier_*` volume操作
* failure後のretry
* failure原因の自動修正

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

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/05b2_restore_application_stack_result.md'

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
    printf '%s\n\n' '# 05b2 Restore Application Stack Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`05b2_restore_application_stack_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '%s\n' '- Restore scope: `api + worker + frontend + artifact persistence`'
    printf '%s\n' '- Known allowed diff: `D deploy/.nfs000000000076202f00000088`'
    printf '\n'
    printf '%s\n' '> Application restore retry after explicit assessment of the known NFS temporary-file diff.'
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
    '05b2-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '05b2-02 Runtime-area tracked differences' \
    'git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy' \
    || abort_phase 'unable to inspect runtime-area differences' 11

record_command \
    '05b2-03 Verify only known NFS deletion is present' \
    'ACTUAL="$(git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy)"; EXPECTED="$(printf "D\tdeploy/.nfs000000000076202f00000088")"; printf "%s\n" "$ACTUAL"; test "$ACTUAL" = "$EXPECTED"' \
    || abort_phase 'runtime-area contains differences other than the assessed NFS deletion' 12

record_command \
    '05b2-04 Verify assessed NFS blob still matches nginx.conf' \
    'git show HEAD:deploy/.nfs000000000076202f00000088 | cmp - deploy/nginx.conf' \
    || abort_phase 'known NFS blob no longer matches deploy/nginx.conf' 13

record_command \
    '05b2-05 Docker daemon access' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"' \
    || abort_phase 'Docker daemon inaccessible' 14

record_command \
    '05b2-06 Database health precondition' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'database is not running and healthy' 15

record_command \
    '05b2-07 Migration completion precondition' \
    'EXIT_CODE="$(docker inspect ariadne-e1a-migrate-1 --format "{{.State.ExitCode}}")"; printf "migration_exit_code=%s\n" "$EXIT_CODE"; test "$EXIT_CODE" -eq 0' \
    || abort_phase 'Product migration container is not successfully completed' 16

record_command \
    '05b2-08 Product revision precondition' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'unexpected Product migration revision' 17

record_command \
    '05b2-09 Verify legacy Alembic table absent before restore' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table exists before application restore' 18

record_command \
    '05b2-10 Verify artifact volume absent before restore' \
    'if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi' \
    || abort_phase 'artifact volume already exists before application restore' 19

record_command \
    '05b2-11 Verify application services absent before restore' \
    'for service in api worker frontend; do COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --filter label=com.docker.compose.service="$service" -q | wc -l)"; printf "%s_container_count=%s\n" "$service" "$COUNT"; test "$COUNT" -eq 0 || exit 1; done' \
    || abort_phase 'one or more application containers already exist' 20

record_command \
    '05b2-12 Restore application services' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml up -d --build api worker frontend' \
    || abort_phase 'application Compose startup failed' 30

record_command \
    '05b2-13 Wait for API health' \
    'timeout 120 sh -c '\''until [ "$(docker inspect ariadne-e1a-api-1 --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}" 2>/dev/null)" = "healthy" ]; do sleep 2; done'\''' \
    || abort_phase 'API did not become healthy within fixed wait' 31

record_command \
    '05b2-14 API container state' \
    'STATUS="$(docker inspect ariadne-e1a-api-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'API is not running and healthy' 32

record_command \
    '05b2-15 Worker container state' \
    'STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'worker is not running' 33

record_command \
    '05b2-16 Frontend container state' \
    'STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'frontend is not running' 34

record_command \
    '05b2-17 Active Compose project inventory' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect restored Compose project' 35

record_command \
    '05b2-18 Host API readiness request' \
    'curl --fail --silent --show-error --include --max-time 10 http://127.0.0.1:18000/health/ready' \
    || abort_phase 'host API readiness endpoint failed' 40

record_command \
    '05b2-19 Host frontend request' \
    'STATUS="$(curl --silent --show-error --output /dev/null --write-out "%{http_code}" --max-time 10 http://127.0.0.1:18080/)"; printf "http_status=%s\n" "$STATUS"; test "$STATUS" -ge 200 -a "$STATUS" -lt 400' \
    || abort_phase 'host frontend endpoint failed' 41

record_command \
    '05b2-20 Recreated artifact volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'artifact volume was not recreated correctly' 42

record_command \
    '05b2-21 API artifact volume mount' \
    'VOLUME="$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'API artifact mount mismatch' 43

record_command \
    '05b2-22 Worker artifact volume mount' \
    'VOLUME="$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")"; printf "%s\n" "$VOLUME"; test "$VOLUME" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'worker artifact mount mismatch' 44

record_command \
    '05b2-23 Artifact storage initial state' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; printf "state_dirs="; find /state -type d | wc -l; du -sh /state /state/objects'\''' \
    || abort_phase 'unable to inspect recreated artifact storage' 45

record_command \
    '05b2-24 Verify legacy Alembic table remains absent' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table appeared after application startup' 46

record_command \
    '05b2-25 Product revision after application startup' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'Product revision changed unexpectedly during application startup' 47

record_command \
    '05b2-26 Exact row counts after application startup' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to inspect Product table row counts after startup' 48

record_command \
    '05b2-27 Verify stale non-target volumes remain untouched' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify stale non-target volumes' 49

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Database: `RUNNING / HEALTHY`'
    printf '%s\n' '- API: `RUNNING / HEALTHY`'
    printf '%s\n' '- Worker: `RUNNING`'
    printf '%s\n' '- Frontend: `RUNNING`'
    printf '%s\n' '- Artifact persistence: `RECREATED`'
    printf '%s\n' '- Known NFS deletion diff: `PRESERVED / NOT MODIFIED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 8. Expected State

成功時:

```text
database:
  running / healthy

migrate:
  exited / 0

api:
  running / healthy

worker:
  running

frontend:
  running

ariadne-e1a_artifact-data:
  recreated

legacy alembic_version:
  absent

product revision:
  20260807_product_0006
```

また、既知の

```text
D deploy/.nfs000000000076202f00000088
```

というworking-tree差分はそのまま維持される。

---

## 9. Failure Semantics

途中で失敗した場合はretryしない。

特にapplication containerが一部だけ作成された場合も、

* stop
* rm
* restart
* rebuild
* source修正

を自動実行しない。

その時点の状態をresultとして保存し、人間が次の操作を決定する。

---

## 10. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
05b2_restore_application_stack_result.md
```

---

## 11. Stop Condition

result生成後は停止する。

test data作成やanalysis実行には進まない。

次phaseでpost-reset verificationを行う。
