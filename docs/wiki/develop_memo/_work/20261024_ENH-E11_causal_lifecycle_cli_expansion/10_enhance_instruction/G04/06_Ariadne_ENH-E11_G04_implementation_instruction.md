# Ariadne ENH-E11 / G04 — 06 実装指示書（一括Authoring Draft）

**Contract status: DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED**  
**Gate ID: G04 (Enhance Workflow semantic Gate)**  
**Execution mode: WORK_PACKAGE**（一括レビュー用の提案。Owner Freeze前に変更可能）  
**Required packages: P01,P02,P03,P04**（全PxxはDRAFT。存在・契約の一致を確認しない限り起動不可）  
**Depends on: G02 PASS, G03 PASS**（暫定依存。Freeze時に正式Gate999で検証）  
**Target: Non-IV CATE/HTE and EconML DRIV / UC-04**  
**Issue provenance: G01〜G10 Gate Decompositionおよび10_32 PLAN mapping**  

## 0. Authority・状態・着手の制限

本書はG04の**Gate-level Coding Contract草案**であり、作成時点ではOwner承認・07 Verification Contract・06/07 Freeze・Coding Authorization・実装/Science実測のいずれも主張しない。06は何を作るか、07は何をもって独立Gate PASSか、P00はPackage DAG、Pxxは担当Agentのbounded execution contract、999は独立判定。互いを代替しない。
**受入境界:** 7方式のnon-IV CATE(x)と1方式のconditional IV structural slope(DRIV-A)を別Estimand/Eligibilityとして提供し、探索的点推定と確認的推論を区別する。
**下流が利用できる結果:** 対象Method/Operationについて、同一Local Run内のSchema/Scientific/Technical/Inference/Privacy stateとSource/Config/Backend/Seed/Lineageを、実file bytes hashとreadbackまで整合した型付き成果物として検証できること。該当Gateの科学的妥当性は07/999の独立試験で初めて受入とする。

## 1. Scope / Non-scope / 適用条件

**対象:** Non-IV CATE/HTE and EconML DRIV。対象UC: UC-04。Formal Requirement trace: FR-193, FR-194, FR-195, FR-202, FR-201, FR-203; AR-034, AR-035, AR-042, AR-044。
**実行依存:** G02 PASS, G03 PASS。前Gateの実際のlatest canonical 999 PASSとprotected contractを確認し、未達の場合は起動しない。G01が提供するstrict Local Study/Graph/Manifest/JCS/ContentRef/Publisher/Reader/CLI compositionを再利用し、科学Kernel/Domain/Portを別系列に再実装しない。
**対象外:** 新Web UI/Web API/Worker/DB/Product Migration、既存Product v2 CLI署名の破壊、G01 GraphVersion/Product authorityの複製、未承認Method・Estimand/CIの一般化、顧客配布の法務承認を科学テストで代替すること、現行`docs/wiki/requirement_definition/`への早期昇格。
**原則:** 全Method提供義務を削らないが、未確定Method profile・実効Backend・独立ReferenceをDRAFT段階でAVAILABLE/SUCCESS/PASSにしない。Gateで必要な科学条件が未Freezeなら当該条件をBLOCKEDとして記録する。

## 2. Gate実装の固有不変条件（そのままCoding Contractに反映する案）

- Non-IV CATEはX=effect modifiers、W=confounders、Treatment/Outcome/target population/nuisance/folds/overlapをMethod別に宣言。S/T/X-LearnerとDML/Forest/DRを単一Estimatorへ縮退しない。
- P2-M08 DRIV-Aの`CONDITIONAL_IV_STRUCTURAL_SLOPE`はnon-IV CATE、B0 complier LATE、B1 linear IV slopeとは異なる。IVのrelevance/exclusion、X/W/weak IV、不適格時のtyped negativeを記録する。
- Inference RegistryはMethod×Backend×Version×configurationごとにPOINT_ONLY/SUPPORTED_CI/UNSUPPORTED/UNAVAILABLE/FAILEDを判定。pointwise confidenceとsimultaneous bandは異なる。探索的点推定をConfirmatory成功にしない。
- G04で個票Parquetをデフォルト生成しない。row release authority/verified policyと公開前の診断・発行はG05の専権、G04ではaggregate/内部Stagingのみ。

