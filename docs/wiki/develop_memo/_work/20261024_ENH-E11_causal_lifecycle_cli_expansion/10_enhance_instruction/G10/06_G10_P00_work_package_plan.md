# ENH-E11 G10 P00 — Work Package Plan (DRAFT)

**Gate:** G10 / Official Enhance Workflow Gate  
**Class:** Planning/Operator Artifact, not Coding Agent's normative package  
**Plan status:** OWNER_REVIEW_APPROVED / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Gate06:** [Implementation Contract](06_Ariadne_ENH-E11_G10_implementation_instruction.md)  
**Gate07:** [Independent Verification Draft](07_Ariadne_ENH-E11_G10_test_instruction.md) / DRAFT / NOT_FROZEN / TESTS_NOT_RUN  
**Owner-approved execution mode:** WORK_PACKAGE / P01,P02,P03,P04,P05  
**Owner-approved upstream dependency:** G01 PASS, G02 PASS, G03 PASS, G04 PASS, G05 PASS, G06 PASS, G07 PASS, G08 PASS, G09 PASS。2026-11-18 JST Owner一括レビューで承認。各上流canonical 999 PASSは未成立、Runtimeで別途検証する。

**Owner review:** PREP-03 Final AuditのOD-04（G10 Gate Dependency / Required Packages / Package DAG）を承認。Planの承認はGate06/07 Freeze、Owner Coding Authorization、Agent実行を許可しない。科学Method・Privacy Authority・Row Writer等のOpen Decisionを維持する。参照：[`PREP03_final_audit.md`](../PREP03_final_audit.md) §6。

## 1. Gate semantic acceptance

41 Method/10 UCの有効独立科学証拠を全件照合し、影響分のみ再実行してManifest/依存/旧v2互換を統合する。

**主要不確実性:** 各GateのScience999を省略しない。GPLの顧客配布時の手動License審査は内部分析Gate外。

## 2. Package ownership map

| Package | Scope | Required Pxx deps | Method | Package obligations |
|---|---|---|---|---|
| P01 | registry_lock | NONE | — | 41 Method Registryと4必須Environment Profile（BASE/DOWHY/ECONML/TIGRAMITE）、uv.lock/effective API/optional extrasを検証。ENV-COMBINED同時導入・SBOM生成・配布承認サービスは初期Gate必須でない。 |
| P02 | operation_matrix | P01 | — | DISCOVER/IDENTIFY/ESTIMATE/REFUTE/SENSITIVITY/DIAGNOSEのMethod×Estimand×Backend×CI。 |
| P03 | replay_manifest | P01,P02 | — | JCS semantic hash/Graph self hash/ContentRef bytes/Manifest marker bytes別値、readback/atomic no-clobber。 |
| P04 | science_benchmarks | P02,P03 | — | 全41のDGP/NEG/REF、FWER=.05、独立K/R/Compute/coverage/MC-SE。未測定をPASSにしない。 |
| P05 | compatibility_evidence | P03,P04 | — | 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy/license evidence・顧客Legal非認定。 |


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row ParquetはStudyの`privacy.row_export_requested=true`による単独opt-in、Linux非root実効EUID所有private ext4/XFS root（0700/0600、owner/mode/local ext4-XFS/同一FSを検証）、Method別ApprovedRowSchema/ordered column/row/byte/memory capsに合致する場合だけ、認可後の`RowEffectsParquetWriter`がG01 StagingSinkに遅延生成する。初期denyはexit3/Source反復0/row bytes0。署名鍵・独立承認者・失効はOwner 2026-11-21限定改訂で不要。G01 Publisher/Readerが唯一の公開/readback authority。実FS/Parquet/Method RowSchemaの実測未完はBLOCKED。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer delivery legal acceptance（配布時のみ）を意味しない。

## 3. Execution DAG and handoff

- `P01` <- NONE
- `P02` <- P01
- `P03` <- P01,P02
- `P04` <- P02,P03
- `P05` <- P03,P04

Each Pxx→focused verification→20 Package Report→Checkpoint SHA。全required Package完了→Candidate Assembly→Gate-wide self-verification→single fixed candidate SHA→Independent 07→canonical 999。Package Completed≠ReadyForTest≠PASS。

## 4. Governance / Coding Authorization

P00は独立受入条件でも実装許可でもない。06/07 Freeze、Owner採用のPackage list/dependency、上流Gate canonical 999、実基準SHAとenvironment preflightが揃うまでPxxは実行禁止。Issue、Package結果、P00の状態を999代用にしない。
### Owner SIM-01/03/04 initial-Gate simplification (2026-11-21)

Mandatory integration profiles are ENV-BASE, ENV-DOWHY, ENV-ECONML and ENV-TIGRAMITE, each with actual lock/distribution/API smoke and Method-specific science/reproducibility checks. ENV-COMBINED all-extras runtime/CI is an optional later interop check, **not** G10 initial PASS dependency; do NOT claim simultaneous all-extras environment is verified. Local scientific Manifest has NO required `runtime.sbom_ref` or `review.legal_delivery_status` (the active Draft 2020-12 Schema removed them); installed distribution/version/lock source provenance and independent science review evidence remain required. SBOM generation, per-customer authorization state and legal evidence are NOT G10 CLI runtime functionality. Prior to any actual customer external delivery, the Owner/legal reviewer must manually review actual shipped dependencies and block unapproved distribution. FS privacy boundary is ordinary nonroot Linux EUID/private owner-only ext4/XFS root with 0700/0600 and FD-safe paths/same FS; no separate ACL/xattr digest, mount namespace/ID proof or CI/container classification. Preserve G01 Publisher/Reader, NFR-030/031/032/033/035/036, all science, all Method ID targets, upstream Gate999 independence and Product v2. Historical DEC08/PREP02 remains historical, specifically superseded by combined_review/131. No runtime evidence / Gate999 PASS / Coding Authorization.


