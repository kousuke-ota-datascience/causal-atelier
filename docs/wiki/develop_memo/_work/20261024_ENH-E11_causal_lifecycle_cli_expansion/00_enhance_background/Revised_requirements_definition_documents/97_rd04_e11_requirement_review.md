# RD-04 — ENH-E11新規44条文の科学的・機能的整合性レビュー

**Date:** 2026-11-16  
**State:** `ALL_44_REVIEWED_FOR_TRACE_AND_CLAUSE_PRESERVATION / NO_STATUS_CHANGE / OWNER_FINAL_SEMANTIC_REVIEW_PENDING`。

## 1. Review judgement

- **44/44条文がRD-03発行時の原文と一致**し、`MUST / ACTIVE / UNVERIFIED / ENH-E11`を保持。RD-04で要件の既存258件を改訂したことにより、新規E11要件は無断変更していない。
- 対象はOwnerがDEC09で意味論・Scopeを承認したE11のFR19/NFR8/科学的AR17である。E11-Aは別Architecture要求草案であり、Science ARへ付け替えない。
- 要件が互いに矛盾するという確定的な反例は今回の条文レビューでは検出していない。しかし、以下の設計・実効Backend・科学的適格性は**未検証**であり、矛盾が存在しないことを証明した意味ではない。

## 2. Clause-by-clause review

