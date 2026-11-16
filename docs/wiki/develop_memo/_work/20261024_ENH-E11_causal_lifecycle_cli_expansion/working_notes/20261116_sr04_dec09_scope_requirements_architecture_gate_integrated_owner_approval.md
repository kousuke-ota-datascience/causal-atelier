# ENH-E11 — DEC-SR04-09：68 Scope・Requirements・Architecture・Gate統合Owner承認記録

**承認日:** 2026-11-16 JST（承認時刻は記録していない）。  
**意思決定者:** Human owner。本ターンの明示指示「全体Scope・Requirements・Architecture・Gateの統合承認を実施する」に基づく。  
**承認区分:** **CONCEPT_AND_68_SCOPE_OWNER_APPROVED / REQUIREMENTS_SEMANTIC_DELTA_OWNER_APPROVED / ARCHITECTURE_POLICY_OWNER_APPROVED / GATE_PLAN_OWNER_APPROVED**。  
**実行制約:** **FORMAL_FR_NFR_AR_PUBLICATION_PENDING / ADR_DETAIL_AND_SCHEMA_FREEZE_PENDING / GATE06_GATE07_NOT_FROZEN / SCIENCE_NOT_RUN / CODING_NOT_AUTHORIZED / CUSTOMER_DELIVERY_LEGAL_NOT_APPROVED**。  
**承認の意味:** 実施対象・後続送りと例外・新旧要件の**意味上の差分**・責務を分けた基本Architecture・Gateの**計画／出入口原則**をHuman ownerが採用。これは承認済みの実装または科学的達成の宣言ではない。文書の表やMethod一覧のレビューはGitHub上の静的監査であり、実効Backend・Science・法律適合性は実測／法務の対象。

## 0. DEC09の判断と根拠Snapshot

| 判断 | Owner承認事項 | 限界・別Gate |
|---|---|---|
| **DEC09-1 Scope（採用）** | Phase1〜3＋A0横断の**全68行を本書付録AのDispositionで承認**。全41 Methodの対応はSR04-Fを採用し、必要なMethodを「少数のfamilyだけ」へ黙って縮小しない | Dとした後続方式はE11初期の納入必須外。Sourceに残る「要承認」は本DEC09の判断により対象行の処遇のみ解消 |
| **DEC09-2 Concept/Requirements（採用）** | CLI-onlyの10 UC、03のE11-REQ群・8不変条件を**意味上の要求ベースライン**として採用。正本§11外部engine除外はE11の機能別Optional Capabilityを許す方向へ変更する方針を承認 | 正本にFR/NFR/ARの新規採番・条文・Statusを発行／改定したことにはならない。正式公開には差分付きRevisionとOwnerのSHA確認が必要 |
| **DEC09-3 Architecture（採用）** | 04の責務分離・versioned local contract・識別／推定分離・型付き負結果・Graph fidelity・privacy/legacy保護・環境分離を**Architecture Decisionの方針**として承認 | 正式ADR ID・JSON Schema/enum・API/Path/atomic write細則と独立Architecture Reviewは未freeze |
| **DEC09-4 Gate（計画採用）** | 暫定G01〜G10をIssue/UC/Methodの実装Work Package区分として採用し、Gate06準備とGate07の独立科学受入の**閉鎖条件**を承認 | **Gate06/07はPASSでもfreeze済みでもない**。45 Quant ACのmethod別Hard適用、K/R/Budget、Reference/ENV/Library/Legal条件を固定後にGate snapshotを作成 |
| **DEC09-5 Existing Product & Foundation Gap（採用）** | Product GAP-C01〜04はE11 CLI新機能による自動閉鎖を拒否し、別Product backlog／Architecture Issue #14へ追跡移管。既存FR/Status/v2/DBを保護 | #14は仮の追跡元。Product側実担当者・別Enhancement ID・期限・受入Ownerは未割当。移管追跡だけでGapをCLOSEDにしない |
| **DEC09-6 Implementation Authority（採用）** | Scope/要件方針のOwner承認と実装開始・依存変更・科学的確認・納入権限を分離。対象／承認外を明示したWork Package単位で次段階へ進む | **本書だけではCoding指示にならない**。承認済みFR/NFR/ARの発行、具体ADR/Schema、Gate evidence pre-freeze、実行環境の承認をCoding Entryとして別確認 |

### 0.1. 監査したGitHub Blob（本決定の入力版）

