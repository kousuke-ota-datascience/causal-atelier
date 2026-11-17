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
  "estimand": {"family": "LATE_COMPLIER", "population": "compliers", "contrast": "A1-A0"},
  "design_ref": {"id": "design-1", "sha256": "example-not-a-real-hash"},
  "question_ref": {"id": "question-1", "sha256": "example-not-a-real-hash"},
  "graph_ref": null,
  "identification": {"status": "IDENTIFIED", "proof_ref": "proof-1", "reasons": []},
  "point": {"availability": "AVAILABLE", "value": 0.5, "unit": "outcome", "reason": null},
  "uncertainty": {"availability": "NOT_REQUESTED", "kind": null, "confidence_level": null, "confidence_set": null, "reason": "not_requested"},
  "science_acceptance": {"state": "NOT_EVALUATED", "evidence_ref": null},
  "diagnostics": [],
  "method": {"id": "P3-M09", "backend": "native", "inference_method": null},
  "privacy": {"classification": "AGGREGATE", "row_level_export": false}
}
~~~

上記のexample hashは意図的に無効であり、実行入力としては受け付けない。examplesはSchema Testでsynthetic valid hashへ差し替える。

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
- `topology` は `ALL_REAL / DISCONNECTED / UNBOUNDED / BOUNDED`。優先順位はALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDEDとし、DISCONNECTEDには非有界componentが混在し得る。全実数は `topology=ALL_REAL; components=[(-∞,+∞)]` の一意表現。正常B0/B1ではEMPTYは有効な結果としてpublishしない。
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
| runtime | repo commit/dirty、Python/platform/CPU/BLAS threads、uv.lock hash、installed distribution/version、extras、actual API probes、SBOM ref |
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
