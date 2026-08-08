# 05b1 Runtime Diff Assessment — Human Operator Prompt

## 1. Purpose

Phase 05b はapplication startup前のworking-tree preconditionでABORTした。

検出された差分は以下である。

```text
D deploy/.nfs000000000076202f00000088
```

このphaseでは、この差分がapplication runtimeへ影響するファイルなのかをread-onlyで確認する。

ファイルの復元・削除・変更は行わない。

---

## 2. Scope

以下のみ確認する。

1. 現在のworking tree差分
2. `.nfs...` ファイルがGit管理対象であること
3. HEAD上の `.nfs...` と `deploy/nginx.conf` の内容同一性
4. Composeが実際に参照するdeployファイル
5. `.nfs...` ファイル名へのコード上の参照有無
6. `.gitignore` にNFS一時ファイル除外規則があるか

---

## 3. Prohibited Operations

以下は禁止する。

* `git restore`
* `git checkout --`
* `git reset`
* `git clean`
* ファイル作成
* ファイル削除
* ファイル変更
* `.gitignore` 変更
* container操作
* volume操作
* application startup
* migration
* DB変更
* retry
* 追加調査

---

## 4. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/05b1_runtime_diff_assessment_result.md'

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
    printf '%s\n\n' '# 05b1 Runtime Diff Assessment Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`05b1_runtime_diff_assessment_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Read-only assessment of the working-tree difference that blocked Phase 05b.'
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
}

record_command \
    '05b1-01 Current branch' \
    'git branch --show-current'

record_command \
    '05b1-02 Current working tree status' \
    'git status --short'

record_command \
    '05b1-03 Runtime-area diff names' \
    'git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy'

record_command \
    '05b1-04 Git-tracked deploy files' \
    'git ls-files deploy | sort'

record_command \
    '05b1-05 HEAD NFS file SHA-256' \
    'git show HEAD:deploy/.nfs000000000076202f00000088 | sha256sum'

record_command \
    '05b1-06 Working-tree nginx.conf SHA-256' \
    'sha256sum deploy/nginx.conf'

record_command \
    '05b1-07 Compare HEAD NFS file with nginx.conf' \
    'git show HEAD:deploy/.nfs000000000076202f00000088 | cmp - deploy/nginx.conf; RC=$?; printf "cmp_exit_code=%s\n" "$RC"; exit "$RC"'

record_command \
    '05b1-08 Compose frontend configuration' \
    'sed -n "50,60p" compose.yaml'

record_command \
    '05b1-09 References to tracked NFS filename' \
    'git grep -n -F ".nfs000000000076202f00000088" HEAD -- . || true'

record_command \
    '05b1-10 NFS ignore rules' \
    'grep -nE "(^|/)\.nfs|\*\.nfs|\.nfs\*" .gitignore || true'

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Working tree modified by this phase: `NO`'
    printf '%s\n' '- Application startup: `NOT EXECUTED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 5. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
05b1_runtime_diff_assessment_result.md
```

---

## 6. Stop Condition

result生成後は停止する。

このphaseでは `.nfs...` ファイルを復元・削除・ignore追加しない。

Phase 05b の再実行にも進まない。
