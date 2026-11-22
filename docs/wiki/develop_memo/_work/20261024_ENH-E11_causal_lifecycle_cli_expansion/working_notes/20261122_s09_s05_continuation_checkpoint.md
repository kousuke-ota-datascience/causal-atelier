# ENH-E11 S09/S05 継続作業ログ — 2026-11-22

**文書区分:** WORKING NOTE（分析・実行メモ）。正本FR/NFR/AR・23/30の定義代替、独立Reviewerの判定、S10 Contract Freeze、S11 Coding Authorizationのいずれでもない。  
**Repository/branch:** `kousuke-ota-datascience/causal-atelier` / `prototype/ariadne_mvp`。  
**Previous checkpoint:** `combined_review/166_20261122_s09_second_pass_cross_wire_contract_reconciliation.md` at `00e63f11f2384ec493f24d61911ed1ef69526e91`.  

## A. 進め方（Ownerの2026-11-22指示）

Ownerによる新たな意味論的判断・承認が不可避な場合のみ依頼する。判断を要しない既承認範囲の文書・証拠整理・監査準備は継続。誤ったPASS、未承認の数理既定値、Linux/Backend/Independent reviewerの未実施を実施済みと記録しない。作業と判断の状態をGit source SHAで固定し、Notionへの重複転記は同期漏れを招くため本段階ではGit working_notesを検証ノートとして使用する。

## B. S05-B02 200 Method Profile のGitHub静的確認

5つのfactored `e11_<kind>_factored_v1.json`をGitHub connectorから取得し、GitHub Treeの200元Schema blob SHA、各kind全40 Methodの一意性、Output/Config/Inferenceの最低限のclosed object構造・required/property整合、200 Dispatch Registryの一意のMethod/Kindを照合。

- Source baseline blob SHA: **200/200一致**
- 5 kind ×40 Method: **200/200配置**
- Dispatch registry Method/Kind: **200件、重複／不足なし**
- Factored object basic closure/required fields: **今回の限定静的チェックで不一致0**
- Method Config: **全40件で少なくとも1 required field**
- Output Profile: `IDENTIFY` 5、`ESTIMATE` 23、`REFUTE` 4、`SENSITIVITY` 2、`DIAGNOSE` 3、`DISCOVER` 3。Output inventoryの基本Operation/Effect受理規則に違反0。
- P2-M01〜08 `cate_surface.json`、P3-M05 `event_time_effects.json`、P3-M12 `scm_gaps.json` のMethod Output記述整合。**P3-M06 ITSのみ新規出力不足を検出し追記**。

**証拠の上限:** 上記はJSON parse、source SHA、Method/Kind/required/mapの静的照合である。実際の`jsonschema.Draft202012Validator.check_schema`、各positive/negative instance、200元Schema対再構成Schemaの標準Validatorの等価性試験は本チャットから実行していない。従ってS05-B02をPASSへ変更しない。レビュー専用CLI `combined_review/tools/e11_profile_factor_compiler.py --report <path>` をユーザー承認済みの隔離Python3.12環境で、Git HEAD/lock/blobを固定して実行する必要がある。

## C. S09-R12 — P3-M06 ITS のMethod Output取りこぼし

Owner採用済み `working_notes/20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md` のITS数理は `β_L`（intervention level change）、`β_S`（post trend increment）およびpredeclared horizon `τ(t0+h)=β_L+β_S h`。一方P3-M06 Configは `effect_components=LEVEL|LEVEL_AND_SLOPE` を既に識別するが、Output Profileでは `positive_artifacts=[result.json]` のみ。多成分対象を1 scalarへ落とすことはMethod意味論の喪失／偽scalar生成のリスク。

### 既承認の科学的対象を変えない暫定技術契約

- `LEVEL`: `result.json.point.availability=AVAILABLE`, `point.value=β_L`; 同じRunの`its_components.json`ではlevelのみ、slope null、horizonなし。
- `LEVEL_AND_SLOPE`: `result.json.point.availability=NOT_AVAILABLE`, `point.value=null`, `point.reason.code=NON_SCALAR_TARGET`; sidecar `its_components.json`が `β_L`、`β_S`、指定済みhだけの `τ(t0+h)` を保有。
- 内部strict draft `23_api_interface_design/schema_drafts/internal_scientific/e11_its_components_draft1.schema.json`。`study_ref`/`design_ref`、intervention time、`horizon_predeclaration_ref`、非観測個票、finite値、Method bind、hash/manifest/readbackを検証。Horizon値の事後生成や事後選択禁止。
- Output/Profile元Schema、factored overlayの`P3-M06`とsource SHA、Method Output Descriptor catalogを更新し、G07 06/P00/P02/P03/07とStock 23_42に反映。独立07は両branchのpositive/negative（DGP-014、NEG-023）を要求。
- 新しい独立科学Target・Methodは追加していない。Public E11 ResultとProduct v2 Schemaは変更しない。Method-specific HAC、joint covariance、T3 coverage、fixed-horizon適格性は**未実施／未確定**。既存Owner採用のHACを適格性証拠なしでCI availableとはしない。

