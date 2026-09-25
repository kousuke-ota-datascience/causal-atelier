# ENH-E9 申し送り事項 — Post-E8 Workflow Stabilization

- 文書状態: `HANDOFF_DRAFT`
- Enhancement ID: `ENH-E9`
- 仮称: `Post-E8 Workflow Stabilization`
- 上流 Enhancement: `ENH-E8 Analysis Stage Content Architecture Redesign`
- 最低開始条件:
  - ENH-E8 G03 の retrospective contract が current source に re-baseline 済み
  - **ENH-E8 G03 formal Independent Verification = PASS**
- Baseline SHA:
  - **E8 G03 PASS candidate の exact accepted SHA を E9 kickoff 時に固定すること**
- historical inputs:
  - `docs/wiki/develop_memo/_work/20260822_NEXT_Enhance_request/Enhance_request.md`
  - `docs/wiki/develop_memo/_work/20260823_ENH-E9_causal_result_presentation_followup/01_backend_handoff.md`

---

## 1. 結論

ENH-E9 は新しい analytical capability を追加する Enhancement ではない。

目的は次である。

> ENH-E8 完了後の実利用・CHAT-direct bugfix過程で発見された workflow usability residual gap と、既存 Causal Diagnostics requirement に対する backend conformance gap のみを抽出し、ENH-E8 で確立した Stage responsibility / lineage / navigation semantics を変更せずに閉じる。

したがって、2026-08-22 の `Enhance_request.md` をそのまま backlog として実装してはならない。

同文書は観測時点の問題 inventory であり、E8/G03 およびその後の直接修正によって既に解決した項目を current source と再照合した上で residual scope を決定する。

---

# 2. ENH-E8 / G03 から引き継ぐ authority

ENH-E8 G03 は、ENH-E8完了後にCHAT上で直接修正された以下の挙動を retrospective regression contract として吸収している。

## 2.1 Estimation

- Identification hidden form validation に依存せず Estimation action を起動する。
- selected `IDENTIFICATION_RESULT` の execution lineage を authority とする。
- `/executions/{execution_id}/prefill` から dataset / graph / analysis specification を復元する。
- native/shared-form submit fallback を作らない。
- handler ready 前は Estimation action を安全に disabled にする。

## 2.2 Effects

- 保存済み `TREATMENT_EFFECT_RESULT` を primary source とする。
- causal question / estimator / effect estimate / uncertainty / warnings / lineage を human-readable に表示する。
- frontend で新しい causal estimate を生成しない。

## 2.3 Diagnostics presentation

- 保存済み `DIAGNOSTICS_RESULT` を primary source とする。
- analysis context
- sample support
- covariate balance
- propensity overlap
- scientific warnings
- associated Treatment Effect
- lineage

を human-readable に表示する。

backend に存在しない ESS / weight diagnostics / weighted balance を frontend で推測・捏造してはならない。

## 2.4 Historical label

source commit / test artifact に `ENH-E9` という historical label が残るものがある。

これは provenance として維持するが、現在の Enhancement ownership を意味しない。

E8 G03 authority 上、それらは ENH-E8 の後追い conformance / bugfix evidence として扱う。

---

# 3. E9 kickoff 前の必須 Gate

E9 を開始する前に、E8 G03 を formal に閉じる。

## Required action

current repository exact SHA を:

> `ENH-E8 G03 Trial01 Fixed Verification Candidate`

として固定し、G03 Verification Contract に基づく Independent Verification を行う。

最低確認:

- Estimation pre-ready / ready lifecycle
- selected Identification Result lineage
- canonical frontend asset delivery
- Effects runtime load / render
- Diagnostics runtime load / render
- E8 G02 Stage separation regression
- API / schema / backend semantics 非破壊

PASS SHA を E9 baseline とする。

---

# 4. 2026-08-22 Enhance Request の residual classification

E9 kickoff 時に current baseline でもう一度再確認すること。

初期分類は以下。

