# ENH-E11 — 8月4日Phase 1〜3構想と現行実装の三資料照合（ステップ3）

**文書区分:** 事前調査／歴史資料の要求差分判定（Workflow 01へ渡す補助証跡）  
**判定状態:** **SOURCE_RECONCILED（Phase別歴史要求の差分照合完了）**／実装スコープ・採否の正式承認前／固定SHAでの全件テスト未実施  
**調査日:** 2026-10-25（日本時間）  
**照合対象の現行Snapshot:** `prototype/ariadne_mvp` at `1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb`。正本要件：[10_requirements_definition.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/requirement_definition/10_requirements_definition.md)。  
**先行する工程1・2:** [9月末案の13項目照合](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/00_foundation_gap_reconciliation.md)／[残存Foundation Gap4領域](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/00_foundation_gap_closure_assessment.md)。  
**後続:** ステップ4での正式なCLI-only実装スコープ**案の確定**。本資料だけで新FR/NFR/ARを承認・改定しない。

## 0. INTRODUCTION

### 0.1. 本文書の目的

2026年8月4日のPhase 1〜3構想に掲げられた機能と実装指示を、**2026年9月末ENH-E11申し送り（当時の取り扱い）および2026年10月現在の正本要件・Scientific Core・CLI・既存テスト**へ照合する。8月に「これから実装する」とされた機能について、既存機能を二重に実装せず、現時点で必要な追加候補を特定する。

本書の「差分照合完了」とは、**歴史資料のPhase別要求・境界を項目別に分類した**意味であり、すべての新機能が正式採用された、または既存の科学的妥当性を最新SHAで再検証した意味ではない。

### 0.2. 本書を作成するに至った背景

8月案はIdentification-first、FCI/DoWhy、EconML CATE、Tigramite・準実験という広い構想だった。9月末のNotion `HANDOFF_DRAFT`は、既存ENH-E5〜E10の実装によってFoundation Gapの相当部分が消滅した可能性を踏まえ、**Foundation-onlyへ一旦範囲を絞り、Phase 2/3を将来送り**にした。後のオーナー方針は、Phase 1〜3の必須因果推論手法を**Scientific Core＋local CLI＋永続local file**に限ってENH-E11候補へ戻した。

これらは**異なる時点の決定**である。旧提案のAPI/Worker/UI/DB指示を新CLI-only方針へそのまま持ち込まず、9月末に除外したCATEや準実験を「以前から承認済みの現行FR」とも扱わない。

### 0.3. 本書が照合する内容

**照合の主資料はA0とA1〜A3の4件**。併せてB0（当時のAs-Is評価）を、8月時点の不足認識が現在と異なることの根拠として読む。A4（Phase 4）は対象外の境界確認にのみ使う。**上位A0に『必須』とあるだけでA1〜A3の実装範囲へ自動追加しない**。

| 資料ID | 歴史資料（固定SHA） | 役割 |
|---|---|---|
| `A0` | [01_required_causal_inference_lifecycle.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/01_required_causal_inference_lifecycle.md) | 全体構想／Phase上位の要求 |
| `A1` | [03_01_coding_instruction_Phase1.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_01_coding_instruction_Phase1.md) | Phase 1の実装指示 |
| `A2` | [03_02_coding_instruction_Phase2.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_02_coding_instruction_Phase2.md) | Phase 2の実装指示 |
| `A3` | [03_03_coding_instruction_Phase3.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_03_coding_instruction_Phase3.md) | Phase 3の実装指示 |
| `B0` | [02_AsIs_codebase_gap.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/02_AsIs_codebase_gap.md) | 2026年8月のコードギャップ評価。**現在のImplementation Statusとして採用しない** |
| `A4` | [03_04_coding_instruction_Phase4.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260804_causal_lifecycle_enhancement/03_04_coding_instruction_Phase4.md) | Phase 4への後続送りの境界確認専用。今回の方法別照合対象外 |

本書の68行（P1 21／P2 18／P3 19／上位・横断 10）について、歴史的要求、9月末扱い、現行根拠、暫定Disposition、次工程の判断を記録する。

### 0.4. 結論サマリ

- **再利用:** 既存Question/Design、DAG/CPDAG/PAG、PC/GES/LiNGAM/NOTEARS、Randomized/Backdoor Identification、Data Eligibility、ATE/ATTとIPW/AIPW、E9診断、既存Refutation/Sensitivity、Scientific CLI/Manifest。既存手法に対する過去のテスト・受入はある。
- **追加候補:** DoWhyのFrontdoor/IV識別、FCI、追加Refutation/Sensitivity、CATE/HTEとEconML、PCMCI系、DiD/Event/ITS、RDD、IV/LATE、Synthetic Control/SDID、手法別Design/Diagnostics/Artifacts。
- **後続へ送る旧実装媒体:** Phase別指示書にある**新機能のWeb UI/API/Worker/DB migration**。現行Product経路は削除せず、CLI-onlyで科学的に検証する。
- **上位構想との未整合:** ATC、matching/g-computation、追加negative control、複数検定等はA0に存在するがA1〜A3で独立した必須実装へ落ちていない。**controlled direct effect／mediationはA4 Phase4側の拡張領域と関連するため後続境界を維持する。** A0単独要求の採否を明示しなければ『Phase 1〜3の必須』という表現だけでは範囲が閉じない。
- **現行Foundation Gap:** GAP-C01〜C04は別工程で確定済み。新手法採用と既存Product要件解消を混同しない。
- **検証:** 今回はコード/テストの読取りと過去999の参照。**新たなpytest、全scientific benchmark、外部Library API互換性試験は未実施**。

