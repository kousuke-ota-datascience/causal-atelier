# ENH-E11 — DEC-SR04-04：GRAPH-A（FCI／Temporal Graph Oracle）個別採用判断・科学的制約

**文書区分:** Human ownerの**個別設計判断**に対応する独立技術記録。正式FR/NFR/AR/ADR/Gate06/07、実装・Graph Science PASSの承認ではない。  
**判断日:** 2026-11-16（JST）。**判断主体:** Human owner（本ターンでGRAPH-Aを明示採用）。  
**個別判断:** `DEC-SR04-04_GRAPH-A_OWNER_ACCEPTED`。  
**科学的実装状態:** `INDEPENDENT_MAG_PAG_CPDAG_ORACLE_PENDING / TEMPORAL_ORACLE_PENDING / SCIENCE_NOT_RUN`。  
**全体状態:** `PENDING_FULL_CONCEPT_APPROVAL / GATE07_NOT_FROZEN`。  
**正本:** 採用事実＝[02 Owner記録](../00_enhance_background/02_enhancement_concept_approval_record.md)；技術根拠・限界＝本ファイル；Fixture/AC/追跡＝SR04 A〜F。  
**対応:** P1-M06 FCI、P3-M01 PCMCI、P3-M02 PCMCI+、P3-M03 LPCMCI、DGP-009〜011/021、NEG-003/021/028、REF-G02/G03、AC-D02/G01〜G06、ENV-BASE/TIGRAMITE、Issue #17/#20、PLAN:G01/G06。

## 0. 結論・採否と禁止する評価

| 案 | 内容 | Owner判断 | 非採用・制約 |
|---|---|---|---|
| **GRAPH-A** | 生成真値Graph、観測潜在射影、同値類Graph、時間ラグを**別々の独立Oracle**で検証 | **採用** | CPDAG/PAGの未確定向きを真DAGの矢印と比較して偽FAILを付けない |
| GRAPH-B | 生成DAGとFCI/LPCMCI/PCMCI+出力の全endpoint完全一致を常時要求 | 非採用 | Markov等価類で識別できない向きまで復元を要求する |
| GRAPH-C | 独立Oracleが難しいためGraph accuracyを受入から全廃 | 非採用 | Graph Discoveryという実装対象の科学的妥当性を未検証のまま残す |

**採用の意味:** Graph出力形式の忠実保持と、科学的な真値・同値類への接近を**別Acceptance**とする。GRAPH-AはGraph Oracleの評価原理を採用する決定であり、特定のPAG/CPDAG真値や初期正式Algorithm/Graph schemaを証明した決定ではない。

## 1. Graph Oracleの層・識別可能性

### 1.1. Oracle型と出力

| 層 | 具体的な対象 | 判定してよいもの | 判定してはいけないもの |
|---|---|---|---|
| `G0-SCM` | 介入/構造方程式の**生成真値DAG**（時間展開可） | 生成edge/lag/latent structureの仕様・物理的真値 | これだけで観測から全矢印が識別できると宣言 |
| `G1-LATENT` | 観測変数へのlatent projection（選択変数の無い初期保証ではMAG等） | m-separationに対応する潜在射影・祖先構造 | MAGの各arrowheadがPAGでも必ず強制されると仮定 |
| `G2-EQUIVALENCE` | 完全観測・因果十分ならCPDAG、潜在変数許容ならPAG | 同値類内で**強制されるendpoint／未決circle/tail/arrowhead** | 生成DAGと未強制方向の完全一致をHard Gateにする |
| `G3-TEMPORAL` | ラグ付き隣接・時間順序・同時点同値類、観測support/CI test | 過去→未来の固定方向、同時点の**識別可能な**方向/非方向、時系列PAG表現 | 真の同時点DAG方向を全て強制する |
| `G4-SERIALIZATION` | CPDAG/PAG/Temporal endpoint・lag・GraphVersionの保存/読戻 | 既知型・edge/endpoint/lag・hashのlossless 100% | 形式的なRound-trip成功をScience Graph Accuracy PASSと呼ぶ |

**仮定の登録:** causal Markov、faithfulness、acyclicity（同時点も必要ならDAG）、causal sufficiencyの可否、latent/selection variables、time order/lag上限、stationarity、CI-testのモデル適格性、missingness/aggregationに伴う失真の可能性を**Method別に登録**する。これらを単一Graph grammarで黙示補完しない。

### 1.2. 独立Oracle構築ルール

