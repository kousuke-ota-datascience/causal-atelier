# BD-01 — エンハンス固有の設計判断・レビュー・履歴

**分類:** `FLOW / REVIEW / TRACE`。本ディレクトリは将来の正本`22_product_basic_design/`へ昇格させるストック文書ではない。

## 1. 分離方針

- 恒常的に有効な**機能と責務別のArchitecture契約**のみを既存の`22_00〜22_17`基本設計に統合する。
- E11固有の判断履歴・当時のドラフト・自己整合レビュー・44条文割当表は、ENH-E11作業領域内の本`bd01_review/`に保管する。
- 元基本設計から`22_20〜22_23`、`22_90〜22_91`の6ファイルを撤去する。原文はGitHub上で履歴保持し、元の個別設計草案4件は`source_snapshots/`に原Blob SHAで完全保存する。
- 元正本`docs/wiki/requirement_definition/`を現時点で変更しない。全対象テストPASS後に昇格する方針は不変。

## 2. Legacy file disposition

| Former (removed from stock) | Category | Permanent design destination / record |
|---|---|---|
| `22_20_e11_local_system_architecture.md` | E11-specific design draft | `22_00_overall_BD.md`、`22_04_workflow_core.md`、`22_15_schema_dependency.md` |
| `22_21_e11_scientific_pipeline.md` | E11-specific design draft | `22_04_workflow_core.md`、`22_06_family_causal.md`、`22_08_validation_architecture.md` |
| `22_22_e11_local_result_artifact_lineage.md` | E11-specific design draft | `22_09_results_artifacts_lineage.md` |
| `22_23_e11_environment_security_compatibility.md` | E11-specific design draft | `22_12_security.md`、`22_13_deployment.md`、`22_15_schema_dependency.md`、`22_16_test_architecture.md` |
| `22_90_architecture_consistency_review.md` | BD-01 review | [Architecture review](90_architecture_consistency_review.md) |
| `22_91_bd01_requirement_architecture_trace.md` | BD-01 Trace | [Requirement/Architecture Trace](91_requirement_architecture_trace.md) |

## 3. Source content preservation

- [22_20_e11_local_system_architecture.md](source_snapshots/22_20_e11_local_system_architecture.md) — blob SHA `81808382d8145738af7f54bc03adfb8bbb7dead1`（無改変履歴）
- [22_21_e11_scientific_pipeline.md](source_snapshots/22_21_e11_scientific_pipeline.md) — blob SHA `483a72f79fe1b9f0c5e0e5302846f18158ed34a3`（無改変履歴）
- [22_22_e11_local_result_artifact_lineage.md](source_snapshots/22_22_e11_local_result_artifact_lineage.md) — blob SHA `f79cfad36d19b52f56bbf4634f3bcc72343be2d1`（無改変履歴）
- [22_23_e11_environment_security_compatibility.md](source_snapshots/22_23_e11_environment_security_compatibility.md) — blob SHA `fd7c1a19664fe958253e3d7fa483957fcec1eaf8`（無改変履歴）

## 4. 状態と受入境界

- [Architecture自律レビュー](90_architecture_consistency_review.md)は13論点（当時2 design-side resolved、11 open）の記録であり、独立審査ではない。
- [Formal requirement allocation](91_requirement_architecture_trace.md)はFR/NFR/Scientific AR 44件の設計担当・Traceを記録するが、科学的受入を意味しない。
- IF-01／DD-01、Architecture独立審査、Science、Legal、Gate06/07は別の閉鎖事項。

## 5. 正本化に向けた残務（この6ファイルの移設とは別）

- 22系の既存`## 98. RD-04`逐条移管記録は、まだ各基本設計に残っている。これは設計の要求起源を保全する中間記録であり、将来の元正本へ昇格する前に、必要な設計拘束を各Stock章へ確定反映したうえでレビュー台帳側へ分離する。
- `22_17_stage_contents_e8_effective.md`等のエンハンス識別を含む既存文書も、内容が持続的機能設計か経過記録かを別途監査する。今回の6ファイル移設だけで22系すべてのStock適合を保証したとは判断しない。
- 再編の構造・内容移管テストと、独立Architecture/科学/実装テストのPASSは区別する。
