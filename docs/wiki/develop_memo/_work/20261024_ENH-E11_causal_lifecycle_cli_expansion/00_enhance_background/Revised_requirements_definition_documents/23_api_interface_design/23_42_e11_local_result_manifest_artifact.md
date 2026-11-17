# 23_42_e11_local_result_manifest_artifact — E11 Local JSON / Parquet / Artifact Interface

## 1. 公開される契約と責務

E11 Local file bundleはProduct DBのResult/Artifact/Lineage Resourceではない。ファイルの作成者・参照者は同一local OS Principalと明示された委譲実行主体の範囲で責務を持つ。ProductのProjectMembership OWNER/EDITOR/VIEWERを、DB未接続のlocal CLIへ擬似適用しない。

公開ディレクトリは `ROOT/runs/{run_id}/` の一単位で不変とする。Readerは `manifest.json` と `_COMMITTED.json` を検証して初めてbundleを受け付け、個々のArtifactの存在だけを成功と解釈しない。公開Manifestは科学的結果の内容、Artifactは物理bytes、statusは実行事実を表す別権威である。

## 2. Local file layout（相対キー）

~~~text
ROOT/
  .staging/
    {random-staging-token}/
       result.json
       graph.json                  # graph operation時のみ
       diagnostics.json            # 対応Method時のみ
       row_effects.parquet         # 明示許可された時だけ
       manifest.json
       _COMMITTED.json
  runs/
    {run_id}/                      # 同一Filesystem内で一括rename公開
       result.json
       ... 
       manifest.json
       _COMMITTED.json
~~~

- `run_id`は安全な固定文法（ASCII英数、`-`、`_`、最大128文字、`.`・`..`・path separator禁止）を満たす。run IDはGraph/Question/Content IDを代用しない。
- Artifact keyはbundle rootからの相対POSIX path。絶対path、`..`、空component、prefix混同、symlink、hardlinkによるroot外参照を拒否する。Path validation後もOpen時のO_NOFOLLOW／dirfd相当の操作でraceを防ぐ。
- `.staging`は完成bundleでない。staging rootとfinal rootの同一デバイス／同一FileSystem／atomic directory rename可能性をpreflightで確認する。NFS/object-store/Windows/異FSで同等性を前提化しない。
- 同じ `run_id` の再実行は既存Manifest/request hashが一致し、readbackも成功する場合のみその結果を参照できる。異なるhashは `RUN_ID_CONFLICT`。上書き禁止。

## 3. Result JSON

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

**D03 G2採用の意味:** B0/B1でAR検定反転により得る信頼集合は、全ての実数を含む場合も、非連結や非有界の場合も単一区間とは限らない。Finite CI schemaへの丸め込み禁止。これはStatistical confidence setであり、D06のPartial Identification Setではない。

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
- 推論がUNAVAILABLE/FAILEDならconfidence_set=nullとreasonが必須。単なる `point_only` から合格区間を捏造しない。Monte Carlo coverageと弱IV頑健性は該当Gateの07独立科学検証で評価する。
- Intervalの端点条件やstrict inequalityの扱い、AR statistic/covariance/threshold/reference・数値探索精度はDDおよび該当Gateの07 Method別検証契約に属する。

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

## 7. PublishとReadback failure semantics

1. Output root自体のowner/permissions、同一FS、run_id未使用、承認済みprivacy policyを確認。
2. `.staging/{token}`を権限 `0700`、各通常fileを `0600` で生成し、Method adapterの**すべての出力先**をstaging配下に限定する。
3. 各Artifactをhash、schema、row-level leakage、method-specific semantics検査。Manifest/markerを作成し、ファイル・ディレクトリをfsyncする。
4. Publication直前にstaging bundleの全件readbackとReference integrityを検証。失敗すれば公開せずrollback。
5. 同一FS directory renameを唯一の可視化pointとして `runs/{run_id}` をpublish。親dir fsyncでdurabilityを補強。
6. Crash後のrecoveryは公開runのmarker検証を行い、未公開stagingは成功とせず隔離／管理者条件下のみ清掃する。rename直後の電源断時の耐久性はOS/FS保証範囲で判定。
7. Runはimmutabilityを保持。partial publicationをsuccess扱いせず、既存runを上書きしない。既存 `ArtifactStorePort.store/retrieve/exists/delete` ではこの複数fileトランザクションは保証しない。

出版のatomicityはディレクトリ単位のvisibilityであり、異Filesystemやネットワーク障害を越えるexactly-once保証ではない。Proofにはfault injectionとFS boundary testが必要。