| 入力正本候補 | Review時のGit Blob SHA | 内容 |
|---|---|---|
| [scope](../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md) | `a0cb5b673d8cbdff2533ef34efd69b1f63b8343b` | 68 Scope：21/18/19/10 |
| [concept](../00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md) | `5eaf402bd8c37621f821c3a2167dfacfc83d9f53` | 最新版の未承認Draftと既往Owner決定 |
| [owner](../00_enhance_background/02_enhancement_concept_approval_record.md) | `5dcb0e6c3467b929bdc564a3b07382652010dcc2` | 最新版の未承認Draftと既往Owner決定 |
| [req](../00_enhance_background/03_requirements_revision.md) | `ca8b821ca7f8cac5dacf4c62800102154dc04fdf` | 最新版の未承認Draftと既往Owner決定 |
| [design](../00_enhance_background/04_design_revision.md) | `7c8da3c5c3ad0c076d4b4f5cf20082743c0c4f9b` | 最新版の未承認Draftと既往Owner決定 |
| [consistency](../00_enhance_background/05_requirements_design_consistency_and_traceability_review.md) | `4bd58ed903d31a6d2b59401914b1159c4de93ad6` | 最新版の未承認Draftと既往Owner決定 |
| [trace](../working_notes/20261115_sr04_gate07_traceability_draft.md) | `4e95150603bd3d599b6227008044155c4f9580fe` | 41 Method、24 DGP/REF、28 NEG、45 AC、9 ENV |
| [review](../working_notes/20261116_sr04_af_integration_review_and_blocker_resolution.md) | `ce78b107464e6f7dffff83914ebda9d63239901f` | 最新版の未承認Draftと既往Owner決定 |

**注記:** 上記は承認審査**前**のGit Blobである。本決定を02/00_04/01/03/04/05/Fへ反映したあとの更新SHAとは一致しない。Gate用の最終証拠Bundle SHAは文書整合再検証・実効Config freezeの後に独立発行する。

## 1. Scope68とA0例外の最終処遇

**68行の正式な個別Scope判断は、付録Aの行ID・Disposition・旧案理由／追跡Issueの組合せを承認対象とする**。対象はP1=21、P2=18、P3=19、A0横断=10。各行のR/Q/N/Dを別Sourceの部分採用に応じて正規化し、**Dを実装対象のNと呼び替えない**。

**A0重要例外を明示承認:**
- `X-01 ATC`: 初期Phase1〜3 **D**（Phase4/後続）、controlled direct effectを初期の既存ATE/IV Methodで代用しない。#14継続。
- `X-02 Mediation`: **D**。ただしPhase1 FD-Aの限定Mediatorを使うFrontdoor数値EstimatorはP1-08として**N**であり、汎用Mediationとの混同禁止。
- `X-03 Matching / generalized g-computation`: 初期 **D**。OLS/IPW/AIPWを科学的に同一Methodとして自動カウントしない。#14で将来採否。
- `X-04`: Nは実在NCE/NCOの2 Method、Simulated Confounder・Graph Perturbationなどは**D**。DEC06-A採用。
- `X-05`: NはClassic OLS partial R²／point RV（q=1）のみ。IPW/AIPW/CATE等のSensitivity一般化は**D**。
- `X-06`: 今回提供Method固有の診断・区間・cluster/Graph評価を**Q**、汎用多重試験・全Graph consensusは**D**。DEC07 FWERは**科学Benchmarkの多重性**であり、分析アプリ全体の任意多重仮説検定機能を提供したとはしない。
- `X-07/08`: Policy／MonitoringはPhase4 **D**。
- `X-09/10`: Local CLI／Manifestの**R+N**のみ実装、既存Product GAP・Web/API/Worker/DB統合は**D**。

**その他重要な採用境界:** P1-08 Frontdoor FD-A数値推定をN、FCI PAG＝Graph保存とReview、P2の非IV CATE7 Method＋別DRIV-A 1 Method、P3の3 Temporal/7 Quasi/B0-B1 weak-IV AR、SCMは初期Point-only、NCE/NCO/RV opt-in。DEC01〜08のMethod固有科学的意味が全行の一般文言より優先する。

**配布制限:** Tigramite/RD（GPL系）MethodをScopeへ含めるOwner判断は、法務審査前に特定顧客へGPLを含むソフトウェアを配布してよいという判断ではない。納入不能なケースは対象Methodの削除ではなく`DELIVERY_BLOCKED`・Owner再審議とする。

## 2. Requirements：承認した意味論と正本の改訂境界

### 2.1. 承認対象のE11 Requirement group