## 1. 判定方法と証拠の読み方

### 1.1. 三資料の権限と時系列

1. **8月4日A0〜A3:** 将来構想と実装指示の**歴史的証拠**。現行Requirement、現行Gate 06/07ではない。
2. **9月末Notion:** [ENH-E11 Foundation Gap Completion](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)（`HANDOFF_DRAFT`）。当時のFoundation-onlyとPhase 2/3除外を保持。
3. **現行正本・ソース:** 既存FR/NFR/ARおよび指定SHAの実装・テストを、機能の有無・契約・未充足の判断の基準とする。
4. **現在のオーナー方針:** Phase 1〜3の必須技術をCLI-onlyで再検討する方向。個別手法・外部Library導入・要件改定・Gateは**未承認**。

9月末はPhase 1のDoWhy/FCIさえも**Requirement revisionで採用判断する候補**とし、Phase 2/3を後続へ送っていた。この歴史的判断を「当時採用済み」と上書きしない。

**旧As-Is評価の再ベースライン:** B0は当時IdentificationやRefutationを未実装、Graph semanticsを部分実装としていたが、現在の正本ではFR-037、FR-042〜050等が`IMPLEMENTED`で、対応するAdapterやBENCH1Aが存在する。したがってB0の`Critical/High/Medium`という**2026年8月時点の優先順位をENH-E11の現在の実装優先度として流用しない**。B0にあるg-computation等の記述も、現行Scientific CLIに独立した対応methodがあることを意味しない。

### 1.2. Dispositionと科学的品質を分ける

| 記号 | 意味 | 今回の判定でしてよいこと |
|---|---|---|
| **A** | `A_CURRENT_REQUIREMENT_GAP`：現行有効要件に対する残差 | 既存要求の未充足として別のGap台帳を参照。新機能の採用と区別 |
| **B** | `B_NEW_CAPABILITY_CANDIDATE`：新しい因果分析Capability | 要件semantic deltaの候補として追加。実装承認ではない |
| **C** | `C_SUPERSEDED`：旧構想の不足が既存実装で解消 | 再利用して保護。必要な科学的品質の追加検証は別に残せる |
| **D** | `D_FUTURE_PHASE`：現時点では後続扱い | 対象外理由と将来境界を記録 |
| **E** | `E_REJECT`：承認済み方針と矛盾し不採用 | 本調査で**科学的手法そのもの**にE確定はない |
| **B?** | A0だけの追加要求、Phase必須の帰属が未決 | ステップ4で「必須か／追加選択か／後続か」を明示判断するまで保留 |
| **C＋B / C＋品質確認** | 既存基盤を再利用し、不足部分のみ追加・品質検証 | 再実装と科学的検証を別扱い。正式なA/B/Cの内訳は要件承認時に分割 |

`B?`は正式なA〜E分類の**保留注記**であり、既に採用した第6の分類ではない。技術上の科学的妥当性の確認は別軸（`TEST_SOURCE_EXISTS`／`HISTORICAL_ACCEPTED`／`FRESH_RERUN_NOT_DONE`）とする。

### 1.3. 実装とテストを確認した参照点

| ID | ソース／テスト／過去999の参照 |
|---|---|
| `SPEC` | [src/ariadne/product/domain/analysis_spec.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/domain/analysis_spec.py) |
| `SPECVER` | [src/ariadne/product/domain/analysis_specification.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/domain/analysis_specification.py) |
| `GRAPH` | [src/ariadne/product/domain/graph_semantics.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/domain/graph_semantics.py) |
| `GRAPHVER` | [src/ariadne/product/application/graph_version_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/application/graph_version_service.py) |
| `DISC` | [src/ariadne/scientific/discovery/adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/scientific/discovery/adapter.py) |
| `IDENT` | [src/ariadne/scientific/identification/adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/scientific/identification/adapter.py) |
| `EST` | [src/ariadne/scientific/inference/adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/scientific/inference/adapter.py) |
| `REFUT` | [src/ariadne/scientific/refutation/adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/scientific/refutation/adapter.py) |
| `SENS` | [src/ariadne/scientific/sensitivity/adapter.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/scientific/sensitivity/adapter.py) |
| `VALID` | [src/ariadne/product/application/scientific_validation_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/application/scientific_validation_service.py) |
| `CLICONF` | [src/ariadne/interfaces/cli/config_schema.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/interfaces/cli/config_schema.py) |
| `CLIRUN` | [src/ariadne/interfaces/cli/scientific_stage.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/interfaces/cli/scientific_stage.py) |
| `MANIFEST` | [src/ariadne/interfaces/cli/manifest.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/interfaces/cli/manifest.py) |
| `LINEAGE` | [src/ariadne/product/application/lineage_query_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/application/lineage_query_service.py) |
| `CLOSURE` | [src/ariadne/product/application/product_closure_service.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/application/product_closure_service.py) |
| `IPW` | [src/ariadne/causal/inference/estimators/ipw.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/causal/inference/estimators/ipw.py) |
| `AIPW` | [src/ariadne/causal/inference/estimators/aipw.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/causal/inference/estimators/aipw.py) |
| `NAV` | [src/ariadne/product/application/navigation_catalog.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/src/ariadne/product/application/navigation_catalog.py) |
| `BENCH1A` | [tests/scientific_benchmarks/test_enh_e1a_acceptance.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/tests/scientific_benchmarks/test_enh_e1a_acceptance.py) |
| `BENCH1` | [tests/scientific_benchmarks/test_enh_e1_benchmarks.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/tests/scientific_benchmarks/test_enh_e1_benchmarks.py) |
| `CLITEST` | [tests/product/test_cli_contract.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/tests/product/test_cli_contract.py) |
| `E9TEST` | [tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py) |
| `E9G04` | [docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G04/Trial01/ENH-E9-G04_01__999_gate_decision.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G04/Trial01/ENH-E9-G04_01__999_gate_decision.md) |
| `E9G05` | [docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/1d67b2a56f97bf16d953e4a6b6ce76ee37102bfb/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md) |

