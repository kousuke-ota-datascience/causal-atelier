# Ariadne ENH-E11 G05 — 07 独立テスト指示書：HTE診断・個票Privacy・Artifact

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がStudy requestとCLI flagで明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、ACL/mount/namespace/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ `--allow-row-level-export` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`の任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mount/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


**Verification contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**
**Owner review: 2026-11-18 JST — PREP-03 audit and G05 Gate-level verification plan reviewed/accepted, with open Method/Profile/Evidence decisions preserved. This is NOT Contract Freeze, Independent Test execution, Gate999 PASS, or Coding Authorization.**
**Gate: G05 / Independent Test Agent / Trial01 NOT_STARTED**
**Dependencies: G04 PASS (canonical upstream 999)**
**Normative WHAT:** 本書のAC/Test Itemsのみ。テストの実physical path・command・runner discoveryは40 Operatorが所有。
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Independent Gate claim

このGateがPASSしたと主張するには「CATE support/calibration/uncertainty診断と、明示的に許可されたときだけの個票Parquetを分離し、原子的なファイル出力と安全なReadbackを提供する。」をFull Fixed Candidate SHAで、後述の全受入軸と独立科学的Referenceに照らして証明する。Pxx COMPLETE、CLI exit0、Source上のMethod名、mock-onlyは独立Gate/Science PASSではない。

## 1. Acceptance Criteria (each blocking)

- **AC01 Strict Method/Design/Estimand:** 受理されたMethod×Operation×Target×Question/Design/GraphVersion/HashとInference Policyのみ実行。unknown/mismatch/partial/unidentifiedはtyped negative。
- **AC02 Actual Science:** 各Methodの既知DGP・Negative・独立REF、Backend実測/現行推論API、明示Assumption/Point/UncertaintyとScience status。
- **AC03 Portable Result:** Graph/Effect/Diagnostic/ConfidenceSet/MethodConfig/Provenanceを正しくBundle/Manifest/Readerへ保存し、hash/readback/negativeを確認。
- **AC04 Compatibility/Safety:** G01 FS/Privacy/Atomic/JCSと旧Product v2のprotected interface/behaviorを壊さず、無言fallback/未認可出力がない。
- **AC05 Identity/Independent QA:** Source/lock/fixture SHA、科学事前登録、test-layer、実効環境、Test Item全証拠と正式999判定。

## 2. Required Test Items (file locations are NOT normative)

| ID | Primary purpose | Primary verification layer | Required observable evidence |
|---|---|---|---|
| `G05-07-01` | HTE support/calibration/uncertainty（cross-cutting） | unit/contract + required integration | CATE/DRIV別support/uncertainty/diagnostics；適格positive/negative・typed Reason |
| `G05-07-02` | Local user double opt-in + private FS | contract + Linux ext4/XFS integration | UID/owner/ACL/mount、Method Schema・deny時Source反復0 |
| `G05-07-03` | bounded Parquet + atomic Publisher | contract + real FS/Parquet integration | Writer/Factory/schema/row byte limit、G01 Publisher/Reader/TOCTOU |
| `G05-07-04` | HTE/Row Export統合と回帰（cross-cutting） | unit/contract + required integration | 不許可出力0、Aggregate互換/Manifest；適格positive/negative・typed Reason |
| `G05-07-05` | Whole Local CLI/Port/Artifact integration | contract + real CLI/FS integration | Strict Operation, Hash, Manifest, Reader, privacy, negative Error status |
| `G05-07-06` | Protected v2/upstream contracts | current actual legacy suite + E11 integration | Upstream 999 invariants, no old v2 CLI/Result change |
| `G05-07-07` | Independent Science/T2/T3 | independently verified reference + real backend integration | Method-specific DGP/NEG/REF, prereg K/R/seed/compute, predeclared quantitative decision |
| `001` | Candidate identity | repository provenance audit | Candidate full SHA, actual checkout, test-only diff classification |
| `999` | Formal Gate decision | independent 30 reports | All blocking items PASS, verified FAIL or BLOCKED and owner action |

**Browser E2E:** 本E11 ScopeはCLI-firstで新規Web UIを実装しないため、当該Gateの新規Browser E2E blocking journeyは**N/A**。既存Productのaffected Browser journeyはRegression対象となり得る。将来UIを本GateScopeへ変更する場合は07の正式Amendment・再Freezeとcritical journey・command・environment・synchronization記述を先行させる。

## 3. Method-by-Method Scientific test obligations

本Gateに新規Method IDはない。上流各Methodの科学的受入証拠を破棄・偽装せず、当該Gateの横断Contract/Privacy/Manifest/再現性に専用の独立Reference/negativeを要求する。

**Independent oracle and numerical rule:** DGP truthとEstimator/Backend outputは別Authority。Fixed generator/Reference SHA、既知EstimandとAssumptions、negative/statusを先に登録。Deterministic schema/JCS/roundtripは100%一致。Stochastic ScienceはT2 PilotとT3正式事前登録を分離し、多重性K/FWER=0.05、K/R/seed/threshold/computeは科学決定に基づきFreeze。未確定を推測で補完せず該当Test Item BLOCKED。


## 3.1. Local executor double opt-in／OS・Parquet privacy matrix（全件blocking）

| Test | Setup | 必須観測／FAIL条件 |
|---|---|---|
| G05-07-POL01 | Studyのみ・CLIのみ・両方false | exit3・row Source反復0・row bytes0・fallback無し |
| G05-07-POL02 | Study/CLI両true・nonroot EUID/private ext4/XFS・Method schema | PrivacyDecision許可・実FS/Parquetの正例・Writer/readback |
| G05-07-POL03 | 異run/変更Method/Study/Data・wrong EUID/owner/ACL | typed exit3・RowSource反復0・bytes0 |
| G05-07-POL04 | unsafe ACL/mount/namespace/symlink/root変更・cross-FS | Fail closed、stage/publish再検証、row値漏洩無し |
| G05-07-WR01 | 両opt-in＋実private FS・Method approved 1..max_rows | ordered column/type/row/byteとG01 Sink/Reader/Marker/hash、0700/0600 |
| G05-07-WR02 | max_rows+1、max_output_bytes超過、NaN/dup IDs/unknown column、empty invalid | no completed row publication、typed rejection/部分成功無し |
| G05-07-WR03 | stage後のroot/ACL/mount不正・rename race/disk failure | 未公開、marker無し、private stage隔離、二重Publish無し |
| G05-07-WR04 | 旧Product v2、Output JSON/console/log/Error中の行値 | 旧ABI維持、無認可行/secretは一切流出しない |

**Class boundary:** LocalPrivacyPolicyがStudy・CLI・EUID/TrustedRoot・Method ApprovedRowSchemaを検証する。RowWriter/Factoryは許可後Serializerだけを所有し、G01 Publisherは変更しない。

## 4. Verification operation, evidence and decision

- Fixed Trial Candidate SHAと実効checkoutが同じsemantic implementation stateか監査。上流Gateのcanonical 999 PASSとprotected contractをSource上の根拠で照合。
- 40 Test Agentは`tests/enhancement/enh_e11/<gate>/`を始点に、関連する`tests/product/`/`tests/integration/`等を現物から発見、test existence/collection/fixture/conftest/dependencies/runner/FS/backendを確認。07にhistorical filename/commandを固定しない。
- Test evidenceにはItem ID/DD ID、actual path/command、source/fixture/lock SHA、effective OS/FS/backend、Known truth/observed output、positive+negative、PASS/FAIL/BLOCKEDと原因を記録。Evidence commitとCandidate SHAを混同しない。
- Independent Test Agentはproduct/test code/runner/CI/06/07を修復しない。Product不変違反を実証したときFAIL、Test-side/UNKNOWN/Backend/独立Oracle不足でProduct判定不能ならBLOCKED。
- G01〜G10各Gateの999は独立であり、Methodごとの未実施・Science未検証・Protected Regression欠落がある限りGate PASS禁止。

## 5. Freeze前のOwner/Science review

CLI flagだけの個票出力許可、偽造Policy、未承認列の持ち出しを禁止。

Method-specific strict Schema・positive/negative・独立Reference/推論Method/CI・threshold・Backend/License・Gate境界/depends/quant computeをレビューし、07をFreezeして初めて実行可能。現時点ではTest NOT_RUN、999 NOT_EXECUTED。

