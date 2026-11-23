# Ariadne ENH-E11 / G01 — 07 テスト・独立検証指示書

**DEC-G01-EXEC-01（Owner 2026-11-23採用・G01のみの実施順序変更）:** `combined_review/177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`がG01の従前S09→S10→S11依存を部分的に上書きする。利用不能なPython3.12実測B02/B04、独立S09/B05科学審査は**Coding Entryの必要条件から外し、G01_999 PASSまでの必須受入条件へ移す**。事前Author契約整合と例外Ledgerを材料に、Ownerの**別個の暫定G01-S10 Freeze**、その後Ownerの**別個の限定G01-S11 Coding Authorization**を認める。どちらも現在**未承認**。限定許可はG01/P01–P05の実装・開発者テストのみ。実Python3.12 Schema/FCI、独立MAG/PAG/BK、実FS/Reader、T2/T3、独立07/999、Product v2回帰の要求・合格基準は維持。未検証をPASS扱いせず、non-null BKはFCI呼出前exit4 fail-closed、科学的真値や閾値の自己創作禁止。G01_999がPASSするまで下流Gate依存は解除しない。

**DEC-PREPCODE-01=B（Owner 2026-11-22採用・Gate別Control Plane）:** G01は共通E11 v1のSchema/JCS/ContentRef/Graph、Port/Privacy、Publisher/Reader、安全なFS、既存Product v2互換、P1-M06 FCI専用Config/Question/DesignおよびENV-BASE・独立MAG/PAG科学Oracleを対象に、**G01+共通契約の独立S09監査→Owner G01-S10 Freeze→Owner G01-S11 Coding Authorization**をこの順で取得する。本書の存在・Author静的改訂・全402資料のSHA索引・他GateのS09/S10/S11はG01のindependent verification許可を意味しない。G02以降40 Method/他Optional Backendの未確定はG01固有の停止条件にしないが、共通依存の不整合は止める。G01完成後もreal FS/FCI Adapter/T2/T3/保護Product回帰は独立07/999の実測必須であり、先行してPASSとしない。現時点は**G01 S09 NOT_RUN / S10 NOT_FROZEN / S11 NOT_AUTHORIZED**。

**Contract status: DRAFT / NOT_FROZEN / TESTS_NOT_RUN**  
**Gate ID: G01 (Enhance Workflow Gate)**  
**対象：G01（Graph/PAG/Local CLI基盤）**。本07は**G01の独立検証**であり、Gate G07（DiD/Event/ITS）ではない。  
**Authority:** [G01 06](06_Ariadne_ENH-E11_G01_implementation_instruction.md)／[PREP-02 baseline](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)／[Owner DEC07 定量受入](../../working_notes/20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)／[GRAPH-A判断](../../working_notes/20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)。

## 0. Template verification authority

07はGate Acceptance Criteria authority。Test Item 001はFixed Trial Candidateのfull SHA対checkoutのidentity audit、002〜013は本書G01-07-01〜12に対応。独立Test Agentはproduct/test code、migrations、dependencies、ACを変更せず、実効コマンド・exit・raw evidence・固定SHA・DD ID/ACを記録する。999のみが正式Gate PASS/FAIL/BLOCKEDを判定する。現状の受入境界は再審査中で、本書は未Freeze。

**Gate境界の技術判定（Owner承認前）：** G01は単一のLocal scientific DISCOVER垂直スライスとして保持する。独立した受入軸を混同しない：(A) JCS/FS/atomic publication/Reader（G01-07-01〜06）、(B) FCI/backend適格性と独立MAG/PAG科学Reference（07-08〜10）、(C) Study/Graph/Status Bundle・CLI privacy・既存v2回帰（07-07/11/12）。P02/P04の個別検証成功や科学的negativeをG01全体のPASSへ昇格せず、**共通のFixed Trial Candidate full SHAで全必須受入軸に実測が揃った場合のみ999 PASS候補**。T2 Pilot・T3の定量科学検証はGate PASS前に必要だが、07の設計・独立Oracleの計画が成立していればCoding Authorizationの前提にはしない。**実行・Owner承認・06/07 Freezeは未実施**。

## 1. テスト着手・判定原則