**照合の範囲:** ソースの主要Scientific Adapter、Domain Graph/Spec、CLI設定/Manifestと指定テスト、正本のImplementation Status。FCI/DoWhy/EconML/Tigramite/準実験の「現行CLIに未登録」は該当するregistryとSpecの不在に基づく。**全リポジトリに同等機能が一切ない**、あるいは最新科学的受入試験にすべて合格した、とは断定しない。

## 2. Phase 1 — 基盤と識別／探索

### 2.1. Phase 1実装指示と現行実装の照合

| ID | 8月4日の要求（出典） | 9月末での扱い | 現行要件・実装の根拠 | Disposition | 差分と後続判断 |
|---|---|---|---|---|---|
| P1-01 | Causal Questionのpopulation/treatment/outcome/estimand等（A1§2/3） | Foundation候補 | FR-040 IMPLEMENTED。SPEC／SPECVERに定義と固定がある | C 再利用 | 既存Question snapshotを基準にし、仕様変更なら差分定義 |
| P1-02 | 独立したCausalQuestionおよびVersion resource（A1§3.1） | Foundation候補 | SPECVERのAnalysisSpecification versionはある。独立QuestionVersionの同一性は未確定 | B 新規候補 | 独立resourceが必要か、既存Spec versionで足りるかArchitecture Reviewで判断 |
| P1-03 | Causal Design／Target Trial要素（A1§2、A0§2.2） | Foundation候補 | FR-041 IMPLEMENTED。assignment/time zero/eligibility/assumptionsあり（SPEC） | C＋B? | 既存Design再利用。follow-up等の独立version追加は明示的要件差分待ち |
| P1-04 | DAG／CPDAG／PAGとTAIL/ARROW/CIRCLE（A1§3.2） | Foundation候補 | FR-037 IMPLEMENTED。GRAPH／GRAPHVER、BENCH1A | C 再利用 | 既存Graph semanticsを保護。PAGがFCI出力であることは別 |
| P1-05 | Graph provenance／制約／編集・再固定（A1§3.2、A0§2.4） | Foundation候補 | FR-036/038/039 IMPLEMENTED。GRAPHVERにderived editとsource | C＋B? | CONSENSUS等旧全enum・bootstrap edge probabilityの差は承認候補に分離 |
| P1-06 | Randomized／Backdoor Identification、非識別status（A1§3.3/7） | Foundation候補 | FR-042/043/046、AR-005/010/023 IMPLEMENTED。IDENT／VALID／BENCH1A | C 再利用 | Graph reviewと負結果を維持。PARTIALLY_IDENTIFIEDの使用全件は未認定 |
| P1-07 | DiscoveryなしでUser-defined/Imported Graphから開始（A1§8/13） | Foundation候補 | FR-036 IMPLEMENTED。SPEC／IDENTにGraph入力 | C 再利用 | 既存CLIの非Discovery経路を回帰で守る |
| P1-08 | DoWhyのBackdoor／Frontdoor／IV、識別失敗の正規化（A1§5） | 要件改定後のみ候補 | IDENTのstrategyはNative Randomized／Backdoor。DoWhy専用adapterなし | B 新規候補 | 方法別の識別式、仮定、負結果、optional versionを新要件化 |
| P1-09 | FCI、潜在交絡下のPAG Discovery（A1§6） | 要件改定後のみ候補 | DISCはPC/GES/LiNGAM/NOTEARSのみ。GRAPHはPAGを表現可能 | B 新規候補 | FCI結果のCIRCLE endpoint、latent-confounder warning、CI testを契約化 |
| P1-10 | Data EligibilityとScientific Validation gate（A1§7、A0§2.6） | Foundation候補 | FR-044/045/046 IMPLEMENTED。IDENT／VALID、BENCH1A | C 再利用 | 新Designに固有のpanel/time/IV/RD eligibilityはBとして追加 |
| P1-11 | ATE／ATT推定と区間（A0§2.7/2.8） | Foundation候補 | FR-047 IMPLEMENTED。ESTはdiff/OLS/IPW/AIPWとATE/ATT | C 再利用 | 既存の推定対象を再実装しない |
| P1-12 | IPW/AIPW・Overlap/Balance/ESS/Weight診断（A0§2.9） | Foundation候補、E9充足 | FR-048 IMPLEMENTED。EST／IPW／AIPW／E9G04／E9TEST | C＋品質確認 | E9の手法適用性を保護。IPW推定Propensity下のSE/CI被覆は未認定 |
| P1-13 | Placebo Treatment／Data Subset Refutation（A1§5.2） | Foundation候補 | FR-049 IMPLEMENTED。REFUT／BENCH1A | C 再利用 | 新Refuterの導入を理由に既存2手法を置換しない |
| P1-14 | Random Common Cause／Bootstrap Refutation（A1§5.2） | 承認された追加のみ | REFUTのmethodはPlacebo/Data Subset。該当method未登録 | B 新規候補 | 効果再推定の摂動・seed・負結果・可用backendを契約化 |
| P1-15 | Negative Control exposure/outcome・Simulated Confounder等（A0§2.10；A1§5.2のextension） | 旧Foundation-onlyでは自動採用しない | REFUTに専用methodなし。Phase1ではnegative controlはモデルのextension | B? 上位要求 | A0には『必須refuter』と記載、A1では実装必須列挙外。採否・方法論を明示審議 |
| P1-16 | Adjustment Set／Propensity Clipping Sensitivity（A0§2.11） | Foundation候補 | FR-050 IMPLEMENTED。SENS／BENCH1A | C 再利用 | 2軸の正規出力を維持 |
| P1-17 | Unobserved-confounder等の追加Sensitivity（A0§2.11） | 承認された追加のみ | SENSのdimensionはAdjustment/Clippingのみ | B? 上位要求 | 測定可能性・結論反転thresholdと補助分析法を別途決定 |
| P1-18 | Result/Artifact/Manifest／Question・Graph・識別来歴（A1§10） | Foundation残差 | FR-008/054/095、NFR-001b/002 PARTIAL。MANIFEST／LINEAGE／CLOSUREに一部機構 | A 現行Gap | GAP-C02/C03のProduct canonical要件とCLI-only新Manifestを区別 |
| P1-19 | API／Worker／DB migration／RBAC統合（A1§9/11） | 9月末当初は残差確認、現方針で新規統合を後続へ | 既存Product API/Worker/DB経路は存在。新機能統合の正本要件は未承認 | D 後続対応 | 旧Phase1の実装媒体指示を新機能へそのまま適用しない |
| P1-20 | CLI Identify／Refute／Sensitivity、local Artifact（A1§9/10） | Foundation候補 | CLICONF／CLIRUN／CLITESTで既存CLIが存在 | C＋B 新方式 | CLI基盤は再利用。新手法設定・artifact schemaはB |
| P1-21 | Scientific synthetic benchmark／非識別・overlap負例（A1§12/13） | 既存Gate再利用を指示 | BENCH1A／BENCH1には現行方法のknown-truth試験。FCI/DoWhyは対象外 | C＋B 検証 | 新方式は独立known-truthと負例を追加。既存テストを新方式のPASSとしない |

