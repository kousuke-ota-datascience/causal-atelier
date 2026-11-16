# ENH-E11 — DEC-SR04-08：Backend・Optional Dependency・uv.lock・License／Delivery（Owner正式個別採用記録）

**文書区分:** SR04独立技術判断記録。2026-11-16 Human ownerがDEC08-1〜8のA案をすべて明示採用。**正式FR/NFR/AR/ADR・Gate06/07・Coding開始・Science PASS・個別納入の法務承認ではない。**  
**策定日:** 2026-11-16 JST。**対象Branch:** prototype/ariadne_mvp。  
**状態:** DEC-SR04-08_A1_TO_A8_OWNER_ACCEPTED / ENV_DEPENDENCY_POLICY_APPROVED / DEPENDENCY_AND_LOCK_NOT_FROZEN / LICENSE_REVIEW_PENDING / SCIENCE_NOT_RUN / GATE07_NOT_FROZEN / PENDING_FULL_CONCEPT_APPROVAL。  
**先行Owner決定:** DEC-SR04-01〜07は個別採用済み。科学的Estimand・Method・Inference方針、DEC07のMonte Carlo計画は変更しない。  
**参照:** [02 Owner承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)／[SR-02 Backend実行証跡](20261101_sr02_backend_runtime_probe_results.md)／[SR04-E Environment Contract](20261115_sr04_execution_environment_contract_draft.md)／[SR04-F Gate07 Trace](20261115_sr04_gate07_traceability_draft.md)。

## 0. 基本結論：uv.lockは中心だが単独でEnvironment Contractにはならない

### 0.1. 実際のリポジトリのBaseline（2026-11-16のGitHub現物確認）

| 対象 | 確認した事実 | 何を追加する必要があるか |
|---|---|---|
| pyproject.toml | requires-python は >=3.12,<3.13。core dependenciesと既存predictive-advanced extra、dev/docs groupsが存在 | E11 Backend別Extraと採用するAPI version制約を宣言 |
| uv.lock | universal lock。既存base/predictive-advanced/dev/docsの依存解決結果がある | E11 extras定義後に再解決。Version、wheel/Sdist hash、metadata/lock整合・Profile別導入検証 |
| uv.lockの実効package | DoWhy、EconML、Tigramite、rdrobustのpackage entryが**ない**。既存causal-learn 0.1.4.8、lingam 1.13.0、numpy 2.2.6、scipy 1.13.1、statsmodels 0.14.6等 | SR02別環境で観測したstatsmodels 0.15.0と、現行uv.lockの0.14.6を**同一環境だと誤認しない** |
| SR02 GitHub Actions | Ubuntu24.04 / Python3.12.15 / x86_64の4 Job（DoWhyのみ／EconMLのみ／Tigramiteのみ／3者同時）はinstall/API smoke PASS | 試験時の個別python環境から現行uv.lockは変更されていない。科学Benchmark／各プロファイルfull lock／納入法務は未PASS |
| 本契約作成時 | pyproject.tomlとuv.lockは読取のみ | **今回の個別Owner方針採用は依存ファイル改変の実行承認ではない。**承認後の実装Work Packageで両ファイルを整合的に変更する |

**役割の分離:** pyproject.toml＝依存・環境要求の**宣言**、uv.lock＝platform marker込み依存集合の**解決結果**、Environment Profile＝実際に選択したextra／OS・Python・native ABI・BLAS等、Run Manifest＝その実行で使った実効版／Method config／seed／hash、Legal Gate＝特定成果物を特定受領者に配布できるかの審査。uv.lockだけで残りを代替しない。

## 1. DEC08の選択肢：8項目のOwner採用A

