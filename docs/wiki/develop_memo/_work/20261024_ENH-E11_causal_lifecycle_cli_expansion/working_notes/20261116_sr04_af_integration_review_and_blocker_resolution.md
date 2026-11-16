# ENH-E11 — SR-04 A〜F 統合レビュー・残余Blocker解消記録（2026-11-16）

**文書区分:** working_notes／独立統合レビュー、是正記録および未採用事項の決定案。正式要件、Method、Architecture Decision、Gate06/07、Coding権限を新規承認する文書ではない。  
**実施日:** 2026-11-16 JST。  
**対象:** `kousuke-ota-datascience/causal-atelier`、branch `prototype/ariadne_mvp`。  
**総合結論:** **CHANGES_REQUIRED / MATHEMATICAL_AND_TRACEABILITY_CORRECTIONS_APPLIED / SCIENTIFIC_BLOCKERS_OPEN / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL**。

> **2026-11-16正式個別判断の追補（本レビュー後の更新）:** [DEC-SR04-01／02の技術判断記録](20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md)を作成し、02 Owner記録の第18・19項へ**B1-AとDRIV-Aの採用**を反映済み。本レビューが作成された時点の「OWNER_PENDING」という記載は**上記2件のsemantic target採用に限り解消**。表の状態は`OWNER_ACCEPTED / SCIENCE_PENDING`へ更新した。B1の正式schema enum/ARとDRIVの実効Estimator/CI/coverage、全体構想・FR/ADR/Gate07は未承認・未検証。Next owner decisionはDEC-SR04-03（Frontdoor）／DEC-SR04-04（Graph Oracle）。

> **2026-11-16後続Owner判断（DEC-SR04-03／04）:** [FD-A 独立技術記録](20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md)と[GRAPH-A 独立技術記録](20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)を作成し、[02承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)の第20・21項にHuman ownerの個別採用を反映。**DEC-SR04-03／04のOwner判断はCLOSED**。DoWhy stage・CI、独立PAG/CPDAG/Temporal Oracle・Graph科学的受入、正式FR/ADR/Gate07・全体構想は引き続きOPEN。

> **2026-11-16 DEC-SR04-05実施追補:** [7手法Estimator／Inference独立判断](20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)を作成し、[02 Owner記録](../00_enhance_background/02_enhancement_concept_approval_record.md)第22項に**7個別Method baseline方針の採用**を反映。Method設計選択は`OWNER_BASELINE_ACCEPTED`であり、推論科学妥当性・backend/lock・独立Reference/CI coverage・正式Gateは`PENDING`。旧表「05 Owner pending」はこの新判断で改訂。

> **2026-11-16 DEC-SR04-06 Owner採用追補:** [NCE/NCO＋OLS partial R²/RV独立技術判断](20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)の**DEC06-1〜5すべてA**をHuman ownerが明示採用し、[02承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)第23項に登録。P1-M18/19/20を初期N、広範なX-04/X-05を後続Dとする個別Owner採否は**CLOSED**。RVの独立数値Reference、Null size/power、適格Inference・Runtime、正式FR/ADR/全体Scope/GateはOPEN。

## 0. 目的、審査条件、適用した証拠レベル

### 0.1. 審査対象（SR04 A〜Fと先行正本案）

| 対象 | 資料 | 検証したGit blob SHA（レビュー後の版） |
|---|---|---|
| A Method Acceptance Matrix | [20261115_sr04_method_acceptance_matrix_draft.md](20261115_sr04_method_acceptance_matrix_draft.md) | `cd7327cc99f03b2a97adedb9e5cf53bf139b626b` |
| B Scientific Fixture Catalog | [20261115_sr04_scientific_fixture_catalog_draft.md](20261115_sr04_scientific_fixture_catalog_draft.md) | `f0a7847b382aa134fefd8b295491624eb583a907` |
| C Reference Specification | [20261115_sr04_reference_specification_draft.md](20261115_sr04_reference_specification_draft.md) | `e8f5e4df4677c50ed3578eac7931c3d80f715f3f` |
| D Quantitative Acceptance Criteria | [20261115_sr04_quantitative_acceptance_criteria_draft.md](20261115_sr04_quantitative_acceptance_criteria_draft.md) | `443c1c6549179402ca1582b92d445c366832e133` |
| E Execution Environment Contract | [20261115_sr04_execution_environment_contract_draft.md](20261115_sr04_execution_environment_contract_draft.md) | `924b4c3af0e0f790838d1031a6a43874dd6973db` |
| F Gate07 Traceability | [20261115_sr04_gate07_traceability_draft.md](20261115_sr04_gate07_traceability_draft.md) | `1654196e31795a5f1f62e62141ac038071e68df1` |
| 承認権限の基準 | [02 Owner decision](../00_enhance_background/02_enhancement_concept_approval_record.md)、[03 Requirements](../00_enhance_background/03_requirements_revision.md)、[04 Design](../00_enhance_background/04_design_revision.md)、[05 Consistency](../00_enhance_background/05_requirements_design_consistency_and_traceability_review.md) | 03/04/05は承認前Draft |
| 過去レビュー | [20261029_cli_scope_review.md](20261029_cli_scope_review.md) | SR-01〜12 CHANGES_REQUIRED。単にSR04を作成してもこれらは自動的に閉鎖しない |

