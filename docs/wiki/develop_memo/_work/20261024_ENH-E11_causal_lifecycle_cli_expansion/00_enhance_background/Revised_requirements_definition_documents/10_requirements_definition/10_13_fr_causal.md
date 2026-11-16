# 10_13_fr_causal

**Status:** `RD03_FORMAL_E11_ISSUED / OWNER_SHA_REVIEW_PENDING`; original ID, level and state retained.  
**Source blob:** `40b83f29c67b4a39f6db5393be7534c5e892d656`.

---

## FR original requirement rows

| ID | Area | Requirement | Level | Requirement Status | Implementation Status | Delivery |
| --- | --- | --- | --- | --- | --- | --- |
| FR-035 | Causal | 複数algorithm / parameterでcausal discoveryを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-036 | Causal | User-definedまたはImported GraphをDiscoveryなしで登録できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-037 | Causal | DAG、CPDAG、PAGおよびendpoint semanticsを保持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-038 | Causal | Graph Candidateの共通条件、変更条件およびedge差分を比較できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-039 | Causal | FIXED Graphからchild DRAFTを作成し、編集理由を記録して再固定できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-040 | Causal | Population、Treatment、Comparator、Outcome、Time、Estimand、Decision UseをCausal Questionに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-041 | Causal | assignment、time zero、eligibility、strategy、adjustment set、assumptionsをCausal Designに固定する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-042 | Causal | Graph、Question、DesignからIdentification Resultを生成する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-043 | Causal | 識別判断に確定的不整合がある場合はそれを明示し、レビュー待ちとして誤表示しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-044 | Causal | 型、欠測、post-treatment、sample size、overlapをData Eligibilityとして評価する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-045 | Causal | 【設計制約移管・Legacy Trace】FR-044の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-046 | Causal | Identification、Eligibility、Estimator互換性を満たす場合のみEstimationを受け付ける | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-047 | Causal | ATEまたはATTと区間推定を生成できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-048 | Causal | 推定手法に適合した診断を提示し、適用不能な診断を強制しない | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-049 | Causal | Placebo TreatmentおよびData SubsetによるRefutationを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-050 | Causal | Adjustment SetおよびPropensity ClippingのSensitivityを実行できる | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-051 | Causal | 同一データを探索と確認的分析で再利用する場合、その事実と根拠を警告できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-052 | Causal | 同一条件のRERUNと条件変更のREVISEDを区別し、changed dimensionsとreasonを保存する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-053 | Causal | 科学的負結果をExecution failureと区別する | MUST | ACTIVE | IMPLEMENTED | BASELINE |
| FR-054 | Causal | 因果分析結果から入力データ・仮定・実行・成果物の来歴を追跡できる | MUST | ACTIVE | PARTIAL | ENH-E5 |
| FR-153 | Causal | Causalは`setup / discovery / identification / estimation / effects / diagnostics / sensitivity`をFamily-local Navigation Stageとして提供する | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-154 | Causal | IdentificationとEstimationを別Navigation Stageとして扱い、識別可能性と有限標本推定を混同しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-155 | Causal | EstimationとEffectsを別Navigation Stageとして扱い、推定設定と推定結果の閲覧・利用を混同しない | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-156 | Causal | DiagnosticsとSensitivityを別Navigation Stageとして扱う | MUST | ACTIVE | IMPLEMENTED | ENH-E5 |
| FR-186 | Causal Graph | 因果Graphの種類・未確定端点・潜在交絡可能性・時間遅れと方向を保持し、未確定Graphを確定DAGや効果値に暗黙変換しない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-187 | Causal Identification | 指定Estimand・Design・Graph・仮定に対する識別可能性とEstimator適格性を区別して判定し、不適格・非識別を数値推定成功として扱わない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-188 | Causal Frontdoor | 承認済みの限定Frontdoor条件下で平均介入効果を数値推定でき、識別結果と推定結果を別個に提示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-189 | Causal Robustness | 承認済みのRefutationおよびSensitivityを実行でき、適用範囲・結果・再現条件・科学的限界を手法別に提示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-190 | Causal Negative Controls | 適格な観測Negative Control Exposure／Outcomeを研究者が明示指定した場合に限り、条件付き負対照診断を行い、適格性と結果を提示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-191 | Causal Sensitivity | 承認済みの回帰モデルについて未観測交絡への感度を定量評価し、非対応推定器に無根拠に一般化しない | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-192 | Causal Weight Quality | 重み付き因果推定で重みの意味・安定性・overlap・balance・標本損失・推論可否を区別して診断できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-193 | Causal Heterogeneity | 条件付き因果効果の推定で効果修飾因子と交絡調整因子を区別し、対象集団・適格性・支持域・不確実性を提示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-194 | Causal IV Heterogeneity | 条件付き操作変数による構造係数を、非IVのCATEおよびcomplier LATEと異なる推定対象として識別・評価できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-195 | Causal Heterogeneity Output | 探索的点推定と確認的推論を区別して提示し、個票の異質効果について閲覧・出力を権限と適格性に応じて制御できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-196 | Causal Temporal | 時系列の因果探索で時間遅れ・同時点関係・方向の未確定性を保持し、時系列と手法の適格性を示せる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-197 | Causal Quasi Experimental Time | 介入時点を伴う準実験で、手法固有のEstimand・前提・時点別効果・誤差構造・推論可否を評価できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-198 | Causal Discontinuity | 閾値による準実験で局所効果の推定対象を明示し、Cutoff周辺の適格性と結果を評価できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-199 | Causal Instrumental Variables | 操作変数のcomplier LATEと線形IV構造係数を区別して推定し、弱操作変数の下で妥当な推論集合と診断を提示できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-200 | Causal Synthetic Controls | 対照Donorを用いた準実験で介入前Fit・汚染・期間条件と手法別の推定／推論範囲を評価できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
| FR-202 | Scientific Result | 効果点推定・不確実性の可用性・科学的受入状態を区別し、有界・非有界・非連結・全実数の推論集合を損失なく表現できる | MUST | ACTIVE | UNVERIFIED | ENH-E11 |
