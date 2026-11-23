# 22_09_results_artifacts_lineage


---

## 12. Result / Artifact / Lineage

### 12.1 Canonical Resultとcompatibility read model

現行のcanonical `Result` authorityは、`execution_id / result_level / stage_execution_id / result_type / scientific_status / summary / payload / diagnostics / warnings`を持つ。ProjectとAnalysis Familyは親Executionから解決する。

同時に、過去のFamily workflowを読むための`FamilyResult` compatibility read modelが残っており、こちらは`project_id / analysis_family / schema_version / analytical_status`を持つ。新規write authorityはcanonical Resultに寄せ、両者を同一entityとして扱わない。

Navigation StageをResult ownership keyとして必須化しない。

### 12.2 Artifact

Canonical Artifactは`SOURCE`または`EXECUTION_OUTPUT` scopeを持ち、`object_key / content_hash / media_type / size_bytes`でArtifactStore上のcontentを参照する。Artifact readでは保存済み`content_hash`と取得contentのSHA-256を照合する。

Predictive等のhistorical Family read modelとして`FamilyArtifact`が残るが、新規canonical Artifact ownershipと区別する。

### 12.3 Lineage

Lineageには2つの表現層がある。

1. canonical/generic authority: `LineageEdge(ResourceRef -> ResourceRef)`およびtyped structural relation。
2. Result起点read projection: Project / Dataset / Execution / Result / GraphVersion / Artifact / Annotationをtraverseし、表示用relation名へ変換する。

表示用`CONTEXT_FOR / SOURCE_OF / INPUT_TO / HAS_ARTIFACT / HAS_ANNOTATION`等と、generic authoritative relation typeを同一のwrite contractにしない。

Navigation Stageをpersistent lineage resourceとして追加しない。

Current lineage read modelは`ResearchContextVersion -> AnalysisSpecification -> ExecutionPlan -> Execution -> StageExecution -> Result -> Artifact`を最低chainとし、DatasetVersion / AnalysisView / GraphVersion / input Result / base Executionを接続する。FK/snapshotからdeterministically導出できるstructural relationをgeneric LineageEdgeへ二重persistせず、`MOTIVATED`等のsemantic relationだけをgeneric edgeとして保持する。

Exploratory ResultからAnalysisSpecification DRAFTへのhandoffは`Result --MOTIVATED--> AnalysisSpecification`を明示保存する。



### 12.4. ProductとLocal Artifactの正本境界

| Aspect | Existing Product (unchanged) | ENH-E11 Local (added) |
|---|---|---|
| Identity | Project/Execution/StageExecution/Result/ArtifactのDB正本 | content-addressed local Question/Design/Graph/Dataset/Run/Result参照（論理仕様） |
| Persistent location | Product Metadata DB＋ArtifactStore | Local JSON/Parquet/Manifest (Filesystem-based) |
| Authority | Product Domain/Application/Worker | Local Scientific Domain/Application＋Artifact Publisher |
| Scientific status | Product schemaと既存Review/Override | E11 typed outcome（point/inference/science独立） |
| Lineage | Product FK/LineageEdge/projection | Manifestでlocal refs/hashes/effective environmentを辿る |
| Cross-lane migration | 旧readerは旧仕様を読む | E11へ旧v2 Manifestを暗黙変換しない。双方向自動同期しない |

Domainは現行Productの`ArtifactStorePort`と設計概念を再利用できるが、Local ArtifactをProduct `Artifact`行に自動登録してはならない。Portの共有可否は既存Repoの実装調査によりDDで決める。

### 12.5. Local Scientific Resultと推論の意味

- **Identity and provenance:** Study identity、Question/Design/Estimand、Data snapshot、GraphVersion、Identification/Estimator specification、parent run、Method、effective backend/API、runtime。
- **Typed effect:** point estimate availability/value、target population/contrast、diagnostics、Identification result、scientific status／review reasons。
- **Typed inference:** `not requested`／`supported and valid`／`unsupported`／`calculation failed`／`scientifically ineligible`を区別。区間の存在と科学的受入は同義でない。
- **AR confidence set:** disjoint component intervals、非有界端点、全実数、confidence level、assumption・method/Referenceを損失なくserializeする。JSONにInfinityを裸数値として書くか否かなどのwire仕様はIF-01へ委譲する。
- **Data minimization:** aggregate summaryとrow-level CATE/individual local explanationを別Artifact classificationとし、制御応答・Manifestに個票を暗黙埋込しない。

### 12.6. Local ArtifactとManifestの公開手順