| 要件群（03／05仮ID） | 承認内容 | Issue |
|---|---|---|
| E11-REQ-P1Q / P1G | Local Question/Design/Graphのversion・hash、FCIのPAG circle endpoint/GraphVersion、識別と探索の分離 | #15/#17 |
| E11-REQ-P1I / SR03 / SR03D06 | DoWhy Backdoor/Frontdoor/IV、FD-A numeric、GraphからEstimatorへのfail-closed gate、旧v2保護、IV/B1/ARの型付きConfidence Set | #16/#22/#24 |
| E11-REQ-P1R / P1S / P1NC | 既存RefutationとRandom Common Cause/Bootstrap、Observed NCE/NCO opt-in、古典OLS限定partial R²/point RV | #16 |
| E11-REQ-P1W | IPTW/AIPW quality／既存E9 overlap/balance/ESS保護とPS推定のCI科学的審査 | #19 |
| E11-REQ-P2 / P2A / SR03D05 | CATE/HTE非IV7 Method、DRIV IV separate、Explore point／Confirmatory inference分離、個票Privacy/Parquet・group summaries | #18/#24 |
| E11-REQ-P3T | PCMCI、PCMCI+、LPCMCIとCI-test／lag／endpoint忠実性 | #20 |
| E11-REQ-P3D / P3I / P3S | 7つの準実験・IVのDesign／Estimand／Estimator／Inference条件・SCM point-only | #21/#22/#23 |
| E11-REQ-CLI / DEC07 / DEC08 | Versioned local config／lineage／Status／atomic write／実効version・seed／manifest、Backend Extras/uv.lock、法務/再現性・科学Benchmark | #24/#14 |

### 2.2. Original Requirementの改定権限

- **E11内での例外方針を承認:** 現行[要件正本 §11](../../../../requirement_definition/10_requirements_definition.md)は未承認のDoWhy/EconML等をScope外としている。Human ownerは**ENH-E11の承認済みOptional Capabilityに限り**この除外の例外を正式改定することを承認する。これは勝手に正本条文／Statusを書き換えたことではない。
- **新旧互換性:** 既存Product/web/API/Worker/DB、`causal-analysis-spec/2`、既存ATE/ATT・IPW/AIPW/REQUIRES_REVIEW＋overrideを回帰保護し、E11の新MethodやScience Resultを旧v2 JSONへ無言で格納しない。
- **新E11の仕様差分:** E11に新FR/NFR/ARを登録し、最新approved prior FRと矛盾しない条文・version/Status/UC/Issue/Gateの正規追跡を別の変更パッチで提出する。**この時点でFR番号を未出典の番号で創作しない。**
- **未完正本の区分:** 03は**Meaning/Delta Owner-approved**、正式な要求正文の新FR/NFR/ARの逐条・Owner SHA freezeとGitHub workflow reviewは**別Closure**。元Requirementの未充足を`IMPLEMENTED`へ変更しない。

## 3. Architecture Owner決定（ADR採用方針）

| Architecture item | 採用した不変条件・責務 | 具体化・独立審査未完 |
|---|---|---|
| ARC09-01 Domain authority | Question/Design/Estimand/GraphVersionの科学的意味はLibraryに依存しないDomain。識別結果・科学StatusはAriadne側で正規化 | 具体的Schema enum、method compatibility |
| ARC09-02 Backend isolation | Scientific Core Adapterがoptional DoWhy/EconML/Tigramite/RD等をMethod別に呼び、既存Product backend/API契約を破壊しない | effective adapter mapping、APIとvalidation、full lock |
| ARC09-03 Identification first | Estimand×Graph×Design×Assumptionsで識別後にEstimator可否。PAG/CPDAGの未確定端点・weak-IV/不適格を黙って点推定に昇格しない | FD-A/DRIV-A/B1/weak-IV ARの実効point/CI |
| ARC09-04 New local contract | Versioned scientific local CLI＋JSON/Parquet/Manifestを別契約。Identity/hash、atomic write、readback、permission/privacy。Product DB authorityの代替でない | exact schema/name/version/path、安全性試験 |
| ARC09-05 Result & inference | Effect point／confidence_set形状・uncertainty availability／Science statusは別軸。Fuzzy RDの局所IV、SCM point-only、Graph OracleをMethod固有のResultへ保持 | 数値Reference/Method-specific interval validity |
| ARC09-06 Execution provenance | `pyproject.toml`＋universal `uv.lock`を承認変更し、5 profilesとRD条件付き候補、実効Version/BLAS/seedのManifest、SBOM/Licenseを検証 | Extras具体名・lock成功・Legal Review/Owner resources |
| ARC09-07 Future Product | API/UI/DB migrationは新規実装しない。Product gap C01-04の担当レーンを明示し、将来の適合移行は別Owner Decision | Product Gap個別改修、正式担当・期限 |