| ID | Area | Clause as issued | Level / Status / Implementation | Trace | Review status / design follow-up |
|---|---|---|---|---|---|
| FR-185 | Local Scientific Identity | ローカル因果分析の問い・デザイン・グラフ・データと参照版を識別し、上流条件が異なる結果の暗黙の再利用を拒否できる | MUST / ACTIVE / UNVERIFIED | [10_10_fr_project_context_data.md](10_requirements_definition/10_10_fr_project_context_data.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-186 | Causal Graph | 因果Graphの種類・未確定端点・潜在交絡可能性・時間遅れと方向を保持し、未確定Graphを確定DAGや効果値に暗黙変換しない | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-187 | Causal Identification | 指定Estimand・Design・Graph・仮定に対する識別可能性とEstimator適格性を区別して判定し、不適格・非識別を数値推定成功として扱わない | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-188 | Causal Frontdoor | 承認済みの限定Frontdoor条件下で平均介入効果を数値推定でき、識別結果と推定結果を別個に提示できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | FD-A限定の数値識別／推定について、線形モデル・単一Mediator・CIを科学的受入で確認する |
| FR-189 | Causal Robustness | 承認済みのRefutationおよびSensitivityを実行でき、適用範囲・結果・再現条件・科学的限界を手法別に提示できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-190 | Causal Negative Controls | 適格な観測Negative Control Exposure／Outcomeを研究者が明示指定した場合に限り、条件付き負対照診断を行い、適格性と結果を提示できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-191 | Causal Sensitivity | 承認済みの回帰モデルについて未観測交絡への感度を定量評価し、非対応推定器に無根拠に一般化しない | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-192 | Causal Weight Quality | 重み付き因果推定で重みの意味・安定性・overlap・balance・標本損失・推論可否を区別して診断できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-193 | Causal Heterogeneity | 条件付き因果効果の推定で効果修飾因子と交絡調整因子を区別し、対象集団・適格性・支持域・不確実性を提示できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-194 | Causal IV Heterogeneity | 条件付き操作変数による構造係数を、非IVのCATEおよびcomplier LATEと異なる推定対象として識別・評価できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-195 | Causal Heterogeneity Output | 探索的点推定と確認的推論を区別して提示し、個票の異質効果について閲覧・出力を権限と適格性に応じて制御できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | ローカルCLI個票出力の認可主体とOSファイル権限制御の対応をIF／Securityで定義する |
| FR-196 | Causal Temporal | 時系列の因果探索で時間遅れ・同時点関係・方向の未確定性を保持し、時系列と手法の適格性を示せる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-197 | Causal Quasi Experimental Time | 介入時点を伴う準実験で、手法固有のEstimand・前提・時点別効果・誤差構造・推論可否を評価できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-198 | Causal Discontinuity | 閾値による準実験で局所効果の推定対象を明示し、Cutoff周辺の適格性と結果を評価できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-199 | Causal Instrumental Variables | 操作変数のcomplier LATEと線形IV構造係数を区別して推定し、弱操作変数の下で妥当な推論集合と診断を提示できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | B0 LATE／B1 IV構造係数、AR反転の弱IV推論を独立Benchmarkで確認する |
| FR-200 | Causal Synthetic Controls | 対照Donorを用いた準実験で介入前Fit・汚染・期間条件と手法別の推定／推論範囲を評価できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-202 | Scientific Result | 効果点推定・不確実性の可用性・科学的受入状態を区別し、有界・非有界・非連結・全実数の推論集合を損失なく表現できる | MUST / ACTIVE / UNVERIFIED | [10_13_fr_causal.md](10_requirements_definition/10_13_fr_causal.md) | 有界・非有界・非連結・全実数の型付き信頼集合と非識別StatusのIF schemaをFreezeする |
| FR-201 | Local Scientific CLI | 承認された因果分析をProduct Web／DBに依存せずCLIから実行し、科学的負結果・利用不能状態・技術失敗を区別する再現可能な成果物を得られる | MUST / ACTIVE / UNVERIFIED | [10_17_fr_api_cli.md](10_requirements_definition/10_17_fr_api_cli.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| FR-203 | Legacy Compatibility | 既存Product因果分析と新Local Scientific CLI契約を区別し、旧仕様と既存Review／Override統制を維持できる | MUST / ACTIVE / UNVERIFIED | [10_17_fr_api_cli.md](10_requirements_definition/10_17_fr_api_cli.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| NFR-029 | Reproducibility | ローカル分析の入力・実行条件・実効Backend／Library版・乱数／分割条件・出力の同一性と来歴を第三者が検証できる | MUST / ACTIVE / UNVERIFIED | [10_20_nfr_reproducibility.md](10_requirements_definition/10_20_nfr_reproducibility.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| NFR-033 | Environment Reproducibility | 採用された科学Methodを再現可能な依存関係と検証済み実行Profileで導入・実行でき、導入前後の互換性を確認できる | MUST / ACTIVE / UNVERIFIED | [10_20_nfr_reproducibility.md](10_requirements_definition/10_20_nfr_reproducibility.md) | uv.lock profile/optional backendの実効互換性・サポート実行環境を検証する |
| NFR-030 | Reliability | ローカル成果物の保存に失敗した場合、部分的な書込みや不完全な成果物を正常な正本として公開しない | MUST / ACTIVE / UNVERIFIED | [10_21_nfr_reliability_performance.md](10_requirements_definition/10_21_nfr_reliability_performance.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| NFR-035 | Scientific Acceptance | 採用Methodの科学的受入を独立した既知真値・負例・再現性・推論品質の検証で実施し、事前登録した比較と多重性を考慮する | MUST / ACTIVE / UNVERIFIED | [10_21_nfr_reliability_performance.md](10_requirements_definition/10_21_nfr_reliability_performance.md) | Gate07のMethod別K/R/MC、FWER=0.05、事前登録と科学評価は未実施 |
| NFR-036 | Backward Compatibility | 新Local CLI機能が既存Scientific CLI、Product API／UI／Worker／DBおよび因果分析仕様・結果の互換性を損なわない | MUST / ACTIVE / UNVERIFIED | [10_21_nfr_reliability_performance.md](10_requirements_definition/10_21_nfr_reliability_performance.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| NFR-031 | Security and Privacy | ローカル分析で不正なPath／Symlink／任意実行Objectを拒否し、個票出力を権限・最小化条件に従い管理する | MUST / ACTIVE / UNVERIFIED | [10_22_nfr_security_compatibility.md](10_requirements_definition/10_22_nfr_security_compatibility.md) | CLI-onlyでProduct RBACに依存しない出力権限・ファイル保護モデルを設計する |
| NFR-032 | Dependency Isolation | 任意導入の科学Backendの不在・不適合が既存Coreや別Methodの稼働を妨げず、当該能力のUnavailable状態と理由を明示できる | MUST / ACTIVE / UNVERIFIED | [10_22_nfr_security_compatibility.md](10_requirements_definition/10_22_nfr_security_compatibility.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| NFR-034 | License Compliance | 配布先ごとのライセンス審査が完了しない限り、審査対象の外部ライブラリを含む顧客納入を許可しない | MUST / ACTIVE / UNVERIFIED | [10_22_nfr_security_compatibility.md](10_requirements_definition/10_22_nfr_security_compatibility.md) | 顧客別配布ライセンス審査はテストPASSと別に未完了 |
| AR-031 | Negative Control Semantics | 観測NCE／NCOは研究者の明示opt-inとGraph／時間的適格性を要し、Null検査の非有意を未観測交絡がない証明と解釈してはならない | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-032 | Sensitivity Scope | 初期の未観測交絡感度は古典OLS係数のpartial R²とpoint RV（q=1）に限り、HC3やIPW／AIPW／CATEへ無検証に一般化してはならない | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-033 | Weight and Inference Validity | IPW／IPTW／AIPWの解析重み・正規化・Clipping／Trimmingとoverlap／balance／ESSを区別し、適格性に裏付けられない区間推論を生成してはならない | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-035 | Exploratory and Confirmatory | 探索的点推定を確認的推論の成功と表してはならず、確認的区間推論には対象Method・構成に適合した推論根拠が必要である | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | Exploratory point-only／Confirmatory valid inferenceを区別するMethod別契約が必要 |
| AR-042 | Scientific Negative State | 非識別・適格性不足・Review要・推論未対応・Backend利用不能を技術失敗や数値ゼロに読み替えてはならない | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-044 | Method-specific Scientific Validation | 採用MethodのEstimand・適格性・点推定・推論を個別の既知真値と負例で検証し、未対応の推論や点ごとの区間を同時信頼帯として報告してはならない | MUST / ACTIVE / UNVERIFIED | [10_30_ar_scientific_integrity.md](10_requirements_definition/10_30_ar_scientific_integrity.md) | 既知真値・負例・pointwise CI coverage・FWERをMethod別独立受入で検証する |
| AR-028 | Graph Uncertainty | GraphのPAG／CPDAG等価類・circle端点・潜在交絡可能性は識別可能性と独立に保持し、未確定辺を無根拠に方向確定してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-029 | Identification Integrity | 因果識別の前提・証拠とEstimator適格性を分離し、明示的な識別根拠と適格性が成立しない場合は科学的負結果を返さなければならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-030 | Frontdoor Scope | 初期Frontdoor数値推定は単一Mediatorの承認済み限定線形設計FD-Aに限り、追加モデル仮定・適格性・識別と推定の差を明示しなければならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | Frontdoor FD-Aの追加識別条件・線形推定仮定を科学的に検証する |
| AR-034 | Estimand Separation | 非IV CATE・IV条件付き構造係数・complier LATE・ATE／ATT・RD局所効果は別Estimandであり、無条件に同一効果へ変換してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | 非IV CATE7／DRIVを別Estimandとして保持し、各構成CIを別に評価する |
| AR-036 | Temporal Validity | 時間遅れ・同時点関係・潜在交絡の不確実性とCI検定の適用条件を保持し、時間索引・欠損・自己相関等の不適格状態を無視してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-037 | Quasi Experimental Validity | DiD／Event Study／ITSでは介入時点・事前傾向・採用時期・集計単位・自己相関・Cluster等の手法固有前提と推論可否を評価しなければならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-038 | Regression Discontinuity | Sharp／Fuzzy RDの局所Estimandを明示し、Cutoff・Bandwidth・DensityおよびFuzzy RDのFirst Stage適格性を区別しなければならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |
| AR-039 | IV Target Distinction | B0の二値Z／A・無調整complier LATEと、B1の単一二値Z／A・事前指定共変量・加法線形IV構造係数を区別し、B1を一般ATEや同一LATEと呼んではならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | B0/B1構造差を数学的に保持し、B1をLATEと誤表示しない |
| AR-040 | Weak IV Confidence Sets | B0／B1のAR反転信頼集合は有界・非有界・非連結・全実数を区別し、初期の正常AR反転からEMPTYを返してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | 正常AR反転でEMPTY禁止、非標準集合4形態のlossless representationを検証する |
| AR-041 | Synthetic Design Constraints | SCM／SDIDでDonor適格性・介入前Fit・汚染・期間条件を検査し、初期SCMをpoint-onlyとして未検証CIを付与してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | SCM初期point-only・SDIDとの混同を防ぎ、Donor適格性を個別検証する |
| AR-043 | Graph Revision Provenance | 研究者が未確定Graphの方向を変更する場合、元Graphを不変に保持して根拠付き新Versionとして再識別し、単なる警告Overrideで非識別を回避してはならない | MUST / ACTIVE / UNVERIFIED | [10_31_ar_estimand_inference.md](10_requirements_definition/10_31_ar_estimand_inference.md) | RD-03条文維持。対象Method/ScopeとのTraceを保護し、技術・科学的充足は未検証 |

## 3. Open semantic/design questions

1. **CLI-onlyの認可境界**（FR-195/NFR-031）：Project RBACを新CLIに暗黙導入してはならない。ローカル実行者の認証・ファイルへのアクセス制御の主体と責務をSecurity/IFで決める。
2. **識別・推定・推論**（FR-187/188/199/202、AR-029/030/039/040/042）：識別結果とEstimator適格性、点推定とConfidence Set、および科学的負結果と技術失敗を型別にFreezeする。
3. **CATE/DRIV**（FR-193/194、AR-034/035）：非IV7 MethodとDRIV-AのEstimandが混同されないか、探索的点推定／確認的推論の制約をMethod・構成別に科学検証する。
4. **Method受入**（NFR-035/AR-044）：FWER=0.05、K/R/MC、Simulation、Known-truth、Negative fixture、Coverageの独立Gate証拠は未生成。
5. **Profile／ライセンス**（NFR-033/034）：実行互換・uv.lock・配布先Legal Gateは科学的・構造的な要件の正式条文化とは独立。
6. **SCM初期提供**（FR-200/AR-041）：point-onlyとし、同時に未検証CIを出力してはならない。

## 4. Scope limitation

このレビューは条文・トレースの整合性と未解決条件の抽出であり、コードテスト・統計的受入・ライセンス法務審査ではない。要件改訂版の正式なOwner SHA確認も未完。次はBD-01／IF-01／DD-01で具体化し、Gate06/07で独立判定する。元正本への昇格は**ENH-E11の全対象テストPASS後**のみ。[方針](93_enh_e11_canonical_promotion_policy.md)
