# 06a Post-reset Functional Verification — Human Operator Prompt

## 1. Purpose

Phase 05b2 により、database reinitialization後のapplication stackが正常に復旧し、以下のclean stateが確認された。

```text
database:
  running / healthy

api:
  running / healthy

worker:
  running

frontend:
  running

Product application rows:
  0

artifact files:
  0

legacy alembic_version:
  absent

Product revision:
  20260807_product_0006
```

このphaseでは、

> 空の状態から再構築した現行システムが、実際のProduct workflowを正常実行できること

を検証する。

---

## 2. Verification Strategy

検証を2段階で実施する。

### A. Isolated Active Product Tests

`tests/product/` のActive Product testsを実行する。

ただし、実PostgreSQLを直接操作する `test_postgres_contract.py` は除外する。

また、host environmentのDB関連environment variableを明示的に除去して実行する。

このtest phaseによってactive Compose DBを変更してはならない。

### B. Running Compose Golden Path

現在稼働している `ariadne-e1a` stackに対して、

```text
tests/product/compose_golden_path_smoke.py
```

を実行する。

このGolden Pathは意図的にactive DBおよびartifact storageへtest dataを書き込む。

この書き込みはfunctional verificationのための一時的なものであり、次phase `06b` で再度完全初期化する。

---

## 3. Important State Transition

このphaseでは以下の状態遷移を意図する。

```text
clean running system
        |
        v
isolated Product tests
        |
        v
clean running system
        |
        v
Compose Golden Path
        |
        v
verified system with temporary test data
```

したがって、このphase完了時点ではDBをcleanとみなさない。

最終clean stateはPhase 06bで再構築する。

---

## 4. Prohibited Operations

以下は禁止する。

* legacy migration
* manual SQLによるデータ作成
* manual SQLによるschema変更
* manual artifact作成
* source code変更
* test code変更
* migration変更
* configuration変更
* container restart
* volume削除
* stale `causal-atelier_*` volume操作
* test failure後のretry
* test failure後の修正

Golden Pathが失敗した場合も、その時点の状態を記録して停止する。

---

## 5. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

repository rootで実行する。

Agent sandboxでは実行しない。

---

## 6. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/06a_post_reset_functional_verification_result.md'

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
    printf '%s\n\n' '# 06a Post-reset Functional Verification Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`06a_post_reset_functional_verification_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' '- Target Compose project: `ariadne-e1a`'
    printf '\n'
    printf '%s\n' '> Functional verification after clean database reinitialization.'
    printf '%s\n' '> Golden Path intentionally writes temporary verification data.'
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
        printf '%s\n' '- Final clean reinitialization: `NOT EXECUTED`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"

    trap - EXIT
    rm -f "${CMD_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit "${EXIT_CODE}"
}

record_command \
    '06a-01 Current branch precondition' \
    'CURRENT_BRANCH="$(git branch --show-current)"; printf "%s\n" "$CURRENT_BRANCH"; test "$CURRENT_BRANCH" = "refactor/ariadne_mvp_e4"' \
    || abort_phase 'unexpected Git branch' 10

record_command \
    '06a-02 Verify known runtime diff only' \
    'ACTUAL="$(git diff --name-status HEAD -- compose.yaml compose.e1a.yaml alembic_product.ini product_migrations src frontend deploy)"; EXPECTED="$(printf "D\tdeploy/.nfs000000000076202f00000088")"; printf "%s\n" "$ACTUAL"; test "$ACTUAL" = "$EXPECTED"' \
    || abort_phase 'unexpected runtime-area working-tree difference' 11

record_command \
    '06a-03 UV availability' \
    'uv --version' \
    || abort_phase 'uv executable unavailable' 12

record_command \
    '06a-04 Database health precondition' \
    'STATUS="$(docker inspect ariadne-e1a-database-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'database is not running and healthy' 13

record_command \
    '06a-05 API health precondition' \
    'STATUS="$(docker inspect ariadne-e1a-api-1 --format "{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running/healthy"' \
    || abort_phase 'API is not running and healthy' 14

