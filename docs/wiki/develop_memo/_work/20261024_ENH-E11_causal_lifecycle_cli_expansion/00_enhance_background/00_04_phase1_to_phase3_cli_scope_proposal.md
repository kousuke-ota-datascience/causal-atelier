# ENH-E11 — Phase 1〜3・CLI-only実装スコープ案（ステップ4）

**文書区分:** 構想01に先行する実装対象の境界整理／スコープ判定案（正式要件・設計・Gateではない）  
**状態:** **STEP4_SCOPE_PROPOSAL_PREPARED／TECHNICAL_REVIEW_CHANGES_REQUIRED**／68行の採否案を作成／**Human ownerの正式承認前**  
**策定日:** 2026-10-26（日本時間）  
**調査・判断の基準:** `prototype/ariadne_mvp`、`07874a6b1475aa6535265f0c95ae1f062bd1b306`。新しい科学的pytest／外部Library互換性確認は未実施。  
**根拠:** [00_01（9月末照合）](00_01_foundation_gap_reconciliation.md) → [00_02（既存Gap4領域）](00_02_foundation_gap_closure_assessment.md) → [00_03（8月Phase1〜3との68行照合）](00_03_phase1_to_phase3_reconciliation.md)。  
**反映先:** [01_enhancement_concept_and_requirement_revision_plan.md](01_enhancement_concept_and_requirement_revision_plan.md) 第5章。**2026-10-29技術審査:** [20261029_cli_scope_review.md](../working_notes/20261029_cli_scope_review.md)＝**CHANGES_REQUIRED**（BLOCKER SR-01〜05、MAJOR SR-06〜12）。このスコープ案の行IDと候補Dispositionは**承認前・未改定**。承認記録02・正本FR/NFR/AR・Gate 06/07は未更新。

## 0. INTRODUCTION

### 0.1. 本文書の目的

本書は、オーナーから示された**「2026年8月4日のPhase 1〜3必須科学機能を、既存を再利用したうえで、Scientific Core／ローカルCLI／永続ローカルファイルに限り提供する」**方針を、実装単位で検証可能な**スコープ案**に変換する。

00_03の歴史資料68項目を1対1で追跡し、各項目を「既存機能再利用」「品質強化」「新規科学機能」「後続対応」の組合せで扱う。既存能力を新規実装として水増しせず、8月の必須手法を「何か4種類動けばよい」などと縮小しない。

### 0.2. 本文書の位置付けと非承認事項

前提3調査（00_01〜00_03）は**現状の根拠**、本書（00_04）は**実装する／しない範囲の提案**、正式な01は**分析上の目的・ユースケース・ENH-E11構想**、02は**Human ownerの承認記録**である。このため00_04を読んだだけでは新FR/NFR/ARが承認済みにならない。

8月A0上位構想とA1〜A3の実装指示で「必須」の意味が食い違う項目は、**具体的な採否案と承認留保**を併記する。特にNegative Control／未観測交絡Sensitivityは保留だけで済ませず、最小の科学的実行契約をPhase1の採用候補に含めている。

### 0.3. スコープ案の結論

**対象:** Phase1 DoWhy/FCI／追加Refutation・Sensitivity／IPTW検証、Phase2 CATE/HTEの列挙Estimator群、Phase3 PCMCI系とDiD/Event Study/ITS、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control/SDID、これらを支えるVersioned Local CLI・Result・Manifest・Benchmark。

**対象外:** 新規Web UI/API/Worker/DBとmigration、Phase4 Policy/Monitoring/Mediation、RPCMCI/J-PCMCI+等の拡張候補。**現行Product Foundation Gapの未充足をCLI成果物で閉鎖したと主張しない。**

**採否留保:** 上位A0にのみ記載のATC、matching/g-computation等の後続送り、およびNegative Control/Unobserved-confoundingの最小実装境界は、02承認記録で項目単位に同意／変更を確認する。過去の除外を現在の承認済み必須条件として扱わない。

## 1. 対象境界・Disposition・方法の採用原則

### 1.1. 実行境界