- 06のCoding Entry後、**実際に実装されたSource SHA**に対して独立に実施する。07を先に策定したことをPASSとしない。テストAgentは合否を改善するためにSourceを無断変更しない。
- `PASS / FAIL / BLOCKED`を**テストごと**に返す。動作確認していない環境・FS・Backend API・PAG Oracleは`BLOCKED`、その対象の正式Gate PASSは不可。なお独立レビュー完了記録の追加提出は、G01のテスト着手条件ではない。
- CLIのExit 0は技術的完了であり、`science_acceptance=PASS`とは違う。テスト合格とScience pass、Unit testとMonte Carloは分離する。
- **数値検証：** Owner採用のDEC07方針（既知型/serialization一致=100%、stochastic K/FWER=.05、必要R/Compute Budgetは独立Pilotから）を適用する。実効K/R/Computeの架空設定はしない。**Coding Entryは計画設計を完了していれば可能**だが、G01科学的999 PASSを出す前にT2 Pilot→独立PAG reference→T3事前登録が必要。

## 2. Required verification layers and lifecycle authority — not physical test paths

**本07は WHAT のauthority:** Required behavior / DD ID / negative and positive cases / primary proof layer / pass-block-failの根拠。具体的なテストファイル名・配置・実行コマンドは受入条件ではない。ENH-E9 [test architecture handoff](../../../20260905_ENH-E9_workflow_stabilization/00_enhance_background/08_test_architecture_migration/09_handoff_to_enh_e11.md)と ENH-E11 40 Operator PolicyがWHERE/HOWを所有する。

**二軸:** Lifecycle = enhancement / regression / characterization / benchmark / support / legacy; verification layer = unit / contract / integration / frontend / browser_e2e。新規G01テストはenhancement lifecycleから開始する。`component` / `scientific`を正規G01 layerと見なさない。`scientific`は対象科学分野または再利用可能なcharacterization/benchmarkの用途であって、このGate固有のテスト階層を増やす根拠ではない。

| G01 Verification Item | Primary verification layer | Mandatory evidence |
| --- | --- | --- |
| 07-01/03/04 Study/Graph/JCS pure invariants | unit + contract | exact schema, bytes, lossless, negative |
| 07-02/05/06 Trusted FD, atomic publication/readback | contract + **real Linux integration** | actual root/OS/FS behavior; mocks alone insufficient |
| 07-07/11 DISCOVER Bundle, CLI, Privacy | contract + integration | E11 end-to-end no row/Effect, typed status/exit |
| 07-08 FCI config/API/BK eligibility | contract + effective backend integration | real selected distribution/API and CI execution |
| 07-09/10 independent MAG/PAG scientific reference | deterministic contract + real backend integration + independent reference evidence | Graph-A compelled/uncertain endpoints, BK/latent negatives |
| T2 Pilot / T3 stochastic science | preregistered independent scientific verification with executable integration/contract assertions | actual K/R/seed/compute/effect measures, not a mock or orphan benchmark |
| 07-12 Product v2 compatibility | current existing test suite at its actual current layer + G01 integration regression cases | no change to legacy behavior; keep existing tests in place |
| Test Item 001 candidate identity | independent provenance audit | exact SHA + actual resolved checkout |
 
**Life-cycle:** A newly authored test that checks old Product behavior remains `enhancement` until a recorded semantic PROMOTE decision. Existing `tests/product/` and other pre-migration suites are acceptable current evidence locations. End-of-ENH-E11 disposition is explicit `PROMOTE/REWRITE/MERGE/SPLIT/RETIRE/ARCHIVE/KEEP_ENHANCEMENT`. Do not create or populate `tests/regression/` just to label an assertion. Full estate migration is ENH-E12+.

**CLI-only G01:** No Browser UI journey and **no mandatory Browser E2E**. Scientific correctness belongs to independent MAG/PAG reference and statistical tests, not Browser proof. Real OS/FS and backend must still be exercised.

**Execution evidence:** The 40 Independent Test Agent discovers actual current tests (G01 enhancement first, then relevant existing Product/legacy suites, any approved regression/benchmark sets), verifies their existence, pytest collection and runner/environment, and records actual path/command/candidate SHA/fixture/env and DD IDs **as evidence only**. A past test path is not the 07 normative test authority. Never silently exclude a mandatory DD case because the expected filename is absent: distinguish `BLOCKED` test-side infrastructure/collection issue from `FAIL` demonstrated product violation.

**Execution order:** First pure deterministic/contract assertions, then real filesystem/CLI/backend integration, then independent scientific Oracle and appropriately designed quantitative evidence. Required fixed candidate and independent Gate test rules in `1, `3–6 remain unchanged.