1. **小Graph・既知SCM**から生成真値を作成。Graph仕様・変数・latent/observed集合・time conventionを固定し、reference implementationとは異なる経路で理論チェックする。
2. **独立d-separation／m-separationテーブル**を構築。観測したすべてのconditional independenceが出ると言うのではなく、faithfulness下でのgraph-theoretic implicationを列挙。
3. 完全観測DAGは同じskeleton・unshielded colliderによりMarkov同値類を列挙してCPDAGの**強制端点**を求める（時間方向・背景知識の許容範囲は別記録）。
4. 潜在変数を持つDAGは、適切なlatent projectionおよびMAGのMarkov同値類からPAGを導出。**Markov equivalentな各候補MAGの合法性の証明**とendpoint consistencyを必要とする。FCI自身の出力を真値Referenceにしない。
5. Temporalの場合、時系列展開とstationarity/time order/lag制限、同時点方向の制約を反映。単に静的PAGアルゴリズムを時系列に適用した結果をLPCMCIの真値とみなさない。
6. `OracleCI`（Tigramite）・外部参照実装は補助的**crosscheck**として利用できるが、同じDiscovery Backendの出力を自己検証の最終正解とする循環を禁止。独立数式・小Graph列挙をprimary truthとする。

### 1.3. 機械的に識別できない方向の具体例

- **未遮蔽collider:** 観測3変数で`X→Y←Z`かつ`X-Z`の隣接なし、faithfulnessなどの適切な条件下では、YへのarrowheadがMarkov同値類で強制される。完全観測CPDAGの基本正例候補。
- **chain/fork同値:** 同じ3変数の`X→Y→Z`と`X←Y→Z`は（当該条件下で）同じskeletonとunshielded collidersを持ち、通常の観測CIでは方向を区別できない。生成DAGの中間方向を完全復元する義務を課さない。
- **潜在共通原因の2変数例:** `H→X,H→Y`の同時点観測2変数で、潜在Hに由来する関連を、観測CIだけで常にbidirectedに向けることはできない。直接X→Yなど観測的に等価なモデルがあり、**DGP-011の2観測変数をFCIの完全latent識別の正例にしない**。

後者に対しては、**独立同値類導出により強制endpointが存在すると証明された多変数Motif**を別variantとして構築する。現段階では、その具体的なMAG/PAGと強制endpointを発明して「正解」として採用しない。DGP-021の追加variantを候補とするが、正式DGP IDやOracle acceptedとはしない。

## 2. FCI／PCMCI／PCMCI+／LPCMCIのMethod別保証対象

| Method | Fixture／Reference | 初期科学検証の主眼 | 残余必須事項 |
|---|---|---|---|
| `P1-M06` FCI | DGP-011（uncertainty/stress）、DGP-021追加motif候補、REF-G02 | latent-allowed PAGのskeleton、**同値類で強制されるendpointのみ**、circle保存 | 独立PAG/m-separation Oracle、FCI CI-testと有限標本失敗率 |
| `P3-M01` PCMCI | DGP-009、REF-G03 | time-lagged parents/CI-test size/graph structure。因果十分・stationary VARの限定正例 | lag上限、burn-in、CI-test、stationarity、FPR/Recall、time indexing |
| `P3-M02` PCMCI+ | DGP-010、REF-G02/G03 | lag + contemporaneous adjacencyと時間CPDAGの**強制された同時点向き** | temporal Markov equivalence oracle、lag0 orientation、conflict handling |
| `P3-M03` LPCMCI | DGP-011、REF-G02/G03 | latent temporal graphのPAG endpointとuncertaintyの忠実性 | latent temporal PAG Oracle、実効Tigramite版のalgorithm status、inference/CI test |
 
**Temporalの重要な区別:** `time`は「全向きが自動決定する」根拠ではない。遅延関係には時間順序の制約があるが、同時点の識別性はMarkov等価類・仮定に依存する。

## 3. Acceptance・Negative・Evidenceの科学的境界

### 3.1. 科学・契約Acceptanceを分ける

| Acceptance | 必要な基準 | Gateの制限 |
|---|---|---|
| `AC-D02`／`AC-G01` | Known Graph type/lag/endpoint/GraphVersionの**lossless serialization/round-trip** | 形式・忠実性テストとしてOracleから分離。100%の定義済みcase一致 |
| `AC-G02` | CI testのnull calibration、stationarity・conditional independence assumptions | 適格なnull designが存在するときのみsize。候補の定量閾値はSR04-D参照 |
| `AC-G03`／`AC-G05` | Adjacency precision/recall/FPR/SHD/lag recovery、replicate-level MC uncertainty | DGP/CI test/Oracleが有効でsignal条件を固定したときに評価 |
| `AC-G04`／`AC-G06` | **oracle強制endpointのみ**orientation fidelityと不確定性を評価 | PAG/CPDAG Oracle未導出ならScience orientation **BLOCKED**。生成DAG全arrowheadの復元を要求しない |
| `SR03-D06` | Graph再固定は**新GraphVersion**・編集根拠・親子lineage・再識別。未識別をoverrideで推定可へ昇格禁止 | Graph accuracy合格＝Causal Effectの識別/推定を許可、ではない |

