# ENH-E6 Revised Requirements / Design Snapshot

**Document class:** Authoring Guide / Snapshot Applicability Record  
**Self-containment:** MUST.

## 1. Purpose

workflow templateではenhancement開始時点で改定・承認されたcanonical requirement/design snapshotを保存する。しかしENH-E6はcanonical `docs/wiki/requirement_definition/**`を変更しないbugfixであるため、fake revised snapshotを生成しない。本READMEがsnapshot applicability decisionを記録する。

## 2. Standard files

| Standard snapshot | ENH-E6 applicability | Reason |
|---|---|---|
| `00_product_concept_memo.md` | N/A / not instantiated | product concept revisionなし |
| `10_requirements_definition.md` | N/A / not instantiated | canonical requirement revisionなし |
| `21_logical_data_design.md` | N/A / not instantiated | data design revisionなし |
| `22_product_basic_design.md` | N/A / not instantiated | canonical basic design revisionなし |
| `23_api_interface_design.md` | N/A / not instantiated | API interface revisionなし |
| `30_detailed_design.md` | N/A / not instantiated | canonical detailed design revisionなし |

## 3. Authoring rules

- `docs/wiki/requirement_definition/**`はENH-E6ではREAD ONLY。
- ENH-local realization requirements/design deltaは親00層の03/04へ記録するが、canonical snapshotを装って複製しない。
- 将来Human ownerがcanonical requirement/design revisionを承認した場合はENH-E6 scope/contract前提が変わるため、勝手にsnapshotを追加せずcontract amendment/re-baseline routeを検討する。
- snapshotはCoding/Test Agentのexecution contractではない。