### 2.2. Phase 1特有の誤判定を避ける

- **GraphのPAG表現（C） ≠ FCI探索の実装（B）。** CPDAG/PAGを暗黙にDAGへ変換しない。
- **Native Backdoor（C） ≠ DoWhy Frontdoor/IV（B）。** DoWhyを入れても仮定の真偽は保証されない。
- **既存ATE/ATT＋E9 Diagnostics（C） ≠ IPTWの全推論ケースでCI被覆が保証（品質確認）。** BENCH1Aのrandomized diff estimator試験をIPWの全推論の証明としない。
- **既存2種Refutation/2種Sensitivity（C） ≠ A0のすべての追加Refuter/Sensitivity（B?）。** 上位A0とPhase1指示A1で強さが異なる。
- **Product canonical lineageのPARTIAL（A） ≠ E11 CLI-only Manifestの新仕様（B）。** GAP-C02/C03は別の権威が必要。

## 3. Phase 2 — 異質処置効果・EconML

### 3.1. Phase 2実装指示と現行実装の照合

| ID | 8月4日の要求（出典） | 9月末での扱い | 現行要件・実装の根拠 | Disposition | 差分と後続判断 |
|---|---|---|---|---|---|
| P2-01 | 第一級CATE/HTE estimandとeffects modifiers（A2§3） | Phase2除外 | SPECはATE/ATT、ESTもATE/ATTのみ | B 新規候補 | ATE/ATTとの対象・条件付け・標準出力の区別 |
| P2-02 | LinearDML（A2§2/5） | Phase2除外 | EST／CLICONFにEconML methodなし | B 新規候補 | continuous/binary処置互換、cross-fitting、SE/CI、負例 |
| P2-03 | CausalForestDML（A2§2/5） | Phase2除外 | EST／CLICONFにCausalForestDMLなし | B 新規候補 | 異質効果・森林sample support・uncertainty |
| P2-04 | DRLearner（A2§2） | Phase2除外 | AIPWはあるがDRLearner契約なし | B 新規候補 | 既存AIPWとCATE推定を混同しない |
| P2-05 | ForestDRLearner（A2§2） | Phase2除外 | ESTにmethodなし | B 新規候補 | forestとDR nuisance及び推論の制約 |
| P2-06 | S-Learner（A2§2） | Phase2除外 | Scientific Estimation registryに専用methodなし | B 新規候補 | CATE意味・effect modifiers・適用条件 |
| P2-07 | T-Learner（A2§2） | Phase2除外 | Scientific Estimation registryに専用methodなし | B 新規候補 | arm別support・過学習と比較可能性 |
| P2-08 | X-Learner（A2§2） | Phase2除外 | Scientific Estimation registryに専用methodなし | B 新規候補 | 非対称arm・pseudo-outcome等の条件 |
| P2-09 | DRIVまたは科学的に同等なIV+ML（A2§2） | Phase2除外 | IDENTに現行IV識別なし。ESTにもIV+MLなし | B 新規候補 | Phase1識別IV・Phase3 LATEとの差と同等条件を定義 |
| P2-10 | EstimationSpecification／HeterogeneityResult（A2§3） | Phase2除外 | SPECのEstimand ATE/ATT、ESTに専用Resultなし | B 新規候補 | nuisance/final、effect modifier、CI、subgroupを契約化 |
| P2-11 | Capability validation／optional backend隔離（A2§4/5/6） | Phase2除外 | VALIDは旧estimatorsのみ。NFR-028既存原則はIMPLEMENTED | B＋C原則再利用 | EconML・SKLearn依存隔離、実効版、利用不能status |
| P2-12 | Cross-fittingのfold／seed／split・group/time leakage（A2§5） | Phase2除外 | AIPWには部分的cross-fitting。CATE固有のsplit artifact契約なし | C部分＋B | 既存AIPWを再利用し、CATE固有のnuisance・fold・partitionを追加 |
| P2-13 | 適格性：post-treatment・sample・overlap・IVなど（A2§6） | Phase2除外 | IDENT／VALIDに現行方法向け検証あり | C部分＋B | CATEのeffect modifier、instrument、forest、小sample等を追加 |
| P2-14 | CATE support／calibration／stability／uncertainty（A2§7） | Phase2除外 | EST/E9はATE向けDiagnostics。CATE固有のcalibrationなし | B 新規候補 | Known-truth/poor-overlapとcalibration、group支持集合 |
| P2-15 | CATE Parquet・group summary・PII制約（A2§8） | Phase2除外 | MANIFESTにはlocal artifact基本形。個票CATE schemaなし | B 新規候補 | unsafe export禁止、unit IDとsupport、checksumを定義 |
| P2-16 | Benchmarks：bias/RMSE/coverage/runtime（A2§10/11） | Phase2除外 | BENCH1AはATE/ATT中心、CATE methodのknown truthなし | B 新規検証 | constant/linear/nonlinear heterogeneity、valid/weak IV、poor overlap |
| P2-17 | 最低4 estimator family共通契約（A2§12） | Phase2除外 | 既存Scientific estimator contractはATE/ATTのみ | B 新規候補 | 8月の『4 family以上』だけで必須列挙8行を黙って削らない |
| P2-18 | EconML向けAPI/UI/Worker/DB・paged retrieval（A2§8/9/13） | Phase2除外 | 旧Product interfacesあり、新CATEのAPI/DBはなし | D 後続対応 | CLI-onlyなので個票CATEは安全なlocal fileへ。Product RBAC統合は後続 |

