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
2. \`IdentificationResult\`が対象Estimand・Graph／Question／dataset hash、推定根拠、制限・原因codeを保持する。DoWhyの内部\`nonparametric-ate\`は**IVによるLATE推定の対象を保証しない**ため、そのまま科学的estimand labelに転用しない。
3. \`EstimatorSpec\`で識別結果とMethod適格性を照合し、数値推定の前に\`REQUIRES_REVIEW\`／\`NOT_IDENTIFIED\`の新Method自動通過を禁止。現行CLIのREQUIRES_REVIEW入力許容は**回帰保護対象であると同時に安全性の審査対象**。
4. \`EffectResult\`は**識別状態・点推定状態・推論区間可用性**を別軸で保持。EconMLで実証された点推定のみのケースではCI=\`null\`と理由を保存し、架空のCIを作らない。
5. IVでは二値Z/AのLATE、連続処置のDRIV heterogeneous effectを区別。FrontdoorはATE識別と**モデル依存の二段階推定**を別受入とする。
6. CLIはResult間のhash一致、effective backend version、seed/split、optional dependency欠落を検査する。Product DBに新規統合せず、local manifestでトレースする。

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
