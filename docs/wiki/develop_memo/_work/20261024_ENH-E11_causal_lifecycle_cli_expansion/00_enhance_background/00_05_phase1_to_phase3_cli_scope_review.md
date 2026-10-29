# ENH-E11 — 00_04 CLI-only実装スコープ案の技術審査記録

**文書区分:** 事前調査の審査記録／構想01・承認記録02への入力  
**審査日:** 2026-10-29（日本時間）  
**審査対象:** [00_04_phase1_to_phase3_cli_scope_proposal.md](00_04_phase1_to_phase3_cli_scope_proposal.md)（68項目、承認前）  
**根拠Snapshot:** `prototype/ariadne_mvp`、`e5ab0b25666f166ac836e24164bb5b32797057a9`（**審査時のコード・文書参照**。実装受入Baselineとしてfreezeしていない）  
**技術審査結論:** **CHANGES_REQUIRED（修正要求）**。追跡性・CLI-only境界は**適切**だが、必須Method・科学的方式・依存互換性・例外・Product Gap移管を**このまま正式実装契約として承認できる状態ではない**。  
**承認権限:** Human owner／Architecture owner。**本書は審査指摘であり、オーナーによる承認・不承認の代行ではない。**  
**実施しなかったもの:** 新規コード・正本FR/NFR/AR修正、外部Library install、実環境API probe、fresh pytest／Scientific Benchmark、Gate 06/07 freeze、canonical 999。

## 0. INTRODUCTION

### 0.1. 本文書の目的

ステップ4の`00_04`を**単に「全68行が埋まっている」として完了扱いせず**、(i)歴史的要求の網羅性、(ii)科学的方法の適用条件、(iii)現行実装との整合、(iv)CLI-onlyとProductの境界、(v)採否の権限、(vi)実装・検証可能性を審査する。指摘は`SR-01〜SR-12`で管理し、影響する`P1/P2/P3/X`行ID、差戻し理由、解消条件を記載する。

### 0.2. 結論と審査範囲

**差戻し対象は「スコープ案の未確定事項」であり、Phase 1〜3をCLI-onlyで追加する事業・科学的目標の否定ではない。**

- **妥当:** 既存PC/GES/LiNGAM/NOTEARS、Graph、Native Identification、ATE/ATT、E9 Diagnostics、Refutation/Sensitivity、現行CLIを再利用する。新FCI/EconML/Temporal/Quasiの候補を既存FRの「未実装」と誤認しない。
- **妥当:** 新機能のWeb UI/API/Worker/DB/migrationとPhase4を対象外にし、局所ManifestでProduct canonical lineageを閉鎖したとしない。
- **要修正:** 必須Methodの成立条件、エンドツーエンドに`問い→識別→推定/探索→診断→結果`が閉じることの証明、外部Library/platform・ライセンス、受入基準を記載する。
- **要承認:** 上位A0にのみあるATC/matching/g-computation等の対象外、Negative Control／未観測交絡Sensitivityの追加範囲、GAP-C01〜04の移管先をHuman ownerが確定する。

### 0.3. 証拠水準

現行正本[10_requirements_definition.md](../../../../requirement_definition/10_requirements_definition.md)のFR-035〜050、FR-051/054/086a/087b/095、NFR-001b/002/025/028、AR-004/005/010/023および§11を照合した。ソースは`src/ariadne/scientific/{discovery,identification,inference,refutation,sensitivity}/adapter.py`、`src/ariadne/interfaces/cli/{config_schema,scientific_stage,manifest}.py`、`pyproject.toml`を確認した。過去の受入や既存テストの**存在**は認めるが、今回のSHAで再実行していない。

外部APIの仕様は下記の公開upstream文書を**方法・依存制約の参考**として確認しただけで、現行環境でinstallできる・安定動作するとは認定していない。