### 3.2. Phase 2の科学的な受入単位

- CATE/HTEは単なるsubgroupの**予測精度**ではなく、条件付き介入効果のEstimandである。識別・positivity・time leakageの制約を保持する。
- 旧A2の**8手法群の列挙**と「4以上の主要Estimator familyを同一契約で実行」のAcceptance Criteriaは同一ではない。**後者を理由に前者を縮小しない**。承認する方法一覧と同等実装の条件をステップ4で決定する。
- IPW/AIPWとの重複部分は再利用するが、AIPWが存在することはDRLearner/ForestDRLearner/CausalForestDMLの存在証明にならない。
- 個票CATEのローカル出力はprivacy・suppression・アクセス条件の審査対象。旧A2のpaged APIやWorker内object所有はCLI-only方針へそのまま移行しない。
- 既存BENCH1AのATE known-truth試験を、CATEのsupport/calibration/CI coverageの科学的PASSとして転用しない。

## 4. Phase 3 — 時系列因果と準実験デザイン

### 4.1. Phase 3実装指示と現行実装の照合

| ID | 8月4日の要求（出典） | 9月末での扱い | 現行要件・実装の根拠 | Disposition | 差分と後続判断 |
|---|---|---|---|---|---|
| P3-01 | TemporalDesign／TIME_SERIES_GRAPH／lag/endpoint（A3§3/4） | Phase3除外 | GRAPHのDAG/CPDAG/PAGが存在。時間専用GraphTypeなし | B 新規候補 | lagと同時点及びLPCMCI uncertaintyを第一級化 |
| P3-02 | PCMCI（A3§2.1/4） | Phase3除外 | DISCにPCMCIなし | B 新規候補 | 既知lag・stationarity・CI-testで検証 |
| P3-03 | PCMCI+（A3§2.1/4） | Phase3除外 | DISCにPCMCI+なし | B 新規候補 | 同時点edgeと向き・入力制約 |
| P3-04 | LPCMCI（A3§2.1/4） | Phase3除外 | DISCにLPCMCIなし | B 新規候補 | 潜在交絡と時間端点の不確実性を保持 |
| P3-05 | CI-test registry：ParCorr/robust/nonlinear等（A3§2.1） | Phase3除外 | DISCのPC独立性検定設定はあるがTemporal CI registryなし | C一部＋B | Library提供範囲とdata type互換性を確定 |
| P3-06 | Time index／missing／duplicate／lag／stationarity Validation（A3§4） | Phase3除外 | IDENTは横断データのeligibilityを提供。Temporal専用検証なし | B 新規候補 | time leakage・irregular timestampsの負例 |
| P3-07 | DiD（A3§2.2/5） | Phase3除外 | ESTはATE/ATTの4methodのみ、DiD登録なし | B 新規候補 | parallel-trend、timing、cluster、staggered |
| P3-08 | Event Study（A3§2.2/5） | Phase3除外 | Event-time estimand／coefficients出力なし | B 新規候補 | event supportとpretrend、staggered bias警告 |
| P3-09 | Interrupted Time Series（A3§2.2） | Phase3除外 | ITS専用Design/Estimatorなし | B 新規候補 | 介入時点、自己相関、seasonalityとcounterfactualを定義 |
| P3-10 | Sharp RDD（A3§6） | Phase3除外 | Running variable/cutoff schemaなし | B 新規候補 | local estimand、bandwidth感度、density |
| P3-11 | Fuzzy RDD（A3§6） | Phase3除外 | Compliance/first-stageとFuzzy schemaなし | B 新規候補 | local Wald等の識別とfirst-stage不成立 |
| P3-12 | IV／LATE（A3§7） | Phase3除外 | IDENTはNative Backdoor、LATE estimandなし | B 新規候補 | relevance/exclusion/monotonicity/weak-IVを分ける |
| P3-13 | Synthetic Control（A3§8） | Phase3除外 | donor-weightの推定器がScientific CLIにない | B 新規候補 | pre-fit／placebo-in-space/time／RMSPE |
| P3-14 | Synthetic Difference-in-Differences（A3§8） | Phase3除外 | Synthetic DiD methodなし | B 新規候補 | panel balance、donor選択、重みの意味を分離 |
| P3-15 | QuasiExperimentalDesignと方法固有の識別仮定（A3§3） | Phase3除外 | SPEC/VALIDは旧横断的CausalDesignのみ | B 新規候補 | IV/RD/DiD/Synthごとの必須fields・negative statuses |
| P3-16 | 手法別Diagnostics／known-truth tests（A3§5〜12） | Phase3除外 | BENCH1Aは現行ATE/Identification。専用Design試験なし | B 新規検証 | pretrend・density・weak-IV・donor・lagの成功/失敗fixture |
| P3-17 | Temporal Graph／effect report／file Artifact（A3§9） | Phase3除外 | MANIFEST/CLIRUNは基本のlocal成果物のみ | C基盤＋B | Graph/lag/event-study/first-stage/RMSPEのschemaを追加 |
| P3-18 | RPCMCI／J-PCMCI+ extension（A3§2.1） | 当時対象外 | A3自身が初期実装の必須から除外 | D 後続対応 | Phase3必須メソッドに含めない |
| P3-19 | Quasi-experimental API/UI/DB・migration（A3§10/13） | Phase3除外 | 新DesignのProduct統合なし。旧Product環境は現存 | D 後続対応 | 旧媒体指示を新CLI-only Phase3の完了条件にしない |

