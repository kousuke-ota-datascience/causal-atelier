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

## H. S09監査対象の全Stock索引化（2026-11-22／次スレッド継続）

- 新規 `combined_review/s09_post_reconciliation_document_snapshot_draft7.json` を作成。`source_full_commit_sha=0d5b5971d0e5b5127a68e010cfdc83dbd6020545`。S09の監査対象に、既存の71 Gate / 7 Operator / 200 original Method Profile / 5 factored bundle / 13 public/internal Schema / 34 selected stockに加え、**全98件のactive stock Markdown**（RD=22、BD=18、IF=31〔Schema READMEを含む〕、DD=27）と**8件の追加cross-contract assets**（FCI draft 4件、Method dispatch/output catalog 2件、科学Acceptance registry/metric matrix 2件）のfull Git blob SHAを列挙。歴史的な`doc01_review/prior_drafts`の5ファイルは現行Stock索引から除外。
- GitHub Treeのcurrent HEADで旧`draft6`の71+7+200+5+13+34各項目blob SHAが全件一致することを確認。`097f33f...`→`0d5b597...`の3 commitでは、独立レビュー指示書・証拠索引・本working noteのみ変更され、Normative契約・Profilesは不変。新規98+8のblob SHAは同じGit Tree由来。
- `combined_review/165_20261122_s09_independent_document_audit_instruction.md`の主索引を`draft7`へ更新し、独立Reviewerに98 active Stockと8件の追加資料、歴史的draft除外、最終Review SHA再照合を明記。`draft1`〜`draft6`は履歴資料。
- **検証限界:** 本作業はAuthorによるGit Tree/SHAとreviewer discoverabilityの静的整備であり、各98文書の意味論的整合性PASS、S09 independent verdict、S05 B02/B03/B04/B05、AR科学承認、S10/S11を意味しない。Ownerの新たな決定事項はない。次は実際の独立S09全件監査とS05の残証拠を閉じること。

## I. S09第三巡Author修正（2026-11-22、次スレッド続行）

- G01〜G10現行Gate指示書71件とOperator起動Prompt 7件を、主要Owner判断とAR、Graph、G05個票、CATE/ITS/SCM、G10証拠再利用の限定語句・重要本文について追加巡回。**Authorのtargeted semantic scan**であり、全行の独立意味論審査ではない。
- **S09-R13:** G08/P01〜P04の主文にHC1/χ²(1)を採用済み算法と読める3箇所ずつ（合計12）の表現が残存。Owner DEC-S05-AR01=Aの科学Targetを保持し、HC1は未Freeze候補、実算法未承認なら`BLOCKED_SCIENCE_METHOD_NOT_FROZEN`、full-real robust AR必須と明記。後段の免責追記だけで主要命令を無効にする旧構造を是正。
- **S09-R14:** G01/P03 §10 DoDの`Standalone`限定と`optional real Product parent lineage retained`が、全E11 Local Graph `version_id=parent_version_id=null`契約を曖昧化。全Local wireはnull、科学的親はimmutable provenance/ContentRef/hash、実Product版親は別既存Bridgeだけと明記。
- 修正根拠・未検証は`combined_review/169_20261122_s09_third_pass_author_contract_remediation.md`。旧draft7の5 blob SHA差分を新`combined_review/s09_post_reconciliation_document_snapshot_draft8.json`へ再固定。source snapshot=`2e529a38f1bc19afba9bec693a9a828bb7e1f9de`。71 Gate + 7 Operator + 200 original Method + 5 factored + 13 public/internal Schema + 98 active Stock Markdown + 8追加asset（402 uniqueのsource index、既選定34は98の内数）。`165`独立監査指示書をdraft8参照・R13/R14チェックへ更新。
- **未達成:** 真の独立S09 verdict、Python3.12 B02、実Artifact/Reader B03、実Backend B04、独立41 Method/HC1数理審査/各scientific acceptance B05、S10 Freeze、S11 Authorization。**追加Owner判断なし。** S10はOwnerが別途統合審査・明示承認した場合のみ。

## J. S05-B02 200 Profile限定実行（2026-11-22／最新継続）