1. CLI/Applicationが入力・上流hash・実効Environmentを検証し、局所出力候補をPlanする。
2. Publisherが指定Root配下の安全な`relative artifact keys`へstagingし、出力内容のchecksumを計算する。Traversal／symlink／外部Pathを拒否する。
3. JSON/Parquet/Manifestの型とSource SHA、Effective Method/Environment/seed/split、Scientific Status、Artifact refs、サイズ/checksumを照合する。
4. Staged contentをreadbackし、byte identity・hash・link整合性を確認。**失敗なら正常Run Manifestを公開しない**。
5. Success/科学的negativeが適切な状態で揃った場合のみ、publish上のcommit marker／complete manifestを外部から認識可能にする。部分書込を完全成功と見せない。
6. 再試行は同一入力identityと実効seed/Backend条件で比較し、既存正本の内容差異は競合として扱う。変更があれば新Run/versionへ明示移行する。

**Atomicity caveat:** 複数ファイルの移動が単一OS操作で原子的になる保証はない。実装では同一Filesystemのrename/transaction-like marker等の方式とcrash-recovery/readbackをIF/DDでFreezeし、原子的publishの意味（可視状態の判定単位）をテストする。技術失敗後のstaging残骸を正本と認識させない。

### 12.7. 再現可能性とRun Manifestの要求

| Group | Information required |
|---|---|
| Source identity | input dataset hashes、Question/Design/Graph refs、Method/Estimand、Config/Schema Version、Git/source SHA |
| Effective environment | Python patch、OS/arch/CPU、Backend/distribution API/version、lock/pyproject hash、Native ABI/BLAS/thread info、selected Extras/Profile |
| Reproducibility | effective parameter、seed derivation/role、split/fold、upstream-run refs、analysis mode |
| Result validity | identification/eligibility status、point/CI availability、Science status、negative reasons、limiting assumptions |
| Artifacts | relative keys、media type、size、output checksum、readback/complete status、privacy classification |

Manifestは科学的根拠と実行条件の来歴であり、実行結果のbitwise再現や科学的有効性を保証した宣言ではない。SBOM／License provenanceは法務Gateへ独立Traceする。

詳細なJSON/Parquet field、commit marker、Path safety・multi-file crash recoveryはIF/DDで規定する。

**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-020a`**：Artifact storageを`ArtifactStore` Port abstraction越しに利用する


### Local publish privacy decision authority boundary

In the local run path the Application authorizes the *declared output capability* once before staging, and passes the immutable run/hash/root/UID-bound decision into the **single run-scoped Publisher**. The Publisher is the final pre-publication authority: it reopens the staged Study, matches the JCS request hash, current verified root/principal and complete real artifact inventory, and independently re-evaluates privacy policy. The declared aggregate-only G01 output class includes approved Graph or scientifically justified diagnostics without advance knowledge of eventual artifact hashes; an extra row/Parquet/Result artifact never fits. Missing/denied/stale or cross-run/root decisions are rejected **before** sealing/rename; publish rechecks the sealed identity and the independent Reader verifies the final run. This requirement refines existing atomic publication and Local/ Product boundary but adds no separate persistent Policy service.


### Local Manifest pure versus verified publication boundary (G01)

P01 constructs a pure immutable versioned Manifest from validated Study/Status and staged descriptor values; it computes strict Study JCS request hash and checks run/Method/scientific axes, output Graph Ref versus bundle-relative artifact descriptor, privacy and exact operation-specific inventory. It does not read actual files or claim physical hash authenticity. P02 safely stages and verifies actual descriptor bytes; P05 checks provenance and cross-file Study/Status/Graph contents; independent Reader reopens committed Marker/Manifest/artifacts. Graph semantic content hash differs from actual graph.json file-byte SHA. A staged technical_status=COMPLETED is only a candidate, not externally successful publication before Reader. No Product v2 reader or schema migration is implied.


### Publisher final authority versus decision issuance provenance

The local CLI does **not** authenticate which process instantiated an immutable `PrivacyDecision`; this value is an untrusted assertion until checked. The same field values on a fresh immutable instance have the same meaning as on the originally returned instance. A Publisher independently executes its **trusted injected** stateless policy on the live Study, verified root/effective principal and actual staged artifact inventory, compares all fields and requires `allowed=true`. The decision value never overrides policy and neither caller-controlled policy replacement nor missing runtime verification is permitted. G01 row/Parquet publication remains prohibited.


### Local DISCOVER negative diagnostic responsibility

For a valid G01 DISCOVER scientific-negative, the P04 science producer must actually justify the non-admissible PAG outcome; the P05 integration stage produces the **internal** typed diagnostic and Status with the same reserved reason; the P02 Publisher validates its real staged bytes and cross-file consistency before seal and the independent Reader checks after publication. A stored digest and inventory entry alone do not prove a meaningful diagnostic. This requirement does not modify Product v2, add a public schema, or permit scientific failures to be treated as completed negative results.
