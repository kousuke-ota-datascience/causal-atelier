# ENH-E11 G08 P00 — Work Package実行計画

**Contract status: DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED**
**Gate: G08 / formally planned G01〜G10 / Trial01 NOT_STARTED**
**Depends on: G01 PASS, G02 PASS — upstream canonical 999 mandatory (DRAFT dependency proposal)**
**Execution Mode: WORK_PACKAGE (DRAFT proposal); Required packages: P01, P02, P03, P04, P05**
**Owner Freeze: PENDING / Coding Authorization: NOT_AUTHORIZED / Baseline full SHA: NOT_FIXED**
**References:** [10_32 Scientific Method Scope](../../00_enhance_background/Revised_requirements_definition_documents/10_requirements_definition/10_32_scientific_method_scope.md) / [30_61 Domain/Ports](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_61_causal_domain_ports.md) / [30_62 Local Execution](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_62_local_execution_publication.md) / [30_63 Method Adapters](../../00_enhance_background/Revised_requirements_definition_documents/30_detailed_design/30_63_causal_method_adapters.md) / [23_41 Scientific Ports](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_41_cli_scientific_ports.md) / [23_42 Artifact](../../00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design/23_42_local_result_manifest_artifact.md)

## 1. Gate boundary and P00 responsibility

Sharp/Fuzzy RDD局所効果と、B0 binary Z/A complier LATE、B1指定Cの加法線形IV構造係数を分離し、weak IV時のAR反転集合を損失なく表現する。

P00はCoding Unitでなく、Package DAG・Entrypoint/Checkpoint・Candidate handoffを管理。Pxxの実装WHATや独立07のACを上書きしない。

## 2. Package DAG

| Package | Responsibility | Depends on | Exit proof |
|---|---|---|---|
| `P01` | RD/IV Design・Estimand適格性 | NONE | cutoff/density/first-stage/B0/B1 target |
| `P02` | Sharp/Fuzzy RD Adapter | P01 | bandwidth/local target/discontinuity/CI |
| `P03` | Wald・2SLS B0/B1 | P01 | binary Z/A、C、robust covariance/first stage |
| `P04` | Weak-IV HC1・AR set推論 | P03 | bounded/unbounded/disconnected/empty/all-real AR set |
| `P05` | RD/IV CLI・Typed Result・科学 | P02,P03,P04 | REF-Q03/E07/E08/U01とv2回帰 |

## 3. Entry and restart

- 全PxxとGate06/07が一意でOwner承認/Freeze済み、DependsOn upstream canonical 999 PASS、実行基準full SHA・Git/remote/lock・Backend/環境・Coding Authorizationを確認する。未成立はBLOCKED。
- Dependency Pxxの20 Package report/checkpoint full SHAを一意に確認。異なるTrialや未承認Sourceとの混在禁止。
- 各PxxのFocused Testと20 status/reportは当該PackageのCheckpointに帰属し、`PACKAGE_READY`をGate PASSと見なさない。

## 4. Final integration and independent test

- 全required Pxx completion後Candidate Assembly AgentがSource/Manifest/Method/Protected regressionを検証しFixed Trial Candidateを1個確定。20 CompletionとSha Chainを残す。
- Independent Test Agentは07のTest Itemsと999を同一Fixed SHAで判定。正式FAIL後だけ08 remediation、契約欠陥は09 amendment/再Freeze。

## 5. Test architecture and stop

- 40が初期`tests/enhancement/enh_e11/<gate>/<layer>/`、実効test discovery/collection、legacy Product suite維持を定める。G01のCLI-only条件を他Gateへ誤適用しない。
- Schema/Reference/Backend/Policy/License未定義はtyped BLOCKED。Owner review未完でCoding禁止。E11 closure時のPROMOTE判断まで`tests/regression/`への自動移動禁止。
