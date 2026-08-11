# 04b Remove Active Containers — Human Operator Prompt

## 1. Purpose

Phase 04a により、active Compose stack `ariadne-e1a` の全service containerが正常停止した。

このphaseでは、停止済みのactive Compose containerのみを削除する。

**persistent volumeは削除しない。**

このphaseの目的は、

> stopped containers → no active-project containers

へ状態を遷移させ、次phaseでvolumeを明示的に削除できる状態にすることである。

---

## 2. Confirmed State

対象Compose project:

```text
ariadne-e1a
```

対象Compose files:

```text
compose.yaml
compose.e1a.yaml
```

削除対象container:

```text
ariadne-e1a-api-1
ariadne-e1a-worker-1
ariadne-e1a-frontend-1
ariadne-e1a-database-1
ariadne-e1a-migrate-1
```

保持対象volume:

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

以下のstale volumeには触れない。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

---

## 3. Safety Principle

このphaseではcontainerだけを削除する。

以下は禁止する。

* `docker volume rm`
* `docker compose down -v`
* `docker compose rm -v`
* Docker image削除
* network削除
* stale `causal-atelier_*` 操作
* DB変更
* artifact内容変更
* migration
* application起動

---

## 4. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

---

## 5. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/04b_remove_active_containers_result.md'

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
    printf '%s\n\n' '# 04b Remove Active Containers Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`04b_remove_active_containers_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '\n'
    printf '%s\n' '> This phase removes stopped containers only. Persistent volumes must remain.'
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
    '04b-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '04b-02 Active project containers before removal' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"' \
    || abort_phase 'unable to inspect active project containers' 11

record_command \
    '04b-03 Verify no active-project container is running' \
    'test -z "$(docker ps --filter label=com.docker.compose.project=ariadne-e1a -q)"' \
    || abort_phase 'one or more active-project containers are still running' 12

record_command \
    '04b-04 Verify metadata volume before container removal' \
    'test "$(docker volume inspect ariadne-e1a_metadata-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")" = "ariadne-e1a/metadata-data"' \
    || abort_phase 'metadata volume identity mismatch' 13

record_command \
    '04b-05 Verify artifact volume before container removal' \
    'test "$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'artifact volume identity mismatch' 14

record_command \
    '04b-06 Remove stopped active Compose containers' \
    'docker compose -p ariadne-e1a -f compose.yaml -f compose.e1a.yaml rm -f -s' \
    || abort_phase 'container removal failed' 15

record_command \
    '04b-07 Verify active project containers removed' \
    'test -z "$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a -q)"' \
    || abort_phase 'active-project containers remain after removal' 16

record_command \
    '04b-08 Verify metadata volume preserved' \
    'docker volume inspect ariadne-e1a_metadata-data --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"' \
    || abort_phase 'metadata volume missing after container removal' 17

record_command \
    '04b-09 Verify artifact volume preserved' \
    'docker volume inspect ariadne-e1a_artifact-data --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"' \
    || abort_phase 'artifact volume missing after container removal' 18

record_command \
    '04b-10 Metadata volume consumers after removal' \
    'docker ps -a --filter volume=ariadne-e1a_metadata-data --format "{{.ID}} {{.Names}} {{.Status}}"' \
    || abort_phase 'unable to inspect metadata volume consumers' 19

record_command \
    '04b-11 Artifact volume consumers after removal' \
    'docker ps -a --filter volume=ariadne-e1a_artifact-data --format "{{.ID}} {{.Names}} {{.Status}}"' \
    || abort_phase 'unable to inspect artifact volume consumers' 20

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Active containers: `REMOVED`'
    printf '%s\n' '- Persistent volumes: `PRESERVED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 6. Expected State

成功時:

```text
ariadne-e1a project containers:
  none

ariadne-e1a_metadata-data:
  exists
  no container consumer

ariadne-e1a_artifact-data:
  exists
  no container consumer
```

この時点でも既存DBデータとartifact dataはvolume上に残っている。

---

## 7. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
04b_remove_active_containers_result.md
```

---

## 8. Stop Condition

result生成後は停止する。

volumeは削除しない。

次phase `04c_delete_active_persistence` でのみ、persistent volumeを削除する。