record_command \
    '06a-06 Worker state precondition' \
    'STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'worker is not running' 15

record_command \
    '06a-07 Frontend state precondition' \
    'STATUS="$(docker inspect ariadne-e1a-frontend-1 --format "{{.State.Status}}")"; printf "%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'frontend is not running' 16

record_command \
    '06a-08 API readiness precondition' \
    'curl --fail --silent --show-error --max-time 10 http://127.0.0.1:18000/health/ready' \
    || abort_phase 'API readiness endpoint failed before verification' 17

record_command \
    '06a-09 Verify Product database is clean before tests' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT COALESCE(SUM(n_live_tup),0) FROM pg_stat_user_tables WHERE relname LIKE '\''product_%'\'' AND relname <> '\''alembic_version_product'\'';")"; printf "estimated_product_rows=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'Product database is not clean before verification' 18

record_command \
    '06a-10 Verify artifact storage is clean before tests' \
    'COUNT="$(docker exec ariadne-e1a-api-1 sh -lc '\''find /state -type f | wc -l'\'')"; printf "artifact_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'artifact storage is not clean before verification' 19

record_command \
    '06a-11 Run isolated Active Product tests' \
    'env -u ARIADNE_PRODUCT_DATABASE_URL -u ARIADNE_PRODUCT_TEST_DATABASE_URL -u ARIADNE_ARTIFACT_ROOT uv run --frozen pytest -q tests/product --ignore=tests/product/test_postgres_contract.py' \
    || abort_phase 'isolated Active Product tests failed' 30

record_command \
    '06a-12 Verify active database unchanged by isolated tests' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT COALESCE(SUM(n_live_tup),0) FROM pg_stat_user_tables WHERE relname LIKE '\''product_%'\'';")"; printf "estimated_product_rows=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'isolated Product tests modified active database' 31

record_command \
    '06a-13 Verify active artifact storage unchanged by isolated tests' \
    'COUNT="$(docker exec ariadne-e1a-api-1 sh -lc '\''find /state -type f | wc -l'\'')"; printf "artifact_file_count=%s\n" "$COUNT"; test "$COUNT" -eq 0' \
    || abort_phase 'isolated Product tests modified active artifact storage' 32

record_command \
    '06a-14 Run Compose Product Golden Path' \
    'timeout 300 env ARIADNE_GOLDEN_PATH_BASE_URL=http://127.0.0.1:18000/api/v1 uv run --frozen python tests/product/compose_golden_path_smoke.py' \
    || abort_phase 'Compose Product Golden Path failed' 40

record_command \
    '06a-15 API health after Golden Path' \
    'curl --fail --silent --show-error --include --max-time 10 http://127.0.0.1:18000/health/ready' \
    || abort_phase 'API readiness failed after Golden Path' 41

record_command \
    '06a-16 Worker state after Golden Path' \
    'STATUS="$(docker inspect ariadne-e1a-worker-1 --format "{{.State.Status}}")"; printf "status=%s\n" "$STATUS"; test "$STATUS" = "running"' \
    || abort_phase 'worker is not running after Golden Path' 42

record_command \
    '06a-17 Verify Golden Path created execution data' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_execution;")"; printf "product_execution=%s\n" "$COUNT"; test "$COUNT" -gt 0' \
    || abort_phase 'Golden Path produced no Product executions' 43

record_command \
    '06a-18 Verify Golden Path created result data' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_result;")"; printf "product_result=%s\n" "$COUNT"; test "$COUNT" -gt 0' \
    || abort_phase 'Golden Path produced no Product results' 44

record_command \
    '06a-19 Verify Golden Path created lineage data' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_lineage_edge;")"; printf "product_lineage_edge=%s\n" "$COUNT"; test "$COUNT" -gt 0' \
    || abort_phase 'Golden Path produced no lineage edges' 45