### 4.2. Phase 3の科学的な受入単位

- **Temporal Graph ≠ 横断DAG。** lag、同時点endpoint、time indexとLPCMCIの潜在交絡の可能性を正規schemaで保存する。
- **DiD/Event Study/ITSは異なる識別デザイン。** 単純TWFEだけでstaggered adoptionを網羅せず、ITSの介入前後比較をDiDの比較群付き推定と同一視しない。
- **RDD／IV／LATEは局所的・complier等の対象が異なる。** LATEをATEと記録せず、manipulation・weak-IVの科学的negative caseを検証する。
- **Synthetic donor重み ≠ IPTWの処置重み。** donor汚染、pre-fitとplaceboの妥当性を独立に確認する。
- RPCMCI/J-PCMCI+はA3自体でextension候補・初期必須対象外。Phase4 Policy/Monitoringと合わせて後続送りを維持する。

## 5. A0上位構想とPhase実装指示との未整合

### 5.1. Phase 1〜3に自動算入してはならない追加要求

| ID | 8月4日A0の記載 | 9月末での扱い | 現行要件・コードとの対応 | Disposition | ステップ4での判断 |
|---|---|---|---|---|---|
| X-01 | A0§2.3：ATC／controlled direct effect | 上位構想とPhase4に跨る | SPECはATE/ATTのみ | B? ATC／D direct effect（Phase4） | ATCはPhase別実装指示に必須指定なし。controlled direct effectはA4のmediation拡張領域と関連し後続境界を維持 |
| X-02 | A0§2.5：mediation識別 | A4 Phase4にextension point | IDENTはBackdoor/Randomized中心 | D Phase4 | A4§2/8がmediation extensionを扱う。Phase1〜3に黙示的に採用しない |
| X-03 | A0§2.7：matching／g-computation | Foundation相当候補 | ESTはOLS/IPW/AIPWなど。matching/g-computation専用methodなし | B? 上位のみ | outcome regressionの実装と一般のg-computationを同一視しない |
| X-04 | A0§2.10：negative control outcome/exposure、simulated confounder、graph perturbation | 上位構想 | REFUTはPlacebo/Data Subset | B? 上位のみ | A1でnegative controlはextensionと記載。必須化するならAC追加 |
| X-05 | A0§2.11：モデル・欠測・graph/sampling sensitivity | 上位構想 | SENSはAdjustment Set/Clipping | B? 上位のみ | 現行FR-050の未実装ではない |
| X-06 | A0§2.8/2.9/2.15：cluster SE/bootstrap/multiple tests、Discovery stability・agreement | 上位構想＋一部現行 | E9 diagnostics、DISC bootstrap設定、BENCH1Aは部分対応 | C部分＋B? | 選定手法別に必要な科学的品質要件を次工程で固定 |
| X-07 | A0§2.13：Policy Evaluation／Decision、off-policy/cost/capacity | 9月末Phase4扱い | 新CLI Policy Executionの実装なし | D Phase4 | policy-ready fileはPhase2で候補、Policy自動実行とは異なる |
| X-08 | A0§2.17：Monitoring／Drift／automated re-analysis | 9月末Phase4扱い | 当該因果運用Capability未定義 | D Phase4 | 今回のPhase1〜3 CLI-only対象に含めない |
| X-09 | A0§2.16：Product canonical lineageと科学的provenance | Foundation残差 | GAP-C01〜C04。LINEAGE/CLOSURE/MANIFESTに部分機能 | A 現行Gap | 詳細は00_foundation_gap_closure_assessment.mdへ参照。CLI ManifestでProduct要件を閉鎖しない |
| X-10 | A0§4：UI/API/CLI/Workerでの意味統一 | 9月末Foundation統合確認、今回はCLI-first | 既存API/Worker/CLIがある。新methodsは未統合 | C既存＋D新統合 | 新手法のCLI意味・Artifactを検証しProduct統合は別scope |

