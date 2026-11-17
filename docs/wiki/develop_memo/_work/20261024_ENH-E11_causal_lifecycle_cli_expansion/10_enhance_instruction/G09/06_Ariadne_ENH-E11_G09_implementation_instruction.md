# Ariadne ENH-E11 G09 — 06 実装指示書：Synthetic Control・Synthetic DiD

**Contract status: DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED**
**Gate: G09 / formally planned G01〜G10 / Trial01 NOT_STARTED**
**Depends on: G01 PASS — upstream canonical 999 mandatory (DRAFT dependency proposal)**
**Execution Mode: WORK_PACKAGE (DRAFT proposal); Required packages: P01, P02, P03, P04**
**Owner Freeze: PENDING / Coding Authorization: NOT_AUTHORIZED / Baseline full SHA: NOT_FIXED**
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 0. Gate Acceptance Authority and Entry

本06は本GateのImplementation WHATの一次契約。P00は計画、Pxxはbounded Coding Unit、07は独立Verification、999は正式Decision。Method IDのP1-Mxx等とPackage P01等を混同しない。上流Gate 999 PASS・本Gate 06/07/Pxx Owner承認とFreeze・固定Source/lock SHA・実行環境/remote/preflight・明示Coding Authorizationが成立する前はCodingを禁止。G01の06/07を他Gateの仕様として参照・転用しない。

## 1. Objective / Downstream contract

**UC: UC-09。**Meaningful PASS:** 汚染のないdonor/事前適合性を検査し、SCM point-only反事実ギャップとSDID panel平均効果の異なる対象を正確に記録する。

Gate単位のPASS後に守るもの: Typed Result/Graph/Diagnostic、Method固有Estimand・Identification/Eligibility・Science negative、strict Local CLI/Manifest/Readerと環境再現性を、本Gateの統合Fixed Candidateで独立に検証した状態。Pxx checkpointやCLI Exit=0はGate/Science PASSではない。

## 2. In scope, prohibited scope and compatibility

- **In scope:** Gate固有MethodとDesign/Question/Method strict Schema、30_63 Class Adapter、30_61 Domain/Port、Local CLI composition、typed status/Result、独立Scientific Reference、上流Protected Contract回帰。
- **Reuse:** G01のContentRef/JCS/GraphEvidence/Version authority/TrustedRoot/AtomicPublisher/ManifestReader/MethodCapabilityRegistry・既存ScientificCore/v2計算処理を適格に再利用し、CLI専用Scientific Domainを並行実装しない。
- **Out of scope:** 本Gate外のMethod、Web/API/Worker/DB/UI統合、Product migration、正本documentsの昇格、未採用Policy/CI/Backend、ライセンス未審査配布。
- **科学/安全上の禁止:** SCM point-onlyにCIを捏造、donor contamination、事後選択の無言許可を禁止。
- **Protected invariant:** 旧Product v2 CLI/Manifest/Result・上流PASS Gateの06/07/999が保護するsemantics。Unsupported Backend/Inferenceはtyped UNAVAILABLE、silent fallback/placeholder Effect/CI/Graphは禁止。

## 3. Work Package map and provisional DAG

| WP | Owned boundary | Method IDs | Depends on Pxx | Mandatory proof |
|---|---|---|---|---|
| `P01` | Donor pool/Panel Design | Cross-cutting | NONE | preperiod eligibility/contamination/treated unit |
| `P02` | Synthetic Control Adapter | `P3-M12` | P01 | donor weights/RMSPE/placebo/point-only |
| `P03` | Synthetic DiD Adapter | `P3-M13` | P01 | time/unit weights・panel ATT・inference |
| `P04` | SCM/SDID Result/CLI・独立科学 | Cross-cutting | P02,P03 | REF-Q04/Q05とnegative |

P00はCoding Unitではない。各Pxxがself-contained Class.Method実装、正負例、Checkpoint SHAと20 Package reportを作る。Package構成/依存はOwnerレビューで確定し、Freeze前に実行しない。

