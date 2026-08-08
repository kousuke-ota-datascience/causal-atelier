# 03e Active Artifact Inventory — Human Operator Prompt

## 1. Purpose

Phase 03d により、現在のactive databaseにはProduct schemaのみが存在し、既存のProduct application dataが保存されていることが確認された。

また、現行Composeではartifact実体がdatabaseとは別のDocker volumeに保存されている。

このphaseでは、Reset前のactive artifact storage状態をread-onlyで記録する。

この結果をもって、破壊操作前のinventoryを完了する。

---

## 2. Confirmed Target

現在のactive Compose project:

```text
ariadne-e1a
```

artifact volume:

```text
ariadne-e1a_artifact-data
```

artifact volumeを使用しているcontainer:

```text
ariadne-e1a-api-1
ariadne-e1a-worker-1
```

Compose上のartifact root:

```text
/state/objects
```

このphaseでは `ariadne-e1a-api-1` をinspection containerとして使用する。

---

## 3. Scope

確認する対象は以下のみ。

* API containerの稼働状態
* artifact volume mount
* `/state` の存在
* `/state/objects` の存在
* 使用容量
* file数
* directory数
* `/state` 直下および浅い階層の構造

ファイル内容は表示しない。

---

## 4. Safety

このphaseは **read-only** である。

以下は禁止する。

* ファイル作成
* ファイル変更
* ファイル削除
* directory作成
* volume削除
* volume作成
* container restart
* container stop
* `docker compose down`
* DB変更
* migration
* application設定変更
* permission変更
* retry
* 追加調査

---

## 5. Execution Environment

Phase 03b〜03dと同じ、Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

---

## 6. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03e_active_artifact_inventory_result.md'

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
    printf '%s\n\n' '# 03e Active Artifact Inventory Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03e_active_artifact_inventory_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target container: `ariadne-e1a-api-1`'
    printf '%s\n' '- Target volume: `ariadne-e1a_artifact-data`'
    printf '%s\n' '- Target path: `/state`'
    printf '\n'
    printf '%s\n' '> Read-only artifact inventory. File contents were not inspected.'
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
    '03e-01 API container state' \
    'docker ps --filter name="^/ariadne-e1a-api-1$" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"'

run_command \
    '03e-02 API container mount mapping' \
    'docker inspect ariadne-e1a-api-1 --format "{{json .Mounts}}"'

run_command \
    '03e-03 Artifact volume metadata' \
    'docker volume inspect ariadne-e1a_artifact-data --format "Name={{.Name}} Driver={{.Driver}} Mountpoint={{.Mountpoint}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"'

run_command \
    '03e-04 State directory presence' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; test -d /state; printf "%s\n" "PRESENT: /state"; if [ -d /state/objects ]; then printf "%s\n" "PRESENT: /state/objects"; else printf "%s\n" "ABSENT: /state/objects"; fi'\'''

run_command \
    '03e-05 State storage usage' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; du -sh /state; if [ -d /state/objects ]; then du -sh /state/objects; fi'\'''

run_command \
    '03e-06 State file count' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; find /state -type f | wc -l'\'''

run_command \
    '03e-07 Artifact object file count' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; if [ -d /state/objects ]; then find /state/objects -type f | wc -l; else printf "%s\n" "ABSENT: /state/objects"; fi'\'''

run_command \
    '03e-08 State directory count' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; find /state -type d | wc -l'\'''

run_command \
    '03e-09 Shallow state tree' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; find /state -mindepth 1 -maxdepth 2 -print | sort'\'''

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

## 7. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03e_active_artifact_inventory_result.md
```

---

## 8. Stop Condition

`03e_active_artifact_inventory_result.md` が生成されたら停止する。

以下には進まない。

* container停止
* volume削除
* database reset
* rebuild

次の破壊操作は、result確認後に別promptとして実施する。