**Architecture Review結論（Owner権限の範囲）:** 上記**Architecture原則・責務境界をOwner採用**。設計04の将来追加が必要な詳細ADR・Schema・Port定義を既に独立Architecture Reviewerが科学/実装的に検証した、とは扱わない。Architecture Reviewの正式完了条件はARC09-01〜07の具体ADR/Interface Manifest・legacy regression/negative scenarioが揃ったSnapshotに対する別の独立レビューとする。

## 4. Gate/Issueの実装計画承認

### 4.1. Stage/Workstreamの承認区分（**正式受入Gateではない**）

| Plan stage（暫定 G01〜G10 の用途） | 承認した対象と条件 | Issue |
|---|---|---|
| G01 | Local Graph/Question/Design、FCI PAG fidelity・Version lineage | #15/#17 |
| G02 | Identification/Eligibility、DoWhy FD-A、type-safe nonidentified | #15/#16 |
| G03 | IPTW/AIPW quality、Refutation・NC/RV Sensitivity | #16/#19 |
| G04 | EconML CATE/DRIV Method・Estimand | #18 |
| G05 | CATE inference/support/個票Privacy・files | #18/#24 |
| G06 | Temporal Graph/CI testsと同値類・lag | #20 |
| G07 | DiD/Event/ITSのmethod-specific推論 | #21 |
| G08 | Sharp/Fuzzy RDD、B0/B1 IV/AR集合 | #22 |
| G09 | SCM/SDID weights/point/CI可用性 | #23 |
| G10 | Manifest/lock/seed/Readback/legacy v2/independent Science evidence | #24/#14 |

**名前空間の衝突を避ける:** 上表の`G06`／`G07`は**01の暫定Workstream番号**である。「開発全体のGate06／Gate07（実装適合・独立科学受入の正式受入）」とは**別の識別子**。本書は`G01〜G10`を実装・検証の計画グループとして採用しただけで、Gate番号の既存Workflow正本を上書きしない。

### 4.2. Gate06／Gate07で将来freezeすべき事項

| Governance Gate | 承認する閉鎖条件（今回Owner決定） | 本日の実際の状態 |
|---|---|---|
| **Gate06 Implementation/Architecture readiness** | approved FR/NFR/AR条文と適用Issue、ADR/API schema、E11 local CLIのtrace、旧v2/E9回帰、atomic/privacy、全必須MethodのInterface/Backend Profile contractとCode品質の検証 | **NOT_FROZEN / NOT_EXECUTED** |
| **Gate07 Independent Scientific acceptance** | SR04-A〜FのMethod41/Scope68/DGP24/NEG28/REF24/AC45/ENV-AC9/X9を一貫した評価Cell登録とSHAで紐付ける。DGP Referenceの独立性、数値ACのMethod別Hard/conditional/N/A、KとBonferroni、R/CI/Bootstrap、negative/legacy/Graph Oracle、CPU予算、License/Env gateを分離した実測証拠を要する | **NOT_FROZEN / SCIENCE_NOT_RUN** |
| **Delivery/Legal** | Software artifact／GPL library／受領者・配布形態／Required Source/Noticeを実名の法務・Ownerにて個別承認 | **NOT_APPROVED** |

**重要:** 数値閾値の具体適用、K/R・CPU Budget、Backend version・Lock SHA、Graph/Frontdoor/DRIV/RDDの独立Oracleが未確定。ここで「Gate設計方針を承認した」ことと、「Gate06/07をfreeze/PASSと判定した」ことは**論理的に別**。

### 4.3. Coding前のEntry Checklist（この記録は許可票ではない）

1. **FR/ADR diff:** 新Requirement／Designの条文・Status・Effective Profile／API/JSON SchemaをOwner承認Snapshotとして提出。
2. **Source／Gate prep:** mandatory Method／DGP／Ref／ACに対応するpre-implementation Gate baselineと責務・許容数値の承認、実装段階と独立Science Gateを分離。
3. **Work Package:** Issue #15〜24の分解、各WPのOwner・実装対象/対象外・acceptance/rollback・Coding authorityを発行。
4. **Environment:** DEC08方針に従い、`pyproject.toml`/`uv.lock`改修の承認済みWPとfresh profile testingの条件を先に固定。
5. **Science and delivery:** 実装後のT2 Pilot→T3 ScienceとDelivery法務は独立Gate。Coding開始時点で将来の科学PASSを捏造しない。

