# Revised Requirements / Design Snapshot

- Snapshot baseline: `386521d18e9c5cc4d42fb99c97c212430908afc3`
- ENH-E8 Requirement semantic delta: `NONE`
- Snapshot status: `APPROVED`
- Freeze mode: `IMMUTABLE_BASELINE_PLUS_APPROVED_E8_DELTA`

`00_product_concept_memo.md`, `10_requirements_definition.md`, `21_logical_data_design.md`, `23_api_interface_design.md` はbaseline commitのapproved canonical snapshotを変更せず保持する。

`22_product_basic_design.md` はbaseline contentにENH-E8 Basic Design addendumをmaterializeしたapproved effective snapshotである。

`30_detailed_design.md` はENH-E8 frontend Detailed Design addendumを本workflow内に保持し、**baseline commit `386521d18e9c5cc4d42fb99c97c212430908afc3` のcanonical approved `30_detailed_design.md` と本addendumの組を一体のimmutable composite effective snapshotとしてfreezeする。**

このfreeze方式では次をauthorityとする。

1. baseline部分: immutable commit `386521d18e9c5cc4d42fb99c97c212430908afc3`
2. E8変更部分: 本directoryのapproved `30_detailed_design.md`
3. semantic conflictがある場合: E8 addendumがENH-E8対象frontend scopeに限りbaselineをoverrideする
4. ENH-E8 scope外のbaseline Detailed Designは変更しない

Coding Agentのnormative contextはassigned 06/Pxxにself-containedで転記されるため、Agentがこのcomposite snapshotを探索して仕様補完することは禁止する。

本snapshotは `APPROVED` であり、snapshot incompletenessによるfreeze blockerは存在しない。
