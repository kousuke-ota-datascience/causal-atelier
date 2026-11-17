# Ariadne ENH-E11 / G02 — 06 実装指示書（一括Authoring Draft）

**Contract status: DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED**  
**Gate ID: G02 (Enhance Workflow semantic Gate)**  
**Execution mode: WORK_PACKAGE**（一括レビュー用の提案。Owner Freeze前に変更可能）  
**Required packages: P01,P02,P03,P04**（全PxxはDRAFT。存在・契約の一致を確認しない限り起動不可）  
**Depends on: G01 PASS**（暫定依存。Freeze時に正式Gate999で検証）  
**Target: Identification / Eligibility / DoWhy / FD-A / UC-02**  
**Issue provenance: G01〜G10 Gate Decompositionおよび10_32 PLAN mapping**  

## 0. Authority・状態・着手の制限

本書はG02の**Gate-level Coding Contract草案**であり、作成時点ではOwner承認・07 Verification Contract・06/07 Freeze・Coding Authorization・実装/Science実測のいずれも主張しない。06は何を作るか、07は何をもって独立Gate PASSか、P00はPackage DAG、Pxxは担当Agentのbounded execution contract、999は独立判定。互いを代替しない。
**受入境界:** Question/Design/Graph/Assumptions/Data Eligibilityに基づき、識別可能性とEstimator適格性を別々に判定する。optional DoWhy・限定FD-Aだけを科学的前提が成立する条件で提供し、未識別を効果値に変えない。
**下流が利用できる結果:** 対象Method/Operationについて、同一Local Run内のSchema/Scientific/Technical/Inference/Privacy stateとSource/Config/Backend/Seed/Lineageを、実file bytes hashとreadbackまで整合した型付き成果物として検証できること。該当Gateの科学的妥当性は07/999の独立試験で初めて受入とする。

## 1. Scope / Non-scope / 適用条件

**対象:** Identification / Eligibility / DoWhy / FD-A。対象UC: UC-02。Formal Requirement trace: FR-187, FR-188, FR-201, FR-202, FR-203; AR-028, AR-029, AR-030, AR-042, AR-043。
**実行依存:** G01 PASS。前Gateの実際のlatest canonical 999 PASSとprotected contractを確認し、未達の場合は起動しない。G01が提供するstrict Local Study/Graph/Manifest/JCS/ContentRef/Publisher/Reader/CLI compositionを再利用し、科学Kernel/Domain/Portを別系列に再実装しない。
**対象外:** 新Web UI/Web API/Worker/DB/Product Migration、既存Product v2 CLI署名の破壊、G01 GraphVersion/Product authorityの複製、未承認Method・Estimand/CIの一般化、顧客配布の法務承認を科学テストで代替すること、現行`docs/wiki/requirement_definition/`への早期昇格。
**原則:** 全Method提供義務を削らないが、未確定Method profile・実効Backend・独立ReferenceをDRAFT段階でAVAILABLE/SUCCESS/PASSにしない。Gateで必要な科学条件が未Freezeなら当該条件をBLOCKEDとして記録する。

## 2. Gate実装の固有不変条件（そのままCoding Contractに反映する案）

- 識別の識別対象・Design assumptions・Graph endpoint・既存Review/Override statusを別の軸として保存する。PAG/CPDAGの未確定方向はDAGに丸めず、overrideで未識別→識別成功にしてはならない。Graph版変更にはProduct GraphVersion authorityによる新Version・再識別が必要。
- P1-M05のDoWhy IV識別targetは現行Catalogで未確定（BLOCKED）。DoWhyの内部ラベルからLATE/ATEを決定してはならない。対応するtyped negativeを実装する。
- FD-A(P1-M07)は承認された単一Mediatorの限定線形設計・Mediator/Outcome回帰・追加仮定に限る。Frontdoor一般識別と数値二段階推定は別結果とし、直接効果・違反Designは拒否。
- `IDENTIFY`は`identification.json`を発行しダミー`result.json`を作成しない。`ESTIMATE`は明示された識別証拠とEstimator適格性を通過したMethodだけに許可する。

## 3. Method責務・Class.Method・科学的検証の範囲