## 5. Existing Product GAP-C01〜04の明示移管判断

| GAP | 現状の根拠・未充足 | E11今回Owner承認した帰属 | 本Gapの真正な閉鎖条件 |
|---|---|---|---|
| GAP-C01 | Productの探索→Confirmatory warning全経路網羅は未証明 | E11新CLIと別。Product側tracking #14で担当Owner割当・Follow-up | 全入口（Dataset/Project/Resource）positive/negativeとSource Result lineage |
| GAP-C02 | ProductのCanonical Context→Spec→Plan→Execution→Result→Artifact chain未完全 | CLI Manifestは代替でない。Product側tracking #14 | typed edges／cross-project/Readback/export、既存FR-008/054/095 |
| GAP-C03 | Product runtime library/seed一部とstochastic全経路は未証明 | E11に新CLIのManifest/seedはN、Product StageAttemptは#14で別 | Product/CLIの対象責務を分離した実効backend version／retry/seed E2E |
| GAP-C04 | ProductのFamily Navigation concrete catalogの所属が中央に残存 | E11 CLI Scope外。Product Architecture側#14で将来責任者を指定 | Family ownershipへ移管、E7/E8/E9既存回帰 |

**Owner採用:** 上記の**E11外への実装帰属の分離**と監査継続を承認。ただしGitHub Issue #14が各Gapの**正式な専任人員・別Enhancement・期限を既に引受けた証拠ではない**。本承認により4つのGapの`Implementation Status`や`Requirement Status`を変更しない。#14の実在/Assignee/未閉鎖登録とProduct Ownerへのhandoffを後続チェックで確認し、未設置なら別Issue作成を要求する。

## 6. 解消扱いと残余Blockerの厳密な線引き

| 指摘（20261029審査） | 今回の解消根拠 | 判定 |
|---|---|---|
| SR-01 ScopeのOwner判断 | Scope68付録A、DEC01〜08、A0例外の明示採否 | **OWNER_SCOPE_APPROVED** |
| SR-02 Backend/Env | DEC08全A方針採用、SR02は別環境smokeのみ | **POLICY_RESOLVED / LOCK_SCIENCE_PENDING** |
| SR-03 Identification→Estimator | SR03 D01〜06とDEC01〜04の意味論採用 | **POLICY_RESOLVED / IMPLEMENTATION_SCIENCE_PENDING** |
| SR-04 Method Science | A〜F、DEC01〜07のMethod/AC意味論・方法論採用 | **POLICY_RESOLVED / METHOD_BENCHMARK_PENDING** |
| SR-05 Exceptions/Product Gap | X-01/03/04/05/06とGap4を個別Owner帰属決定 | **SCOPE_RESOLVED / PRODUCT_ASSIGNEE_PENDING** |
| SR-06 NC | DEC06で3 method＋opt-in/typed null採用 | **POLICY_RESOLVED / CALIBRATION_PENDING** |
| SR-07 CATE | SR03 D05＋DRIV-A＋Method別CI availability | **POLICY_RESOLVED / BACKEND_COVERAGE_PENDING** |
| SR-08 Temporal | GRAPH-A＋Tigramite CI-test／lag contracts | **POLICY_RESOLVED / PAG_ORACLE_PENDING** |
| SR-09 Quasi | DEC05 7手法の限定Estimator/Inference | **POLICY_RESOLVED / QUASI_COVERAGE_PENDING** |
| SR-10 CLI/Artifacts | SR03 D04／DEC08 Manifest、Privacy、Atomic | **POLICY_RESOLVED / SCHEMA_IMPLEMENTATION_PENDING** |
| SR-11 IPTW | DEC07定量受入、SR04 DGP/ACとの対応 | **POLICY_RESOLVED / STATISTICAL_EVIDENCE_PENDING** |
| SR-12 Scope→Science trace | SR04-F 41/68/24/28/24/45/9/9 registry | **DOCUMENT_TRACE_READY / EVIDENCE_NOT_GENERATED** |

**全体判定:** `DEC09_OWNER_POLICY_APPROVED`。**実装・法務・科学・数値／実行環境のBlockerは未閉鎖**。過去の技術レビュー`CHANGES_REQUIRED`を、本決定によって実装検証も完了した`PASS`へ改竄しない。

