# 22_06_family_causal

**Status:** `BD01_E11_BASIC_DESIGN_REVISED / OWNER_POLICY_APPROVED / INDEPENDENT_REVIEW_PENDING`. Original chapter and source provenance retained; DD physical coverage remains partial.  
**Source blob:** `87196f2f03a7f3367724bc05fb254d1a4d98109e`.

---

### 10.2 Causal

現行実装の`CausalPlanner`は`causal-analysis-spec/2`向けcompatibility plannerである。canonical `Execution.operation`を次のruntime StageTypeへ写像し、**1 canonical Executionにつき1 runtime StageからなるExecution Plan**を生成する。

| ExecutionOperation | StageType |
| --- | --- |
| `DISCOVERY` | `causal.discovery.v1` |
| `IDENTIFICATION` | `causal.identification.v1` |
| `ESTIMATION` | `causal.estimation.v2` |
| `REFUTATION` | `causal.refutation.v1` |
| `SENSITIVITY` | `causal.sensitivity.v1` |

したがって、現行実装のruntimeを次のような単一Plan内のDAGとして扱わない。

```text
IDENTIFICATION -> ELIGIBILITY -> ESTIMATION -> ...
```

`IDENTIFICATION`処理から`DATA_ELIGIBILITY_RESULT`等が生成され得ることと、`ELIGIBILITY`というruntime Stageが存在することは別である。科学的な前提関係はcanonical Executionの`input_graph_version_id` / `input_result_id`等とResult lineageで表現される。

Navigation側の`Setup / Discovery / Identification / Estimation / Effects / Diagnostics / Sensitivity`はユーザーの作業・閲覧コンテキストであり、runtime StageTypeと1:1対応させない。Identification / Estimationの科学的責務分離はNavigation設計として維持するが、それを理由に既存Causal runtime planを多段化しない。



### 10.2.1. Local Causal Graphの識別・不確実性保持

| Graph / evidence | Invariant / treatment |
|---|---|
| DAG | 指向辺の構造と仮定・versionを保持する |
| CPDAG | 向きの不確定な等価類をDAGとして捏造しない |
| PAG / FCI | endpoint circle/tail/arrow、潜在交絡に関する不確実性を保存し、無断DAG化しない |
| Latent MAG | Graph種別と潜在構造の解釈を区別し、PAGを特定MAGと自動同一視しない |
| Temporal | lag／same-time／direction／CI test条件を保存し、時間依存検証を省略しない |

- 修正Graphは**旧Version不変＋新Version/parent/edit rationale**とし、必ずIdentificationを再実行する。未確定Graphの方向を手で固定しただけで、未知の識別根拠があると主張しない。
- `Identification Outcome`はQuestion/Design/Estimand/Graph/Datasetのcontent identityと根拠・reasonsを保持。Estimator eligibilityはIdentification successとは別であり、Method support、instrument/mediator、sample/support、time structure、実効Backendを確認する。

### 10.2.2. Method別EstimandとDesignの契約

| Family | Initial target / design contract | Mandatory separation and limits | Trace |
|---|---|---|---|
| Baseline identification | Native Randomized／Backdoor、DoWhy Backdoor／Frontdoor／IV（各対応条件に限定） | Backdoor/IVの識別対象と利用者が指定したEstimandの対応を別途検査。DoWhyの内部`nonparametric-ate` labelをIV-LATEの証明とみなさない | FR-187, AR-029 |
| Baseline ATE/ATT estimation | diff-in-means、OLS、IPW、AIPW | Randomization/adjustment/overlap/weights、ATE/ATTの対象母集団、variance/CIをEstimator・構成ごとに区別 | FR-192, AR-033 |
| Refutation / Sensitivity | Placebo Treatment、Data Subset、Random Common Cause、Bootstrap、Adjustment Set、Propensity Clipping | どの科学仮説・上流Resultに対する反証か、random seed、再標本化・負例・Method制約を明示。単なる非有意を「頑健性証明」としない | FR-189, AR-044 |
| FD-A | 1 Mediator、承認済み限定線形FrontdoorによるATE数値推定 | Frontdoorの識別とモデル依存の2-stage estimationは別の成否／証拠 | FR-188, AR-030 |
| Observed Negative Control | 明示指定NCE/NCOとGraph・時間的適格性 | Null診断の非有意は無交絡の証明ではない；X-04の一般化はD | FR-190, AR-031 |
| OLS Unobserved Confounding | 古典OLS partial R²とpoint RV(q=1) | HC3推論への無検証転用、IPW/AIPW/CATE全面化不可 | FR-191, AR-032 |
| Weighted effect | IPW/IPTW/AIPWのATE/ATTと診断 | weight specification、normalization、clipping/trimming、overlap/balance/ESS/失効標本の区別 | FR-192, AR-033 |
| Non-IV CATE7 | LinearDML, CausalForestDML, DRLearner, ForestDRLearner, S/T/X-Learner | XとW、対象母集団、support；Method別CI availabilityを一括保証しない | FR-193, AR-034/035 |
| DRIV-A | 条件付きIV構造係数（IV_HETEROGENEOUS_EFFECT） | 非IV CATE、B0 complier LATE、将来の条件付きLATE estimator Cとは別 | FR-194, AR-034 |
| Temporal | PCMCI、PCMCI+、LPCMCIの承認済みscope | lag・endpoint・CI test適格性保持；RPCMCI/J-PCMCI+はD | FR-196, AR-036 |
| Time quasi-experiment | DiD、Event Study、ITS | 採用時期・parallel trends・cluster/autocorrelation・時点効果、Method別推論を区別 | FR-197, AR-037 |
| Threshold quasi-experiment | Sharp／Fuzzy RD | Cutoff、bandwidth、density、first-stage、局所IV Estimandを区別 | FR-198, AR-038 |
| IV-B0 | 単一二値Z/A、無調整のcomplier LATE | Wald/2SLSを承認済み比較として区別、IV仮定を検査 | FR-199, AR-039/040 |
| IV-B1 | 単一二値Z/A、事前指定Cを伴う加法線形IV構造係数 | B0や一般ATEと呼ばず、弱IVのAR反転に対応 | FR-199, AR-039/040 |
| SCM／SDID | donor-based counterfactual/DiD | SCM初期は**point-only**、未検証CI禁止。donor leakage／fit／期間を検査 | FR-200, AR-041 |

承認済みMethod一覧の**41件の義務とR/Q/N/Dの68 Scope**は [Scientific Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md) がauthority。本表はMethod採用範囲を変更しない。

採用Methodの正確な範囲・Phase・非対応事項は[Scientific Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)を参照する。

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-043（SPLIT）

- 既存要件の設計情報を含む原文：Identificationは全reasonを収集後、確定的不整合をreview statusより優先してstatus決定する
- RDに残る能力／Legacy Trace：識別判断に確定的不整合がある場合はそれを明示し、レビュー待ちとして誤表示しない
- Original Requirement：`FR-043`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-045（MOVE_BD）

- 既存要件の設計情報を含む原文：Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-044の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-045`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-048（SPLIT）

- 既存要件の設計情報を含む原文：estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない
- RDに残る能力／Legacy Trace：推定手法に適合した診断を提示し、適用不能な診断を強制しない
- Original Requirement：`FR-048`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)
