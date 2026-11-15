# ENH-E11 — 設計書改定案

**文書区分:** 計画・設計判断案  
**状態:** DRAFT／Architecture Review未完了  
**前提:** 事前調査`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`、スコープ案`00_04_phase1_to_phase3_cli_scope_proposal.md`のR/Q/N/D、ならびに`03_requirements_revision.md`の要件改定案。

## 1. 参照設計

正本：`docs/wiki/requirement_definition/21_logical_data_design.md`、`22_product_basic_design.md`、`23_api_interface_design.md`、`30_detailed_design.md`。
既存実装：`src/ariadne/interfaces/cli/`、`src/ariadne/scientific/`、`src/ariadne/causal/inference/`、`src/ariadne/product/domain/analysis_spec.py`、Scientific Core ports。

## 2. 設計差分（案）

### 2.1. Scientific CoreとDomainの責務

- **Question/Design/Graph:** 現行schemaを可能な限り再利用する。DB不要のlocal executionでProduct versionを直接使用できなければ、版管理されたlocal identity/provenanceを用意する。
- **Identification:** Native/DoWhyの結果をAriadneの科学的statusに正規化する。前提仮定とsource graphを保持し、Libraryオブジェクトを標準payloadに含めない。**Frontdoorの数値推定もPhase1に必須包含するオーナー判断（2026-11-01）**は識別成功とは別Estimator契約・科学Benchmarkで受け入れる（[SR-03追加メモ](../working_notes/20261101_sr03_late_estimator_options_econml_inference_review.md)）。
- **Discovery:** FCI/PCMCI系にalgorithm ID、CI test、parameter、backend versionを持たせる。endpoint・lagと不確実性を失わない往復serializeを保証する。
- **Estimation:** 既存`ipw`/`aipw`を維持し、CATEと準実験固有estimandを一律ATE/ATTのフィールドに押し込めない。
- **Refutation/Sensitivity:** 上流Effectの識別子と実効parameter/seedを持つ方法別Resultを定義し、既存method codeを保護する。Negative Control exposure/outcome、Unobserved-confoundingの最小実行方式は`00_04_phase1_to_phase3_cli_scope_proposal.md`の**採用案・承認待ち**として、適用仮定・negative result・独立検証方法を別途決定する。
- **Temporal/Quasi-experimental:** Panel、時刻、running variable、IV、donor poolの妥当性を、横断データの既存入力契約とは分けて検証する。

### 2.2. ローカル成果物の流れ

`検証済みCLI設定 → 科学メソッドAdapter → Result/Diagnostics → 永続ローカルファイル → Manifest`。

Manifestに入力hash、parameter、実効dependency version、seed、split、科学的status、artifact checksumを記録する。Product DBのIDを必須としない。既存CLI helperを再利用し、従来`config_version=2.0`読取との互換性・schema version境界はArchitecture Reviewで判断する。

大規模な個票CATEはParquet、要約はJSON、手法別科学監査はMarkdown/JSONとし、個票全件を小さな制御応答へ格納しない。

### 2.3. SR-03識別→Estimand→推定器の責務境界（技術案）

**設計入力:** [20261101_sr03_identification_estimand_estimator_contract_review.md](../working_notes/20261101_sr03_identification_estimand_estimator_contract_review.md)（SR-02実測を参照した**未承認の設計案**）。