## 3. Deterministic/Contract Matrix（12件）

| Test | 正例／負例 | PASSの観測条件（実結果を記録） | 詳細設計Class.MethodとDD検証ID |
| --- | --- | --- | --- |
| **G01-07-01 Strict Study+dispatch** | Schema v1、P1-M06 only、**Question/Design G01内部Profile**、question_idとStudy.identity一致、Designの変数名・Dataset列順・CI type照合、BK Study/Design一致。duplicate YAML/JSON key、unknown fields、旧Product`causal-analysis-spec/2`、G02 Method指定 | 正例parse。未知・旧版・余剰config/不一致→exit2。旧Product v2は別入口で成功し挙動不変 | 30_60 `9 `LocalConfigDecoder.decode`：SPEC01〜04；30_62 `1：RUN03/04 |
| **G01-07-02 ContentRef and Root** | Regular input same root、../、/abs、Windows separator、symlink/hardlink、hash不一致、違うowner/unsafe local FS、race | 元FDの実bytesとSHA一致のみ許可、root外open 0、破損/不正入力exit3 | 30_60 `11 `ContentRef.from_payload` / 30_60 `10 `ContentReferencePort.verify`：REF01〜04；30_62 `3：PUB06、`5：READ07、`6：PRIV03/06 |
| **G01-07-03 Graph/PAG fidelity** | `o-o`, `o->`, `--o`, `->`, `<->`、source/target swap、Graph content hashとProduct Version ID不使用（Local version_id/parent_version_id=null）、Self-loop/duplicate/unknown node/unknown endpoint | 全定義済みendpoint pair・version/parent/lag=nullの**100% roundtrip**、DAG化なし、GraphEvidenceはrevisionを作らずProduct writerのみVersionを発行、INVALID拒否 | 30_61 `1 `GraphEvidence`：GRAPH01/03/04 |
| **G01-07-04 Canonical JCS** | 用意済み7 positive+7 negative vectors、UTF16 sort/NFC-NFD/大値/-0、duplicate/NaN/nonfinite、Graph self digest | Python出力と事前固定の独立RFC8785期待値の**実bytes一致**、それぞれSHA256一致、Hashの対象混同0。既知JSON文字列をhashするだけではPASS不可 | 30_61 `1 `GraphEvidence.canonical_payload`：GRAPH01；30_62 `4 `LocalRunManifest.to_canonical_bytes`：MAN01〜03 |
| **G01-07-05 Atomic publish** | 同run_idの2 process競合（same/different request hash）、EEXIST、ENOSYS/EINVAL/EOPNOTSUPP/EXDEV、rename/fsync前後SIGKILL、既存不正run | No-clobber=**0 overwrite**、同一hash再利用は完全readbackだけ、post-rename不定はCOMPLETED 0件、fsync/reader実証 | 30_62 `3 `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`：PUB01〜05/PUB07〜09 |
| **G01-07-06 Bundle readback** | Complete manifest/marker/status/graph/study、marker欠損/破損、run ID/Hash/Method違い、duplicate key、symlink、unsafe owner/mode | 有効なもののみ`VerifiedLocalRun`、保存破損はexit5、検査できないFS種別・owner/modeはBLOCKED（schema parseだけでPASSにしない） | 30_62 `4/5 `LocalRunManifest/LocalManifestReader.read_run`：MAN01〜05、READ01〜04/07、PUB07〜09 |
| **G01-07-07 DISCOVER-only envelope** | `P1-M06`成功/合理的科学的負結果、Missing Graph時はdiagnosticsとnonempty reason、no Effect file、`schema_dispatch.result=null`、Study.graph=null | No dummy Effect、Graph成功/科学的negativeのOperation別Bundle inventoryを検査。Registry→DiscoveryPort→FCI AdapterのMethod/Capability一致、UseCase ContextのTrustedRoot/実効Principal保持を確認。StatusはIdentification NOT_APPLICABLE/Point NOT_REQUESTED/Inference NOT_REQUESTED/Science NOT_EVALUATED、cross-file hash一致 | 30_62 `1/4 `LocalCausalUseCase.run(spec,context)/LocalRunManifest`：RUN01、MAN03/04；30_61 `1/5.5：GRAPH01、DISC01〜03 |
| **G01-07-08 FCI API and eligibility** | 実効Python3.12 `causal-learn`のFCIで`node_names`を明示して観測Dataset列名に一意対応させ、`fisherz/chisq/gsq`の**各方式の**適格入力・正例fit、およびmissing/nan/constant/n<p／Method違い／混合scale／`chisq/gsq`への非整数・浮動小数カテゴリ／宣言カテゴリとDataset値の矛盾／十分なカテゴリ・条件付けsupportを欠く場合の負例を実測。Backendの`Chisq_or_Gsq`が`np.unique`で任意観測値を内部再符号化する動作に依存して、非整数入力を暗黙カテゴリ化してはならない。Ariadneのstrict preflightはBackend呼出**前**にtyped拒否し、サンプル不足・support不足の閾値と適用条件はOwner採用の科学契約・独立Referenceに基づいて固定する（未承認の数値閾値を補完しない）。`0.1.4.8`リリースタグ上のsignature/`node_names`はAuthor静的確認済みだが、実環境のimport/fit結果ではない。| GraphNode/Edge名とDataset列順1:1、CI適格・Backend evidenceを確認。黙示デフォルト/PC fallback、stdoutの追加出力、虚偽の科学PASS 0件。 | 30_62 CAP01/04/05；30_63 METH-P106 |
| **G01-07-09 GRAPH-A reference** | 小さな**3変数以上**のDAGとlatent付きMAG、Oracle PAGの強制endpointと未確定endpoint、複数seed/依存variant | 独立に導出したPAG/MAG同値類の正解と比較。Backend自身のGraphを教師にしない。DGP母集団truthと推定Graphを分ける | 30_63 `1.3/4.4 `FciDiscoveryAdapter.execute`：METH-P106（GRAPH-A独立Oracle）；30_61 `1：GRAPH01/03 |
| **G01-07-10 BK and latent negatives** | 2変数latent confounderの不可識別性、required/forbidden矛盾、Issue #266の非強制TAIL過剰確定motif、および**BK空配列objectでも出る `fci_orient_bk` print**の静的既知負例。`verbose=false,show_progress=false`だけではstdout封止にならない。 | 現行`0.1.4.8`では**全非null BKを適格性判定時に`BACKEND_SEMANTICS_UNVERIFIED`/exit4でFCI呼出前拒否**、`--json` stdoutは余剰行0、node名漏洩0。BKを実行可能と宣言するには独立MAG/PAG motif と stdout/log containment の両方の実測・独立承認が必要。 | 30_63 METH-P106；30_61 GRAPH03 |
| **G01-07-11 CLI error/privacy** | `--check-only`零書込、Study row request、bad hash、bad config、backend failure、corrupt readback | exit2/3/4/5をphaseごとに検証。実効principal/root/owner/modeの不一致でdenyし、個票・secretのlogs/stdout/staging漏洩0。非Effect科学的負結果と技術失敗を混同しない | 30_62 `1/6/8.5 `UseCase/LocalPrivacyPolicyPort.authorize/command.main`：RUN07、PUB07、PRIV01〜06、READ03 |
| **G01-07-12 Product & scope regression** | 現存する旧Product v2 CLI/Scientific Coreテスト群（実効PathはOperatorが発見）、既存discovery/identify/estimate/refute/sensitivityとResult v2、G01外Method | legacy`manifest_version=2.0`・旧CLI output semantics不変、Product DB/Web/Worker Source不変、G01外Method変更0 | 30_62 `1/3/4/5/8.5 `command.main/Manifest/Reader`：RUN06、PUB10、MAN06、READ06；30_61 `4：EFF05（旧v2回帰のみ） |


**G01-07-08 category-domain authority/compatibility addition — DEC-G01-P04-CATEGORY-DOMAIN-01=A:** Independently validate the **actual strict P1-M06 Design schema and parser**, not a mock-only predicate: CATEGORICAL with [0,1] (full balanced support) accepts structurally; missing `category_codes` rejects; [0,1,2] with observed [0,1] fails due to missing declared cell/stratum; [0,2] is valid noncontiguous coding when support is adequate; duplicated, nonascending, fractional, JSON lexical `1.0`/`1e0`, boolean, string, out-of-range/nonrepresentable integer codes reject without coerced equivalence; CONTINUOUS with `category_codes` rejects and ordinary continuous remains valid. Reject undeclared Dataset code, missing values, incorrect Design column order/name, zero-row declared S=s even if unconditional marginal table passes, and all X/Y declared levels missing from margins; all rejects cause zero FCI calls and no Graph/staging/Marker. Test S=empty plus all subsets through p-2, and exact E=5/E<5 using independently calculated counts. Verify no fallback to the earlier `e11_g01_design_evidence_profile.schema.json`, and verify modified Design actual SHA + JCS Study request_hash + Graph provenance ContentRef equality; stale hashes reject at their existing boundaries. The internal Design compatibility tightening is explicit; unchanged P01/P03 code and published Study/Graph schema versions retain protected regression. No staged row values or unjustified science PASS. Keep 07-09/10 and G01_999 unchanged.

**G01-07-08 independently specified A eligibility acceptance:**

### DEC-G01-P04-CI-ELIG-01 — Owner adopted A: conservative exhaustive CI preflight (formal 09/S10/S11 pending)

For G01/P1-M06, before invoking the FCI backend, enumerate every unordered pair (X,Y) from the p ordered observed variables V and every S subset of V excluding X,Y, including the empty set and |S|=p-2. The required count is C(p,2)*2^(p-2). The FCI Possible-D-Sep stage in the pinned causal-learn 0.1.4.8 source may inspect conditioning sets beyond the user-configured adjacency-search depth; neither depth nor max_path_length may truncate this preflight. This screening is a deliberately conservative sufficient G01 policy, not a claim that FCI uses every triple.

- fisherz (DEC-G01-P04-FISHERZ-NUMERIC-01=A, Owner-adopted 2026-11-23; formal AMD-003/S10/S11 pending): require declared continuous, complete, finite, nonconstant numeric observations, and n > |S|+3 for **every** unordered X/Y pair and every S subset, independent of depth. Use the verified ordered Dataset in effective Backend-compatible **float64** and its complete-sample correlation matrix R_full computed compatibly with pinned causal-learn FisherZ's np.corrcoef(data.T); each R=R_full[np.ix_([X,Y,*ordered(S)],[X,Y,*ordered(S)])] is the exact submatrix for that CI test, not a differently rounded per-subset recomputation. Before any FCI invocation, verify every R has finite entries, strict positive definiteness (successful Cholesky), and finite 2-norm condition number kappa2(R) such that **kappa2(R) * np.finfo(np.float64).eps <= 1e-6** (eps denotes 2.220446049250313e-16, *not* epsilon/2). Compute the float64 inverse W of the same R; require W finite and **max(||R@W-I||_inf, ||W@R-I||_inf) <= 1e-8**, where ||M||_inf is the maximum absolute row sum, and both products must be finite. With ordered X,Y as the first two indices, require finite positive W[0,0]*W[1,1], finite r=-W[0,1]/sqrt(W[0,0]*W[1,1]) and strict **abs(r) < 1**, and finite Fisher-Z transform/statistic/p-value intermediates when computed. Use no clipping of abs(r)>=1 into acceptance. Every inequality is inclusive at its stated threshold; a failed/NaN/Inf/overflow check, algebraic singularity, negative or zero pivot, incomplete scan, or numerically undecidable result is typed pre-FCI reject/eligibility-unresolved, with **zero FCI invocation**, no fabricated Graph/Marker and no SCI_NO_ADMISSIBLE_PAG. The two numeric thresholds are conservative Owner-approved eligibility heuristics, **not** verified inverse forward-error or p-value accuracy guarantees, nor proof of Gaussianity, observation independence, Markov or faithfulness.
- Independent G01-07-08 Fisher-Z numerical matrix (DEC-G01-P04-FISHERZ-NUMERIC-01=A): independently compute the complete-data float64 correlation and every ordered (X,Y,S) submatrix; verify Cholesky, condition2*float64 eps **<=1e-6**, both float64 inverse residual maximum absolute row-sum norms **<=1e-8**, finite inverse and strict abs(partial_r)<1. Verify inclusive equal-threshold decisions via independently constructed matrix examples/tolerance-free comparator controls (do not assert a continuous synthetic sample equals an exact numerical threshold by rounding), well-conditioned positive with actual effective FCI fit separately, n=|S|+3 rejection vs |S|+4 conditional positive, rank deficient, nonfinite, numerical inverse failure, near-singular cases that successfully invert but breach the condition budget, cases that breach only residual, cases where partial_r is >=1 or nonfinite, depth=0 with later S and incomplete scan (all preflight rejects cause zero backend calls). As regression examples, epsilon=1e-4 may satisfy the condition criterion while 1e-6 and 1e-7 violate it; **this is not proof of global all-S eligibility**, and inverse residual and other checks remain independent. Independently check the norms as max row sums (not entrywise max), and distinguish np.finfo(float64).eps from unit roundoff. Reject any reliance on causal-learn's abs(r)>=1 clipping, and do not infer reliable p-value accuracy from pass. Preserve all G01-07-08/09/10 and G01_999 conditions.
- chisq and gsq: require exact integer-coded categorical values compatible with declared category domains; Backend implicit recoding does not validate them. For each triple and each declared conditioning category combination S=s, require positive stratum count, nondegenerate X-by-Y contingency table with positive degrees of freedom, and null-independence expected count E(x,y|s)=N(x,+|s)*N(+,y|s)/N(+,+|s) >= 5 for every declared X/Y cell. Empty/unsupported strata, a zero-degree table, or any expected count below 5 are ineligible. The adopted A proposal treats 5 as a conservative G01 screening floor, not a universal statistical validity guarantee.
- Exhaustive review must finish; absent verified resources, exhausted budget, unresolved category domain or unstable numerical matrix gives a typed eligibility-unresolved/technical block before FCI. Never truncate, skip difficult triples, silently switch CI, or label error SCI_NO_ADMISSIBLE_PAG. No new public wire/exit code is authorized. A fixed maximum-p/resource limit or numerical stability tolerance, if necessary for deterministic positive eligibility, remains a separate specification requiring justification.
- Log only non-row eligibility evidence: method/CI, p,n, total and examined triple counts, aggregate minimum expected count, typed reason and evaluation completeness; no raw observations, secret values or variable-name leakage in CLI JSON. Non-null BK remains pre-FCI rejected as separately agreed. Passing these screens is not FCI fit, independence-assumption verification, correct PAG, or independent science acceptance.

Independent tests must cover FisherZ n=|S|+3 (reject) and n=|S|+4 (only algebraically sufficient), singular/near-singular matrices, discrete E=5 versus E<5, fully supported and marginal-only-supported categorical tables, declared empty strata, depth=0 with possible larger FCI conditioning sets, wrong categorical codes, incomplete enumeration and zero Backend invocation on all preflight failures. Keep G01-07-09/10 and G01_999 obligations unchanged.

**P01 evidence factory / G01-07-06/07 pure and readback joins:** Require valid `ValidatedRunEvidence` factory examples for both Graph-positive and justified Graph-negative with exact Study↔Status↔Manifest run_id equality, Study JCS-derived `request_hash` equality to Manifest/Marker (Status has no `request_hash` field), exact Status `manifest_relative_path="runs/{run_id}/manifest.json"`, five-field Question/Design/Dataset lineage equality, positive `manifest.lineage.graph` TrustedRoot-relative `runs/{run_id}/graph.json` ↔ bundle-relative `graph.json` Descriptor prefix mapping and SHA/media equality, and negative null Graph+typed diagnostics. Synthetic P01 negative must use exactly SCI_NO_ADMISSIBLE_PAG in the tuple and Status; reject BACKEND_API_MISMATCH, BACKEND_SEMANTICS_UNVERIFIED and other technical codes even when repeated in both, unknown SCI_*, mixed/duplicate codes and nonempty positive Status reasons. Pure synthetic acceptance cannot establish real P04 provenance; no actual science-negative publication unless independent Method proof exists. Reject a mismatched output Graph Ref (including incorrectly treating bare `graph.json` as TrustedRoot-relative or confusing semantic content_hash with exact file SHA), missing/extra/duplicate Artifact, mistaken Study input Graph-as-output, status mismatch, incorrect Method, row artifact and self-referenced Manifest/Marker. P01 tests check pure values; real P02/Reader test must confirm the actual FD bytes, upstream schema, Graph provenance and publication separately. Existing acceptance criteria are not relaxed.

**P02 PrivacyDecision binding (G01-07-05/06/11, PUB04/07, PRIV01–06):** Positive exact same run/hash/live-root EUID and aggregate-only staged inventory, facade seal forwards unchanged decision to concrete validate(manifest,*,privacy), concrete independently recomputes injected Policy. Negative missing/denied/forged decision, allow for another run/hash/root fd (including equal path string)/UID, changed Study/manifest, altered or extra restricted row Artifact, Policy disagreement and stale root all reject before Marker/rename, with no COMPLETED, row data or science-negative substitution. Pure mocks do not satisfy real FD/FS acceptance.

**B03 strict cross-wire negatives (G01-07-02/06):** Use an actual marked/manifested run after Coding Authorization and actual Linux FS. Positive marker→Manifest→Study/Status/optional Result/Graph/sidecar must be independently readable; negative variants are `manifest.execution.technical_status` mismatching `status.technical_status`, any unknown technical_status string (e.g. `SUCCESS`), stale Manifest/marker byte SHA, duplicate inventory key, internal scientific ContentRef.relative_key `../outside`, `/absolute`, `dir//file`, `dir\\file` or NUL, symlink swaps and unjustified private row bytes. Reject at appropriate schema/Reader boundary; absence of a source path leak is required. These are **post-authorization Gate test obligations**, not a claim of pre-code S05-B03 runtime PASS.

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
3. `Serialization/typing`: PAG辺のendpoint・Local科学的親provenance・Product version_id/parent_version_id=null・JSON/Manifest全Hashの定義済みFixtureは**100%一致（false authorization 0）**。ここはstochastic測定と独立して合否確定。
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
| AC-01 | Study/ContentRef/Version/Method Config strict integrity | unit + contract; FD security in integration |
| AC-02 | Lossless PAG/Local graph identity and strict JCS hashes | unit + contract |
| AC-03 | Linux same-FS no-replace atomic publish/readback/privacy | contract + real Linux integration |
| AC-04 | Effective FCI/CI/BK validity and independent MAG/PAG oracle | contract + real backend integration + independent scientific evidence |
| AC-05 | DISCOVER-only status/result semantics; v2 regression | contract + integration; protected legacy suite at current physical location |
| AC-06 | Candidate identity, protected contracts, full evidence | independent provenance audit, not filesystem test layer |