## 4. Method/Class/Port matrix

| Method | Estimand/target | Adapter | FR/AR | DGP/NEG・REF | Readiness |
|---|---|---|---|---|---|
| `P3-M12` | treated-unit counterfactual gap | `SyntheticControlAdapter` | FR-200/AR-041 | DGP-017; NEG-024; REF-Q04 | PLAN:G09 / OWNER_BASELINE_ACCEPTED_POINT_ONLY_SCIENCE_PENDING / NOT_GENERATED |
| `P3-M13` | panel average effect | `SyntheticDidAdapter` | FR-200/AR-041 | DGP-018; NEG-024; REF-Q05 | PLAN:G09 / OWNER_ESTIMATOR_INFERENCE_POLICY_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

### 4.1. Concrete Adapter Class/Method duties

- `ariadne.scientific.causal_methods.quasi.SyntheticControlAdapter`：`preflight(self, request: ValidatedMethodRequest) -> EligibilityOutcome` / `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink) -> TypedScientificOutcome`（30_63の一般署名。既存v2 Refutation/Sensitivity runは互換維持）。Descriptor/BackendFactory/ScientificEligibilityPolicyを注入し、effective Method config/Target検証、lazy backend import、portable typed DTOのみを返す。
- `ariadne.scientific.causal_methods.quasi.SyntheticDidAdapter`：`preflight(self, request: ValidatedMethodRequest) -> EligibilityOutcome` / `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink) -> TypedScientificOutcome`（30_63の一般署名。既存v2 Refutation/Sensitivity runは互換維持）。Descriptor/BackendFactory/ScientificEligibilityPolicyを注入し、effective Method config/Target検証、lazy backend import、portable typed DTOのみを返す。

**Common signature contract:** `__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`はMethod/Target/Operation一致を検査しBackend import/外部I/Oを行わない。`preflight`は実データ実行前のMethodConfig/Design/GraphVersion/Backend/Inferenceの適格性を型付き判定する。`execute`は適格Requestのみ、`StagingArtifactSink`へportable finite DTOを渡し、Library Instanceを公開しない。例外：既存Product v2の`RefutationAdapter.run`/`SensitivityAdapter.run`公開署名を改変しない。

### 4.2. Common cross-Port signatures (reuse, not duplicate)

- `IdentificationOutcome.from_evidence(evidence: ValidatedIdentificationEvidence) -> IdentificationOutcome`：識別Proof/Estimand/GraphVersion/hash・nonidentifiedを保持。
- `EstimatorRequest.validate_against(self, identification: IdentificationOutcome, design: CausalDesign, policy: EstimandEligibilityPolicy) -> ValidatedEstimatorRequest`：識別先行・全upstream hashとTargetの一致、未識別/弱識別を拒否。
- `LocalCausalUseCase.preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport` / `run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome`：validated RequestからPort実行・publication。CLIに科学的判断を書かない。
- `LocalRunManifest.to_canonical_bytes(self) -> bytes` / `LocalManifestReader.read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun`：Operation別Inventory、JCS/hash、marker/Readback一致。
- `LocalPrivacyPolicy.authorize(self, *, study: ValidatedStudy, cli_row_flag: bool, root: TrustedLocalRoot, principal: LocalPrincipal, policy: VerifiedStudyPolicyEvidence|None, output_shape: OutputShape) -> PrivacyDecision`：PolicyはCLIから独立した唯一の判断者。

## 5. Per-package mandatory implementation behavior

### 5.1 P01 — Donor pool/Panel Design

Owner: P01。Methods: No new Method ID; cross-cutting。Entry dependencies: NONE。**Pre:** Gate/Package frozen, upstream checkpoint fixed, strict Profile/Method Target consistent. **Required:** preperiod eligibility/contamination/treated unit。**Post:** typed Result/Reason, correct OutputShape/Hash/Backend/seed, package-scoped focused tests and checkpoint. No Gate PASS.
### 5.2 P02 — Synthetic Control Adapter