## 8. Local privacy／distribution

- 個票を含む `row_effects.parquet` は `RESTRICTED_ROW_LEVEL`。通常出力では作らない。明示flag、Study policyの許可、OS principal・output root owner一致をすべて確認し、最小限のcolumnのみ保存。
- Local OS PrincipalはProduct ProjectMembershipを代替する認証ではない。共有端末/CI/コンテナの実効UID・umask・volume mountに応じたアクセス制御を別途検証する。stdout/stderr/log/exception traceに個票やsecretを出さない。
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

## 10. Publication Interface設計の未Freeze境界（PREP-02）

**ここでいうAtomicは同一local filesystem内の、読取可能な1 run directoryの可視化と不変性を指す。** 次の実装前Contractを厳密に区分する。

| Concern | REQUIRED semantic contract | 未確定・独立実証 |
| --- | --- | --- |
| no-clobber | 既存`runs/{run_id}`を上書きせず、同じrequest hash＋verified bundleのみ再使用 | POSIX plain renameの存在確認だけでは並行書込み競合を防げない。Linux no-replace primitive／exclusive lockを固定し、競合negativeを実測 |
| trusted relative key | run root配下にのみopen、各path componentでsymlink traversal防止 | O_NOFOLLOWのleafだけで中間symlinkは防げない。dirfd walk/secure openのSource・FS試験 |
| same-FS visibility | staging→runs一括切替、Marker・Manifest・全Artifacts検証 | NFS/object store/cross-device/Windowsには保証を拡大しない。File/dir fsyncとcrash recoveryの実FS evidence |
| manifest identity | Manifest自己hash禁止、MarkerがManifest bytes hashを参照し、MarkerはArtifact一覧から除外 | Canonical JSON encoding/version、Manifestのartifactリスト順序、入出力hashの最終JSON Schema |
| Result・AR topology | Effect point、Inference、Science statesを別軸とし、Infinityや非連結ARをタグ付き型で正規化 | Empty/invalid CI、unknown endpoint、Roundtrip、null reasonのSchema/Test |
| row Privacy | default no individual export、Spec policy ∧ CLI flag ∧ OS principal/permissionすべてを要求 | Shared mount/container root/delegation/ACLの認可、redaction、Parquet column negative |
| Legacy separation | E11 Local run marker+schemaと旧v2`CliManifest` readerを別dispatchし、旧データの意味を改変しない | v2 regression fixtures、unknown version/fallback negative |

**Status:** `DESIGN_CONTRACT_DRAFT / ADR_AND_JSON_SCHEMA_FREEZE_PENDING / FS_SECURITY_INDEPENDENT_TEST_NOT_RUN`。この表はOwnerの方法論/安全性承認範囲を狭めず、実装済みまたはPASSを意味しない。対応DD：`30_62`§4（Classの7区分）。対象Finding：BD01-F03/04/05/06/07/12。


## 11. DEC-PREP02 Owner-approved interface constraints (2026-11-17)

[Decision](../combined_review/decisions/94_20261117_dec_prep02_owner_architecture_choices.md): A/B/C all Option A **ADOPTED**. For IO-E11-01/02/03/06/08/09, normative initial support is non-delegated same-UID owner-controlled trusted root; restricted row export requires both Study authorization and explicit CLI opt-in; shared/CI/container-root/delegated accessible volumes denied until separately approved. Publish must use effective Linux same-FS atomic **no-replace** directory operation and fail closed when not supported. Version identifiers `e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1` are adopted; unknown/legacy v2 cannot be silently parsed as E11. §10's 'unfrozen' label now applies to **mechanical schema/signatures/FS proof**, not Owner's selected policy. `OWNER_POLICY_ADOPTED / JSON_SCHEMA_NOT_FROZEN / TESTS_NOT_RUN`.



## 12. F07 AR Confidence Set/Inference wire詳細規範（2026-11-17）

`e11-local-effect-result/1`の`uncertainty`内で`availability`・`kind`・`interval/confidence_set`・`reason`を独立に表す。Confidence Setの成分は`lower/upper`に`{"kind":"FINITE","value":...}` / `{"kind":"NEG_INFINITY"}` / `{"kind":"POS_INFINITY"}`を使用し、無限区間の端点の開閉を真偽値で表す。`ALL_REAL`、`DISCONNECTED`、`UNBOUNDED`、`BOUNDED`を`topology`で明示し、成分の完全な配列を保存する。`JSON Infinity/NaN`は禁止。`AR_CONFIDENCE_SET`には`inversion_evidence`のContentRefとconfidence levelが必要。正常な`AVAILABLE`と、`UNSUPPORTED/UNAVAILABLE/FAILED/NOT_REQUESTED`による推論不在は相互排他的であり、後者には理由コードを残す。`EffectOutcome.point`、`science_acceptance`、`technical_status`は推論可用性から独立。