| ID | A案（採用） | B/C案の問題 | 今回状態 |
|---|---|---|---|
| **DEC08-1** | pyproject.toml宣言＋単一uv.lock解決＋環境Manifestを分離管理し、同一PRで差分・Lockを整合させる | uv.lockを直接手編集する／現行lockをE11依存導入済みと扱う | OWNER_ACCEPTED |
| **DEC08-2** | Ubuntu24.04 / Python3.12系 / x86_64 / CPUの候補を5既存Profileでpreflight、RDは追加のoptional profile候補とする | Python patch・GPU・macOS等を未検証で保証／各Profile検証を省略 | OWNER_ACCEPTED |
| **DEC08-3** | DoWhy・EconML・Tigramite・rdrobustのMethod別Backend/Estimatorを明示。SR02観測版は**候補のみ**、実効科学/互換性の採用条件付き | 全Methodのバックエンド一律化／旧API smokeをMethod科学PASSとする | OWNER_ACCEPTED |
| **DEC08-4** | E11 extrasを機能別に定義し、universal resolution・Combinedの適格性を必須検証。競合時はOwner/Architectureに差戻し | optional化＝必ず依存隔離と誤認、競合を許可したままCombined PASSとする | OWNER_ACCEPTED |
| **DEC08-5** | fresh venvでuv lock --check、uv sync --locked、uv pip check、profile isolation/legacy回帰を検証し、freeze済みcommitを記録 | --frozenをlock stale検証に使用／最新patch自動更新 | OWNER_ACCEPTED |
| **DEC08-6** | Seed/Method/backend/final model/env/BLAS/lock/wheel/Source SHA/RuntimeのManifestとSBOMを同時に管理 | seed＋uv.lockだけでbitwise結果再現やlicense provenanceを保証 | OWNER_ACCEPTED |
| **DEC08-7** | LGPL/MIT/BSD/GPLその他のライセンスを配布形態・artifact単位でReview。Tigramite/RDは法務判定前に**顧客Delivery BLOCKED** | GPLをoptional extrasにすれば義務無し／内部利用と顧客配布の区別無し | OWNER_ACCEPTED |
| **DEC08-8** | Env/Legal・Scientific・DEC07 Compute・正式Gateを別状態とし、Owner判断→Lock前提固定→T2 Pilot→T3→配布承認 | 科学PASS・uv lock成功・GPL法務承認を相互代用する | OWNER_ACCEPTED |

**正式判断:** Human ownerがDEC08-1〜8の**A案をすべて採用済み**。これは基準・設計方針の採用であり、未実測の実効依存版・release可能性・Legal approval・Coding承認を作らない。

## 2. DEC08-1：プロジェクト宣言とLockの整合

- core（現在のAriadneと既存v2）への追加を最小化し、E11の機能別BackendはOptional Extraとしてプロジェクトに明示する。既存predictive-advancedを無断変更しない。
- Method-specific API/意味が厳密な直依存については、**受入に用いる版をpreflightで確かめたうえで明示的なpinまたは厳しいversion constraintを採用**。推移依存は解決結果をuv.lockに保持し、適用wheelと環境の実効版を別途記録する。
- 依存とロックの変更は同一PR/commitで扱う。release候補のpyproject.toml SHA／uv.lock SHAをGate evidenceへ記載し、dirty working treeや自動更新でベンチマーク実行版がずれることを禁止。
- 実装順は **(1) SR02候補版から隔離resolution試作 → (2) package/API smokeとlegacy regression → (3) Bench前のBaseline Lock SHAをfreeze → (4) T2/T3 ScienceとLicense → (5) 受入版として批准**。**Science Benchmarkはlock済みの環境で実行する**。最終採用に至る前の候補lockと、Science検証後の承認済みlockを区別する。
- uvのuniversal lockは全extras/dev groupを同時に解決する。**Extraはinstall selectionであり、単独にConflictを解消する仕組みではない**。依存競合時にtool.uv.conflictsで相互排他宣言する案もあるが、Combinedを保証する要件とは矛盾し得る。Combined維持の可否をOwner判断のもと再設計する。

### 2.1. pyproject.tomlへの追加設計イメージ（**現在の実装ではない**）

~~~toml
[project.optional-dependencies]
# 既存predictive-advancedは維持。
e11-dowhy = ["dowhy==<validated-version>"]
e11-econml = ["econml==<validated-version>"]
e11-temporal = ["tigramite==<validated-version>"]
# RDは配布形態とGPL適合・Method科学Review後の別Extra
# e11-rdd = ["rdrobust==<validated-version>"]
~~~

**注記:** 上記の <validated-version> は設計上のプレースホルダーであり、**有効なバージョン制約を表す動作するTOMLではない**。GitHub実装にそのままコピーしないこと。実装時にはSR02で観測したDoWhy0.14、EconML0.17.0、Tigramite5.2.10.1を最初の検証候補とし、RDは別途実版・licenseを確かめる。Python実効patchとtransitive版が成立して初めて採用可。

## 3. DEC08-2：Environment Profile（既存5件＋条件付きRD候補）