**Evidence分類:** (a) GitHub文書・Scope/Method/IDの直接照合、(b) 定義されたDGP/Estimatorの数学的導出と別の数値計算によるsanity check、(c) 公式Backend仕様の静的照合、(d) 実環境・Monte Carlo・Graph Oracleの**未実証**、(e) Owner/Architecture/Legalの**未承認**を混同しない。

この記録の「解消済み」は**科学的な意味誤りまたは追跡欠落が文書上で修正された**という限定的な意味。Runtime/Inference coverage/Method正式採用の達成とは別。

### 0.2. 主要な数量の照合

| 集合 | 定義数 | 状態 |
|---|---:|---|
| Scope行 | 68（P1=21、P2=18、P3=19、A0横断=10） | 全行に追跡Disposition案が存在。正式承認前 |
| Method | 41（Phase1=20、Phase2=8、Phase3=13） | A/B/C/D/Fで方法ID照合。P1-M18〜20は具体Method採否未決 |
| DGP | 24 | Bに全ID定義、Fに全24の参照（AR集合代数DGP-024を含む） |
| NEG | 28 | 短縮表記を展開しMethodへの逆引き28/28。Hidden violationの全自動検出は要求しない |
| REF | 24 | Method由来23種に横断`REF-X01`を加えて24。独立Referenceのソースコードは未実装 |
| Quant AC | 45 | 45/45定義。うち11件はMethod directではなくCross/Conditional/Report-onlyへ是正結合 |
| ENV-AC | 9 | 定義9/9、実行は未了 |
| SR04横断Contract | 9 | Fで`SR04:X-*`と`SCOPE:X-*`を区別。横断範囲はDraft |
| E11-REQ仮ID | 17 | 03/05と照合。正式FR/NFR/ARに未承認 |
| Issue | #14〜#24の11件 | GitHub各Issueの存在とopen/PLANNINGを照合。Issueのclose/文書の有無≠科学的PASS |

## 1. 統合レビュー指摘と是正（Findings）

### 1.1. 是正できた事項 — 追加のOwner判断を要しない範囲