| 項目 | 今回のENH-E11の対象 | 明示的に対象外とするもの |
|---|---|---|
| **Scientific Core** | 既存port/domain contract再利用、adapter／eligibility／diagnostic／scientific result／negative status拡張 | Product固有Navigation Stage、Product DB authorityの変更 |
| **Local CLI** | DB・Web非依存で全採用手法の設定検証・実行・終了code/科学的状態の出力 | 新規Product REST endpoint、Worker queue/job、Browser UI |
| **Local files** | versioned config、validated design/estimand、JSON/Parquet/Markdown結果、checksum、Manifest、実効Library版・seed/split | Product DB migration、canonical Project lineage DBの代替 |
| **Scientific tests** | method別Unit/Contract/Known-truth/negative fixture、既存CLI/E9の回帰 | 新機能の科学的受入をBrowser E2Eのみで代用 |
| **既存Product** | 現行API/Worker/DB/UIが動作することを回帰で保護 | 新手法のProduct統合、Product側Gapの暗黙の閉鎖 |

### 1.2. 判定記号と採用の条件

| 記号 | 説明 | 合否・Scopeでの扱い |
|---|---|---|
| **R** | 再利用 | 現行FRの意味と既存コードを維持。必要な回帰試験は行う |
| **Q** | 品質強化／科学的妥当性検証 | 推論・適格性・診断の意味を測定し、既存科学契約の不足を明らかにする |
| **N** | 新規Scientific Core／local CLI／local file Capability | 今回採用候補。承認された場合は要件／設計／method別ACに展開 |
| **D** | 後続対応 | 今回実装しない。Phase4/旧Product統合/追加extensionの別スコープ |
| **要審査** | 旧上位構想とPhase指示が異なる／具体方式未確定 | 本書は案を提示するがHuman ownerの承認・同等性検証なしに確定しない |
| **R+N等** | 同一行の既存部分と追加部分を分離 | 行を無理に二重実装しない。実装Work Packageではさらに分解可能 |

「不採用（E）」は**科学的機能を妥当性不問で廃止する判断**ではない。本段階でそのようなE判定はしない。旧Web/API/Worker/DBの実装指示はDとする。**外部BackendのMethod/class availabilityは調査前であり、使用可能と断定しない。** 適用versionでmethodが存在しなければ、要件・科学的同等条件・独立評価を確認してオーナー承認による代替とする。

## 2. Phase 1の実装スコープ案

### 2.1. 基盤・Graph・識別・新規手法の採否