- [DoWhy CausalModelの識別／推定API](https://github.com/py-why/dowhy/blob/main/dowhy/causal_model.py) と[Refutation API](https://github.com/py-why/dowhy/blob/main/dowhy/causal_model.py)。
- [EconML Estimator Reference](https://econml.azurewebsites.net/reference.html)（0.16系列の公開API一覧を含むが、ENH-E11採用版は未決定）。
- [Tigramite 公式README](https://github.com/jakobrunge/tigramite/blob/master/README.md)（PCMCI／PCMCIplus／LPCMCIの仮定表とGPLv3ライセンス表示）。

## 1. 68項目の完全性・追跡性審査

### 1.1. 歴史資料との行ID照合

| 対象 | 00_03の項目 | 00_04の項目 | 照合結果 |
|---|---:|---:|---|
| Phase 1 | 21 | 21 | **一致** |
| Phase 2 | 18 | 18 | **一致** |
| Phase 3 | 19 | 19 | **一致** |
| A0上位・横断 | 10 | 10 | **一致** |
| **合計** | **68** | **68** | **欠落0、余剰0、重複ID0** |

`00_04`の68行すべてに`R/Q/N/D`の処遇案とIssueの対応がある。**これは文書上の完全性のPASSであり、手法のAPI実行・科学的品質・必要十分性のPASSではない。**同一行に`R+N/D`が含まれるため、68を独立した新FR/実装Taskの件数へ換算しない。

### 1.2. 妥当と判定したスコープ境界

| 審査観点 | 判定 | 根拠 |
|---|---|---|
| 既存能力の再利用 | **PASS（方針）** | 現行Discovery registryはPC/GES/LiNGAM/NOTEARS、Native識別はRandomized/Backdoor、推定はATE/ATTとDiff/OLS/IPW/AIPW、既存Refutation/Sensitivityは2方式ずつ |
| 9月末除外候補の再分類 | **PASS（追跡）** | 8月Phase2/3を候補として復帰する方針を明記。正式要件改定は未実施 |
| CLI-only boundary | **PASS（方針）** | 新Web/API/Worker/DB/migrationなし。既存Product経路の回帰保護を要求 |
| 既存Foundation Gapとの分離 | **PASS（方針）／帰属未決** | ProductのGAP-C01〜C04をlocal CLI/Manifestで解消済みとはしない |
| 科学的方法の提供可否 | **未認定** | 外部Backendと採用版の互換性、方法別Benchmark、依存ライセンス等が未確認 |
| 実装スコープの正式採否 | **未承認** | 02にHuman ownerの承認記録なし。正本§11の未承認Engine除外規定は未改定 |

## 2. 修正要求と技術的な判定

### 2.1. 先行解消が必要な指摘（BLOCKER）

| 指摘 | 対象行ID | 内容／理由 | 対応を要求するもの |
|---|---|---|---|
| **SR-01：必須Scopeの承認境界** | P1-08/09/14/15/17、P2-02〜09、P3-02〜14、X-01/03〜06 | `N（要審査）`や`D（要承認）`が実装必須と同じ表で扱われている。上位A0とA1〜A3の不一致に対し「何を必須とするか」を判断者が追跡できても、**最終採否・代替の判定欄と権限が固定されていない**。 | Human ownerが**必須／条件付き／後続／不採用、例外理由、代替方法、追跡Issue**を行ID単位で確定する。技術審査はその決定の前提資料を用意する |
| **SR-02：外部依存・実現可能性の未検証** | P1-08/09、P2-02〜09/11、P3-02〜05 | 現行`pyproject.toml`はPython `>=3.12,<3.13`、pandas `>=3.0.2`等を要求し、DoWhy/EconML/Tigramiteを新しいoptional groupとしてまだ固定していない。外部資料でAPI名が見えるだけでは、**同時install、適合method、推論API、性能・実効version**を保証しない。TigramiteのGPLv3表示は配布・組合せ方針の確認事項。 | Python/OS/library lock/optional extrasのSupport Matrix、試験用環境でのimport・signature・最小fit/identify/refute probe、ライセンス利用・配布上のレビューを準備。法的適合を本書で断定しない |
| **SR-03：IdentificationとEstimationの接続契約** | P1-08/09/10、P2-09、P3-12 | 既存CLIの`identification/adapter.py`はCPDAG/PAGを`REQUIRES_REVIEW`とし、`inference/adapter.py`はDAG以外に数値推定を実行しない。FCIでPAGを出力できても**そのまま効果推定できるわけではない**。DoWhyのFrontdoor/IVで識別できても、**対応する推定器・estimand・結果の意味**が未規定ならUC-02/08は満たせない。 | FCI→PAG→review/追加仮定、User-defined DAGでの別識別、DoWhy Backdoor/Frontdoor/IV→適格性→対応するEstimator→Resultの**成功/非識別経路**を設計。Frontdoor/IV等で実装する推定方法を明示し、識別だけで「効果が推定できる」と認定しない |
| **SR-04：Methodごとの科学的実行契約** | P2-02〜09/14/16、P3-02〜16 | CATE推定器によってbinary/continuous treatment、nuisance model、CATE区間の可否が異なる。PCMCI、PCMCI+、LPCMCIも同じ因果仮定ではない。DiD、Event、RDD、IV、Syntheticにもdesign/estimand別に**成功条件・不適格条件・診断・数値閾値**が必要。現案の「各Methodを実行」は受入として不十分。 | `Method ID→Design/データ型→Estimand→識別仮定→推論/CI availability→負結果→Benchmark`を全Methodで固定。外部APIが期待結果を提供しない場合は科学的同等代替をHuman ownerへ差戻す |
| **SR-05：Scope例外とProduct Gapの帰属** | X-01/03/04/05/06/09、P1-18/19 | ATC、Matching、汎用g-computation、多重検定等はA0にあるが、D案に対する科学的理由・将来の所有Issueがまだ未承認。Product GAP-C01〜04も「#14で後で審議」では**閉鎖責任者と検証条件がない**。 | 02に**採用・後続理由、移管Issue、Owner、Closure Evidence/Gate**を記録する。未決のGapを`IMPLEMENTED`に変えない。Human判断なしの暗黙の例外処理は不可 |

### 2.2. 要件・設計化までに是正する指摘（MAJOR）

| 指摘 | 対象行ID | 内容／理由 | 要求する補足と検証 |
|---|---|---|---|
| **SR-06：Negative Controlの識別・反証上の位置** | P1-14/15/17、X-04/05 | **Random Common Cause**（ランダムな独立変数の追加）と**Unobserved Common Cause**（処置・Outcome双方に影響すると仮定した交絡の摂動）は異なる。Negative Control exposure/outcomeにも**有効なcontrolと想定する独立性/因果構造**が必要。単に乱数を生成すればNegative Controlとなるわけではない。 | 最小方式、入力の根拠、適格性、反証できる範囲、変化の尺度、seed/Result/失敗条件を方法ごとに確定。「Refutation PASS＝交絡不存在の証明」とは表示しない |
| **SR-07：CATE推論のCapability差分** | P2-02〜16 | EconMLのDML/Forest/DR/Meta/IV+MLを**共通Estimator入力にまとめても、すべてが同一のCATE/CI contractを提供するとは限らない**。補助学習のfold/split、分類処置、instrument、honesty/support/coverageをmethod別に扱う必要。 | 実効APIで`effect`、`effect_interval`等の可否をprobeし、提供不可はtyped`UNAVAILABLE`／`UNCERTAINTY_NOT_AVAILABLE`を設計。予測差と因果CATEを混同せず、個票Parquetをdefaultで無制限に出さない |
| **SR-08：Temporalの仮定とGraph忠実性** | P3-01〜06 | Tigramite公式の方法表では**PCMCIは同時点因果関係なし・潜在交絡なし**、**PCMCI+は潜在交絡なし**、**LPCMCIは潜在交絡を許す**等の前提が異なる（いずれもstationarity等を要する）。横断PAGとの相互変換だけではlag/endpointの意味を保てない。 | CI-test別データ適格性、lag/same-time/schema、Graph serialization、潜在交絡/時刻不整の成功・負例を方法別に定義。どのMethodがどの仮定を許すかを明示 |
| **SR-09：準実験のEstimator選択を明確化** | P3-07〜16 | DiDで導入時期が異なる場合、単純な2群2期/素朴なTWFEが十分とは限らない。Event Studyのevent-time、RDDの局所estimand、IV/LATEのcomplier条件、Syntheticのdonor重みは互換な出力ではない。 | パネル／cohort／cluster／bandwidth／first-stage／donor別に**使用する推定器・推論法・制約**を固定。並行トレンド等の仮定を「検定にPASSしたから真」とは主張しない |
| **SR-10：CLIとファイルの安全・再現性契約** | P1-02/18/20、P2-12/15/18、P3-17/19、X-09/10 | 現行`scientific_stage.py`の`runtime_versions`はPythonのみ、`backend_version`は固定値。出力ファイルの存在と、**入力・方法・seed/split・実効backend版を含むAtomic/portableなManifest**は別。新CLIで`dataset_version_id`等のProduct DBを必須にしない境界が要る。 | CLI config/schema version、method names、path検証、上書き/途中失敗、hashとeffective seed、backendの実使用version、個票CATE privacy、optional欠落時exit/status、read-backを定義 |
| **SR-11：IPTW推論の品質の誤認防止** | P1-11/12、X-06 | 既存`FR-047/048`はIMPLEMENTEDであり、E9診断は再利用対象。一方、**Propensity推定込みのSE/CI被覆**やclipping下のtarget estimandは、既存のrandomized diff試験だけでは立証できない。 | `ipw`/`aipw`、ATE/ATT、normalized/stabilized、clip/trim、overlapの組合せを分け、既知真値のbias/coverage/ESSをfreezeして検証。品質審査を既存FRの「全面未実装」と表示しない |
| **SR-12：スコープとAcceptanceの接続** | 全68行、UC-01〜10 | 01のUC→E11-AC-01〜08は方向性を与えるが、Methodごとの**方法固有の科学的negative result、既知真値fixture、環境/OS対応と閾値**までは凍結していない。 | `00_04行ID→UC→仮FR/NFR/AR→Design/Method→Issue→Gate→独立Benchmark`の追跡表。Gate 06/07の固定前に成功/負例・許容誤差・CI被覆・performance/依存条件を明文化 |

## 3. 審査対象のPhase別処遇案

### 3.1. Phase 1：基盤と識別・探索

- **暫定妥当（再利用）:** P1-01/03〜07/10〜13/16/20/21の**既存部分**。既存Graph、Native識別、ATE/ATT、E9、2種Refutation/2種Sensitivity、CLIを新実装扱いしない。
- **追加の科学的Capabilityとして審査継続:** P1-08 DoWhy、P1-09 FCI、P1-14 Random Common Cause/Bootstrap、P1-15 Negative Control、P1-17 Unobserved-confounding Sensitivity。
- **条件:** P1-08は**識別だけでなく対応する推定・反証の使用方法と負結果**を決める。P1-15/17は採否留保を残し、Human ownerが最小方式の採用可否を判断する。
- **Product Gap:** P1-02/18/19のDB資源やcanonical lineageはProduct側の継続案件として責任を分ける。

### 3.2. Phase 2：異質効果

- **必須候補は縮退させない:** LinearDML、CausalForestDML、DRLearner、ForestDRLearner、S/T/X Learner、DRIVまたは科学的同等IV+MLを個別に追跡する。
- **要修正:** それぞれに対応するTreatment/Outcome型、CATE定義、識別仮定、CI/inference、support/cross-fitting、出力と負結果を別々のCapability rowで確定する。
- **後続:** Paged Web/API/Worker/DBはD。個票CATEのローカルArtifactは個票出力ポリシーを先に決める。

### 3.3. Phase 3：Temporalと準実験

- **候補として保持:** PCMCI、PCMCI+、LPCMCI、DiD、Event Study、ITS、Sharp/Fuzzy RDD、IV/LATE、Synthetic Control/Synthetic DiD。
- **要修正:** Temporal method間の因果仮定差、CI test/data型、staggered DiDのEstimator、RDD manipulation、weak-IV、donor検証、方法別estimandと推論を固定する。
- **対象外を維持する方向:** RPCMCI/J-PCMCI+、Policy/Monitoring、旧Web/API/Worker/DB統合。ただし正式なオーナー判断は02へ記録する。

## 4. Human ownerへ提出する採否・承認判断票

### 4.1. オーナーの明示判断が必要な項目

| 判断ID | 承認すべき選択肢／要求 | 推奨する審査処遇 | 正式な決定・根拠の記録先 |
|---|---|---|---|
| **D-01：基本スコープ** | Phase 1〜3の列挙手法をCLI-onlyで必須とするか、例外・科学的同等代替を許すか | **採用を推奨、ただしSR-02〜04解消が前提** | 02構想承認記録／要件03 |
| **D-02：上位A0例外** | ATC、matching/g-computation、Simulated Confounder、Graph Perturbation、一般多重検定をDにするか | **提案のDを条件付き推奨**。方法別の省略理由・将来Issueを記録 | 02／#14 |
| **D-03：追加Refutation** | Negative Control exposure/outcomeとUnobserved-confounding Sensitivityを今回必須にするか | **現時点で未決**。最小Methodの科学的成立条件を定義して再審査 | 02／#16 |
| **D-04：外部Backend** | Python/OS/DoWhy/EconML/Tigramiteの組合せ、optional extra、許可されたmethod代替 | **互換性・ライセンス確認後に採用判断** | Architecture Review／02／#16〜#24 |
| **D-05：Product残存Gap** | GAP-C01〜C04をE11で閉鎖・別Enhancementへ移管・承認済み要件変更するか | **CLI-onlyとは別のOwner/Issue/Closure条件を付けて移管推奨**。現行Statusは維持 | 02／#14／移管先Issue |
| **D-06：科学的受入** | 各MethodのBenchmarkと負例、CI被覆/効果誤差、CLI provenance、privacy | **Gate 06/07の明示契約化を必須**。本審査ではGate固定しない | 要件03／設計04／整合性05／Gate |

**D-01〜06の「推奨」は技術審査側の見解であり、正式なオーナー判断・署名ではない。** 単に本書をGitHubへcommitしても、表の「未決」は承認へ移らない。

### 4.2. 00_04の修正完了とみなす条件

1. **SR-01〜05（BLOCKER）**それぞれに修正版の条項、根拠、審査者の応答が存在し、Human ownerの採否が必要なものは02に明示記録される。
2. **SR-06〜12（MAJOR）**は方法別科学的Contractと検証計画へ具体化される。後続文書へ引き渡す場合も責任者・期限・入力要件を固定し、曖昧な「後で検討」を残さない。
3. 00_03の68行と00_04の全行IDの**同数・同一対応を維持**し、削除/代替/追加は別の変更差分で説明する。
4. 既存正本FR/NFR/ARのImplementation Status、旧受入999、現在のコードの存在を混同しない。
5. 正本§11、Architecture Review、03〜05、Gate06/07の権威を越えて未承認の実装指示を発行しない。

## 5. 審査結果と後続の工程

### 5.1. 技術審査の判定

**判定：CHANGES_REQUIRED（修正要求）。**

**通過:** 68行の網羅性、既存実装と新Capabilityの区別、CLI-only／Product境界、Phase4分離。

**保留:** SR-01〜05のBlocker解消とHuman ownerのD-01〜06判断。現行文書だけで「最終採用スコープとしてAPPROVED」とはしない。

**要補強:** SR-06〜12の科学的・設計上のContractとBenchmark設計。これはPhase1〜3が科学的に不要という主張ではなく、**方法ごとの利用可能性・限界を確認してから実装契約に変換するための修正要求**である。

### 5.2. 次の作業順序

1. `00_04`にSR-01〜05の対応方針・例外表・Library support matrixを反映し、再審査する。
2. Human ownerが**D-01〜06の採否とScope例外・Product Gap移管**を決め、02に正式な判断時刻・理由を記録する。
3. その判断に基づいて構想01、要件03、設計04、整合性05、Architecture Reviewを改訂・承認する。
4. 数値・負例・依存versionの科学的受入ContractをGate 06/07へ固定し、その後にWork Packageとcoding可否を決定する。

**禁止:** 本書の判定をHuman owner承認、現行Requirement修正、Architecture Review完了、Gate 999 PASSと表示しない。
