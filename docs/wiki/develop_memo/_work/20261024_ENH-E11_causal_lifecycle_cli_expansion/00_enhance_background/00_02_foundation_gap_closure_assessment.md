# ENH-E11 — 事前調査：未解消Foundation Gapの確定

**文書区分:** 事前調査・残差判定資料（Workflow所定の01より前に参照）  
**判定状態:** 残差の候補と証拠水準を確定／固定SHAでの全件テスト未実施／実装計画・正式承認ではない  
**判定日:** 2026-10-25（日本時間）  
**対象基準:** `prototype/ariadne_mvp`、source SHA `e00b3e35be6adc536dffd270609b193669062dd3`。事実認定に用いるRequirementは[req](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/docs/wiki/requirement_definition/10_requirements_definition.md)。  
**先行資料:** [reconcile](00_01_foundation_gap_reconciliation.md)。9月末のNotion `HANDOFF_DRAFT`（[ENH-E11構想](https://app.notion.com/p/403e5855be3980c186c3f778a7bfaac5)）と現行基準を13項目で照合した結果を引き継ぐ。  
**利用先:** `01_enhancement_concept_and_requirement_revision_plan.md` の要件・実装差分の入力。8月案Phase 2/3の新規実装判断はこの資料の対象外。

## 0. INTRODUCTION

### 0.1. 本文書の目的

本書は、先行する13項目のFoundation Gap Reconciliationから、**現行正本の有効なFR/NFR/ARに対して、現時点で解消されていない部分を漏れなく切り分ける**ための事前評価資料である。9月末の旧構想をそのまま作業指示にすることなく、既に実装された能力、要件の実質的残差、検証だけが不足している状態、新規Capability候補を区別する。

「Gapとして確定」は**現行正本との不一致・未立証箇所を登録する**意味であり、修正方法の承認、ENH-E11の実装範囲への自動採用、科学的受入の完了を意味しない。

### 0.2. 本文書を作成するに至った背景

先行`00_01_foundation_gap_reconciliation.md`では、Graph・Identification・Eligibility・ATE/ATT・既存Diagnostics等の基盤が概ね現行コードに存在する一方、lineage、探索データ再利用warning、実行環境provenanceの部分充足を確認した。ただしこの三領域のみでは、現行正本で`NOT_IMPLEMENTED`として残る**Family-specific NavigationのCapability所有権（FR-145/NFR-023）**を取りこぼす。

さらに、実装の存在を確認しても網羅的な経路の証明がないものと、コード自体が正本の全構造を提供していないものを同じ「未実装」にすると、実装対象と検証作業の境界が不明確になる。そこで正本の原文・実装・テストで残差を再点検し、根拠と未決事項を保存する。

### 0.3. 本文書で実施している内容

(1) 既存正本のImplementation Statusと要件文言、(2) Source codeの実装経路、(3)既存Unit／Integration／Scientific Benchmarkの主張範囲、(4)過去Gateの受入記録、(5)今回の固定SHAでの新規実行有無、を分けて評価する。

残存課題は **GAP-C01〜GAP-C04の4領域**で登録し、各領域に実装済みの部分、確認できる欠落、未証明の条件、閉鎖判定を行うための受入条件、所管の未確定事項を付ける。網羅的な実行テストがない項目について、`SOURCE_CONFIRMED`と`COVERAGE_NOT_PROVEN`を使い分ける。

### 0.4. 結論サマリ

| 区分 | 確定した扱い | 説明 |
|---|---|---|
| GAP-C01 探索→検証の再利用警告 | **要件上の残差：COVERAGE_NOT_PROVEN** | 明示的handoffは実装・試験があるが、対象となるconfirmatory全経路の網羅性は未立証 |
| GAP-C02 Canonical Lineage | **構造残差：SOURCE_CONFIRMED** | Result個別照会とProject統合照会に存在する情報が異なり、正本の完全なResource chainがない |
| GAP-C03 再現性・Provenance | **複合残差：SOURCE_CONFIRMED＋COVERAGE_NOT_PROVEN** | Library version収集は部分的。StageAttempt seedの保存機構は存在するが全stochastic経路は未立証 |
| GAP-C04 NavigationのCapability所有権 | **構造残差：SOURCE_CONFIRMED** | Family固有Stage catalogの具体定義がgeneric applicationにあり、正本のownership制約を満たさない |

この4領域を**現行要件に対する残存Foundation Gapの登録簿**とする。ただしC04は全Family共通の設計残差であり、C01〜C03もProduct DB側の改修が必要なものは、既決の新機能CLI-only範囲に**自動的には含めない**。DoWhy・FCIは新Capability候補であり、この4件へ合算しない。

## 1. 判定の根拠と限界

### 1.1. 正本と調査基準

RequirementのStatusは、実装済み`IMPLEMENTED`を旧Phase全手法の実装と同一視せず、`PARTIAL`を「全機能未実装」ともしない。9月末資料は`HANDOFF_DRAFT`であり、正本の要件を上書きしない。

本資料が示すStatusは**調査時点のコードと要件の対応に関する判定**である。正本の`Requirement Status`、`Implementation Status`、`Delivery`列は書き換えていない。

### 1.2. 証拠水準

- `SOURCE_CONFIRMED`：正本の具体的な要求とコードの具体的な挙動・所有者・欠落構造を比較して残差を確認したもの。
- `COVERAGE_NOT_PROVEN`：該当機能と一部テストは存在するが、要件に含まれる全経路・retry・例外条件の充足を示す証拠が不足するもの。「対象機能が全く動かない」とは断定しない。
- `METHOD_QUALITY_REVIEW`：既存推定の科学的性能の再評価を要するが、現行正本の未充足をこの調査だけで断定できないもの。
- `NEW_REQUIREMENT_CANDIDATE`：9月末構想にあるが現在の必須FRにない能力。新規採用の正式承認を要するもの。

**本調査では新たなpytest・DB E2E・科学Benchmarkを実行していない。** テストファイルの存在や過去の999 PASSは、新規再実行に代わらない。

## 2. 未解消Foundation Gapの確定一覧

| ID | 現行要件・Status | 本調査の判定 | 既存の充足範囲 | 未充足／未立証 | 完了判定に必要な証拠 |
|---|---|---|---|---|---|
| **GAP-C01** | FR-051、AR-004：**PARTIAL** | **COVERAGE_NOT_PROVEN** | Exploratory Result→Causal/Predictive DRAFTの明示的handoffはsame-data warningとsource Result IDを保持 | 先行Exploratory Resultを利用したconfirmatory分析のほかの開始・引継ぎ経路、警告の最終Result/lineageへの保存の網羅性 | 同一Dataset・同一Source Result・別Dataset・別Project・非Confirmatory・非handoff・API/Worker/CLIの各適用経路でpositive/negativeと証跡をassert |
| **GAP-C02** | FR-008/054/095、NFR-002：**PARTIAL** | **SOURCE_CONFIRMED** | Result↔Execution、Dataset、Graph、上流Result、Artifactの追跡、およびProject投影のContext/Specノード | 正本が定めるContext→Spec→Plan→Execution→StageExecution→Result→Artifactの連続した方向付き構造、Resource所有権およびResult起点の十分な絞込 | 型付き権威による全Resource edge、Project boundary、upstream/revision、export一致、不要なsibling混入の禁止を固定fixtureで検証 |
| **GAP-C03** | FR-087b・NFR-001b：**PARTIAL**、FR-086a：**PARTIAL** | **SOURCE_CONFIRMED＋COVERAGE_NOT_PROVEN** | Productの一部Library version、StageAttemptのseed field/retry保持実装、WorkerからExecutorへのseed受渡し、CLIの一部hash/metadata | 実際に使った科学Library/Backend versionの網羅性、および全stochastic Stage/retryで実効seedが保存・再利用されること | backend別の実効version/環境再構築、実行Attempt・retry seedの同値、固定seed再現、Manifest/DB読戻し |
| **GAP-C04** | FR-132/133/144：**PARTIAL**、FR-145/NFR-023：**NOT_IMPLEMENTED** | **SOURCE_CONFIRMED** | Frozen descriptor、Family固有のdefault stage・表示・Navigation切替は存在 | concrete Stage ID/slug/order/defaultの定義場所がFamily Capabilityでなくgeneric applicationの中央catalog | Family Capabilityがdescriptorを所有し、aggregatorはread-only取得のみ。E7/E8/E9のroute/history/presentation回帰も維持 |

### 2.1. GAP-C01：探索結果を用いた検証分析の再利用警告

**根拠:** [explore](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/exploratory_service.py) の`create_analysis_draft`はExploratory Resultを起点にCausal/Predictive DRAFTを生成し、`CONFIRMATORY`の場合`EXPLORATORY_REUSE_SAME_DATA`とsource Result IDを付与する。[handoff](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/tests/product/test_exploratory_api_worker_e2e_e3.py)はこの明示的経路を検証する。

**区別すべき実装:** [exect](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/execution_service.py)の`_post_selection_inference_warnings`は、同一Datasetに先行する`DISCOVERY` Executionがあるconfirmatory Estimationへ`POST_SELECTION_INFERENCE_RISK`を付ける。この警告は**Exploratory Resultの同一データ再利用と同じ条件・警告codeではない**。

**確定内容:** 要件が要求する「先行Exploratory Resultを**利用した**confirmatory分析」をあらゆる経路で検出している証拠がない。単に同じDatasetで探索と推定を行っただけで必ず関連があると誤認する設計も避ける。Source Result IDとDataset Versionの因果的な参照関係を明示してpositive/negativeのcase matrixを作る。

### 2.2. GAP-C02：Canonical Lineageの完全性

**根拠:** [lineage](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/lineage_query_service.py)のResult中心の`get_lineage`が構成する主なnodeはProject、Execution、DatasetVersion、Result、GraphVersion、Artifact、Annotationであり、Context/Spec/Plan/Stageを正本の連続した関係として形成しない。

[closure](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/product_closure_service.py)の`project_lineage`にはResearchContextVersion、AnalysisSpecificationノードがある一方、ExecutionPlan/StageExecutionのnode・edgeを構成しない。Result中心`result_lineage`は**無向の連結性**で絞り込んでおり、単一Dataset経由で無関係の兄弟Resultが含まれ得る（実際に含むことの実行試験は別途必要）。[cross](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/tests/product/test_cross_analysis_lineage_e3.py)は一部edgeの存在を検証するが、完全chainの受入ではない。[export](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/tests/product/test_results_lineage_export_e3.py)には、Spec→Executionの`USED_INPUT` edgeが存在しないことをassertする箇所もある。

[edge](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/domain/lineage.py)はtyped structural relationの権威とgeneric-only relationを厳格に区別するため、欠けた構造edgeを任意のgeneric lineage書込みで補ってはいけない。**Resource authorityを先に設計・承認する**必要がある。

### 2.3. GAP-C03：実効Library versionとStageAttempt seed

**根拠:** [exect](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/execution_service.py)の`_runtime_manifest`は`numpy/pandas/scikit-learn/scipy/networkx/pyarrow`を列挙して保存するが、`statsmodels`を含め、**実際に使用したすべてのScientific Libraryを記録する契約にはなっていない**。[cli](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/interfaces/cli/scientific_stage.py)・[estimate](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/interfaces/cli/estimation.py)の`runtime_versions`はPython中心、`backend_version`は`ariadne/0.1.0`という固定値であり実効Backend版の確定証拠ではない。

一方、[attempt](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/domain/stage_execution.py)の`StageAttempt.effective_random_seed`は実装済みでretryは既存seedを引き継ぐ。[executor](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/workflow/executor.py)はstochasticと判定したStageに`effective_random_seed`を渡し、[worker](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/interfaces/worker/execution_processor.py)は`execution.random_seed`をExecutorへ渡している。[repo](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/persistence/repositories.py)にはStageAttemptの永続化処理も存在する。

**確定内容:** Versionの網羅性はコード上の残差。seed欄やretry保持の存在は認めるが、`random_seed=None`時の実効seed決定、すべてのstochastic Stage経路、永続化を伴うretry、並列実行等の完了条件は**COVERAGE_NOT_PROVEN**とする。既存seed機構の再実装が必要とまでは断定しない。

### 2.4. GAP-C04：Family-specific Navigationの所有権

**根拠:** [navigation](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/src/ariadne/product/application/navigation_catalog.py)に`CATALOG`と`FamilyNavigation`があり、Exploratory/Predictive/Causalの具体Stage IDsとdefault stageが**generic application**で宣言されている。[navtest](https://github.com/kousuke-ota-datascience/causal-atelier/blob/e00b3e35be6adc536dffd270609b193669062dd3/tests/product/test_enh_e5_g00_navigation.py)はCatalogの動作・妥当性とNavigation APIを検証するが、Capabilityによる定義の所有権を証明するものではない。

正本のFR-133/144とNFR-023は**Family-specific Capabilityが具体catalogを所有**することを要求し、FR-145はgeneric layerの集中所有を禁止する。これはUIのStage分離（FR-153〜156）とは別の**保守性・Architecture Gap**である。

**確定内容:** 現行コードと正本の設計制約が直接衝突する。修正してCapability所有へ移すか、正本の制約をArchitecture Reviewで正規に改定するかを決める必要がある。**この判断をもってENH-E11のCLI-only作業へ自動的に組み込まない。**

## 3. 閉鎖条件・検証方法の記録

| ID | 最低限のAcceptance Criterion候補（未承認） | 逆方向の検証 | 閉鎖判定に必要なAuthority |
|---|---|---|---|
| GAP-C01 | Exploratory Resultに紐づくsame-Dataset confirmatory全経路で正しいwarning codeとsource Result evidenceを保存 | 無関係な探索、別Dataset、別Project、単なるDiscoveryの誤報なし | 現行FR-051/AR-004の意味、関係Resourceの識別 |
| GAP-C02 | 指定の連続chainの各node/edgeをcanonical read model・exportで往復できる | 不正Project跨ぎ、chain切断、graph cycle、無関係Result混入なし | Typed structural lineageの資源権威、read model |
| GAP-C03 | 実効Dependency package/version、seedとAttempt履歴をManifest/DBで再構築 | optional backend欠落、Stage retry、seed未指定、追加Library使用時も虚偽version/seedを記録しない | Scientific runtimeとExecution/StageAttemptの値決定責務 |
| GAP-C04 | concrete catalogはFamily Capability由来で、generic aggregatorはread-only | 新Family追加でgeneric stage実装を変更せず、既存route/history/APIは退行しない | Capability-owned descriptorとgeneric read modelの境界 |

本表は**試験規格の草案**であり、正式なGate 07および統計的許容値の代わりにはならない。再検証の結果、一部の行が実装済みと証明される場合は、要件の意味を変えずに判定を更新する。

## 4. 閉鎖済み・対象外・判断待ちの整理

### 4.1. 既存基盤として再利用するもの

Graph（DAG/CPDAG/PAG semantics）、Randomized/Backdoor Identification、Data Eligibility、ATE/ATTと既存IPW/AIPW、E9の適用可能なDiagnostics、Placebo/Data Subset Refutation、Adjustment Set/Propensity Clipping Sensitivity、Scientific CLI、既存API/Workerの限定実行経路。

これらの現行FRが`IMPLEMENTED`であることは、DoWhy、FCI、CATE、時系列因果、準実験、IPTWの統計的推論品質の全項目まで認定するものではない。

### 4.2. 本4件へ混入させないもの

- **新規Capability候補（B）:** DoWhy、FCI、独立した`CausalQuestionVersion`の追加resource、Refutation/Sensitivityの新方式。8月Phase 2/3は後段で別に照合する。
- **明示DEFERRED（D）:** FR-118のgeneric Product CLI。既存standalone Scientific CLIはこれと異なる。
- **科学的品質検証（METHOD_QUALITY_REVIEW）:** IPTWの推定傾向スコアを考慮した標準誤差・信頼区間被覆率など。性能が十分かを検証するが、今回の情報だけで現行FR-047/048違反と断定しない。
- **隣接する既存PARTIAL:** FR-034（Exploratory provenance）のような関連する汎用Product要件、その他E5残差。因果Foundationの未充足として全件を再分類せず、該当するauthority/lineage試験の入力に含める。

## 5. ENH-E11への取込み判断（本書では未承認）

| 項目 | 適用面 | 取り扱い |
|---|---|---|
| GAP-C01 | 既存Product Exploratory→Confirmatory handoff | 要件Gapとして維持。CLI-only E11での対応可否を決めるには、既存Product API/DB改修を許すかの別途判断が必要 |
| GAP-C02 | 既存Product canonical DB lineage | **現行要件Gapとして維持**。CLIのローカルManifestを作るだけでFR-054等を閉鎖したとは主張できない。E11外での改修または適用範囲の明示的承認が必要 |
| GAP-C03 | 既存Product metadataと新規CLIの再現性 | CLI側の新手法version/seed対策はE11共通契約候補。既存Product StageAttempt/Execution部分の是正範囲は別途決定 |
| GAP-C04 | 全FamilyのProduct Navigation architecture | 現行要件Gapとして維持。CLI-only科学手法の実装前提と断定せず、別Issue／別Enhancementへの帰属や要件改定を審議 |

**注意:** 「未解消のFoundation Gap一覧を確定する」ことと「そのすべてを今回のENH-E11で実装する」ことは独立した判断である。この区別を維持し、後続の三資料比較で適用スコープを最終決定する。

## 6. 判定結果と後続工程

### 6.1. 確定できる内容

現在の正本に対する残存Foundation Gapは**GAP-C01〜GAP-C04**の4領域とする。C02/C04とC03の実効Library versionは直接の構造不一致を確認した。C01とC03のstochastic seed網羅性は、動作する既存実装を認めつつ全経路での充足が未立証な状態である。

### 6.2. 確定していない内容

各要件のruntime最終受入、再実行による全件PASS、修正方法、専用GitHub Issue割当、ENH-E11の正式scope、Gate数・06/07の固定、正本Implementation Statusの変更。これらをこの事前判定から推定しない。

### 6.3. 後続への入力

本書の4領域を`01_enhancement_concept_and_requirement_revision_plan.md`の**現行基盤残差**の確定入力とする。その後に2026年8月4日Phase 1〜3構想を突き合わせ、新Capability候補とCLI-onlyの追加スコープを別表で判断する。GitHub Issue #14はその後続まで完了していないためOpenを維持する。
