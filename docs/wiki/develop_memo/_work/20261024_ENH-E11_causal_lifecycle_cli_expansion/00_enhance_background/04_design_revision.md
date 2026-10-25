# ENH-E11 — 設計書改定案

**文書区分:** 計画・設計判断案  
**状態:** DRAFT／Architecture Review未完了  
**前提:** `00_foundation_gap_reconciliation.md`の既存機能・残差分類、`03_requirements_revision.md`の要件改定案。

## 1. 参照設計

正本：`docs/wiki/requirement_definition/21_logical_data_design.md`、`22_product_basic_design.md`、`23_api_interface_design.md`、`30_detailed_design.md`。
既存実装：`src/ariadne/interfaces/cli/`、`src/ariadne/scientific/`、`src/ariadne/causal/inference/`、`src/ariadne/product/domain/analysis_spec.py`、Scientific Core ports。

## 2. 設計差分（案）

### 2.1. Scientific CoreとDomainの責務

- **Question/Design/Graph:** 現行schemaを可能な限り再利用する。DB不要のlocal executionでProduct versionを直接使用できなければ、版管理されたlocal identity/provenanceを用意する。
- **Identification:** Native/DoWhyの結果をAriadneの科学的statusに正規化する。前提仮定とsource graphを保持し、Libraryオブジェクトを標準payloadに含めない。
- **Discovery:** FCI/PCMCI系にalgorithm ID、CI test、parameter、backend versionを持たせる。endpoint・lagと不確実性を失わない往復serializeを保証する。
- **Estimation:** 既存`ipw`/`aipw`を維持し、CATEと準実験固有estimandを一律ATE/ATTのフィールドに押し込めない。
- **Refutation/Sensitivity:** 上流Effectの識別子と実効parameter/seedを持つ方法別Resultを定義し、既存method codeを保護する。
- **Temporal/Quasi-experimental:** Panel、時刻、running variable、IV、donor poolの妥当性を、横断データの既存入力契約とは分けて検証する。

### 2.2. ローカル成果物の流れ

`検証済みCLI設定 → 科学メソッドAdapter → Result/Diagnostics → 永続ローカルファイル → Manifest`。

Manifestに入力hash、parameter、実効dependency version、seed、split、科学的status、artifact checksumを記録する。Product DBのIDを必須としない。既存CLI helperを再利用し、従来`config_version=2.0`読取との互換性・schema version境界はArchitecture Reviewで判断する。

大規模な個票CATEはParquet、要約はJSON、手法別科学監査はMarkdown/JSONとし、個票全件を小さな制御応答へ格納しない。

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
- optional dependencyは遅延importとし、対象Capabilityだけunavailable状態を返す。実効package/Python versionを記録する。
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
