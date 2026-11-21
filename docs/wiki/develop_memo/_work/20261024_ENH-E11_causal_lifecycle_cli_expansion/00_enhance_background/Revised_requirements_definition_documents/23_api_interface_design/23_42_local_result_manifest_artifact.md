# 23_42_local_result_manifest_artifact

## 1. 公開される契約と責務

Local runのFile BundleはProduct DBのResult/Artifact/Lineage Resourceと異なる永続化Interfaceであり、同じ科学的Resultの意味を共有する。ファイルの作成者・参照者は検証済みsame-UID、non-delegated OS Principalとprivate TrustedRootの範囲で責務を持つ。共有・委譲主体を無条件には許さない。ProductのProjectMembership OWNER/EDITOR/VIEWERを、DB未接続のFile Interfaceへ擬似適用しない。

公開ディレクトリは `ROOT/runs/{run_id}/` の一単位で不変とする。Readerは `manifest.json` と `_COMMITTED.json` を検証して初めてbundleを受け付け、個々のArtifactの存在だけを成功と解釈しない。公開Manifestは科学的結果の内容、Artifactは物理bytes、statusは実行事実を表す別権威である。

## 2. Local file layout（相対キー）

~~~text
ROOT/
  .staging/
    {random-staging-token}/
       study.json
       status.json
       result.json                  # Effect Operation時のみ
       graph.json                  # graph operation時のみ
       diagnostics.json            # 対応Method時のみ
       row_effects.parquet         # 明示許可された時だけ
       manifest.json
       _COMMITTED.json
  runs/
    {run_id}/                      # 同一Filesystem内で一括rename公開
       study.json
       status.json
       result.json                  # Effect Operation時のみ
       ... 
       manifest.json
       _COMMITTED.json
~~~

- `run_id`は安全な固定文法（ASCII英数、`-`、`_`、最大128文字、`.`・`..`・path separator禁止）を満たす。run IDはGraph/Question/Content IDを代用しない。
- Artifact keyはbundle rootからの相対POSIX path。絶対path、`..`、空component、prefix混同、symlink、hardlinkによるroot外参照を拒否する。Path validation後もOpen時のO_NOFOLLOW／dirfd相当の操作でraceを防ぐ。
- `.staging`は完成bundleでない。staging rootとfinal rootの同一デバイス／同一FileSystem／atomic directory rename可能性をpreflightで確認する。NFS/object-store/Windows/異FSで同等性を前提化しない。
- 同じ `run_id` の再実行は既存Manifest/request hashが一致し、readbackも成功する場合のみその結果を参照できる。異なるhashは `RUN_ID_CONFLICT`。上書き禁止。

### 2.1. Operation別Bundleとcross-schema不変条件

`manifest.schema_dispatch.result`はEffect Resultを判別するだけであり、IDENTIFYや診断の結果を代替しない。OperationごとにManifest/Status/Artifact inventory/Method/上流hashを連結して検証する。

