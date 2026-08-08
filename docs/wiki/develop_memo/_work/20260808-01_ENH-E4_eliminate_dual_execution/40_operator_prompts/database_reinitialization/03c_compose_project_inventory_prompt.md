# 03c Compose Project Inventory — Human Operator Prompt

## 1. Purpose

Phase 03b により、以下の2つのCompose projectに属する永続volumeが存在することが確認された。

```text
ariadne-e1a
causal-atelier
```

このphaseでは、それぞれのprojectについて、

* containerの存在
* container状態
* volumeとの関連

だけをread-onlyで確認する。

DBは起動しない。

volumeは削除しない。

---

## 2. Execution Environment

Phase 03b と同じ、Docker daemonへアクセス可能なホストterminalで実行する。

---

## 3. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03c_compose_project_inventory_result.md'

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
    printf '%s\n\n' '# 03c Compose Project Inventory Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03c_compose_project_inventory_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Read-only Compose project inventory. No container or volume was modified.'
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
    '03c-01 causal-atelier Compose project containers' \
    'docker ps -a --filter label=com.docker.compose.project=causal-atelier --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"'

run_command \
    '03c-02 ariadne-e1a Compose project containers' \
    'docker ps -a --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"'

run_command \
    '03c-03 causal-atelier Compose project volumes' \
    'docker volume ls --filter label=com.docker.compose.project=causal-atelier --format "{{.Name}}" | sort'

run_command \
    '03c-04 ariadne-e1a Compose project volumes' \
    'docker volume ls --filter label=com.docker.compose.project=ariadne-e1a --format "{{.Name}}" | sort'

run_command \
    '03c-05 causal-atelier metadata volume consumers' \
    'docker ps -a --filter volume=causal-atelier_metadata-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03c-06 ariadne-e1a metadata volume consumers' \
    'docker ps -a --filter volume=ariadne-e1a_metadata-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03c-07 causal-atelier artifact volume consumers' \
    'docker ps -a --filter volume=causal-atelier_artifact-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03c-08 ariadne-e1a artifact volume consumers' \
    'docker ps -a --filter volume=ariadne-e1a_artifact-data --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03c-09 Target volume creation timestamps' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} CreatedAt={{.CreatedAt}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; done'

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

## 4. Prohibited Operations

以下は禁止する。

* container起動
* container停止
* container削除
* volume削除
* volume作成
* DB接続
* migration
* `docker compose up`
* `docker compose down`
* permission変更
* retry
* 追加調査

---

## 5. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03c_compose_project_inventory_result.md
```

生成後は停止する。