| Finding | Severity | 根拠・是正内容 | 修正先 | 進捗 |
|---|---|---|---|---|
| IR-01 ID collision | MAJOR | 68 ScopeのX-01〜10とSR04横断X-01〜09を別名前空間に正規化。PLAN:G07と科学受入Gate07を別扱い | F | **DOC_RESOLVED** |
| IR-02 Negative短縮表記 | MAJOR | Bの`NEG-011,012,013`等をFで完全IDへ展開、28/28にMethod逆引きを作成 | F | **DOC_RESOLVED** |
| IR-03 Quant AC 11件未結合 | MAJOR | AC-D04/D05/D06・I04/I05/I06・T04/T05・P02/P04/P06をCross/Condition/Report-onlyに再バインド | D/F | **TRACE_DRAFT_RESOLVED** |
| IR-04 Cross Oracle未結合 | MAJOR | 横断`REF-X01`の適用先をSR04:X-01〜09と明記。Methodへの誤分類は禁止 | F | **TRACE_DRAFT_RESOLVED** |
| IR-05 Markdown構造不整合 | MAJOR | Bの縦棒文字を含むDGP table、DのAC-P01数式table、C/Dのliteral escaped backticksを修復 | B/C/D | **DOC_RESOLVED** |
| IR-06 DRIVのoff-support評価 | **BLOCKER** | DGP-008はX∈{-1,+1}なのにDのDRIV評価点を非IV CATEの3点Gridと共通化していた。DRIV gridを{-1,+1}へ是正 | A/B/C/D | **DESIGN_ERROR_RESOLVED**（formal theta/CIはOPEN） |
| IR-07 FCI潜在交絡の過剰主張 | **BLOCKER** | DGP-011の同時点2観測変数でlatent Hの存在をbidirected edgeとして必ず識別できるとは言えない。生成DAGの真値≠FCIのPAG向きのOracle。用途をStress/uncertaintyに限定 | A/B/C/D | **FALSE_ACCEPTANCE_REMOVED**（独立PAG oracleはOPEN） |
| IR-08 Wald単独とAR義務の衝突 | MAJOR | P3-M09は通常のWald比。P3-M10/M11のG2 AR集合を自動必須としたC側のREF-U01引用を除去しD/Fと整合 | C/F | **DOC_RESOLVED** |
| IR-09 AIPW ATTのReference欠落 | MAJOR | ATT-AIPWをATE式の流用でなく別のDR式としてCに明示。推定PS込みInfluence Function/CIは別検証 | C | **ANALYTIC_REFERENCE_DEFINED**（Inference OPEN） |
| IR-10 B1の母集団射影式が曖昧 | MAJOR | 固定線形共変量への母集団残差化後のIV係数と異質効果下の比をCに導出 | C | **MATHEMATICAL_TARGET_DEFINED**（formal Estimand enum OPEN） |
| IR-11 ARの代数参照に数値端点不足 | MAJOR | DGP-024の4集合形状と数値端点を独立二次不等式計算でCに明記 | C | **ALGEBRA_CHECK_DONE**（raw sample・Coverage OPEN） |
| IR-12 FのSource版差分 | MAJOR | A/B/C/Dの修正後のblob SHAをFへ更新。正式Gate evidenceのfreezeではない | F | **DOC_RESOLVED** |

**残りの重要な制約:** 文書の一部で`BLOCKER`と書かれているのは、数学的に未定義な箇所だけでなく、未実装/未計測/未承認の箇所も含む。今後は`MATH_PENDING`、`METHOD_CONFIG_PENDING`、`REFERENCE_IMPLEMENTATION_PENDING`、`RESOURCE_PENDING`、`OWNER_APPROVAL_PENDING`、`LEGAL_PENDING`を併記し、単一の「Blocker」として放置しない。

### 1.2. 数学的Referenceの独立sanity check（Science PASSではない）

1. **DGP-003のATT:** \(e(x)=0.5+0.3x\)、\(\tau(x)=2+x\)、X~Unif[-1,1]より、\(E[X|A=1]=0.2\)、ATE=2、ATT=2.2。DGP-004はATE=7/3、ATT=38/15。
2. **ATT-AIPW:** \(n_1=\sum A_i\)、\(\widehat\mu_0\)と\(\widehat e\)を用いる独立候補：
\[
\widehat\tau_{ATT}
=\frac{1}{n_1}\sum_i\left[A_i\{Y_i-\widehat\mu_0(X_i)\}-(1-A_i)\frac{\widehat e(X_i)}{1-\widehat e(X_i)}\{Y_i-\widehat\mu_0(X_i)\}\right].
\]
   現行AIPW実装の有限標本normalize方式とのパリティ、cross-fit nuisanceとCIは実コードprobeを必要とする。
3. **DGP-005 Frontdoor:** A→Mの線形係数=1.5、Y~M+AのM係数=2、全媒介のATE=3。一般frontdoor functionalと2段階線形積の一致は本DGPの追加仮定に条件付き。DoWhy実効StageにAが入るかを独立probeするまではBackend contract未完了。
4. **DGP-007 B1:** \(\tilde Z=Z-\Pi_{1,C}Z\)、\(\beta_{IV,lin}=E[\tilde ZY]/E[\tilde ZA]\)。均質線形効果DGPではβ=2。異質\(\tau(C)\)下では、追加仮定のもと \(E[\tilde ZA\tau(C)]/E[\tilde ZA]\) という射影であり、一般のcomplier LATEやATEではない。
5. **DGP-008 DRIV:** \(\theta_{IV}(x)=Cov(Y,Z given X=x)/Cov(T,Z given X=x)=2+0.5x\)（本DGPの線形構造下）。x=-1→1.5、x=+1→2.5。Final modelに切片が無い場合、この関数を表現できない構成がある。
6. **DGP-024 AR:** \(q=\chi^2_{1,0.95}\approx3.841458820694124\)。AR-Q1は[1.0518218236251204,5.926895365726481]、Q2は(-∞,-0.20315286487771517]∪[0.20315286487771517,∞)、Q3は[-0.7248752638076998,∞)、Q4は全実数。**集合形状の独立代数チェックであり、ARの有限標本coverageやweak-IV下の推論validityの実測ではない。**

