# ENH-E11 — DEC-SR04-07：Quantitative Acceptance／Monte Carlo／Compute Budget（Owner正式個別判断）

**日付:** 2026-11-16 JST  
**区分:** SR04独立技術記録。Human ownerが2026-11-16にDEC07-1〜7のA案をすべて明示採用。**正式FR/NFR/AR、Gate06/07、Coding、Science PASSの承認ではない。**  
**現在状態:** DEC-SR04-07_A1_TO_A7_OWNER_ACCEPTED / ACCEPTANCE_POLICY_APPROVED / K_NOT_ENUMERATED / R_NOT_FROZEN / PILOT_NOT_RUN / COST_NOT_MEASURED / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL。  
**先行:** 02 Owner判断のDEC01〜06は個別採用済み。適用Method・Estimandを本判断で変更しない。  
**根拠:** [SR04-D 定量AC](20261115_sr04_quantitative_acceptance_criteria_draft.md)、[SR04-E Environment](20261115_sr04_execution_environment_contract_draft.md)、[SR04-F Trace](20261115_sr04_gate07_traceability_draft.md)、[SR04 A〜F統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md)、[02決定記録](../00_enhance_background/02_enhancement_concept_approval_record.md)。

## 0. 結論・代替案

**Owner採用 DEC07-A:** **共通の数学的AC判定ポリシー、Method別の評価セル、Gate全体に対する多重性、事前登録R、独立Pilotによる実測Compute Budget**を採用する。数値未測定のCPU能力・金額・実効K・対象Cellを推測で補完せず、それらはPre-freezeのBlockerとして保持する。

| 案 | 内容 | 評価 |
|---|---|---|
| **DEC07-A（採用）** | ADEMPベースのセルレジストリを構築、全Hard確率判定数KにFWER 0.05を割当て、Wilson等で誤判定を評価。pilotでruntime/memoryを測りRとcompute上限をOwner承認後freeze | 科学的な受入品質と実行費用を分離。Method別Rを導出できる |
| DEC07-B（非採用） | 全41 Method・全組合せでR=6,000を無条件固定 | セル定義・K・Bootstrap内側ループを無視して費用が爆発。稀な失敗率でPass確率不足 |
| DEC07-C（非採用） | 小さいRに変更し多重性・MCSEや推論資格を省略 | 偽PASS・optional stopping・失敗replicate選別の危険。非推奨 |

**今回の個別採用境界:** 形式的な統計判定の方針を採用した。一方、実効K、Method固有n/T/cluster・CI/Bootstrap数、必要R、実測CPU秒、資源・金額上限は現在確定していない。**決定式を記しただけで実測予算が確定したと宣言しない。**

## 1. DEC07-1：AC分類・数値閾値（A採用）

| AC family | 値／判断方針 | 適格性の境界 |
|---|---|---|
| D01/D02/D04/D05/D07 | **既知Fixtureのtyped status、lineage、Graph endpoint、JSON readback、既存v2回帰は完全一致・誤許可0** | 未構築のPAG Oracleの真値方向まで一致を要求しない |
| D03 | well-conditionedな同一演算のfloat64 Reference一致：絶対差 <= 1e-10 + 1e-8 max(1,abs(ref))（候補） | 目安κ₂<=1e8。near-singular／optimizer／AR重根は専用Numerical AC |
| A01〜A05 | AR集合の4種形状・unbounded・componentは厳密一致、通常simple root端点の候補相対精度1e-6 | ARの真値coverageと集合の表現契約を別検査 |
| I01 | Confirmatory pointwise CI / AR coverage：95%名目、**多重補正済み片側Wilson下限 >= 0.93** | CI Methodの科学的妥当性を事前Review、point-only SCMなどはN/A |
| I02/P05 | 正常Eligible caseの推論・点推定失敗割合：**多重補正済み片側Wilson上限 <= 0.01** | Failureを分母から除外しない。ARの無界集合は失敗でない |
| T01/T02 | 妥当なnullのサイズ：**片側Wilson上限 <= 0.07**。定義済み強い対立のみPower：**片側Wilson下限 >= 0.80候補** | null/対立・Design・nが未確定ならN/A/BLOCKED |
| P01/P03 | Bias上限 **0.05 × 事前固定した母集団尺度s0**、nを4倍にしたRMSE比 **<=0.90** はregular DGP限定の候補 | Outcome尺度・Noise・Rate・nが不適切ならMethod別に審査。弱IV/Graphへ一律適用禁止 |
| G03/G04 | Strong-signal GraphのPrecision/Recall各 **>=0.80**、FPR **<=0.10** は候補。方向は同値類で強制されるendpointのみ | Independent CPDAG/PAG/Temporal oracleがなければGraph ScienceはBLOCKED |
| Q01〜05/R01〜05 | DiD/Event/ITS/RDD/SCM/SDIDとNC/OLS-RV固有の独立Reference・負例・適格な数値検証 | SCM初期Point-only。DRIVと非IV CATEは評価格子別、RVは古典OLS限定 |

