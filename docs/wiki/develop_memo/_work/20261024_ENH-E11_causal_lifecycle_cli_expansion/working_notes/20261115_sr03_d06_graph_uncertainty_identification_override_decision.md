# ENH-E11 — SR03-D06：CPDAG/PAG不確定性・部分識別・Graph再固定・Overrideの科学契約

**文書区分:** working_notes／個別Human owner採用判断・技術比較・科学的制約の管理正本。正式FR/NFR/AR、Architecture Review、Gate 06/07、Coding許可ではない。  
**判断日:** 2026-11-15（JST）  
**判断状態:** `SR03-D06_BBBBBA_OWNER_ACCEPTED / METHOD_SPECIFIC_SCIENCE_PENDING / FORMAL_SCHEMA_PENDING / SCIENCE_NOT_RUN`  
**審議ベース:** `prototype/ariadne_mvp`、記録着手時HEAD `c70ae48462416fcf792a4bd247d4538abe5b1ca3`。固定済み承認Snapshotではない。  
**対象:** SR-03／SR-04、00_04 P1-04/P1-09/P1-08、Phase3のGraph Fidelity、E11-REQ-P1G/E11-REQ-SR03D06、Issue #16/#17/#24。

## 0. 目的・他の採用判断との関係

CPDAG/PAGには方向未確定や潜在交絡可能性があり、**Graphが未確定であることと、対象Estimandが（適切な識別条件の下で）識別できるかは別問題**である。一方、任意のCPDAG/PAGをDAGに自動補完してEffect Estimatorへ流すことも、研究者の注意警告を飛ばして未識別の点推定を表示することも禁止する。

本書を**D06の選択肢比較・科学根拠・非採用理由・受入/負例fixtureの唯一の管理先**とし、オーナー採用事実は[02構想承認記録](../00_enhance_background/02_enhancement_concept_approval_record.md)へ、要件/設計/traceabilityは03/04/05、SR-03進捗は[SR-03総合契約](20261101_sr03_identification_estimand_estimator_contract_review.md)へ要約する。

**先行採用と非衝突:** D04-2 E2（method別fail-closed）、D04-3 M2（lineage/hash）、D04-5 R2（旧Product/v2 override回帰保護）、D05（点推定・推論・科学受入分離）を維持。D06は新E11の例外受入条件と初期実装範囲を定めるもので、旧Product/v2を遡及変更しない。

## 1. コード照合と科学的境界（観測できる事実）

| 対象 | 現行コードで確認できる事実 | 判断上の制約 |
|---|---|---|
| `product/domain/enums.py` | GraphTypeはDAG/CPDAG/PAG、GraphVersionStatusはDRAFT/FIXED、ScientificStatusにはIDENTIFIED/NOT_IDENTIFIED/PARTIALLY_IDENTIFIED/REQUIRES_REVIEWが存在 | Graph種別・識別状態を区別できるが、これだけで新E11の識別証明は成立しない |
| `product/domain/graph_semantics.py` | GraphTypeごとのendpointペア検証。CPDAGの無向、PAGのCIRCLEなどを保持する | Endpointを消してDAGに偽装しない。検証は全ての意味論的妥当性の数学的証明ではない |
| `product/domain/graph_version.py` | GraphVersionがparent_graph_version_id、source_result_id、graph_origin、provenance_json、edit_rationale、statusを持ち、FIXED後の編集を拒否 | 新GraphVersionによる改訂・由来記録と整合。ただしGraphVersionをFIXEDにする操作は因果的正しさの検証ではない |
| `scientific/identification/adapter.py` | Nativeは非DAGでUNRESOLVED_GRAPH_ORIENTATIONのreasonを記録しREQUIRES_REVIEWを返す | 現行Nativeは「CPDAG/PAGを使った一般化識別」ができない。科学的に常に識別不能という証明ではない |
| `interfaces/cli/estimation.py`（D04照合済） | upstream REQUIRES_REVIEWを入力として許容する分岐があるが、非DAGは現行下流adapterに拒否される | 入力許容＝任意非識別への数値出力ではない。新E11に限って別の厳密なゲートを構築する |

**科学的な区別:**
- CPDAGは観測条件・仮定下での同値なDAGの集合を表す。方向未確定でも、対象効果について一般化調整基準などの識別可能な場合がある。
- PAGは潜在交絡・選択等を含むモデルクラスを表現し得る。PAGをDAGへ変換することは「形式変換」ではなく追加仮定を課す科学判断になり得る。
- IDA等が返す「可能な効果の候補集合」と、一般の非パラメトリックな部分識別集合、及び信頼集合は無条件に同一ではない。
- Graph・識別式を構成できたことは、識別仮定が現実に正しいことや点推定器が適切であることの証明ではない。

