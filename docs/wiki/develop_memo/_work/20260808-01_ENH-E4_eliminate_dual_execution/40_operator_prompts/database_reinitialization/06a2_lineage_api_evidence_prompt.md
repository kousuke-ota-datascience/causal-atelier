# 06a2 Lineage API Evidence — Human Operator Prompt

## 1. Purpose

Phase 06a1 により以下が確認された。

```text
Golden Path root Result:
  present

product_lineage_edge:
  0 rows

Result lineage API:
  HTTP success
```

しかし、Phase 06a1 の計測スクリプトでは lineage API response のsummaryがresultへ記録されなかった。

このphaseでは、その欠落だけを補完する。

Golden Pathは再実行しない。

Product stateは変更しない。

---

## 2. Target

対象Result:

```text
9203bd6d-abbc-47a4-9bc2-bc5ea061f98c
```

対象endpoint:

```text
http://127.0.0.1:18000/api/v1/results/9203bd6d-abbc-47a4-9bc2-bc5ea061f98c/lineage
```

---

## 3. Record

以下のみ記録する。

* lineage API HTTP success
* node count
* edge count
* node type別件数
* Golden Path required node typesの存在
* `product_lineage_edge` row count
* Golden Path source上のlineage assertion

---

## 4. Prohibited Operations

以下は禁止する。

* Golden Path再実行
* INSERT
* UPDATE
* DELETE
* migration
* container操作
* volume操作
* source code変更
* test code変更
* retry
* final reset

---

## 5. Execution Block

以下を変更せず1回だけ実行する。

`````bash
bash <<'OPERATOR_SCRIPT'
set -u

RESULT_REL='docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/40_operator_prompts/database_reinitialization/06a2_lineage_api_evidence_result.md'
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
LINEAGE_JSON="$(mktemp)"
ERROR_OUTPUT="$(mktemp)"

cleanup() {
    rm -f "${TMP_RESULT}" "${LINEAGE_JSON}" "${ERROR_OUTPUT}"
}
trap cleanup EXIT

cd "${REPO_ROOT}" || exit 4

{
    printf '%s\n\n' '# 06a2 Lineage API Evidence Result'
    printf '%s\n\n' '## Metadata'
    printf '%s\n' "- Prompt: \`06a2_lineage_api_evidence_prompt.md\`"
    printf '%s\n' "- Started at: \`$(date -Iseconds)\`"
    printf '%s\n' "- Repository root: \`${REPO_ROOT}\`"
    printf '%s\n' "- Git commit: \`$(git rev-parse HEAD)\`"
    printf '%s\n' "- Root result: \`${ROOT_RESULT_ID}\`"
    printf '\n'
    printf '%s\n' '> Read-only evidence capture. No Product state was modified.'
} > "${TMP_RESULT}"

curl \
    --fail \
    --silent \
    --show-error \
    --max-time 10 \
    "http://127.0.0.1:18000/api/v1/results/${ROOT_RESULT_ID}/lineage" \
    > "${LINEAGE_JSON}" 2> "${ERROR_OUTPUT}"

CURL_RC=$?

{
    printf '\n## 06a2-01 Lineage API request\n\n'
    printf '%s\n' '### Exit Code'
    printf '\n````text\n%s\n````\n' "${CURL_RC}"
    printf '%s\n' '### Error Output'
    printf '\n````text\n'
    cat "${ERROR_OUTPUT}"
    printf '````\n'
} >> "${TMP_RESULT}"

if [ "${CURL_RC}" -ne 0 ]; then
    {
        printf '\n## Completion\n\n'
        printf '%s\n' '- Phase execution: `ABORTED`'
        printf '%s\n' '- Reason: `lineage API request failed`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"
    trap - EXIT
    rm -f "${LINEAGE_JSON}" "${ERROR_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit 10
fi

LINEAGE_JSON="${LINEAGE_JSON}" uv run --frozen python - <<'PY' >> "${TMP_RESULT}" 2>&1
import json
import os
from collections import Counter

with open(os.environ["LINEAGE_JSON"], encoding="utf-8") as f:
    payload = json.load(f)

nodes = payload["nodes"]
edges = payload["edges"]

counts = Counter(node["node_type"] for node in nodes)

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
print("## 06a2-02 Lineage API summary")
print()
print("````text")
print(f"node_count={len(nodes)}")
print(f"edge_count={len(edges)}")
for node_type in sorted(counts):
    print(f"node_type[{node_type}]={counts[node_type]}")
print(
    "required_node_types_present="
    + str(required.issubset(counts.keys())).lower()
)
print(
    "missing_required_node_types="
    + ",".join(sorted(required - counts.keys()))
)
print("````")
PY

PYTHON_RC=$?

if [ "${PYTHON_RC}" -ne 0 ]; then
    {
        printf '\n## Completion\n\n'
        printf '%s\n' '- Phase execution: `ABORTED`'
        printf '%s\n' '- Reason: `lineage JSON summary failed`'
    } >> "${TMP_RESULT}"

    mv "${TMP_RESULT}" "${RESULT_PATH}"
    trap - EXIT
    rm -f "${LINEAGE_JSON}" "${ERROR_OUTPUT}"

    printf 'Created aborted result: %s\n' "${RESULT_PATH}"
    exit 11
fi

{
    printf '\n## 06a2-03 Persisted LineageEdge count\n\n'
    printf '%s\n' '````text'
    docker exec ariadne-e1a-database-1 \
        psql -X -U ariadne -d ariadne -Atqc \
        'SELECT count(*) FROM product_lineage_edge;'
    printf '%s\n' '````'

    printf '\n## 06a2-04 Golden Path lineage assertion\n\n'
    printf '%s\n' '````python'
    sed -n '228,231p' tests/product/compose_golden_path_smoke.py
    printf '%s\n' '````'

    printf '\n## Completion\n\n'
    printf '%s\n' "- Finished at: \`$(date -Iseconds)\`"
    printf '%s\n' '- Phase execution: `COMPLETED`'
    printf '%s\n' '- Product state modified: `NO`'
} >> "${TMP_RESULT}"

mv "${TMP_RESULT}" "${RESULT_PATH}"

trap - EXIT
rm -f "${LINEAGE_JSON}" "${ERROR_OUTPUT}"

printf 'Created: %s\n' "${RESULT_PATH}"
OPERATOR_SCRIPT
`````

---

## 6. Result

以下を生成する。

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
database_reinitialization/
06a2_lineage_api_evidence_result.md
```

---

## 7. Stop Condition

result生成後は停止する。

Golden Pathを再実行しない。

temporary verification dataもまだ削除しない。
