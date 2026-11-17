# ENH-E11 PREP-01/02 — 実行証跡・Source照合・未完了事項

**Date:** 2026-11-17 JST  
**Classification:** FLOW / PREPARATION EVIDENCE (not Stock design, not independent review)  
**Baseline:** `prototype/ariadne_mvp` at `ca936190c5283af0c2f714597e2d7faf5ba26761`  
**Status:** `PREP01_IN_PROGRESS / PREP02_IN_PROGRESS / ARCHITECTURE_NOT_FROZEN / SCIENCE_NOT_EXECUTED / CODING_NOT_AUTHORIZED`

## 1. ScopeとGateの語彙

PREP-01/02の対象は**ENH-E11全体**の改訂Requirement/Architecture/Interface/Physical Designと科学・環境契約である。初回実装Gateの先行依存を優先してよいが、残りのMethodやAPI/設計Classを対象外としない。DEC09の68 Scope、41 Method、10 UCと採用・後続Dispositionは変更しない。

Enhancement Workflowの**Gate**はAcceptance Contractに対する独立検証・判定の単位という意味に限定する。**G01〜G10**はE11で計画された個別のGate ID、各Gateに属する**06**はCoding Contract、**07**はVerification Contract、**999**はGate Decisionの文書種別であり、G06/G07とは異なる。DEC09/BD01等の「Gate06=実装段階」「Gate07=科学受入段階」という過去の記述は旧表現として残っている。用語の一意性を回復するにはOwner承認済み歴史記録は改変せず、Stock本文・今後の実行指示で「実装工程／科学的受入」と記述する。正式なGate計画・番号の採用は元Workflowと照合してから決める。

## 2. PREP-01：設計書と文書構造の実地照合

| 対象 | 確認できた事実 | 未完了の是正と完了証拠 |
| --- | --- | --- |
| Root Flow | `90,92,93,95,96(rd03),96(rd04),97,98`の8件は工程履歴・Owner昇格決定・レビュー証跡。READMEは混在を既に認識 | 移動前の全参照探索→Flowへの同一内容移管→relative links/anchors更新→元内容SHA一致検証。Owner昇格条件`93`の参照切れ禁止 |
| 23 numbering | `23_20`が全体§4、`23_10`が§5。ファイル番号と読順は異なる。`23_41/42`は別namespaceの§1〜 | グローバル章とLocal独立章の識別を正規化。改名は全リンク更新と一体で実施 |
| 23 operation contracts | `23_10`はProject/Context約11操作のMethod/Path/用途中心。`23_15/19`は比較的詳細 | 全Operationにidentity, path/query/body, typed response/status, auth, lifecycle, error, idempotency, version, trace/testの9欄をsource/OpenAPIで補完。未確認は`UNVERIFIED`、未実装の提案は`PROPOSED` |
| 30 numbering | `30_41`に全体§4/5、`30_21`にも§4、`30_20`は§9後に§2/3 | Global/Local番号の衝突と見出し順を是正。リンク・anchor再検査 |
| 30 Class | `30_01`にOwnerの7区分Templateがあるが、`30_61/62/63`や既存Classはクラス単位で未充足 | 全Class/Protocol/DTOのinventory→1 Classにつき7区分、既存はSource blobと照合、Proposedはfreeze pendingを明記 |
| Requirements | RD03は新44条文、RD04は既存122改訂条文の監査記録がある | 122件の旧正文と改訂正文の逐条semantic diff、44件のFR/NFR/AR→21/22/23/30→Method/Gate traceの再照合は未実施 |
| Verification | Sourceと設計の限定サンプル照合のみ | 全ファイル相対リンク/anchor検査、Source/OpenAPI equality、class inventory coverage、no canonical changes、reviewer evidenceが必要 |

## 3. PREP-02：現行Sourceとの突合（固定blob）

