# 22_20 — ENH-E11 Local Scientific CLI：System Boundary & Authority

**State:** `BD01_REVISED_DESIGN / OWNER_ARCHITECTURE_POLICY_ACCEPTED / INDEPENDENT_REVIEW_PENDING / IF_DD_SCHEMA_UNFROZEN / NOT_IMPLEMENTED`  
**Date:** 2026-11-16. **Authority:** [DEC-SR04-09](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md), [formal RD-03 trace](../96_rd03_formal_requirement_traceability.md), [RD-04 audit](../98_rd04_consistency_verification.md). 本文のPort名・層は論理的な責務名称であり実装済Class/Schemaを意味しない。

## 1. 決定を反映したSystem Boundary

```text
Existing Product lane (unchanged)                 ENH-E11 local lane (new, independent)
Web UI → Web API → Product Application             CLI / local config & data
          ↓                                                   ↓
       Product Domain                               Local Application / Preflight
          ↓                                                   ↓
Product DB / Worker / Execution lifecycle           Local Scientific Domain / Identification
          ↓                                                   ↓
      Product Scientific Adapter                       Method Scientific Port
          ↓                                                   ↓
  Canonical Product Result / Artifact                 Optional Scientific Adapter
                                                               ↓
                                                  Local Result + Local Artifact Publisher
                                                               ↓
                                                  JSON / Parquet / Manifest + readback

        Both may reuse scientific algorithms/interfaces only via compatible Ports.
        Neither lane silently writes or upgrades the other lane's canonical state.
```

- 左は既存Productの説明でありE11の改修対象外。旧`causal-analysis-spec/2`、Execution/StageExecution、Worker、Project DB、Navigation、Product Web APIの意味を維持する。
- 右は**Local CLI → Local Application → Scientific Domain/Ports → Method別Adapter → Local Artifact**。E11を追加するためにWeb APIを経由させず、Product Execution ID／Project Membership／DB connectionを必須入力にしない。
- 両レーンでアルゴリズムの共通化は許すが、**Productの永続正本をLocal Manifestで置換しない**。独立のauthorityとprovenanceを明記する。
- Web UIのFamily/Navigation Stage、既存Product Workflowのruntime Stageと、Local CLIの分析処理順序は**異なる概念**。Local CLIでpreflight→identification→estimationと処理することはProductのStageType増設を意味しない。

## 2. Layerごとの責務・禁止依存

| Layer | Owner / Responsibility | Allowed input / dependency | Forbidden dependency |
|---|---|---|---|
| Local Scientific Domain | Question, Design, Estimand, Graph, assumptions, identification/eligibility state, result意味・不変条件 | versioned domain values / immutable refs | DoWhy/EconML/Tigramiteの生object、Product ORM、Web route |
| Scientific Port | Domain入力をMethod実行可能性と標準結果に接続 | versioned domain contract | backend独自のdtype／method objectを外部契約に露出 |
| Method Scientific Adapter | optional backend/APIのAvailability・版確認、入力翻訳、出力正規化 | declared Port, optional library | Domain上のEstimand再定義、silent fallback、Product DB直接更新 |
| Local Application | Preflight・Identification・Eligibility・Execution・Result validation・publish coordination | Domain, Port, local IO abstractions | Navigation Stage ID、Product Worker claim/lease、browser route |
| CLI Interface | 明示schema dispatch、config/args・ファイル検証、Method選択、exit class表示 | Local Application API | Product API必須化、旧v2の無断reinterpretation |
| Local Artifact Port/Adapter | canonical relative key、安全なstaging、checksum/readback、publish、failure cleanup | Root/policy, normalized data | 部分保存の成功宣言、制御外パスへの任意書込 |
| Product Domain / Application | 現行Product Resource・RBAC・persistent lifecycle authority | 既存契約 | E11を理由にしたDB migration・Product API/Worker拡張 |

**Dependency direction:** CLI→Local Application→Domain/Ports、External adapter→Port implementation。DomainからCLI/Framework/Adapterへ逆依存させない。既存のPortと重複する新Portを導入するかはDD-01で実物コード・Authorityを照合してから決定する。

## 3. Responsibility matrix（R: owner, C: consulted）

| Operation / invariant | Domain | Local Application | Scientific Adapter | CLI | Local Artifact |
|---|---|---|---|---|---|
| Estimandの科学的意味、Graph不確実性、IV target区別 | R | C | C | — | — |
| Method/Estimand/Identification適格性 | R | R（順序・Gate） | C（実効Capability） | — | — |
| Backend実効API/version probe | C（許容契約） | C | R | C（表示） | — |
| config/version dispatch・入力Fileの検証 | C | C | — | R | C（Path） |
| Scientific Resultと各状態の正規化 | R | R（検査・公開可否） | R（raw変換） | C | C（保存） |
| Manifest・hash・staging・Readback/atomic publish | C | R（commit決定） | C（実効版） | C | R |
| 局所データ/個票出力のプライバシー方針適用 | R（分類） | R（Policy Gate） | — | R（opt-in受付） | R（権限/Path） |
| Product auth/Execution/DB/Worker | — | — | — | — | —（既存Productのowner） |

## 4. Scope hard boundary

- Phase1〜3は承認されたLocal Scientific CLI（41 Method内のR/Q/N）とLocal Artifactのみに限る。DEC09のD-only、Product統合、GAP-C01〜04の解消を「Local CLI実装」と同一視しない。
- Version dispatchは**旧`causal-analysis-spec/2`と新Local契約を別に扱う**。旧読取とREQUIRES_REVIEW/overrideは変更せず、E11新Methodを旧v2経由で無条件に実行しない。
- 正確なCLI command・config version・Port/class名・Backend pin・具体enumは**IF-01/DD-01/ADRでFreeze**。ここで仮名を既成事実化しない。

## 5. Trace & acceptance

- ARC09-01/02/04/07、E11-A-01/02/04/07；FR-185/187/201/203、NFR-029/032/036、AR-028/029/042。
- Positive: no Product DB、no navigation IDでLocal Methodを実行可能。Negative: v2 reinterpretation、cross-lane resource write、backend unavailable fallback、Product Worker起動がE11の必須条件になる挙動を拒否。
- 実証・実効Portテストは未実施。[Architecture Review](22_90_architecture_consistency_review.md)を参照。
