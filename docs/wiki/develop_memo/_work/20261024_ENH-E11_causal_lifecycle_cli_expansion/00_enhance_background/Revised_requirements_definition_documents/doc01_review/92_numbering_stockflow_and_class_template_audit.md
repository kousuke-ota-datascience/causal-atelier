# DOC-01 follow-up — 90番台配置／23・30文書構造の監査

**監査日:** 2026-11-17 JST  
**対象Branch:** `prototype/ariadne_mvp`  
**基準Git Commit:** `a24e7d528c39f3869a43443ddbaaa588986e2741`  
**種類:** Flow / Audit（正本候補10・21・22・23・30群へ昇格しない）  
**判定:** `DOC01_OWNER_APPROVAL_RETAINED / DOCUMENT_STRUCTURE_AND_TEMPLATE_NONCONFORMITY_FOUND / REMEDIATION_OPEN`

## 1. 原文書と現行版の章対応

GitHub上の退避Source Snapshotを照合した。

| Original | 元の章構造 | Current splitの実所在 | Structural finding |
|---|---|---|---|
| 23 API | §1/2 | `23_00_overall_IF` | 概ね対応 |
| 23 API | §3 | `23_01_common_conventions` | 概ね対応 |
| 23 API | **§4 Browser Navigation** | `23_20_browser_navigation` | **§5 Web APIのファイル番号より後に位置する** |
| 23 API | §5 Web API | `23_10`〜`23_19` | 11〜19の一部は`###5.x`から開始し、ファイル内で親`##5`がない |
| 23 API | §6 Worker | `23_30_worker_runtime` | §6 |
| 23 API | §7 CLI | `23_40_cli_library` | §7、追加Local契約とは別の局所§1〜9を併存 |
| 23 API | §8 Cross-cutting | `23_50`〜`23_52` | 51/52の冒頭に親`##8`がない |
| 23 API | §9 Verification | `23_90_interface_verification` | 恒常的Contract Testの受入条件はStock要素 |
| 23 API | §20 CHANGEPOINT | `23_99_change_log` | Enhancement履歴はFlowに該当 |
| 30 DD | §3 Domain Values | `30_10_domain_resources` | §3 |
| 30 DD | **§4 Navigation / §5 Context** | `30_41_navigation_routing` | **§3より後のファイルにあり、§18 Routingと同居** |
| 30 DD | §6以降 | `30_11`〜`30_90` | 概念責務とClass実装詳細が混在 |
| 30 DD | §30 Change log | `30_99_change_log` | Enhancement変更経緯はFlowに該当 |

**結論:** `## 4.`の内容は双方とも欠落していない。ただし「ファイル番号順に読める」「各分割ファイルは独立して親見出しを持つ」という2点に不整合がある。元の章番号の温存と新しいファイル責務分類が競合している。

## 2. ルート90〜98：意味と適正配置

`Revised_requirements_definition_documents/`は、将来正本化する**Stock候補5群**と改訂工程の**Flow**を暫定的に同じRootに置いた作業場である。Rootの90系を正本階層の一部とみなしてはならない。

| 現在のRoot文書 | 主な内容／真正な役割 | 推奨配置 | 分類 |
|---|---|---|---|
| `90_structural_split_verification.md` | 分割実施時点の監査Snapshot | `doc01_review/historical/` | Flow / historical |
| `92_rd02_restructure_verification.md` | RD-02の57移管と番号・保全証拠 | `rd02_review/` | Flow / audit |
| `93_enh_e11_canonical_promotion_policy.md` | Ownerによる正本昇格のDecision | `owner_decisions/`（ENH単位） | Flow / decision（効力は維持） |
| `95_rd04_fr_application_review.md` | 旧FRの逐条修正監査 | `rd04_review/` | Flow / trace |
| `96_rd03_formal_requirement_traceability.md` | 68 Scope／41 Method／10 UCから正式条文への発行Trace | `rd03_review/` | Flow / issuance trace |
| `96_rd04_nfr_ar_application_review.md` | 旧NFR/ARの逐条適用監査 | `rd04_review/` | Flow / trace |
| `97_rd04_e11_requirement_review.md` | 新44条文の科学・機能レビュー | `rd04_review/` | Flow / review |
| `98_rd04_consistency_verification.md` | RD-04の整合・未完検証記録 | `rd04_review/` | Flow / verification |

8件とも実装仕様の正本本文ではない。特に`93`は**Owner決定という権威ある記録だが、Stock要件の章ではない**。決定記録はFlow保存、現在有効な「全テストPASSまで元正本を変更しない」という拘束規範はStock文書の昇格条件にも反映する。

移動時はRoot索引、各RD/BD/Review、Notion/Handoff等の**既存リンクとrelative pathを全面再配線**してから旧Pathを除去する。リンクを壊してまで物理移動したと見せかけない。後続Commitで移管・リンク全件確認を一体実施すること。