record_command \
    '06a-20 Verify Golden Path created artifact metadata' \
    'COUNT="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT count(*) FROM product_artifact;")"; printf "product_artifact=%s\n" "$COUNT"; test "$COUNT" -gt 0' \
    || abort_phase 'Golden Path produced no artifact metadata' 46

record_command \
    '06a-21 Verify Golden Path created artifact files' \
    'COUNT="$(docker exec ariadne-e1a-api-1 sh -lc '\''find /state/objects -type f | wc -l'\'')"; printf "artifact_object_files=%s\n" "$COUNT"; test "$COUNT" -gt 0' \
    || abort_phase 'Golden Path produced no artifact files' 47

record_command \
    '06a-22 Product table row counts after Golden Path' \
    'printf "%s\n" "SELECT format('\''SELECT %L AS table_name, count(*) AS row_count FROM public.%I;'\'', tablename, tablename) FROM pg_tables WHERE schemaname = '\''public'\'' ORDER BY tablename" "\\gexec" | docker exec -i ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off' \
    || abort_phase 'unable to record Product rows after Golden Path' 48

record_command \
    '06a-23 Artifact storage after Golden Path' \
    'docker exec ariadne-e1a-api-1 sh -lc '\''set -eu; printf "state_files="; find /state -type f | wc -l; printf "object_files="; find /state/objects -type f | wc -l; du -sh /state /state/objects'\''' \
    || abort_phase 'unable to record artifact state after Golden Path' 49

record_command \
    '06a-24 Verify legacy Alembic table remains absent' \
    'VALUE="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT to_regclass('\''public.alembic_version'\'');")"; printf "legacy_version_table=%s\n" "${VALUE:-NULL}"; test -z "$VALUE"' \
    || abort_phase 'legacy Alembic table appeared during functional verification' 50

record_command \
    '06a-25 Verify Product revision unchanged' \
    'REVISION="$(docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -Atqc "SELECT version_num FROM alembic_version_product;")"; printf "product_revision=%s\n" "$REVISION"; test "$REVISION" = "20260807_product_0006"' \
    || abort_phase 'Product migration revision changed unexpectedly' 51

record_command \
    '06a-26 Verify stale non-target volumes remain untouched' \
    'for v in causal-atelier_metadata-data causal-atelier_artifact-data; do if docker volume inspect "$v" >/dev/null 2>&1; then printf "PRESERVED: %s\n" "$v"; else printf "ABSENT: %s\n" "$v"; fi; done' \
    || abort_phase 'unable to verify stale non-target volumes' 52

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Isolated Active Product tests: `PASSED`'
    printf '%s\n' '- Compose Product Golden Path: `PASSED`'
    printf '%s\n' '- Execution / Result / Lineage / Artifact creation: `VERIFIED`'
    printf '%s\n' '- Active persistence state: `CONTAINS TEMPORARY VERIFICATION DATA`'
    printf '%s\n' '- Final clean reinitialization required: `YES`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 7. Failure Semantics

このphaseではGolden Pathがactive persistenceへ書き込む。

したがって、途中で失敗した場合でもtest dataが部分的に残る可能性がある。

失敗時には、

* manual cleanup
* retry
* database reset
* container restart
* code修正

を自動実行しない。

その状態をresultに残して停止する。

---

## 8. Expected Success Evidence

成功した場合、少なくとも以下が確認される。

```text
Isolated Active Product tests:
  PASS

Compose Golden Path:
  PASS

product_execution:
  > 0

product_result:
  > 0

product_lineage_edge:
  > 0

product_artifact:
  > 0

artifact object files:
  > 0

API:
  healthy

Worker:
  running

legacy alembic_version:
  absent

Product revision:
  20260807_product_0006
```

---

## 9. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
06a_post_reset_functional_verification_result.md
```

---

## 10. Stop Condition

result生成後は停止する。

**Golden Pathで生成されたtest dataをまだ削除しない。**

次phase `06b` にて、今回すでに検証済みのreset/rebuild経路を再度適用し、最終的な空状態へ戻す。
