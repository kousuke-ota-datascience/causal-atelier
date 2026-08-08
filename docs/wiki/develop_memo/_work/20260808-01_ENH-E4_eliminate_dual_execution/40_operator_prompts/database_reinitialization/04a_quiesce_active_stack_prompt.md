# 04a Quiesce Active Stack — Human Operator Prompt

## 1. Purpose

Database reinitialization の破壊操作に入る前に、現在稼働中の active Compose stack を停止する。

このphaseでは **containerを停止するだけ**とする。

以下はまだ削除しない。

* container
* Docker volume
* database data
* artifact data

このphase完了後に状態を確認してから、次phaseで不可逆な削除操作を行う。

---

## 2. Confirmed Active Environment

対象Git branch:

```text
refactor/ariadne_mvp_e4
```

対象Compose project:

```text
ariadne-e1a
```

対象Compose files:

```text
compose.yaml
compose.e1a.yaml
```

現在のactive persistence:

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

このphaseでは上記volumeを変更・削除しない。

---

## 3. Safety Principle

このphaseは、

> running system → stopped system

への状態遷移だけを行う。

persistent dataは保持する。

したがって、以下は禁止する。

* `docker compose down`
* `docker rm`
* `docker volume rm`
* `docker compose down -v`
* database schema変更
* SQL変更
* migration
* filesystem削除
* artifact削除
* stale `causal-atelier_*` volume操作

---

## 4. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

repository内の任意のdirectoryから実行してよい。

---

## 5. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/04a_quiesce_active_stack_result.md'

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
    printf '%s\n\n' '# 04a Quiesce Active Stack Result'

    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`04a_quiesce_active_stack_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target branch: `refactor/ariadne_mvp_e4`'
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '\n'
    printf '%s\n' '> This phase stops the active stack only. Persistent volumes are not removed.'
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
    '04a-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '04a-02 Docker daemon access precondition' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"' \
    || abort_phase 'Docker daemon inaccessible' 11

record_command \
    '04a-03 Active project container inventory before stop' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect active Compose project' 12

record_command \
    '04a-04 Database container project identity' \
    'test "$(docker inspect ariadne-e1a-database-1 --format "{{index .Config.Labels \"com.docker.compose.project\"}}")" = "ariadne-e1a"' \
    || abort_phase 'database container is not owned by expected Compose project' 13

record_command \
    '04a-05 Database volume mount precondition' \
    'test "$(docker inspect ariadne-e1a-database-1 --format "{{range .Mounts}}{{if eq .Destination \"/var/lib/postgresql/data\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_metadata-data"' \
    || abort_phase 'database volume mount differs from expected target' 14

record_command \
    '04a-06 API artifact volume mount precondition' \
    'test "$(docker inspect ariadne-e1a-api-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'API artifact volume mount differs from expected target' 15

record_command \
    '04a-07 Worker artifact volume mount precondition' \
    'test "$(docker inspect ariadne-e1a-worker-1 --format "{{range .Mounts}}{{if eq .Destination \"/state\"}}{{.Name}}{{end}}{{end}}")" = "ariadne-e1a_artifact-data"' \
    || abort_phase 'worker artifact volume mount differs from expected target' 16

record_command \
    '04a-08 Active volumes before stop' \
    'for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done' \
    || abort_phase 'unable to verify active volumes' 17

record_command \
    '04a-09 Stop active Compose stack' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml stop' \
    || abort_phase 'docker compose stop failed' 18

record_command \
    '04a-10 Active project container inventory after stop' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to verify stopped containers' 19

record_command \
    '04a-11 Active volumes after stop' \
    'for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done' \
    || abort_phase 'unable to verify preserved volumes after stop' 20

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Persistent volumes: `PRESERVED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 6. Expected State After Completion

成功時には、

```text
ariadne-e1a
```

projectのservice containerが停止している。

ただし以下のvolumeは存在し続ける。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

この時点では既存DBデータおよびartifactはまだ復旧可能である。

---

## 7. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
04a_quiesce_active_stack_result.md
```

---

## 8. Stop Condition

`04a_quiesce_active_stack_result.md` が生成されたら停止する。

次の操作はまだ実施しない。

特に以下は禁止する。

```text
docker compose down
docker volume rm
docker rm
```

次phaseで不可逆な削除対象を再確認してから実施する。
