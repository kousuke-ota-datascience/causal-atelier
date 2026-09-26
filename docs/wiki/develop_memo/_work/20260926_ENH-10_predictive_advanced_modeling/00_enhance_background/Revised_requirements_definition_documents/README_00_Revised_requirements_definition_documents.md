# Revised Requirements / Design Snapshot — 作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでsnapshotの目的・対象・作成規則が分かること。

## 1. Purpose

Enhancement開始時点で改定・承認された要件・設計のeffective snapshotを保存する。後続で要件・設計が変わっても「このenhancementが何を前提に計画されたか」を再構成できるようにする。

## 2. Standard files

- `00_product_concept_memo.md`
- `10_requirements_definition.md`
- `21_logical_data_design.md`
- `22_product_basic_design.md`
- `23_api_interface_design.md`
- `30_detailed_design.md`

対象外は`N/A`と明示するか、不要templateを削除してよい。

## 3. Authoring rules

- snapshot作成時点のapproved effective contentを本文内に保存する。
- source document pathはprovenanceとして併記してよい。
- 「原本を参照」の一文だけでsnapshotを代替してはならない。
- snapshotはCoding / Test Agentへの直接execution contractではない。
- Agentへ直接必要なimplementation / acceptance semanticsはGate-local primary contractへ記載する。
- snapshotとactive primary contractに意味上の矛盾を発見した場合、勝手に補完せずHuman / contract ownerへescalateする。