数値は**Ariadne向けの工学的な許容案**であり、原著論文がこの値を保証しているわけではない。Method別の適用が未指定の統計閾値を、全Methodの必須Hard Gateにしてはならない。Exact、Hard stochastic、report-only、conditional、N/Aの区分をセルIDごとに登録する。

## 2. DEC07-2：多重性・Wilson／連続指標の判定（A採用）

**Kの正しい定義:** mandatory な **stochastic Hard Gate comparisonの総数**。41 Method＝Kではない。各DGP variant、Estimand、固定x/time、sample size、推論構成、Coverage/Size/Power/Bias/Graph metricが異なれば独立したHard比較として計上し得る。固定sample exact-caseは別の100%契約としKに機械的に混ぜない。すべてのmandatory cellと判定指標を登録し、Kを実数として確定するまではAlpha-adjusted PASS不可。

**統一案:** Gate-wide family-wise alpha=0.05。各Hard stochastic comparisonに Bonferroni alpha_j=0.05/K。依存する比較が混ざっていてもBonferroniのFWER上界は成立する。Kを後から合否に合わせて減らすことは禁止。

R independent DGP replicate中のBernoulli success数kに対して、p_hat=k/R、z_K=Phi_inverse(1-0.05/K)、g=1+z_K^2/Rとする。

- center = (p_hat + z_K^2/(2R))/g
- half = z_K sqrt(p_hat(1-p_hat)/R + z_K^2/(4R^2))/g
- L=center-half、U=center+half

**下側閾値:** L>=p_minでPASS_CANDIDATE、U<p_minでFAIL、その他INCONCLUSIVE。**上側閾値:** U<=p_maxでPASS_CANDIDATE、L>p_maxでFAIL、その他INCONCLUSIVE。小失敗率に通常のWald正規区間を無批判に適用しない。

**連続性能:** Biasの片側上限は abs(bias_hat)+z_K MCSE_biasをregular finite-variance時の候補とし、非正規/Heavy-tailなどでは校正済み別方式を要求。RMSE比はpaired replicateを保持してdelta法／replicate bootstrap。Graph metricsの標本独立単位は各DGP replicateであり、同一Graphの多数edge・複数xを擬似独立試行にしない。

**CoverageとAvailability:** R_total、R_ci、R_coveredを必ず保存。I01は conditional coverage=R_covered/R_ci の側面を評価するが、同時にI02のfailure/availabilityとjoint covered-and-available率を報告し、I02未合格でI01だけPASSさせない。

## 3. DEC07-3：RをMCSEと受入通過確率から逆算（A採用）

R=6,000、名目p=0.95の場合、Monte Carlo SE=sqrt(0.95×0.05/6000)=**0.002813657**（0.2814 percentage points）。MCSE<=0.003だけならR>=5278。この精度だけでWilsonのHard Gate通過が保証されるわけではない。

**独立計算に使った仮定:** Familywise alpha .05、Bonferroni K=256/1024（**説明用であって実Kではない**）、仮定した観測coverage .95、size .05、failure .005。各kはround(R p)、Wilsonの式へ直接代入。

| K | R | z_K | coverage=.95のL | size=.05のU | failure=.005のU |
|---:|---:|---:|---:|---:|---:|
| 256 | 3000 | 3.54634 | .93391 | .06609 | .01207 |
| 256 | 6000 | 3.54634 | .93905 | .06095 | .00942 |
| 1024 | 3000 | 3.89634 | .93210 | .06790 | .01308 |
| 1024 | 6000 | 3.89634 | .93786 | .06214 | **.01000657** |
| 1024 | 8000 | 3.89634 | .93962 | .06038 | .00915 |
| 1024 | 10000 | 3.89634 | .94081 | .05919 | .00860 |

