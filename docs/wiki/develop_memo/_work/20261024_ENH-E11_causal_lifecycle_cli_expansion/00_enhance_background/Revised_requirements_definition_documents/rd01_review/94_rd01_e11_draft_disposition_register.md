# RD-01 — ENH-E11 Provisional Requirement Register (34 IDs)

**Review ID:** RD-01  
**Date:** 2026-11-16  
**Source branch:** `prototype/ariadne_mvp` / source blob `40b83f29c67b4a39f6db5393be7534c5e892d656`; E11 draft blob `e6b151a0537054a11e8368520e940bd42cb68e2f`  
**Status:** `DISPOSITION_PROPOSED / NOT_YET_APPLIED / OWNER_REVIEW_REQUIRED`. 本書は逐条分類の提案記録であり、正式RD/BD/IF/DDの改訂、既存Requirementの失効、Method Scopeの変更、Gate PASSを意味しない。

**判定原則:** 『何を満たさなければならないか』をRDに残す。方法自体が承認された提供義務の場合は`10_32_scientific_method_scope.md`相当のScope契約で保持し、実装と同一視しない。科学的Estimand/前提の制限は`10_31`等で保持する。移管のみのIDもTrace台帳から削除せず、統合元要求を明記してControlled Publicationで処理する。

Source: [E11 formal requirement publication draft](../10_requirements_definition/10_14_enh_e11_formal_requirement_publication_draft.md).

## 1. E11-F (19 candidates)