## 7. DEC10・次工程へ引き渡すEvidence

- **02 Owner Decision:** 本DEC09採用の記録と承認範囲／非承認範囲。2026-11-16 JST、後続オーナー指定でなければ時刻を捏造しない。
- **03/04/05:** Meaning-approved requirement／architecture／Gate planning表、正式条文とFreeze未了の区分。
- **SR04-F:** 41 Method／68 Scope／DGP24／NEG28／REF24／AC45／ENV9／X9のID・Source SHAと、Owner Approval／Independent Science Evidenceの独立Axis。
- **DEC07・DEC08:** Accepted policies。K/R/Budget/Full lock/LicenseとScienceの未実施を維持。
- **DEC10:** 独立Reference・Monte Carlo／negative／Graph／Quasi／legacy v2のT3実行後、Method別Metric/失敗/Resource/ReadbackとReviewer署名を持つGate判断。DEC09の承認は将来のDEC10 Passの先取りではない。

## Appendix A：Owner承認した68 ScopeのDispositionと理由

**承認されたのはこの行ごとの実装帰属とDEC01〜08によるScience限定事項である。** 元00_04で過去に「要承認」だった行も、下記の扱いは本DEC09によりOwnerが判断した。Method別のInference/Backendが未検証の場合はそのまま実装可能な科学的保証と誤解しない。