### 5.2. 必須範囲の確定で避けるべきこと

A0の`ATC`、`matching/g-computation`、`negative control`、`graph perturbation`等を**既存FRでIMPLEMENTEDである**とも、A1〜A3の詳細指示だけで**明示的に不採用である**とも扱わない。A0の`controlled direct effect`と`mediation`はA4がextension pointとする後続Phase4の領域と区別して管理する。B0は`g-computation`が当時の推定系に存在したと記録しているため、これを「当時から全く存在しない」とは判定しない。ただし、現在の`scientific/inference/adapter.py`と`interfaces/cli/config_schema.py`に**独立した`g_computation` methodは登録されておらず**、B0の記述だけでは現行の一般的なg-computation契約の充足を証明できない。上位A0は分析ライフサイクル全体の必要機能を定義し、A1〜A3は当時のPhase実装の範囲と受入を定義している。**両者の不一致を採否保留で露出**させる。

一方、A0のPolicy Evaluation/MonitoringはA4のPhase 4文書にも必須機能として独立して記載されており、今後のPhase4等として明示D。Phase2の「Policy-ready Artifact」は将来利用できるファイルの意味であり、Policy自動執行の実装を意味しない。

## 6. 比較結果とRequirementへの影響

### 6.1. 確定した差分と未確定の採否

| 照合区分 | 照合した機能／契約行数 |
|---|---|
| P1 | 21 |
| P2 | 18 |
| P3 | 19 |
| 上位・横断 | 10 |

**68件の比較行すべてに判定を付けた。** 分割された機能が同一行に複数あるため、これは独立した新規FRの件数やGate数ではない。

**判定として確定できる事実:** 現行Native基盤・CLI/E9診断は再利用すべき。FCI・DoWhy・CATE・PCMCI・準実験は現行必須FRにない新Capabilityの候補。旧新機能Web/API/Worker/DB実装指示は新CLI-only方針ではD。上位A0のPhase帰属の曖昧な要求はB?として保留。

**未確定:** 個々のB/B?の最終採否、ライブラリ・統計的同等実装、Requirement revision、実装優先度、費用/リスク許容基準、Gate/Work Package、実装・独立検証のPASS。**ステップ3が完了してもステップ4の正式決定・承認は別工程。**

### 6.2. 既存Foundation Gap4領域との関係