Test Item 001 = Candidate identity audit; 002〜013 = G01-07-01〜12 in §3; 999 = independent Gate Decision. Actual Test Path and command exist only in Operator/Execution Evidence, not in the normative AC. CLI-onlyでBrowser E2Eは対象外。固定候補/環境/独立Referenceを検証できないならBLOCKED、MUST違反を実証したらFAIL、全MUST実測成立の場合のみPASS。

### Owner SIM-01/02 scope cut (2026-11-21, current G01 contract)

G01 supports non-root Linux effective UID owned private local ext4/XFS with directory 0700, file 0600, safe dirfd/O_NOFOLLOW, no path traversal/symlink escape and same-FS no-clobber publication/readback. Separate ACL/xattr-digest, statx mount-ID/namespace visibility attestation, and CI/container heuristic detection are **removed** as mandatory proof. This does not protect against root or same-UID actors. Retain real path/UID/mode/FS positive and negative tests. Strict RFC8785 JCS codec and all SHA256/semantic/version checks remain, but **external ECMAScript execution and Python-JavaScript parity as a blocking test are removed**; compare exact bytes to independent RFC8785 golden expectations. The independent FCI/PAG science oracle and all F03 atomic Publisher/Reader tests are unchanged. Historical PREP02 decisions are superseded solely within SIM-01/02, combined_review/131. No runtime tests, Gate999 or Coding Authorization are authorized.


