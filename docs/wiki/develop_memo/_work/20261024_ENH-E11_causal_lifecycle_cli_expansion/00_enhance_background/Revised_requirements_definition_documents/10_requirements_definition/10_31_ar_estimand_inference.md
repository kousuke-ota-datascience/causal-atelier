# 10_31_ar_estimand_inference

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## AR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| AR-005 | Scientific Integrity | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-006 | Scientific Integrity | 因果識別の成否は全ての不適格理由と不確実性を考慮して決定しなければならない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-007 | Scientific Integrity | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-008 | Scientific Integrity | 推定に必要な変数型が適格かを識別できなければならない | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-009 | Scientific Integrity | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-010 | Scientific Integrity | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-023 | Scientific Integrity | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-024 | Scientific Integrity | 因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-028 | Graph Uncertainty | GraphのPAG／CPDAG等価類・circle端点・潜在交絡可能性は識別可能性と独立に保持し、未確定辺を無根拠に方向確定してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-029 | Identification Integrity | 因果識別の前提・証拠とEstimator適格性を分離し、明示的な識別根拠と適格性が成立しない場合は科学的負結果を返さなければならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-030 | Frontdoor Scope | 初期Frontdoor数値推定は単一Mediatorの承認済み限定線形設計FD-Aに限り、追加モデル仮定・適格性・識別と推定の差を明示しなければならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-034 | Estimand Separation | 非IV CATE・IV条件付き構造係数・complier LATE・ATE／ATT・RD局所効果は別Estimandであり、無条件に同一効果へ変換してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-036 | Temporal Validity | 時間遅れ・同時点関係・潜在交絡の不確実性とCI検定の適用条件を保持し、時間索引・欠損・自己相関等の不適格状態を無視してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-037 | Quasi Experimental Validity | DiD／Event Study／ITSでは介入時点・事前傾向・採用時期・集計単位・自己相関・Cluster等の手法固有前提と推論可否を評価しなければならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-038 | Regression Discontinuity | Sharp／Fuzzy RDの局所Estimandを明示し、Cutoff・Bandwidth・DensityおよびFuzzy RDのFirst Stage適格性を区別しなければならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-039 | IV Target Distinction | B0の二値Z／A・無調整complier LATEと、B1の単一二値Z／A・事前指定共変量・加法線形IV構造係数を区別し、B1を一般ATEや同一LATEと呼んではならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-040 | Weak IV Confidence Sets | B0／B1のAR反転信頼集合は有界・非有界・非連結・全実数を区別し、初期の正常AR反転からEMPTYを返してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-041 | Synthetic Design Constraints | SCM／SDIDでDonor適格性・介入前Fit・汚染・期間条件を検査し、初期SCMをpoint-onlyとして未検証CIを付与してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| AR-043 | Graph Revision Provenance | 研究者が未確定Graphの方向を変更する場合、元Graphを不変に保持して根拠付き新Versionとして再識別し、単なる警告Overrideで非識別を回避してはならない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |

### 7.0.2. Scientific comparability contract

Comparisonは次の二段階で判定する。

1. `semantic_compatible`
2. `direct_metric_comparable`

Predictive semantic keyは`task_type / prediction target(outcome) / prediction unit / prediction time / horizon / deployment/evaluation population semantics`。Direct metric comparisonではさらに`same dataset_version_id / same TEST-row identity(hash) / same metric definition`を要求する。

Causal semantic keyは`treatment(exposure) / outcome / estimand / target population`。Direct comparisonではsame data/view/analysis populationも要求する。

semantic mismatchは比較request自体のtechnical failureにせず、compatible=falseとreasonを返し、quantitative delta/rankingを生成しない。AUC/RMSE/ATE等を単一scoreへ正規化しない。