| Profile（案） | ベース | 選択Extra | 必須の初期検証 |
|---|---|---|---|
| ENV-BASE | Ubuntu 24.04 / CPython3.12.x / x86_64 / CPU | E11追加無し | E9/v2回帰、Method非対応時のtyped unavailable、現行causal-learn/LiNGAM |
| ENV-DOWHY | 同上 | e11-dowhy | Identification/FD-A actual stage、旧CLI regression |
| ENV-ECONML | 同上 | e11-econml | CATE/DRIV-A、Inference availability/final model、nuisance |
| ENV-TIGRAMITE | 同上 | e11-temporal | PCMCI/PCMCI+/LPCMCI、CI-test/Graph endpoint、内部実験Only vs Delivery |
| ENV-COMBINED | 同上 | e11-dowhy + e11-econml + e11-temporal | universal resolutionと3者同時API/Science関連の干渉・旧CLI |
| **ENV-RD（追加提案・初期Profile5に含めない）** | 同上 | e11-rddを候補 | sharp/fuzzy RD RBC、実効Python API、GPL顧客配布法務、weak first-stage |

Ubuntu24.04、Python3.12.15、x86_64という値はSR02の**観測環境**。DEC08-Aはこの構成を**初期検証基準候補**として審議する決定であり、別OS/CPU/Python patch/GPU等の保証ではない。正式patch pinは実際のWheel可用性・Security update・Environment isolationと科学的再現性を検証してから定める。

**注意:** e11-econmlだけでも、その推移依存に特定の別Backendが現れる可能性がある。「Extraを選んでいない」ことと「任意packageが必ず未インストール」は同値でない。Profileの判定は**指定Methodの有効・無効と実効依存**に対して行う。

## 4. DEC08-3：Method↔Backend mapping・実効Config

| Method family | Backend候補 | SR02/DEC05時点で言えること | Science preflightで必要なこと |
|---|---|---|---|
| P1 identification/backdoor/FD-A | DoWhy | SR02ではID/backdoor API smoke PASS、frontdoor identifyのみ。FD-A数値は未検証 | DoWhy 0.14でM~1+A、Y~1+M+Aが実際に再現できるか、version/name、CI method |
| P2 7種非IV CATE＋DRIV-A | EconML | SR02 0.17.0で個別fit/effect smoke済。MetaLearner/DRLearnerにCI不可構成あり | final estimator・cross-fit・nuisance・projection/weights・MethodごとのCI |
| P3 PCMCI/PCMCI+/LPCMCI | Tigramite | SR02 5.2.10.1でAPI smoke。Graph Oracle SCIENCE未実施 | CI testごとの有効性、endpoint型/lag、独立PAG/CPDAG/temporal oracle |
| P3 Sharp/Fuzzy RD | rdrobust Python（**新候補**） | 公式にsharp/fuzzyとRBC。Ariadne採用版・API・Licenseは未検証 | cutoff、p/q、bandwidth、weak local IV、license/distribution |
| P1/P3 base methods／Quasi | NumPy/SciPy/statsmodels・独立実装候補 | Baseに既存依存があるが各新Methodは未実装 | DiD/ITS HAC、SCM最適化、SDID unit/time weights、cluster inference、独立Reference |
| SR03 B0/B1 weak IV／AR | Method-specに沿う独立adapter/NumPy/statsmodels候補 | 限定IV構造係数とAR topologyはOwner採用。Backend選定と科学CIは未完 | Wald/2SLS point、HC robust AR、unbounded/disconnected set、V2保護 |

**禁止:** Backendがfit可能というだけで、Estimator/Estimand/Inference適格性・分布仮定/Graph同値類・科学Passを認定しない。ARやSCM等の独立Referenceは、同一Backendの出力を丸写ししたOracleではない。

## 5. DEC08-4／5：依存Extra・Lock/CI acceptance

**基本コマンド候補（正式Extra未導入のため現段階では実行しない）:**

~~~bash
uv lock --check
uv sync --locked --no-dev
uv pip check
uv sync --locked --no-dev --extra e11-dowhy
uv pip check
uv sync --locked --no-dev --extra e11-econml
uv pip check
uv sync --locked --no-dev --extra e11-temporal
uv pip check
uv sync --locked --no-dev --extra e11-dowhy --extra e11-econml --extra e11-temporal
uv pip check
~~~