## 3. 23系：Stock/Flow混在

| Path | 修正すべき性質 | 判定 |
|---|---|---|
| `23_41_e11_local_cli_scientific_ports.md` | CLI/Port/Version/Resultの恒常契約はStock。ただし`IF-01`という工程名、Owner候補版の採否経緯、実装前の状態表記はFlow | **MIXED** |
| `23_42_e11_local_result_manifest_artifact.md` | JSON/Graph/AR/Manifest/Atomic/Privacyの契約はStock。ただしD03採用経緯、IF固有試験と候補状態はFlow | **MIXED** |
| `23_90_interface_verification.md` | Interface全般の不変条件・Contract Testの「満たすべき条件」はStock（結果／実測証拠は別） | **STOCK** |
| `23_99_change_log.md` | ENH-E2〜E10ごとの差分・変更経緯。現在有効なAPI定義の権威ではない | **FLOW：分離推奨** |
| `23_10`〜`23_19` | 多くが`Method/Path/用途`の代表API一覧で、Input/Output/Auth/Validation/Failure/Idempotency/VersionがEndpoint単位で正規化されていない | **STOCKだが粒度欠落** |
| `23_01_common_conventions.md` | 現行実装の認証現状（X-User-Id/anonymous）と将来の「全Project route RBAC義務」が同ファイル内にある | **CURRENT／REQUIREDの区別を維持** |

名称にE11が含まれるだけではFlowと判定できない。将来も有効なVersioned Interface契約ならStockに残る。ただしEnhancement承認経緯、Review status、実行済みと誤認するテスト表はFlowへ分離する。

## 4. 30系：Classテンプレートの適合性

[Class template](../30_detailed_design/30_01_class_design_template.md)の必須7区分が、下記主要なClassの現行記述に完全には実装されていない。

| Class／Class group | 現状の主要配置 | 未充足の例 |
|---|---|---|
| GraphVersion | `30_10_domain_resources.md` | constructor／field詳細、Method別副作用・例外、7区分 |
| PlanValidator / StageRunnerRegistry | `30_20_planning_validation.md` | Constructor/Factory、field mutability、methods side effects/error、test evidence |
| GenericExecutor / ExecutionOutcome | `30_21_execution_runtime.md` | 2 Classを分離した7区分・retry/exception |
| StoredArtifact / ArtifactStorePort | `30_50_persistence_artifacts.md` | Protocol方法別例外・I/O、N/A理由 |
| CliManifest | `30_60_cli_adapters.md` | default factory/ネスト可変性、Method/Serialization、7区分 |
| Local Domain/Port候補 | `30_61_e11_local_domain_ports.md` | 複数Classを1節で混在、7区分でのField/Constructor/Method非整合 |
| Local UseCase/Publisher候補 | `30_62_e11_local_execution_publication.md` | Field table、Constructor、exceptionの明文化不足 |
| Method Adapter候補 | `30_63_e11_method_adapters.md` | 41 Method ID表はClass定義ではない。具体Adapter Classごとの7区分が未定義 |

また`30_30`〜`30_37`、`30_40`〜`30_43`にはStage/Navigationのプレゼンテーション上の責務説明が多く、**Class/Protocol/Moduleの物理仕様を記載したことにはならない**。これらはBasic DesignのUI/Navigation設計への移管候補、あるいは実コードへ対応付けた詳細処理仕様への再執筆対象である。

**結論:** 30系のテンプレート適合はFAIL。対象がClass/Protocolなら7区分すべて必須、Module-level関数はSignature／副作用／例外／検証必須。設定値・型がSource/承認済みADRに無い場合は`UNSPECIFIED / FREEZE_PENDING`と記し、架空のSignatureを作らない。

## 5. 是正条件

1. 90番台Flowを配置替えし全Backlink・相対リンクを検証する。
2. 23系で「Global chapter」と「File-local detail」を明示、見出し親を各ファイルに補い、API interfaceを統一のContract schemaで監査する。
3. 23_41/42の恒常契約とIF-01経緯を分離する。23_99はFlow。
4. 30系の物理Classを実際のSource/ADRと突合し、**1 Class / 7 Subsections**で書き直す。概念／UI説明をClass定義と混同しない。
5. 機械的にMarkdown heading hierarchy、File links、Class template coverage、旧v2/METHOD41 trace、元正本不変を検査する。

**Approval boundary:** DOC-01のOwner承認／IF-01・DD-01の設計案採用を遡及取消しはしない。本書は承認後の**文書構造と記載粒度の欠陥**を証拠に基づいて指摘し、設計意味・Schema/Port Freeze、独立Architecture／Gate06/07は別の責務とする。