## 3. Method責務・Class.Method・科学的検証の範囲

| Method / DD ID | Adapter Class (current design) | Estimand/semantic obligation | Environment / DGP+NEG / REF |
|---|---|---|---|
| P2-M01 / DD-E11-METH-P201 | `EconmlCateAdapter` | LinearDML／CATE(x); X/W/treatment/outcome、inference registry、fold | ENV-ECONML; DGP-003; NEG-011, NEG-012, NEG-013; REF-E05 |
| P2-M02 / DD-E11-METH-P202 | `EconmlCateAdapter` | CausalForestDML／CATE(x); leaf/support/nuisance/CI API、row privacy | ENV-ECONML; DGP-004; NEG-010, NEG-012, NEG-013; REF-E05 |
| P2-M03 / DD-E11-METH-P203 | `EconmlCateAdapter` | DRLearner／CATE(x); binary treatment/propensity、inference method | ENV-ECONML; DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05, REF-E03 |
| P2-M04 / DD-E11-METH-P204 | `EconmlCateAdapter` | ForestDRLearner／CATE(x); propensity+forest inference/support | ENV-ECONML; DGP-004; NEG-010, NEG-011, NEG-013; REF-E05, REF-E03 |
| P2-M05 / DD-E11-METH-P205 | `MetaLearnerAdapter` | S-Learner／CATE(x); counterfactual prediction、point/CI制限 | ENV-ECONML; DGP-002, DGP-003; NEG-010, NEG-012, NEG-013; REF-E05 |
| P2-M06 / DD-E11-METH-P206 | `MetaLearnerAdapter` | T-Learner／CATE(x); treated/control support、point/CI制限 | ENV-ECONML; DGP-003, DGP-004; NEG-010, NEG-013; REF-E05 |
| P2-M07 / DD-E11-METH-P207 | `MetaLearnerAdapter` | X-Learner／CATE(x); cross-model weights、point/CI制限 | ENV-ECONML; DGP-003, DGP-004; NEG-011, NEG-012, NEG-013; REF-E05 |
| P2-M08 / DD-E11-METH-P208 | `EconmlDrivAdapter` | DRIV-A／CONDITIONAL_IV_STRUCTURAL_SLOPE; Z/A/X/W、IV relevance/exclusion、inference | ENV-ECONML; DGP-008; NEG-009, NEG-012, NEG-013; REF-E06 |

**Method Adapter共通署名（新規型付きAdapter）:** 特記がなければ`preflight(self, request: ValidatedMethodRequest) -> EligibilityOutcome`（副作用・fit・published bytesなし）と`execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink) -> TypedScientificOutcome`（適格性通過後のみ実行、Artifactはstagingのみ）。各Methodは実効`MethodDescriptor`/backend factory/ScientificEligibilityPolicyを保持し、requestには検証済みQuestion/Design/Dataset/Graph/Estimand/Method Config/Context/Backend Evidenceを渡す。`MethodConfig`空ObjectやBackend Defaultを未定義Profileの代用品にしない。
**旧Product Adapter例外:** 既存`RefutationAdapter.run(input_, output_dir)`、`SensitivityAdapter.run(input_, output_dir)`の公開v2署名は変更しない。型付きBridgeは別adapterで入出力を厳密検証する。独立CLI engineは作らない。統合済みlegacy testがある場合はその実在Pathを発見して再実行する。
**Result/Port契約:** `IdentificationPort.identify(request: ValidatedIdentificationRequest) -> IdentificationOutcome`、`EstimatorPort.estimate(request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome`、`DiagnosticPort.run(request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome`、`MethodCapabilityPort.resolve(request: ValidatedCapabilityRequest) -> BackendCapabilityRecord`、`DiscoveryPort.discover(request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome`。該当Operationに必要なPortだけを使用し、Typed scientific negativeとtechnical exceptionを混ぜない。

## 4. Work Package execution contract（DRAFT）

