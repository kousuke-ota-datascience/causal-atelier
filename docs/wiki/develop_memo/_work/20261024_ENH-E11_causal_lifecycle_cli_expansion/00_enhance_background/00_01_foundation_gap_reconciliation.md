# ENH-E11 — 事前調査：2026年9月末のFoundation Gapと現行実装の照合

**文書区分:** 事前調査・証跡資料（構想文書01の入力）  
**状態:** ソース照合済み／現行SHAでの全件テスト未実施／未承認  
**調査日:** 2026-10-25  
**参照順序:** 本資料（00_01）→ 未解消Gap確定（00_02）→ 8月Phase 1〜3差分照合（00_03）→ 構想・要件改定計画（01）→ 承認記録（02）→ 要件・設計改定（03〜05）。事前調査はWorkflowの規定文書を代替しない。  
**比較基準:** 2026年9月末 `ENH-E11 Causal Lifecycle Foundation Gap Completion`（Notion `HANDOFF_DRAFT`、最終閲覧版）  
**現行基準:** `prototype/ariadne_mvp` at `4c0129146a59e7a294f13f41a2e27a4b0d820a6f`。要件実装状態是正コミット `84c5a624389b233fcb97c656f1c94d177f459c5a` を継承。  
**対象:** 9月末Notion §5 の13項目と、そこに直接関係する現行FR/NFR/AR、現行ソース、既存テスト、過去のcanonical 999。  
**対象外:** 8月4日Phase 2/3の新規スコープ確定、今後のCLI-onlyスコープに基づく作業分解、FR/NFR/AR改定、Gate 06/07、実装。

## 0. INTRODUCTION

### 0.1. 本文書の目的

本書は、**ENH-E11の構想・要件改定計画を策定する前に、2026年9月末の「Causal Lifecycle Foundation Gap Completion」構想と現行実装との事実関係を確定するための事前調査資料**である。9月末に解消対象とされた基盤的な不足が現時点で残っているかを検証し、既存機能の再実装や、未承認の新機能を「既存要件の未実装」と誤認することを防ぐ。

本書はWorkflowテンプレートに存在しない補助資料である。ただし、正規の`01_enhancement_concept_and_requirement_revision_plan.md`を作るための判断根拠として**01より先に作成・参照する必要がある**。本書自体は要件変更の承認、実装指示、Gate判定を行わない。

### 0.2. 本文書を作成するに至った背景

ENH-E11の9月末申し送りは、2026年8月4日の広い因果推論構想をそのまま採用せず、ENH-E5〜E10までに実現された機能を踏まえて**残存するFoundation Gapのみを特定する**方針を示していた。一方、現行の要件定義書ではImplementation Statusの是正が行われ、Graph、Identification、Estimation、Diagnosticsなどの実装状況は9月末の当初認識と異なる可能性があった。

この照合を省略して8月4日のPhase 1〜3実装計画やGitHub Issueの作業分解へ進むと、①既存機能の二重実装、②現行要件の未充足と新Capability候補の混同、③過去のGate PASSと現在の再検証の混同、④正式承認前のスコープ確定を招く。そのため、**第一工程を「9月末構想 × 現行実装」に限定**して事実を整理することとした。

### 0.3. 本文書で実施している内容

9月末のENH-E11申し送り§5に掲げられた**13項目（S01〜S13）を漏れなく照合**する。項目ごとに、(1)現行FR/NFR/ARのImplementation Status、(2)実装コード、(3)既存自動テスト、(4)過去のcanonical 999 Gate受入記録、(5)固定SHAでの新規再実行の有無を分けて記録し、残差をA〜Eに分類する。

さらに、13項目に直結する横断課題として、探索データ再利用warning、Navigationの責務分離、再現性・Provenanceを確認する。証拠不足と実際の要件未充足を混同せず、残存課題の追加検証条件を示す。**2026年8月4日のPhase 2・3追加スコープおよびCLI-onlyの実装計画確定は本書の対象外**であり、後続の三資料照合・構想検討で扱う。

