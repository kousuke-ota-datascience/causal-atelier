# DOC-01 — 10要件定義：RD-03／RD-04の発行・移管履歴

**Kind:** FLOW/AUDIT. **Source HEAD:** `eed23303f0104ca2ffc2cc4ed13042cff0cd314a`. 正式要件行・科学的制約は改訂後の10系ストック文書に保持する。

## 10_00_overall_RD.md — original §§90〜93

**Source blob:** `41ef6a133636de52fd6ac8e346e7145254b3519f`.

## 90. この文書種別の目的・責務・規範性

- **目的:** User/OperatorがAriadneに期待してよい機能、科学的許容条件、状態、セキュリティ、再現性および検証可能な受入条件を定める。
- **含む:** MUST/SHOULD/MUST NOT、FR/NFR/AR ID、Requirement Status/Implementation Status/Delivery、Actor/UC/Scope、科学的反例、Test/Acceptance Sourceへのリンク。
- **含まない:** Python classの命名やprivate field、REST/CLIのwire format詳細、推定アルゴリズムの実装手続。
- **優先順位:** 現行正本の規範性は`docs/wiki/requirement_definition/10_requirements_definition.md`に残る。DEC09で採用された意味差分は別途この作業コピーで改訂草案を作り、Ownerによる最終内容・SHA確認に加え、ENH-E11の全対象テストPASS後にのみControlled Publicationする。
- **E11特則:** 旧§11のDoWhy/EconML除外は、DEC09採用のE11機能別optional外部engineに限定して作業版§11.1で例外規定を反映済み。旧FR-161（E10 optional predictive engine）はこの許可の根拠として転用しない。
- **受入:** Scope68行ごとのR/Q/N/D、E11-REQ仮ID→新正式ID、Method/UC/Issue/Architecture/Gate、旧条文との逐条diffを監査する。既存ProductのPARTIALを黙ってIMPLEMENTEDにしない。

**E11旧草案（正式条文発行前）:** [../prior_drafts/10_requirements_definition/enh_e11_formal_requirement_publication_draft.md](../prior_drafts/10_requirements_definition/enh_e11_formal_requirement_publication_draft.md)（RD-03で条文化済み）

## 91. ENH-E11正式要件の発行規則（RD-03）

- **発行済みの正式ID：FR-185〜203（19）、NFR-029〜036（8）、科学的AR-028〜044（17）。** 全44件のLevel/Statusは`MUST / ACTIVE / UNVERIFIED / ENH-E11`とする。
- `ACTIVE`は要求義務が有効なこと、`UNVERIFIED`は充足状態が未検証であることを示す。**実装完了、科学的受入、Gate PASS、Coding指示ではない。**
- 既存の195 FR、36 NFR、27 Scientific ARのID・原文・Statusは変更していない。既存Productの保存済み契約と`causal-analysis-spec/2`も維持する。
- E11-A-01〜07はArchitecture候補であり、Scientific Integrityの`AR`系列へ採番しない。22 BD/ADRへ移管し、外部観測可能な義務だけをFR/NFR/Scientific ARに反映する。
- 新E11要件と草案の対応は[RD-03 traceability](../rd03_review/96_rd03_formal_requirement_traceability.md)を参照。Method固有の提供義務とEstimandの科学的制限は[10_32_scientific_method_scope.md](../../10_requirements_definition/10_32_scientific_method_scope.md)に保持する。
- **Authority boundary:** OwnerはDEC09で要件の意味とScopeを承認した。今回、改訂版working-copyに正式条文・IDを発行した。**最終SHAのOwner確認・原正本への昇格・ADR/Schema Freeze・Gate06/07・Science/Legalは別途未完了**。

## 92. ENH-E11のCanonical昇格条件（Owner決定 2026-11-16）

ENH-E11の要件・設計・監査成果物は、この`Revised_requirements_definition_documents/`ディレクトリを作業期間中の正規の格納先とする。元`docs/wiki/requirement_definition/`は、**ENH-E11の対象テストが全件PASSした後にのみ昇格**する。したがってRD-03の新FR/NFR/科学的AR発行やScope/Method/UCのトレース完了だけでは昇格しない。実装充足・科学的受入・回帰試験の未完を記録し、対象全件のPASS証拠を確認してから昇格を実施する。詳細は[昇格方針](../../combined_review/decisions/93_enh_e11_canonical_promotion_policy.md)。

## 93. RD-04：既存要件の改訂・設計移管（2026-11-16）