## S02-01〜08：G10 全Method証拠・差分再実行の正規契約

G10は41 Method全件（P1=20/P2=8/P3=13）の独立DGP/NEG/REF、Method別Schema/Estimand/Inference、Backendとsource+fixture SHA、T2/T3事前登録・FWER=.05、上流999を検証する。**全件を無条件に数値再実行する要求はない**。承認済み独立証拠について、Method code、shared scientific kernel、Method Registry/descriptor/schema、ports/validation、依存コード/ABI、Python/uv.lock/extra/Backend distribution+version、fixture/DGP、negative、Oracle/reference source、seed/quantitative AC/protocol、privacy・Result/Manifestが科学的結果に影響し得る**推移的依存閉包**を監査し、厳密に同一のものだけ再利用する。完全な閉包不変証明が欠損・不整合なら再実行し、再実行不能なら該当MethodをBLOCKしてG10_999 PASSを禁止する。新規/変更された評価指標を既存証拠から事後推測しない。最終Fixed Trial Candidate全体のOperation・Method/Estimand/Inference dispatch、JCS/ContentRef/Manifest/Marker/Reader、G05 Study単独opt-in/Privacy、Product v2互換と横断Negativeは毎回独立に実行する。Libraryのsymbol/API存在はScience PASSではない。

G10-07の最小受入集合：同一full-SHA閉包→上流Science証拠再利用の正例、共有Kernel/Schema/lock/Backend/Fixture/REF/Policyの各1点変更→影響Methodの再実行またはBLOCK、依存グラフに未知辺→BLOCK、既存証拠に欠損/科学的FAIL→全41のPASS禁止、未変更41件のScience真値と後続横断統合別軸検証。旧Productの無関係なSuiteは全件無条件再試験せず、protected境界への影響閉包を証明して必要分を実行する。未知影響なら実行またはBLOCK。G05はStudy trueとnonroot same-UID private ext4/XFS/Method別allowlist・row/byte/memory capsのAND、false/省略は個票なし。署名Verifier・PolicyRef・追加CLI許可Flagは実装しない。現行Local Graphは内容hash/由来、Product Version IDはnull、非対応import拒否。40 Profileは共通Schema＋Method overlayを再構成して厳格検証し、未登録/未試験はfail-closed。外販向けLicense Governance NFR-034はDEFERREDだが社内OSS義務は継続。Coding Authorization未発行、B04/B05の実効証拠は未取得。

## S09-R12 P3-M06 ITS output integration invariant (2026-11-22; DRAFT)

P3-M06 output is Method-config dependent: `effect_components=LEVEL` publishes scalar β_L and typed `its_components.json`; `LEVEL_AND_SLOPE` has a non-scalar Result point with `NON_SCALAR_TARGET` and the same typed sidecar carrying β_L, β_S and only explicitly predeclared horizon effects `β_L+hβ_S`. Both must match the current strict P3-M06 Output Profile/Descriptor catalog and the `e11_its_components_draft1.schema.json` draft. G10 must not drop the sidecar when rebuilding the 41-Method Operation/Result/Manifest matrix; preserve checksum/Study/Design/Method identity, request-mode/Status consistency, and independent DGP-014/NEG-023 science tests. Tested marginal HAC intervals do not automatically certify joint level+slope coverage. No arbitrary default horizon, no observed row leakage, no new public wire.

**This package:** P00 sequences P02/P03/P04 separately and aligns to G07 07/999 evidence.

## DEC-S09-P3M04-01 Owner A — G10 cross-Gate capability reconciliation (2026-11-22)

Owner DEC-S09-P3M04-01=A: P3-M04 initial 2×2 DiD ATT is the sole executable positive variant (`design_variant=DID_2X2`) when separately scientifically/backend eligible. `STAGGERED` remains a syntactically recognized but `DEFERRED` future capability. The Method-specific scientific preflight must reject STAGGERED as `SCIENCE_CONTRACT_NOT_AVAILABLE` / `CAPABILITY_UNAVAILABLE` (CLI exit4), never estimating, publishing a successful Effect Result/Manifest or silently falling back to DID_2X2, TWFE or P3-M05. Unknown/malformed variant is validation exit2. The 41-Method count stays unchanged. The G10 41-Method evidence matrix requires independent valid science for P3-M04 DID_2X2 and the deferred-variant negative, **not** a staggered ATT(g,t) executable positive. DGP-013 remains mandatory where applicable to P3-M05, but not as positive P3-M04 STAGGERED. Existing G10 transitive-closure evidence reuse rules remain unchanged.

**Package-scoped action:** P00 integrates P01 registry, P02 Method operation, P03 readback, P04 science, P05 protected regressions with same fixed SHA.