### 0.4. 結論サマリ

| 判定対象 | 照合結果 | ENH-E11の構想策定に与える意味 |
|---|---|---|
| 既存Causal Foundation | Graph表現、Randomized/Backdoor Identification、Data Eligibility、ATE/ATT・IPW/AIPW、既存Diagnostics・Refutation・Sensitivity、既存API/Worker/CLI実行経路をコード・既存検証資料で確認 | **現行の契約範囲では再利用を原則**とし、歴史的な不足をそのまま新規実装対象にしない |
| 現行要件上の未充足 | FR-051/AR-004の同一Dataset再利用警告、FR-008/054/095・NFR-002のcanonical lineage、FR-086a/087b・NFR-001bの実効version/seed等はPARTIAL。加えてFR-132/133/144はPARTIAL、FR-145/NFR-023はNOT_IMPLEMENTED（Family-specific CapabilityによるNavigation catalog所有権） | **現行Requirement Gap（A）として残す**。4領域への整理・証拠水準・閉鎖条件は後続の`00_02_foundation_gap_closure_assessment.md`に記録 |
| 旧構想にある追加技術 | DoWhyおよびFCIは現行の必須FRとしては規定されていない | **新Capability候補（B）**。必要な場合は要件・設計の正式承認を得る |
| 将来送りの機能 | 汎用Product CLI（FR-118）はDEFERRED | 既存Scientific CLIと区別し、現行MUSTの未実装としない |

**結論:** 9月末が想定したFoundation Gapの大部分は、現行の基本機能として存在する。一方、lineage・探索データの再利用warning・再現性metadata・Navigation catalogのCapability所有権には残差がある。DoWhy/FCIは既存要件の修正ではなく新機能として採否を判断する。

**検証上の制限:** 今回の結論は現行ソース、既存テスト、歴史的Gate記録の照合に基づく。**今回の固定SHAで全件pytestやScientific Benchmarkを新たに実行した結果ではない**ため、全機能の最新環境における動作保証・科学的妥当性認定は行っていない。

## 1. 出典と判定方法

### 1.1. 一次資料とその位置付け

一次資料は[2026年9月末ENH-E11申し送り](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)の§1/§5/§6/§7/§9/§10/§11/§15/§19、[req](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/requirement_definition/10_requirements_definition.md)、本SHAの実装である。**9月末の原案は承認済み要件ではなくHANDOFF_DRAFT**。これを実装済み・未実装の定義に転用しない。

### 1.2. 事実と検証証拠の区別

以下を**別の列**で判定する：（a）現行要件のImplementation Status、（b）ソースの実装、（c）自動テストの存在、（d）過去のcanonical 999 PASS、（e）このSHAでの新規再実行。**(e)は今回未実施**。テスト名・過去のGate PASSのみで現行全経路の正当性を断定しない。

### 1.3. 未充足事項の分類と適用ルール

Notion §6の分類を適用する。
- **A_CURRENT_REQUIREMENT_GAP:** 現行要件に明記されているが部分充足・未充足。
- **B_NEW_CAPABILITY_CANDIDATE:** 旧構想にはあるが、現行要件に義務がない新技術。導入には新規要件・承認が必要。
- **C_SUPERSEDED:** 9月末の「不足」が現在の実装/設計で解消済み、または旧前提が不要。現行実装の検証範囲内で再実装しない。
- **D_FUTURE_PHASE:** 要件上将来送り・DEFERRED。
- **E_REJECT:** 現行方針に反する候補。今回の13項目に確定REJECTなし。

1項目に既存基盤と新規機能が混在する場合、**能力を分割してそれぞれ分類**する。残差なしとするのは現行要件に限定し、歴史的な無制限の機能充足を意味しない。

## 2. 9月末 §5 全13項目：要件 × コード × 検証証跡

### 2.1. 13項目の照合結果