## S02-01/02/06/07 対象Gateの確定契約（Owner採用・未実装）

G01は`P1-M06`のDISCOVERのみで、個票の出力を常に拒否する。Valid Studyの`privacy.row_export_requested=false`（省略の扱いはstrict Study schemaのdefault/requiredに従う）を要求し、trueはPrivacy exit3。廃止された追加CLI row許可flagを登録せず、渡された場合は不明オプションとしてconfig exit2。Contextは`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`であり、署名Policy/Study policy_refは存在しない。G05のみStudy単独opt-in（true）とOS/Method制約の全件ANDを満たす個票中間出力を担当する。

新Local Graphのimmutable identityは内容hash、parent/source科学証拠とContentRef。Product GraphVersion DBへlookup/write/edit/FIXせず、現行E11 Graph wireの`version_id`と`parent_version_id`はどちらもnullとし、non-nullは未対応importとして拒否する。既存ProductのGraphVersionServiceや旧v2は無変更。

OS/FS受入は有界な不変条件別の正負例（owner EUID・0700/0600・dirfd/O_NOFOLLOW・same FS・symlink/race・rename前後・post-rename indeterminate・Marker/Reader/hash）に限定する。冗長なfault-permutation全順列、statx mount-ID/namespace証明、ACL/xattr digest/コンテナ推測、電源断耐久保証は追加しない。JCS RFC8785 golden bytes、no-clobber、公開後整合性、独立PAG Science Oracleは維持する。Coding Agentが未承認の広いProof強化を推測で復活させない。