| Current Source | Blob SHA | 観測した現行契約とE11への影響 |
| --- | --- | --- |
| `src/ariadne/interfaces/cli/scientific_stage.py` | `0467a56ceb0e95bd8e4e6a99b844d5f56c7f75c3` | `run_stage`は旧Product analysis-spec validation、`ScientificCoreAdapter`、`CliManifest`を使用。E11のversion dispatch/atomic bundle publishが実装済みとはいえない |
| `src/ariadne/interfaces/cli/estimation.py` | `2f0f95a92d3f29c35476ac49dc0f2c9494972ca1` | standalone estimation、legacy manifest/識別入力を使用。旧科学的negativeと新typed outcomeの意味を無断統合しない |
| `src/ariadne/interfaces/cli/manifest.py` | `97216eca9d777e97f7a5ebd4e248afd31c6b4de0` | `CliManifest` frozen dataclass、`snapshot_schema_version="causal-analysis-spec/2"`、`to_dict=asdict`。新Local Manifestは別versionの明示dispatchを必要とする |
| `src/ariadne/product/ports/scientific_core.py` | `ccf89d307d626e7b4c82fe3f919230bb781d7f6a` | `ScientificCorePort`の5 method、`ScientificResultDescriptor`はProductの`ScientificStatus`。E11のIdentification/Point/Inference/Science軸をlosslessに表す保証なし |
| `src/ariadne/product/ports/artifact_store.py` | `e5bb990f9b69ef68df46a1559560ffb67b64caaf` | `store/retrieve/exists/delete`のみ。atomic multi-file commit/readbackのPortは確認できない |
| `src/ariadne/product/domain/graph_version.py` | `37ff76e001c8e269a00127e18d375f1dbc34c0e3` | ProductのGraphVersionは状態付きEntity。E11のPAG circle/bidirectedやLocal Graph Evidenceを同一Authorityとして再利用できるか未検証 |
| `src/ariadne/product/workflow/executor.py` | `81d91e7de0fc0eb5a582711968b698fa4ac44761` | `GenericExecutor`はProduct Stage/Planを実行。CLI-only LocalのDB/Worker実行権威へ暗黙に転用しない |
| `pyproject.toml` | `7c24ed729be1a31c15a173ef4510aa3ed961d0b9` | Python `>=3.12,<3.13`。optional dependenciesに`predictive-advanced`はあるが、E11全Backendのextrasは現行project宣言上で未確認。5 profile/lock/OS probeは未実行 |

**Design authority:** `23_41/42`、`30_61/62/63`は採用済み**設計候補**であり、現行Sourceの証拠ではない。E11 Domain/PortはProductへの依存を増やさず、純粋DTOとadapter bridgeを別途検討する。既存v2の`causal-analysis-spec/2`とE11 Local schemaの意味を自動変換しない。

## 4. Architecture FindingのDisposition（BD01の13件）

| Finding | PREP分類 | 根拠／残作業 |
| --- | --- | --- |
| F01,F02 | BD文書修正済み、実装証明なし | Product/Local authorityの境界と図は改訂済み |
| F03 | Blocking / implementation contract | Staging, crash consistency, commit marker, secure readback, negative FS tests |
| F04 | Blocking / Port freeze | Legacy Product Portと新typed E11 DTO/adapter bridge、regression |
| F05 | Blocking / Security contract | Local OS主体・export opt-in・path/permission/audit |
| F06 | Blocking / Schema freeze | Strict version dispatch、old v2 reader、roundtrip |
| F07 | Blocking / Science data contract | ConfidenceSet unbounded/disconnected/ALL_REAL、typed negative/null reasons |
| F08 | Blocking per method Gate | Method-specific eligibility/inference/effective backend; all41 are in scope, validation staged per Gate |
| F09 | Blocking for required execution profiles | 5 profiles + combined lock + environment actual probe; not run |
| F10 | Delivery blocker, not universal Coding blocker | GPL/distributed artifact customer-specific legal decision |
| F11 | Separate Product backlog | GAP-C01〜04 remain open; not silently included in E11 CLI |
| F12 | Coding-entry blocker | Independent Architecture Review and Port/Schema freeze not completed |
| F13 | Canonical-promotion blocker | Original requirement_definition may change only after all applicable E11 tests PASS |

**Independent Review:** NOT_RUN. This document is an execution record, not a self-issued PASS.

## 5. Science・Backend・Environment acceptance

41 Method IDs (`P1-M01〜20`, `P2-M01〜08`, `P3-M01〜13`) have candidate allocation in `30_63`, but an allocation table is **not** a tested adapter or Method-specific scientific acceptance. For each ID, before its Gate's 07 freeze, bind `MethodConfig × Estimand × Identification × Backend/version × DGP/NEG/REF/AC × inference policy × reference SHA × seed × acceptance threshold`. Negative outcomes (not identified, weak IV, unsupported CI, partial identification, nonfinite, null controls) must not be silently reclassified as successful point estimates. For Monte Carlo, predeclare K/R, coverage/MCSE/FWER, valid-run denominator, pilot vs confirmatory execution and budget. These are not yet measured.

**NOT_VERIFIED:** actual isolated Python environments, optional backend imports/API versions, five profiles/combined lock, CI coverage, scientific DGP oracle, security/crash tests, license/SBOM. No claim of full compliance or PASS.

## 6. Concrete next actions and Exit