| ID / 9月末項目 | 現行要件上の状態 | 現行実装の具体的証跡 | 自動テスト / 過去の受入 | 現在も残るGapと分類 |
|---|---|---|---|---|
| S01 Causal Question / version | FR-040 **IMPLEMENTED**；FR-054 **PARTIAL**（lineageは別行） | [spec](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/domain/analysis_spec.py)：population/treatment/comparator/outcome/time/estimandを検証しquestion hashを生成。[specver](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/domain/analysis_specification.py)：versioned AnalysisSpecification DRAFT/FIXED。 | [cliTest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/product/test_cli_contract.py)、[bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)；当該独立Question-Version専用999は**NOT_LOCATED**。 | **C**：Question内容とspec snapshotは現行基盤。独立した `CausalQuestionVersion` の要求/充足はこのFRから導けず、必要なら **B**（要件改定候補）。「独立Versionまで実装済み」とは主張しない。 |
| S02 Causal Design extension | FR-041 **IMPLEMENTED** | [spec](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/domain/analysis_spec.py)：identification strategy/adjustment/assumptions、time zero関連内容を検査。[specver](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/domain/analysis_specification.py)：FIXEDなSpecification。 | [eligtest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific/test_identification_e1a.py)、[bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)；専用の最終999は**NOT_LOCATED**。 | **C**：既存Designの明示的固定。9月末の未特定の「extension」をそのまま新規要件にしない。新属性が必要なら**B**として個別定義。 |
| S03 DAG / CPDAG / PAG | FR-036～039 **IMPLEMENTED** | [graph](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/domain/graph_semantics.py)：TAIL/ARROW/CIRCLEとDAG/CPDAG/PAG許容endpointを検証。[graphver](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/graph_version_service.py)：USER_DEFINED/IMPORTED、derived edit draft、FIXED Graph、hash。 | [bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)のunresolved CPDAG/PAG試験、[eligtest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific/test_identification_e1a.py)。 | **C**：現行graphの基礎表現。発見アルゴリズムFCIやPAGからの一般的識別成立は包含しない（S13）。 |
| S04 Identification | FR-042/043、AR-005/023 **IMPLEMENTED** | [identify](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/identification/adapter.py)：Randomized/Backdoor、multiple reasons、`IDENTIFIED/NOT_IDENTIFIED/REQUIRES_REVIEW`、CPDAG/PAGの非強制変換。 | [bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)、[eligtest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific/test_identification_e1a.py)。 | **C**：現行strategyでの識別基盤。Frontdoor/IV/DoWhyは**B**（S12）、現行要件の未実装ではない。 |
| S05 Data Eligibility | FR-044/045 **IMPLEMENTED** | [identify](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/identification/adapter.py)：列、型、欠測、二値処置、sample、preliminary propensity overlap等を別DATA_ELIGIBILITY_RESULTで返す。 | [eligtest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific/test_identification_e1a.py)のmissing/unsupported/prevalence/overlap等と[bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)。 | **C**：既存手法のeligibility。新推定法固有のeligibilityは今回の9月末Gapとして未確定。 |
| S06 Estimation / gate | FR-046/047、AR-005/010 **IMPLEMENTED** | [validation](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/scientific_validation_service.py)：上流identification/eligibility、WARN override、method compatibilityを検査。[estimate](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/inference/adapter.py)：diff/OLS/IPW/AIPW、ATE/ATT、区間推定、非適格のnegative result。[cliest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/estimation.py)：identification manifestを検証。 | [bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)、[cliTest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/product/test_cli_contract.py)。 | **C**：既存範囲での推定とgate。IPTWのestimated-propensity下のSE/CI被覆などは**追加科学検証を要するが、この調査だけでAとは断定しない**。CATE等は旧9月末スコープ外。 |
| S07 Diagnostics | FR-048 **IMPLEMENTED** | [estimate](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/inference/adapter.py)：sample loss/design/balance/overlap/weighting適用性、scientific resultへ保存。 | [weightTest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/enhancement/enh_e9/g04/scientific/test_ipw_weighting_persistence.py)、[E9 G04 canonical 999 PASS](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G04/Trial01/ENH-E9-G04_01__999_gate_decision.md)：43 mandatory checksとAC1–AC15；[E9 G05 PASS](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md)：critical Causal journey。 | **C**：E9で当時のstructured diagnostics gapは閉鎖済み。新手法の診断や未検証の分散式まで自動的に充足しない。 |
| S08 Refutation | FR-049 **IMPLEMENTED** | [refute](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/refutation/adapter.py)：PLACEBO_TREATMENT / DATA_SUBSET、seed、perturbation、failure/no-failure status。 | [bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)、[benchOld](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1_benchmarks.py)。 | **C**：要件の2手法。Random Common Cause/Bootstrap等は**B**（新規候補）、旧要件の未実装ではない。 |
| S09 Sensitivity | FR-050 **IMPLEMENTED** | [sensitivity](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/sensitivity/adapter.py)：ADJUSTMENT_SET / PROPENSITY_CLIPPINGを複数条件で再推定しFRAGILE/ROBUST/INCONCLUSIVEを区別。 | [bench](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1a_acceptance.py)、[benchOld](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/scientific_benchmarks/test_enh_e1_benchmarks.py)。 | **C**：要件の2軸。未測定交絡の一般感度分析は**B**（未採用の追加Capability）。 |
| S10 Artifact / Manifest / lineage | FR-090等 **IMPLEMENTED**、FR-008/054/095・NFR-002・NFR-001b **PARTIAL** | [lineage](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/lineage_query_service.py)：Result→Execution/Dataset/Graph/Artifact/上流Resultの参照。[closure](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/product_closure_service.py)：Project read-modelにResearchContext/Specification等ノード・edge。[climan](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/manifest.py)と[clistage](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/scientific_stage.py)：local SHA256 input/artifact/seed。 | [cliTest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/product/test_cli_contract.py)はhash・local manifestを検証。E9 G05は一定のcross-layer lineageを検証。ただし全resource chainの専用証明は**NOT_ESTABLISHED**。 | **A**：正本上のfull canonical Result lineageの部分充足。**A**：effective scientific library version/StageAttempt seedの完全性（NFR-001b）。CLI runtime_versionsはPython中心、[execution](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/execution_service.py)のProduct runtime metadataは限定library列挙。DB lineageとlocal CLI manifestを同一authorityとしない。 |
| S11 API / CLI / Worker | FR-142・NFR-025 **IMPLEMENTED**、FR-118 **DEFERRED/NOT_IMPLEMENTED** | [worker](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/worker/execution_processor.py)：Execution処理、Result/Artifact永続化。[clistage](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/scientific_stage.py)、[cliest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/estimation.py)：DB不要のScientific CLI。Product APIは `src/ariadne/interfaces/web_api/routers/{executions,results,graph_versions}.py`。 | [cliTest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/tests/product/test_cli_contract.py)、[e8gate](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign/30_test_report/G02/Trial02/999_GATE_DECISION.md)：E8 stage separation受入、[e9gate5](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md)：API/Worker/DB/Browserを通した限定Causal journey受入。 | **C**：既存Product科学実行経路の存在。generic Product CLIでsubmit/status取得するFR-118は**D**（明示DEFERRED）であり、既存standalone CLIと混同しない。9月末の「integration residual」全般は受入経路別に再判定する。 |
| S12 DoWhy | 現行FRにDoWhy必須要件なし。正本§11は未承認外部engineを対象外とする。 | [identify](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/identification/adapter.py)はnative、[clispec](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/config_schema.py)にDoWhy method選択なし。 | DoWhy adapterのコード/テスト/999は**NOT_LOCATED**。 | **B**：導入可否をRequirement改訂で判断する候補。現行実装が欠けている事実と、現行Requirement Gapであることは別。 |
| S13 FCI | FR-035/037は一般Discovery/Graph表現でありFCI固有要件なし。 | [discovery](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/scientific/discovery/adapter.py)のregistryはPC/GES/LiNGAM/NOTEARS、[clispec](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/config_schema.py)も同様。PAG表現（S03）は存在。 | FCI専用テスト/999は**NOT_LOCATED**。 | **B**：FCI discovery、PAG endpointsの忠実な保存・潜在交絡warningを新規Capabilityとして承認判断。PAGをDAGへ強制変換しない。 |

