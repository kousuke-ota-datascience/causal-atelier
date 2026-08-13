# Revised Requirements / Design Documents

このディレクトリは、Enhancement適用後に有効となるrequirements/designのeffective snapshotを保存する。

## 1. 文書言語

日本語話者が各文書を単独で読み、背景、要件、設計、制約を理解できることを基準とする。

API名、class/type/schema、`Family`, `Stage`, `Gate`, `Work Package`等、英語を維持した方が実装との対応が明確な専門語は英語を許容する。

## 2. 自己完結性

- 完成文書に「ENH-E4の文書を参照のこと」のような外部workflow文書依存を残さない。
- ENH-E4から継承する有効内容は本文へ統合する。
- 本文は現在有効なproduct requirement/designを記述する。
- Enhancement番号を主語にした変更説明は、必要な場合にCHANGE LOGまたは専用の変更範囲sectionへ分離する。

## 3. 見出し階層

見出しは情報アーキテクチャとして扱う。

- 同一heading levelに異なる抽象度の概念を混在させない。
- major product concernと個別UI behaviorを同じlevelへ置かない。
- 抽象 -> 具体、Why -> What -> Howの順に降りる。
- 現在のproduct構造、今回のchange、future extension、implementation detailを同一levelへ混在させない。

## 4. 文書責務

| 文書 | 主責務 |
| --- | --- |
| `00_product_concept_memo.md` | WHY / product vision / analytical model / future direction |
| `10_requirements_definition.md` | WHAT / effective requirements / E2E / FR-NFR-analytical requirements |
| `21_logical_data_design.md` | logical resource/value/state model |
| `22_product_basic_design.md` | layer/function responsibilityと主要behavior |
| `23_api_interface_design.md` | external/internal interface contract |
| `30_detailed_design.md` | module/class/data-flow/test seamへの具体化 |

## 5. Change Log

過去Enhancementを知らなくても本文を理解できることを優先し、履歴説明は各文書末尾のCHANGE LOGへ分離する。

## 6. Execution Agent boundary

本ディレクトリはPlanning / Human Review / future auditのための背景層である。

Coding Agent / Test Agentが通常実行時に本ディレクトリを読み、仕様を再探索してはならない。実装・検証に必要な決定はfreeze前に対象06/07またはassigned Pxxへ収束させる。