**重要な反例:** K=1024、R=6000で実際の推論失敗数が30なら、観測失敗率は0.5%でも補正Wilson上限は**1.000657%**。1%以下のHard Gateは満たさない。四捨五入で1.00%と表示してPASSさせない。

**通過確率:** 真の失敗率がp_f=.005と仮定した場合の Binomial(R,.005) に対し、Wilson上限<=.01を満たす最大失敗数x_maxと P(X<=x_max) を**事前解析計算**する。

| K | R | x_max | 仮定p_f=.005で受入通過確率 |
|---:|---:|---:|---:|
| 256 | 6000 | 32 | .6849 |
| 256 | 8000 | 48 | .9081 |
| 1024 | 6000 | 29 | **.4755** |
| 1024 | 8000 | 45 | **.8102** |
| 1024 | 10000 | 61 | .9448 |

これらは実装の成功率ではない。**R=8,000でも成功保証ではなく**、真の失敗率が上限に近づくと通過は難しくなる。

**採用するR選定アルゴリズムの案:**
1. Cellごとの推論Method・Estimand・n/T・assumptions・真値と許容目標を**先にfreeze**。
2. R_min_MCSE = ceil(p_design(1-p_design)/epsilon_MCSE^2)。
3. 実際のK、許容閾値、仮定したperformanceと目標Pass確率（候補0.80／0.90）から、Binomial/Wilsonまたは連続量の区間で R_min_acceptance を**整数探索**。
4. R_final は両方とMethod-specific最低条件の最大以上、ただし実効CPU/RAM/支出見積りの上限を満たす場合だけ採用。R=6000は初期検討点であって全セル共通のfreezeではない。
5. 所要RがResource capを超えるなら **RESOURCE_BLOCKED**。閾値緩和や必須DGPの事後除去で合格にしない。Method/Scope/検証階層の再審議へ戻す。

## 4. DEC07-4：Pilotの実施計画（A採用）

| Tier | 候補規模 | 使用目的・受入 |
|---|---|---|
| T0 Fixed algebra/schema | 独立Reference、全41 Methodの接続・必要Fixtureと負例、AR Q1〜Q4 | 数学・型・読戻しの固定一致。SCM/PAG/RVでOracle不在ならBLOCKED |
| T1 API/Runtime Smoke | 依存/Profile別にfit/CI/Version/旧v2回帰 | Science PASSと同一視しない |
| T2 Resource/Variance Pilot | regularはまず約200 reps、重いGraph/Forest/Bootstrapは約100 reps、2種類以上のn/Tやinner B | 各methodのcore-seconds、RSS、failure、推定分散・inner refit countを測定。正式T3とは別のseed/campaign |
| T3 Preregistered Science | K/R/seed/DGP/Reference/CI method/Hard ACとCompute capのすべてを事前freeze | 全mandatory cellの独立replicate、失敗含めて計測。R完遂前にPASS不可 |
| T4 Independent Review | Metric集計、別Referenceとの比較、旧v2回帰、Owner Gate | Science PASSはOwner/Reviewerが証拠SHAに署名後のみ |

既存SR04-Dの n/T候補（OLS n1000/4000、FD n2000/8000、CATE n2000/8000、DRIV x=-1/+1、IV first-stage強弱、Graph T1000/4000、Quasiのcohort/cluster/bandwidth/donorなど）は**Method-specificな候補**。全直積をmandatoryに自動追加しない。CATE x=-0.75/0/+0.75とDRIV x=-1/+1は相互流用禁止。GraphのPAG Oracle、DoWhy FD-A第2段階、EconML DRIV実効推論、B1 AR、Quasiで不適格なMethodは数値Rを増やす前に科学的契約を是正する。

**停止:** 固定Rを完遂してから単一回判定。途中でWilsonを繰り返し覗き、INCONCLUSIVEだからRを足して最後のPASSを採用するoptional stoppingは禁止。Sequential confidence sequenceやalpha-spendingを**別途事前承認**した場合だけ例外。