### P02 privacy authorization parity and evidence classification

NFR-030/031 ↔ LDD 21_23/21_40 ↔ BD 22_09/22_12 ↔ IF 23_41/23_42 ↔ DD 30_62 ↔ G01/P02-P05 06 ↔ G01 07-05/06/11. Required contract tests include a positive same-run staged aggregate and negatives for wrong run/hash/root FD/EUID, stale/forged/denied/missing PrivacyDecision, changed Study or inventory, restricted row output and disagreed publisher policy. These are developer/G01 independent 07 proof obligations: real FD/root/no-clobber/Reader behavior needs actual Linux testing, while pure port mocks do not establish G01-07-05/06 PASS. Requirements and implementation instructions have no separate competing PrivacyDecision contract.


### G01 07-05/06/11 decision equality: positive and negative oracle

Required positives: (A) a genuine P05-issued, immutable all-field valid aggregate Decision, and (B) a **separately instantiated object of the same type with every field identical**; in both cases the Publisher's trusted current Policy, staged Study, live root FD, UID and exact aggregate inventory must allow, and normal seal/publish/readback applies. Required negatives: change each field (`allowed`, run ID, JCS request hash, verified root FD identity, UID, classification, row flag, output shape), alter staged Study/inventory, deny independently evaluated policy, or attempt to substitute untrusted caller policy; assert no Marker/rename/COMPLETED and typed rejection. **Do not assert rejection of a fully value-identical Decision solely because it is reconstructed.** `forged` cases elsewhere in 07 mean detectable mismatch or re-evaluation bypass, not object-origin provenance. Actual FD/FS/Reader tests and independent G01_999 remain unwaived.


