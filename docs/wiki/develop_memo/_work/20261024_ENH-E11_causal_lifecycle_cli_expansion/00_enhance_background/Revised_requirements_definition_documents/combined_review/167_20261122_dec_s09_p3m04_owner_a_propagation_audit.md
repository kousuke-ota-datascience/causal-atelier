# ENH-E11 / S09 — DEC-S09-P3M04-01 Owner A伝播・静的整合性監査（2026-11-22）

**判断:** Owner明示回答「A案を採用する」(2026-11-22)。判断記録: `working_notes/20261122_dec_s09_p3_m04_staggered_scope_and_output.md`。  
**Author-side state:** `OWNER_A_ADOPTED / INSTRUCTION_AND_STOCK_RECONCILED / STATIC_SHA_CHECK_DONE / S09_INDEPENDENT_REVIEW_NOT_RUN / S05_RUNTIME_NOT_VERIFIED / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`。  
**Revision scope:** enhancement-local stock Requirement/IF/DD, draft Method Profiles, 06/Pxx/07 and 40-independent audit preparation only. No source code, product API/UI/DB, test code, `pyproject.toml`, `uv.lock`, or official canonical RD was changed.

## 1. Owner選択と理由

**P3-M04の初期提供はDID_2X2 ATTのみ。** `STAGGERED`は `DEFERRED` であり `RETIRED`ではない。科学的 `ATT(g,t)` と事前固定集計weightおよびstaggered専用Inference/Referenceの契約が未確定のため、現在の`result.json` scalarへstaggered異質効果を押し込まない。P3-M05 Event Studyは別Methodであり代替ルーティングには使わない。41 Method/10 UCおよび既承認のDEC-S02/DEC-S05を維持。

**文法と科学的実行能力の二層判定（Owner Aを損なわず、将来DEFERREDを認識する設計）：**
- `e11_p3_m04_method_config_v1.schema.json` は `design_variant=[DID_2X2,STAGGERED]` を厳密に解析できる（未知値や必須欠落はconfig exit2）。これにより将来variantであることを識別し、誤って未知Methodへfallbackしない。
- Variant-specific scientific preflight: `DID_2X2`はMethod/Design/Backend/Science適格時に限るpositive。 `STAGGERED` は構文上適格でも必ず `SCIENCE_CONTRACT_NOT_AVAILABLE` reason、`CAPABILITY_UNAVAILABLE` status、CLI exit4。Estimator/Backendと科学row-source呼出し前に停止し、成功Effect Result/Manifest/Markerを発行しない。
- `e11_p3_m04_output_profile_v1.schema.json` の `positive_artifacts=["result.json"]` は初期DID_2X2専用。Catalogに明示的`positive_design_variant`と`deferred_design_variants`を記録。
- 禁止: `STAGGERED → DID_2X2`サイレントfallback、TWFE scalar化、P3-M05 Event Studyへの暗黙転用、DEFERREDをScience PASSまたは`RETIRED`と主張すること。

## 2. 正本候補・指示書の伝播

| Layer | 対象・責務 | 状態 |
| --- | --- | --- |
| Decision | `working_notes/20261122_dec_s09_p3_m04_staggered_scope_and_output.md` | OPEN→Owner A採用へ更新、§5 implementation meaning追加 |
| Requirement | `10_requirements_definition/10_32_scientific_method_scope.md` | P3-M04初期2×2、STAGGERED future、DGP-013区別 |
| IF | `23_api_interface_design/23_42_local_result_manifest_artifact.md` | scalar positiveはDID_2X2限定、deferred error/fallback禁止 |
| Class/DD | `30_detailed_design/30_63_causal_method_adapters.md` | `PanelQuasiAdapter`初期positive、STAGGERED preflight拒否を本文に反映 |
| Strict Method Profile | `e11_p3_m04_method_config_v1.schema.json` / `e11_p3_m04_output_profile_v1.schema.json` | Config syntax/capability分離、Output positive限定 |
| Factoring | `factored/e11_method_config_factored_v1.json` / `factored/e11_output_profile_factored_v1.json` | 変更後元Source SHAとOverlay反映、両Profileの再構成AST一致 |
| Dispatch/Output | `e11_method_profile_dispatch_registry_draft1.json` / `e11_method_output_descriptor_catalog_v1.json` | Owner-A per-variant capability/exit4/positive modeを追跡、runtime未登録 |
| G07 | Gate `06`、P00/P01/P02/P03、`07` の6文書 | 2×2正例、STAGGERED exit4拒否負例、DGP-012/REF-Q01初期、DGP-013の将来・P3-M05区別 |
| G10 | Gate `06`、P00–P05、`07` の8文書 | 41 Method横断証拠からSTAGGERED fake positiveを排除、Method Registry/Manifest/Science/G05/旧v2保護 |
| S09 Reviewer | `combined_review/165_20261122_s09_independent_document_audit_instruction.md` | "Owner判断OPEN"誤状態を削除、Owner Aの正負例を独立レビュー対象として追加 |

