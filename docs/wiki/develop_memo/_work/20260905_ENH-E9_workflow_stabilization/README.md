# ENH-E9 — Post-E8 Workflow Stabilization

**Document class:** Enhancement Workflow Instance / Authoring Guide  
**Self-containment:** MUST  
**Workflow state:** `DRAFT_NOT_FROZEN / BLOCKED_PREREQUISITE`  
**Agent execution:** NOT READY. ENH-E8 G03 formal Independent Verification PASS と exact PASS SHA の baseline 固定が完了するまで E9 Coding を開始してはならない。

## 0. Identity

| Item | Value |
|---|---|
| Project | Ariadne |
| Enhancement ID | `ENH-E9` |
| Enhancement Short ID | `E9` |
| Working title | Post-E8 Workflow Stabilization |
| Work root | `docs/wiki/develop_memo/_work/20260905_ENH-E9_workflow_stabilization` |
| Working branch | `bugfix/ariadne_mvp_e9` |
| Authoring-time observed branch HEAD | `9fd4ce03ccb00c3e5a0c9536ac94cedafff74d4c` — **E9 baselineではない** |
| E9 baseline | `UNSET` — ENH-E8 G03 formal PASS の exact accepted SHA を kickoff 時に固定する |
| Initial Trial | `01` |
| Primary language | 日本語。API/schema/class/identifier/workflow status等は英語を維持する |

## 1. Enhancement objective

ENH-E9 は新しい analytical capability を追加する Enhancement ではない。

目的は、ENH-E8完了後の実利用およびCHAT-direct bugfix過程で観測された **workflow usability residual gap** と、既存 Causal Diagnostics requirement に対する **backend conformance gap** のみを、ENH-E8で確立した Stage responsibility / lineage / navigation semantics を変更せずに閉じることである。

Historical `Enhance_request.md` は backlog authority ではなく観測時点の problem inventory として扱う。E8/G03およびその後の直接修正で解決済みの項目を再実装しない。E9 scopeは E8 G03 formal PASS baseline に対する residual evidence から確定する。

## 2. Authority and precedence

E9 authoring / executionで使用する authority domain は次のとおり。

1. `docs/wiki/requirement_definition/` — current effective requirements/design snapshot。Requirement/design semanticsの正本。
2. ENH-E8 G03 frozen/amended contract + canonical final `999 PASS` — E9開始時のprotected regression authority。
3. 本workflow `00_enhance_background/*` — E9 scope/design rationale、residual classification、requirement review。
4. 各Gate `06` — Gate implementation semantic authority。
5. 各Gate `07` — Gate Acceptance Criteria authority。
6. Pxx — bounded Coding execution authority。Gate semanticsを変更できない。
7. `20_implementation_reports` — implementation evidence。acceptance authorityではない。
8. `30_test_report/.../999_gate_decision` — Independent Verification final Gate authority。

Source codeはrequirement/designとのconformance確認対象であり、requirement/design正本の代替ではない。

## 3. Mandatory entry gate

E9 Coding開始前に次をすべて満たすこと。

- [ ] ENH-E8 G03 formal Independent Verification = `PASS`
- [ ] canonical `ENH-E8_G03_*_999_gate_decision.md` が存在する
- [ ] PASS対象の exact accepted SHA を E9 baseline として記録する
- [ ] `Enhance_request.md` 全観測を baseline source/runtime と再照合する
- [ ] 各観測を `RESOLVED / RESIDUAL / OUT / ARCHITECTURE_QUESTION` へ分類する
- [ ] G01-G04 scopeを residual evidenceからfreezeする
- [ ] Outcome one-way ownershipをprotected regressionとしてfreezeする
- [ ] FR-048 implementation truthを再評価する
- [ ] G04のIPW/AIPW diagnostics semanticsをfreezeする
- [ ] G05 browser journeyをfreezeする
- [ ] Applicable Gate 06/07を `FROZEN` にする

これらが完了する前のGate contractはauthoring draftであり、Coding Agentへのexecution authorityを持たない。

## 4. Requirement decision at workflow initialization

**New analytical capability: NONE. New FR: NONE at initialization. New NFR: NONE at initialization.**

E9は原則として既存requirementへのconformance/usability enhancementである。

主要 requirement authority:

- `FR-035`–`FR-039`: Causal Discovery / Graph Candidate / comparison / FIXED Graph
- `FR-040`: Causal Question — Population / Treatment / Comparator / Outcome / Time / Estimand / Decision Use
- `FR-044`: Data Eligibility — sample size / overlap 等
- `FR-048`: applicable diagnosticsをResultとして保存し、全estimatorへ同一diagnostic setを強制しない
- `FR-106`: Analysis Contextとして Current Project / Active Research Context / Dataset Version / Analysis Viewを明示
- `FR-168`: DataがAnalysis View lifecycleを所有
- `FR-171`–`FR-173`: Analysis Context ownership / restore / invalidation
- `FR-174`: UI再配置を理由にanalysis execution semanticsを変更しない

`FR-048` は current snapshot で `IMPLEMENTED` と記録されている。しかし、ESS / weight diagnostics / adjusted balanceのstructured Result不足がbaseline実装で確認された場合、implementation truthとsnapshot statusの整合性をHuman review対象とする。Evidenceなしにstatusをsilent修正しない。

## 5. Gate structure

| Gate | Semantic claim | Draft execution mode | Dependency |
|---|---|---|---|
| `G01` | Project / Analysis Contextの既存resourceを変更せず、保存済みAnalysis View内容と主要Context入力の意味をUI上で確認できる | `SINGLE_EXECUTION` | E9 entry gate |
| `G02` | DiscoveryからGraph比較・選択・採用までの既存workflowを、比較対象と操作結果が明確なinteractionとして利用できる | `WORK_PACKAGE` | G01 final PASS |
| `G03` | Identification causal-question inputをscientific semanticsを変えず意味と入力候補を理解できる形で指定できる | `SINGLE_EXECUTION` | G02 final PASS |
| `G04` | estimatorにapplicableなdiagnosticsがstable structured `DIAGNOSTICS_RESULT` として保存され、Frontendがparse/推測せず利用できる | `WORK_PACKAGE` | G03 final PASS |
| `G05` | E9 residual fixes統合後もE8で確立したCausal workflowが1つのbrowser journeyとして成立する | `SINGLE_EXECUTION` | G04 final PASS |

Gate splitはsemantic acceptance boundaryであり、実装量を理由に変更しない。Execution量が大きい場合はWork Packageで分解する。

## 6. Protected regression

### 6.1 Outcome ownership

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

- IdentificationでOutcomeを別途編集可能に戻す
- EstimationでOutcomeを独立入力させる
- Graph lineageと無関係なOutcome overrideをUI convenienceとして導入する

Treatment selector改善とOutcome ownershipは別問題として扱う。

### 6.2 E8 protected semantics

- Stage Content architecture redesign
- Estimation submission architecture
- Effects presentation framework
- Diagnostics presentation framework
- Estimation vertical layout
- Outcome inheritance
- Discovery submit feedback
- Result / Execution lineage
- Navigation Stage / Execution operation separation
- existing API route grammar

## 7. Explicitly out of scope

### ENH-E10

- LightGBM
- SHAP
- LIME
- predictive model registry generalization
- predictive explanation registry generalization

### ENH-E11

- historical causal lifecycle Phase1 reconciliation
- DoWhy candidate
- FCI candidate
- broad foundation architecture audit
- lifecycle-wide lineage reconciliation

E9ではProject Management IA redesign、Analysis View schema revision、canonical Navigation Stage redesign、runtime Stage redesignも行わない。

## 8. Execution order

1. E8 G03 formal Independent VerificationをE8 workflow authorityの下で完了する。
2. E8 G03 exact PASS SHAをE9 baselineとして本workflowへ固定する。
3. `00_enhance_background/06_residual_scope_matrix.md` をcurrent baseline evidenceで更新する。
4. Requirement/design revision要否を確定し、必要ならHuman review後にlocal revised snapshotを更新する。
5. G01-G04の06/07およびWork Package planをfreezeする。
6. G01 → G02 → G03 → G04を順にIndependent Verificationまで完了する。
7. G05でintegrated browser journeyとprotected regressionをformal acceptanceする。
8. formal FAIL時のみ08 remediation contractを作る。Gate semantic claim / AC defectは09 Gate Contract Amendmentで扱う。

## 9. Initial critical browser journey

G05のdraft journey:

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

Final blocking journey、canonical command、environment、synchronization、assertionsはG05 `07` freeze時に確定する。

## 10. Directory map

`TEMPLATE_STRUCTURE.md` を参照する。README filenameは `README_NAMING_CONVENTION.md` のpath-derived naming ruleに従う。

`README_Appendix_HowToUse.md` はoperator runbookであり、個別GateのAcceptance Criteria authorityではない。