数値サンプルの簡易spot check（Python/NumPy/Scipy、GitHubリポジトリ外）でも、Frontdoor2-stageの積≈3、B1のsample IV係数≈2、DRIV conditional covariance ratio≈1.5/2.5という方向の整合を確認した。しかし**生成コードとランダムseed/依存版をScientific Evidenceとして固定しておらず、これらをGate07のReference implementation/Monte Carloとして認めない**。

## 2. 未解消Blockerの選択肢・推奨案・承認境界

以下の案は**Human ownerとScientific Methods ownerの承認に供する判断票**であり、この文書に書いたことだけで採用された扱いにはしない。

### 2.1. SR04-R01 B1：Estimandの正式分類

| 案 | 対象・制限 | 長所／重大な制約 |
|---|---|---|
| **B1-A（推奨）** | 単一Z/Aと事前指定Cによる**加法線形IV構造係数β**をformal targetとする。対象outcome equation Y=α+βA+γ'C+ε、Instrument moment/Rank、処置前Cを要求 | D03で採用済みのB1範囲と整合。均質性等を明示。異質効果時に一般LATE/ATEと命名しない |
| B1-B | 残差化IV比をより一般の**線形射影target**として公開。異質効果下でもweighted ratioを計算可能 | 数値の定義は広いが、処置効果の非負加重平均・complier LATEとしての因果解釈は別途証明が必要 |
| B1-C | 条件付きcomplier LATE/多変量GMMを初期必須へ拡張 | SR03-D03 C1の「初期C不採用」に抵触。再承認と新科学Methodが必要 |

**レビュー提案:** B1-Aで最小契約を確定する。正式enum名は候補\(\mathrm{LINEAR\_IV\_STRUCTURAL\_COEFFICIENT}\)だが採番未承認。C後続Triggerは維持し、IVのheterogeneityがある現実研究ではineligible/reviewに回す。**未解決:** Owner承認、DGP-007のraw estimator/inference/HC0-vs-HC1、DGP-024 AR集合とcoverage、method config。

### 2.2. SR04-R02 DRIV：条件付きIV targetとEstimatorの射影

| 案 | 対象・制限 | 科学的リスク |
|---|---|---|
| **DRIV-A（推奨）** | 連続T/Z、\(X\)ごとの\(\theta_{IV}(x)=Cov(Y,Z given X=x)/Cov(T,Z given X=x)\)を、部分線形構造・IVの独立性/除外/関連性の下での**conditional structural treatment slope**として定義 | Final modelがθを表現できなければ不一致。弱い条件付きIV、W有り時のモーメント、最終射影とinferenceを別検証 |
| DRIV-B | Backend特定final modelへの重み付き射影を正式targetとする | 構成依存のtargetになりMethod/版本ごとの意味説明が複雑。汎用な`IV_HETEROGENEOUS_EFFECT`として過大な互換性を主張しやすい |
| DRIV-C | Complier CLATE/LATEに統一 | binary Z/Aとmonotonicity等が無い現在の連続IV fixtureとは別。SR03-D01の区分に抵触 |

**レビュー提案:** DRIV-Aを採用候補。DGP-008はx=-1/+1だけ評価。EconML DRIVで`model_final`、`fit_cate_intercept=True`相当、`projection=False`、`opt_reweighted=False`、`cov_clip`、`cv`、推論方式をversionごとに明示して独立probe。0.16の公式ドキュメントを0.17.0での挙動保証とみなさない。**未解決:** ownerによるformal moment/Wを含むtargetの承認、actual 0.17.0 fit/inference/coverage/弱IV検証。

### 2.3. SR04-R03 Frontdoor：数値推定の段階構造