| Historical observation | Initial current disposition |
|---|---|
| Saved Analysis View に `[表示]` がない | `RESIDUAL_CANDIDATE` |
| Active Research Context tooltip がない | `RESIDUAL_CANDIDATE` |
| SetupでDiscovery Graphを要求 | `RESOLVED / E8` |
| Setup Stage自体の存在意義 | `ARCHITECTURE_QUESTION / OUT` |
| Discovery operation領域にtitleがない | `RESIDUAL_CANDIDATE` |
| Discovery Objective tooltipがない | `RESIDUAL_CANDIDATE` |
| Discovery Rationale tooltipがない | `RESIDUAL_CANDIDATE` |
| Discovery submit後feedbackがない | `RESOLVED` |
| Graph Candidates overflow | `RESIDUAL_CANDIDATE / runtime verify` |
| Graph Candidate一括選択/解除 | `RESIDUAL_CANDIDATE` |
| Graph Comparison current selection highlight | `RESIDUAL_CANDIDATE` |
| Graph Comparison説明にalgorithm/parameter不足 | `RESIDUAL_CANDIDATE` |
| Graph採用結果がmodal外notice | `RESIDUAL_CANDIDATE` |
| Graph Mermaid export | `RESIDUAL_CANDIDATE` |
| Population tooltip | `RESIDUAL_CANDIDATE` |
| Comparator tooltip | `RESIDUAL_CANDIDATE` |
| Treatment schema-backed selector | `RESIDUAL_CANDIDATE` |
| Outcome手入力 | `RESOLVED` |
| Estimation横方向layout | `RESOLVED / E8` |

---

# 5. Protected regression — 特に Outcome ownership

Outcome の ownership を変更してはならない。

current intended flow:

```text
Discovery
  designated Outcome
       ↓
Graph Version
  designated_outcome_node
       ↓
Identification
  read-only Outcome
       ↓
Estimation
```

禁止:

- Identification で Outcome を別途編集可能に戻す。
- Estimation で Outcome を独立入力させる。
- Graph lineage と無関係な Outcome override を UI convenience として導入する。

Treatment の selector 改善と Outcome ownership は別問題として扱う。

---

# 6. Proposed Gate structure

## G01 — Context / Data Usability Residual

Acceptance claim:

> Project / Analysis Context の既存resourceを変更せず、利用者が保存済みAnalysis Viewの内容と主要Context入力の意味をUI上で確認できる。

候補:

- Saved Analysis Views `[表示]`
- Active Research Context tooltip

Non-goal:

- Project Management IA redesign
- Analysis View schema revision

---

## G02 — Causal Discovery / Graph Interaction Residual

Acceptance claim:

> DiscoveryからGraph比較・選択・採用までの既存workflowを、操作結果と比較対象を明確に把握できる interaction として利用できる。

候補:

- Discovery operation block title
- Objective tooltip
- Rationale tooltip
- Graph Candidates overflow correction
- Select All / Clear
- current comparison candidate highlight
- algorithm / relevant parameter summary
- modal-local graph adoption feedback
- Mermaid source export

Protected:

- Discovery execution semantics
- Graph Candidate identity
- GraphVersion lineage
- FIXED semantics
- current comparison API
- editing/adoption scientific semantics

---

## G03 — Identification Input Ergonomics

Acceptance claim:

> Identification の causal question inputs を、既存 scientific semantics を変えず、利用者が意味と入力候補を理解できる形で指定できる。

候補:

- Population tooltip
- Comparator tooltip
- Treatment Dataset-schema-backed selector

Protected:

- Outcome one-way inheritance
- FIXED Graph requirement
- estimand semantics
- identification strategy
- adjustment set semantics
- scientific assumptions

---

## G04 — Causal Diagnostics Backend Contract Completion

Acceptance claim:

> estimator に applicable な diagnostics が stable structured `DIAGNOSTICS_RESULT` として保存され、Frontendが文字列parseや推測を行わず利用できる。

最低対象:

### Effective Sample Size

IPW 等 applicable estimator について:

```text
diagnostics.weighting.effective_sample_size
```

等の stable structured contract で取得可能にする。

### Weight diagnostics

estimator が実際に使用した analysis weight について最低限:

- count
- min
- mean
- median / p50
- p95
- p99
- max
- extreme-weight count / rule

を検討する。

weight scale / normalization semantics を明記すること。

### Balance

```text
balance.before
balance.after
```

等として weighting 前後を区別する。

current unweighted balance を after-weighting と誤認させない。

### Estimator applicability

すべての estimator に同一diagnostic setを強制しない。

特に:

- difference-in-means
- OLS
- IPW
- AIPW

を methodologically 区別する。

AIPW について「AIPW全体の単一final weight」を捏造しない。

