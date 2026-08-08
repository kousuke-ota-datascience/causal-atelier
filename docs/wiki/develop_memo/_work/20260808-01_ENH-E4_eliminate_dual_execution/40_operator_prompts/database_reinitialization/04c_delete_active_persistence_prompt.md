# 04c Delete Active Persistence — Human Operator Prompt

## 1. Purpose

Phase 04b により、active Compose project `ariadne-e1a` のcontainerがすべて削除され、以下のpersistent volumeにcontainer consumerが存在しないことが確認された。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

このphaseでは、この2つのactive persistent volumeを明示的に削除する。

この操作により、以下の既存データは復元不能になる。

* PostgreSQL database data
* Product execution / result / lineage 等のDBデータ
* artifact storage data

このphaseが、database reinitializationにおける最初の不可逆操作である。

---

## 2. Delete Targets

削除対象を以下に固定する。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

これ以外のvolumeを削除してはならない。

---

## 3. Explicit Non-targets

特に以下はこのphaseでは削除しない。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

これらは旧Compose projectに属するstale persistenceとして別工程で扱う。

また以下も削除しない。

* Docker images
* Docker network
* source code
* `.ariadne`
* migration files
* repository files
* Git data

---

## 4. Preconditions

このphaseは、以下がすべて成立する場合のみ削除操作を行う。

1. Git branchが `refactor/ariadne_mvp_e4`
2. Docker daemonへアクセス可能
3. `ariadne-e1a` project containerが0件
4. `ariadne-e1a_metadata-data` が存在する
5. `ariadne-e1a_artifact-data` が存在する
6. metadata volumeのCompose labelが期待値と一致する
7. artifact volumeのCompose labelが期待値と一致する
8. metadata volumeのcontainer consumerが0件
9. artifact volumeのcontainer consumerが0件

1つでも満たさない場合は、volumeを削除せずABORTする。

---

## 5. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

Agent sandboxでは実行しない。

repository内の任意のdirectoryから実行してよい。

---

## 6. Execution Block

以下を**変更せず1回だけ実行すること。**

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/04c_delete_active_persistence_result.md'

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
    printf '%s\n\n' '# 04c Delete Active Persistence Result'

    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`04c_delete_active_persistence_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '\n'
    printf '%s\n' '> WARNING: This phase irreversibly deletes active database and artifact persistence.'
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
        printf '%s\n' '- Persistent data deletion: `NOT EXECUTED OR NOT COMPLETED`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"

    trap - EXIT
    rm -f "${CMD_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit "${EXIT_CODE}"
}

record_command \
    '04c-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '04c-02 Docker daemon access precondition' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"' \
    || abort_phase 'Docker daemon inaccessible' 11

record_command \
    '04c-03 Verify active-project containers absent' \
    'COUNT="$(docker ps -a --filter label=com.docker.compose.project=ariadne-e1a -q | wc -l)"; printf "container_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'ariadne-e1a project containers still exist' 12

record_command \
    '04c-04 Verify metadata volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_metadata-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/metadata-data"' \
    || abort_phase 'metadata volume identity mismatch' 13

record_command \
    '04c-05 Verify artifact volume identity' \
    'IDENTITY="$(docker volume inspect ariadne-e1a_artifact-data --format "{{index .Labels \"com.docker.compose.project\"}}/{{index .Labels \"com.docker.compose.volume\"}}")"; printf "%s\n" "$IDENTITY"; test "$IDENTITY" = "ariadne-e1a/artifact-data"' \
    || abort_phase 'artifact volume identity mismatch' 14

record_command \
    '04c-06 Verify metadata volume has no consumers' \
    'COUNT="$(docker ps -a --filter volume=ariadne-e1a_metadata-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'metadata volume still has container consumers' 15

record_command \
    '04c-07 Verify artifact volume has no consumers' \
    'COUNT="$(docker ps -a --filter volume=ariadne-e1a_artifact-data -q | wc -l)"; printf "consumer_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'artifact volume still has container consumers' 16

record_command \
    '04c-08 Record target volumes immediately before deletion' \
    'for v in ariadne-e1a_metadata-data ariadne-e1a_artifact-data; do docker volume inspect "$v" --format "Name={{.Name}} CreatedAt={{.CreatedAt}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}} Mountpoint={{.Mountpoint}}"; done' \
    || abort_phase 'unable to record target volumes before deletion' 17

record_command \
    '04c-09 Verify stale causal-atelier volumes before active deletion' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then docker volume inspect "$v" --format "Name={{.Name}} Project={{index .Labels \"com.docker.compose.project\"}} Volume={{index .Labels \"com.docker.compose.volume\"}}"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to inspect explicit non-target volumes' 18

record_command \
    '04c-10 Delete active metadata volume' \
    'docker volume rm ariadne-e1a_metadata-data' \
    || abort_phase 'active metadata volume deletion failed' 20

record_command \
    '04c-11 Delete active artifact volume' \
    'docker volume rm ariadne-e1a_artifact-data' \
    || abort_phase 'active artifact volume deletion failed' 21

record_command \
    '04c-12 Verify active metadata volume absent' \
    'if docker volume inspect ariadne-e1a_metadata-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_metadata-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_metadata-data"; fi' \
    || abort_phase 'metadata volume still exists after deletion' 22

record_command \
    '04c-13 Verify active artifact volume absent' \
    'if docker volume inspect ariadne-e1a_artifact-data >/dev/null 2>&1; then printf "%s\n" "PRESENT: ariadne-e1a_artifact-data"; exit 1; else printf "%s\n" "ABSENT: ariadne-e1a_artifact-data"; fi' \
    || abort_phase 'artifact volume still exists after deletion' 23

record_command \
    '04c-14 Verify stale causal-atelier volumes were not deleted' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify explicit non-target volumes' 24

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Active metadata persistence: `DELETED`'
    printf '%s\n' '- Active artifact persistence: `DELETED`'
    printf '%s\n' '- Rebuild executed: `NO`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 7. Expected State After Completion

成功した場合、以下は存在しない。

```text
ariadne-e1a_metadata-data
ariadne-e1a_artifact-data
```

したがって、この時点で旧active environmentの、

* database records
* database schema
* Alembic state
* artifact files

は削除済みとなる。

一方で、以下はこのphaseでは変更されない。

```text
causal-atelier_metadata-data
causal-atelier_artifact-data
```

---

## 8. Important Failure Semantics

`04c-10` 以降は不可逆操作である。

例えば、

```text
metadata volume deletion succeeded
artifact volume deletion failed
```

となった場合、metadataだけ削除済みという部分状態が発生する。

その場合も自動retryや修復を行わない。

resultに状態を残して停止し、人間が次の操作を決定する。

---

## 9. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
04c_delete_active_persistence_result.md
```

---

## 10. Stop Condition

`04c_delete_active_persistence_result.md` が生成されたら停止する。

このphaseでは再構築を行わない。

特に以下をまだ実行しない。

```text
docker compose up
alembic upgrade head
application startup
```

再構築はPhase 05で別途実行する。