| ID | 原文（正本 / 草案） | Disposition | RD側の要件核・暫定改訂文 | 下位文書・保持先 | 判定根拠 | Level | Requirement Status | Implementation Status | Delivery |
|---|---|---|---|---|---|---|---|---|---|
| E11-F-01 | Local Question、Design、Graph、Datasetはversionおよびcontent hashで同定し、上流条件が異なる推定の暗黙再利用を拒否する | SPLIT | 異なる研究条件の結果を混同せず、入力・仮定・成果物の来歴を識別し再利用の適否を検査できる | 21 LDD・23 IF・30 DD | version/hashの実装識別を分離 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-02 | FCIのPAG端点、CPDAG不確実性、潜在MAG、temporal lag/directionをGraph種別ごとに忠実保持する。未確定Graphから自動的にDAGや点効果を生成してはならない | SPLIT | 因果Graphの部分識別と端点・時間的な不確実性を保持し、未確定関係を確定因果関係へ暗黙変換しない | 10_31 AR・21 LDD・22 BD | PAG/CPDAG/FCI等の科学的適用Scopeは保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-03 | Estimand・Design・Graph・仮定を用いたIdentificationとEstimator eligibilityを分離し、不適格・非識別を数値推定の成功に変換してはならない | REWRITE_RD | 因果効果の識別可能性と推定手法の適格性を個別に判定し、不適格時に推定成功として扱わない | 10_31 AR | Estimand/Designとの連結定義は科学契約 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-04 | Phase1で単一Mediator・限定線形条件のFrontdoor数値効果（FD-A）を識別と推定の別結果として提供する | SPLIT | 承認済みFrontdoor条件下で因果効果を識別・数値推定できる | 10_32 Method Scope・22 BD | FD-AのMediator数・線形仮定は科学的制約で保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-05 | Random Common CauseおよびBootstrap Refutationを方法別に提供し、既存Placebo/Subsettingを回帰保護する | SPLIT | 因果推定結果に対し、承認済みの複数の反証・頑健性評価を実行できる | 10_32 Method Scope・22 BD | Random Common Cause/Bootstrap提供義務を別管理 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-06 | 実在するNCE/NCOを研究者が明示opt-inしたときのみ条件付きnull分析を行い、DAG/時間適格性、null結果、非適格理由を出す | SPLIT | 適格なNegative Controlが明示指定された場合に限りNull関連の妥当性を評価し、不適格理由を示す | 10_31 AR・10_32 Method Scope・22 BD | NCE/NCOと時間・Graph適格条件は保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-07 | 古典OLSに限定してpartial R²とpoint RV(q=1)を提供し、IPW/AIPW/CATEへ無根拠に一般化しない | SPLIT | 承認済みの回帰モデルに対する未観測交絡感度を定量評価し、非対応Estimatorへ適用を拡張しない | 10_31 AR・10_32 Method Scope・22 BD | OLS partial R²/RV(q=1)を採用Scopeで保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-08 | IPTW/IPW/AIPWの重み種別、Hájek正規化、clipping/trimming、overlap/ESS/balance、推論適格性を区別し診断する | SPLIT | 重み付き因果推定の不安定性・支持域・標本損失・推論適格性を定量診断できる | 10_31 AR・10_32 Method Scope・22 BD | Hájek/clipping/trimming/ESS等の方法契約保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-09 | Phase2の非IV CATE7 MethodについてEffect ModifierとConfounder、target population、crossfit/支持域・推論availabilityを明示する | SPLIT | 条件付き効果推定において効果修飾因子・交絡調整因子と推定対象集団を区別し、推論可否を示す | 10_31 AR・10_32 Method Scope・22 BD | 7 CATE Methodの採用Scopeは保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-10 | DRIV-Aをconditional IV structural slopeとして非IV CATEおよびcomplier LATEと異なるEstimand familyで扱う | REWRITE_RD | 条件付きIV構造係数をCATEおよびcomplier LATEと区別して扱う | 10_31 AR・10_32 Method Scope | DRIV-Aの承認済みEstimand識別を保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-11 | Exploratory point-onlyとConfirmatory inferenceを分離し、個票CATEのアクセス・export・supportを検証可能に制限する | SPLIT | 探索的な点推定と確認的推論を区別し、個人別推定結果の利用・出力を制限する | 10_31 AR・22 BD・23 IF | point-onlyと個票privacy契約は保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-12 | PCMCI/PCMCI+/LPCMCIのTemporal Graph、lag、CI-testと適用条件・不適格状態を保持する | SPLIT | 時系列上の因果関係を遅れと方向の不確実性を含めて表現し、適用条件を検証できる | 10_32 Method Scope・21 LDD・22 BD | PCMCI/PCMCI+/LPCMCIは採用Scopeで保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-13 | DiD、Event Study、ITSでtime intervention、pretrend、aggregation、cluster/autocorrelation、Method別CI適格性を検査する | SPLIT | 介入時点を伴う時系列準実験の前提・事前傾向・誤差構造と推論可否を診断できる | 10_31 AR・10_32 Method Scope・22 BD | DiD/Event Study/ITSの採用範囲を保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-14 | Sharp/Fuzzy RDでcutoff、bandwidth、density/first-stage条件とlocal effectのEstimandを保持する | SPLIT | 閾値による局所因果効果の推定に必要な適格性を検証し対象効果を明示できる | 10_31 AR・10_32 Method Scope・22 BD | Sharp/Fuzzy RDとcutoff/bandwidth等を保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-15 | 二値Z/AのB0 complier LATEとB1 linear IV structural slopeを別名で表し、Wald比/2SLS、weak-IV ARの型付き集合を保持する | SPLIT | complier LATEと線形IV構造係数を区別し、弱操作変数の下でも妥当な推論集合を表現できる | 10_31 AR・10_32 Method Scope・21 LDD・22 BD | B0/B1/Wald/2SLS/AR集合の科学的区別を保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-16 | SCM/SDIDのdonor適格性、pre-fit、汚染、placebo、time window、Method別推論を保存する。初期SCMはpoint-onlyとする | SPLIT | 比較対象群の妥当性や介入前適合性を診断し、手法ごとに許可された推定・推論結果を示す | 10_31 AR・10_32 Method Scope・22 BD | SCM/SDIDとSCM point-onlyを保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-17 | local CLIから科学的な失敗・nonidentification・method unavailableを技術的実行失敗と区別したversioned ResultとManifestを生成する | SPLIT | CLI分析結果について科学的な非識別・不適格・利用不可と技術障害を区別し、再現可能な成果物を得られる | 21 LDD・23 IF・30 DD | Manifestの物理SchemaとCLI終了契約 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-18 | Effect point・uncertainty availability・科学的受入状態は独立し、AR setのbounded/unbounded/disconnected/ALL_REALを損失なく表す | SPLIT | 点効果・区間推論の可用性・科学的受入状態を区別し、非標準形状の推論集合も損失なく表せる | 10_31 AR・21 LDD・23 IF | AR集合の4形状は科学・形式契約で保持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-F-19 | E11新Methodを旧&#96;causal-analysis-spec/2&#96;へ暗黙適用せず、旧Product/v2のREQUIRES_REVIEWとoverride契約を変更しない | REWRITE_RD | 既存Product因果分析と新しいCLI分析は暗黙に混在せず、旧仕様・既存のレビュー統制を維持する | 23 IF・22 BD | 旧spec/2・overrideの既存互換義務を保持 | MUST NOT | DRAFT | UNVERIFIED | ENH-E11 |

## 2. E11-N (8 candidates)

