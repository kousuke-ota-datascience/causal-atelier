# Ariadne ENH-E11 / G01 — 07 テスト・独立検証指示書

**Contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**  
**Gate ID: G01 (Enhance Workflow Gate)**  
**対象：G01（Graph/PAG/Local CLI基盤）**。本07は**G01の独立検証**であり、Gate G07（DiD/Event/ITS）ではない。  
**Authority:** [G01 06](06_Ariadne_ENH-E11_G01_implementation_instruction.md)／[PREP-02 baseline](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[Owner DEC07 定量受入](../../working_notes/20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)／[GRAPH-A判断](../../working_notes/20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)。

## 0. Template verification authority

07はGate Acceptance Criteria authority。Test Item 001はFixed Trial Candidateのfull SHA対checkoutのidentity audit、002〜013は本書G01-07-01〜12に対応。独立Test Agentはproduct/test code、migrations、dependencies、ACを変更せず、実効コマンド・exit・raw evidence・固定SHA・DD ID/ACを記録する。999のみが正式Gate PASS/FAIL/BLOCKEDを判定する。現状の受入境界は再審査中で、本書は未Freeze。

## 1. テスト着手・判定原則

- 06のCoding Entry後、**実際に実装されたSource SHA**に対して独立に実施する。07を先に策定したことをPASSとしない。テストAgentは合否を改善するためにSourceを無断変更しない。
- `PASS / FAIL / BLOCKED`を**テストごと**に返す。動作確認していない環境・FS・Backend API・PAG Oracleは`BLOCKED`、その対象の正式Gate PASSは不可。なお独立レビュー完了記録の追加提出は、G01のテスト着手条件ではない。
- CLIのExit 0は技術的完了であり、`science_acceptance=PASS`とは違う。テスト合格とScience pass、Unit testとMonte Carloは分離する。
- **数値検証：** Owner採用のDEC07方針（既知型/serialization一致=100%、stochastic K/FWER=.05、必要R/Compute Budgetは独立Pilotから）を適用する。実効K/R/Computeの架空設定はしない。**Coding Entryは計画設計を完了していれば可能**だが、G01科学的999 PASSを出す前にT2 Pilot→独立PAG reference→T3事前登録が必要。

## 2. テスト配置と実行方法

実装に合わせて次のPathを作る。既存Test Configは`pyproject.toml`の`[tool.pytest.ini_options]`に従う。実行コマンドは**実装後の実行案**であって本書作成時に実行した結果ではない。

```text
tests/enhancement/enh_e11/g01/
  unit/test_g01_spec_schema_codec.py
  unit/test_g01_graph_roundtrip.py
  component/test_g01_fci_method.py
  component/test_g01_bundle_reader.py
  integration/test_g01_atomic_publication.py
  integration/test_g01_cli.py
  scientific/test_g01_fci_graph_oracle.py
```

```bash
uv sync --frozen
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/unit -q
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/component -q
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/integration -q
uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01/scientific -q
uv run --no-sync python -m pytest tests/product/test_cli_contract.py -q
uv run --no-sync python -m pytest tests/scientific_benchmarks -q
```

`uv sync --frozen`が変更するのは環境であり`uv.lock`更新ではない。Linuxのroot/FS検証とfault injectionはprivate temp rootで実施し、既存データや共有mountを破壊しない。科学的T3で別の資源が必要なときは事前に承認された環境でのみ実行する。

## 3. Deterministic/Contract Matrix（12件）

| Test | 正例／負例 | PASSの観測条件（実結果を記録） | 詳細設計Class.MethodとDD検証ID |
| --- | --- | --- | --- |
| **G01-07-01 Strict Study+dispatch** | Schema v1、P1-M06 only、**Question/Design G01内部Profile**、question_idとStudy.identity一致、Designの変数名・Dataset列順・CI type照合、BK Study/Design一致。duplicate YAML/JSON key、unknown fields、旧Product`causal-analysis-spec/2`、G02 Method指定 | 正例parse。未知・旧版・余剰config/不一致→exit2。旧Product v2は別入口で成功し挙動不変 | 30_60 `9 `LocalConfigDecoder.decode`：SPEC01〜04；30_62 `1：RUN03/04 |
| **G01-07-02 ContentRef and Root** | Regular input same root、../、/abs、Windows separator、symlink/hardlink、hash不一致、違うowner/unsafe mount、race | 元FDの実bytesとSHA一致のみ許可、root外open 0、破損/不正入力exit3 | 30_60 `11 `ContentRef.from_payload` / 30_60 `10 `ContentReferencePort.verify`：REF01〜04；30_62 `3：PUB06、`5：READ07、`6：PRIV03/06 |
| **G01-07-03 Graph/PAG fidelity** | `o-o`, `o->`, `--o`, `->`, `<->`、source/target swap、GraphVersion参照整合（CLI standaloneではversion_id/parent_version_id=null）、Self-loop/duplicate/unknown node/unknown endpoint | 全定義済みendpoint pair・version/parent/lag=nullの**100% roundtrip**、DAG化なし、GraphEvidenceはrevisionを作らずProduct writerのみVersionを発行、INVALID拒否 | 30_61 `1 `GraphEvidence`：GRAPH01/03/04 |
| **G01-07-04 Canonical JCS** | 用意済み7 positive+7 negative vectors、UTF16 sort/NFC-NFD/大値/-0、duplicate/NaN/nonfinite、Graph self digest | Python↔独立JavaScriptのJCS **実bytes一致**、それぞれSHA256一致、Hashの対象混同0。既知JSON文字列をhashするだけではPASS不可 | 30_61 `1 `GraphEvidence.canonical_payload`：GRAPH01；30_62 `4 `LocalRunManifest.to_canonical_bytes`：MAN01〜03 |
| **G01-07-05 Atomic publish** | 同run_idの2 process競合（same/different request hash）、EEXIST、ENOSYS/EINVAL/EOPNOTSUPP/EXDEV、rename/fsync前後SIGKILL、既存不正run | No-clobber=**0 overwrite**、同一hash再利用は完全readbackだけ、post-rename不定はCOMPLETED 0件、fsync/reader実証 | 30_62 `3 `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`：PUB01〜05/PUB07〜09 |
| **G01-07-06 Bundle readback** | Complete manifest/marker/status/graph/study、marker欠損/破損、run ID/Hash/Method違い、duplicate key、symlink、ineligible ACL | 有効なもののみ`VerifiedLocalRun`、保存破損はexit5、検査できないFS/ACLはBLOCKED（schema parseだけでPASSにしない） | 30_62 `4/5 `LocalRunManifest/LocalManifestReader.read_run`：MAN01〜05、READ01〜04/07、PUB07〜09 |
| **G01-07-07 DISCOVER-only envelope** | `P1-M06`成功/合理的科学的負結果、Missing Graph時はdiagnosticsとnonempty reason、no Effect file、`schema_dispatch.result=null`、Study.graph=null | No dummy Effect、Graph成功/科学的negativeのOperation別Bundle inventoryを検査。Registry→DiscoveryPort→FCI AdapterのMethod/Capability一致、UseCase ContextのTrustedRoot/実効Principal/row flag保持を確認。StatusはIdentification NOT_APPLICABLE/Point NOT_REQUESTED/Inference NOT_REQUESTED/Science NOT_EVALUATED、cross-file hash一致 | 30_62 `1/4 `LocalCausalUseCase.run(spec,context)/LocalRunManifest`：RUN01、MAN03/04；30_61 `1/5.5：GRAPH01、DISC01〜03 |
| **G01-07-08 FCI API and eligibility** | 実効`causal-learn 0.1.4.8`、fisherz/chisq/gsq、missing/nan/constant/n<p、CI test mismatch/unknown、Backend absent | 正例selected backend実行、必要列・カテゴリ前提・実効API照合、欠損補完・勝手な離散化・Backend fallback 0件 | 30_62 `2 `MethodCapabilityRegistry`：CAP01/04/05；30_63 `1.3/4.4 `FciDiscoveryAdapter.preflight/execute`：METH-P106 |
| **G01-07-09 GRAPH-A reference** | 小さな**3変数以上**のDAGとlatent付きMAG、Oracle PAGの強制endpointと未確定endpoint、複数seed/依存variant | 独立に導出したPAG/MAG同値類の正解と比較。Backend自身のGraphを教師にしない。DGP母集団truthと推定Graphを分ける | 30_63 `1.3/4.4 `FciDiscoveryAdapter.execute`：METH-P106（GRAPH-A独立Oracle）；30_61 `1：GRAPH01/03 |
| **G01-07-10 BK and latent negatives** | 2変数のlatent confounderと、BK forbidden edgeが余分な`TAIL`を作る可能性、required/forbidden矛盾 | 2変数だけでlatentを「識別」したと宣言しない、BKに過剰確定があれば拒否/Method not available。BK負例は理由付きで止まり偽PASS 0件 | 30_63 `1.3/4.4 `FciDiscoveryAdapter`：METH-P106（BK負例）；30_61 `1：GRAPH03 |
| **G01-07-11 CLI error/privacy** | `--check-only`零書込、row flag / Study row requested、bad hash、bad config、backend failure、corrupt readback | exit2/3/4/5をphaseごとに検証。実効principal/root/Policy Anchorの不一致でdenyし、個票・secretのlogs/stdout/staging漏洩0。非Effect科学的負結果と技術失敗を混同しない | 30_62 `1/6/8.5 `UseCase/LocalPrivacyPolicyPort.authorize/command.main`：RUN07、PUB07、PRIV01〜06、READ03 |
| **G01-07-12 Product & scope regression** | `tests/product/test_cli_contract.py`、既存discovery/identify/estimate/refute/sensitivityとResult v2、G01外Method | legacy`manifest_version=2.0`・旧CLI output semantics不変、Product DB/Web/Worker Source不変、G01外Method変更0 | 30_62 `1/3/4/5/8.5 `command.main/Manifest/Reader`：RUN06、PUB10、MAN06、READ06；30_61 `4：EFF05（旧v2回帰のみ） |

**具体的な実効コマンドは上記Test Pathの作成後に実行する。** ABI不適合をmockだけで隠すことを禁止。Tests 05/06はReal Linux target filesystemの実際のsystem call pathを観測し、monkeypatchだけでPASSとしない。


### 3.1 既存詳細設計への逆引きとG01の非適用

このテスト表の右端列は**30_61〜30_63が定義するDD検証ID**に対応する。07の合否を報告する際は、`test_id`だけでなく`DD検証ID / Class.Method / 実装SHA / fixture / 実測副作用とexit / PASS・FAIL・BLOCKED`をセットで記録する。**複数DD-IDが1テストに対応する場合、ID別の未実施を隠さない**。

- G01直接対象：`REF01〜04、SPEC01〜04、GRAPH01/03/04、RUN01/03/04/06/07、CAP01/04/05、PUB01〜10、MAN01〜06、READ01〜07、PRIV01〜06、DD-E11-METH-P106`。Testごとに個別正例・負例を実行して初めて各DD-IDを判定する。
- G01対象外：`GRAPH02` Temporal→G06、`RUN02/05` Identification連携→G02（Graph Factory RevisionはGRAPH04）、`CAP02/03` Multi-profile→G10、`CAP06` Delivery/legal→別審査、`PRIV07` row export approval/column controls→G05、`ID01〜04 / AR01〜05 / EFF01〜04`の科学的実装→後続Method Gate。`EFF05`は旧v2回帰として07-12だけ実施。
- 例：`DD-E11-PUB05`（30_62 `3.7 concurrent no-clobber）→06 `2 G01/P02/`2.1 `LocalArtifactPublisher.commit`→07-05。`DD-E11-GRAPH01`（30_61 `1.1.5 PAG marks）→06 `2 G01/P03/`2.1 `GraphEvidence.canonical_payload`→07-03（**形式保存**）と07-09（**PAG科学的正しさ**）。この2種類を同じScience PASSにはしない。


## 4. FCI独立Graph Referenceと定量セル（G01 Gate07）

**正解をBackend出力から生成しない。** 07担当は、独立に検査できる小Graph（多変数・潜在の有無両方）に対し、以下を満たすOracleを作る。

1. `DGP`: node集合（observed/latent分離）、SCM式・親構造・母集団CI制約・faithfulness、効果の強さ、sample size/n、CI familyと分布仮定、seed、Generator/source SHAを固定。
2. `Reference`: 真のDAG → 観測変数へのlatent projection / MAG → Markov同値類のPAGのうち**強制される端点・不確定端点を独立理論で導出**。生成DAGの全部の方向を直接PAGの正解にしてはならない。
3. `Serialization/typing`: PAG辺のendpoint・GraphVersion parent・JSON/Manifest全Hashの定義済みFixtureは**100%一致（false authorization 0）**。ここはstochastic測定と独立して合否確定。
4. `Stochastic performance`: 強信号で適格なGraph DGPについて、Owner DEC07の候補`adjacency Precision, Recall ≥0.80; FPR≤0.10`を**候補**として独立Pilotで妥当性を検討し、Hard/conditional/N/Aの分類を決める。強制Endpointは同値類Oracleに対してのみ測る。数値未確定の方向正答率を勝手に100%としない。
5. `Multiplicity/K/R`: Gate全体のmandatory stochastic Hard cellを列挙した後、Bonferroni`α_j=.05/K`、replicate-level WilsonなどOwner DEC07の統計設計に従う。T2 PilotはGraphの場合まず約100 repsを**計算量見積り**の起点とし、T3正式R/K/seed/CPU capは本GateのScience実行前に確定。Pilot結果をT3の分母に混ぜない。
6. 判定は`PASS/FAIL/INCONCLUSIVE/BLOCKED`。独立PAG Oracle未完成なら`G01-07-09=BLOCKED`、強信号Graphの数値Science PASSを捏造しない。ただし他の機械Contract テスト実装・実行を妨げない。

**Graph-specific negative:** `DGP-011`の2変数潜在構造はlatent presenceを一意識別する正例には使用しない。Graph tokenのROUNDTRIPとFCI statistical recoveryは別物。

## 5. 受入の判定ロジックと実施結果様式

- **Mechanical PASS候補:** 07-01〜08/10〜12の実証に成功。ただし09の独立Graph scientific oracleはG01全体の受入に必須で、未実行なら**G01_999=BLOCKED**。
- **Science PASS候補:** Graph-a independent oracle、Model/test eligibility、G01に適用する確定済みK/R/Resource/Hard ACの実replicateとnegative testをすべて満たす。確定前はScience PASSを付けない。
- **G01_999:** 一つの共通実装Commitの実際のtest evidenceをReviewerが評価する。No false COMMITTED、No raw row leak、No DAG fabricationはHard invariants。

最小の結果行：

```text
dd_id | class.method | test_id | source_sha | fixture_sha | env_lock_sha | command |
real_or_mock | actual_result/exit | expected | PASS/FAIL/BLOCKED |
defect_or_reason | evidence_relative_key
```

計算不能なtestを削除、未実行をSKIP扱いでPASS、科学的負結果をExit4として隠すことは不可。

**実行状況:** `07_SPEC_PREPARED / TESTS_NOT_RUN / INDEPENDENT_SCIENCE_NOT_RUN / G01_999_NOT_DECIDED / CODING_NOT_AUTHORIZED`。


### G01内部Question/Design入力の検証追加（2026-11-17）

[Question evidence profile](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_question_profile_v1.schema.json)、[Design evidence profile](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json)は、5つの公開E11 payload version以外に新しいwire versionを追加するものではない。G01-07-01/08で`question_id`・Study ContentRef identity・Design同一性、Design列名/順序/型とDataset、Method config背景知識の同値、unknown/duplicate field・混合尺度不適格、宣言された仮定を科学的真と誤表示しないことを確認する。


## 6. Gate Acceptance Criteria / template Test Items

| AC | MUST acceptance claim | Primary test layer |
| --- | --- | --- |
| AC-01 | Study/ContentRef/Version/Method Config strict integrity | UNIT_DOMAIN, COMPONENT |
| AC-02 | Lossless PAG/GraphVersion and strict JCS hashes | UNIT_DOMAIN |
| AC-03 | Linux same-FS no-replace atomic publish/readback/privacy | REAL_FS_INTEGRATION |
| AC-04 | Effective FCI/CI/BK validity and independent MAG/PAG oracle | COMPONENT, SCIENTIFIC |
| AC-05 | DISCOVER-only status/result semantics; v2 regression | INTEGRATION, REGRESSION |
| AC-06 | Candidate identity, protected contracts, full evidence | META |

Test Item 001 = Candidate identity audit; 002〜013 = G01-07-01〜12 in §3; 999 = independent Gate Decision. CLI-onlyでBrowser E2Eは対象外。固定候補/環境/独立Referenceを検証できないならBLOCKED、MUST違反を実証したらFAIL、全MUST実測成立の場合のみPASS。