- 本チャットで実際にGitHub連携から5 factored Profile bundle（各40 Method）を取得し、JS/V8の**限定Schema構造評価器**により、正例200、必須Field欠落拒否200、未知Field拒否200、不正型/値拒否200、不正Method ID拒否40、Inference条件不整合拒否22、**合計862検証、期待値不一致0**。最初の6件の正例生成器の64桁hexフィクスチャ欠陥は修正し、全200件を再実行済み。
- Dispatch Registry 200組の一意性、各factoredのsource_file/元Schema blob SHA 200/200、Output Catalogのconst項目40/40、P3-M04 STAGGERED DEFERRED及びP3-M06 ITS sidecar記述を検査し不一致なし。
- Evidence: `combined_review/170_20261122_s05_b02_factored_profiles_author_bounded_instance_smoke.md`。**使用したのは標準Draft202012Validatorではなく独自のsubschema evaluator**。完全なJSON Schema metaschema/parser/ref/実行等価性の検証、元Schema200件のPython実Validator正負例及びPython3.12実行は未実施。正式S05-B02は**BLOCKED**のまま。
- 現コンテナはPython3.13.5、jsonschema4.26.0が使用可能だが、指定Python3.12はなく、GitHubへの直接git通信はDNS解決不能。Notion Custom Agentはentitlement_requiredで開始不可。承認済みLinux VM/Codex CLIへの接続手段が本チャットにない。これは実証実行のBlockerであり、独立S09・B03/04/05・S10/S11をPASSに変更しない。
- 既存の実行手順は`combined_review/159_20261122_s05_linux_isolated_execution_runbook.md`、Python標準Validator実行コードは`combined_review/tools/e11_profile_factor_compiler.py`。今後、承認済み隔離Python3.12と独立Reviewerで固定Source SHA+Lock+実Report/hashを収集する。新たなOwner科学選択はない。

- B04追加観測（このチャットの非承認Python3.13.5 runtimeのみ）: `dowhy` / `econml` / `tigramite` / `causal-learn` distributions/modulesは未導入。`statsmodels 0.14.6`, `numpy 2.3.5`, `scipy 1.17.0`, `jsonschema 4.26.0`は導入済み。これをOwner承認済みPython3.12のENV-BASE/DOWHY/ECONML/TIGRAMITE fitted API検査に読み替えない。B04はBLOCKED。

## K. S05-B03 Schema/Reader交差契約のAuthor修正（2026-11-22／最新継続）

- **B03-R01:** `e11_local_manifest_v1.schema.json` の `execution.technical_status` が任意の非空stringだった不一致を修正、`status.json`と同一の5値Enumに制限。別File間の値一致は実Readerの義務であり、Schema修正だけで実COMPLETEDを証明しない。
- **B03-R02:** 6個の内部科学Schema（CATE/Event/Identification/ITS/Diagnostics/SCM）に合計21ある`ContentRef.relative_key`へ公開Schemaと同一の相対path guardを追加。固定正例3、負例6の限定JS正規表現検査を実行。これだけで安全な実FD/permission/symlink/readbackを保証しない。
- **B03-R03:** G01/P02 06、G01 07、G10/P03 06、G10 07の4指示書にSchema差異、実Bundle cross-wire一致、入力拒否負例・privacy/run hash/checksumを本文反映。
- **B03-R04:** Stock正本候補`23_42_local_result_manifest_artifact.md`と`30_62_local_execution_publication.md`の規範設計にManifest/Status閉Enum一致・内部ContentRef safe lexical/実Reader FD/SHA権限検証を反映。エンハンス固有の事情を本文へ転記せず、永続設計として記載。
- 現行Public Schema 6について、Operation/Mode/Status 7、run_id 4、Schema dispatch 3、Request Hash 1、ContentRef path 2、Local Graph null 2の合計**19/19 static pair一致**。13 public/internal Schema IDに重複なし。これは**Author source-level限定検査**であり、標準jsonschema/実Bundle reader/独立証拠ではない。
- Case/evidence一覧: `combined_review/171_20261122_s05_b03_cross_schema_author_remediation_and_test_matrix.md`。S09監査索引: `combined_review/s09_post_reconciliation_document_snapshot_draft10.json`、normative Source=`a3268a1cf104e28e4508744b87db3c49237bda27`。402 unique blobsの索引でありS09独立PASSではない。165の独立監査指示はdraft10/R15-R16を参照する。
- **Phaseの区別:** S10は実装前契約のReview/Freeze、完成したE11 Publisher/Readerの実FS readback受入はS11後G01/G10 07/999。まだ実装していないE11実行コードの成功結果をS10前提に置くと循環。S05-B03実readbackは現時点でNOT_RUNのまま。B02 Python3.12、B04 backend、B05独立科学、S09独立Reviewも未実施。S10 NOT_FROZEN、S11 NOT_AUTHORIZED、新規Owner科学判断なし。

