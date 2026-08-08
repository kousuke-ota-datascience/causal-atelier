# 02 Database Configuration — Operator Prompt

## 1. Task

DB完全初期化作業の Phase 02 として、DB・migration・Compose構成を固定コマンドで記録する。

このphaseは **read-only** である。

`database_reinitialization/README.md` の運用規則に従うこと。

Agent自身で追加調査・判断・retryを行わないこと。

---

## 2. Execution

以下のExecution Blockを**変更せず1回だけ実行すること。**

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/02_database_configuration_result.md'

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
    printf '%s\n\n' '# 02 Database Configuration Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`02_database_configuration_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '\n'
    printf '%s\n' '> Command execution records only. No interpretation has been added.'
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
    '02-01 Current branch' \
    'git branch --show-current'

run_command \
    '02-02 Compose database and persistence configuration' \
    'sed -n "1,120p" compose.yaml'

run_command \
    '02-03 E1a Compose override' \
    'sed -n "1,120p" compose.e1a.yaml'

run_command \
    '02-04 Legacy Alembic configuration' \
    'grep -nE "script_location|sqlalchemy\.url" alembic.ini'

run_command \
    '02-05 Product Alembic configuration' \
    'grep -nE "script_location|sqlalchemy\.url" alembic_product.ini'

run_command \
    '02-06 Legacy Alembic runtime configuration' \
    'grep -nE "ARIADNE_DATABASE_URL|target_metadata|version_table|sqlalchemy\.url" migrations/env.py'

run_command \
    '02-07 Product Alembic runtime configuration' \
    'grep -nE "ARIADNE_PRODUCT_DATABASE_URL|target_metadata|version_table|sqlalchemy\.url" product_migrations/env.py'

run_command \
    '02-08 Web API database and artifact configuration' \
    'grep -nE "ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|create_engine" src/ariadne/interfaces/web_api/dependencies.py'

run_command \
    '02-09 Worker database and artifact configuration' \
    'grep -nE "ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|create_engine" src/ariadne/interfaces/worker/runner.py'

run_command \
    '02-10 Legacy migration files' \
    'find migrations/versions -maxdepth 1 -type f -name "*.py" -print | sort'

run_command \
    '02-11 Product migration files' \
    'find product_migrations/versions -maxdepth 1 -type f -name "*.py" -print | sort'

run_command \
    '02-12 Legacy migration revision chain' \
    'grep -HnE "^(revision|down_revision)[[:space:]]*=" migrations/versions/*.py || true'

run_command \
    '02-13 Product migration revision chain' \
    'grep -HnE "^(revision|down_revision)[[:space:]]*=" product_migrations/versions/*.py || true'

run_command \
    '02-14 DB-related shell environment variable names' \
    'env | sed "s/=.*//" | grep -E "^(ARIADNE_DATABASE_URL|ARIADNE_PRODUCT_DATABASE_URL|ARIADNE_PRODUCT_TEST_DATABASE_URL|ARIADNE_ARTIFACT_ROOT|ARIADNE_STATE_DIR)$" | sort || true'

run_command \
    '02-15 Compose services' \
    'docker compose -f compose.yaml config --services'

run_command \
    '02-16 Compose volumes' \
    'docker compose -f compose.yaml config --volumes'

run_command \
    '02-17 E1a merged Compose services' \
    'docker compose -f compose.yaml -f compose.e1a.yaml config --services'

run_command \
    '02-18 E1a merged Compose volumes' \
    'docker compose -f compose.yaml -f compose.e1a.yaml config --volumes'

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

## 3. Restrictions

このphaseでは以下を行わないこと。

* DB接続
* SQL実行
* `docker compose up`
* `docker compose down`
* container操作
* volume操作
* migration実行
* ファイル変更
* `.env` 内容表示
* 環境変数値の表示
* test実行
* application起動
* 追加コマンド実行
* retry

Execution Block内の `docker compose ... config` はCompose設定のread-only解析に限定する。

---

## 4. Stop

Execution Block終了後は追加操作を行わないこと。

成功時の最終応答:

```text
02_database_configuration_result.md を生成しました。
Phase 02 completed.
```

Execution Block自体が失敗してresultが生成されなかった場合は、そのエラー出力だけを返すこと。