| 00_03行ID | 実装スコープ案 | CLI-onlyで提供する内容／明示的に外すもの | 対応Issue |
|---|---|---|---|
| `P1-01` | **R** | 現行Causal Question/Specを再利用。CLIで入力と参照IDを固定 | #15 |
| `P1-02` | **R+N／D** | 既存Spec versionを参照しlocal identity/hash追加。独立Product DB QuestionVersionは後続 | #15,#24 |
| `P1-03` | **R+N** | 現行Causal Design再利用。新識別に必要なlocal design項目のみ追加 | #15 |
| `P1-04` | **R** | DAG/CPDAG/PAG endpoint semanticsをそのまま保護 | #17 |
| `P1-05` | **R／D** | 既存Graph revision/provenanceを再利用。Consensus Graph等の独立新方式は後続 | #17 |
| `P1-06` | **R** | Native Randomized/Backdoor、nonidentified/review statusを保護 | #15,#16 |
| `P1-07` | **R** | Imported/User-defined GraphからIdentificationを開始する既存経路を保護 | #15 |
| `P1-08` | **N** | optional DoWhy識別：Backdoor/Frontdoor/IV、識別式・仮定・負結果 | #16 |
| `P1-09` | **N** | FCI/PAG Discovery：circle等のendpoint、背景知識、警告、CI test | #17 |
| `P1-10` | **R+N** | 既存Data Eligibility/Validation再利用＋新方式固有の適格性 | #15,#16 |
| `P1-11` | **R** | 既存ATE/ATTの差・OLS/IPW/AIPWを維持 | #19 |
| `P1-12` | **R+Q** | E9 Weight/Balance/ESS/Overlapを再利用。IPTW推論品質・SE/CI被覆を追加検証 | #19 |
| `P1-13` | **R** | Placebo Treatment/Data Subset Refutationを維持 | #16 |
| `P1-14` | **N** | Random Common Cause／Bootstrap Refutation、再推定・seed・再現性 | #16 |
| `P1-15` | **N（方法・設計は要審査）** | **適切な観測Negative Controlを指定できる研究に限り、研究者が明示的に要求して実行できる反証分析**を提供する方針を採用。NCO/NCEの2方式を科学的Method候補とし、未指定時に自動実行しない。不適格時は理由付きの負結果、非有意時も無交絡と解釈しない（2.3節・実装計画メモ）。 | #16 |
| `P1-16` | **R** | Adjustment Set/Propensity Clipping Sensitivityを維持 | #16 |
| `P1-17` | **N（要審査）／D** | 最小Nは**Cinelli–Hazlett partial R²／Robustness Value**のOLS係数に限定する案。現行のHC3を古典OLS公式へ無断適用しない。IPW/AIPW等の全面対応や追加A0方式は後続の個別判断（2.3節） | #16 |
| `P1-18` | **R+N／D** | 既存Lineage/Manifestを再利用しlocal manifest増強。Product canonical DB Gapは別Issue審議 | #15,#24,#14 |
| `P1-19` | **D** | 新しいProduct API/Worker/DB migration/RBACは後続。現行経路を変更しない | #14 |
| `P1-20` | **R+N** | 既存Scientific CLI再利用。新Identify/Refute/Sensitivity引数と版付き成果物を追加 | #16,#24 |
| `P1-21` | **R+N** | 既存Known-truth tests保護＋DoWhy/FCI/追加refuterの独立科学受入 | #16,#17,#24 |

### 2.2. Phase 1の必須Method・受入境界

- **必須候補として列挙:** FCI（PAG）、optional DoWhy Backdoor/Frontdoor/IV、Random Common Cause／Bootstrapを含むRefutation、既存Placebo/Data Subset、Adjustment Set／Propensity Clippingと追加Unobserved-confounding Sensitivity、Negative Control exposure/outcomeの方法契約。既存Native識別・ATE/ATT・IPW/AIPWはRとして保護する。
- **Quality:** IPTWの推定Propensity下のSE/CI、overlap・extreme weight・ESS、correct estimandの判定は実装済みと断定せず、E9回帰を含めて科学的に評価する。
- **要審査:** NCE／NCOの2方式とOLS係数へのpartial R²を**科学的な最小候補として具体化**した。ただし観測対照のvalidity、HC3／古典OLSの分離、IPW/AIPWへの非適用、Human ownerによるPhase1採否は未決であり、方法の存在だけで科学的受入を主張しない。A0全方式の無条件実装も意味しない。
- **旧Product媒体:** 独立CausalQuestionVersion DB、API/RBAC/Worker/DB migrationの部分はD。Local identity／manifestが今回Nであり、この二者を混同しない。

### 2.3. Negative Control／未観測交絡Sensitivityの科学的方式（2026-11-01技術案）

**方法検討の根拠・fixture・負結果:** [20261101_negative_control_unobserved_confounding_method_review.md](../working_notes/20261101_negative_control_unobserved_confounding_method_review.md)。**Negative Control実装計画案:** [20261101_negative_control_implementation_plan.md](../working_notes/20261101_negative_control_implementation_plan.md)。

**オーナー確認済みの機能原則（2026-11-01）:** 「適切なNegative Controlを指定できる研究に対し、科学的に解釈可能な反証分析を提供する」。**全研究への実行義務ではない**。分析者の明示的opt-in、対照nullの科学的根拠、適格性確認を要し、不適格・未指定・シグナル未検出を区別する。本節はSR-06の具体化であり、**NCO/NCEのMethod、結果enum、正式FR/AC・Gateの承認は未実施**。現行Scientific CLI・Domain enumには下記新Methodを実装していない。