| 案 | 識別と数値の関係 | 判定 |
|---|---|---|
| **FD-A（推奨）** | Frontdoor criterionを別に確認し、**線形・単一Mediator**の初期正例に限って1段M~1+A、2段Y~1+M+A、全媒介効果を2係数積で評価 | DGP-005でATE=3の独立Oracleが存在。DoWhy 0.14の`mediation_second_stage_confounders`の実際の中身/fit/inferenceと一致をprobe |
| FD-B | 任意非線形frontdoor functionalの一般的数値積分まで初期提供 | FD-Aより適用範囲は広いが、非パラメトリック条件付きdensity、integration、SEの実装と独立Benchmarkが増える |
| FD-C | Frontdoor識別のみを初期提供 | D02の**数値推定をPhase1必須としたOwner判断に反する** |

**レビュー提案:** FD-Aを初期Method仕様候補に固定するためのowner審議へ。Nonlinear caseは識別可能/数値model misspecの負例として残す。**未解決:** DoWhy実効二段階調整集合・標本パリティ・Bootstrap/Delta SEとcoverage。

### 2.4. SR04-R04 FCI/LPCMCI/PCMCI+のGraph Oracle

| 案 | 検証粒度 | 評価 |
|---|---|---|
| **GRAPH-A（推奨）** | truth DAG、latent projection MAG、Markov equivalence PAG/CPDAG、temporal lagを別Oracleとする。independent m-separation列挙で強制端点を求め、TigramiteのOracleCIは補助比較 | 科学的に保守的。DGP-011の2変数潜在交絡を、FCIが必ずbidirectedと断定する正例にしない |
| GRAPH-B | 生成DAGに含まれる全矢印と、FCI/LPCMCI/PCMCI+出力を厳密完全一致させる | 同値類上決定不能な向きまで誤って偽FAILにする。不採用推奨 |
| GRAPH-C | 偽りのOracleを避けるためGraph Accuracyを全廃する | Required Graph discoveryの科学Benchmark不在となり不採用推奨 |

**レビュー提案:** GRAPH-A。DGP-011は潜在交絡Stressとして保持し、FCIのGraph方向正例には**理論的に強制端点が存在する多変数小Graph fixture**を別途導入（新DGP IDではなくDGP-021 variantも候補）。Tigramiteの`OracleCI`がGraphからCI真値を返せても、同一BackendのDiscoveryを正解とする循環検証とは分離。独立PAG/CPDAG導出が完成するまではG04および当該MethodのScience PASSをBLOCK。

### 2.5. SR04-R05〜R11 準実験Method・Inferenceの最小決定案

| Method | Scientific baseline候補 | Required reference/negative/Inference決定 | 現時点 |
|---|---|---|---|
| DiD（P3-M04） | 2x2 group-time ATT、事前指定された比較群を用いた標本差分 | DGP-012真値ATT=2、parallel trends・no anticipation、cluster SEか独立単位bootstrap。staggeredへの単純TWFE無審査一般化禁止 | 方法・SE未freeze |
| Event Study（P3-M05） | Cohort-time ATT(g,t)を先に求め、事前指定weightでevent-timeにaggregate | DGP-013のcohort support/weight/ref period、異質な効果とstaggeredでTWFE汚染を負例に | weights/estimator未freeze |
| ITS（P3-M06） | 季節・trend＋水準step＋傾きchangeのsegmented regression | DGP-014 level=2・slope=.1、AR(1)残差、HAC/GLSと因果解釈上のconcurrent shockを別検証 | estimator/SE未freeze |
| Sharp RDD（P3-M07） | Cutoff近傍のlocal-linear jump。bandwidth・kernel・RBCなどの選択肢を明示 | DGP-015 local jump=3、密度/score操作診断、robust-bias-corrected CIと通常CIを区別 | bandwidth/CI未freeze |
| Fuzzy RDD（P3-M08） | Cutoffの処置jump比による局所complier効果 | DGP-016 jump_A=.5、jump_Y=1.5、local LATE=3。B0全域WaldのARを無審査再利用しない | local IV inference未freeze |
| Synthetic Control（P3-M12） | 非負・和1・事前期間fitのdonor convex weights | DGP-017 noiseless w=(.6,.4)、post effect=2。donor rank・一意性・placebo/permutationと通常CIの区別 | optimizer/inference未freeze |
| Synthetic DiD（P3-M13） | 介入前dataによるunit/time weights、処置後差をSDIDで補正 | DGP-018 panel ATT=2、unit/time weightそれぞれの独立Reference、cluster構造とInference | optimizer/SE未freeze |