## 5. DEC07-5：計算量・Compute Budget（A採用）

科学Benchmarkの総CPU費用を、各cellの独立反復数R、DGP生成、fit、推論、inner Bootstrap/RefitのCPU core-secondsを分けて見積もる。

B_core_hour = SUM_over_cells [ R_cell × { t_data + t_fit + t_infer + B_inner × t_refit } / 3600 ] + B_reference + B_io + B_review_compute

**上式のt値は未測定。** 実際のWall時間は並列プロセス数、BLAS/CPUオーバーサブスクリプション、メモリ、I/Oに依存する別量。環境Eの選定Profileが同一の場合のみPilot外挿を許容する。

| 説明用の仮定 | 必要処理 | Core-hourの試算 |
|---|---:|---:|
| 41 Methodで各1必須cell、R=6000 | 246,000独立fits | 1 core-second/fitなら**68.33 core-h** |
| 同条件 | 246,000独立fits | 30 core-seconds/fitなら**2050 core-h** |
| 同条件の各fitに999のinner full refitが必要と仮定 | 245,754,000 inner refits | 1 core-second/refitなら**68,265 core-h（innerだけ）** |

**これらは実測値や推奨実行数ではなく、費用のオーダーを可視化した例**。実際はMethodごとに多数の評価cellが存在し、内側Bootstrapが不要な方法もある。

### 5.1. 予算パラメータと許可条件

事前登録レジャーで次を必須にする。

- B_pilot_core_hours、B_T3_core_hours、max_wall_hours、max_parallel_workers、max_peak_RSS_GiB/job、max_total_RAM_GiB
- 必要なら price_per_core_hour、storage/egress/actions cost、currency、max_spend、cost source/as_of_date
- Method/DGP/CI/inner bootstrapごとの p50/p95 core-seconds、R、B_inner、peak RSS、failure/timeout、Env SHA、BLAS/thread設定
- 各Mandatory cellについて T3 forecast、worst-case reserve、resource cutoff、owner許可参照

**現在は実機構成と価格・Owner上限が与えられておらず、実測Core-hour予算を数値freezeできない。** これを都合のよい数字で埋めた場合の失敗を防ぐため、DEC07では**予算の算定・審査・fail-closedのルール**のみをOwner判断対象とする。T3実行許可は予測総額<=承認Core-hour/Wall/RAM/Cost capかつMethod/Reference/CIが科学的に適格な場合だけ。費用超過なら RESOURCE_BLOCKED とし、後からRだけ減らして同じHard Gateを満たしたと主張しない。

## 6. DEC07-6：RNG・失敗分母・Evidence（A採用）

- **RNG:** ENV-EのSeedSequence/PCG64DXSM候補、campaign/cell/replicate/roleからSHA-256で安定streamを導出。Data-generation seedは同一DGPとreplicateでMethod間共有可、Method-fit/bootstrap RNGは分離。正式採用のBitGenerator/Library版とseed hierarchyはDEC08/Gate後段でfreeze。
- **Pilot隔離:** T2とT3は別のcampaign/root seed。Pilot結果を見てDGP/Method選定を固定する場合は**T3実行前の新登録version**に記載する。
- **分母:** R_planned、R_attempted、R_point_available、R_CI_available、R_covered、timeout、nonfinite、typed reasonを全replicateで保存。失敗を分母から削除しない。CI conditional coverageとI02 failureとjoint rateを同時報告。
- **Status:** 確実な契約違反=FAIL、予測範囲で閾値をまたぐ=INCONCLUSIVE、参照不足や予算超過=BLOCKED。正式Methodの非適用にはN/A＋科学的根拠。PASS_CANDIDATEはOwner Gate前の内部候補。
- **Reproducibility:** Repo/DGP/Reference SHA、uv.lock/effective versions、OS/CPU/BLAS/thread/seed derivation hash、全部のHard比較Kとz_K、DGP真値、Runtimeを保存。過去の判定Snapshotは上書きしない。

## 7. DEC07-7：Gate/Ownersの段階を分離（A採用）