- RD-01の旧258件を再審査して`KEEP_RD=136`、`REWRITE_RD=7`、`SPLIT=96`、`MOVE_BD=19`を適用した。122条文を改訂し、136条文は維持。
- 元ID／Level／Status／Implementation Status／DeliveryとE11新44条文を変更せず、設計情報を21/22/23/30系の各担当ファイルへ移管記録として保持した。
- Method Scope／数値受入（AR-016 bootstrap、FR-072比較、E11の科学制約）を維持する。
- [RD-04全体監査](../rd04_review/98_rd04_consistency_verification.md)は文書構造とTraceに関してPASS。人間の内容最終レビュー、BD／IF／DDの具体化、科学・Gate・Legalの独立判定は未完了。
- 正本昇格は全対象テストPASS後にのみ実施する。


---

## 10_30_ar_scientific_integrity.md.md — original RD-04 transfer register

**Source blob:** `f07626f0cb79aa19e7489db6341b8ea419f885cf`；records 2.

## 98. RD-04：Scientific Integrityへの原文制約保持

**Status:** `RD04_SCIENTIFIC_TRANSFER_RECORDED / OWNER_CONTENT_REVIEW_PENDING`。要件の抽象化で科学的に有効な方法・受入条件を落とさない。元条文・元IDは監査可能であり、科学的PASSやMethod互換性を意味しない。

### 98.1. FR-067（SPLIT）

- 元条文に含まれる条件：untouched TEST population上で指定subgroup columnごとのmetric、`sample_count`、計算可能な場合のbootstrap uncertaintyを確認できる
- RDでの要求核：指定Subgroupの評価指標・標本数と計算可能な不確実性を確認できる
- ID：`FR-067`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.2. FR-072（REWRITE_RD）

- 元条文に含まれる条件：Result比較はまずsemantic compatibilityを検証し、direct metric comparisonではさらに同一DatasetVersion、同一TEST-row identity/hash、同一定義metricを要求する
- RDでの要求核：意味的に比較可能なResultのみを比較する。直接数値差分は、同一DatasetVersion・同一TEST標本identity/hash・同一定義metricが一致する場合に限り算出できる
- ID：`FR-072`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

---

## 10_31_ar_estimand_inference.md.md — original RD-04 transfer register

**Source blob:** `86ba789748a1b196708022d38ab2bbb6acb6684c`；records 2.

## 98. RD-04：Estimand / Identificationへの原文制約保持

**Status:** `RD04_SCIENTIFIC_TRANSFER_RECORDED / OWNER_CONTENT_REVIEW_PENDING`。要件の抽象化で科学的に有効な方法・受入条件を落とさない。元条文・元IDは監査可能であり、科学的PASSやMethod互換性を意味しない。

### 98.1. FR-043（SPLIT）

- 元条文に含まれる条件：Identificationは全reasonを収集後、確定的不整合をreview statusより優先してstatus決定する
- RDでの要求核：識別判断に確定的不整合がある場合はそれを明示し、レビュー待ちとして誤表示しない
- ID：`FR-043`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.2. AR-006（REWRITE_RD）

- 元条文に含まれる条件：Identification statusは全reasonを収集後に決定する
- RDでの要求核：因果識別の成否は全ての不適格理由と不確実性を考慮して決定しなければならない
- ID：`AR-006`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

---

## 10_32_scientific_method_scope.md.md — original RD-04 transfer register

**Source blob:** `15fb554c37f5a046147ae6da15844c570eb55dd0`；records 8.

## 98. RD-04：Method Scopeへの原文制約保持

**Status:** `RD04_SCIENTIFIC_TRANSFER_RECORDED / OWNER_CONTENT_REVIEW_PENDING`。要件の抽象化で科学的に有効な方法・受入条件を落とさない。元条文・元IDは監査可能であり、科学的PASSやMethod互換性を意味しない。

### 98.1. FR-069（SPLIT）

- 元条文に含まれる条件：explanation method capabilityが宣言するsupported scopeに従いglobal / local Predictive Explanationを生成でき、unsupported scopeを擬似出力で補完しない
- RDでの要求核：利用可能な範囲でモデル全体・個別予測の説明を生成でき、未対応の範囲を偽装しない
- ID：`FR-069`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.2. FR-161（SPLIT）

- 元条文に含まれる条件：LightGBM / SHAP / LIME等のexternal analytical engineはoptional capabilityとして導入し、未導入でもcore startupと既存supported flowを壊さず、unavailable capabilityから別model/methodへsilent fallbackしない
- RDでの要求核：追加分析機能が未導入でも基本機能を使え、未対応手法へ勝手に切替えない
- ID：`FR-161`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.3. FR-178（SPLIT）

