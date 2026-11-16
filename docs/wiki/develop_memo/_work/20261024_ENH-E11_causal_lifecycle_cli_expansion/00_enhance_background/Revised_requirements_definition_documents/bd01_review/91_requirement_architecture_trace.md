> **Archive location note (2026-11-16):** This is a BD-01 enhancement-specific review/trace record, not a stock Basic Design chapter. The owner-approved permanent architecture obligations are maintained in `22_product_basic_design/22_00〜22_17`. Original content at source blob `9e33b3000c8744aee192f0f6997cdc65feffc691`; links were updated to current stock files. This record is not independent Architecture PASS.

# BD-01 — Requirement ⇄ Architecture Responsibility Trace

**Date:** 2026-11-16  
**State:** `TRACE_ALLOCATED_44_44 / OWNER_DEC09_POLICY_MAPPED_7_7 / IF_DD_AND_INDEPENDENT_REVIEW_PENDING`.

## 1. Contract and status

- 既存[RD-04](../doc01_review/rd04_review/98_rd04_consistency_verification.md)の改訂と[RD-03 68 Scope／41 Method／10 UC](../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md)を起点に、新規E11 FR19/NFR8/Scientific AR17の44条文を責務別BDへ割り当てる。
- この表の`BD primary`は条文の主要な設計責務であり、Method全件の実装／科学Evidenceが揃った意味ではない。各条文のStatusは元RDと一致させる。
- E11-A1〜7はArchitecture草案であり、新規Scientific ARではない。

## 2. Formal requirement 44 rows