| Operation | 正常な必須Artifact | 条件・禁止項目 |
|---|---|---|
| DISCOVER | `study.json`、`status.json`、Graph生成成功なら`graph.json` | 科学的なGraph無し負結果では`diagnostics.json`とnonempty reasonが必須。Graph無しは`schema_dispatch.graph=null`。いずれも`result.json`は禁止 |
| IDENTIFY | `study.json`、`status.json`、`identification.json` | 識別Proof、Graph/Design/Estimandと上流hashを検証。非識別もtyped negativeとして保持。Effect Resultは禁止 |
| ESTIMATE | `study.json`、`status.json`、`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point不在はnull+reason。Estimator未呼出のnegativeを架空の推定値に置換しない |
| REFUTE / SENSITIVITY / DIAGNOSE | `study.json`、`status.json`、`diagnostics.json` | Method別診断のtyped result、上流Effect/Graph/Design hash、seed、適用条件を検証。Effectを再発行しない |

全Operationで`manifest.json`と`_COMMITTED.json`が必要で、どちらもartifact inventory外に置く。Inventoryは実在するstudy/status/Graph/Identification/Effect/Diagnosticsと対応するbytes hash、size、MediaType、Privacyを全件列挙する。各Operation/Method固有の内部JSON profileをstrictに検証し、Method profile未登録を実行許可としない。内部profileは5種類の公開payload versionを増やさない。

DISCOVER成功時はGraphが必須。科学的に正当なGraph無しnegativeを技術的Backend失敗と区別し、後者を成功Bundleに変換しない。その他OperationのMethod-specific profileは当該Method提供前に厳格化してpositive/negative fixturesを検証する。

## 3. Result JSON

本節のEffect ResultはEffectを生むOperationにだけ適用する。`DISCOVER/IDENTIFY`ではダミーEffectを生成せず、Manifestの`schema_dispatch.result=null`とOperation別ValidatorでGraph/Identification成果物を検証する。

| Key | JSON type | Mandatory | Meaning |
|---|---|---|---|
| `schema_version` | string | YES | `e11-local-effect-result/1` |
| `result_id` | string | YES | immutable result identity |
| `run_id` | string | YES | Local run identity |
| `estimand` | object | YES | family、population、contrast、time、target reference |
| `design_ref` / `question_ref` | object | YES | content identity、hash |
| `graph_ref` | object/null | conditional | graph evidence、kind、version、hash |
| `identification` | object | YES | status、proof reference、reasons、lineage |
| `point` | object | YES | availability、value（number/null）、unit、reason |
| `uncertainty` | object | YES | availability、kind、level、CI/AR set、reason |
| `science_acceptance` | object | YES | evidence state、evidence ref/null |
| `diagnostics` | array | YES | method-specific typed refs、warnings |
| `method` | object | YES | Method ID、effective estimator/backend/inference config |
| `privacy` | object | YES | classification、row-level capability、release policy |

数値 `point.value`がない場合は `point.availability != AVAILABLE` かつ理由必須。`point.value`が存在しても `science_acceptance.state=PASS` を導けない。未知・未実測のScienceは `NOT_EVALUATED`。Result中に生データ、Python object、非有限JSON number、絶対入力path、secret、credentialsを埋め込まない。

例：

~~~json
{
  "schema_version": "e11-local-effect-result/1",
  "result_id": "example-effect",
  "run_id": "example-run",
  "estimand": {
    "family": "LATE_COMPLIER",
    "population": "compliers",
    "contrast": "A1-A0"
  },
  "design_ref": {
    "identity": "design-1",
    "relative_key": "inputs/design.json",
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "media_type": "application/json",
    "schema_version": null
  },
  "question_ref": {
    "identity": "question-1",
    "relative_key": "inputs/question.json",
    "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "media_type": "application/json",
    "schema_version": null
  },
  "graph_ref": null,
  "identification": {
    "status": "IDENTIFIED",
    "proof_ref": {
      "identity": "proof-1",
      "relative_key": "upstream/identification.json",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
      "media_type": "application/json",
      "schema_version": null
    },
    "reasons": []
  },
  "point": {
    "availability": "AVAILABLE",
    "value": 0.5,
    "unit": "outcome",
    "reason": null
  },
  "uncertainty": {
    "availability": "NOT_REQUESTED",
    "kind": null,
    "interval": null,
    "confidence_set": null,
    "reason": {
      "code": "NOT_REQUESTED_BY_USER"
    }
  },
  "science_acceptance": {
    "state": "NOT_EVALUATED",
    "evidence_ref": null
  },
  "diagnostics": [],
  "method": {
    "id": "P3-M09",
    "backend": "native",
    "config": {},
    "inference_method": null,
    "backend_version": null
  },
  "privacy": {
    "classification": "AGGREGATE",
    "row_level_export": false
  }
}
~~~

上記の`sha256`は64桁0で**Schema上は形式妥当だが、実bytes由来の検証済みdigestではない**。実行入力として受け付けない。例は説明用であり、MethodとEstimand/識別の科学的適格性を証明しない。Schemaと実効Hash/Methodの受入条件は別に検証する。

## 4. AR Confidence Setの損失ない表現

B0/B1でAR検定反転により得る信頼集合は、全ての実数を含む場合も、非連結や非有界の場合も単一区間とは限らない。Finite CI schemaへの丸め込み禁止。これはStatistical confidence setであり、Partial Identificationの識別集合とは異なる（その区別は科学的推論契約に属する）。

~~~json
{
  "confidence_level": 0.95,
  "topology": "DISCONNECTED",
  "components": [
    {
      "lower": {"kind": "NEG_INFINITY"},
      "upper": {"kind": "FINITE", "value": -2.0},
      "lower_closed": false,
      "upper_closed": true
    },
    {
      "lower": {"kind": "FINITE", "value": 3.0},
      "upper": {"kind": "POS_INFINITY"},
      "lower_closed": true,
      "upper_closed": false
    }
  ],
  "inversion_evidence": {"identity": "ar-grid-and-brackets", "relative_key": "artifacts/ar-grid.json", "sha256": "0000000000000000000000000000000000000000000000000000000000000000", "media_type": "application/json", "schema_version": null}
}
~~~

- 上例はAR集合のサブオブジェクトであり、外側の`uncertainty.kind=AR_CONFIDENCE_SET`に配置する。`inversion_evidence`は必須ContentRef。ゼロdigestは実測でないダミーであり実行時には拒否する。
- 各endpointは `FINITE(value) / NEG_INFINITY / POS_INFINITY` のtagged union。JSONに `NaN / Infinity / -Infinity` numberを含めない。
- Componentは下界昇順・空でないintervalで、重複・接続する成分は数学的に和集合として正規化する。真のdisconnectedは成分数2以上。有限・無限端点のclosed flagは規定値に一致すること。
- `topology` は **`EMPTY / ALL_REAL / DISCONNECTED / UNBOUNDED / BOUNDED`**。優先順位はEMPTY（`components=[]`）→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDEDとし、DISCONNECTEDには非有界componentが混在し得る。全実数は `topology=ALL_REAL; components=[(-∞,+∞)]` の一意表現。**数学的EMPTYは汎用Codecで正常な推論結果として表現可能**。B0/B1のjust-identified MethodでEMPTYが科学的不整合ならMethod-specific validatorで拒否し、計算`FAILED`と混同しない。
- 推論がUNAVAILABLE/FAILEDならconfidence_set=nullとreasonが必須。単なる `point_only` から合格区間を捏造しない。Monte Carlo coverageと弱IV頑健性はMethod別の独立科学検証で評価する。
- Intervalの端点条件やstrict inequalityの扱い、AR statistic/covariance/threshold/reference・数値探索精度は30_61/30_63のMethod別検証契約に属する。

## 5. Graph／temporal evidenceの往復

Graph JSONは `e11-local-graph/1`。`version_id`／`parent_version_id`は実在するProduct GraphVersionへの参照であり、CLI単独生成時は両方`null`とする。`parent_version_id`が非nullの場合、`version_id`も非nullで両者が実際に存在するProduct GraphVersion lineageに一致しなければならない。架空Product IDを発行しない。Graph自身のimmutable identityは`content_hash`と外部ContentRefで識別する。頂点ID、graph kind（DAG、CPDAG、PAG、必要なlatent/temporal variants）、edge endpoint pairs（tail/arrow/circle）、lag付き向き、time index policy、optional Product GraphVersion参照（存在時のparent/version provenanceを含む）、assumptionとsource reference/hashを保存する。`GraphEvidence`はimmutable科学Valueであり、CLIのGraph生成はProduct GraphVersion発行を必要としない。Graph編集/新Version作成/FIXはProduct連携時に既存`GraphVersionService`だけが実施する。

禁止する可逆でない変換：
- PAG circle-circle、circle-arrow、bidirected等をDAG単一向きへ丸める。
- 不確定な同時点edgeを確定時系列方向とみなす。
- lagと時刻の正負規約を失う。
- Graph FIXEDを「因果モデル科学的真」とみなす。
- 未確定GraphからのIdentificationをWARN overrideで勝手に点推定へ許す。

## 6. Manifest／Commit marker

`manifest.json` の最小必須項目：

| Group | 必須情報 |
|---|---|
| identity | `manifest_version=e11-local-manifest/1`、run_id、operation、request_hash、schema dispatch |
| lineage | question/design/graph/dataset/upstream Identification refs＋hash、effective Estimand |
| execution | technical/result science axis、actual backend and method、inference config、analysis mode |
| runtime | repo commit/dirty、Python/platform/CPU/BLAS threads、uv.lock hash、installed distribution/version、extras、actual API probes、**canonical_codec_version** |
| stochastic | effective seed、stream derivation、split/partition hash、fold、Bootstrap config、retries |
| artifacts | canonical relative key、type、size bytes、sha256、privacy classification、visibility |
| review | method Reference／Science evidence refs（未実行ならnull）。顧客配布の法務判断はManifest外で管理 |

`_COMMITTED.json` は `{"marker_version":"e11-commit/1","run_id":"...","manifest_sha256":"...","request_hash":"..."}`。Manifestは自身のhashを含めず、markerがManifestのbytes hashを指す。Markerはartifact一覧の外側にあり循環hash参照を作らない。Readerは marker→Manifest→各Artifact hash/size/MediaType→Operation別必須/禁止Artifact、schema_dispatch、Status、Method、upstream lineage cross-refを検証する。外部からの上流参照もtrusted root＋hashの範囲で再照合する。

Manifestに全source pathを生の絶対パスで記録せず、再現に必要な参照とdigest、非機微な環境要約を格納する。内部CLIのManifestにはSBOM referenceや顧客配布承認状態を要求しない。個票Parquetをdefault summary／console／JSONに含めない。

### 6.1. Operation dispatch・Hashの非循環性

5つの採用済みVersion (`e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1`) はstrictに判別し、Markerは独立`e11-commit/1`。Resultの不存在は非Effect Operationで`schema_dispatch.result=null`として表現し、Operation別validatorで必要/禁止の整合を検査する。

`request_hash = SHA256(JCS(validated typed Study JSON))`、Codecはstrict `e11-json-jcs-rfc8785/1`（Product `hash_mapping(default=str)`不使用）。Graph内部`content_hash`は自己fieldを除いた意味射影のSHA256、外部`ContentRef.sha256`はGraph File実bytesのSHA256。Manifestは自己hashを持たず、Markerの`manifest_sha256`は保存Manifest実bytes。run_id/request_hash/Method/Estimand/GraphVersion/Privacyと全upstream/file hashはcross-schema意味Validatorで突合する。

## 7. PublishとReadback failure semantics

1. Output root自体のowner/permissions、同一FS、run_id未使用、承認済みprivacy policyを確認。
2. `.staging/{token}`を権限 `0700`、各通常fileを `0600` で生成し、Method adapterの**すべての出力先**をstaging配下に限定する。
3. 各Artifactをhash、schema、row-level leakage、method-specific semantics検査。Manifest/markerを作成し、ファイル・ディレクトリをfsyncする。
4. Publication直前にstaging bundleの全件readbackとReference integrityを検証。失敗すれば公開せずrollback。
5. Linux同一FSの`renameat2(RENAME_NOREPLACE)` directory操作のみを可視化pointとして `runs/{run_id}` をpublish。親dir fsyncでdurabilityを補強。
6. Crash後のrecoveryは公開runのmarker検証を行い、未公開stagingは成功とせず隔離／管理者条件下のみ清掃する。rename直後の電源断時の耐久性はOS/FS保証範囲で判定。
7. Runはimmutable。rename後のfsync/readback不明は`PUBLICATION_INDETERMINATE`として既存runを削除・上書きせず、partial publicationをsuccess扱いしない。既存 `ArtifactStorePort.store/retrieve/exists/delete` ではこの複数fileトランザクションは保証しない。

出版のatomicityはディレクトリ単位のvisibilityであり、異Filesystemやネットワーク障害を越えるexactly-once保証ではない。Proofにはfault injectionとFS boundary testが必要。

## 8. Local privacy／distribution

- 個票を含む `row_effects.parquet` は `RESTRICTED_ROW_LEVEL`。通常出力では作らない。明示Study requestとCLI flagのdouble opt-in、非root実行UIDが所有するprivate ext4/XFS TrustedRoot、Method別の列/行/byte/memory上限を全件検証する。独立承認や署名鍵を要求しない。
- Local OS PrincipalはProduct ProjectMembershipを代替する認証ではない。初期対象は非root EUID所有のprivate local ext4/XFS root/0700、row file/0600で、safe dirfd・Path・same-FSを検証する。独立ACL/xattr/namespace/mount visibility証明やCI/container環境種別判定を要件化しない。同一UIDとOS管理者からの隔離は保証しない。stdout/stderr/log/exception traceに個票やsecretを出さない。
- Customer delivery可否は科学的結果・内部実行の状態とは別。GPL系Backendを含む受領者別Bundleの法務レビュー未完は `CUSTOMER_DELIVERY_BLOCKED` として扱う。

## 9. 恒久Interface Contract Test

| ID | Test | 失敗なら拒否する条件 |
|---|---|---|
| IO-E11-01 | Artifact key traversal / symlink / race | root外read/write、symlink attack |
| IO-E11-02 | Multi-artifact crash/fault injection | marker無し、hash mismatch、途中bundle |
| IO-E11-03 | Same run_id retry, content equivalence | request hash不一致で再利用 |
| IO-E11-04 | JSON AR topology round-trip | DISCONNECTED/ALL_REAL/無界endpoint喪失 |
| IO-E11-05 | Graph endpoint/lag/GraphVersion round-trip | circle消失、parent欠落 |
| IO-E11-06 | Restricted CATE Parquet/summary/CLI leakage | opt-in無しの個票公開 |
| IO-E11-07 | Backend/env/lock metadata readback | 適用不能Versionや不明依存の成功扱い（内部CLIでSBOM非必須） |
| IO-E11-08 | immutable run／partial Manifest rejection | stale hashes、non-atomic backend |
| IO-E11-09 | Product v2 reader regression | legacy Manifestを新Bundle Schemaとして誤解釈 |

参照：[CLI / Scientific Port](23_41_cli_scientific_ports.md)、[Results/Artifacts/LineageのBD](../22_product_basic_design/22_09_results_artifacts_lineage.md)、[Existing Product Artifact Port](../30_detailed_design/30_50_persistence_artifacts.md)。

### AR・Privacyの意味的検証

AR集合は`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`の5分類。`EMPTY`は数学的に正常に反転した0成分で`AVAILABLE + inversion_evidence`と共存しうる一方、計算失敗は`FAILED + reason`。端点で双方openの接触区間はgapを保存する。非退化なB0/B1 HC1 ARの非空条件はMethod固有Validatorで判定し、CodecやSchemaの検証を統計的Coverageの証明としない。

行出力はStudyとCLI両方の明示opt-inを実行UIDのprivate root・Method別schemaとAND検証し、不成立なら個票を生成せずexit3。出版前の検証だけでなく、ReaderもMarker/Manifest/Filesの実bytes・size/type、private Artifactの権限とLineageを再検証する。

### 9.1. Class・Portとの単一Authority／互換性

`ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`はManifest ValueのSchemaとstrict bytes射影を所有し、`ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`が発行済みBundleの独立readbackを担当する。`LocalArtifactPublisher`は同一FS run単位のatomic publicationを担い、既存`product.ports.artifact_store.ArtifactStorePort`の単一File/Object storeを置換しない。`GraphEvidence`と`EffectOutcome`の科学的意味はCausal Domain側のValue/Validatorで検証する。

Schemaの`e11-local-*/1`、`e11-commit/1`、`e11-json-jcs-rfc8785/1`は既存Wire識別子であり、文書名に含まれるEnhancement番号とは別の**Version互換契約**として維持する。将来改訂する際は明示的Version dispatch／migrationと旧Readerの回帰検証を必要とし、表示上のファイル改名だけで変更しない。

## 10. G05 Local row intermediate Artifact contract

### 10.1. Opt-in and compatibility

- 対象は一般権限Linuxユーザーがlocal ext4/XFS上で生成する個票中間成果物。実行者自身による明示的な出力指示であり、独立Approver・Ed25519署名・署名鍵Store・失効を求めない。従前の独立承認方式はOwnerの2026-11-21限定改訂により撤回。
- Studyは既存`e11-local-study/1`を保持。`privacy.row_export_requested=true`かつCLI `--allow-row-level-export`を必須とし、任意の`privacy.policy_ref`は現行unsigned modeではnullのみ受理（non-nullを承認として認めない）。
- `RESTRICTED_ROW_LEVEL`、対象Methodの`ApprovedRowSchema`、許可列順・row ID・dtype・max_rows・max_output_bytes・max_memory_bytesを照合。Method固有数値や列名を推測しない。
- 実行EUIDが所有するprivate TrustedRoot・同一local filesystem、root/staging 0700、row artifact 0600、実行UID/owner/mode/FS/symlink/dirfd安全性を実行時に確認。rootまたは同一UID processからの分離は保証しない。
- 初期拒否はexit3、Source iteration0、row bytes0、aggregateへ暗黙fallbackしない。認可後のprivate staging失敗は公開せず、過去の生成bytesが0だったと偽らない。

### 10.2. Authorized bounded Parquet and G01 publication

1. `LocalPrivacyPolicy.authorize(*,study,cli_row_flag,root,principal,output_shape)`でStudy、CLI、UID/root、Method出力適格性をAND検証し、`filter_export_columns`で列順を確定する。
2. Owner採用済み`RowEffectsParquetWriter.write(*,source,study,decision,selection,sink)`とFactory/Serializer/Deferred Source署名は維持。Source.schema()とMethod別RowSchemaを検査した後、両opt-inかつOS適格性を確認した時のみ`read_rows()`を反復し`max_rows+1`で超過を拒否。重複行ID/unknown columns/不正dtype/NaN/Inf/上限超過はfail closed。
3. `row_effects.parquet`、media type `application/vnd.apache.parquet`、classification `RESTRICTED_ROW_LEVEL`を既存G01 `StagingArtifactSink.stage_bytes`へ渡す。Writerが直接final runs/、Manifest、markerを発行することは禁止。G01 Publisherが唯一のatomic no-clobber authority、Readerが独立readbackを行う。
4. Stage/Seal/Publish前にroot/UID/FS identity/同一Sinkとinput hashを再検証。異常時にcommit markerなし。行値をResult/Manifest/status/CLI stdout・stderr・logに転記しない。

### 10.3. Independent acceptance

`IO-E11-06`：double opt-in正例とflag単独/Study単独/両false負例、wrong UID/root、owner/mode/symlink/dirfd/cross-filesystem、pre-authorization Source iteration0、row/byte/memory/column/schemaエラー、実ext4/XFSでのParquet読戻し、G01 fault injection/Marker/Readback/旧v2 regressionを必須とする。署名・鍵rotation/失効試験は対象外。実行証拠・Method別RowSchema/Parquet ABIは未確認であり、07/Gate999/Freeze/Coding AuthorizationをPASS扱いしない。