- 元条文に含まれる条件：Binary Classification / RegressionでLightGBM backend（`lightgbm_classifier.v1` / `lightgbm_regressor.v1`）をtask-compatible modelとして選択できる
- RDでの要求核：表形式分類・回帰で承認済み追加学習方式を選択して学習・評価できる
- ID：`FR-178`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.4. FR-181（SPLIT）

- 元条文に含まれる条件：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- RDでの要求核：利用可能なモデル説明方式を適合性に応じて選択し、予測への変数寄与を定量的に説明できる
- ID：`FR-181`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.5. FR-182（SPLIT）

- 元条文に含まれる条件：`SHAP_TREE`はapproved compatibility範囲でglobal/localを提供し、`LIME_TABULAR`はlocal-onlyを提供する。unsupported capabilityを別methodまたは擬似global出力で補完しない
- RDでの要求核：個別予測・モデル全体への説明の提供範囲を明示し、未対応の説明を擬似出力しない
- ID：`FR-182`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.6. FR-048（SPLIT）

- 元条文に含まれる条件：estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない
- RDでの要求核：推定手法に適合した診断を提示し、適用不能な診断を強制しない
- ID：`FR-048`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.7. AR-016（SPLIT）

- 元条文に含まれる条件：subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない
- RDでの要求核：評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない
- ID：`AR-016`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

### 98.8. AR-027（REWRITE_RD）

- 元条文に含まれる条件：coefficient contribution / SHAP / LIMEはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない
- RDでの要求核：予測モデルの説明値はモデルの挙動に関するものであり、変数の因果的重要性・介入効果・因果機構を示さない
- ID：`AR-027`。定量的条件・Method名・原文制約は後続のScience／Acceptance検証で引き続き拘束として扱う。

---

## 10_91_acceptance_conditions.md — original §§12.1〜12.2

**Source blob:** `a8094f5f957cd141c246305b299fa8f72a07c3ea`.

## 12.1. ENH-E11の追加総合受入条件（正式要件発行時点）

1. DEC09の68 Scope行についてR/Q/N/Dを区別し、既存・新規Requirementへ追跡する。後続送りDを初期実装の完了義務と見なさない。
2. 全41 Methodを、Method別Estimand・適格性・推論Availability・実効Backend/Library・既知真値・科学的負例・参照比較で独立検証する。
3. 10 UCについて、Formal FR/NFR/Scientific AR、Method Scope、実装Workstream、受入Evidenceを追跡可能にする。
4. DEC07採用のGate-wide `FWER=0.05`方針とMethod別K/R/MC・Compute Budgetは、独立受入用の事前登録・Owner Freeze・科学的評価を別途必要とする。未測定値を科学的PASSとして扱わない。
5. 旧`causal-analysis-spec/2`と既存Product Web/API/Worker/DB、CLI、既存FR/NFR/ARの互換性を保護する。
6. 個票CATEやLocal Artifactの機微情報保護、Partial Artifactの不正公開防止、Optional Backend不在の隔離、配布前ライセンス審査を必須とする。

**Evidence status:** `NOT_GENERATED / GATE06_GATE07_NOT_FROZEN / SCIENCE_NOT_RUN`。計画の承認と科学的受入は区別する。[全件Trace](../rd03_review/96_rd03_formal_requirement_traceability.md)を参照。

## 12.2. RD-04で保持する既存の数値受入条件

- `AR-016`：適用可能なSubgroup metricは`sample_count`を保持し、現行の採用済み仕様において、信頼水準0.95のpercentile bootstrap、**1000回の再標本化、deterministic seed**を使用する。推論が計算不能な条件で区間を捏造しない。
- `FR-072`：直接metric差分には同一`DatasetVersion`、同一TEST-row identity/hash、同一定義metricの一致が必要。一般的なsemantic compatibilityだけでは十分でない。
- `AR-027`：SHAP／LIME／coefficient contributionを因果効果・因果機構の証拠として報告しない。
- `NFR-035`及びENH-E11 DEC07の独立科学受入（FWER=0.05、Method別K/R/MC等）は前節§12.1のとおり未完。数値受入条件を今回の抽象化で変更しない。

**Note:** `AR-016`の方式・反復数は既存に承認されたSubgroup評価の対象へ適用するのであり、ENH-E11のすべての因果Estimatorに対する普遍的なBootstrap義務と拡張解釈しない。


---