## L. PREP-04→S10 / Coding Entryの実行証拠境界（2026-11-22）

- 元のControl PlaneはPREP-01/02/03で要件・共通設計・06/07/DAGを作成/Owner静的承認し、PREP-04でMethod/Backend/Science/実装前契約を具体化、PREP-05独立監査、PREP-06 Contract Freeze、Owner Coding Authorization→Trial/Independent Test/Gate999の順。
- 簡素化S01–S04およびS06–S08はAuthor改訂済みだが、S05の独立Science/実効Backend、S09独立監査、S10/11は未了。過去PREP-03採択の06/07は現行S02追加B×8改訂前の監査記録であり現行Freezeではない。
- 41件の独立Science Registryを再読: G01=1/G02=6/G03=13/G04=8/G06=3/G07=3/G08=5/G09=2の41 unique。独立Reference実体/SHA、Fixture SHA、K/R/epsilon/許容差/seed/定量判定がすべてnullまたは未実行、`oracle_algorithm_status=DESIGN_PROPOSAL_NOT_IMPLEMENTED`が41/41。T3/Gate999の数値PASSはCoding前に要求できないが、Science Target/算法/独立Oracle/試験プロトコルの実装前承認は必要。
- 本文書の核心成果: `combined_review/172_20261122_prep04_s10_precode_evidence_phase_assignment.md`にB02/B03/B04/B05のpre-code設計契約とpost-S11実候補の証拠を分離。既存`combined_review/159`実行RunbookのE節で`B03 real Reader PASS`をCoding前の無条件成功条件と誤読しないよう改訂。S09独立監査指示`combined_review/165`にR17追加。
- **DEC-PREPCODE-01 未決:** 既存引継ぎは`S10全体統合Freeze→S11 Gate別Authorization`。G01 P00はcandidate T2/T3はCoding Entry前の必要条件ではない、他方147は41全MethodのOracle/数値受入パラメータをContract Freeze前の要件としている。A=元のGlobal S10 Freezeを維持（41 Method全件のPre-code契約を閉じてからG01着手）、B=共通Invariantの独立監査/Freezeを前提に、Gate-scoped S09独立監査→S10 Freeze→S11（G01等そのGateとupstream依存の必要契約だけ完備すれば着手、各後続Gateは個別監査/Freeze/Authorization、402全件はimpact inventoryのまま管理し未監査GateはNOT_REVIEWED）。現時点は**Aが現行規則**、BはOwner明示承認が必要。実装前の未決を隠さず、Owner判断要求のために172へ比較記録した。
- S05-B02 Python3.12実Validator、B03実Reader、B04本物のBackend、B05独立Science、S09独立監査は依然NOT_RUN/BLOCKED。S10 NOT_FROZEN、S11 CODING_NOT_AUTHORIZED。

## M. DEC-PREPCODE-01=B採用後の実行・G01独立監査準備（2026-11-22）