| 既存Gap | 現行正本の状態 | この三資料照合の結論 |
|---|---|---|
| GAP-C01：探索再利用warning | FR-051・AR-004 PARTIAL | 既存Productの未充足。FCI/DoWhy導入で閉鎖しない |
| GAP-C02：canonical lineage | FR-008/054/095・NFR-002 PARTIAL | 既存Product資源の未充足。local Artifactを作るだけで閉鎖しない |
| GAP-C03：version/seed provenance | FR-086a/087b・NFR-001b PARTIAL | 新CLIの有効版・seed/splitは新契約へ。既存Product残差は別 |
| GAP-C04：Navigation Capability ownership | FR-132/133/144 PARTIAL、FR-145/NFR-023 NOT_IMPLEMENTED | 全Family共通Architecture Gap。新CLI-only科学手法の必須実装と自動連結しない |

### 6.3. Requirement semantic deltaの入力（承認前）

| 種別 | 意味上の改定候補 | 注意 |
|---|---|---|
| **現行要件を再利用** | FR-035〜050、FR-153〜156、NFR-025/028、AR-005/010/023など | 既存FRの範囲をFCI/CATE/DiDまで拡大解釈しない |
| **新しい機能要件候補** | FCI/optional DoWhy、追加refuter/sensitivity、CATE/HTEとEstimator、Temporal Graph/PCMCI、準実験Design/Estimand、local-file schema | 正本§11の未承認external backend除外とのsemantic conflictを改定で解消 |
| **横断品質要件候補** | 手法別eligibility、科学的negative result、推論・診断、optional dependency/version、seed/split、privacy、Known-truth Benchmark | 旧A0の曖昧な`must`は採否・測定法を先に決定 |
| **既存Gapの扱い** | GAP-C01〜C04の閉鎖・別Enhancement移管・正本改定 | P0/P1は調査優先度であって実装優先度ではない |
| **後続へ送る媒体** | 新規Web/API/Worker/DB/UI、Phase4 Policy/Monitoring、RPCMCI/J-PCMCI+ | 既存Productの動作や既存Requirementを削除する決定ではない |

## 7. 監査可能な証拠の範囲

### 7.1. 既存テストと過去999の読み方

- `BENCH1A`／`BENCH1`：Randomized/Backdoor Identification、ATE/ATT、Placebo/Adjustment/Clipping、CPDAG/PAG review、poor-overlap等の**既存テストソース**。今回のSHAで新たに再実行したわけではない。
- `CLITEST`：現行CLIの契約とManifestの試験ソース。新しいFCI/EconML/Temporal/Quasi-experimental CLIが実装されている証拠ではない。
- `E9G04`と`E9G05`：過去のcanonical 999 Gate DecisionのPASS（当時の対象に限る）。E9 Diagnostics/critical causal journeyの**歴史的受入**であり、新手法の受入証拠ではない。
- 今回は**現行固定SHAのpytest、optional external libraryのinstall/API調査、既知真値の新規ベンチマークを実施していない**。メソッド提供の科学的性能と安定性はGate 07以降で確定する。

### 7.2. 再照合・反証の条件

1. B/B?行が既に実装されていると判断するには、**対応する手法のcallable、Domain/CLI method contract、実行可能なテストとResult schema**の組合せを示す。名称・型の存在だけでは不可。
2. C行の「実装済み」は**現行FRが定める範囲**であり、旧A0/A1〜A3のすべての境界条件を満たす主張ではない。
3. 外部Libraryに希望したMethod/classが存在しない場合は、同等手法の科学的要件を満たすことを立証するか、そのCapabilityを未達として明示する。架空のclass名で要件を閉じない。
4. 要件の適用範囲が現行と矛盾する場合は、**変更差分・承認根拠・互換性・科学的影響を正本改定案へ記載**し、監査証拠を遡及的に書き換えない。

## 8. 後続ステップ4への引継ぎ

### 8.1. ステップ3の判定完了の意味

本書は2026年8月4日のA1/A2/A3実装指示とA0上位構想から、Phase 1〜3の機能群・実装媒体・科学的品質条項を抽出し、B0の当時のAs-Is評価を現在の正本・実装で再ベースラインして、A4によりPhase 4の境界を確認したうえで、**9月末の扱いと現行Baselineを対応付けた68行のSource Reconciliationを完了**した。差分判定をもって新機能を自動採用しない。

### 8.2. ステップ4で必ず決めること

1. **B候補の採否と必須機能の最終リスト:** 各Phaseの方法を削除・代替・追加する場合、理由とscientific equivalenceの証拠を残す。
2. **A0上位構想とA1〜A3の齟齬:** ATC、negative control、matching/g-computation等の**B?**を必須/選択/将来/不採用へ明示振分け。Mediation/controlled direct effectはA4 Phase4の後続扱いとし、変更には別承認を要する。
3. **対象面:** 新機能はScientific Core＋ローカルCLI＋durable local fileのみ。旧API/UI/Worker/DB項目を後続でどう扱うかを判断。
4. **既存要件Gapの帰属:** GAP-C01〜C04をE11で閉鎖するか別Issueに移管するか。Local CLI契約とProduct canonical lineageを混同しない。
5. **改定・科学受入の準備:** 正本§11を含むFR/NFR/AR semantic delta、Library support、Known-truth Benchmark/negative cases、Gate候補（**未固定**）を整理し、Human/Architecture承認へ渡す。

**ステップ4、要件・設計承認、Gate 06/07、Work Package、実装は本書の完了範囲外。**
