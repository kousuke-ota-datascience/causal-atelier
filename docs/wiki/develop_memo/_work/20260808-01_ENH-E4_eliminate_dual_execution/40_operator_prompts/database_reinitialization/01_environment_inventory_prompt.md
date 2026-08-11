# 01 Environment Inventory — Operator Prompt

## 1. Task

DB完全初期化作業の Phase 01 として、repositoryおよびDB関連構成ファイルの所在を記録する。

このphaseは **read-only investigation** である。

DBへの接続、container操作、migration、database変更、ソースコード変更は行わない。

---

## 2. Agent Responsibility

あなた自身で調査方法を考えないこと。

あなた自身で追加コマンドを選択しないこと。

以下の「Execution Block」を**内容を変更せず、そのまま1回だけ実行すること。**

Execution Block自身が実行結果を以下へ生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
01_environment_inventory_result.md
```

実行後、resultの内容を解釈・要約・修正しないこと。

---

## 3. Prohibited Operations

このphaseでは以下を実行してはならない。

* `docker compose up`
* `docker compose down`
* `docker compose rm`
* `docker volume rm`
* containerの作成・停止・削除
* volumeの作成・削除
* DBへの接続
* SQL実行
* migration実行
* database reset
* schema変更
* `.env` 内容の表示
* secret値の表示
* source code変更
* configuration変更
* dependency install
* test実行
* application起動
* promptに記載されていない追加調査
* エラー発生後のretry
* エラー原因の修正

---

## 4. Execution Block

以下を**そのまま実行すること**。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/01_environment_inventory_result.md'

START_DIR="$(pwd)"

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
REPO_ROOT_EXIT=$?

if [ "${REPO_ROOT_EXIT}" -ne 0 ]; then
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
    printf '%s\n\n' '# 01 Environment Inventory Result'

    printf '%s\n\n' '## Metadata'

    printf '%s\n' "- Prompt: \`01_environment_inventory_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Invocation working directory: \`${START_DIR}\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '\n'
    printf '%s\n' '> This file contains command execution records only. No interpretation has been added.'
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
    '01-01 Current working directory' \
    'pwd'

run_command \
    '01-02 Git repository root' \
    'git rev-parse --show-toplevel'

run_command \
    '01-03 Current branch' \
    'git branch --show-current'

run_command \
    '01-04 Working tree status' \
    'git status --short'

run_command \
    '01-05 Repository root listing' \
    'ls -la'

run_command \
    '01-06 Docker and Compose files' \
    'find . -maxdepth 2 -type f \( -name "docker-compose.yml" -o -name "docker-compose.yaml" -o -name "compose.yml" -o -name "compose.yaml" -o -name "Dockerfile" -o -name "Dockerfile.*" \) -print | sort'

run_command \
    '01-07 Environment files' \
    'find . -maxdepth 2 -type f \( -name ".env" -o -name ".env.*" \) -print | sort'

run_command \
    '01-08 Dependency and migration configuration files' \
    'find . -maxdepth 3 -type f \( -name "pyproject.toml" -o -name "requirements.txt" -o -name "requirements-dev.txt" -o -name "Pipfile" -o -name "poetry.lock" -o -name "package.json" -o -name "alembic.ini" -o -name "manage.py" \) -print | sort'

run_command \
    '01-09 Migration directory candidates' \
    'find . -maxdepth 4 -type d \( -name "alembic" -o -name "migrations" -o -name "migration" \) -print | sort'

run_command \
    '01-10 Files containing DB-related configuration identifiers' \
    'git grep -l -E "DATABASE_URL|DB_HOST|DB_PORT|DB_NAME|POSTGRES|SQLALCHEMY|sqlite|postgresql|postgres" -- ":!*.lock" ":!package-lock.json" ":!pnpm-lock.yaml" ":!yarn.lock" || true'

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

## 5. After Execution

Execution Blockが終了したら、以下のみ確認すること。

```text
01_environment_inventory_result.md
```

が生成されていること。

resultの内容に対して以下を行わないこと。

* 要約
* 分析
* 判断
* 修正
* 追加調査
* 次phaseの実行

---

## 6. Response

Agentの最終応答は以下だけとする。

```text
01_environment_inventory_result.md を生成しました。
Phase 01 completed.
```

Execution Block自体が失敗しresultが生成されなかった場合のみ、上記定型文の代わりに、**Execution Blockが返したエラー出力をそのまま返すこと。**

エラー原因を推論したり修正したりしないこと。

---

## 7. Stop Condition

以下のいずれかで直ちに停止する。

1. `01_environment_inventory_result.md` が生成された
2. Execution Blockがエラー終了した

どちらの場合も、それ以上のコマンドを実行しないこと。