- **各Profileはfresh isolated venv**で実行する。共通.venvへ順次syncすると前のProfileのpackageが除去・入替えされ、Profile間の独立Evidenceにならない。
- uv lock --check と --lockedはpyprojectとlockの整合を確認しstale時に失敗する。**--frozenはstaleかを検査しないため、正式Lock acceptanceの代用に禁止**。
- uv syncは特に明示しなければdev groupが同期され得る。科学Runtime profileは--no-devを基準にし、pytest等の専用Dev profileは明示的に別定義。
- ENV-AC01/02/03/08をMethodごとに追跡。optional-disabledでMethodを誤実行させない、enabledの実効Backend versionが事前登録と不一致ならfail-closed、BASE/各単独/COMBINEDのlegacy E9/v2回帰は別試験。
- lockfile自体にOS shared library/BLAS実効linked version、CPU microarchitecture、Python patch build、RNGアルゴリズム、ライセンス法的審査結果は含まれない。環境Manifest/asset hashに保持する。
- Lockの責務は依存グラフ・packageバージョン解決であり、CVE/SBOM/License/Backend APIの合格は**別のEnvironment Acceptance**。

## 6. DEC08-6：Run Manifest・RNG・Artifact/SBOM

**必要な記録:** Git commit/dirty、pyproject/uv.lock hash、Platform/CPU/Python patch/build、extras、resolved distribution/wheel hash、effective versions、BLAS/LAPACK/threadpool、backend/Method/Inference API config、DGP/Graph/Question/Design/ReferenceSHA、seed derivation version/replicate/role、input/output data hash、R/CI availability、CPU core-second/Wall/RSS、artifact hash、Review/Owner/Gate refs。

- SR03 D04/E5の新CLI Result/Manifest Schemaを旧Product/v2から分離。既存legacy Resultを未承認で上書きしない。
- ENV-AC04/05/06/07ではparallel/shard/retry/seed/elapsedの再現性を区別し、ビット単位一致をあらゆるOS/BLAS/Backendへ拡張しない。
- 第三者インベントリはdirect/transitive両方、個別package SPDX ID、著作権・License文・配布方式、source/wheel hash、security/vulnerability確認を含める。SBOMはCycloneDX等の標準形式を候補とするが具体ツール/formatは別の実効検証を要する。
- **No unauthorized data export**：Science Fixtureは合成データを既定とし、顧客個票や秘密をCI Artifactに保存しない。

## 7. DEC08-7：OSSライセンス／顧客納入と法務ゲート

| Component | 現時点の一次資料上のLicense | 扱い |
|---|---|---|
| DoWhy | MIT | Copyright/License noticeを保持し、推移依存も棚卸し |
| EconML | MIT。ただしeconml.tree/grf等にBSD-3-Clauseの第三者由来Codeがある | MIT + 該当BSD noticeを同梱。具体受入Versionで再確認 |
| Tigramite | **GPLv3-or-later**（upstream READMEはv3または以降と記述） | 個別SIで顧客へwheel/container/sourceを配布・結合する形態とsource obligationを法務レビュー |
| rdrobust Python | **GPL-3.0-only**（PyPI metadata） | Tigramiteと別のGPL権利・版条件として個別レビュー。DRDのBackend候補であり、現行ロック・正式採用ではない |
| Python base/transitive dependencies | Mixed | uv.lockからの自動「全てMIT」推定を禁止。決済/顧客別配布物に含むソフトウェア全体をSBOMと法務で確認 |

**配布類型を分ける:**
1. **社内研究使用:** 配布・顧客へのcopyを伴わない場合は一般に対外的なGPLのソース提供義務が発生する状況と異なる（ただし社内規程・顧客データは別審査）。
2. **顧客環境への個別SI納入:** Ariadne wheel／container／コード等の結合・配布形態、GPL対象モジュール、ソース提供・著作権表示、顧客契約の再配布禁止条項を審査。**Legal Approvalまでdelivery-ready false**。
3. **サービスとして社内側で実行して結果のみ返却:** ソフトウェア納入とは論点が異なる。ただし実装実態／顧客権限等による判断が必要。Phase1〜3はCLI-only個別SI納入を想定しており、SaaS前提へ無断変更しない。
4. **GPL Backendを別Extraにする／顧客がpip installする:** 法的適合を自動保証しない。単なる同梱・Import有無で結合作品性を断定せず、実際のコンポーネント構造・受領者・契約を法務に提示する。

