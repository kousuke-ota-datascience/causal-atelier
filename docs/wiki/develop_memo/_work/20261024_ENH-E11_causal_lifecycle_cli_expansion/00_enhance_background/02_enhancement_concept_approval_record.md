# ENH-E11 — 構想承認記録

**文書区分:** 計画・意思決定記録  
**承認状態:** **正式な構想承認は未実施**（`PENDING_FULL_CONCEPT_APPROVAL`）  
**承認日時:** 未発行  
**承認権限:** Human owner  
**審査対象:** `01_enhancement_concept_and_requirement_revision_plan.md`  
**事前調査・スコープ案・技術審査:** `00_01_foundation_gap_reconciliation.md` → `00_02_foundation_gap_closure_assessment.md` → `00_03_phase1_to_phase3_reconciliation.md` → `00_04_phase1_to_phase3_cli_scope_proposal.md`  
**途中レビュー（非正規の作業メモ）:** [20261029_cli_scope_review.md](../working_notes/20261029_cli_scope_review.md)（**CHANGES_REQUIRED**）  
**追跡:** [GitHub Issue #13](https://github.com/kousuke-ota-datascience/causal-atelier/issues/13)

## 1. 計画の前提として確認されたオーナー方針（Gate承認ではない）

1. ENH-E11では2026年8月4日のPhase 1〜3の必須因果推論Capabilityを実装対象候補とし、既存実装は再利用する。
2. **新機能**の提供範囲はScientific Core、ローカルCLI、永続ローカルファイル成果物に限定する。Web UI/API、Worker、DB統合は後続へ送る。
3. まず9月末のFoundation Gap案と現行実装を照合し、その結果を踏まえて8月構想との差分・正式要件を整理する。
4. Workflowの必須文書に加えてGitHub Issueを使い、Issue→Requirement→Gate→Acceptance Criterionの対応を示す。
5. **Negative Controlの機能原則（2026-11-01の明示方針）:** 「適切なNegative Controlを指定できる研究に対し、科学的に解釈可能な反証分析を提供する」。全分析にNegative Controlの実行を義務付けない。方法実装案は[作業メモ](../working_notes/20261101_negative_control_implementation_plan.md)に記録し、**Method・正本FR/AC・Gateの正式承認と区別する**。

6. **SR-02外部Backendのオーナー方針（2026-11-01）:** **A採用＝Python 3.12／Linux基準**、**B採用＝DoWhy・EconML・Tigramiteを機能別optional依存**、**C採用＝Phase1〜3の列挙Methodを維持し、実装不能な場合は根拠付きで再審議**、**E採用＝実証された採用versionをlock＋科学Benchmarkで固定**。
7. **D採用＝個別SIで顧客環境へ構築・納入、現時点でSaaSは想定しない。** Tigramiteを使用する場合、実際の納入物と結合・提供形態に即してGPLv3適合性を**顧客納入前に審査する方針**を採用。PCMCI／PCMCI+／LPCMCIの利用場面は[SR-02技術メモ](../working_notes/20261101_external_backend_policy_temporal_scenarios.md)で精査。**D方針の採用は個別納入の法的適合性を認定するものではない**。

8. **SR03-D02 Frontdoor（2026-11-01の明示判断）:** **Phase1では識別だけでなく数値推定Capabilityも含める**。識別だけを完了条件としない。ただし推定器の線形性等の追加仮定、数値的実行可能性、CI、科学Benchmarkは未承認・未検証。LATE初期推定器については次項の個別判断で**A＋Bを採用**。[選択肢・科学的制約](../working_notes/20261101_sr03_late_estimator_options_econml_inference_review.md)を参照。

9. **SR03-D03 LATE（2026-11-01の明示判断）:** **Phase3初期提供はA＝二値Z・二値AのWald比を基準、B＝2SLSにも対応する構成を採用**。**C＝条件付きIV向けDR／効率的LATEは追加審議**であり今回の採用範囲ではない。LATEの対象は独立性・除外制約・関連性・単調性等を仮定した**complier**であり、一般ATEや連続TのIV heterogeneous effectと混同しない。2SLSの共変量・複数IV拡張はEstimandと仮定の適合を別審査（**2026-11-05のD03-1 S2採用については下記11項参照**）。**2026-11-05のD03-2 I2個別採用によりAR反転を弱IV推論の初期基準方式とする**。具体的実装／G2正式schema／閾値／科学Gateは未承認（G2の集合意味は下記13項で採用済み）（[科学契約・検討メモ](../working_notes/20261101_sr03_identification_estimand_estimator_contract_review.md)）。

10. **SR03-D01 IV異質効果（2026-11-01の明示判断）:** **A案＝`IV_HETEROGENEOUS_EFFECT`を独立Estimand familyとする方針を採用**。これはD01の個別判断であり、Method別識別対象・schema・BenchmarkおよびENH-E11全体承認を含まない。**本書はオーナー判断の記録を管理し、選択肢比較・科学的根拠・非採用理由・詳細な検証条件は[ファイルD01](../working_notes/20261101_sr03_iv_heterogeneous_estimand_decision.md)に一元化する。**

11. **SR03-D03-1／S2（2026-11-05の明示判断）:** **2SLSのPhase3初期保証範囲としてS2＝B0＋B1を採用**。B0は二値Z/A・切片・単一excluded IV・共変量なしのjust-identifiedモデル（Wald比と点推定一致）。B1は二値Z/A・事前指定の処置前共変量C・切片・単一内生処置／単一excluded IVの加法線形構造モデル。B1はモデル固有の線形IV構造係数であり、一般のATE・LATE・CLATEへ自動変換しない。複数IV、連続処置、複数内生変数等は初期保証の対象外。**本書は個別判断を記録し、比較・識別仮定・数値検証条件は[残余D03審議ファイル](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)に一元化する。D03-2のI2は下記12項で採用済み。D03-3 G2改訂の集合意味は下記13項で採用済み。D03-4 C1の後続管理方針は下記14項で採用済み。正式要件・設計・Gate・実装は未承認。**

12. **SR03-D03-2／I2（2026-11-05の明示判断）:** **S2のB0/B1に対し、Anderson–Rubin（AR）検定反転を初期基準の弱IV頑健な信頼集合推論方式として採用**。単一excluded IV・単一内生処置・独立観測・異分散頑健漸近推論に限定し、First-stage効果・SE・supportと適切なIV共分散を記録する。通常Wald CIを弱IV頑健と表示しない。ARはInstrumentの妥当性を証明しない。Cluster/HAC等は初期保証外。**技術根拠・比較・検証条件は[残余D03審議](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)に責務を移譲**。G2改訂の集合意味は下記13項で採用済み。C1の後続管理方針は下記14項で採用済み。G2正式schema、AR実装、科学Benchmark/Gateおよび全体構想は未承認。

13. **SR03-D03-3／G2改訂（2026-11-06の明示判断）:** **AR反転の信頼集合を有限単一区間に限定せず、型付き区間成分の和集合として損失なく保持する意味契約を採用**。有界・非有界・非連結・全実数を表現し、点推定・推論可用性・科学的適格性を分離する。汎用型には将来の`EMPTY`を表現する余地を残すが、初期just-identified B0/B1では`AVAILABLE/EMPTY`を**正常AR結果として許可しない**。JSON数値にInfinity/NaNを使わず、nullable端点と無界flagを区別する。**本書は採用事実を管理し、科学的根拠・比較・負例・検証条件は[残余D03審議](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)に一元化**。正式schema/enum・D04 migration・AR実装・coverage・Gate・全体構想は未承認。

14. **SR03-D03-4／C1（2026-11-15の明示判断）:** **Phase3初期はA（Wald比）＋B0＋B1（2SLS）のまま、条件付きIV向けDR／効率的LATE推定器Cを追加しない。** Cは**条件付きIVと処置効果の異質性が重要で、B1では必要なEstimandを扱えない具体的ユースケースが判明した場合**に後続の科学的方法審議を起動する。責任主体として**Scientific Methods owner／スコープ承認者の明示義務**を採用し、後続審議の成果物に**識別対象・仮定・推定方式・推論方法・科学Benchmarkおよび根拠付き採否判断**を要求する。**これはCのMethod採用・実装承認ではない。** 担当者の実名／固有識別子、C専用Issue／期限は未指定・未作成。**本書はオーナー判断を管理し、Triggerの科学的意味・比較・詳細要件は[残余D03判断](../working_notes/20261101_sr03_d03_remaining_2sls_weak_iv_review.md)へ責務を委譲**する。正式なFR/NFR/AR、Science/Gate、ENH-E11全体構想の承認は未完了。

15. **SR03-D04-1〜5（2026-11-15、Human owner明示判断）:** 「5案をそのまま採用する」の指示により、**D04-1＝V2（既存`causal-analysis-spec/2`・Product/v2 CLI/Resultを保護し、新E11新規Methodは別の版付きlocal契約に分岐）、D04-2＝E2（Ariadne normalized IdentificationResult→Method別EstimatorSpecによるfail-closed識別・Estimand・適格性審査）、D04-3＝M2（旧v2 Manifestの新Methodへの暗黙昇格を禁止、version dispatchとQuestion/Design/Graph/Dataset／upstream hash一致を保証）、D04-4＝G2-Bridge（採用済みG2の型付き信頼集合をEffectResultの独立推論軸で損失なく扱い、B0/B1正常ARのEMPTYを禁止）、D04-5＝R2（旧Product/v2のREQUIRES_REVIEW＋override契約を回帰保護し、新E11数値経路の未識別・要レビュー自動通過を禁止）を一括採用**する。技術的意味・代替案・Method境界・fixture・非採用理由は[独立D04審議記録](../working_notes/20261115_sr03_d04_identification_estimator_contract_options.md)に一元化。**個別方針の採用のみであり、正式な新schema/enum/version番号、migration実装、Science/Gate 07、D05のMethod別具体推論・科学受入およびD06、全体構想、ADR、Gate freeze、Codingは未承認／未実施。**D05の方針判断は後続の16項で個別採用済みであり、ここでいう未承認はD05 Method別具体化と全体承認を指す。**

16. **SR03-D05-1〜5（2026-11-15、Human owner明示判断）:** 「D05-1〜D05-5の5項目すべてB案を採用する」との指示により、**D05-1=B（非IVのCATE 7手法とDRIVのIV異質効果をMethod/Estimand別契約に分離）、D05-2=B（Exploratoryでは適格な点推定のみの保存を許容／Confirmatoryでは事前指定し科学的妥当性が検証されたCI等の推論証拠を必須）、D05-3=B（推論方式は各Method・最終モデル・backend構成ごとに選択・検証、全Method一律Bootstrapを採用しない）、D05-4=B（点推定・推論区間のavailability・科学的受入を分離して保存、区間無しはnull＋理由）、D05-5=B（有限CIのAPI取得だけでは認定せず、既知真値・pointwise coverage・Method固有の負例/適格性を独立検証）をすべて個別採用**する。点ごとの区間を全x同時信頼帯と混同せず、Method別の推論適格性を確認する。**科学的意味、A/B/C比較、非採用理由、推論の適用限界、候補fixtureは[独立D05技術記録](../working_notes/20261115_sr03_d05_cate_driv_inference_scientific_contract_decision.md)に一元化**する。これはPhase2の8手法を4手法等へ黙って削減する判断でも、DRIVをcomplier LATEと認定する判断でもない。**個別方針採用のみ**。各Methodの具体的推論アルゴリズム・正式schema/enum/version・CI被覆/定量閾値・Bootstrap反復・DRIVの識別対象、SR-04/Gate07、全体構想・Architecture Review・Codingは未承認または未検証。

17. **SR03-D06-1〜6（2026-11-15、Human owner明示判断）:** 「推奨案を採用する」との明示判断により、**D06-1=B（Graph未確定でも検証済みの別識別証明があれば将来推定候補を認める。ただし未識別Resultを直接通さない）、D06-2=B（Estimand・Graph・仮定・Methodに紐づく検証可能な識別証明を要求。研究者宣言やBackend successだけでは不十分）、D06-3=B（研究者のGraph再固定は新GraphVersion・編集根拠・親子lineageを保持し再識別）、D06-4=B（科学的に定義された部分識別集合を点推定や信頼集合とは別の将来Resultとして扱う）、D06-5=B（Human overrideは緩和可能なwarningのみ。未識別・要レビュー・部分識別を点推定へ強制昇格しない）、D06-6=A（初期追加実装をGraphの忠実保持・レビュー・研究者再固定・新Graphからの再識別に限定し、CPDAG/PAG自動一般化識別・汎用部分識別推定器は初期非採用）を個別採用**する。**D06-1/2の例外方針は後続のMethod別検証・採用の余地であり、D06-6=Aにより初期実装に一般化識別証明器を追加するものではない。** 具体的な代替案比較・科学的境界・負例・14件の検証候補は[独立D06技術記録](../working_notes/20261115_sr03_d06_graph_uncertainty_identification_override_decision.md)で管理する。D04の新E11 fail-closed gateと旧Product/v2互換を維持。**個別設計方針だけの採用**であり、Graph再固定の正式schema、別証明受入アルゴリズム、部分識別境界Method/Result、RBAC/override enum、科学Benchmark、FR/NFR/AR、Architecture Review、Gate 06/07、全体構想とCodingは未承認・未実施。

18. **DEC-SR04-01／B1-A（2026-11-16、Human ownerからの正式判断実行指示）:** **B1のMethod固有Estimandとして「加法線形IV構造係数β」（B1-A）を個別採用**する。単一二値excluded Z／内生A、事前指定の処置前共変量C、切片付き加法線形Outcome equation、均質構造係数β、IV外生性・除外・rank等の条件に限定する。科学的なsemantic identifier候補`LINEAR_IV_STRUCTURAL_COEFFICIENT`を採用し、一般ATE/ATT/LATE/CLATEへの自動変換を禁止する。異質効果下の残差化IV比（B1-B）は数学的Reference/negative stressに限って保持し、当初の正式B1 Estimandとしては非採用。条件付き効率的LATE拡張B1-CはSR03-D03 C1方針に従い初期非採用。**これはB1の科学的対象・適格性のOwner判断であり、正式schema enum名/版、2SLS/AR実装、HC設定・被覆、SR04-D AC、Gateや全体構想の承認ではない。** 具体的な比較・独立数式・反証・Evidenceは[DEC01/02独立判断記録](../working_notes/20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md)を参照。

19. **DEC-SR04-02／DRIV-A（2026-11-16、Human ownerからの正式判断実行指示）:** **DRIVのMethod固有Estimandとして条件付き構造IV処置斜率`θ_IV(x)`（DRIV-A）を個別採用**する。既採用family`IV_HETEROGENEOUS_EFFECT`内のsemantic target `CONDITIONAL_IV_STRUCTURAL_SLOPE`として、構造式`Y=θ_IV(X)T+h(X,W)+U`、処置前Wでの残差化を用いた条件付きIV moment、relevance/除外/外生性/構造線形性、処置dose contrastとX支持域を要求する。W無しのDGP-008ではθ(-1)=1.5、θ(+1)=2.5。W有りの適格性は別々に実証する。**推定器の重み付き射影を正式な構造EstimandとするDRIV-B、binary complier LATEへの一律再分類DRIV-Cは非採用。** 現行EconMLの特定`model_final`/`projection`/`opt_reweighted`/`fit_cate_intercept`/`cov_clip`と実効0.17.0 API、Method固有CI、Coverage、科学Benchmarkは**未選定・未検証**。正式schema enum、FR/ADR、Gate、全体構想・Codingは引き続き未承認。[DEC01/02独立判断記録](../working_notes/20261116_sr04_dec01_b1_dec02_driv_owner_decisions.md)に比較・追加仮定・負例を一元化。

20. **DEC-SR04-03／FD-A（2026-11-16、Human owner明示採用判断）:** **Phase1のFrontdoor数値推定について、FD-A＝線形・単一Mediator・二段階推定の係数積を初期Method保証範囲として個別採用**する。Frontdoorの識別条件を数値推定の追加仮定から分離し、適格な線形Stage1 `M∼1+A` とStage2 `Y∼1+M+A` の係数積を限定正例とする。DGP-005の既知真値ATE=3で識別式と数値Referenceを検証する。一般非線形g-functionalを初期必須とするFD-Bは非採用、識別のみのFD-Cは既採用SR03-D02に反するため非採用。**DoWhy 0.14で実際にAが第2段階の調整変数として入るか、stage別数値パリティ、独立Inference/CI coverage、正式Method Config・FR/NFR/AR・Gateは未検証・未承認**。Frontdoor識別条件の成立だけで線形two-stageが必ず正しいとしない。科学的比較・数式・負例・検証条件は[DEC-SR04-03独立技術判断](../working_notes/20261116_sr04_dec03_frontdoor_fd_a_owner_decision.md)に一元化する。

21. **DEC-SR04-04／GRAPH-A（2026-11-16、Human owner明示採用判断）:** **FCI、PCMCI/PCMCI+、LPCMCIの受入Graph Oracleについて、GRAPH-A＝生成DAG、latent projection MAG、Markov equivalence CPDAG/PAG、temporal lag／同時点関係を科学的に区別し、独立に導出する方針を個別採用**する。生成真値DAGの全方向と出力PAG/CPDAGの完全一致を要求するGRAPH-Bは非採用、Graph精度検証を廃止するGRAPH-Cも非採用。DGP-011の同時点2観測変数に対しFCIがlatent confounderを一意識別・bidirected方向へ確定できるという誤基準は禁止。m-separation／独立Graph同値類から強制端点を導出し、Tigramite OracleCI等は補助的cross-checkに限る。**Graph忠実保持・科学的Graph accuracy・Causal Effectの識別は別判定**。独立MAG/PAG/CPDAG/temporal Oracle実装、FCI/Tigramite version/CI-test・Endpoint科学Benchmark、正式Gate・FR/NFR/AR・Architecture・Codingは未完了。先行SR03-D06のGraphVersion新規固定・strict識別・初期一般化識別エンジン非採用の方針は変更しない。詳細比較・科学的境界・Fixture・Acceptanceは[DEC-SR04-04独立技術判断](../working_notes/20261116_sr04_dec04_graph_oracle_graph_a_owner_decision.md)に一元化する。

22. **DEC-SR04-05-1〜7（2026-11-16、Human ownerによる「準実験7手法のEstimator／Inference契約を実行する」指示）:** **準実験7手法のMethod別初期科学契約を個別採用**する。**(1) DiD**＝2×2 ATTの群差の差＋独立unitに対するcluster適格推論、staggeredはgroup-timeへ別契約。**(2) Event Study**＝never-treated controlを用いるcohort-time ATT(g,t)を非負の事前指定cohort weightでevent-time集約し、cohort-stratified unit trajectory bootstrapを推論候補にする（naive staggered TWFE leads/lagsを保証対象としない）。**(3) ITS**＝time trend/seasonality/介入level・slopeのsegmented regression、HAC型推論を初期候補。**(4) Sharp RD**＝cutoff左右のlocal-linear・triangular kernel・bandwidth明示＋robust bias-corrected（RBC）CI候補。**(5) Fuzzy RD**＝cutoffのoutcome/treatment jump比の局所complier効果＋分子分母の依存を考慮したRBC推論候補、弱い局所first stageではfail-closed。**(6) Synthetic Control**＝preperiodのsimplex-constrained donor weightsとtreated unitのpost gap、**初期は探索的点推定のみ**、placebo rank/RMSPEを普遍的95%CI扱いしない。**(7) Synthetic DiD**＝control unit重みとpre time重みを別最適化したweighted DID、十分な独立treated/control unitsを前提に毎replicateで両weightsも再推定するunit-cluster bootstrapを推論候補とする。**各Methodの推論は必要なDesign/cluster/CIの科学的成立を条件とする**。これらは**方法論的ベースラインと条件付きInference方針の個別採用**であり、rdrobust等の実効依存追加/版・Config・license、Method別SE/bandwidth/optimizer/bootstrap設定、独立DGP Reference、推論Coverage、Quant AC、正式schema/FR/ADR/Gate・Coding・全体構想を承認するものではない。代替案・数式・既知真値・負例・適用不可条件・科学的検証への引渡しは[DEC-SR04-05独立技術判断記録](../working_notes/20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md)に一元化する。

23. **DEC-SR04-06／DEC06-1〜5全A（2026-11-16、Human owner明示採用判断）:** **DEC06-Aを5項目すべて個別採用**する。**DEC06-1=A:** P1-M18 `NEGATIVE_CONTROL_EXPOSURE`（実在する対照Zと研究Designで事前指定した条件付き関連null）をPhase1初期Nに含める。**DEC06-2=A:** P1-M19 `NEGATIVE_CONTROL_OUTCOME`（実在する対照W、処置AのWへの因果無影響と適格な帰無・共有バイアスの根拠）をPhase1初期Nに含める。**DEC06-3=A:** P1-M20のCinelli–Hazlett `UNOBSERVED_CONFOUNDING_PARTIAL_R2`を**連続Y・古典OLS係数**に限定して初期Nに含め、2軸partial R² grid・OVB感度曲線・**点推定を0に動かすpoint RV（q=1）**を必須とする。既存HC3推論をclassic OLS t/dfの公式へ無断流用しない。**DEC06-4=A:** NCE/NCOは明示opt-in、観測対照/null・DAG/Design/時間とconditioningの適格性を必須とし、無指定・不適格なら型付き非適用/要レビューとする。関連の有意性は未観測交絡の存在を特定せず、非有意も無交絡を証明しない。**DEC06-5=A:** 上位SCOPE:X-04のSimulated Confounder/Graph Perturbation、X-05のIPW/AIPW/CATE等への汎用Sensitivity拡張を**初期非採用D（後続個別判断）**とし、P1-M18〜20の提供だけで上位A0要求を全面完了としない。**採用したのはMethod採否・最小適用範囲・意味論的fail-closed方針であり、正式FR/NFR/AR/Architecture/Schema、Runtime、Null size/power・Inference/CIの科学的適格性、RV数値Oracle・Monte Carlo、Gate06/07とENH-E11全体構想/Codingは未承認・未実施。** 比較・数式・反証・負例と残余依存は[DEC-SR04-06独立技術記録](../working_notes/20261116_sr04_dec06_negative_control_ols_rv_scope_decision_proposal.md)を正とする。

24. **DEC-SR04-07／DEC07-1〜7全A（2026-11-16、Human owner明示採用判断）:** **定量Acceptance／Monte Carlo／Compute Budget設計の7つのA案をすべて個別採用**する。**DEC07-1=A:** Exact／statistical Hard／conditional／report-only／NOT_APPLICABLEをMethod×Fixture別に区別し、契約の100%一致と各科学的数値ACを混同しない。**DEC07-2=A:** Gate-wide family-wise α=0.05、事前登録した全mandatory stochastic比較数KでBonferroni配分し、割合指標に片側Wilson、連続指標にはMethod適格なMC不確実性boundを使用する。**DEC07-3=A:** RはMCSE、実際のK、Hard閾値を通過できる確率を踏まえてMethod×DGP×target別に整数設計する。R=6,000は一律必須・計算上限ではない。**DEC07-4=A:** 本番T3とは独立な100〜200rep程度のT2 Pilotを候補として、n/T・Backend/CI/inner bootstrap別のコア秒・実効メモリ・失敗率を実測する。**DEC07-5=A:** 実効CPU core-hour／Wall／RSS／コストとOwnerの資源・支払上限を照合してから数値Budgetを凍結し、超過時はRESOURCE_BLOCKEDとしてScope/Method/設計を再審議する。**DEC07-6=A:** 安定したseed階層、失敗を含む全分母、R事前固定とno peeking、環境/Reference/Metric証跡を必須化する。**DEC07-7=A:** Owner方針採用と、Method-specific Cell/K/R/Resource/Source SHAのfreeze、独立T3 Science、正式Gate判定を別工程にする。**受入値の初期数値候補（coverage Wilson下限0.93、failure上限0.01、size上限0.07、Bias/RMSE/Graph等）はMethod-specific適用とDGPの正式採用・実効Configが確定するまで包括的に凍結しない。** 本採用は**統計・Resource審査方針の承認**であり、実際のK/R/反復数・CPU秒・金額・Backend／License、全68 Scope・FR/NFR/AR/ADR、Gate06/07、独立Science Benchmark・Codingの承認ではない。比較・数式・数値監査・Blockerは[DEC-SR04-07独立技術判断](../working_notes/20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)に保存する。

## 2. まだ承認されていない事項

- **DEC-SR04-07の数値freezeと科学的実施（2026-11-16、Owner方針は第24項で採用済み）:** [独立技術判断](../working_notes/20261116_sr04_dec07_quant_mc_compute_budget_owner_decision_proposal.md)によりDEC07-1〜7の設計方針は個別採用した。**残余は実効mandatory cell/K、n/T/R/inner bootstrap、Method別数値閾値・CI/Oracle資格、T2 PilotのCPU秒・RSS・Wall、Owner資源・金額上限の取得、T3 Science・Gate批准である。** 未測定値を「承認済み数値」と扱わない。


- 拡大後の構想名称、必須手法一覧および例外・同等手法。
- 正本§11の外部engine除外の変更、FR/NFR/ARの追加・削除・変更。
- Design/Resultの所有権、**optional依存の具体的version・実効API・CLIファイル契約**、科学的許容基準。 DEC-SR04-06のP1-M18〜20とX-04/X-05 Deferredは個別承認済みだが、正式要件や実効契約の批准は未実施。A/B/C/D/Eの基本方針、DEC-SR04-01/02の**科学的semantic target**、DEC-SR04-03/04の**Frontdoor数値Method・Graph Oracle方針**、DEC-SR04-05-1〜7の**準実験Method別ベースライン推定・条件付き推論方針**は個別採用済み。ただし正式Schema enum/Methodの実効Config、科学的に認定されたInference algorithmとCoverage、数値受入は未承認。
- **DEC-SR04-06の科学的実装・正式Scope引渡し（2026-11-16）：** 5件のOwner採否は**第23項で個別承認済み**。未解消なのは、新E11 Methodの正式schema/enum・backend・Null検定の有効性・CI・RV計算の独立Reference・実効データ契約・受入閾値・68 Scope全体批准であり、これらを採否未決と混同しない。
- **Tigramiteを含む個別SI納入物のGPLv3適合性**（配布前評価方針は採用済み。個別の組合せ・納入主体・対応ソース義務等は未判定）。
- Architecture Review結論、Gate分割、06/07のfreeze、受入用基準SHA。

## 3. 遵守条件

- 新機能のWeb UI/API/Worker/DB統合をENH-E11内で行わない。
- CPDAG/PAG等の不確定性を黙ってDAGへ変換しない。
- 非識別、仮定違反、適格性不足等は科学的statusとして記録し、技術失敗と区別する。
- 既存FR/NFR/ARの意味、現行実装、独立Gate証跡を保護する。
- Issue完了はcanonical 999 PASSを意味しない。

## 4. 明示的な非承認

- 実装Agentの起動、Gate 06/07の固定、受入済みソフトウェアの宣言。
- 審査済みの要件差分がないままの正本書換え。
- Phase 4のPolicy automation、監視、意思決定権限の付与。

## 5. 承認のための残作業

1. 先行調査の`00_01_foundation_gap_reconciliation.md`→`00_02_foundation_gap_closure_assessment.md`→`00_03_phase1_to_phase3_reconciliation.md`を確認し、`00_04_phase1_to_phase3_cli_scope_proposal.md`の68行と[作業メモ](../working_notes/20261029_cli_scope_review.md)の**SR-01〜12を是正・再審査**した結果を確認する。
2. `00_04_phase1_to_phase3_cli_scope_proposal.md`にあるATC/matching等の後続送り、**§2.3の観測NCE/NCO・OLS partial R²候補の採否・適用限界（[方法検討メモ](../working_notes/20261101_negative_control_unobserved_confounding_method_review.md)）**、外部Libraryの同等代替、Product GAP-C01〜04の帰属を**項目単位で明示承認または差戻し**したうえで、`03_requirements_revision.md`、`04_design_revision.md`を固定SHAに照らして再確認する。
3. Architecture Reviewを完了し、`05_requirements_design_consistency_and_traceability_review.md`を改訂する。
4. Human ownerの正式判断を**実際の日時と根拠**付きで追記する。遡及的に承認済みとしない。
5. 承認後に正本と承認Snapshotを固定し、Gate 06/07を作成する。