| 候補Method ID | 必要なDesignと計算 | 出力・拒否条件 |
|---|---|---|
| `NEGATIVE_CONTROL_EXPOSURE`（P1-15） | 観測されたZがYへ因果的に影響せず、対象A–Yと検出したいバイアス構造を共有する根拠を分析者が指定する。事前指定した`Y ~ Z + C_Z`などの**条件付き関連null**を検査。Aの条件付けはDAG上妥当な場合のみ | 係数・区間・P値・対照選択理由・警告。妥当なZ／null／conditioning setがない場合は`NOT_APPLICABLE`／要レビュー |
| `NEGATIVE_CONTROL_OUTCOME`（P1-15） | 観測されたWがAから因果的影響を受けず、懸念するバイアス構造を共有する根拠を指定する。事前指定した`W ~ A + C_W`などの**条件付き関連null**を検査 | 同上。Wが後処置・対照nullに反する、設計根拠がない場合は拒否・要レビュー |
| `UNOBSERVED_CONFOUNDING_PARTIAL_R2`（P1-17） | 事前指定した**連続Yの古典的OLS係数**について、仮想Uと処置A・結果Yの**条件付きpartial R²（2軸）**のgridを設定し、OVB感度曲線・係数0へのRobustness Valueを計算 | OLS係数/古典SE/残差df、grid、RV、仮定・Reference。既存HC3 SEを古典公式へ流用しない。IPW/AIPW、非線形・CATE等には**最小方式を適用しない** |

**解釈上の不変条件:** Negative ControlのNull非棄却もpartial R²上の高いRVも「未観測交絡の不存在」を証明しない。Negative ControlはPlacebo変換・Random Common Causeと区別する。両方式でnull自体が不当なら、効果数値や「PASS」を生成しない。

**依存・品質の前提:** 初期実装は外部DoWhyへの依存を必須とせず、現行Scientific Coreで利用可能な回帰機構を評価する。ただしOLS refitの係数・完全ケース・古典SE/dfと元Resultとの同一性、およびsensemakr参照計算とのパリティを**科学Benchmarkで検証する必要**がある。現行`robust_se="HC3"`の結果を感度分析の古典SEとして誤用しない。固定した閾値・seed・Reference version・CLI schemaは要件03／設計04／Gate 07で決定する。

**留保:** **『NCO/NCEを利用できるCapability』と『全分析での実行必須』は別**。NCO/NCE双方をPhase1で提供するか、Null検査のモデル・受入条件、OLS限定SensitivityでA0の要求を満たすか、より一般のIPW/AIPW/CATE等へのSensitivityやSimulated Confounder／Graph Perturbationを後続に送るかは、Human ownerが個別判断し承認記録02へ記す。

## 3. Phase 2の実装スコープ案

### 3.1. CATE/HTE・EconML・成果物の採否

| 00_03行ID | 実装スコープ案 | CLI-onlyで提供する内容／明示的に外すもの | 対応Issue |
|---|---|---|---|
| `P2-01` | **N** | CATE/HTE estimand、effect modifier、ATEとの差、Result schema | #18 |
| `P2-02` | **N** | LinearDMLを方法候補として必須一覧へ。利用版/APIを審査 | #18 |
| `P2-03` | **N** | CausalForestDMLを方法候補として必須一覧へ。利用版/APIを審査 | #18 |
| `P2-04` | **N** | DRLearner。既存AIPWとは別のCATE方法契約 | #18 |
| `P2-05` | **N** | ForestDRLearner、support/forest inference | #18 |
| `P2-06` | **N** | S-Learner、効果と予測の意味の分離 | #18 |
| `P2-07` | **N** | T-Learner、処置群別support診断 | #18 |
| `P2-08` | **N** | X-Learner、arm非対称とpseudo-outcome対応 | #18 |
| `P2-09` | **N** | DRIVまたは承認済み科学的同等IV+ML。代替を黙認しない | #18,#22 |
| `P2-10` | **N** | EstimationSpecification/HeterogeneityResult、nuisance/final/CI/subgroup | #18 |
| `P2-11` | **R+N** | 既存optional依存隔離原則を再利用しEconML能力・version・unavailableを追加 | #18,#24 |
| `P2-12` | **R+N** | 既存AIPW cross-fitting再利用＋CATE専用fold/seed/split/漏洩防止 | #18,#24 |
| `P2-13` | **R+N** | 既存Eligibility再利用＋effect modifier/IV/forest等の条件を拡張 | #18 |
| `P2-14` | **N** | CATE support/calibration/stability/uncertaintyと負結果 | #18 |
| `P2-15` | **N** | プライバシー制限付きCATE Parquet、群別JSON、checksum | #18,#24 |
| `P2-16` | **N** | 一定/線形/非線形異質性の既知真値、bias/RMSE/coverage/runtime | #18,#24 |
| `P2-17` | **N** | 列挙したEstimator群を個別追跡。『4 family以上』を削減根拠としない | #18 |
| `P2-18` | **D／N** | Paged Product API/UI/Worker/DBは後続。成果物はlocal Parquet/JSONで代替 | #18,#24 |