| WP | Name | Methods | Depends on (within Gate) | Class.Method / action |
|---|---|---|---|---|
| P01 | EconML DML / DR CATE adapters | P2-M01, P2-M02, P2-M03, P2-M04 | NONE | `EconmlCateAdapter.preflight/execute`、`EstimatorPort.estimate` — LinearDML、CausalForestDML、DRLearner、ForestDRLearnerのモデル・support・nuisance/seed/folds・backend API・inference capabilityをMethod別実装。 |
| P02 | S/T/X meta learners | P2-M05, P2-M06, P2-M07 | NONE | `MetaLearnerAdapter.preflight/execute`、`EstimatorPort.estimate` — S/T/Xのcounterfactual-model/treated-control support/X weightのMethod差異を保持。未承認CIを生成せず探索的point-onlyをtypedに記録。 |
| P03 | Conditional IV DRIV-A | P2-M08 | P01 | `EconmlDrivAdapter.preflight/execute`、`EstimatorPort.estimate` — `CONDITIONAL_IV_STRUCTURAL_SLOPE`、Z/A/X/Wの別役割、IV仮定・弱IV negative・method-specific inferenceを実装。Non-IV CATE/LATEへの自動castを拒否。 |
| P04 | CATE inference registry / aggregate Result integration | No new Method | P01, P02, P03 | `MethodCapabilityRegistry.resolve`、`InferenceEvidence`、`EffectOutcome`、`LocalManifestReader.read_run` — point availability/inference availability/science acceptanceの独立軸と各Estimator/Backend config/seed/lock、aggregate summary、Effect Resultのpublication/readbackを統合。 |

**依存DAG:** P01←NONE; P02←NONE; P03←P01; P04←P01+P02+P03。**最終WPがGate-wide integrationを担当**し、すべてのPxx checkpointが集まった後、Candidate AssemblyがGate-wide self-verification/old Product regression/Fixed Trial Candidate SHA/20 Completion Reportを記録する。Package READYはGate PASSではない。
**Pxxは単独にAgentへ渡せる自己完結のPrimary Contract**として別文書化し、この06からしか意味を復元できない状態にしない。P00は計画、Runtime authorityはFrozen06のRequired packagesと個別Pxx `Depends on`。Test実物の物理配置・収集command・runnerは40 Operatorが決める。

## 5. 共通Local Execution・Bundle・Security契約

- **入口:** `LocalConfigDecoder.decode`によるstrict `e11-local-study/1`、typed `ValidatedStudy`→`LocalCausalUseCase.preflight/run`→Capability/Identification/Estimator/Diagnostic/Discovery Ports→Method Adapter→`StagingArtifactSink`→Publisher→Verified Reader。operation-specific profileはこのGateのMethodを追加する前にstrict Schema/cross-asset validatorを定義する。Gate IDをMethod dispatchキーとしない。
- **Codec/identity:** RFC8785 JCS strict `e11-json-jcs-rfc8785/1`、`request_hash=SHA256(JCS(validated Study))`。ContentRefはraw file bytes、Graphの意味hashとGraph保存bytesのhashは別。未知v2 Schema／`default=str`を自動受理しない。
- **Bundle:** `DISCOVER`→`graph.json`、`IDENTIFY`→`identification.json`、`ESTIMATE`→`result.json`、`REFUTE/SENSITIVITY/DIAGNOSE`→`diagnostics.json`。科学的negativeではschema適合するstatus/reasonと適切な欠落Artifactを示す。`DISCOVER/IDENTIFY`にdummy Effectを書かない。全Operationに`study.json`/`status.json`/`manifest.json`/`_COMMITTED.json`と厳密schema_dispatch/lineage/sha256を要求。
- **Publisher:** same UID owner-only private TrustedLocalRoot、dirfd/no-follow、同一FS、`renameat2(RENAME_NOREPLACE)` no-clobber、staged fsync/manifest/marker/parent fsync/Verified Readerの順序を再利用。欠落hash/manifest/marker、publish indeterminateは成功にしない。既存run上書き・silent delete禁止。
- **Privacy:** デフォルトaggregate-only、row Effect bytesをG05の独立事前承認前に生成しない。Studyの自己宣言/CLI flagのみで認可しない。token/secret/rowをStdout/Manifest/traceへ出さない。正式なCustomer DeliveryはSBOM/Licenseの受領者別法務判断を別途必要とする。
- **Error/Science:** CLI exit 0=技術的完了で科学的negativeを含み得る、2=入力Schema、3=Path/Hash/Privacy、4=実行Backend、5=Publication/Readback。`identification`, `point`, `uncertainty`, `science_acceptance`, `technical outcome`を別々に保つ。`CI unavailable`を0/finite CIと偽装しない。
- **Product互換:** 旧v2 `ScientificCorePort.run_*`、Product `GraphVersionService`、`StageRunnerRegistry`、`RefutationAdapter`/`SensitivityAdapter`公開署名とlegacy Readerを変更しない。Portの共通科学Kernelだけ再利用し、旧v2 DTOへPAG/AR/typed negativeを損失castしない。