**選択肢（ライセンス懸念が確定したときの再審議）:** (A) 法的義務を満たす配布形態にする、(B) 当該Methodをローカル解析用に限り顧客配布から外す（Scope変更はOwner再承認）、(C) Apache/MIT等の代替Backendを科学的同等性とReferenceで評価し再承認する。GPLの法務レビューを飛ばすためにMethod名を維持して別Estimatorへ差し替えることは禁止。

**ENV-AC09の判定:** \`LICENSE_REVIEW_PENDING\`ではinternal scienceの有効性とは独立に\`CUSTOMER_DELIVERY_BLOCKED\`。法律上の最終判断は本提案で行わず、法務/契約/受領者・artifact SHAとOwnerを記録する。

## 8. DEC08-8：実装・Science・Resource・DeliveryのGate分離

| レベル | 事前条件 | 現状態 |
|---|---|---|
| DEC08 Owner Policy | DEC08-1〜8のA案すべてを02承認記録第25項に記録 | **OWNER_ACCEPTED** |
| SPEC/EXTRAS/LOCK | Architecture/OwnerがMethod↔Backend・extras名・候補版・Combined方針を採用し、pyproject+uv.lockをPR変更 | **NOT IMPLEMENTED** |
| ENV PREFLIGHT | fresh isolationの全Profileで--locked・pip check・smoke/legacy regression・Manifestを確認 | **NOT RUN under E11 Lock** |
| SCIENCE T2 Pilot | 採用ProfileとLock SHAでMethod別CPU/RSS/Inference・n/Tを実測、DEC07のResource予算に渡す | **NOT RUN** |
| SCIENCE T3 Acceptance | Method-specific oracle/Monte Carlo/ACとeffective Backend、Source SHAの一致 | **NOT RUN** |
| LICENSE/DELIVERY | 納入artifact・software combination・受領者・ソース提供義務を法務/Ownerが個別承認 | **NOT APPROVED** |
| Formal Gate | 68 Scope→FR/NFR/AR/Architecture、06/07、独立Review、Owner Snapshot | **PENDING_FULL_CONCEPT_APPROVAL** |

**今回の実施範囲:** 現行pyproject.toml / uv.lockとSR02 Evidenceを照合したBackend/Version/Extras/Legalの8件の設計案について、Ownerが明示的にすべてAを採用した。02承認記録第25項とSR04 E/F／統合レビューに接続する。**実際のpyproject.toml/uv.lock・Source code・Extra導入・lock生成・Runtime/Pilot/Science/法務審査は実施していない。**

## 9. Ownerの正式採用・実装前の閉鎖条件

**Owner正式決定：DEC08-1〜8のA案をすべて個別採用済み**。これにより正式なBackend/Lock/Licenseの設計方針は確定するが、**実効ライブラリの最終pin・全Profileのuv.lock成功・GPL納入法務・Science Pass・Coding許可**は別の未解決事項として残る。

後続の推奨順序：**DEC08 Owner判断（A×8採用）は完了** → DEC09 全体Scope/FR/Architecture/Gateの統合承認 → 承認済みWork Packageでpyproject.toml/uv.lockとEnvironment Manifestを更新 → 全Profile Preflight → 独立科学T2/T3／Legal Review → 配布承認。T2 Pilotの予算計測は正式なArchitectureと依存の組合せが決まった後に開始する。

## 10. 外部一次資料

1. [uv公式：ResolutionとOptional Dependencies](https://docs.astral.sh/uv/concepts/resolution/) — universal lockは全extras/groupsを一緒に解決、競合処理の制約。
2. [uv公式：Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) — --locked / --frozen、--extra、dev group、fresh envの挙動。
3. [uv公式：Command reference](https://docs.astral.sh/uv/reference/cli/) — --no-dev、uv pip checkなど実効CLIの照合先。
4. [DoWhy upstream LICENSE（MIT）](https://github.com/py-why/dowhy/blob/main/LICENSE)、[EconML upstream LICENSE（MIT＋BSD-3）](https://github.com/py-why/EconML/blob/main/LICENSE)。
5. [Tigramite upstream README](https://github.com/jakobrunge/tigramite/blob/master/README.md)・[LICENSE](https://github.com/jakobrunge/tigramite/blob/master/license.txt)、[rdrobust PyPI metadata](https://pypi.org/project/rdrobust/)。
6. [GNU GPL公式FAQ](https://www.gnu.org/licenses/gpl-faq.html) — linking/combined workと配布の扱い。**法律解釈の一般説明であり個別顧客配布の法務判断ではない**。