機械可読な**内部$defsドラフト**：[e11_ar_inference_defs.schema.json](schema_drafts/e11_ar_inference_defs.schema.json)。[F07 review input](../combined_review/99_20261117_prep02_f07_ar_inference_schema_candidate.md)`2〜4をsemantic validation・positive/negative test条件として併用する。これは正式なE11 Result JSON Schema全体のFreezeではない。Interval unionの正規化や科学的CoverageはJSON Schema検証だけで確定できない。Method別推論とIndependent Reviewが残る。


## 13. F03/F05/F06出版・Privacy・Version整合（Freeze準備）

F03：`ValidatedStagedBundle`だけをLocal Publisherへ渡し、`renameat2(...RENAME_NOREPLACE)`で既存runを不変のまま保護する。発行後のfsync/readback失敗は、削除や再上書きをせず`PUBLICATION_INDETERMINATE`として扱う。詳細：[F03契約](../combined_review/104_20261117_prep02_f03_atomic_publish_contract.md)。

F05：default row-level Parquetなし。明示Study request ∧ CLI flag ∧ 別に証拠を持つ事前Study Policy ∧ private TrustedLocalRoot ∧ column/row制限が一致した場合のみ行出力。Unknown ACL/mount/namespaceは拒否。[F05契約](../combined_review/105_20261117_prep02_f05_trusted_root_privacy_contract.md)。

F06：5種類の採用済みVersion文字列と独立`e11-commit/1` markerを厳格dispatch。[F06契約](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)、[機械可読Schemaドラフト](schema_drafts/README.md)参照。例の`ContentRef`は5キー形式。旧`id/sha256`例・`path/sha256`例を新v1正規値として暗黙解釈しない。

F07：[DEC-PREP02-D](../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)で汎用ARの`EMPTY`をOwner採用。`arConfidenceSet.components=[]`は`topology=EMPTY`の場合に限り許可し、Effect schemaでも同条件を反映済み。**Science/Method別の妥当性と統計的Coverage、JSON Schema正式試験は未実施**。


## 14. Owner採用4事項とResult/Manifestとの同期（2026-11-17）

- F07: AR集合は`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`の5 topology。`EMPTY` iff components空。成功ARのinversion_evidence必須。古い4分類・一律EMPTY拒否は失効。[Owner決定](../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)。
- F05: Study `privacy.policy_ref`の提出は**未信頼**。別の事前承認Authorityと照合して`VerifiedStudyPolicyEvidence`ができた場合のみ個票出力を許可。Row拒否ではCLI exit3、暗黙のAggregate fallback禁止。
- F06: F06 codecの候補版`e11-json-jcs-rfc8785/1`をManifest `canonical_codec_version`に保存する設計案（[F06詳細](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)）。`request_hash`はTyped Studyのcanonical JSON bytes、`manifest_sha256`は保存Manifestの**実bytes**、ContentRefはFile実bytesのSHA256。全て異なるHashの対象であり混同しない。
- 形式・Reason/StatusはSchemaドラフトに同期済み。Method-specific科学的適格性、Policy trust anchor、Codec/FS/Schema正式試験は未完了。


## 15. Graph自己Digest・Operation別Bundle・科学的Stateの整合規則

Graph JSON内の`content_hash`をGraph JSON全体のSHA256と定義すると自己参照になるため、候補仕様は**`content_hash = SHA256(JCS(Graphからcontent_hashを除いた意味射影))`**とし、外側の`ContentRef.sha256`はGraph JSON実bytes全体を検証する。両者を照合し、一方だけでTrustedとしない。Result/Status/Manifest/Marker間のrun_id・request_hash・Method・Estimand一致は個別Schemaだけでは証明できない。[Cross-schema規範](../combined_review/114_20261117_prep02_f06_schema_semantic_invariants.md)を参照。

`DISCOVER/IDENTIFY`等の非Effect操作でEffect Resultをダミー生成しない。Manifestの`schema_dispatch.result`はOperationごとの実際のResult有無に応じnullを許すSchema候補とし、実効Bundle validatorが必須/禁止を判定する。実行時のOperation別DTO契約・strict Schema、数値科学・Privacy・FS受入は独立Review/各Gate検証が必要。