**方法論の一次資料:** [Perković et al. (2015), *A Complete Generalized Adjustment Criterion*](https://proceedings.mlr.press/r13/perkovic15a.html) および [Perković et al. (2018), *Complete Graphical Characterization and Construction of Adjustment Sets in Markov Equivalence Classes of Ancestral Graphs*](https://jmlr.org/papers/v18/16-319.html) はDAG/MAG/CPDAG/PAGの共変量調整の必要十分条件を扱う。[Maathuis, Kalisch & Bühlmann (2009), *Estimating High-Dimensional Intervention Effects from Observational Data*](https://doi.org/10.1214/09-AOS685) は同値類のDAGごとの介入効果の候補集合（IDA）を扱う。**一般化調整で識別できないことは他のあらゆる方法による識別不能の証明ではない**し、候補集合は無条件に一般の部分識別集合・CIに等しくない。原著による理論的存在は、Ariadneに当該Methodが実装・検証済みである証拠ではない。対象Graphクラス・介入の定義・潜在交絡と選択の条件をMethodごとに追跡する。

## 2. D06-1：未確定Graphからの推定許可 — B採用

| 案 | 内容 | 評価 | 判断 |
|---|---|---|---|
| A | CPDAG/PAGでは永続的に一律禁止 | 単純だがGraph不確定でも識別可能なケースを捨てる | 非採用 |
| **B** | **Method固有で検証済みの識別根拠がある場合のみ例外として推定候補へ進める** | 理論上の識別可能性と実装安全性を両立 | **採用** |
| C | 未確定Graphを警告付きでそのまま推定器へ流す | 未識別の点推定を生む | 非採用 |

**新E11の不変条件:** 識別証明のない`REQUIRES_REVIEW`/`NOT_IDENTIFIED`/`PARTIALLY_IDENTIFIED`を直接点推定に接続しない。例外はD06-2の認定済み・対象固有の識別証明により**新しいIdentificationResult**が出て、そのResultとEstimatorSpecのmethod別適格性・lineageを再照合した場合だけ。元の未確定Graphや旧Resultを自動的にIDENTIFIEDへ書き換えない。

**初期実装範囲との整合:** Bは**将来受け入れられる識別証拠の意味契約**。D06-6=Aの初期実装で一般化識別証明エンジンや無監督の外部proof importを実装する意味ではない。初期の運用経路は研究者のGraph再固定→再識別に限定し、将来の別証明経路はMethod別検証・追加承認後に開放する。

## 3. D06-2：別識別証拠の要件 — B採用

| 案 | 内容 | 判断 |
|---|---|---|
| A | 研究者の「識別可能」という宣言のみで承認 | 非採用 |
| **B** | **検証可能な対象・Graph・仮定・Methodに紐づく識別証明**を要求 | **採用** |
| C | Backendの`success=True`や内部Estimand名をそのまま採用 | 非採用 |

別証明の候補情報（**正式field名は未承認**）：
1. `estimand_kind`、対象集団・介入contrast・識別の対象単位、識別式／調整集合／必要な条件。
2. Graphの`graph_type`、graph hash、元GraphVersion、可能なDAG/MAG集合の取り扱いと、method適用可能な範囲。
3. 前提仮定と利用者が説明する根拠（例：時間順序・背景知識・潜在交絡の制限・一般化調整条件）。
4. 理論Reference/algorithm+version、validation result、未確定/不適格のreason、provenance、Question/Design/Dataset hash。
5. `EstimatorSpec`への数値推定許可は別判定。識別可能でもEstimatorの一致・データ適格性が無ければ点推定不許可。

**未決の承認ゲート:** 証明器の実装・各Algorithmの範囲、手動証明の第三者再現性、Method-specific fixtures、利用者/Reviewer権限、機械的validationをどこまで可能にするかはSR-04／Architecture Reviewへ送る。本人の宣言だけでは証明と見なさない。

## 4. D06-3：研究者によるGraph再固定 — B採用

| 案 | 内容 | 判断 |
|---|---|---|
| A | 元のDiscovery Graphに上書き | 非採用 |
| **B** | **別のGraphVersionを発行し、追加仮定・親子関係を保存して再識別** | **採用** |
| C | 未確定端点を自動方向付けして自動推定 | 非採用 |

新GraphVersionの作成では、`parent_graph_version_id`、`graph_origin`、`edit_rationale`、`provenance_json`、Graphのhash、編集者・根拠、旧/新GraphVersionの関連を保持し、`DRAFT→FIXED`の固定操作と識別判定を分離する。旧Discovery/CPDAG/PAGを上書きしてはいけない。

**追加の科学的条件:** CPDAGからのDAG選択は、元のMarkov同値類・背景知識との整合性、閉路不在などを確認する。PAGから潜在交絡を除外してDAGを作る行為は、元PAGの機械的な「等価変換」ではなく**追加仮定を明示した別のモデル**である。正しいと保証してはならない。`FIXED`は版の不変化であり真理性の保証ではない。新Graphを参照して新たな`IdentificationResult`を発行し、下流hash・eligibilityを照合する。

## 5. D06-4：部分識別の保存 — B採用

| 案 | 内容 | 判断 |
|---|---|---|
| A | 部分識別は状態のみ保存し、将来の境界表現を除外 | 非採用 |
| **B** | **識別集合・境界が科学的に定義できた場合、点推定と異なる専用Resultに損失なく保持** | **採用** |
| C | 境界の中点や任意代表値を点識別推定値へ昇格 | 非採用 |

**科学的意味契約:** 部分識別集合`Theta_I`は単なる`confidence_interval`ではない。識別集合（母数の集合値の識別）と、その集合に対する統計的なconfidence region、D03 G2の弱IV AR confidence setをそれぞれ分離する。集合は単区間に限らない可能性を残す（有限和・複数候補・多次元などの対応はMethod別）。単に`PARTIALLY_IDENTIFIED` enumが既存にあることを理由に境界算出を主張しない。

**初期実装:** D06-6=Aにより**一般的な部分識別境界推定器は初期の追加実装対象外**。識別集合・境界が認定済みMethodで得られた場合に保持可能な**将来の型と責務**を方針採用する。未算出の境界を生成・保存したことにしない。専用Result/enumの正式設計は将来の別審査。

## 6. D06-5：Human overrideの権限 — B採用

| 案 | 内容 | 判断 |
|---|---|---|
| A | あらゆる警告のoverrideを一律禁止 | 非採用 |
| **B** | **科学的識別を損なわない緩和可能な診断警告のみ、根拠付きoverride許容** | **採用** |
| C | 未識別・方向不確定をoverrideで強制点推定へ通過 | 非採用 |

| 条件 | 新E11での扱い |
|---|---|
| 軽微でMethod別に緩和許容を定義済みの`WARN` | 根拠・actor・effective parameter・対象Result参照を記録した場合のみoverride可能 |
| `REQUIRES_REVIEW`、識別式/対象に必要な根拠の欠落 | overrideによる識別成立は禁止。新Graph/認定証明で新IdentificationResultを発行 |
| `NOT_IDENTIFIED` | overrideで点推定へ昇格しない |
| `PARTIALLY_IDENTIFIED`（点識別なし） | 代表値を自動点推定へ昇格しない |
| upstream Question/Design/Graph/Dataset/hash mismatch | Contract Error。override不可 |
| DAG/PAG間の無断自動変換、MethodのEstimand不一致、必要Instrument不足 | Hard eligibility/semantic error。override不可 |

**レガシー互換:** 既存Product/v2のREQUIRES_REVIEW＋validation_override運用はD04-5 R2により変更せず、別経路回帰で保護。新E11のoverride権限を旧Productへ無条件適用しない。正式role/RBAC、reason enum、CLI exit codeはArchitecture Review待ち。

## 7. D06-6：初期実装の範囲 — A採用

| 案 | 初期の追加Capability | 判断 |
|---|---|---|
| **A** | **CPDAG/PAGの忠実な保持→review、研究者の根拠付き新GraphVersion固定→新Graphで再識別。一般化識別・集合推定エンジンは後続審査** | **採用** |
| B | 初期から限定的なCPDAG/PAG一般化識別アルゴリズムも実装・検証 | 非採用（初期） |
| C | 初期から一般的なGraph同値類の識別・効果集合・不確実性推定を実装 | 非採用（初期） |

**実装範囲と科学可能性を分離:** Phase1のFCI/PAG出力は保持する。初期の標準数値推定経路は、研究者の追加科学仮定によって新GraphVersionを作成し、採用済みD04の新識別・Method eligibility gateを通過したもののみ。数学的にCPDAG/PAGから効果が識別可能な例が存在することは認めるが、その**自動識別Capability**を初期追加提供の保証には含めない。

**後続拡張のTrigger:** 明確な対象Estimandとユースケース、適用するCPDAG/PAG同値類と識別定理、独立Method評価、失敗例、計算上の複雑性、versioned Result、SR-04/Gate07の合格基準、Human ownerの個別スコープ採否。Graph不確定からの汎用な「単一値への補完」実装は認めない。

## 8. Human ownerが採用した6件（2026-11-15）

| 決定ID | 選択肢 | 個別採用方針 | 未承認の具体化 |
|---|---|---|---|
| D06-1 | **B** | 検証済み別識別根拠があれば将来例外許可。ただし未識別Resultは直接通過不可 | Proof backend適格性／検証方式 |
| D06-2 | **B** | Estimand×Graph×仮定×Methodに紐づく検証可能な識別証明 | Formal proof schema/acceptance |
| D06-3 | **B** | 新GraphVersion＋根拠/lineage＋新識別結果 | Graph整合アルゴリズム・具体schema |
| D06-4 | **B** | 正当化された部分識別集合を専用Resultに保持する将来契約 | 境界推定器・集合schema/coverage |
| D06-5 | **B** | 緩和可能なwarningのみoverride、硬い識別条件の解除不可 | role・reason enum・CLI semantics |
| D06-6 | **A** | 初期はGraph保持／review／研究者の再固定／再識別。自動一般化識別・集合推定は後続 | 拡張Method採否、Gate、実装 |

**Human ownerの明示指示:** 「推奨案を採用する」（直前のD06推奨：B / B / B / B / B / A）。この表が採用のスコープである。初期実装にCPDAG/PAG専用自動識別器や包括的部分識別エンジンを含める承認ではない。全体68行スコープ案の正式承認にも該当しない。

## 9. SR-04／Gate07へ引き渡す検証候補（未実行）

| Fixture ID | 入力／反例 | 期待する科学・実装契約 |
|---|---|---|
| D06-T01 | 同一CPDAG/PAGをsave/read | circle／tail／arrowなどendpoint fidelity、GraphType/lineage不変 |
| D06-T02 | PAG/CPDAGで未識別／要reviewの状態 | 新E11推定へ自動進入しない。旧v2とは回帰を分離 |
| D06-T03 | 未確定Graphに適用可能な理論的調整条件の正例 | 将来Method導入前は未実装扱い。認定済み別証明＋新Result経路でのみ候補許可 |
| D06-T04 | Backend successフラグ／研究者宣言だけ | 認定識別証明とせず推定拒否 |
| D06-T05 | Discovery CPDAG→研究者新DAG、根拠明示 | 元Graph不変、parent/actor/edit rationale、Graph/Design hash更新、新識別 |
| D06-T06 | PAGから潜在交絡を勝手に除去したDAG | 自動「等価変換」としない。新しい強い仮定としてレビュー対象 |
| D06-T07 | 制約不整合または閉路付きDAG | 新GraphVersion／Identificationの固定または推定が失敗。理由分類 |
| D06-T08 | PARTIALLY_IDENTIFIED＋境界なし | point estimateへ昇格禁止。算出していない集合を生成しない |
| D06-T09 | 識別集合と95%信頼集合、AR confidence setを混同した入力 | Result type／科学的意味を分離、誤変換拒否 |
| D06-T10 | 未識別Resultへwarning override投入 | 推定拒否。緩和可能WARNだけ根拠を残し許可 |
| D06-T11 | Graph/Question/Design/Dataset hashの食い違い | D04のstrict lineage gateで拒否 |
| D06-T12 | 旧Product/v2のREQUIRES_REVIEW＋override既存fixture | 旧経路を遡及変更しない回帰を実測 |
| D06-T13 | 研究者Graph改訂後の新DAGを対象にBackdoorを再識別 | 通常識別契約で認定可能。Graph FIXEDだけでは識別済みとしない |
| D06-T14 | 未対応の一般化調整・IDA・partial-ID指定 | 初期Aスコープでは`NOT_SUPPORTED`等の正式未定コードで、架空の効果を出力しない |

**科学的受入は未実施。** 各fixtureの既知真値・Graphの数学的正当性・Method-specific acceptance・Graph migration・versionと契約schema、positive/negative coverageはSR-04／Architecture Review／Gate07で固定する。

## 10. 残余・次工程

- **D06個別方針の判断は完了:** B/B/B/B/B/A（2026-11-15）。
- **SR-03のD01〜D06の個別方針決定は完了:** D01 IV独立family、D02 Frontdoor数値、D03 A+B0+B1・AR/G2/C後続管理、D04 V2/E2/M2/G2-Bridge/R2、D05 BBBBB、D06 BBBBBA。**SR-03全体のScience PASS・正式schema/FR/NFR/AR・Design/Gate承認を意味しない**。
- **後続:** SR-03残余仕様と科学的検証事項の引渡し、SR-04のMethod別科学Acceptance設計、SR-01〜12 blocker/majorの是正、68行Scopeの再審査、Architecture Review、承認Snapshot、Gate06/07とWork Package freeze。Codingはこれらを通過するまで禁止。
- **Product/UI/API/Worker/DB:** E11への新規統合はしない。旧Product/v2契約は別の回帰確認とする。