この表は採用Methodを7件に縮小するのではなく、7件それぞれの必要な技術判断を明示する。**推奨候補は正式採用ではない**。推論方式を実装の都合だけで一律bootstrapに揃えない。

## 3. Quantitative/Environment/Gate横断レビュー

### 3.1. 定量AC（D）の科学的制約

- **元の11ルールの割当漏れ**はF §6.1で解消。AC-P02/P04はAC-P01の条件、AC-I04はreport-only、AC-D04/05/06はCross、AC-I05/06はMethod-specific、AC-T04/05はNegative/非適用条件である。独立なすべての`Hard Gate comparison`へ二重加算しない。
- **数値候補の出典を誤表現しない:** 0.93 coverage lower、0.07 Type-I upper、1% failure、0.05 s0 bias、0.90 RMSE ratio、0.80 Graph precision/recall等は科学論文がAriadneに指定した数値ではない。各Method/DGP/n/Inferential settingに対する工学・統計設計判断である。
- **R=6,000の意味:** p=.95でMCSE≈0.002814。BonferroniのKをfreezeした上で、Wilson上下限でPASS/FAIL/INCONCLUSIVE。多数比較の補正を入れてもCI自体が科学的に妥当である保証ではない。
- **Graph難度:** adjacencyとendpointを分離し、Oracleが強制する端点のみを方向正解候補とする。DGP-011のFCI latent-bidirected偽正例は除去済み。
- **推論が存在しないMethodにCIを要求しない:** DRIV/Forest/MetaLearnerや準実験はMethod-specific inferential proofが無ければ確認的Science PASS不可。探索的適格point-onlyと同一視しない。

**保留理由:** n/T/cluster/donor/DGP noise・正規化、実効Method/inference、R/K/seedとCompute budgetが未確定。**定量ACの最終freezeはBLOCKED。**

### 3.2. 実行環境（E）のレビュー

- Python 3.12／Linux、DoWhy/EconML/Tigramite機能別optionalはOwnerの既採用大枠。Ubuntu24.04/x86_64/具体Python patch、`dowhy==0.14`／`econml==0.17.0`／`tigramite==5.2.10.1`はSR02 probeの**観測版**であって正式pin承認ではない。
- 5 Profile：BASE、DoWhy、EconML、Tigramite、Combined。現行`pyproject.toml`にE11 extras未定義、現行`uv.lock`にE11のfull resolution未固定。Install/API smokeはScience benchmarkではない。
- RNG: campaign/dgp/replicate/roleごとのstable deterministic seed derivation、DGP Method間共通・Bootstrap/fit別stream、worker数やshard変更でsource sample不変。NumPy/SciPy/BLAS/thread/CPU・Environment hashと実効versionを記録。
- Quality: T0 contract、T1 API smoke、T2 pilot、T3 pre-registered science、T4旧Product/v2回帰を別扱い。Resource予算未計測ならT3 Scienceを実行可能とみなさない。
- 個票privacyとTigramiteの**顧客への個別SI納入GPLv3適合**は独立のOwner/Legal Gate。optional dependencyだから法的配布審査不要との推論は禁止。

**評価:** 環境契約の粒度は実行再現性の設計案として妥当。ただし実効extras・lock・run-level manifest/seed hierarchy/scale budgetの実装は**未完**。

### 3.3. F Traceability：埋まっていることと、いないこと

- 41 Methodは各1以上のPositive DGP・NEG・Reference・AC・Environment・Requirement Draft・Issue・PLAN Gateへ接続。28 NEG逆引き、24 DGP参照、SR04:X9、68 ScopeのR/Q/N/D境界とDeferredが残る。
- 横断Reference `REF-X01`と11横断ACをFへ追補し、**形式上の未接続**を修正。科学的実装・AC threshold承認・Independent Evidenceが未発行であることは変更しない。
- 03のE11-REQ仮IDは正式FR/NFR/ARではない。05の暫定G01〜G10は正式科学的Gate07と同一とは確定していない。SCOPE:X と SR04:Xの衝突も明示済み。
- 単にTraceability cellを表形式で作ったことは、必須Methodに科学的正例が揃ったこと、Source snapshotをfreezeしたこと、未知の仮定違反を機械的に検出することの証明にはならない。

**評価:** Fの文書レベルのID接続は概ね充足。ただし最終FR/Issue/正式Gate/evidence IDとIssue別Work PackageのDispositionはまだ承認されていない。