**Accuracyとlosslessを区別:** 保存したGraphの全endpointが再読込一致することと、そのGraphが真の同値類に近いことは別の命題。両方必要であり、いずれか片方でGraph Science PASSにしない。

### 3.2. Negative/stress

- `NEG-003`: PAG/CPDAGのcircle・unoriented edgeをDAG化して保存したり、識別済み状態へ勝手に変換することを拒否。
- `NEG-021`: timestamp重複、欠測・非定常、CI test model misspec、lag誤解を区別。欠測/非定常の単なる存在を無条件に必ず拒否するのではなく、選定したMethodとMissingness処理の適格性に従う。
- `NEG-028`: GraphVersion親子lineage破壊、編集理由欠落、旧PAG方向のlossを拒否。
- **理論上のstress:** MAGは真であってもPAGはcircleを含み得る。Graph Discovererが生成MAGの「正しい向き」を一意に決めないことをfalse negativeとしない。

### 3.3. Science evidence未生成／正式freezeの前提

評価セルに、Graph truth/latent projection/CPDAG-PAG Referenceの証明、DGP generator SHA、`n/T/burn-in/tau_max`、CI testの名称とkernel/param、`pc_alpha`、失敗分母、seed/crossfit、API/BLAS/CPU・effective package version、MAC/endpoint definitions、GraphVersion hash、oracle proof version、Monte Carlo R/K/MCSEを必須記録。Tigramiteの個別SI顧客納入GPLv3 reviewは**科学Graph accuracyとは別のLegal Gate**。

**現時点:** Graph Oracle設計原則をOwner採用しただけで、独立PAG/CPDAG/temporal Oracle未構築、`AC-G04/G06`の本受入不可。GRAPH-Aを採用した結果、Graph Science PASSに必要な独立Oracleを**削除せず明確にした**。

## 4. SR-03 D06／SR-04の境界・残余Blocker

| 項目 | 新状態 | 解消に必要なこと |
|---|---|---|
| DEC-SR04-04 GRAPH-A判断 | **OWNER_DECISION_CLOSED** | 02 Owner記録と技術記録の一致 |
| Graph Oracle構築・科学的同値類 | **SCIENTIFIC_ORACLE_PENDING** | MAG/PAG/CPDAG・temporal等価類の独立導出とReview |
| FCI/Tigramite実効API・依存の採用 | **BACKEND_AND_VERSION_PENDING** | Library/CI-test/Graph schema/optional lock・Method別integration smoke |
| Graph Accuracy／Monte Carlo | **SCIENCE_NOT_RUN** | G02〜G06の真値・R/n/T/seed/閾値のfreezeと独立検証 |
| 正本FR/NFR/AR・Gate07 | **PENDING** | SR04-F trace・Architecture/Ownerと批准Snapshot SHA |

**先行D06は不変:** CPDAG/PAG不確定方向の偽DAG化禁止、研究者のGraph再固定は新GraphVersion、別識別証拠は科学的に検証可能でなければならず、初期の汎用PAG identification/partial identification推定器は採用しない。**Graph Oracle作成は科学受入試験用であり、初期Productに一般化識別エンジンを追加する判断ではない。**

## 5. 外部一次・公式根拠

1. [Tigramite 5.2公式Documentation](https://jakobrunge.github.io/tigramite/) — PCMCI/PCMCIplus/LPCMCIの範囲、PCMCI+の同時点方向と同値類。
2. [Tigramite pcmci.pyの公開実装](https://github.com/jakobrunge/tigramite/blob/master/tigramite/pcmci.py) — `graph` endpointとtime lag、`pc_alpha`などの実効Config解釈の参考。masterブランチは採用版5.2.10.1の同一挙動を保証しない。
3. [pcalgのFCI/PAG公開技術仕様](https://search.r-project.org/CRAN/refmans/pcalg/help/fci.html) — PAGのcircle/tail/arrowhead、潜在交絡許容、等価類。
4. [SR03-D06のOwner採用方針](20261115_sr03_d06_graph_uncertainty_identification_override_decision.md) — GraphVersionとfail-closed。
5. [SR04統合レビュー](20261116_sr04_af_integration_review_and_blocker_resolution.md) — GRAPH-A/B/C比較・DGP-011の科学的注意。
