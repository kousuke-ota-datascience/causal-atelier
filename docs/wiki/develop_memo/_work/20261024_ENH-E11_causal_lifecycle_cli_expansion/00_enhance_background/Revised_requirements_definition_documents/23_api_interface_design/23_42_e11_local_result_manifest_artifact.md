# 23_42_e11_local_result_manifest_artifact — E11 Local JSON / Parquet / Artifact Interface

## 1. 公開される契約と責務

E11 Local file bundleはProduct DBのResult/Artifact/Lineage Resourceではない。ファイルの作成者・参照者は検証済みsame-UID、non-delegated OS Principalとprivate TrustedRootの範囲で責務を持つ。共有・委譲主体を無条件には許さない。ProductのProjectMembership OWNER/EDITOR/VIEWERを、DB未接続のlocal CLIへ擬似適用しない。

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

B0/B1でAR検定反転により得る信頼集合は、全ての実数を含む場合も、非連結や非有界の場合も単一区間とは限らない。Finite CI schemaへの丸め込み禁止。これはStatistical confidence setであり、D06のPartial Identification Setではない。

~~~json
{
  "kind": "ANDERSON_RUBIN_INVERSION",
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
  "inversion_evidence_ref": "artifact:ar-grid-and-brackets"
}
~~~

- 各endpointは `FINITE(value) / NEG_INFINITY / POS_INFINITY` のtagged union。JSONに `NaN / Infinity / -Infinity` numberを含めない。
- Componentは下界昇順・空でないintervalで、重複・接続する成分は数学的に和集合として正規化する。真のdisconnectedは成分数2以上。有限・無限端点のclosed flagは規定値に一致すること。
- `topology` は **`EMPTY / ALL_REAL / DISCONNECTED / UNBOUNDED / BOUNDED`**。優先順位はEMPTY（`components=[]`）→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDEDとし、DISCONNECTEDには非有界componentが混在し得る。全実数は `topology=ALL_REAL; components=[(-∞,+∞)]` の一意表現。**数学的EMPTYは汎用Codecで正常な推論結果として表現可能**。B0/B1のjust-identified MethodでEMPTYが科学的不整合ならMethod-specific validatorで拒否し、計算`FAILED`と混同しない。
- 推論がUNAVAILABLE/FAILEDならconfidence_set=nullとreasonが必須。単なる `point_only` から合格区間を捏造しない。Monte Carlo coverageと弱IV頑健性はMethod別の独立科学検証で評価する。
- Intervalの端点条件やstrict inequalityの扱い、AR statistic/covariance/threshold/reference・数値探索精度は30_61/30_63のMethod別検証契約に属する。

## 5. Graph／temporal evidenceの往復

Graph JSONは `e11-local-graph/1`。頂点ID、graph kind（DAG、CPDAG、PAG、必要なlatent/temporal variants）、edge endpoint pairs（tail/arrow/circle）、lag付き向き、time index policy、parent GraphVersion ID、assumption／edit rationale、source referenceとhashを保存する。Graph修正は元Graphを上書きせず新しいVersionとして発行する。

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
| runtime | repo commit/dirty、Python/platform/CPU/BLAS threads、uv.lock hash、installed distribution/version、extras、actual API probes、SBOM ref、**E11 canonical_codec_version** |
| stochastic | effective seed、stream derivation、split/partition hash、fold、Bootstrap config、retries |
| artifacts | canonical relative key、type、size bytes、sha256、privacy classification、visibility |
| review | method Reference／Science evidence refs（未実行ならnull）、legal delivery status別記 |

`_COMMITTED.json` は `{"marker_version":"e11-commit/1","run_id":"...","manifest_sha256":"...","request_hash":"..."}`。Manifestは自身のhashを含めず、markerがManifestのbytes hashを指す。Markerはartifact一覧の外側にあり循環hash参照を作らない。Readerは marker→Manifest→各Artifact hash/size/MediaType→cross-refを検証する。外部からの上流参照もtrusted root＋hashの範囲で再照合する。

Manifestに全source pathを生の絶対パスで記録せず、再現に必要な参照とdigest、非機微な環境要約を格納する。SBOMへの内部referenceは秘密やライセンス未承認状態を解除しない。個票Parquetをdefault summary／console／JSONに含めない。

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

- 個票を含む `row_effects.parquet` は `RESTRICTED_ROW_LEVEL`。通常出力では作らない。明示Study request、CLI flag、独立Authorityの事前承認`VerifiedStudyPolicyEvidence`、same-UID private TrustedRoot、許可column/max_rowsを全件検証する。
- Local OS PrincipalはProduct ProjectMembershipを代替する認証ではない。共有端末/CI/container-root-accessible mountと不明ACL/namespaceは別の信頼可能な契約がない限り拒否する。stdout/stderr/log/exception traceに個票やsecretを出さない。
- Customer delivery可否は科学的結果・内部実行の状態とは別。GPL系Backendを含む受領者別Bundleの法務レビュー未完は `CUSTOMER_DELIVERY_BLOCKED` として扱う。

## 9. IFテスト

| ID | Test | 失敗なら拒否する条件 |
|---|---|---|
| IO-E11-01 | Artifact key traversal / symlink / race | root外read/write、symlink attack |
| IO-E11-02 | Multi-artifact crash/fault injection | marker無し、hash mismatch、途中bundle |
| IO-E11-03 | Same run_id retry, content equivalence | request hash不一致で再利用 |
| IO-E11-04 | JSON AR topology round-trip | DISCONNECTED/ALL_REAL/無界endpoint喪失 |
| IO-E11-05 | Graph endpoint/lag/GraphVersion round-trip | circle消失、parent欠落 |
| IO-E11-06 | Restricted CATE Parquet/summary/CLI leakage | opt-in無しの個票公開 |
| IO-E11-07 | Backend/env/lock/SBOM readback | 適用不能Versionや不明依存の成功扱い |
| IO-E11-08 | immutable run／partial Manifest rejection | stale hashes、non-atomic backend |
| IO-E11-09 | Product v2 reader regression | legacy ManifestのE11誤解釈 |

参照：[E11 CLI/Port](23_41_e11_local_cli_scientific_ports.md)、[E11関連BD](../22_product_basic_design/22_09_results_artifacts_lineage.md)、[Existing Product Artifact Port](../30_detailed_design/30_50_persistence_artifacts.md)。

### AR・Privacyの意味的検証

AR集合は`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`の5分類。`EMPTY`は数学的に正常に反転した0成分で`AVAILABLE + inversion_evidence`と共存しうる一方、計算失敗は`FAILED + reason`。端点で双方openの接触区間はgapを保存する。非退化なB0/B1 HC1 ARの非空条件はMethod固有Validatorで判定し、CodecやSchemaの検証を統計的Coverageの証明としない。

行出力に対する独立Policy trust anchorはStudy YAMLの自己宣言と区別し、権限不足なら個票を生成せずexit3。出版前の検証だけでなく、ReaderもMarker/Manifest/Filesの実bytes・size/type、private Artifactの権限とLineageを再検証する。