## 4. 残余Blockerを閉鎖するための決定票（Ownerに委ねる事項）

| ID | 親論点 | 推奨する選択 | 明確に必要な承認/科学証拠 | 現在状態 |
|---|---|---|---|---|
| DEC-SR04-01 | B1 formal Estimand | B1-A 構造係数β、異質効果には自動拡張しない | Human ownerがB1-A構造係数targetと境界を採用。正式schema enum、独立IV/AR・HCとCoverageは未検証 | **OWNER_ACCEPTED / SCIENCE_PENDING** |
| DEC-SR04-02 | DRIV IV heterogeneous target | DRIV-A conditional structural IV slope | Human ownerがDRIV-A条件付き構造斜率とX/W残差化IV momentを採用。実効0.17.0/projection/nuisance/CI/coverage未検証 | **OWNER_ACCEPTED / SCIENCE_PENDING** |
| DEC-SR04-03 | Frontdoor数値 | FD-A 線形singleton mediator＋2-stage積 | Human ownerがFD-A（線形・単一Mediatorの2-stage係数積）を採用。DoWhy 0.14実効stage、CI/独立sample Reference/coverageは未検証 | **FD-A OWNER_ACCEPTED / STAGE_AND_CI_SCIENCE_PENDING** |
| DEC-SR04-04 | FCI/temporal Graph | GRAPH-A 独立PAG/CPDAG/lag oracle | Human ownerがGRAPH-A（DAG/MAG/CPDAG/PAG/temporal別Oracle）を採用。FCI/LPCMCI/PCMCI+の独立同値類とGraph精度は未検証 | **GRAPH-A OWNER_ACCEPTED / INDEPENDENT_ORACLE_PENDING** |
| DEC-SR04-05 | 準実験7手法の初期Estimator／条件付きInference契約 | 7手法の初期Method baseline・個別Inference方針の採用は完了。SCM=point-only、RDD=RBC、SDID=2種重みとcluster bootstrapなど。実効Backend/CI科学受入は未検証 | [DEC-05独立技術記録](20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)＋02 Owner第22項、7 MethodへのTrace更新 | **OWNER_BASELINE_ACCEPTED / INFERENCE_SCIENCE_PENDING** |
| DEC-SR04-06 | P1-M18/19 Observed Negative Control／P1-M20 OLS partial R²＋point RV | **DEC06-Aの全5項目を採用**：P1-M18 NCE、M19 NCO、M20古典OLS partial R²／point RV。opt-in/typed非適用必須、X-04/X-05広範方式は初期非採用D。Null size/power・RV独立Oracle・科学Benchmark未完 | [DEC06 Owner採用済み技術記録](20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)・02第23項・00_04のP1-15/17・X-04/05・A〜F改訂 | **OWNER_METHOD_SCOPE_ACCEPTED / SCIENCE_PENDING** |
| DEC-SR04-07 | Quant AC / MC / Compute | Dを事前登録方式で凍結。普遍的閾値としない | Method/DGP別n/R/K/seed/CI/BLAS、pilot costと独立レビュー | **RESOURCE+METHOD_PENDING** |
| DEC-SR04-08 | Environmental/License | Eの5 Profile、機能別extras、顧客別GPL Legal Review | full lock/effective version/legacy regression、納入Artifact別法務判断 | **IMPLEMENTATION+LEGAL_PENDING** |
| DEC-SR04-09 | Scope/Requirement/Architecture/Gate | 68 Scope全行とA0例外・GAPのOwner決裁 | 正本FR/NFR/AR/ADR、G01〜10→正式Gate07責務、批准SHA | **FULL_CONCEPT_PENDING** |
| DEC-SR04-10 | Science Evidence | 独立Reference/Monte Carlo/Graph・負例・旧v2回帰を実行後、独立review | F §8のEvidence Bundle＋受入結果・否定結果・独立Gate判断 | **SCIENCE_NOT_RUN** |

### 4.1. 順序制約と閉鎖条件

```text
既存採用済み SR03 D01〜D06（個別方針のみ）
    ├─> DEC-01 B1、DEC-02 DRIV
    ├─> DEC-03 Frontdoor、DEC-04 Graph Oracle
    └─> DEC-05 Quasi Method/Inference
                │
                v
   DEC-06 Method/Scope採否 + DEC-09 正式FR/ADR/Gateの権限確定
                │
                v
   DEC-07 Quant+R/K/予算  + DEC-08 Env/lock/license
                │
                v
   承認されたCoding/Reference implementation（今回は実行しない）
                │
                v
   DEC-10 独立Science Benchmark / Gate07 Approval
```