| Method / DD ID | Adapter Class (current design) | Estimand/semantic obligation | Environment / DGP+NEG / REF |
|---|---|---|---|
| P1-M01 / DD-E11-METH-P101 | `NativeIdentificationAdapter` | Native Randomized identification／A; 割当機構・target、proofの型付き正規化 | ENV-BASE; DGP-001; NEG-001, NEG-027; REF-G01, REF-I01 |
| P1-M02 / DD-E11-METH-P102 | `NativeIdentificationAdapter` | Native Backdoor identification／ATE; adjustment/backdoor、Graph・Design適格性 | ENV-BASE; DGP-002, DGP-021; NEG-002, NEG-003; REF-G01, REF-I01 |
| P1-M03 / DD-E11-METH-P103 | `DoWhyIdentificationAdapter` | DoWhy Backdoor identification／ATE候; effective API、method-specific proof、Graph対応 | ENV-DOWHY; DGP-002, DGP-021; NEG-002, NEG-027; REF-G01, REF-I01 |
| P1-M04 / DD-E11-METH-P104 | `DoWhyIdentificationAdapter` | DoWhy Frontdoor identification／ATE; 単一Mediator／識別仮定、数値FD-Aとは別 | ENV-DOWHY; DGP-005; NEG-004; REF-G01, REF-I02 |
| P1-M05 / DD-E11-METH-P105 | `DoWhyIdentificationAdapter` | DoWhy IV identification／方法固有の対象は未確; DoWhy内部ラベルをLATEと同一視せず対象未確定をBLOCK | ENV-DOWHY; DGP-006; NEG-006, NEG-007; REF-I03, REF-G01 |
| P1-M07 / DD-E11-METH-P107 | `FrontdoorLinearAdapter` | Frontdoor two-stage regression／ATE; 線形Mediator/Outcomeモデルとno direct path仮定、別Reference・CI | ENV-DOWHY; DGP-005; NEG-004, NEG-005; REF-I02, REF-E04 |

**Method Adapter共通署名（新規型付きAdapter）:** 特記がなければ`preflight(self, request: ValidatedMethodRequest) -> EligibilityOutcome`（副作用・fit・published bytesなし）と`execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink) -> TypedScientificOutcome`（適格性通過後のみ実行、Artifactはstagingのみ）。各Methodは実効`MethodDescriptor`/backend factory/ScientificEligibilityPolicyを保持し、requestには検証済みQuestion/Design/Dataset/Graph/Estimand/Method Config/Context/Backend Evidenceを渡す。`MethodConfig`空ObjectやBackend Defaultを未定義Profileの代用品にしない。
**旧Product Adapter例外:** 既存`RefutationAdapter.run(input_, output_dir)`、`SensitivityAdapter.run(input_, output_dir)`の公開v2署名は変更しない。型付きBridgeは別adapterで入出力を厳密検証する。独立CLI engineは作らない。統合済みlegacy testがある場合はその実在Pathを発見して再実行する。
**Result/Port契約:** `IdentificationPort.identify(request: ValidatedIdentificationRequest) -> IdentificationOutcome`、`EstimatorPort.estimate(request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome`、`DiagnosticPort.run(request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome`、`MethodCapabilityPort.resolve(request: ValidatedCapabilityRequest) -> BackendCapabilityRecord`、`DiscoveryPort.discover(request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome`。該当Operationに必要なPortだけを使用し、Typed scientific negativeとtechnical exceptionを混ぜない。

## 4. Work Package execution contract（DRAFT）