| ID | 原文（正本 / 草案） | Disposition | RD側の要件核・暫定改訂文 | 下位文書・保持先 | 判定根拠 | Level | Requirement Status | Implementation Status | Delivery |
|---|---|---|---|---|---|---|---|---|---|
| E11-N-01 | local input/outputのcanonical hash、version、effective backend/library、seed/split、input/output SHA、upstream referenceをManifestへ記録する | SPLIT | CLI実行の入出力と実効解析環境を追跡・検証し同じ条件を再現できる | 21 LDD・23 IF・30 DD | hash/SHA/seed/Manifest項目 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-02 | File publishはstaging→validate→atomic commitを基本とし、失敗時にpartial成功を正本扱いしない | SPLIT | 成果物の公開失敗時に部分的結果を正本として扱わない | 22 BD・30 DD | staging/atomic commit方式 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-03 | untrusted path、symlink、traversal、任意pickle/import、個票exportを明示的に検証し不正入力を拒否する | SPLIT | 不正なファイル参照・実行内容・個票出力を防止できる | 22 BD・23 IF・30 DD | symlink/traversal/pickle等の具体防御 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-04 | Optional Backend欠落は該当CapabilityのみUNAVAILABLEとし、core/legacyを停止しない | SPLIT | 分析Backendが利用不能でもCLIの基本機能と既存機能が稼働し、Unavailable理由を特定できる | 22 BD・23 IF | Profileとimport分離方式 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-05 | &#96;pyproject.toml&#96;でoptional extrasを宣言しuniversal &#96;uv.lock&#96;と実効APIを検証する | SPLIT | 任意の分析機能を再現可能で検証済みの依存関係から導入できる | 22 BD・30 DD・検証計画 | pyproject extras/universal uv.lockは承認済方式 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-06 | GPL系Backendを含む顧客別の配布は、納入artifact・ライセンスの個別Legal Gateを通るまでBLOCKする | KEEP_RD | GPL系Backendを含む顧客別の配布は、納入artifact・ライセンスの個別Legal Gateを通るまでBLOCKする | — | 能力・科学的制約・品質または受入結果を規定 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-07 | Gate07定量比較では全mandatory Kの事前登録、Gate-wide FWER=.05、Method別R/MC誤差とcompute budgetを固定する | SPLIT | 分析性能と統計的妥当性について事前定義された独立の受入検証を実施できる | 10_32 Scientific Acceptance・検証計画 | FWER=.05とK/R/MCの承認条件を維持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-N-08 | 旧&#96;causal-analysis-spec/2&#96;、E9/E10、Product API/UI/Worker/DBの回帰を守る | SPLIT | 新しいCLI機能によって既存因果分析仕様・Product機能の挙動を損なわない | 22 BD・回帰試験計画 | 旧spec/2・E9/E10保護範囲を維持 | MUST | DRAFT | UNVERIFIED | ENH-E11 |

## 3. E11-A (7 architecture candidates, NOT scientific AR)

| ID | 原文（正本 / 草案） | Disposition | RD側の要件核・暫定改訂文 | 下位文書・保持先 | 判定根拠 | Level | Requirement Status | Implementation Status | Delivery |
|---|---|---|---|---|---|---|---|---|---|
| E11-A-01 | Question/Design/Estimand/Graphおよび科学的statusのauthorityは外部engineではなくAriadne Domainに置く | MOVE_BD | Domainが研究条件・Estimand・科学状態の意味を規定する設計原則として保持 | 22 BD・ADR | Domain authorityの責務境界 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-02 | Scientific Adapterで外部Libraryとnormalized input/resultを隔離し、Backend objectをpersistent Domainへ渡さない | MOVE_BD | 外部分析LibraryとのAdapter分離契約として保持 | 22 BD・30 DD・ADR | backend objectをDomain正本に渡さない | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-03 | Identification→eligibility→estimator→inference順のfail-closed connectionを実装する | SPLIT | 識別・適格性・推定・推論の不成立を検出し、不正な成功結果を返さない | 22 BD・30 DD・ADR | fail-closed実行順序の構造 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-04 | New local versioned spec/result/manifestはProduct DB/Executionのcanonical authorityと独立させる | MOVE_BD | Local CLIとProductの永続正本を分離する設計制約として保持 | 21 LDD・22 BD・ADR | Product DB/Executionとの物理責務 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-05 | ConfidenceSet、negative result、scientific statusをtyped schemaで表現する | SPLIT | 推論集合・科学的負結果・科学状態を損失なく表現できる | 21 LDD・23 IF・ADR | typed schemaの設計形式 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-06 | Method×Backend profile/API/version/lock及びSBOMを実効検証可能にする | SPLIT | 利用する方法・Backend・依存版を再現・検証できる | 22 BD・30 DD・ADR | profile/API/version/lock/SBOMの物理管理 | MUST | DRAFT | UNVERIFIED | ENH-E11 |
| E11-A-07 | 新E11 Methodのためだけに既存Product Web/API/Worker/DB/migrationを変更しない | MOVE_BD | E11の提供対象をCLIのみに制限する承認済スコープ境界として保持 | 22 BD・ADR・10_90 Scope | Product Web/API/Worker/DB migration禁止 | MUST NOT | DRAFT | UNVERIFIED | ENH-E11 |