## 6. Coding-side verification / evidence obligations

- 各Methodに10_32の`DD-E11-METH-*`、positive DGP、negative case、independent REF、provisional ACを対応付ける。数値既知真値/coverageの独立ReferenceはBackend自身の出力で作らず、Method-specific R/K/seed/budget・推論適格性を07 Freezeまでに明示する。上記表に既に`BLOCKED`とあるMethodの欠落契約を勝手に補完しない。
- Unit: strict DTO/Method profile/semantic distinctions/negative Status。Contract: Port/Manifest/Graph/Result/ConfidenceSet/Privacy・API互換。Integration: 実Backend/実Linux file publicationとcurrent CLI/old v2回帰。Frontend/Browser E2EはCLI-only ENH-E11新機能の対象外。TestのLifecycle/Layer、物理Path、pytest collectionと実行commandは40 Operatorがcurrent checkoutから選び、06に硬直したfilenameを置かない。
- Focused verificationは各Pxxで実行し、実コマンド/Checkout SHA/fixtures/Backend/OS/FS/seed/結果を20系Package statusへ記録する。Mock-onlyで実Sci/FilesystemのPASSを宣言しない。Gate-wide候補を一つのFixed SHAに固定した後、独立Agentだけが07 Test Item/999で最終受入を判定する。

## 7. Freeze前のOwnerレビュー・未閉鎖事項

- Method別config/optional EconML API/CI policyのeffective probe・schema freeze
- DRIV-Aの対象と非IV差分、weak-IV negative、独立Science Referenceをmethod-specificに確定
- 各Methodのconfirmatory inference方式・coverage予算・target populationとCI availabilityの受入閾値
- G05に渡すrow-evidence内部型・public byte生成の責任境界
- Gate依存/Work Package数/Package間DAG/クラスの既存Source所在と直接再利用方法は今回の**草案判断**。現在の`src/ariadne`と承認済み詳細設計の差異を最終的に照合し、必要なら06/Pxxを再作成してからFreezeする。
- 当該Gateの`07_Ariadne_ENH-E11_G04_test_instruction.md`は**未作成**。07の全AC/Test Item/科学負例/環境/Bench・独立Science受入を別途具体化・Owner承認してから06/07をFreezeする。
- Freeze後に仕様やACを静かに書き換えない。Contract defectは09 Amendment、formal independent FAILは08 Remediation、test-side repairは別Authority。

## 8. Completion / Stop / Coding Authorization

**着手前:** G04の06 + 全Required Pxx + 07を一意に解決し、06/07双方`FROZEN`、上流999 PASS、実効Source SHA、`uv.lock`/Optional dependency/License（該当時）、Runtime Operator preflight、Owner Coding Authorizationを明示して初めてCoding Agentを起動する。現時点は未承認。
**Coding complete:** 全Pxxの自己検証・checkpoint/evidence、Candidate AssemblyのGate-wide verification・`FIXED_TRIAL_CANDIDATE_SHA`・20 Completion Report。これは`READY_FOR_TEST`であってPASSではない。
**Test complete:** 07が指定する全必須Test Itemを同一Fixed Candidateに対して独立実施し、30系canonical999がPASSした場合のみ下流Gateが依存可能。Science/Legal/Environmentの未確定・blocked項目をPASSとしない。

## 9. Provenance（Source参照は本06の実装意味を代替しない）

- Common PREP02 frozen design baseline: [117](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)
- Formal 41 Method/requirements: [10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md), [10_13](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_13_fr_causal.md), [10_30](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_30_ar_scientific_integrity.md), [10_31](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_31_ar_estimand_inference.md)
- Domain/Port/Method: [30_60](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_60_cli_adapters.md), [30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md), [30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md), [30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)
- File/Port IF: [23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md), [23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)
- Gate decomposition: [03](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)

**Authoring:** 2026-11-17 / DRAFT一括作成。Coding/test executionは未実施。