| WP | Name | Methods | Depends on (within Gate) | Class.Method / action |
|---|---|---|---|---|
| P01 | Native identification / eligibility | P1-M01, P1-M02 | NONE | `NativeIdentificationAdapter.preflight/execute`、`IdentificationPort.identify`、`IdentificationOutcome` — randomized/backdoorのGraph/Design/Data Eligibility・全理由収集と typed proof。Legacy `IdentificationAdapter`の同義ロジック再利用、PAG不確定はfail-closed。 |
| P02 | Optional DoWhy identification | P1-M03, P1-M04, P1-M05 | P01 | `DoWhyIdentificationAdapter.preflight/execute`、`MethodCapabilityRegistry.resolve` — DoWhyをlazy importしeffective API/Graph semantics/assumptionを検証。Backdoor/Frontdoor識別を型付き正規化し、IV target未確定はtyped BLOCKED、無音fallback禁止。 |
| P03 | Restricted numeric Frontdoor FD-A | P1-M07 | P01 | `FrontdoorLinearAdapter.preflight/execute`、`EstimatorPort.estimate` — 単一Mediator・事前指定線形モデル、FD identification proof、Mediator/Outcome条件、係数積の適用範囲を厳守してeffect Point/Inference可否を別管理。 |
| P04 | IDENTIFY/ESTIMATE CLI and bundle integration | No new Method | P02, P03 | `LocalCausalUseCase.preflight/run`、`LocalRunManifest.to_canonical_bytes`、`LocalManifestReader.read_run` — G01のTrustedRoot/Publisher/Reader/Codecを再利用しIDENTIFY/ESTIMATEのoperation-specific artifact, Status, error, lineage/hashを接続。GraphVersionや旧Product CLIは改造しない。 |

**依存DAG:** P01←NONE; P02←P01; P03←P01; P04←P02+P03。**最終WPがGate-wide integrationを担当**し、すべてのPxx checkpointが集まった後、Candidate AssemblyがGate-wide self-verification/old Product regression/Fixed Trial Candidate SHA/20 Completion Reportを記録する。Package READYはGate PASSではない。
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

- P1-M05の識別対象Estimand/DoWhy mapping・対応Science Referenceを正式指定
- DoWhy/FD-Aの実効dependency/API/CI可用性・Method Config/ProfileのSchema Freeze
- G01から受領するGraph/Question/Design/dataset content hashesと旧v2 Review/Overrideの互換試験
- 各MethodのDGP/NEG/Reference・独立07のTest Item/閾値/計算予算
- Gate依存/Work Package数/Package間DAG/クラスの既存Source所在と直接再利用方法は今回の**草案判断**。現在の`src/ariadne`と承認済み詳細設計の差異を最終的に照合し、必要なら06/Pxxを再作成してからFreezeする。
- 当該Gateの`07_Ariadne_ENH-E11_G02_test_instruction.md`は**未作成**。07の全AC/Test Item/科学負例/環境/Bench・独立Science受入を別途具体化・Owner承認してから06/07をFreezeする。
- Freeze後に仕様やACを静かに書き換えない。Contract defectは09 Amendment、formal independent FAILは08 Remediation、test-side repairは別Authority。

## 8. Completion / Stop / Coding Authorization

**着手前:** G02の06 + 全Required Pxx + 07を一意に解決し、06/07双方`FROZEN`、上流999 PASS、実効Source SHA、`uv.lock`/Optional dependency/License（該当時）、Runtime Operator preflight、Owner Coding Authorizationを明示して初めてCoding Agentを起動する。現時点は未承認。
**Coding complete:** 全Pxxの自己検証・checkpoint/evidence、Candidate AssemblyのGate-wide verification・`FIXED_TRIAL_CANDIDATE_SHA`・20 Completion Report。これは`READY_FOR_TEST`であってPASSではない。
**Test complete:** 07が指定する全必須Test Itemを同一Fixed Candidateに対して独立実施し、30系canonical999がPASSした場合のみ下流Gateが依存可能。Science/Legal/Environmentの未確定・blocked項目をPASSとしない。

## 9. Provenance（Source参照は本06の実装意味を代替しない）

- Common PREP02 frozen design baseline: [117](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)
- Formal 41 Method/requirements: [10_32](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md), [10_13](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_13_fr_causal.md), [10_30](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_30_ar_scientific_integrity.md), [10_31](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_31_ar_estimand_inference.md)
- Domain/Port/Method: [30_60](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_60_cli_adapters.md), [30_61](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md), [30_62](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md), [30_63](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md)
- File/Port IF: [23_41](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md), [23_42](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)
- Gate decomposition: [03](../../40_operator_workflows/architecture_review/03_gate_decomposition.md)

**Authoring:** 2026-11-17 / DRAFT一括作成。Coding/test executionは未実施。