### 3.2. Phase 2の必須Estimatorと科学的条件

- **列挙した必須候補を保持:** LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S-Learner、T-Learner、X-Learner、DRIVまたは科学的に同等なIV+ML。実際のEconMLのclass名／signatureは採用versionで**これから検証**する。
- **解釈:** 全Estimatorに対しTreatment/Outcome型、estimand、CATE support、cross-fitting/seed/split、interval availabilityをCapability metadataで明示する。結果は予測group差やATEと混同しない。
- **採用範囲を黙示的に削らない:** A2の「4以上のestimator family」は最低Acceptance条件であって、列挙Methodのうち4件だけを実装すれば終了とする根拠ではない。代替が必要なら科学的同等性と人間承認を記録。
- **出力:** 個票CATEの安全なParquetと群別JSON、Backend・seed・splitのManifestはN。旧paged API/Worker/DBはD。

## 4. Phase 3の実装スコープ案

### 4.1. 時系列因果・準実験デザインの採否

| 00_03行ID | 実装スコープ案 | CLI-onlyで提供する内容／明示的に外すもの | 対応Issue |
|---|---|---|---|
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
| `P3-12` | **N** | IV/LATE。weak-IV、exclusion、monotonicity等の仮定 | #22 |
| `P3-13` | **N** | Synthetic Control。donor、pre-fit、placebo、RMSPE | #23 |
| `P3-14` | **N** | Synthetic DiD。panel、donor重みと処置重みの区別 | #23 |
| `P3-15` | **N** | QuasiExperimentalDesignと各method固有のEstimand・Eligibility | #21,#22,#23 |
| `P3-16` | **N** | Method別known-truthとpretrend/manipulation/weak-IV/donor負例 | #20,#21,#22,#23,#24 |
| `P3-17` | **R+N** | 既存CLI成果物基盤再利用＋Temporal/Quasi専用JSON/Parquet/Manifest | #20,#24 |
| `P3-18` | **D** | RPCMCI/J-PCMCI+は8月Phase3自身の拡張候補。Phase3必須外 | #20 |
| `P3-19` | **D／N** | 新Quasi Product API/UI/DB/migrationは後続。local spec/fileを追加 | #21,#22,#23,#24 |

### 4.2. Phase 3の必須Methodと科学的条件

- **Temporal:** PCMCI、PCMCI+、LPCMCIの**3方式すべてをPhase3の追跡対象として維持**。Methodごとにlag／同時点／潜在交絡の仮定、CI-test、TemporalDesign、Graphの不確定endpointを区別する。2026-11-01オーナー方針はPython3.12＋Linux基準、機能別optional依存、科学検証後のversion lock。**Tigramiteの実効動作・個別SI納入におけるGPLv3適合性は未検証／未承認**。
- **Quasi:** DiD、Event Study、Interrupted Time Series、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control、Synthetic Difference-in-Differences。各Designが異なるEstimand・必要データ構造・適格性を持つことを要件化する。
- **Scientific negative cases:** 不適切なtime index、staggered adoptionの不適合、pretrend、RD manipulation、weak/invalid IV、donor汚染/pre-fit不良では、無理に数値を返さず`NOT_IDENTIFIED`／`REQUIRES_REVIEW`／科学的警告等を出力する。
- **Phase3自身の拡張候補:** RPCMCI/J-PCMCI+はD。新Productサーバ経路もD。

