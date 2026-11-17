# Ariadne ENH-E11 / G01 — 06 実装指示書

**Contract status: DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED**  
**Gate ID: G01 (Enhance Workflow Gate)**  
**Execution Mode: WORK_PACKAGE / Required packages: P01,P02,P03,P04,P05**  
**対象Gate：G01（Local Question/Design/Graph＋P1-M06 FCI/PAG）**  
**基準：`prototype/ariadne_mvp` の本書・07と共通契約の同一Commitを、後続のCoding Entryで固定する。**  
**根拠：** [PREP-02 Common Design Baseline](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[Requirement 10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md)／[DD 30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)・[30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_e11_local_execution_publication.md)・[30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_e11_method_adapters.md)／[IF 23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)・[23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)／[G01 07](07_Ariadne_ENH-E11_G01_test_instruction.md)。

## 0. Gate ID / execution contract authority

`G01`は正式Gate IDでありWorkstream番号ではない。`06`はCoding Contract、`07`はVerification Contract、`999`は独立Gate Decisionである。P00は計画、P01〜P05はCoding Work Package。Package完了はGate PASSではない。

**重要な再審査:** Domain/Graph/FCI ScienceとOS/FS Publicationが一つのGateであることは未証明。この06はDRAFTであり、Coding Authorization前にGate分割の適否・owner承認・06/07 Freezeが必要。Candidate Assemblyは全Package checkpoint→Gate-wide regression→Fixed Trial Candidate SHA→20系Completion ReportでREADY_FOR_TESTとし、30系独立999が最終判定する。

## 1. Coding Agentの責務と実装境界

この06は**Coding Authorizationの対象とする契約**であり、本書のコミットだけではコード変更を開始しない。OwnerがG01 Coding Entryを承認した後、Coding Agentは以下の五つのWPを順番に実装し、07の自動テストを作る。Gate PASS／科学的PASSの自己宣言は禁止。

**対象：** UC-01、`P1-M06`、Local causal context／GraphVersion／FCI/PAG fidelity、最低限の新Local CLI・安全なArtifact Publication・Reader・JCS・Manifest。G02以降のための共通基盤はG01で共通の入口Adapterを一度だけ作り、各Gateで複製しない。

**対象外：** `P1-M01〜05, P1-M07〜20, P2-*, P3-*`の科学的Method実装（既存Productとの互換回帰は例外）。PAGからの自動識別・効果推定、Temporal PCMCI（G06）、個票CATE／署名付き行認可（G05）、AR推論（G08）、Web/API/Worker/DB、Product migration、正本`docs/wiki/requirement_definition/`、配布・顧客利用判断。

**現行Source照合：** `src/ariadne/causal/discovery/algorithms.py`の`run_pc`はPC専用でありFCI実装ではない。`src/ariadne/causal/discovery/graph.py`はlossless endpointをCSVに正規化できるがE11 GraphVersionの新しいwriterではない。`src/ariadne/interfaces/cli/discovery.py`と`src/ariadne/interfaces/cli/manifest.py`はProduct v2 CLIであり書換禁止。`tests/product/test_cli_contract.py`は回帰必須。`pyproject.toml`はPython`>=3.12,<3.13`、`uv.lock`は`causal-learn 0.1.4.8`を含む。E11新CLI scriptを追加する場合だけ[project.scripts]変更可、既存登録は保持する。

## 2. ディレクトリ・Port・開発順序

```text
src/ariadne/
  shared/content_ref.py                # ContentRef; bytes identity, not Product ResourceRef
  shared/serialization/jcs.py         # strict JCS canonical codec
  causal/discovery/graph_evidence.py   # GraphEvidence; no GraphVersion writer
  causal/design/schemas.py            # reuse existing CausalDesign
  scientific/ports/causal.py           # Identification/Estimator/Diagnostic Ports
  scientific/ports/capability.py       # MethodCapabilityPort
  scientific/capabilities.py           # BackendCapabilityRecord
  scientific/causal_methods/fci.py     # P1-M06 adapter; lazy backend import
  capabilities/causal/local_execution.py  # LocalCausalUseCase
  capabilities/causal/method_registry.py   # MethodCapabilityRegistry
  interfaces/cli/local_causal/
    study.py           # LocalStudySpec; CLI envelope
    config_decoder.py  # LocalConfigDecoder
    content_io.py      # ContentReferencePort; TrustedRoot
    command.py         # ariadne-causal-local entrypoint
    publication.py     # TrustedRoot/staging/no-replace
    manifest.py        # LocalRunManifest value
    privacy.py         # LocalPrivacyPolicy
    manifest_reader.py # Reader/verification
 tests/enhancement/enh_e11/g01/
    unit/
    component/
    integration/
    scientific/
```

Where these paths conflict with an already implemented eligible shared abstraction, reuse by explicit adapter rather than copy-paste; modules named above are the selected design destinations; no parallel causal.local_contract tree. Public Port signatures are those in [112 Cross-Port](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/112_20261117_prep02_f03_f07_shared_port_signature_contract.md), including keyword-only`sink` and `ValidatedStudy` constructed in CLI composition root. No return of live external model/library objects across Ports.

| WP | 30系詳細設計 / DD検証ID | Class.Methodの実装操作 | 07テスト |
| --- | --- | --- | --- |
| **G01-P01** | 30_60 §11/12：REF01〜04・SPEC01〜04；30_61 §1：GRAPH01/03/04（CLI Decoder=30_60 §9）；30_62 `5.1：MAN01/02 | `ContentRef.from_payload`、`LocalConfigDecoder.decode`、`GraphEvidence.from_canonical_json`、`LocalRunManifest.to_canonical_bytes`。Strict Study/Question/Design/Method Config/JCS | G01-07-01〜04 |
| **G01-P02** | 30_62 `4/5.2：PUB01〜09、READ01〜07、PRIV03/04/06 | `ContentReferencePort.verify`、`LocalPublicationPort.begin/seal/publish`→`LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`、`LocalManifestReader.read_run` | G01-07-02/05/06 |
| **G01-P03** | 30_61 `1：GRAPH01/03/04；30_62 `5：MAN03/04 | `GraphEvidence.canonical_payload`（Product GraphVersionServiceがrevisionを所有）、PAG端点・親子関係・Graph二種類のHash。CLIのGraph editは対象外 | G01-07-03/07 |
| **G01-P04** | 30_62 `3：CAP01/04/05；30_63 `2/4.4：METH-P106 | `MethodCapabilityRegistry.describe/resolve/load_adapter`、`FciDiscoveryAdapter.preflight/execute`、CI test/BK・PAG独立Graph Oracle | G01-07-08〜10 |
| **G01-P05** | 30_62 `2/6/7：RUN01/03/04/06/07、PRIV01〜06、PUB10、MAN04〜06、READ06 | `LocalCausalUseCase.preflight/run`、`LocalPrivacyPolicy.assert_export_allowed`、`command.main`、DISCOVER-only Bundle、Exit・v2回帰 | G01-07-07/11/12 |

**実装順：** P01 → P02+P03 → P04 → P05。WP単位でunit/componentをGreenにし、最後にreal FS・CLIとGraph Scienceを結合する。中断時は現在WP・変更ファイル・テスト実行結果を短く記録するだけでよい。


### 2.1 Class.Methodによる正規の実装契約（06↔詳細設計↔07）

正本となる詳細設計：[30_61 Domain/Port `1〜5](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md)、[30_62 UseCase/Publisher/Reader/Privacy `2〜7](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_e11_local_execution_publication.md)、[30_63 Method `2/`6.3](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_e11_method_adapters.md)。以下は**詳細設計から抽出したG01用メソッド単位の義務**。06側で独立した設計正本を増やさない。

| Class.Method / DD検証ID | Precondition・必須動作（06） | Postcondition／失敗 | 07 |
|---|---|---|---|
| 30_60 `11 `ContentRef.from_payload` / 30_60 `10 `ContentReferencePort.verify` / REF01〜04 | 5 field strict。TrustedRootのdirfd・file FDでactual bytes/SHA確認。Path文法だけで安全宣言しない | mismatch/TOCTOU/symlink/同一identity別bytesは許可しない | 01/02 |
| 30_60 `9 `LocalConfigDecoder.decode(raw,declared_format)` / SPEC01〜04 | version・Operation・Method・Question/Design Profile・Method Configを検証し`ValidatedStudy`を作る（`decode_yaml`はprivate helper） | Product v2/unknown/CONFIRMATORY/不適格をexit2で拒否 | 01/08/11 |
| 30_61 `1 `GraphEvidence.from_canonical_json/canonical_payload` / GRAPH01/03/04 | endpoint・lag・node/parent不変、Graph semantic hashとFile hashを別検証 | lossless PAG、旧Graph不変。PAG→DAG、偽version編集拒否 | 03/04/07 |
| 30_62 `2 `LocalCausalUseCase.preflight/run` / RUN01/03/04/06/07 | `preflight`は実File/CI/静的capabilityのみ。`run`は`DISCOVER+P1-M06`だけ実行 | check-onlyはFit0回・publish0件。run完了はverified Reader必須 | 01/07/11/12 |
| 30_62 `3 `MethodCapabilityRegistry.describe/resolve/load_adapter` / CAP01/04/05 | P1-M06 metadata検証、実効Distribution/API検査。`load_adapter`だけが科学Engine import | 未対応Method/Backend/versionはtyped unavailable、fallback無し | 08/12 |
| 30_63 `4.4 `FciDiscoveryAdapter.preflight/execute(request,*,sink)` / DD-E11-METH-P106 | CI適格性・BK矛盾・Backend Node/Endpoint対応を検証、StagingSink以外に出力しない | 有効PAGまたはtyped unavailable、engine errorはexit4。独立Science Oracle別 | 08/09/10 |
| 30_62 `4 `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort` / PUB01〜10 | Public`LocalPublicationPort.begin/seal/publish`がper-run Concreteを使用。0600/0700・no-clobber・files/dirs fsync | Sealed後write禁止。rename後不定は`PUBLICATION_INDETERMINATE`、既存run削除/上書き禁止 | 02/05/06/11/12 |
| 30_62 `5.1/5.3 `LocalRunManifest.from_run_evidence/validate_invariants/to_canonical_bytes/from_payload` / MAN01〜06 | G01はStudy/Status/(optional Graph)の実bytesとlineage、Version/Codecを検査。`result=null`、MarkerはInventory外 | Manifest self-hash禁止、型付き負結果はScience PASS偽装なし | 04/06/07/12 |
| 30_62 `5.2/5.3 `LocalManifestReader.read_run(root:TrustedLocalRoot,run_id:RunId)` / READ01〜07 | Public`LocalManifestReaderPort.verify`からAdapter委譲。Marker→Manifest→Artifacts・Privacy→cross-ref確認 | validな`VerifiedLocalRun`だけ返す。保存破損はexit5 | 05/06/11/12 |
| 30_62 `6/6.8 `LocalPrivacyPolicy.assert_export_allowed` / PRIV01〜06 | Study行要求・CLI flagのいずれかでG01はexit3。Root private owner/ACL/mountとログを確認 | Row bytes=0、aggregate-only。`filter_export_columns`と署名認可はG05 | 02/11 |
| 30_62 `7 `interfaces.cli.local_causal.command.main` / RUN06/PUB10/MAN06/READ06 | 新`ariadne-causal-local`のみを追加、v2 CLIの入出力・manifestは変更しない | E11 versionと旧v2別namespace、回帰不変 | 01/11/12 |

**G01非適用の扱い：** 30_61 GRAPH02→G06、ID01〜04→G02以降、AR01〜05→G08、Effect推定本体→G03以降。30_62 RUN02/05の**Identification連携**→G02（Graph Evidence純粋なround-tripだけG01（Version編集は既存Product authority））、CAP02/03の全環境Profile→G10、CAP06の顧客配布Legal→別審査、PRIV07の署名付き行認可/列最小化→G05。未実装対象をG01でPASS扱いしない。

### 2.2 Method不変条件の実装順序（曖昧性防止）

1. `ContentRef.from_payload → LocalConfigDecoder.decode`：入力のVersion/Schema/Methodを検証した後、同一Rootのfile bytes/lineageをverifyする。`ValidatedStudy`を経由せずApplicationを呼び出さない。
2. `LocalCausalUseCase.preflight`：実行前にStudy/Question/Design/CI Eligibilityと安全なRootを調べるが、Fit・Staging・Manifest書込なし（07-11）。`run`はFCIが返すGraphとScience結果の型を維持。
3. `FciDiscoveryAdapter.execute`：Dataset列順↔Backend node IDを検査。source/target順を換えればmarkも同時swap。曖昧なPAG endpointの方向を創作しない（07-03/09/10）。
4. `LocalArtifactPublisher`：`begin→stage_bytes→validate(seal)→commit`が唯一の書込経路。`renameat2(RENAME_NOREPLACE)`と両parent sync＋独立Reader readback後だけCOMPLETED。abortはrename**前**だけ、結果不定時の削除/repair禁止（07-05/06）。
5. `LocalRunManifest/Reader`：DISCOVERではEffect Resultを作らず、`manifest.schema_dispatch.result=null`。実ファイルBytes HashとGraph意味Hashを区別し、StatusのScience NOT_EVALUATEDを誤ってPASSに変更しない（07-04/06/07）。

## 3. G01専用の入力契約

**New CLI：** `ariadne-causal-local --config STUDY.yaml --output-root ROOT [--check-only] [--json] [--allow-row-level-export]`。G01は`DISCOVER`、`method.id=P1-M06`、`method.backend=causal-learn`のみを実行可能とする。他Method/Operationは未対応の型付き拒否（不正構造=exit2、Backend unavailable=exit4）であり、他Methodで代替しない。

- Study `schema_version=e11-local-study/1`、`operation=DISCOVER`、`analysis_mode=EXPLORATORY`。CONFIRMATORYは、FCI Graphを効果推定の確定証拠と扱わないためG01では`METHOD_COMBINATION_UNSUPPORTED`（exit2）。
- Required `inputs.question/design/dataset`は既存のE11 ContentRef 5 field。G01 DISCOVERの`inputs.graph=null`・`inputs.identification=null`（未作成Graphを入力に要求しない）。Question/Designはsemantic validationの対象で、実際のbytes hashを再計算する。OutputGraphは別run artifact。Datasetは`text/csv`または`application/vnd.apache.parquet`。列順と名前の一意性、データ行の順序を保持。
- G01専用の[Question入力JSONプロファイル](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_question_profile_v1.schema.json)と[Design入力JSONプロファイル](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json)を厳格検証する。両者は**G01内部のMethod別入力バリデーション**であり、Owner採用済み5つの公開payload versionを増やすものではない。`ContentRef.schema_version=null`で参照し、`question.question_id=design.question_id=Study.inputs.question.identity`および`design.variables[].name`とDataset列名/列順の完全一致を必須とする。`design.assumptions`は研究者の事前宣言であり、Markov/faithfulness/acyclicityの成立証明ではない。`design.background_knowledge`と`Study.method.config.background_knowledge`はJCS同値であることを求め、勝手に条件を差し替えない。`fisherz`の場合すべての`measurement_scale=CONTINUOUS`、`chisq/gsq`はすべて`CATEGORICAL`。混合型はG01では`METHOD_COMBINATION_UNSUPPORTED`で拒否し、勝手な変換をしない。GraphVersionの初版生成はCLI `DISCOVER`で行い、編集操作はG01のDomain factory / component検証まで（新CLI editサブコマンドは追加しない）。
- 現行共通Study schemaは`estimand`必須なので、G01では`family=GRAPH_STRUCTURE`、`population=OBSERVED_VARIABLES`、`contrast=NOT_APPLICABLE`を**Discovery-onlyの非効果Target**として使用する。ATE等のDummy Effectを作らない。 `inference.requested=false`, `confidence_level=null`, `privacy.classification=AGGREGATE`, `row_export_requested=false`, `policy_ref=null`。違反時は明示的に拒否。
- `Study.method.config`は[FCI専用JSON Schema](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_method_config_v1.schema.json)をMethod registryが選択して厳格検証。**Method configの未知Fieldと別Method用Fieldは拒否**。全Fieldを明示させ、Backend既定値への依存を禁止。
- `indep_test`は`fisherz`（complete continuous numeric、非定数、検定のGaussian条件を記録）、`chisq/gsq`（事前に整数カテゴリ符号化・有効カテゴリsupport確認）の3方式。自動quantile binning、勝手な欠測補完、未申告の標準化は禁止。`alpha∈(0,1)`、`depth/max_path_length`は`-1`または0以上の整数、`background_knowledge`は`null`またはrequired/forbidden ordered pairs。 `show_progress=false,verbose=false`はCLI Adapter固定。
- Validated root内で`openat`/dirfd・`O_NOFOLLOW`等を使い、file descriptor実bytes hash・媒体型・regular file・owner/permissions/FS/mountを検査する。Path lexical checkだけでは十分でない。サポートしないFSやprivilege/mountなら**fail-closed**。
- `--check-only`では科学計算・staging・manifestを書かない。厳格構造・安全な入力参照・Method・CI-test/Design前提・静的capabilityを検査し、Scientific Graph AccuracyをPASS扱いしない。検査だけでPython optional scientific engineのimport/大量計算を行わない。

**G01用Studyの値イメージ（SHA/Ref実値はテストfixtureで生成）：**
```yaml
schema_version: e11-local-study/1
operation: DISCOVER
run_id: g01_fci_case1
analysis_mode: EXPLORATORY
inputs:
  question: {identity: q1, relative_key: inputs/question.json, sha256: "<actual lowercase 64hex>", media_type: application/json, schema_version: null}
  design: {identity: d1, relative_key: inputs/design.json, sha256: "<actual lowercase 64hex>", media_type: application/json, schema_version: null}
  dataset: {identity: data1, relative_key: inputs/data.csv, sha256: "<actual lowercase 64hex>", media_type: text/csv, schema_version: null}
  graph: null
  identification: null
estimand: {family: GRAPH_STRUCTURE, population: OBSERVED_VARIABLES, contrast: NOT_APPLICABLE}
method:
  id: P1-M06
  backend: causal-learn
  config: {indep_test: fisherz, alpha: 0.05, depth: -1, max_path_length: -1, background_knowledge: null}
inference: {requested: false, confidence_level: null}
randomness: {seed: 1711}
privacy: {classification: AGGREGATE, row_export_requested: false, policy_ref: null}
```
**注：** 上記`<actual...>`はliteral placeholderでありそのままの入力はINVALID。QA fixture生成で実ファイルのSHA256へ置換する。Question/Design JSONのG01 domain validationは既存の文書意味（研究問い、変数、制約）を保ち、source file hashだけを妥当性証拠としない。

**Question/Design入力ファイルの最小例（説明用、hashは実ファイルから取得）：**
```json
{"question_id":"q1","research_question":"観測変数間の条件付き独立性構造を探索する","population":"sampled units","analysis_goal":"GRAPH_STRUCTURE"}
```
```json
{"design_id":"d1","question_id":"q1","design_kind":"OBSERVATIONAL_GRAPH_DISCOVERY",
 "variables":[{"name":"x","measurement_scale":"CONTINUOUS"},{"name":"y","measurement_scale":"CONTINUOUS"},{"name":"z","measurement_scale":"CONTINUOUS"}],
 "assumptions":{"causal_markov_declared":true,"faithfulness_declared":true,"acyclicity_declared":true,"latent_confounding_possible":true,"sampling_unit":"one independent row"},
 "background_knowledge":null}
```
実行時は厳格JSONだけを許し、Design変数名の重複・列漏れ・順序違い・Question/DesignのID不一致を拒否。科学的仮定が真である保証にはしない。

## 4. FCI Backend・Graph変換（科学的に誤った方向付けをしない）

**実装候補/照合先：** `causallearn.search.ConstraintBased.FCI.fci`、`(GeneralGraph, edges)`の返却。FCIのAPIは`fci(data, independence_test_method, alpha, depth, max_path_length, verbose, background_knowledge, show_progress, ...)`相当。実際に導入された`0.1.4.8`の**import・inspect.signature・Graph edge accessor**を同一環境で確認し、異なれば`BACKEND_API_MISMATCH`としてexit4（引数やモデル構造の推測による黙示代替は禁止）。[公式FCI説明](https://causal-learn.readthedocs.io/en/latest/search_methods_index/Constraint-based%20causal%20discovery%20methods/FCI.html)。

- Node ordering: 学習入力の列名/順序→Backendの内部Node識別子の対応を明示的に検査。Backendが`X1`等を返す場合も無検証の文字列置換は禁止。対応不能なら`BACKEND_GRAPH_NODE_MISMATCH`。Graph `nodes`は入力観測変数のみを許す。
- Endpoint pair: Backend `edge.get_endpoint1/2()`と`edge.get_node1/2()`を**同じ端点位置**でマップし、`TAIL/ARROW/CIRCLE`のペアをlossless保持。無向ペアはnode名の安定順に並べ、順序反転した場合はmarkも入替。重複edge・Self-loop・未知mark・missing nodesを拒否する。`ARROW/ARROW`は双方向**endpoint**であり二本の有向因果効果ではない。PAGからDAGを合成しない。
- `e11-local-graph/1`: `kind=PAG`、`temporal=null`、全G01 `edges[].lag=null`、`version_id`は不変、初版`parent_version_id=null`。Graph `content_hash=SHA256(JCS(Graph without content_hash))`、外部`ContentRef.sha256=SHA256(actual complete graph.json bytes)`。Graph `provenance`にeffective Backend, CI-test, alpha, n, columns, runtime/library version, Graph uncertainty, permitted background knowledge, reasonsを残す。Backend固有edge propertyの取りこぼしは科学的意味を確認し、必要なら`provenance`内でキー付きに保存する。
- GRAPH-A: 生成DAGを唯一のPAG oracleとして用いない。潜在変数を含む小Graphから観測MAG・同値類の制約を**独立に**導出し、強制されない方向は未確定のまま評価する。PAGのどの円端点も「潜在交絡が証明された」という意味ではない。
- BackgroundKnowledge: `required_edges`／`forbidden_edges`は変数の存在、矛盾、自己辺、cycle/precedenceの妥当性を検査。Backend内部のBK適用には**禁止方向から不要なTAILを確定させる可能性**が報告されている（[上流#266](https://github.com/py-why/causal-learn/issues/266)）。G01ではBK指定時に独立Graph motifのendpoint非過剰確定RegressionがGreenとなるまで`BACKEND_SEMANTICS_UNVERIFIED`で拒否し、結果をPAGとしてPublishしない。修正が必要ならG01内のversioned adapterに限定し、外部ライブラリの無断Patch/依存更新はしない。

## 5. G01 Operation別Bundle・状態・Publication

**成功時の最小相対ファイル（すべてROOT以下）：**
```text
ROOT/runs/{run_id}/
  study.json           # Validated typed Studyのcanonical bytes
  graph.json           # 有効なPAGだけ。構造失敗時は作らない
  status.json          # e11-local-status/1
  manifest.json        # e11-local-manifest/1
  _COMMITTED.json      # e11-commit/1; Manifest inventory外
```

- Manifest `schema_dispatch.study=e11-local-study/1`, `graph=e11-local-graph/1`（Graphが生成できた場合、そうでなければnull）、`result=null`（**Dummy Effect禁止**）、`status=e11-local-status/1`。Manifest artifactsには実際に生成したstudy/status/graphの`key,sha256,size_bytes,media_type,privacy_class,visibility`を列挙。`manifest.json`とmarkerはInventoryに入れない。
- `status.json`は`technical_status=COMPLETED`でも`identification_status=NOT_APPLICABLE`,`point_availability=NOT_REQUESTED`,`inference_availability=NOT_REQUESTED`、`science_acceptance=NOT_EVALUATED`を基本とする。G01テストで独立Science判定するまでは`PASS`不可。科学的に負の有効結果（例: CI不適格でMethodが構造判定を保留）を技術完了とする場合は明示reasons／graph=nullを許す。ただし実行例外やBackend unavailableは成功Bundleへ偽装しない。
- Manifest/Markerは固定のHash連鎖：`request_hash=SHA256(JCS(typed Study))`、`manifest_sha256=SHA256(actual manifest.json bytes)`、Graph semantic digestと全File実bytes digestは区別し、cross-file run_id/method/estimand/lineageを突合する。
- 未公開と公開済みの唯一の可視性境界は`renameat2(RENAME_NOREPLACE)`による**同一FSディレクトリのno-clobber rename**。staging files+dirs fsync、rename、両parent dir fsync、独立Reader readbackが成功して初めて`COMPLETED`を返す。結果不定時に既存runを消したり再renameしてsuccessにしない。Readerはmarker→Manifest→inventory file実bytes→schema/相互参照の順で検証する。
- 初期出力Rootの保護は非委譲・同一effective UIDのprivate local FS。shared/CI/container mount・unsafe ACL/owner/symlinkは拒否。`--allow-row-level-export`やStudyの個票要求はG01では**exit3**、row bytesをstagingにも書かない。

## 6. Error・CLI最小動作

| Exit | 条件 | 結果 |
| --- | --- | --- |
| 0 | `--check-only`の実行可能な静的検査、またはReaderまで正常な技術公開（科学的PASSと別） | stdoutはrun_id/technical/science/manifestのsanitize envelopeのみ |
| 2 | E11 version missing/legacy、schema/unknown method config、Method/Operation/Estimand不適格、Duplicate YAML | no final run; typed INPUT_SCHEMA |
| 3 | input File hash/Path/root/mount/owner/privacy拒否 | no row/write outside TrustedRoot; typed INPUT_SECURITY |
| 4 | selected FCI Backend missing/unsupported/API mismatch/実行Technical error | no completed commit; typed ENGINE |
| 5 | staging/publish/collision/readback/fsync破損 | no false complete; typed PUBLICATION |

**`--check-only`の正常結果はReference/PAG精度のPASSではない。** `stdout --json`は1つのJSON制御object。stderrはsecret／個票／生Pathの不要な公開を避けた識別子とReasonのみ。

## 7. Coding Entry前のセルフチェック（追加承認手続きではない）

G01 06は**詳細設計Class.Method・不変条件・DD検証IDに対応付け済みの実装契約**。必要なRuntime適合性・API probes/Graph oracle・JCS実装・FS crash試験は07の責務であり、この文書を増殖させる必要はない。Coding AgentはG01のWPに着手する前に、環境がPython3.12/Linux、既存`uv.lock`の`causal-learn 0.1.4.8`であること、Source/Contractに破壊的差異がないことを確認する。真に未対応ならsilent fallbackではなくTyped Blockerを出す。

**最終判定:** `G01_06_IMPLEMENTATION_CONTRACT_READY / G01_07_VERIFICATION_CONTRACT_READY / TESTS_NOT_RUN / CODING_NOT_AUTHORIZED`。
