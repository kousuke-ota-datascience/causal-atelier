# ENH-E11 — Formal Requirement Publication Candidate (RD)

**文書状態:** `WORKING_DRAFT / OWNER_SEMANTIC_POLICY_APPROVED / FORMAL_PUBLICATION_PENDING`. 本文の仮ID・候補Schema/Port/classは正式なFR/NFR/AR、ADR、Gate Freezeではない。Owner決定DEC01〜09を変更せず詳細化する。

## 1. 改定原則と現行要件との関係

現行正本の最終既知番号はFR-184、NFR-028、AR-027（文書中の最大参照値であり**空き番号・採番予約の証明ではない**）。本書の`E11-F-*` / `E11-N-*` / `E11-A-*`は**今回草案内のみに有効な仮ID**である。既存FR-040/041/042/046/047/048/049/050/054、NFR-002/028等は変更履歴付きで保持し、既存Productのimplementation statusを変更しない。

## 2. 機能要件（正式ID未発行）

| Draft ID | Level | 規範的な要件文（案） | 原則・対象Scope | Trace |
|---|---|---|---|---|
| E11-F-01 | MUST | Local Question、Design、Graph、Datasetはversionおよびcontent hashで同定し、上流条件が異なる推定の暗黙再利用を拒否する | P1 local identity / M2 | #15,#24 |
| E11-F-02 | MUST | FCIのPAG端点、CPDAG不確実性、潜在MAG、temporal lag/directionをGraph種別ごとに忠実保持する。未確定Graphから自動的にDAGや点効果を生成してはならない | GRAPH-A / D06 | #17,#20 |
| E11-F-03 | MUST | Estimand・Design・Graph・仮定を用いたIdentificationとEstimator eligibilityを分離し、不適格・非識別を数値推定の成功に変換してはならない | D04-E2 / D06 | #16,#22 |
| E11-F-04 | MUST | Phase1で単一Mediator・限定線形条件のFrontdoor数値効果（FD-A）を識別と推定の別結果として提供する | P1-08 FD-A | #16 |
| E11-F-05 | MUST | Random Common CauseおよびBootstrap Refutationを方法別に提供し、既存Placebo/Subsettingを回帰保護する | P1 Refutation | #16 |
| E11-F-06 | MUST | 実在するNCE/NCOを研究者が明示opt-inしたときのみ条件付きnull分析を行い、DAG/時間適格性、null結果、非適格理由を出す | DEC06限定N | #16 |
| E11-F-07 | MUST | 古典OLSに限定してpartial R²とpoint RV(q=1)を提供し、IPW/AIPW/CATEへ無根拠に一般化しない | DEC06限定N | #16 |
| E11-F-08 | MUST | IPTW/IPW/AIPWの重み種別、Hájek正規化、clipping/trimming、overlap/ESS/balance、推論適格性を区別し診断する | P1 quality | #19 |
| E11-F-09 | MUST | Phase2の非IV CATE7 MethodについてEffect ModifierとConfounder、target population、crossfit/支持域・推論availabilityを明示する | D05非IV7 | #18 |
| E11-F-10 | MUST | DRIV-Aをconditional IV structural slopeとして非IV CATEおよびcomplier LATEと異なるEstimand familyで扱う | DEC02 DRIV-A | #18 |
| E11-F-11 | MUST | Exploratory point-onlyとConfirmatory inferenceを分離し、個票CATEのアクセス・export・supportを検証可能に制限する | D05 / privacy | #18,#24 |
| E11-F-12 | MUST | PCMCI/PCMCI+/LPCMCIのTemporal Graph、lag、CI-testと適用条件・不適格状態を保持する | P3 temporal | #20 |
| E11-F-13 | MUST | DiD、Event Study、ITSでtime intervention、pretrend、aggregation、cluster/autocorrelation、Method別CI適格性を検査する | DEC05 quasi | #21 |
| E11-F-14 | MUST | Sharp/Fuzzy RDでcutoff、bandwidth、density/first-stage条件とlocal effectのEstimandを保持する | DEC05 quasi | #22 |
| E11-F-15 | MUST | 二値Z/AのB0 complier LATEとB1 linear IV structural slopeを別名で表し、Wald比/2SLS、weak-IV ARの型付き集合を保持する | DEC01 / D03 | #22 |
| E11-F-16 | MUST | SCM/SDIDのdonor適格性、pre-fit、汚染、placebo、time window、Method別推論を保存する。初期SCMはpoint-onlyとする | DEC05 quasi | #23 |
| E11-F-17 | MUST | local CLIから科学的な失敗・nonidentification・method unavailableを技術的実行失敗と区別したversioned ResultとManifestを生成する | E11 CLI-only | #24 |
| E11-F-18 | MUST | Effect point・uncertainty availability・科学的受入状態は独立し、AR setのbounded/unbounded/disconnected/ALL_REALを損失なく表す | G2-Bridge / D05 | #22,#24 |
| E11-F-19 | MUST NOT | E11新Methodを旧`causal-analysis-spec/2`へ暗黙適用せず、旧Product/v2のREQUIRES_REVIEWとoverride契約を変更しない | D04-V2/R2 | #24 |