### 4.3. PCMCI系の利用場面とSR-02方針（2026-11-01）

**詳細な適用条件・SIライセンス審査前提・検証項目:** [20261101_external_backend_policy_temporal_scenarios.md](../working_notes/20261101_external_backend_policy_temporal_scenarios.md)。

| Method | 分析者が選択する場面 | 重要な仮定・結果 |
|---|---|---|
| `PCMCI`（P3-02） | 観測変数間の**時間遅れの因果的候補**を調べる | 同時点直接因果リンクなし／潜在共通原因なし／causal stationarity。lag付きGraphの仮定と統計量を保存 |
| `PCMCI+`（P3-03） | **同時点と遅延**の関係を共に探索する | 潜在共通原因なし／causal stationarity。time-series CPDAGの向き未確定を保持 |
| `LPCMCI`（P3-04） | **潜在交絡を排除できない**多変量時系列を調べる | causal stationarityなど。time-series PAGのcircle／arrowhead／tailを保持。公式のexperimental設定に注意 |

**Eligibility:** 時刻・sampling interval・lag・欠測・CI-testの適用性を確認し、仮定の正当性は研究者の申告と機械検査を区別する。仮定不足や非定常が疑われるデータで自動的な因果効果の断定をしない。

**SI配布の留保:** 配布形態は個別SIによる顧客環境への構築・納入（SaaS非想定）。TigramiteはGPLv3系であり、**optional import／直接pip install／顧客環境への導入という形式だけでGPLv3適合が自動成立するとは扱わない**。実際に納入するコピー、結合方法、ソース・ライセンス通知等を審査するまで顧客配布を承認しない。

**SR-02追試結果（2026-11-01）:** [実行試験記録](../working_notes/20261101_sr02_backend_runtime_probe_results.md)。Ubuntu 24.04／Python 3.12.15でAriadne＋DoWhy 0.14／EconML 0.17.0／Tigramite 5.2.10.1の**単独・同時依存install、依存check、15のMethod別API smokeが成功**。EconML DRLearner・S/T/X-Learnerは今回の構成では**点推定可・区間推定不可**。**科学Benchmark、既存回帰、実際のextras/lock、SI GPL適合は未実施**のためSR-02は**OPEN（一部検証済み）**。

## 5. A0上位構想・横断事項の採否案

### 5.1. Phase別指示から独立した上位要求の処理

| 00_03行ID | 実装スコープ案 | CLI-onlyで提供する内容／明示的に外すもの | 対応Issue |
|---|---|---|---|
| `X-01` | **D（要承認）** | ATCはPhase別必須リストに独立指定なし。controlled direct effectはPhase4側 | #14 |
| `X-02` | **D** | MediationはPhase4のextension pointへ。Phase1〜3の必須には算入しない | #14 |
| `X-03` | **D（要承認）** | Matching/汎用g-computationはA0上位のみ。既存OLS等を同等扱いしない | #14 |
| `X-04` | **N一部／D** | 観測NCE/NCOの**対照null検査2方式をP1-15で候補化**。DoWhyのrandom/placeboとは異なる。Simulated Confounder/Graph Perturbationは後続提案（オーナー未承認） | #16,#14 |
| `X-05` | **N一部／D** | 未観測交絡の最小方式はP1-17の**OLS partial R²**候補。IPW/AIPW/CATEへの一般化、その他のモデル・欠測・Graph Sensitivityは対象外案（正式採否保留） | #16,#14 |
| `X-06` | **Q一部／D** | 採用手法のCI/cluster/bootstrap/stabilityは必要条件として品質検証。一般的多重検定・全Graph consensusは後続 | #19,#20,#21,#24 |
| `X-07` | **D** | Policy Value、cost/capacity、off-policy/自動配信はPhase4 | #14 |
| `X-08` | **D** | Monitoring/drift/再分析triggerはPhase4 | #14 |
| `X-09` | **R+N／D** | Local reproducibilityは#24で追加。Product GAP-C01〜04は閉鎖せず移管要審査 | #14,#24 |
| `X-10` | **R+N／D** | 既存Product入口は保護。新手法はScientific Core/CLIのみ。新API/Worker/UI/DB統合は後続 | #14,#24 |