1. **PREP-01:** migrate the 8 Root Flow records and Change Logs with reference repair; normalize 23/30 numbering; populate all 23 API operation contracts from current OpenAPI; inventory and rewrite all relevant 30 Classes in seven sections; perform 122-clause semantic comparison and complete Trace; run automated link/heading/source comparison.
2. **PREP-02:** resolve F03〜09, F12 to an implementable ADR/Schema/Port contract, run isolated backend/profile probes, write Method-specific science AC for all 41 (execute science tests later at the appropriate Gate), and obtain independent Architecture Reviewer disposition.
3. **PREP-03/04:** only after blockers are resolved, freeze first Gate's 06/07 and seek explicit Owner Coding Authorization. **No Coding authorized by this report.**

**Non-changes:** No `src/`, `pyproject.toml`, `uv.lock`, or `docs/wiki/requirement_definition/` modifications. No Owner decisions or 41 Method scope changed.


## 7. PREP-01 継続実施：Web API Router全件のStatic Inventory（2026-11-17）

2026-11-17の作業で、`src/ariadne/interfaces/web_api/routers/`の13 Routerから標準`@router.get/post/put/patch/delete`宣言を抽出し、`23_10〜23_19`の10ファイルにSource由来のRoute表を追記した。**観測した101件は実装Route宣言の棚卸しであり、全OperationのContract規範完成ではない。**

| IF Stock | Source対象 | 観測件数 |
| --- | --- | ---: |
| 23_10 Project / Context | projects、workspace_lifecycleのResearch Context | 11 |
| 23_11 Dataset | dataset_versions | 4 |
| 23_12 Analysis Spec | workspace_lifecycleのAnalysis Specification | 7 |
| 23_13 Exploratory | exploration | 14 |
| 23_14 Causal Graph | graph_versions | 9 |
| 23_15 Predictive | predictive、predictive_workflow | 17 |
| 23_16 Execution | executions | 6 |
| 23_17 Result/Lineage | results、product_closureの関連Operation | 15 |
| 23_18 Annotation/Artifact | annotations、artifacts、product_closureの関連Operation | 13 |
| 23_19 Frontend Support | navigation、product_closureのworkspace/authorization関連Operation | 5 |
| **合計** | **10文書・13 Router** | **101** |

- `23_10`はRouter + Project DTOからRequest/HTTP status等を11件突合。操作別Authorization、Lifecycle、Error、Idempotency、Regressionは未検証。
- 他9ファイルはSource decorator（Method/Path/Function/declared response）を記載。Pydantic/Service/Runtimeの9欄実効確認は未完。
- Source Endpointで`X-User-Id` headerを扱う箇所があるが、信頼境界やGateway認証をRouter単体で確認できない。FR-121/RBAC満足を未検証のまま認定しない。
- next: Operation × 9-field matrixを各Service/Schema/ErrorHandlerと照合し、明確にCURRENT / PROPOSED / NOT_SPECIFIED / N_A理由を示す。必要な負例を追加する。
- 本追記はPREP-01＝IN_PROGRESS、PREP-02＝IN_PROGRESSの判定を変更しない。


## 8. 2026-11-17継続作業：Stock契約のSource照合・7区分是正

**GitHubのRead-only Source inspectionに基づく追加是正**。以下の修正は承認済みScope・科学的仮定・Source Codeそのものを変更しない。

| 対象 | 具体的な差分 | 結果と限界 |
| --- | --- | --- |
| `23_10` Project/Research Context HTTP | `ProjectDataService`／`WorkspaceLifecycleService`／`error_handlers`／`IdempotencyService`をRouterと突合。FR-121のMember Role check欠落と、ResearchContext createのIdempotency-Key経由不在をCURRENT/REQUIRED差分として記載 | **Source上の契約Gap**。外部Gateway等のruntime経路は未検証。Product backlogへ割当要。E11 CLIで自動閉鎖しない |
| `22_12` Product Security・`23_51` | Role gapとIdempotency gapをScope＋Negative Test付きで記録 | FR-121 / FR-114bの規範を緩和せず、Product側未実装条件として保持 |
| `30_62` E11 Local | E11LocalCausalUseCase、MethodCapabilityRegistry、LocalArtifactPublisher、LocalRunManifest、LocalManifestReader、LocalPrivacyPolicyを**Class単位のOwner 7区分**へ再設計 | **Proposed**であり実Class未存在。詳細Signature/JSON Schema、FS fault、独立ReviewのFreezeは未了 |
| `23_42`・`22_15` | no-clobber／secure dirfd walk／Marker→Manifest hash／PAG・AR/Privacy・旧v2隔離の具体的契約と未Freeze点を追記 | Design Draft、Atomic/Privacy/Schemaの実効試験はNOT_RUN |
| `30_20`、`30_21` | 旧Product PlanValidator／StageRunnerRegistry／ExecutionOutcome／GenericExecutorを実Source SHAと対応させ7区分化。単独`##2/3/4`の見出しを§9.5/9.6、§10.5/10.6へ変更 | Source静的照合／番号衝突の部分解消。Product runtime回帰はNOT_RUN |
| `30_10` | 既存Product GraphVersionをSource照合し7区分化、重複`##5`見出しを§3.7へ変更 | `apply_edit`は`content_hash`を自動再計算しない点を確認。Product DomainとE11 GraphEvidenceを同一視しない |
| 正式Gate語彙 | DD/IF/BD Stock内の旧全体`Gate06/Gate07`を、該当**各Gateの06/07**文書／独立検証に修正 | DEC09のOwner受入要求を保持。G01〜G10暫定Workstreamを正式PASS扱いしない |
| DEC08 Env | `pyproject.toml`と`uv.lock`の全宣言を静的確認。LockにDoWhy/EconML/Tigramite/rdrobustのPackage entry無し | 5 Profile＋ENV-RDはADOPTED POLICY、**CURRENT LOCK未導入／実測NOT_RUN**。pyproject/lock改変なし |