propensity-derived weighting diagnostics を提示する場合は、それが estimator 全体ではなく weighting component の diagnostic であることを contract に明記する。

---

## G05 — Integrated Regression Acceptance

Acceptance claim:

> E9 residual fixesを統合した後も、E8で確立したCausal workflowが1つのbrowser journeyとして成立する。

最低journey:

```text
Analysis Context
    ↓
Discovery
    ↓
Graph review / comparison
    ↓
FIXED Graph
    ↓
Identification
    ↓
Estimation
    ↓
Effects
    ↓
Diagnostics
```

Protected regression:

- ENH-E8 G01
- ENH-E8 G02
- ENH-E8 G03
- Result / Execution lineage
- Navigation Stage / Execution operation separation
- existing API route grammar

---

# 7. Explicitly out of scope

E9へ含めない。

## E8 ownership

- Stage Content architecture redesign
- Estimation submission architecture
- Effects presentation framework
- Diagnostics presentation framework
- Estimation vertical layout
- Outcome inheritance
- Discovery submit feedback

## Predictive advanced capability

- LightGBM
- SHAP
- LIME
- predictive model registry generalization
- predictive explanation registry generalization

→ ENH-E10

## Causal foundation reconciliation

- historical causal lifecycle Phase1 reconciliation
- DoWhy candidate
- FCI candidate
- broad foundation architecture audit
- lifecycle-wide lineage reconciliation

→ ENH-E11

---

# 8. Requirement handling

E9は原則として既存requirementへの conformance / usability enhancement として扱う。

特に Causal Diagnostics backend gap では current requirement snapshot の `FR-048` と実装事実を再評価する。

FR-048 が requirement 上 `IMPLEMENTED` と記録されていても、ESS / weight / post-adjustment balance の structured Result が不足するなら implementation status の整合性をレビューする。

silentに requirement truth を実装へ合わせない。

---

# 9. Start checklist

- [ ] ENH-E8 G03 formal Independent Verification PASS
- [ ] E8 G03 PASS exact SHAをE9 baselineとして固定
- [ ] `Enhance_request.md` を historical observation inventory と宣言
- [ ] current frontend/sourceで全項目を再照合
- [ ] `RESOLVED / RESIDUAL / OUT / ARCHITECTURE_QUESTION` に分類
- [ ] G01〜G04 scopeを residual evidence からfreeze
- [ ] Outcome one-way ownershipをprotected regression化
- [ ] FR-048 implementation truthを再評価
- [ ] G04でIPW/AIPW diagnostics semanticsをfreeze
- [ ] G05 browser journeyをfreeze
- [ ] 06/07を self-contained execution contract にする

---

# 10. Primary source paths

ENH-E8:

- `docs/wiki/develop_memo/_work/20260820_ENH-E8_analysis_stage_content_redesign/`
- 特に:
  - `README.md`
  - `10_enhance_instruction/G03/README_10_G03.md`
  - `10_enhance_instruction/G03/06_Ariadne_ENH-E8_G03_implementation_instruction.md`
  - `10_enhance_instruction/G03/07_Ariadne_ENH-E8_G03_test_instruction.md`
  - `10_enhance_instruction/G03/09_ENH-E8_G03_A02_Gate_Contract_Amendment.md`

Historical E9 inputs:

- `docs/wiki/develop_memo/_work/20260822_NEXT_Enhance_request/Enhance_request.md`
- `docs/wiki/develop_memo/_work/20260823_ENH-E9_causal_result_presentation_followup/01_backend_handoff.md`

Current implementation:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`
- `frontend/causal_stage_presentation.js`
- `frontend/causal_estimation_submission.js`
- `frontend/causal_effects_presentation.js`
- `frontend/causal_diagnostics_presentation.js`
- `src/ariadne/scientific/inference/adapter.py`
- `src/ariadne/causal/inference/estimators/treatment_effect.py`
- `src/ariadne/causal/inference/diagnostics/balance.py`
- applicable product/scientific/browser tests

---

# 11. 最初の作業

Codingから始めない。

最初の closure unit は:

> E8 G03 formal Independent Verificationを完了し、そのPASS SHAをE9 baselineとして固定する。

その後:

> `Enhance_request.md` の全項目を current baseline に対する residual matrix へ変換する。

これをE9 scope authorityの出発点とする。