### 5.2. 上位構想の不一致をどう承認するか

1. **ATC／matching／g-computation:** A0上位要求だがA1〜A3の独立必須Methodに指定がないため**今回のScope案ではD**とする。一般g-computationを現行OLSと同一視しない。採否・別Issue・科学的必要性について02の承認者判断を要する。
2. **Mediation／controlled direct effect:** A4 Phase4のExtensionに属するためD。後続で具体的なmediation識別や自然直接効果等を検討する。今回のPhase1〜3の必須には黙示的に算入しない。
3. **Negative ControlとUnobserved-confounding Sensitivity:** A0・A1の強度差に対し、第2.3節の**観測NCE／NCOの2つのnull診断**と**OLS限定partial R²／RV**を最小Nとして提案する。これは全推定器に適用可能なSensitivityやNCでの交絡不存在証明ではない。方式の採否・限定範囲・後続拡張は02で個別判断し、異なる方式への代替も科学的根拠を示す。
4. **Method内の品質要件:** DiDのcluster、CATEのcross-fitting、FCIのstability、RDDのdensity等、採用Methodに不可欠な品質検証はスコープのQ/Nに含む。一般的多重比較や全Discovery consensusの独立システムはDとする。

## 6. 既存Foundation GapとCLI-only実装の境界

### 6.1. GAP-C01〜C04の扱い

| 現行Gap | 関連正本の未充足 | 今回の方針案 | 閉鎖の責任と状態 |
|---|---|---|---|
| **GAP-C01：探索データ再利用warning** | FR-051/AR-004 PARTIAL | **D：既存Productの警告経路は変更しない**。Local CLIの探索後推定については結果の誤用防止をNとして定義 | #14で別Enhancementへの帰属審議。**未閉鎖** |
| **GAP-C02：Canonical Lineage** | FR-008/054/095、NFR-002 PARTIAL | **D：Product DB canonical chainは今回修正しない**。Local input/design/result/artifact provenanceのみN | #14でResource authorityの帰属を審議。**未閉鎖** |
| **GAP-C03：実効version/seed** | FR-086a/087b、NFR-001b PARTIAL | **N：新CLIに使用Backend version/seed/split/manifest必須**。既存Product Execution/StageAttemptは保護 | #24 CLI分を扱うが現行Product要件の残差は#14で別審議。**未閉鎖** |
| **GAP-C04：Navigation Capability ownership** | FR-132/133/144 PARTIAL、FR-145/NFR-023 NOT_IMPLEMENTED | **D：新CLI科学実装の対象外**。既存Navigationを変更しない | #14でArchitecture課題として別Enhancementを審議。**未閉鎖** |

### 6.2. 現行要件を黙って閉鎖・改定しない

上表のDは**現行正本の既存Gapを解消しないことの実装帰属案**であり、`Requirement Status`や`Implementation Status`を更新する権限ではない。Human ownerが各Gapの責任・追跡Issue・期日を決定するまでは未解消として記録する。**Product修正が必要な場合に、CLI-onlyの実装完了を理由として既存Product FRを`IMPLEMENTED`へ変更しない。**

## 7. 完了状態・インターフェース・科学的受入への引渡し

### 7.1. 01のユースケースとスコープの対応