- **Owner判断確定:** `DEC-PREPCODE-01=B`。旧「全GateのS09/S10統合完了→Gate別S11」は改訂され、**共通Invariantと対象Gate/実依存閉包の独立S09→Owner Gate別S10→Owner Gate別S11**となる。G02+の実依存Gate999は当該S11前に必要。Gate自身のS09準備は上流実装と並行可能。正式記録`combined_review/173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md`。
- **文書伝播:** G01〜G10各Gateの06/P00/07 **計30文書**、40 Operator実行Prompt **7文書**およびREADME 3件を変更。G01主06に唯一残存した廃止済み`local_policy.py / PolicyVerifierPort`の配置指示を削除。これらはAuthor修正で、Independent S09 PASSではない。
- **変更影響Index:** `combined_review/s09_post_reconciliation_document_snapshot_draft11.json`に402 unique Source blob SHAを再固定。draft10→draft11はGate30+Operator7の**37 normative blobs**変更、元Method200/factored5/Schema13/Stock98は当該Index比較で不変。索引元Source SHA=`6661873f47d1c3c28f80ff190f74a0e2dc92c407`。全402件は世界全体のimpact inventoryであり、400超の独立意味論監査をG01 Coding前に要求しない。
- **G01 initial S09 subset:** `combined_review/s09_g01_scoped_review_inventory_draft1.json`は402 entriesを`OWN_GATE=12`（8 G01 06/P00/Pxx/07 +4 FCI特化Schema）、`COMMON_SHARED=69`（7 Operator含む）、`IMPACT_SAMPLE=4`、`DEFERRED_OTHER_GATE=317`に区分。G01意味論レビュー候補85件。これは独立Reviewerが依存を実現物から発見・拡張するための**候補**であり、真のClosure完備やPASSを証明しない。
- **G01 pre-code blocker/引渡:** `combined_review/174_20261122_g01_coding_entry_readiness_and_s09_submission.md`を作成。G01 FCI Configの2Schemaは差が`$id/title`のみというAuthor JSON comparison。標準Draft202012検証10 Schema、ENV-BASE Python3.12実API+tiny FCI fit/negative、MAG/PAG独立OracleとFixture実体、S09独立review、Owner S10/S11は引き続きNOT_RUN／未承認。Real E11 Reader/Publisher・T2/T3・FS・既存v2回帰はS11後G01 07/999。
- **判断待ち:** 新規Owner科学判断なし（B採用済み）。承認済みLinux VM/Codexと独立Reviewerは本チャットから実行できない。稼働・閲覧権限がないという事実を`B02/B04/B05` PASSに置換しない。

## N. G01 FCI/BK・Graph境界の証拠付きAuthor是正（2026-11-22）