| 段階 | 完了条件 | 現状態 |
|---|---|---|
| METHOD_POLICY_ACCEPTED | DEC01〜06で決めた科学的MethodやEstimandの対象 | 個別Owner判断は完了 |
| DEC07_OWNER_POLICY | DEC07-1〜7のA案をHuman ownerが採用。02第24項へ正式記録 | **OWNER_ACCEPTED** |
| CELL_REGISTRY_FROZEN | mandatory/diag/conditional、DGP × Method × estimand × metrics、Kを列挙しRef/Owner SHAと対応 | **OWNER_ACCEPTED** |
| R_AND_RESOURCE_FROZEN | pilot、正式R/CI/Bootstrap、CPU core-hour・Wall・RAM・Moneyの必要上限をOwner承認 | **OWNER_ACCEPTED** |
| SCIENCE_EXECUTED | 適格なT3独立Reference/MC/負例・旧v2回帰を実行 | **NOT RUN** |
| SCIENCE_GATE_ACCEPTED | 独立Reviewer、実際の証拠SHAとOwner/Gate判定 | **NOT APPROVED** |

## 8. Owner選択票（7項目すべてAを正式採用）

| 判断 | A案（採用） | B／C案の主要問題 | Owner状態 |
|---|---|---|---|
| **DEC07-1** | Exact vs stochastic vs conditional vs N/Aの分類と限定数値AC | 全Methodへの一律CIやBias閾値の強制 | **OWNER_ACCEPTED** |
| **DEC07-2** | FWER 0.05、一つのGate-wide family、K全列挙、Bonferroni／Wilsonと適格な連続bound | 恣意的family分割・多重性を無視 | **OWNER_ACCEPTED** |
| **DEC07-3** | RはMCSE・K・閾値通過確率で逆算。6000は初期検討点、必要時8000/10000以上 | 6000全Method強制、低Rで閾値だけ緩和 | **OWNER_ACCEPTED** |
| **DEC07-4** | 100〜200repのPilotをT3と独立に行いn/T・CI・inner fit別に実測 | Pilot無し予算決定、Pilot標本を正式分母へ混入 | **OWNER_ACCEPTED** |
| **DEC07-5** | Hardware・支払上限を確認しCore-hour/Wall/RAM/Moneyを実測見積りでfreeze。超過はBLOCKED | 架空のCPU単価・Core-hour設定／後から必須Cellを消す | **OWNER_ACCEPTED** |
| **DEC07-6** | 独立seed、失敗分母、固定R、no peeking、完全Manifest | 成功分だけ集計、後出しR追加で好都合PASS | **OWNER_ACCEPTED** |
| **DEC07-7** | 02 Owner方針採用→Cell/K/R/Resource/Ref freeze→独立T3→Science Gate | Owner方針＝Science PASS、FR/ADR/Gate未承認のままCoding | **OWNER_ACCEPTED** |

**正式個別判断:** **DEC07-1〜7の7件すべてAを採用済み**。これは科学的受入設計ポリシーの採用であって、**実効K/R/Compute CostやGate07の数値freezeの採用ではない**。計算予算の数量はT2 Pilot/環境の準備・Owner上限の取得後に別途確定する。

## 9. 外部根拠・限界

1. [Morris, White & Crowther (2019), Using simulation studies to evaluate statistical methods](https://doi.org/10.1002/sim.8086)（[原著公開全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/)）。ADEMPとMonte Carlo SE、独立replicate/報告の方法論。**本書の具体数値は原著の指定ではない**。
2. [NIST Wilson score interval](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)、[NIST Technical Note 2119](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf)。Wilson区間の算式。
3. [SciPy binomtest公式](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html)とそのWilson confidence interval API。採用EnvironmentでのSciPy version/計算parityは別検証。
4. [SR04-D Quant AC Draft](20261115_sr04_quantitative_acceptance_criteria_draft.md)／[SR04-E Env](20261115_sr04_execution_environment_contract_draft.md)／[SR04-F trace](20261115_sr04_gate07_traceability_draft.md)。これらは未凍結Draftである。

**次工程:** DEC07-1〜7のOwner判断は採用済み。02承認記録第24項とSR04 A〜F/F traceへ反映したうえでDEC08（Environment/Extras/License）を審議。実効計算予算のfreezeには独立PilotとOwner資源上限を必ず先行させる。**コード／Backend science fit／大規模Monte Carlo／課金リソースの予約・実行は本書の作成範囲に含まれない。**