| Requirement ID | Clause | Requirement State | Primary BD | Secondary BD | Further review / gate |
|---|---|---|---|---|---|
| FR-185 | ローカル因果分析の問い・デザイン・グラフ・データと参照版を識別し、上流条件が異なる結果の暗黙の再利用を拒否できる | MUST/ACTIVE/UNVERIFIED | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-186 | 因果Graphの種類・未確定端点・潜在交絡可能性・時間遅れと方向を保持し、未確定Graphを確定DAGや効果値に暗黙変換しない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-187 | 指定Estimand・Design・Graph・仮定に対する識別可能性とEstimator適格性を区別して判定し、不適格・非識別を数値推定成功として扱わない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-188 | 承認済みの限定Frontdoor条件下で平均介入効果を数値推定でき、識別結果と推定結果を別個に提示できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | FD-A exact single mediator/linear assumptions and actual numerical API |
| FR-189 | 承認済みのRefutationおよびSensitivityを実行でき、適用範囲・結果・再現条件・科学的限界を手法別に提示できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-190 | 適格な観測Negative Control Exposure／Outcomeを研究者が明示指定した場合に限り、条件付き負対照診断を行い、適格性と結果を提示できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-191 | 承認済みの回帰モデルについて未観測交絡への感度を定量評価し、非対応推定器に無根拠に一般化しない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-192 | 重み付き因果推定で重みの意味・安定性・overlap・balance・標本損失・推論可否を区別して診断できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-193 | 条件付き因果効果の推定で効果修飾因子と交絡調整因子を区別し、対象集団・適格性・支持域・不確実性を提示できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-194 | 条件付き操作変数による構造係数を、非IVのCATEおよびcomplier LATEと異なる推定対象として識別・評価できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-195 | 探索的点推定と確認的推論を区別して提示し、個票の異質効果について閲覧・出力を権限と適格性に応じて制御できる | MUST/ACTIVE/UNVERIFIED | [22_12_security.md](../22_product_basic_design/22_12_security.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | LOCAL authorization principal for individual CATE opt-in |
| FR-196 | 時系列の因果探索で時間遅れ・同時点関係・方向の未確定性を保持し、時系列と手法の適格性を示せる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-197 | 介入時点を伴う準実験で、手法固有のEstimand・前提・時点別効果・誤差構造・推論可否を評価できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-198 | 閾値による準実験で局所効果の推定対象を明示し、Cutoff周辺の適格性と結果を評価できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-199 | 操作変数のcomplier LATEと線形IV構造係数を区別して推定し、弱操作変数の下で妥当な推論集合と診断を提示できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | B0/B1 different estimands, AR inversion shape and coverage |
| FR-200 | 対照Donorを用いた準実験で介入前Fit・汚染・期間条件と手法別の推定／推論範囲を評価できる | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| FR-202 | 効果点推定・不確実性の可用性・科学的受入状態を区別し、有界・非有界・非連結・全実数の推論集合を損失なく表現できる | MUST/ACTIVE/UNVERIFIED | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | effect/inference/science state wire schema |
| FR-201 | 承認された因果分析をProduct Web／DBに依存せずCLIから実行し、科学的負結果・利用不能状態・技術失敗を区別する再現可能な成果物を得られる | MUST/ACTIVE/UNVERIFIED | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | CLI-only versioned contract and legacy regression |
| FR-203 | 既存Product因果分析と新Local Scientific CLI契約を区別し、旧仕様と既存Review／Override統制を維持できる | MUST/ACTIVE/UNVERIFIED | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| NFR-029 | ローカル分析の入力・実行条件・実効Backend／Library版・乱数／分割条件・出力の同一性と来歴を第三者が検証できる | MUST/ACTIVE/UNVERIFIED | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| NFR-033 | 採用された科学Methodを再現可能な依存関係と検証済み実行Profileで導入・実行でき、導入前後の互換性を確認できる | MUST/ACTIVE/UNVERIFIED | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | 5 Profile lock/API fresh venv evidence |
| NFR-030 | ローカル成果物の保存に失敗した場合、部分的な書込みや不完全な成果物を正常な正本として公開しない | MUST/ACTIVE/UNVERIFIED | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | multi-file atomic publish and crash-readback |
| NFR-035 | 採用Methodの科学的受入を独立した既知真値・負例・再現性・推論品質の検証で実施し、事前登録した比較と多重性を考慮する | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| NFR-036 | 新Local CLI機能が既存Scientific CLI、Product API／UI／Worker／DBおよび因果分析仕様・結果の互換性を損なわない | MUST/ACTIVE/UNVERIFIED | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| NFR-031 | ローカル分析で不正なPath／Symlink／任意実行Objectを拒否し、個票出力を権限・最小化条件に従い管理する | MUST/ACTIVE/UNVERIFIED | [22_12_security.md](../22_product_basic_design/22_12_security.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | local OS identity + individual export policy |
| NFR-032 | 任意導入の科学Backendの不在・不適合が既存Coreや別Methodの稼働を妨げず、当該能力のUnavailable状態と理由を明示できる | MUST/ACTIVE/UNVERIFIED | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate06 IMPLEMENTATION; Gate07 where scientific |
| NFR-034 | 配布先ごとのライセンス審査が完了しない限り、審査対象の外部ライブラリを含む顧客納入を許可しない | MUST/ACTIVE/UNVERIFIED | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | artifact-specific GPL delivery approval |
| AR-031 | 観測NCE／NCOは研究者の明示opt-inとGraph／時間的適格性を要し、Null検査の非有意を未観測交絡がない証明と解釈してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-032 | 初期の未観測交絡感度は古典OLS係数のpartial R²とpoint RV（q=1）に限り、HC3やIPW／AIPW／CATEへ無検証に一般化してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-033 | IPW／IPTW／AIPWの解析重み・正規化・Clipping／Trimmingとoverlap／balance／ESSを区別し、適格性に裏付けられない区間推論を生成してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-035 | 探索的点推定を確認的推論の成功と表してはならず、確認的区間推論には対象Method・構成に適合した推論根拠が必要である | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-042 | 非識別・適格性不足・Review要・推論未対応・Backend利用不能を技術失敗や数値ゼロに読み替えてはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-044 | 採用MethodのEstimand・適格性・点推定・推論を個別の既知真値と負例で検証し、未対応の推論や点ごとの区間を同時信頼帯として報告してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Method-specific independent oracle and CI coverage |
| AR-028 | GraphのPAG／CPDAG等価類・circle端点・潜在交絡可能性は識別可能性と独立に保持し、未確定辺を無根拠に方向確定してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-029 | 因果識別の前提・証拠とEstimator適格性を分離し、明示的な識別根拠と適格性が成立しない場合は科学的負結果を返さなければならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-030 | 初期Frontdoor数値推定は単一Mediatorの承認済み限定線形設計FD-Aに限り、追加モデル仮定・適格性・識別と推定の差を明示しなければならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-034 | 非IV CATE・IV条件付き構造係数・complier LATE・ATE／ATT・RD局所効果は別Estimandであり、無条件に同一効果へ変換してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-036 | 時間遅れ・同時点関係・潜在交絡の不確実性とCI検定の適用条件を保持し、時間索引・欠損・自己相関等の不適格状態を無視してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-037 | DiD／Event Study／ITSでは介入時点・事前傾向・採用時期・集計単位・自己相関・Cluster等の手法固有前提と推論可否を評価しなければならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-038 | Sharp／Fuzzy RDの局所Estimandを明示し、Cutoff・Bandwidth・DensityおよびFuzzy RDのFirst Stage適格性を区別しなければならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-039 | B0の二値Z／A・無調整complier LATEと、B1の単一二値Z／A・事前指定共変量・加法線形IV構造係数を区別し、B1を一般ATEや同一LATEと呼んではならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-040 | B0／B1のAR反転信頼集合は有界・非有界・非連結・全実数を区別し、初期の正常AR反転からEMPTYを返してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | non-bounded/nonconnected/ALL_REAL serialization |
| AR-041 | SCM／SDIDでDonor適格性・介入前Fit・汚染・期間条件を検査し、初期SCMをpoint-onlyとして未検証CIを付与してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Gate07 SCIENCE + Gate06 CONTRACT |
| AR-043 | 研究者が未確定Graphの方向を変更する場合、元Graphを不変に保持して根拠付き新Versionとして再識別し、単なる警告Overrideで非識別を回避してはならない | MUST/ACTIVE/UNVERIFIED | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | Gate07 SCIENCE + Gate06 CONTRACT |

## 3. All seven approved Architecture policies

| DEC09 authority | Decision | BD primary | BD secondary | Gate to close |
|---|---|---|---|---|
| ARC09-01 | Domain authority | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | Domain/Adapter invariant split, typed graph/estimand |
| ARC09-02 | Optional Backend Isolation | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | Effective API/profiles/import boundaries |
| ARC09-03 | Identification before estimation | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Graph/assumption eligibility and no unreviewed fallback |
| ARC09-04 | Local versioned CLI and Artifact | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | v2 dual-lane, local manifest/atomic/privacy |
| ARC09-05 | Typed effect & inference | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | AR set topology, point/inference/science separation |
| ARC09-06 | Environment/Lock/SBOM | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | 5 profiles, uv.lock, manifest, legal |
| ARC09-07 | Product freeze/future lane | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | No new Web/API/DB/Worker/GAP closure |

## 4. Architecture candidate crosswalk

| Architecture draft | Responsibility | DEC09 origin | BD destination | Approval status |
|---|---|---|---|---|
| E11-A-01 | Domain authority | ARC09-01 | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-02 | Scientific adapter separation | ARC09-02 | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-03 | Fail-closed execution | ARC09-03 | [22_06_family_causal.md](../22_product_basic_design/22_06_family_causal.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-04 | Local vs Product authority | ARC09-04/07 | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-05 | Typed Result and CI | ARC09-05 | [22_09_results_artifacts_lineage.md](../22_product_basic_design/22_09_results_artifacts_lineage.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-06 | Backend profiles + dependencies | ARC09-06 | [22_13_deployment.md](../22_product_basic_design/22_13_deployment.md) | Owner policy adopted; concrete ADR/schema open |
| E11-A-07 | CLI-only Scope | ARC09-07 | [22_00_overall_BD.md](../22_product_basic_design/22_00_overall_BD.md) | Owner policy adopted; concrete ADR/schema open |

## 5. Remaining published obligation cross-references

| Contract | Source | BD place | Next level |
|---|---|---|---|
| 41 Method | [10_32](../10_requirements_definition/10_32_scientific_method_scope.md) | [22_21](../22_product_basic_design/22_06_family_causal.md) method/estimand matrix | Method-specific IF/Port/DD; Gate07 science |
| 68 Scope dispositions | [RD-03 trace](../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md) | [22_20](../22_product_basic_design/22_00_overall_BD.md) scope negative boundary | Workstream/Gate Scope test |
| 10 UC | [RD-03 trace](../doc01_review/rd03_review/96_rd03_formal_requirement_traceability.md) | [22_20](../22_product_basic_design/22_00_overall_BD.md) use case boundary + [22_21](../22_product_basic_design/22_06_family_causal.md) pipeline | IF/DD/Tests independent |
| Existing FR/NFR/AR transferred | [RD-04 audit](../doc01_review/rd04_review/98_rd04_consistency_verification.md) | Existing 22_00〜17 §97/98 | Preserve original design semantics and Status |
| Full test PASS then canonical promotion | [Owner rule](../combined_review/decisions/93_enh_e11_canonical_promotion_policy.md) | [22_90 review](90_architecture_consistency_review.md) | No promotion before all applicable tests PASS |

## 6. Mechanical assertion summary

- New FR19/NFR8/Scientific AR17 = 44 unique formal IDs, all have exactly one primary BD area; all retain `MUST/ACTIVE/UNVERIFIED/ENH-E11`.
- DEC09 ARC09-01〜07 = 7 decisions mapped. Architecture E11-A01〜07 = 7 mapped. This is a **mapping coverage test**, not independent Architecture PASS.