### 2.2. 判定境界と解釈上の注意

上記の「C」は**記載した現在のmethod/contractの範囲に限る**。例えばFR-047=IMPLEMENTEDを根拠にCATEやLATEを実装済みとは扱わない。上記「NOT_LOCATED」は今回参照した証跡で特定できなかった意味であり、全履歴に存在しないという断定ではない。

## 3. §5以外だが9月末Foundation残差に直結する横断事項

| ID | 現行要件・証跡 | 判定 |
|---|---|---|
| X01 Exploratory reuse warning | FR-051 / AR-004 **PARTIAL**。[explore](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/exploratory_service.py)のExploratory Result→Causal/Predictive DRAFT handoffでは `EXPLORATORY_REUSE_SAME_DATA` とsource Result IDが生成される。一方[execution](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/execution_service.py)の同一Dataset Discovery後のconfirmatory Estimation warningは`POST_SELECTION_INFERENCE_RISK`であり別条件・別code。一般的な同一Dataset reuseの検出網羅は示されない。 | **A**：現行要件の明確な部分充足。2つのwarningを同一とみなさない。 |
| X02 Navigationの分離 | FR-153～156とAR-023/024は正本で **IMPLEMENTED**、[E8 G02 999 PASS](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign/30_test_report/G02/Trial02/999_GATE_DECISION.md)、[E9 G05 999 PASS](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization/30_test_report/G05/Trial01/ENH-E9-G05_01__999_gate_decision.md)。 | **C**：9月末に想定したNavigationの基礎Gapは現在の受入範囲で解消。 |
| X04 Navigation catalog ownership | FR-132/133/144 **PARTIAL**、FR-145/NFR-023 **NOT_IMPLEMENTED**。`src/ariadne/product/application/navigation_catalog.py`が3 Familyの具体的Stage ID/slug/defaultを集中宣言。Stage表示と科学的Stage責務の分離（X02）とは別の所有権制約である。 | **A**：現行正本とコードの設計上の不一致。実装対応をE11 CLI-only範囲へ自動算入しない。 |
| X03 Reproducibility / provenance | NFR-001b **PARTIAL**。[climan](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/manifest.py)は`backend_version`項目を持つが[clistage](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/interfaces/cli/scientific_stage.py)は`ariadne/0.1.0`固定、runtime_versionsはPython中心。Product [execution](https://github.com/kousuke-ota-datascience/causal-atelier/blob/4c0129146a59e7a294f13f41a2e27a4b0d820a6f/src/ariadne/product/application/execution_service.py)の`_runtime_manifest`は固定列挙のlibrary versionsを記録する。 | **A**：実効依存versionとeffective seedの全stage完全性は未立証。CLIのversion placeholderを真のbackend package versionと誤認しない。 |

## 4. 確認方法と未検証範囲（重要）

### 4.1. 実施した確認

1. Notion `HANDOFF_DRAFT` §5の13項目を逐語単位で起点に固定。
2. 正本 `10_requirements_definition.md` のFR/NFR/AR Implementation StatusをSHA付きで照合。
3. Scientific/Domain/Application/CLI/API/Worker/lineageの該当実装とテスト**ソースを閲覧**。
4. E8 G02、E9 G04、E9 G05のcanonical 999 Gate decision本文を読取り、対応する受入の主張範囲を確認。

### 4.2. 実施していない確認

- 固定SHAでの新規pytest再実行、全Scientific Benchmark再実行、Browser E2E再実行。
- 各FRについて「対象となる全テスト/Gate」との厳密な全件一対一追跡。
- 任意の実データでのscience-validity certification / ライブラリ依存version行列。
- FR-054全ノード間の閉包・Graph lineage edgeを全データモデルで実行検証。

したがって**Source Reconciliationとして13/13項目を分類した**が、runtime最終認定ではない。前会話の別SHAに関するテスト報告値をこのSHAの再実行値として転記しない。

## 5. 残存する基盤的課題：追加調査の優先順位（スコープ決定ではない）

| 優先 | 現行要件 | 調査・受入で詰める残差 | 必要な主たる検証 |
|---|---|---|---|
| P0 | FR-054 / FR-008 / FR-095 / NFR-002 | Causal Result起点のRCV→Spec→Plan→Execution→StageExecution→Result→Artifact、Dataset/AnalysisView/Graph/上流resultへの正しい端点・edgeが完全か | Product lineage API/DB fixtureでノード・有向edge・Project boundaryを全件assert |
| P0 | FR-051 / AR-004 | 明示的handoff以外のsame immutable Dataset explorative→confirmatory reuseを検知する条件とResult evidence連結 | same-dataset、有/無handoff、別Dataset、cross-project、同一/異なる分析操作のcase matrix |
| P1 | NFR-001b | effective package/python/version、実効seed、retry/stage attempt、CLI vs Product manifestの意味の違い | manifest contract、multiple stage attempt、optional backend absent、fixed-seed replay |
| P1 | FR-040/041 / FR-054 | Question/Designの独立resource version要否（現行要件には明記なし）。もし要件拡張するならResource authorityを先に定義 | 既存AnalysisSpecification Versionとのmapping、hashとGraph/Result関係 |
| P1 | FR-132/133/144/145・NFR-023 | Family固有StageのCapability所有権がgeneric applicationに集中している。UI挙動がPASSでもArchitecture要件は未充足 | ownershipをCapabilityへ移すか承認された要件改訂。API/historyの回帰を保護 |
| P2 | FR-046/047/048 | 既存IPW/AIPWの分散・区間推定、診断結果の科学的妥当性（現行IMPLEMENTEDを否定する直接証拠は未提示） | known-truth bias/CI coverageとpoor overlapを独立試験で評価 |

**S12 DoWhy、S13 FCI** はこの残存現行Requirement Gapの表へ混入させない。別枠の **B_NEW_CAPABILITY_CANDIDATE**。FR-118もcurrent MUST GapではなくDEFERRED。

## 6. この照合が認める結論／認めない結論

### 6.1. 今回の証拠から支持できる結論

**認める**：9月末の13項目について、基礎Graph・Identification・Eligibility・ATE/ATT・Diagnostics・既存Refutation/Sensitivityおよび既存API/Worker/CLIは現行実装で確認可能。再実装する前に現在の実装を継承する。現行要件上の残差はlineage / reuse warning / runtime provenance / Capability所有権の4領域。詳細な閉鎖条件は`00_02_foundation_gap_closure_assessment.md`で扱う。DoWhy/FCIは新Requirement候補。

### 6.2. 今回の証拠から支持できない結論

**認めない**：13項目がすべて科学的に再検証済みという主張、DoWhy/FCIが現行MUST要件の未実装であるという主張、9月末の将来Phase除外が現時点のowner決定に優越するという主張、Phase 1–3の実装Gate/G01–G10が既に正式承認されたという主張。

### 6.3. 後続工程への引継ぎ

**次の判断点**：この9月末スコープでのSource Reconciliationと残差をレビューした後にのみ、8月4日Phase 1–3案および現在のCLI-only方針との追加差分を別工程で扱う。ここでは新Issueの実装作業や要件・設計の改訂を実施していない。