Owner: P02。Methods: `P3-M12`。Entry dependencies: P01。**Pre:** Gate/Package frozen, upstream checkpoint fixed, strict Profile/Method Target consistent. **Required:** donor weights/RMSPE/placebo/point-only。**Post:** typed Result/Reason, correct OutputShape/Hash/Backend/seed, package-scoped focused tests and checkpoint. No Gate PASS.
### 5.3 P03 — Synthetic DiD Adapter

Owner: P03。Methods: `P3-M13`。Entry dependencies: P01。**Pre:** Gate/Package frozen, upstream checkpoint fixed, strict Profile/Method Target consistent. **Required:** time/unit weights・panel ATT・inference。**Post:** typed Result/Reason, correct OutputShape/Hash/Backend/seed, package-scoped focused tests and checkpoint. No Gate PASS.
### 5.4 P04 — SCM/SDID Result/CLI・独立科学

Owner: P04。Methods: No new Method ID; cross-cutting。Entry dependencies: P02,P03。**Pre:** Gate/Package frozen, upstream checkpoint fixed, strict Profile/Method Target consistent. **Required:** REF-Q04/Q05とnegative。**Post:** typed Result/Reason, correct OutputShape/Hash/Backend/seed, package-scoped focused tests and checkpoint. No Gate PASS.

## 6. Scientific / runtime / failure policy

- 各Methodのstrict Config・Question/Design/Estimand/Inference profileは正式Method IDでdispatchし、Gate IDでMethodを選ばない。必要schema未確定は`METHOD_PROFILE_UNAVAILABLE`などtyped BLOCK。P1-M05のtarget不明などを推測で埋めない。
- Science DGP/NEG/REFは10_32の各行に従い、Backend outputを独立Oracleにしない。K/R/seed/threshold/computeはT2 Pilot→T3事前登録で決定し、未確定を自動数値で補完しない。
- 実効Backend version/API、optional dependency、uv.lockとLicenseの可否は別々に記録。技術的不在と科学的不識別、Inference unavailableは異なるtyped Reason。
- 既存G01 root/no-clobber/fsync/privacyは再利用し、row exportはG05以外で勝手に許可しない。Graph uncertain marksやAR confidence_setはlossless保存、fake Point/CIを出さない。

## 7. Implementation-side verification, assembly, handoff

- 各PxxのDD/METHOD ID・positive/negative・unit/contract/integrationを必要な実境界で検証。テストの実ファイル名/実行commandは40 Operatorがcurrent checkoutから発見。G01 CLI-only等の他Gate固有制約を本Gateに混入しない。
- 既存Product v2 Testsは現配置で実行・保護。新規E11 Testsの初期lifecycleはenhancement、恒久RegressionへのPROMOTEは独立判断。E11中の全repo Test移動禁止。
- Pxxは20 Package reportにcheckpoint full SHA、実path/command、DD ID、fixture/lock/seed/Backend・Observed結果、PASS/FAIL/BLOCKEDを記録。全Pxx完了後Candidate AssemblyがSource chain/実効回帰を監査しFixed Trial Candidate SHAを設定。
- 独立07担当AgentはProduct/Test/Dependenciesを修正せずTest Item/999を判定。Science evidence未実行をPASSとしない。
- **STOP/BLOCKED:** Gate06/07/Pxx未Freeze、上流999未PASS、Version/Target/Schema/Design/Science Oracle不足、Backend/Environment不適格、旧v2互換破壊、fixed SHA不明、未承認Owner選択。

## 8. Owner review items (not implementation claims)

Gate境界・Dependency G01、WORK_PACKAGE modeとDAG、Method/Design/Inference/Backend/License、独立DGP/REF/T2/T3・受入閾値、Reuseと科学的不確実性の契約を一括レビューし、差分承認後にだけFreezeする。**Coding Authorization remains NOT_AUTHORIZED.**