## 3. 静的証拠の到達範囲

GitHub Branch Treeと5 Factored JSON、Dispatch registry、Output Catalogの読出しにより、変更後に次を確認。

- Source Draft blobs `200/200` はFactored `source_blob_sha`に一致。5 kind各40 Method、40 ID coverage一致、Dispatch `200/200` Method×Kind一意、構成したclosed object/required基本整合で指摘0。
- P3-M04 `method_config` / `output_profile` の変更後Source JSON AST は各々 shared+overlay再構成JSON ASTと等価。新元blob SHAは `fd8bc7120b586fe08c8708dab58ba457bf7a69a0` (Config)、`5685a71881af5a56519121f3917aa654d00f9870` (Output)。
- Output Descriptor CatalogはP3-M04のpositive `DID_2X2`、deferred `STAGGERED`、`CAPABILITY_UNAVAILABLE`、exit4、`result.json`と整合。
- 全件読出し型の独立Semantic Review、Python `jsonschema.Draft202012Validator` 200 Method positive/negative/MetaSchemaチェック、Backend fitted API/CI、Artifact/Reader、独立Science Oracleは今回実施していない。SHA一致/AST一致のAuthor証拠は独立S09 PASSではない。

## 4. 独立監査用の厳密な対象

`combined_review/s09_post_reconciliation_document_snapshot_draft5.json` は判断反映後のGit blob source index（71 Gate 06/Pxx/07、7 Operator、200 original Method Profiles、5 factoring bundles、13 Local/internal Schemas、34 selected stock docs）。固定Source Revisionは同indexの `source_full_commit_sha` を参照する。Index作成・監査指示の後続コミットによりHEAD全体はさらに進むため、独立Reviewerは実効レビュー対象HEADを事前に再Pinし、対象全ファイルblobを検査すること。

**S09独立監査のOwner判断Blocker DEC-S09-P3M04-01は解消。** ただし、S09 Reviewer未実行、S05-B02/B03/B04/B05およびG08 AR Algorithm／G06 temporal／G07 ITS covariance／G09 SDID inferenceは独立証拠なしでPASS不可。

## 5. 次の自律進行と厳密な停止境界

1. S09独立監査を最新HEAD固定で実行可能な独立実体へ渡す準備は済み。ただしこのAuthorは独立Reviewerを偽装せず、実行権限のないAgentのPASSを報告しない。
2. S05 200 Schema実Validatorと実Backend/Reader/数値Referenceはユーザーが承認済みの隔離Python3.12/ユーザー実環境で実行証拠を得る。チャットからその環境の実行権限はないため、無条件にSource/Tests/Lockへ変更しない。
3. Science Target・Inferenceアルゴリズム等で既承認解釈だけでは一意に決まらない重要事項が新たに見つかったときのみOwner判断へ昇格。その他の資料整合性と監査準備は中断しない。
4. S10 Contract Freezeには独立文書・科学契約・Backend/適格性の必要な受入証拠を揃え、S11 Coding Authorizationはその後の独立Owner決定。候補コードのT2/T3 Gate999実測を実装前に仮PASS扱いしない。

**Do-not-claim:** `41_METHOD_RUNTIME_PASS`、`S09_INDEPENDENT_PASS`、`B02_DRAFT202012_PASS`、`G08_AR_ALGORITHM_FROZEN`、`S10_FROZEN`、`S11_CODING_AUTHORIZED`。