**未実施のExit blocker（継続）:** Root 8 Flowと5 Change Logの安全な移管・Backlinks全数修復、23/30の残る見出し・Class/Protocol/DTO全数、23 API 101 OperationのService/DTO/Error/Auth/Idempotency contract実効Coverage、122既存条文意味照合、Method41科学ACの全セル、5 ProfileのFresh実行、BD01-F03〜09/F12の独立審査・Schema/Port Freeze。**PREP-01/02は双方IN_PROGRESSであってDONEではない。**

**補足:** Product Project/ResearchContextのSource gapはE11新Local CLIの実装障害であると即断しない。DEC09のE11 CLI-only／Product別Backlog境界に従い、依存するGateに関係する場合だけCoding blockerかを判断する。


## 9. PREP-01/02 latest follow-up and authority distinction

**Migration:** Root Flow8＋ChangeLog5件はGit `cd4e738` で物理移管済み（元Blob SHAは[DOC01台帳](../doc01_review/93_20261117_flow_migration_manifest.md)）。README／Stock105件／移管Flow13件／歴史的移管/Source Snapshot12件におけるrelative Markdown file link計516件を確認し、**改訂Root内broken 0**。この完了事項は初期の§3/§8「移管未完」という当時の状態記録を更新するものであり、別件のSchema/Anchor/Code/Science PASSを意味しない。

**Class design:** Existing Product8件＋Proposed Local6件＝**14 Class**のOwner 7区分を記述済み（[DD01 class delta](../dd01_review/92_class_contract_conformance.md)）。残る`30_61` Domain DTO/Port と`30_63` Method-specific adapter Classesは未完成。

**Architecture review readiness:** [PREP-02 reviewer package](94_20261117_prep02_architecture_review_package.md)にBD01-F03〜F13の11 OPENを共通設計／Method Gate／Product別／Deliveryへ仮分類し、Owner判断が必要なLocal row privacy/no-clobber/Schema Versionの案を明示。**Owner未承認、Independent Reviewer NOT_RUN、Port/Schema未Freeze。**

**Overall:** `PREP01_IN_PROGRESS / PREP02_IN_PROGRESS / CODING_NOT_AUTHORIZED`。全122既存改訂条文の独立意味監査、101 API Operationの9欄、残Class、Method41の科学ACと5 ENV実効Probeは引き続き未完。


## 10. 2026-11-17 Owner decision and continuation checkpoint

[DEC-PREP02 Owner record](decisions/94_20261117_dec_prep02_owner_architecture_choices.md): **A/A/A ADOPTED** for non-delegated same-UID private Local export; same-FS Linux atomic no-replace immutable run publication; strict `e11-local-*/1` discriminator namespace. Reflected into `22_12`, `23_41`, `23_42`, `30_61`, `30_62` and `94` Architecture Review pack. All earlier 'Owner decisions pending' snapshots in this history are superseded **only for these three selections**. No runtime or tests were executed. Remaining PREP01: 101 Operation x 9 fields, 122 changed clauses and full remaining Class inventory/trace. Remaining PREP02: F03/F04/F05/F06/F07 common contracts, strict schema/error/Port freeze, 41 Method Gate-specific science AC, five-profile environment probes and independent Architecture Review. `PREP01_IN_PROGRESS / PREP02_IN_PROGRESS / OWNER_CHOICES_ADOPTED / CODING_NOT_AUTHORIZED`.