**CLOSEDと認める条件:** formal Method/EstimandのOwner決裁、独立Referenceの実装と独立レビュー、Method-specific Quant ACの事前freeze、必要なRuntime/合法性確認、正本/Issue/Gate/evidenceと承認Snapshot SHAが一貫していること。どれかが欠ければ当該BlockerはOPEN。

## 5. 実施結果・最終判定・次の判断

| 審査レベル | 判定 | 理由 |
|---|---|---|
| A〜Fの文書間整合、Markdown/ID修正 | **PASS — documentation consistency only** | scope/Method/NEG/REF/ACなどの構造誤りを是正 |
| 母集団真値・ATT-AIPW・B1・DRIV・ARの基本導出 | **MATHEMATICAL_CANDIDATE / spot-checked** | 数式は具体化し解析的sanity checkした。正式Method targetとInferenceは別 |
| FCI latent confounding/Graphの正しいAcceptance boundary | **FALSE_CRITERION_REMOVED** | 2変数の潜在交絡有無を一意認識するような非実現可能な受入を排除 |
| Frontdoor/DRIV/B1/Quasiの実効Backendと科学的CI | **BLOCKED** | specific Method/Inferential settingとReference code未freeze |
| 45 ACの定量数値と6,000 Monte Carlo | **NOT_ACCEPTED / NOT_RUN** | 事前設定・R/K/予算、Method別科学的妥当性未完了 |
| SR-02 full lock/seed/Manifest/Delivery legality | **BLOCKED** | install/API smokeのみ、顧客別GPL審査未実施 |
| SR-01〜12、68 Scope、正式FR/ADR/06/07 | **CHANGES_REQUIRED** | Human OwnerとArchitecture Reviewの承認が必要 |
| ENH-E11全体およびGate07 | **NOT APPROVED** | このDraftの是正だけではCoding/Science PASS不可 |

**次のOwner判断:** DEC-SR04-01〜06は**2026-11-16に個別採用済み**。次は**DEC-SR04-07（定量Acceptance Criteria・Monte Carlo計画・計算予算のfreeze案）**。続いてDEC-08（Environment/Legal）・DEC-09（全体Scope/FR/ADR/Gate）・DEC-10（実装後の独立科学Evidence）。本判断はCoding・Science PASSではない。

**変更した範囲:** A/B/C/D/Fのworking_notes本文と本レビュー記録。Eはレビューしたが実効環境や正本に変更なし。コード・`pyproject.toml`・`uv.lock`・GitHub Issue/Notion・02のOwner決定記録・正式FR/NFR/AR/Gateは変更していない。

## 6. 一次／公式参照（直接性と限界）

1. [DoWhy v0.14 TwoStageRegressionEstimator source](https://www.pywhy.org/dowhy/v0.14/_modules/dowhy/causal_estimators/two_stage_regression_estimator.html) — linear modelとsingleton Frontdoor、`mediation_first_stage_confounders`／`mediation_second_stage_confounders`を参照して各stageを構成。これだけではAriadne実行時の各confounder listを確定しない。
2. [EconML DRIV official API documentation](https://www.pywhy.org/EconML/_autosummary/econml.iv.dr.DRIV.html) — `model_final`、`fit_cate_intercept`、`projection`、`opt_reweighted`、`fit_cov_directly`、conditional-IV regression。掲載された公開ドキュメント版と実際に使用する0.17.0 buildの動作検証を区別。
3. [Tigramite documentation](https://jakobrunge.github.io/tigramite/) — PCMCI+の同時点関係はMarkov等価類、LPCMCIはlatentを扱う、`OracleCI`はCI真値の検査用。生成DAGの全端点を復元できるという証拠ではない。
4. [Morris, White & Crowther (2019): ADEMP simulation design](https://doi.org/10.1002/sim.8086) — Simulationの方法論、MCSE・欠損/失敗の分母と事前登録。**本Projectの数値閾値そのものの外部根拠ではない**。
5. [Imbens & Angrist (1994): LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)、[Callaway & Sant'Anna (2021) staggered DiD](https://doi.org/10.1016/j.jeconom.2020.12.001) — 対象と識別条件の区別。
