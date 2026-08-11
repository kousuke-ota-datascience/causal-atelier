# 06a1 Lineage Semantics Assessment — Human Operator Prompt

## 1. Purpose

Phase 06a のfunctional verificationでは、以下が確認された。

```text
Isolated Active Product tests:
  131 passed

Compose Golden Path:
  PASS

product_execution:
  7

product_result:
  11

product_lineage_edge:
  0
```

Phase 06a は、

```text
product_lineage_edge > 0
```

という追加verification条件によってABORTした。

しかし、Golden Path自体はResult lineage APIを検証した後にPASSしている。

このphaseでは、

> 現行Product lineageが `product_lineage_edge` の永続行ではなく、
> 他のProduct entity relationshipから動的に構築されているか

をread-onlyで記録する。

このphaseではデータを変更しない。

---

## 2. Target Golden Path Result

Phase 06aで生成されたGolden Path root resultを以下に固定する。

```text
9203bd6d-abbc-47a4-9bc2-bc5ea061f98c
```

API endpoint:

```text
http://127.0.0.1:18000/api/v1/results/9203bd6d-abbc-47a4-9bc2-bc5ea061f98c/lineage
```

---

## 3. Questions to Record

以下だけを確認する。

1. root Resultが現在も存在するか
2. lineage APIが成功するか
3. lineage APIが返すnode数
4. lineage APIが返すedge数
5. node types
6. Golden Pathが要求している主要node typesが存在するか
7. `product_lineage_edge` のrow count
8. `LineageQueryService` がどのようにedgeを生成しているか
9. Product repository層にLineageEdge repositoryが存在するか

Agentまたはoperatorがアーキテクチャ判断を行わない。

生の事実のみ記録する。

---

## 4. Safety

このphaseは **read-only** である。

以下は禁止する。

* INSERT
* UPDATE
* DELETE
* TRUNCATE
* DROP
* ALTER
* migration
* container restart
* container stop
* volume操作
* source code変更
* test code変更
* retry
* Golden Path再実行
* final reset

---

## 5. Execution Environment

Docker daemonへアクセス可能なホストterminalで実行する。

repository rootから実行する。

---

## 6. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/06a1_lineage_semantics_assessment_result.md'

ROOT_RESULT_ID='9203bd6d-abbc-47a4-9bc2-bc5ea061f98c'

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
LINEAGE_JSON="$(mktemp)"

cleanup() {
    rm -f "${TMP_RESULT}" "${CMD_OUTPUT}" "${LINEAGE_JSON}"
}
trap cleanup EXIT

cd "${REPO_ROOT}" || exit 4