**差分後の限定照合:** P3-M06元Output Profile blob SHA `bb3a8500f5ad477032a3ef6fe8647b865037ef47` = factored source_blob_sha。元JSON Schemaとshared+overlay再構成JSON ASTは同一。Catalogの`positive_artifacts`と元Profileは双方 `[result.json,its_components.json]`。この正例は他199 Schemaの正式再検証ではない。

## D. 工程と未解決

- S09 independent review: 監査指示 `combined_review/165_20261122_s09_independent_document_audit_instruction.md` に新ITS分岐を加えた。レビュー担当の独立実行・署名は未実施。
- S05-B02: 実Python Draft202012 200 parity、T2/T3とは別。
- S05-B03: 実Artifact JSON bytes、Manifest/Reader hash/該当Method cross-validation未実施。新ITS draftはこの対象に追加。
- S05-B04: DoWhy/EconML/Tigramite実効Backend fitted API/CI未実施。
- S05-B05: 独立41 Method科学Oracle、AR候補の数学審査、必要なT2 resource/pilotは未完了。実装済みcandidateのT3はCoding Authorization後のGate999実測と区別。
- S10/S11は未Freeze・未承認。既承認S02/B、DEC-S05-AR01=A、S05-02/03=Aを保持。

## E. 次アクション

1. 新ITS schemaとOutput Profiling/G07の参照を含む全71 Gate doc + 7 Operator + 要件/設計/200 Profilesのsource SHA索引を更新。
2. 既承認範囲でMethod固有データモデルの残る不整合を静的照合。見つけた設計欠落は可能な限りOwner採用済み科学契約から直接再構成する。
3. 元事実から複数の実装科学Targetが等しく成立し、選択が意味論を変更する場合に限り、選択肢、証拠、影響Class/Method/Gateを明示してOwnerへ判断依頼。
4. 独立S09/S05実測は実際に実行していない限りPASS扱いせず、実行権限がないこと自体ではdocument-authoringを停止しない。

**NOTE:** 今回のITS追加は依然DRAFTであり、S10へ向けて独立監査・科学的適格性確認が必要。

## F. Owner A判断後の追記（2026-11-22）

`DEC-S09-P3M04-01=A`はOwner明示採用済み。P3-M04初期対象は`DID_2X2`の2×2 ATTのみ。`STAGGERED`は`DEFERRED`（NOT RETIRED）であり、構文上認識できても科学的preflightで`SCIENCE_CONTRACT_NOT_AVAILABLE`/`CAPABILITY_UNAVAILABLE`（exit4）として拒否。Unknown Configは構造検証exit2と区別する。M04 STAGGEREDをDID_2X2/TWFE/P3-M05へ無言fallbackしない。元Method Config/Output 2 Schema＋factored 2 overlay、200-profile Dispatch、Output Catalog、G07 6文書、G10 8文書、Stock 10_32/23_42/30_63、独立監査165へ反映。詳細は`combined_review/167_20261122_dec_s09_p3m04_owner_a_propagation_audit.md`。

静的再照合: 200元Schema blob SHA一致、40×5 ID/dispatch一意、両変更Schemaのoverlay AST一致、Output CatalogのDID_2X2 positive/STAGGERED deferred一致。実Python Draft202012 200 Validator・独立S09・Backend/Scienceは未実行。監査用新Source SHA index `combined_review/s09_post_reconciliation_document_snapshot_draft5.json` を使用し、以前のdraft1–4はhistoricalとして扱う。S10/S11は未承認。

## G. S09 参照整合性・G08 AR予備検査の追加結果（2026-11-22）

- S09相対リンク・権威参照のSource QA: 71 Gate 06/Pxx/07のinline相対Markdown link 198、Operator 7件（該当相対リンク0）、主要要件/設計33ファイルの50を検査。G10/P04に4件のリンク切れを検出して修正、同G10/P04を再走査して欠損0を確認。根拠・検査対象・未検査範囲は`combined_review/168_20261122_s09_reference_integrity_and_g08_ar_candidate_author_review.md`に記録。独立S09 PASSではない。
- G08/P03の§4本文とMandatory Matrixに残った、未Freeze HC1/χ²(1) AR算法を「実装する」とする命令形を修正。他G08のOwner-OD05/Allocation/07行も候補の未承認状態を明示。全実数の弱IV頑健AR集合とB0/B1科学Targetは維持。独立Reviewer・Ownerの実装算法Freezeは依然BLOCKED。
- Author側数学予備検査: `working_notes/20261122_s05_ar_hc1_candidate_author_mathematical_preflight.md`。B1相当の合成データでHC1/χ²逆転を二次不等式に変形し、BOUNDED/DISCONNECTED/ALL_REALの3種類を固定seedで再現。15点で別OLS+HC1実装と数値一致。Python3.13.5を使用、承認済みPython3.12と独立Oracle/弱IV coverageは未実施。
- 現行監査索引: `combined_review/s09_post_reconciliation_document_snapshot_draft6.json`。Reviewer指示`165`も最新索引とAR方針に更新。

**独立監査・200 Method Draft202012・Backend/数値Science・S10/S11の未実施は不変。新たなOwner判断事項なし。**