1. Domainが\`CausalQuestion\`の\`Estimand/Population/Contrast\`、\`CausalDesign\`の\`Strategy/Assumption\`を外部依存なしに型付けする。現行\`causal-analysis-spec/2\`の読み取りを破壊せず、CATE／LATE／IV heterogeneous effectは**新しい版付きvariant**に追加する案。
**SR03-D01個別採用（2026-11-01）：** IV異質効果を独立Estimand familyとする。科学的定義・選択肢比較・必須不変条件は[ファイルD01](../working_notes/20261101_sr03_iv_heterogeneous_estimand_decision.md)に一元化する。本書はDomain/IdentificationResult/EstimatorSpec/CLIの**設計責務と実装互換性**を管理し、正式schema・Method別Science/Gateは未承認とする。
2. \`IdentificationResult\`が対象Estimand・Graph／Question／dataset hash、推定根拠、制限・原因codeを保持する。DoWhyの内部\`nonparametric-ate\`は**IVによるLATE推定の対象を保証しない**ため、そのまま科学的estimand labelに転用しない。
3. \`EstimatorSpec\`で識別結果とMethod適格性を照合し、数値推定の前に\`REQUIRES_REVIEW\`／\`NOT_IDENTIFIED\`の新Method自動通過を禁止。現行CLIのREQUIRES_REVIEW入力許容は**回帰保護対象であると同時に安全性の審査対象**。
4. \`EffectResult\`は**識別状態・点推定状態・推論区間可用性**を別軸で保持。EconMLで実証された点推定のみのケースではCI=\`null\`と理由を保存し、架空のCIを作らない。
5. **オーナー採用：Phase3 IV/LATEの初期EstimatorはWald比（Reference）＋2SLS。2026-11-05にはD03-1 S2＝B0（無調整just-ID）＋B1（単一二値Z/A・事前指定C・加法線形構造）を追加採用**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。B1のEstimandはモデル依存の線形IV構造係数として区別する。基本Estimandは二値Z/Aのcomplier LATE（relevance/independence/exclusion/monotonicity）であり、共変量付き・複数IVの2SLSを同一LATEに黙って変換しない。連続処置のDRIV heterogeneous effectは別契約。**D03-4 C1の後続管理方針は2026-11-15に採用**。Phase3初期にはCを追加せず、条件付きIV＋処置効果異質性によりB1が目的Estimandを扱えないユースケースが明らかになった場合にCの科学的採否を再審議する（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。Scientific Methods ownerとスコープ承認者の実名指定、Cの識別対象・仮定・推定・推論・Benchmarkは後続で確定し、CのMethod・コード実装は未採用。FrontdoorはATE識別とモデル依存の二段階推定を別受入とする。
7. **弱IV推論境界（D03-2 I2を2026-11-05に個別採用、詳細実装未承認）:** B0/B1の単一excluded Z・単一内生A、独立観測・異分散頑健漸近推論の範囲でAR検定反転を弱IV頑健な初期基準信頼集合推論とする（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。First-stage効果・SE・Instrument support・IV推定全体の共分散、通常Wald CIの制約を記録する。ARはIVの妥当性を証明せずcluster/HAC等へ無検証で拡張しない。**D03-3 G2改訂（2026-11-06）で有界・非有界・非連結・全実数の型付き集合／B0・B1での正常EMPTY禁止の意味契約を採用**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。**正式G2 schema・D04 migration・実装アルゴリズム・coverage・Gateは未承認**であり、非有界集合を有限CIへ捏造しない。
6. CLIはResult間のhash一致、effective backend version、seed/split、optional dependency欠落を検査する。Product DBに新規統合せず、local manifestでトレースする。

### 2.4. SR03-D04：新E11の識別→推定接続と旧v2共存（個別方針採用）

**Human owner方針採用（2026-11-15）:** D04-1 **V2**、D04-2 **E2**、D04-3 **M2**、D04-4 **G2-Bridge**、D04-5 **R2**の5案をすべて採用。詳細選択肢比較・科学的制約と候補fixtureは[独立D04審議記録](../working_notes/20261115_sr03_d04_identification_estimator_contract_options.md)が一元管理する。以下は設計責務・差分の要約であり、本書全体と正式schema/ADR/Gateの承認ではない。

1. **V2／version dispatch:** 現行`causal-analysis-spec/2`と既存Product/v2 CLI・Resultの入力/readerを変えず、新E11 Methodは独立の版付きlocal spec・Result/Manifestを使う。新version文字列・API/enumはArchitecture Reviewで確定する。
2. **E2／scientific authority:** AriadneのDomainがCausalQuestion／Design／target estimandとMethod別の科学的適格性を定義し、DoWhy等の結果をportable IdentificationResultへ正規化する。EstimatorSpecで識別状態・Estimand・Design・Instrument/Mediator・必要仮定・データ条件を再照合し、条件不成立なら新Methodの数値推定へ通さない。DoWhy/EconMLの内部オブジェクト・ラベルをそのまま科学的Resultの権威としない。
3. **M2／lineage:** Question/Design/Graph/Dataset/上流Manifestの識別子・hashとEstimatorSpecの適合を検証し、旧v2 Manifestを新Methodへ暗黙昇格させない。明示的な移行が必要な場合も、欠落した識別証拠を捏造せず再識別またはレビューを要求する。canonicalizationとatomic write/relative path/privacyはSR-10/ADRの未決に残す。
4. **G2-Bridge／inference:** EffectResultは点推定・uncertainty availability・科学的statusを独立軸で保持し、D03採用のAR型付き信頼集合（bounded/unbounded/disconnected/ALL_REAL）を損失なく持つ。正常なB0/B1のAR信頼集合をEMPTYと記録しない。正式JSON Schemaと数値反転・coverageは未決。
5. **R2／互換ゲート:** 既存Product/v2のREQUIRES_REVIEW＋overrideをD04だけを理由に改変しない。新E11の未識別・要レビュー・部分識別は自動的な点推定許可を得ない。将来のGraph再固定や別識別証拠の許可範囲はD06へ、旧経路の回帰実証は独立テストへ引き渡す。

**未承認・未実証:** 新版番号、詳細schema/enum、Method別数値受入、旧reader migration・実測回帰、D05の具体的Method inference/科学実証とD06、Architecture Review、Gate 06/07、全体Scope/Coding。既存Product API/Worker/DBへの新規統合は今回の対象外。

### 2.5. SR03-D05：CATE/DRIV推論・CI契約のMethod別設計責務（個別方針採用）

**Human owner採用（2026-11-15）:** D05-1〜D05-5のB/B/B/B/Bをすべて個別採用。詳細な選択肢比較・科学的限界・方法候補・負例は[独立D05科学判断](../working_notes/20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)が一元管理し、本節は設計上の責務を要約する。**正式schema/Method inference設定・coverage・Gate・全体構想は未承認**。

1. **D05-1／B：Estimand contract:** `EstimatorSpec`は非IV CATEの7 Method（LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S/T/X-Learner）とDRIVの`IV_HETEROGENEOUS_EFFECT`を分離。共通Result envelopeを使う場合も、target population、X/W、instrument/contrast、method-specific moment・assumptionsを混同しない。DRIVの具体的`theta_IV(x)`はSR-04のMethod別検証・D01の未解決項目に残す。
2. **D05-2／B：Analysis mode:** 新E11の`EXPLORATORY`では科学的に適格な点推定のみの結果保存を許す（推論主張は不可）。`CONFIRMATORY`は事前指定の目的に沿う妥当なCI等の推論証拠を必須とし、欠落・未校正のfinite区間をScience PASSとしない。
3. **D05-3／B：Inference registry:** Method/構成/Backend version別に使用推論方式・final model・nuisance/fold/seed・Bootstrap parameters等を明示する。Generic Bootstrapの全手法一律適用も、Native defaultの無条件有効性も禁止。方法候補と正式採用を区別する。
4. **D05-4／B：EffectResult:** 上流識別状態、点推定可用性、CI・uncertainty可用性、科学的受入を別軸化し、未要求・利用不能・計算失敗・科学的不適格のreasonを区別。CIが取得不能ならnullを保存し、無根拠な区間・SEを作らない。D04のG2型付きconfidence setと衝突させない。
5. **D05-5／B：Science Acceptance:** Method/estimandに適合した既知真値、support/overlap、bias/RMSE、反復simulationのpointwise coverageとMonte Carlo誤差、負例（CI unsupported、nuisance misspecification、DRIV weak/invalid IV等）を独立測定する。点ごとの区間をsimultaneous bandと誤称しない。CI level、Bootstrap反復、coverage許容差、seed／DGPはSR-04/Gate07で事前固定。

**試験引渡し:** [D05技術記録 §8](../working_notes/20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)のD05-T01〜T13をGate候補として保持するが、未実行・未freeze。旧v2 Product/CLIの回帰、8 Methodの提供範囲、個票CATEのprivacy、SR03-D06を保留せず明示追跡する。

## 3. 所有権（未承認の案）

- Domainが外部ライブラリ非依存のQuestion/Design/Estimand/invariantを定義する。
- Scientific Core Adapterがoptional backendを呼び出し、数値推定と手法固有検証を担当する。
- CLIがlocal path・ファイル入出力・Manifest生成を担当する。
- 現行Web経路ではProductのGraph/Resultが引き続き権威を持つ。Local spec/manifestはこれと同一DB authorityではない。
- 将来のProduct統合に向け、local identityから再構成可能なDesign契約を検討する。

## 4. 実行経路とデータフロー

- **追加候補:** DoWhy、FCI、EconML、Tigramite、準実験手法のlocal CLI入口とversioned operation spec。
- **維持:** 既存のProduct API→Worker→DBのExecution/Result経路。ENH-E11で新機能を統合しない。
- **維持:** Navigation StageとScientific実行Stageは1対1対応せず、CLIはNavigation状態を要求しない。
- **エラー分類:** 非識別、要レビュー、適格性不足等は科学的Result。依存の欠落、不正設定は型付きの技術・設定errorとする。

## 5. 永続性とMigration

ENH-E11では新規DB migrationやサーバ側Resourceは追加しない。Versioned local file schema、checksum、atomic writeを検討し、部分書込み・retry・個票CATEの秘密保持を事前に決める。既存ArtifactStoreとProduct persisted readは変更しない。将来API/DBへ接続する処理は別Enhancementとする。

## 6. 互換性・導入方法

- `ipw`/`aipw`、GraphType、既存CLI設定を保護し、normalizedとstabilizedの混同を避ける引数にする。
- **オーナー採用方針（2026-11-01）:** Python3.12／Linux基準、DoWhy・EconML・Tigramiteを**機能別optional依存**として遅延importし、対象Capabilityだけunavailable状態を返す。実効package/Python versionを記録する。採用版・lock・科学Benchmarkは検証後に確定。
- **個別SIで顧客環境へ構築・納入（SaaS非想定）:** TigramiteのGPLv3対応は実際の納入物・結合形態・コピー提供者・対応ソース／通知等の**配布前審査**を要する。optional構成を自動免責扱いしない。[調査メモ](../working_notes/20261101_external_backend_policy_temporal_scenarios.md)を参照。
- 正確性の第一証拠はUnit/Contract/Scientific Benchmark。CLI-onlyのためにBrowser E2Eを追加しない。
- 意図してE9/E10の契約を変える場合、差分と理由を明記し、protected regressionを単純に省略しない。

## 7. 暫定的なTransition Debt

| 候補 | CLI-firstで許容する理由 | 解消条件 |
|---|---|---|
| 新手法のAPI/Worker/DB統合なし | オーナーが明示した対象境界 | 後続EnhancementでProduct authorityと統合テストを規定 |
| Local-file identityとProduct versionの差 | DB migrationをしない | 将来の永続統合前に変換・関連付け方針を承認 |
| 手法ごとのArtifact schema | 科学的に異質な結果を無理に同じ数値へ変換できない | versioned schemaと将来のadapterを設計 |
| 全backend/platform互換性の未確定 | 外部Engineの依存制約がある | optional dependency support matrixと再現性試験 |

## 8. Gateとの対応

`01`の暫定G01〜G10と`05`の対応表は、Graph/Design/Resultのauthority、local-file identity、privacy、optional dependencyの決定後に改訂する。**Gate 06/07はいずれも未固定。**

## 9. Architecture Reviewで決める事項

1. DB-freeでのGraph/Question/Designの版管理と所有者。
2. Result／Diagnostics／Artifactの境界。
3. IdentificationのGateと非識別状態。
4. TIME_SERIES_GRAPHのendpoint/lag互換性。
5. CATE/準実験Design固有estimand。
6. 方法別推論方式と科学ベンチマーク。
7. 外部依存version matrix・インストール分離。
8. CLI versioning、path安全性、atomic write、privacy。
9. 将来API/Worker/DBへの移行方針。ただしE11では実装しない。