### G01-07-06/07 Graph-negative strict diagnostics acceptance matrix

**Positive envelope (synthetic pure fixture only, not evidence of genuine FCI SCI-negative):** Graph-negative DISCOVER/P1-M06 with staged `diagnostics.json` strict four-field object `{ "run_id": valid_run_id, "operation": "DISCOVER", "method_id": "P1-M06", "reason_codes": ["SCI_NO_ADMISSIBLE_PAG"] }`; Status/Manifest run and reason match, Status technical_status COMPLETED, null Graph schema dispatch/output lineage, exact study/status/diagnostics inventory and real descriptors. **Negative cases:** `{}`; missing/extra field; unknown/wrong Method/Operation; invalid run_id; wrong/duplicate/empty/multi reason; Status and Manifest reason mismatches; duplicate JSON keys; invalid UTF-8/top-level non-object; wrong graph/diagnostic coexistence; technical/backend error reported as SCI-negative; changed physical bytes despite matching/stale Descriptor; failed pre-rename Typed validation. Assert no Marker/rename/COMPLETED on Publisher rejection; committed corrupted diagnostic Reader returns existing typed readback error. Require strict G01 internal schema profile `23_api_interface_design/schema_drafts/internal_scientific/e11_g01_discover_negative_diagnostics_draft1.schema.json` and independent actual Linux FD/Reader evidence. Do not use method diagnostics for P1-M12–20 or elevate synthetic negative fixture to scientific truth; G01-07-09/10/B05 independent science remains mandatory.


### G01-07-03 P03 typed provenance and P02 Reader compatibility test addition

Positive G01/P1-M06 Graph: exact six-field `provenance` object with method `P1-M06`, backend `causal-learn`, CI equal Study.method.config.indep_test, unique declared assumption labels (without claiming validation of scientific truth), source refs strictly equal Study/Manifest question/design/dataset refs and backed by real verified bytes, null initial scientific parent and Product Version IDs, valid internal semantic `content_hash` and distinct exact-file ContentRef SHA256. Negative: `{}`/missing or extra provenance field, duplicate assumptions, method/backend/CI mismatch, each source ref substitution or wrong hash, missing/unsafe parent, invented Product Version ID, cycles and incorrect comparison of Graph semantic hash with full file digest. Existing independent Graph Endpoint/PAG scientific tests remain. Explicit P02 compatibility regression: before any G01 Gate PASS, the committed P02 Reader must reject a Graph whose provenance is invalid even if the payload has a recomputed matching Graph.content_hash and external file digest. Current P02 Reader only accepts arbitrary provenance dict; a separate Owner approval is required for any necessary modification to that completed implementation. These expectations derive from the agreed A contract, **not from the current P02 code behavior**.