{
    printf '%s\n\n' '# 06a1 Lineage Semantics Assessment Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`06a1_lineage_semantics_assessment_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' "- Golden Path root result: \`${ROOT_RESULT_ID}\`"
    printf '\n'
    printf '%s\n' '> Read-only assessment. No Product state was modified.'
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

record_command \
    '06a1-01 Current branch' \
    'git branch --show-current'

record_command \
    '06a1-02 Application service states' \
    'docker ps --filter label=com.docker.compose.project=ariadne-e1a --format "table {{.Names}}\t{{.Status}}\t{{.Label \"com.docker.compose.service\"}}"'

record_command \
    '06a1-03 Golden Path root Result presence' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT result_id, execution_id, result_type, scientific_status FROM product_result WHERE result_id = '\''9203bd6d-abbc-47a4-9bc2-bc5ea061f98c'\'';"'

record_command \
    '06a1-04 Persisted product_lineage_edge count' \
    'docker exec ariadne-e1a-database-1 psql -X -U ariadne -d ariadne -P pager=off -c "SELECT count(*) AS product_lineage_edge_count FROM product_lineage_edge;"'

: > "${CMD_OUTPUT}"

curl \
    --fail \
    --silent \
    --show-error \
    --max-time 10 \
    "http://127.0.0.1:18000/api/v1/results/${ROOT_RESULT_ID}/lineage" \
    > "${LINEAGE_JSON}" 2> "${CMD_OUTPUT}"

CURL_RC=$?

{
    printf '\n## 06a1-05 Lineage API request\n\n'

    printf '%s\n\n' '### Command'
    printf '%s\n' '````bash'
    printf '%s\n' "curl --fail --silent --show-error http://127.0.0.1:18000/api/v1/results/${ROOT_RESULT_ID}/lineage"
    printf '%s\n\n' '````'

    printf '%s\n\n' '### Exit Code'
    printf '%s\n' '````text'
    printf '%s\n' "${CURL_RC}"
    printf '%s\n\n' '````'

    printf '%s\n\n' '### Error Output'
    printf '%s\n' '````text'
    cat "${CMD_OUTPUT}"
    printf '%s\n' '````'
} >> "${TMP_RESULT}"

if [ "${CURL_RC}" -eq 0 ]; then

    LINEAGE_JSON="${LINEAGE_JSON}" python - <<'PY' >> "${TMP_RESULT}"
import json
import os
from collections import Counter

path = os.environ["LINEAGE_JSON"]

with open(path, encoding="utf-8") as f:
    payload = json.load(f)

nodes = payload.get("nodes", [])
edges = payload.get("edges", [])

node_types = Counter(node.get("node_type") for node in nodes)

required = {
    "Project",
    "DatasetVersion",
    "Execution",
    "Result",
    "GraphVersion",
    "Artifact",
    "Annotation",
}

print()
print("## 06a1-06 Lineage API summary")
print()
print("### Output")
print()
print("````text")
print(f"node_count={len(nodes)}")
print(f"edge_count={len(edges)}")
print("node_types:")
for node_type in sorted(node_types):
    print(f"  {node_type}={node_types[node_type]}")
print("required_node_types_present=" + str(required.issubset(node_types.keys())).lower())
print("missing_required_node_types=" + ",".join(sorted(required - node_types.keys())))
print("````")
PY

else

    {
        printf '\n## 06a1-06 Lineage API summary\n\n'
        printf '%s\n' '````text'
        printf '%s\n' 'SKIPPED: lineage API request failed.'
        printf '%s\n' '````'
    } >> "${TMP_RESULT}"

fi

record_command \
    '06a1-07 Golden Path lineage assertions in source' \
    'sed -n "221,236p" tests/product/compose_golden_path_smoke.py'

record_command \
    '06a1-08 LineageQueryService construction logic' \
    'grep -nE "def get_lineage|def add_edge|add_edge\\(|uow\\.|return LineageView" src/ariadne/product/application/lineage_query_service.py'

record_command \
    '06a1-09 Persistent LineageEdge ORM definition' \
    'grep -nA30 -B3 "class LineageEdgeOrm" src/ariadne/product/persistence/orm_models.py'

record_command \
    '06a1-10 Product source references to LineageEdge persistence' \
    'git grep -n -E "LineageEdgeOrm|product_lineage_edge" -- src/ariadne/product || true'

record_command \
    '06a1-11 Product repository references to lineage' \
    'grep -nEi "lineage|LineageEdge" src/ariadne/product/persistence/repositories.py || true'

{
    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Product state modified: `NO`'
    printf '%s\n' '- Final clean reinitialization: `NOT EXECUTED`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${CMD_OUTPUT}" "${LINEAGE_JSON}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 7. Interpretation Boundary

このphaseのoperatorは結果を解釈しない。

特に以下を断定しない。

```text
product_lineage_edge is obsolete
product_lineage_edge should be deleted
dynamic lineage is correct architecture
persistent lineage is correct architecture
```

このphaseでは事実だけ記録する。

アーキテクチャ上の扱いは、database reinitialization完了後の
`ENH-E4 eliminate dual execution` 本体で判断する。

---

## 8. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
06a1_lineage_semantics_assessment_result.md
```

---

## 9. Stop Condition

result生成後は停止する。

Golden Pathを再実行しない。

temporary verification dataをまだ削除しない。

次phaseで最終clean reinitializationを行う。