| UC（01第4章） | この案で提供する利用方法 | 新規Method群／既存再利用 | 科学的な否定例・受入主張 |
|---|---|---|---|
| UC-01 潜在交絡の探索 | CLIでFCI/PAGのuncertaintyを得る | FCI N、PC等R | PAG endpointを強制DAG化しない |
| UC-02 観察研究の識別 | native/optional DoWhyで識別戦略を宣言 | DoWhy N、Native R | frontdoor/IV非識別、仮定不足 |
| UC-03 平均効果とoverlap | CLIでIPW/AIPW・E9診断を比較 | 既存R＋科学品質Q | extreme weight、poor overlap、誤ったCI |
| UC-04 CATE/HTE | Local CATE file/群別比較 | DML/DR/Forest/Meta N | support不足、分割漏洩、interval unavailable |
| UC-05 Temporal探索 | CLIでlag/CI-test/不確定関係を得る | PCMCI系 N | 不正時刻、stationarity疑義、CI-test不適格 |
| UC-06 段階導入施策 | CLIでDiD/Event/ITS | 3手法N | pretrend違反、staggered偏り |
| UC-07 閾値による割当 | CLIでsharp/fuzzy RDD | RDD N | manipulation、bandwidth不適格 |
| UC-08 IV施策効果 | CLIでIV/LATE・関連Design | IV/LATE N | weak-IV、exclusion違反の疑義 |
| UC-09 合成対照 | CLIでSynthetic/SDID | 2手法N | donor汚染、pre-fit不足 |
| UC-10 再現・監査 | Manifestと安全なファイル再実行 | 既存CLI R＋新schema N | 実効版・seed/hash不足、不一致 |

### 7.2. 要件・設計・Gateに渡す内容（未承認）

- **要件03:** 00_04のP1/P2/P3/X-ID→新FR/NFR/AR semantic delta候補。正本§11のDoWhy/EconML除外との衝突は承認差分で解消。既存FRを黙って広げない。
- **設計04とArchitecture Review:** Scientific Domain authority、optional backend/registry、local version/hash、privacy、Method-specific estimand、result/negative status、compatibilityを審査。
- **科学的検証:** 各必須Methodの適格／不適格とKnown-truth、bias/coverage/support/temporal/quasiの閾値をGate 07で固定し、独立検証に回す。
- **Work Package:** **今回割当てない**。#15〜#24のIssueと方法別受入条件から、設計承認後に切り出す。G01〜G10は未固定。
- **実装許可:** Human ownerによる01/02の承認、03/04/05とArchitecture Review、Gate 06/07のfreeze前には発行しない。

## 8. ステップ4の到達点・残存する承認事項

### 8.1. この資料で準備済みの事項

00_03からの**68行をすべて再分類**し、P1=21／P2=18／P3=19／X=10として、既存再利用・科学的品質強化・新規CLI科学機能・Product/Phase4等の後続項目を明確化した。Phase1〜3の列挙された方法を無断で縮小せず、A0上位だけの機能は承認すべきScope例外として登録した。以上を**ENH-E11のCLI-only実装スコープ案（ステップ4の作業成果物）**とする。

### 8.2. Human ownerとArchitecture Reviewへ残す決定

次の承認を得るまでは**STEP4_SCOPE_PROPOSAL_PREPARED**とする。

1. **必須Methodと同等代替:** DoWhy/FCI、EconML全候補、Tigramiteと準実験、**第2.3節のNCE/NCO／OLS partial R²の採否と適用対象・代替条件**、Library版・scientific equivalence。
2. **A0上位要求のScope例外:** ATC、matching/g-computation、多重比較、追加graph perturbation等を今回Dにする案の明示承認。
3. **既存Gapの別案件帰属:** GAP-C01〜C04の責任者・Issue・Closure Gateを別途決定（ここでは未閉鎖）。
4. **既存CLIと成果物の境界:** config version、ファイル入出力の安全性、個票CATEのprivacy、optional dependency、seed/split、Method-specific negative status。
5. **要件・設計と科学的AC:** 正本FR/NFR/AR、Architecture Decision、数値BenchmarkとGate 06/07、Work Packageを承認後に固定。

**この資料を作成したことは、ステップ5〜6の完了、新規コード実装、canonical 999 PASSを意味しない。**