## 3. 非機能要件（正式ID未発行）

| Draft ID | Level | 規範的な要件文（案） | Acceptance |
|---|---|---|---|
| E11-N-01 | MUST | local input/outputのcanonical hash、version、effective backend/library、seed/split、input/output SHA、upstream referenceをManifestへ記録する | 同一入力のreadback/差分検出 |
| E11-N-02 | MUST | File publishはstaging→validate→atomic commitを基本とし、失敗時にpartial成功を正本扱いしない | Crash/partial-write負例 |
| E11-N-03 | MUST | untrusted path、symlink、traversal、任意pickle/import、個票exportを明示的に検証し不正入力を拒否する | Security negative |
| E11-N-04 | MUST | Optional Backend欠落は該当CapabilityのみUNAVAILABLEとし、core/legacyを停止しない | 5 profile fresh --locked |
| E11-N-05 | MUST | `pyproject.toml`でoptional extrasを宣言しuniversal `uv.lock`と実効APIを検証する | Runtime + old regression |
| E11-N-06 | MUST | GPL系Backendを含む顧客別の配布は、納入artifact・ライセンスの個別Legal Gateを通るまでBLOCKする | Legal evidence |
| E11-N-07 | MUST | Gate07定量比較では全mandatory Kの事前登録、Gate-wide FWER=.05、Method別R/MC誤差とcompute budgetを固定する | DEC07 independent pilot and T3 |
| E11-N-08 | MUST | 旧`causal-analysis-spec/2`、E9/E10、Product API/UI/Worker/DBの回帰を守る | Regression suite |

## 4. Architecture requirements（正式ID未発行）

| Draft ID | Level | 規範的な要件文（案） | Decision |
|---|---|---|---|
| E11-A-01 | MUST | Question/Design/Estimand/Graphおよび科学的statusのauthorityは外部engineではなくAriadne Domainに置く | ARC09-01 |
| E11-A-02 | MUST | Scientific Adapterで外部Libraryとnormalized input/resultを隔離し、Backend objectをpersistent Domainへ渡さない | ARC09-02 |
| E11-A-03 | MUST | Identification→eligibility→estimator→inference順のfail-closed connectionを実装する | ARC09-03 |
| E11-A-04 | MUST | New local versioned spec/result/manifestはProduct DB/Executionのcanonical authorityと独立させる | ARC09-04 |
| E11-A-05 | MUST | ConfidenceSet、negative result、scientific statusをtyped schemaで表現する | ARC09-05 |
| E11-A-06 | MUST | Method×Backend profile/API/version/lock及びSBOMを実効検証可能にする | ARC09-06 |
| E11-A-07 | MUST NOT | 新E11 Methodのためだけに既存Product Web/API/Worker/DB/migrationを変更しない | ARC09-07 |

## 5. 現行§11の逐条変更候補

**Before（現行）:** `DoWhy / EconML等、ENH-E10でapprovedされていないexternal analytical engine追加`を対象外とする。

**After（E11 Working Copy案）:** 「ENH-E10に承認されない外部分析EngineのProduct必須依存化は対象外とする。ただしENH-E11でOwner採用されたlocal Scientific Core/CLIの**Method別Optional Backend（DoWhy/EconML/Tigramite/RD等）**は本除外からの限定例外とする。Productへの新方式統合、納入時のGPL等法務承認、実効Runtime/Science受入はこの例外により許可・完了とはならない。」

**FR-161との関係:** E10のPredictive optional engine契約をE11 Causal optional engineの正式ID・科学的受入根拠に転用しない。

## 6. Controlled Publicationに必要な証拠

1. 正本の全FR/NFR/AR ID連番・重複監査と新番号承認、既存条文の旧→新diff、Status/Demand/Deliveryの逐条レビュー。
2. 68 Scope行×41 Method×10 UC×Issue/ADR/Gateのmandatory trace（未対応行の明示）と、Scientific negativeの受入先。
3. Formal Requirement Ownerが新ID・条文・Source SHAを批准。独立Architecture Review / Gate Freezeは別イベント。

## 7. 追跡資料

- [03 要件意味差分](../../../03_requirements_revision.md)
- [04 Architecture改定方針](../../../04_design_revision.md)
- [DEC09 Owner承認](../../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- [Scope68](../../../00_04_phase1_to_phase3_cli_scope_proposal.md)