| 00_03/00_04 Scope ID | DEC09承認Disposition | CLI-only提供・外す内容（00_04とDEC01〜08に従う） | Issue |
|---|---|---|---|
| `P1-01` | **R** | 現行Causal Question/Specを再利用。CLIで入力と参照IDを固定 | #15 |
| `P1-02` | **R+N／D** | 既存Spec versionを参照しlocal identity/hash追加。独立Product DB QuestionVersionは後続 | #15,#24 |
| `P1-03` | **R+N** | 現行Causal Design再利用。新識別に必要なlocal design項目のみ追加 | #15 |
| `P1-04` | **R** | DAG/CPDAG/PAG endpoint semanticsをそのまま保護 | #17 |
| `P1-05` | **R／D** | 既存Graph revision/provenanceを再利用。Consensus Graph等の独立新方式は後続 | #17 |
| `P1-06` | **R** | Native Randomized/Backdoor、nonidentified/review statusを保護 | #15,#16 |
| `P1-07` | **R** | Imported/User-defined GraphからIdentificationを開始する既存経路を保護 | #15 |
| `P1-08` | **N（Frontdoor数値推定をPhase1に含む方針採用）** | optional DoWhy Backdoor/Frontdoor/IVの識別と負結果に加え、**Frontdoorで識別したATEの数値推定をPhase1に必須包含**（2026-11-01オーナー判断）。最初のDoWhy二段階回帰は追加モデル仮定・科学Benchmarkを別検証し、識別API成功を推定成功とみなさない。IV/LATEは別契約 | #16 |
| `P1-09` | **N** | FCI/PAG Discovery：circle等のendpoint、背景知識、警告、CI test | #17 |
| `P1-10` | **R+N** | 既存Data Eligibility/Validation再利用＋新方式固有の適格性 | #15,#16 |
| `P1-11` | **R** | 既存ATE/ATTの差・OLS/IPW/AIPWを維持 | #19 |
| `P1-12` | **R+Q** | E9 Weight/Balance/ESS/Overlapを再利用。IPTW推論品質・SE/CI被覆を追加検証 | #19 |
| `P1-13` | **R** | Placebo Treatment/Data Subset Refutationを維持 | #16 |
| `P1-14` | **N** | Random Common Cause／Bootstrap Refutation、再推定・seed・再現性 | #16 |
| `P1-15` | **N（NCE/NCO各1Method、DEC06-1/2 Owner個別採用）** | **適切な観測Negative Controlを指定できる研究に限り、研究者が明示的に要求して実行できる反証分析**を提供する方針を採用。NCO/NCEの2方式（P1-M18/P1-M19）を初期Methodとして個別採用し、未指定時に自動実行しない。不適格時は理由付きの負結果、非有意時も無交絡と解釈しない（2.3節・実装計画メモ）。 | #16 |
| `P1-16` | **R** | Adjustment Set/Propensity Clipping Sensitivityを維持 | #16 |
| `P1-17` | **N（OLS partial R²/point RV個別採用）／D（広範Sensitivity）** | 最小Nは**Cinelli–Hazlett partial R²／point Robustness Value（q=1）**の古典OLS係数に限定することをDEC06-3で個別採用。現行のHC3を古典OLS公式へ無断適用しない。IPW/AIPW等の全面対応や追加A0方式は後続の個別判断（2.3節） | #16 |
| `P1-18` | **R+N／D** | 既存Lineage/Manifestを再利用しlocal manifest増強。Product canonical DB Gapは別Issue審議 | #15,#24,#14 |
| `P1-19` | **D** | 新しいProduct API/Worker/DB migration/RBACは後続。現行経路を変更しない | #14 |
| `P1-20` | **R+N** | 既存Scientific CLI再利用。新Identify/Refute/Sensitivity引数と版付き成果物を追加 | #16,#24 |
| `P1-21` | **R+N** | 既存Known-truth tests保護＋DoWhy/FCI/追加refuterの独立科学受入 | #16,#17,#24 |
| `P2-01` | **N** | CATE/HTE estimand、effect modifier、ATEとの差、Result schema | #18 |
| `P2-02` | **N** | LinearDMLを方法候補として必須一覧へ。利用版/APIを審査 | #18 |
| `P2-03` | **N** | CausalForestDMLを方法候補として必須一覧へ。利用版/APIを審査 | #18 |
| `P2-04` | **N** | DRLearner。既存AIPWとは別のCATE方法契約 | #18 |
| `P2-05` | **N** | ForestDRLearner、support/forest inference | #18 |
| `P2-06` | **N** | S-Learner、効果と予測の意味の分離 | #18 |
| `P2-07` | **N** | T-Learner、処置群別support診断 | #18 |
| `P2-08` | **N** | X-Learner、arm非対称とpseudo-outcome対応 | #18 |
| `P2-09` | **N** | DRIVまたは承認済み科学的同等IV+ML。**連続TでのIV heterogeneous effectを二値Z/Aのcomplier LATEと自動同一視しない**。条件付き識別対象・推論可用性はSR-03契約案へ | #18,#22 |
| `P2-10` | **N** | EstimationSpecification/HeterogeneityResult、nuisance/final/CI/subgroup | #18 |
| `P2-11` | **R+N** | 既存optional依存隔離原則を再利用しEconML能力・version・unavailableを追加 | #18,#24 |
| `P2-12` | **R+N** | 既存AIPW cross-fitting再利用＋CATE専用fold/seed/split/漏洩防止 | #18,#24 |
| `P2-13` | **R+N** | 既存Eligibility再利用＋effect modifier/IV/forest等の条件を拡張 | #18 |
| `P2-14` | **N** | CATE support/calibration/stability/uncertaintyと負結果 | #18 |
| `P2-15` | **N** | プライバシー制限付きCATE Parquet、群別JSON、checksum | #18,#24 |
| `P2-16` | **N** | 一定/線形/非線形異質性の既知真値、bias/RMSE/coverage/runtime | #18,#24 |
| `P2-17` | **N** | 列挙したEstimator群を個別追跡。『4 family以上』を削減根拠としない | #18 |
| `P2-18` | **D／N** | Paged Product API/UI/Worker/DBは後続。成果物はlocal Parquet/JSONで代替 | #18,#24 |
| `P3-01` | **N** | TemporalDesign/TIME_SERIES_GRAPHとlag・不確実endpoint | #20 |
| `P3-02` | **N** | PCMCIとlag/CI-test固有契約 | #20 |
| `P3-03` | **N** | PCMCI+と同時点edge契約 | #20 |
| `P3-04` | **N** | LPCMCIと潜在交絡・端点の不確実性 | #20 |
| `P3-05` | **R+N** | 既存CI設定原則再利用＋Temporal CI-test registryとmethodごとの互換性 | #20 |
| `P3-06` | **N** | time index/lag/stationarity/欠損/duplication/自己相関検証 | #20 |
| `P3-07` | **N** | DiD。並行トレンド、staggered adoption、clusterなど | #21 |
| `P3-08` | **N** | Event Study。event-time support、pretrend、cohort timing | #21 |
| `P3-09` | **N** | Interrupted Time Series。介入時点、季節性、自己相関 | #21 |
| `P3-10` | **N** | Sharp RDD。cutoff、bandwidth、局所estimand、density | #22 |
| `P3-11` | **N** | Fuzzy RDD。first-stageとcompliance/局所効果 | #22 |
| `P3-12` | **N（初期推定器A＋Bをオーナー採用）** | Phase3のLATE初期提供は**A＝二値Z/AのWald比をReference、B＝2SLS**（2026-11-01判断）。**D03-1でS2＝B0（無調整just-ID）＋B1（単一二値Z/A・事前指定Cの加法線形構造2SLS）を2026-11-05に採用**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。基本EstimandはIV独立性・除外制約・関連性・単調性下のcomplier LATE。共変量／複数IVの2SLS係数を一般ATEや同一LATEに自動変換しない。**D03-2 I2＝B0/B1でAR反転を初期基準の弱IV頑健推論として2026-11-05に採用**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。**D03-3 G2改訂の型付き信頼集合意味契約も2026-11-06に採用済み**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。First Stage／弱IVの診断と推論制限を記録し、**D03-4 C1を2026-11-15に個別採用：Phase3初期にCは含めず、条件付きIV＋効果異質性によってB1では必要Estimandを扱えない具体的ユースケースを再審議Triggerとする**（[詳細](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)）。C自身のMethod採否・担当者割当・科学Benchmarkは後続 | #22 |
| `P3-13` | **N** | Synthetic Control。donor、pre-fit、placebo、RMSPE | #23 |
| `P3-14` | **N** | Synthetic DiD。panel、donor重みと処置重みの区別 | #23 |
| `P3-15` | **N** | QuasiExperimentalDesignと各method固有のEstimand・Eligibility | #21,#22,#23 |
| `P3-16` | **N** | Method別known-truthとpretrend/manipulation/weak-IV/donor負例 | #20,#21,#22,#23,#24 |
| `P3-17` | **R+N** | 既存CLI成果物基盤再利用＋Temporal/Quasi専用JSON/Parquet/Manifest | #20,#24 |
| `P3-18` | **D** | RPCMCI/J-PCMCI+は8月Phase3自身の拡張候補。Phase3必須外 | #20 |
| `P3-19` | **D／N** | 新Quasi Product API/UI/DB/migrationは後続。local spec/fileを追加 | #21,#22,#23,#24 |
| `X-01` | **D／OWNER_APPROVED** — ATCを後続審議へ | ATCはPhase別必須リストに独立指定なし。controlled direct effectはPhase4側 | #14 |
| `X-02` | **D** | MediationはPhase4のextension pointへ。Phase1〜3の必須には算入しない | #14 |
| `X-03` | **D／OWNER_APPROVED** — matching/g-computationを後続審議へ | Matching/汎用g-computationはA0上位のみ。既存OLS等を同等扱いしない | #14 |
| `X-04` | **N(partial)+D／OWNER_APPROVED** — Observed NCE/NCO、追加A0はD | 観測NCE/NCOの**対照null検査2方式をP1-15で個別採用**。DoWhyのrandom/placeboとは異なる。Simulated Confounder/Graph PerturbationはDEC06-5により初期非採用D、後続個別審議 | #16,#14 |
| `X-05` | **N(partial)+D／OWNER_APPROVED** — classic OLS partial R²/RV、一般化D | 未観測交絡の最小方式はP1-17の**古典OLS partial R²／point RV**としてDEC06-3で個別採用。IPW/AIPW/CATEへの一般化、その他のモデル・欠測・Graph Sensitivityは初期非採用D（DEC06-5）、後続審議 | #16,#14 |
| `X-06` | **Q一部／D** | 採用手法のCI/cluster/bootstrap/stabilityは必要条件として品質検証。一般的多重検定・全Graph consensusは後続 | #19,#20,#21,#24 |
| `X-07` | **D** | Policy Value、cost/capacity、off-policy/自動配信はPhase4 | #14 |
| `X-08` | **D** | Monitoring/drift/再分析triggerはPhase4 | #14 |
| `X-09` | **R+N(local)/D(Product)** — Product GAP-C01〜04を後続管理 | Local reproducibilityは#24で追加。Product GAP-C01〜04は閉鎖せず移管要審査 | #14,#24 |
| `X-10` | **R+N(local)/D(Product)** — 新Product統合は後続 | 既存Product入口は保護。新手法はScientific Core/CLIのみ。新API/Worker/UI/DB統合は後続 | #14,#24 |

---

**本書をOwnerの概念・Scope/Requirement/Architecture policy・Gate plan承認記録とする。** `FR/NFR/AR正式発行・ADR Schema Freeze・Gate06/07 Freeze/Pass・Coding/Legal/Science`の各最終承認とは別。人が実際に受入証拠を審査しない限り、Evidence statusや既存Requirement statusを変更しない。