- **R21 Local Graph責務境界：** G01主06/P03 Work Package表にあったProduct `GraphVersionService`がLocal revisionを所有するような表現を、現行Local Graph `version_id=parent_version_id=null`、scientific parent provenance/ContentRef/hashと、既存ProductのみのVersion Writerに修正。Stock 23_41/30_61/P03/Schemaと一致。実Product Source/DBは無変更。
- **R22 G01 Schema構造Probe：** `combined_review/tools/e11_g01_schema_precode_probe.py`を追加。Python3.12 `jsonschema.Draft202012Validator.check_schema`による6 public+4 G01 FCI Profileのメタ検証、P1-M06 Config/Question/Designの明示正負Fixture、Config重複2 Schemaの差分確認、Graph両Version nullとManifest/Status enum一致をsource-SHAで検証するread-only準備。承認環境での実行は`NOT_RUN`。Public 6 wireの完全な正負実例と横断意味論を証明するものではない。
- **R23 G01 Backendのtagged source確認：** `py-why/causal-learn` tag `0.1.4.8` FCI.py Git blob `869b8de01ed495ce4738d3452e0217604dc31e9b`を直接読んだ。APIに`node_names`と`show_progress`あり、BK helperは非null BKに無条件print、forbidden BK方向はadd_directed_edgeで円端点を不要TAILへ上書きしうる。2026-11-22時点[upstream #266](https://github.com/py-why/causal-learn/issues/266)はOPEN。Sourceレベルの危険証拠であり実Python3.12 import/fit成功、PAG数値科学評価ではない。詳細`combined_review/175_20261122_g01_fci_0148_tagged_source_bk_stdout_preflight.md`。
- **R24 契約改訂：** G01主06、G01/P04、G01 07を改訂。現行 tag 0.1.4.8では`background_knowledge=null`のみ候補として実行可、非null（空配列を含む）は`BACKEND_SEMANTICS_UNVERIFIED`/exit4で**FCI呼出前**deny。BKを動かすには独立MAG/PAG不変endpoint motifと実stdout/log封止の双方を検証。科学Scopeを黙って削る権限ではない（Gate999のBK positive obligationsは残る）。`node_names`引数を使いDataset名の1:1検証を要求。
- **R25 非Production fitted API Probe：** `combined_review/tools/e11_g01_fci_backend_precode_probe.py`を追加。ENV-BASE Python3.12に`causal-learn==0.1.4.8`、seed固定合成3列data、明示`node_names`、no-BK fit、GraphEdge/Node検査、stdout/stderrと不正CIメソッド拒否を調査するレビュー用コード。**実行NOT_RUN**、GRAPH-A Science Oracle/Monte Carlo/Policy Source実装にはならない。既存`159` Runbookに両Probeの実行方法を追加した。
- **R26 S09提出資料更新：** 独立Reviewer `165`にR19（FCI BK stdout/過剰TAIL）、R20（Local Graph writer）を追加。G01 readiness `174`にも反映。`s09_post_reconciliation_document_snapshot_draft12.json`に3つの改訂G01規範文書を再pin、全体402件。`s09_g01_scoped_review_inventory_draft2.json`に初期85件（OWN_GATE12/COMMON_SHARED69/IMPACT_SAMPLE4）と別添レビュー脚本2本+Source evidence1本を区別して列挙。スクリプトは402 norm inventoryには混入しない。
- **残件の実態：** G01標準Schema実行、ENV-BASE実fit、BK corrected semantics、独立MAG/PAG Reference実体+科学review、独立G01 S09は`NOT_RUN`。Owner G01 S10 `NOT_FROZEN`、S11 `NOT_AUTHORIZED`。別Owner決定はまだ要求していない（BK正例が最終的に方法能力を満たせず契約の緩和を要するなら別途判断）。

## O. G01 S09最小化・Review-only Runbook是正・B05独立Graph候補（2026-11-22）

- **Runbook実行範囲の実修正:** 159の旧シェル本体は、注釈で「G01だけ」と書いても200 Profileと4つのBackend全環境を**自動実行**していた。実際のコマンドから不要な全Method CompilerとDOWHY/ECONML/TIGRAMITE構築ループを外し、**6共通Schema＋3現行P1-M06 Profile**、Python3.12 `ENV-BASE`のみの実行に変更。200×5確認や追加BackendはG02〜G09の持分に残る。
- **非自己参照SHA:** 159とレビュー専用Pythonスクリプト2件を修正。 `G01_REVIEW_TARGET_FULL_SHA`を外部の独立Reviewerが既にpinした40 hex値として必須とし、checkoutの現在HEADをそのまま期待値にして「一致」を装う手順を削除。`uv.lock`のGit blob SHAとSHA256、Probe Source Git blob SHAをレポートに残す。Schema読込で重複JSON keyをfail closed。
- **現行Schema Authority:** `schema_drafts/README.md`によるActive P1-M06 3 Profile＝Config/Question/Design、`e11_g01_fci_method_config_v1.schema.json`は**historical/non-dispatch**と区別。現行3＋共通6=9をG01必須、旧1は参考上の構造差分診断のみ。S09 scoped inventory `s09_g01_scoped_review_inventory_draft3.json`で**OWN_GATE11 / COMMON_SHARED69 / IMPACT_SAMPLE5 / DEFERRED_OTHER_GATE317**、G01 Author候補85件を維持。旧draft2は過去証跡。
- **GRAPH-A独立科学設計:** `combined_review/176_20261122_g01_p1_m06_graph_a_independent_oracle_candidate_cases.md`を作成。既存DGP-021のcollider `A→K←Y`の `Cov(A,Y|K)=-ab/(a²+b²+σ²)`、mediator `A→M→Y`の `Cov(A,Y|M)=0`を独立数式で導出、DGP-011の2変数latentを直接原因モデルと観測上識別できない反例を整理。**これは完全なPAG同値類／BK救済法の確定でも独立Reference PASSでもない**。既承認GRAPH-Aを維持する。
- **実際のB05科学課題:** `causal-learn 0.1.4.8` FCI BK #266の不正TAIL過剰確定とnon-null BK stdout `print`を証拠とし、非null BKは現時点でfail-closed。P1-M06 positive BKをG01_999で合格させるには、独立科学的に正しいendpoint処理とstdout containmentの具体方法の検証が必要。安易なno-BKのみの本受入は不可。Linux Python3.12 actual fitted backend/独立MAG/PAG Oracle/ReviewerはNOT_RUN。
- **ステータス機械可読化:** `combined_review/s05_current_blockers_draft1.json`をOwner B/ G01 scopeで更新し、古い`S06–S08 NOT_STARTED`、全200 Profile/4環境/全41科学をG01前提にする記載を撤回。S06–S08はAuthor改訂済み（独立PASS未取得）。G01 S09 NOT_RUN, S10 NOT_FROZEN, S11 NOT_AUTHORIZED。
- **最新チェック:** Global source index draft12の**402 unique Git blob一致 402/402**、G01 scope draft3の402全entry一致、補助資料4件SHA一致。チェックは書類/ソース整合性のみでScience/Backend実行ではない。最新HEADは検証のたび変わるため、実S09の真の`REVIEW_TARGET_FULL_SHA`は独立Reviewer起動前に別途固定すること。
