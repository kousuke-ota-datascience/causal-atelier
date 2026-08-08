# 03a Docker Access Diagnosis — Operator Prompt

## 1. Task

Phase 03 の実行時に Docker API へのアクセスが以下のエラーで失敗した。

```text
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

そのため、Phase 03 で予定していた container / volume / database 状態の確認は完了していない。

このphaseでは、Docker daemonへのアクセス権限だけを固定コマンドで確認する。

**DB・container・volumeには変更を加えない。**

---

## 2. Agent Responsibility

Agent自身で解決方法を考えないこと。

Agent自身で以下を行わないこと。

* userをdocker groupへ追加
* permission変更
* socket permission変更
* Docker daemon再起動
* sudoによるDocker操作
* container起動・停止
* volume操作
* DB接続

以下のExecution Blockだけを、変更せず1回実行すること。

---

## 3. Execution Block

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/03a_docker_access_diagnosis_result.md'

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
    printf '%s\n\n' '# 03a Docker Access Diagnosis Result'

    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`03a_docker_access_diagnosis_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Permission diagnosis only. No Docker state was modified.'
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
    '03a-01 Effective user identity' \
    'id'

run_command \
    '03a-02 Effective group names' \
    'id -nG'

run_command \
    '03a-03 Docker socket metadata' \
    'if [ -e /var/run/docker.sock ]; then stat -c "path=%n type=%F mode=%a owner=%U group=%G uid=%u gid=%g" /var/run/docker.sock; else printf "%s\n" "ABSENT: /var/run/docker.sock"; fi'

run_command \
    '03a-04 Docker group definition' \
    'getent group docker || true'

run_command \
    '03a-05 Docker executable' \
    'command -v docker || true'

run_command \
    '03a-06 Docker CLI version' \
    'docker --version'

run_command \
    '03a-07 Direct Docker daemon access' \
    'docker version --format "client={{.Client.Version}} server={{.Server.Version}}"'

run_command \
    '03a-08 Sudo executable' \
    'command -v sudo || true'

run_command \
    '03a-09 Non-interactive sudo availability' \
    'if command -v sudo >/dev/null 2>&1; then sudo -n true; else printf "%s\n" "ABSENT: sudo"; exit 127; fi'

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

## 4. Important Restrictions

このphaseで以下を実行してはならない。

* `sudo docker ...`
* `sudo docker compose ...`
* `usermod`
* `groupadd`
* `gpasswd`
* `chmod`
* `chown`
* Docker socket変更
* Docker daemon再起動
* `docker compose up`
* `docker compose down`
* container操作
* volume操作
* DB接続
* migration
* source code変更
* configuration変更
* retry
* 独自の追加調査

`sudo -n true` は、非対話sudoが利用可能かを確認するだけであり、Docker操作には使用しない。

---

## 5. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
03a_docker_access_diagnosis_result.md
```

---

## 6. Response

成功時:

```text
03a_docker_access_diagnosis_result.md を生成しました。
Phase 03a completed.
```

Execution Block自体が失敗してresultが生成されなかった場合は、そのエラー出力のみ返すこと。

---

## 7. Stop Condition

result生成後は直ちに停止する。

権限問題を自動修復しないこと。
