# ENH-E5 Preflight Analysis

## 0. Purpose

本directoryは、ENH-E5 planningにおける**実装前の詳細調査・証拠・裁定過程を保存する非normative work product**である。

主な用途:

- ENH-E4完了実装baselineに対する静的解析
- ENH-E5 requirements/designのalignment evidence
- Case A/B/C/D diagnosisとD1/D2/D3 remediation decisionの根拠
- planning時にfreezeすべき未確定contractの詳細調査
- NFR-019 documentation self-containment audit

監査baseline: `a770cc4f38137063cd5f22d8035e91e3c63b7502`

## 1. Normative authority

**本directoryはCoding/Test Agent向けnormative contractではない。**

- current/target product contractは `00_enhance_background/Revised_requirements_definition_documents/10/21/22/23/30` を正本とする。
- Coding Agent向け仕様は、上記正本文書から `10_enhance_instruction/GXX/06_*.md` またはassigned `06_GXX_Pxx_*.md` へ完全収束させる。
- Test/Audit Agent向けverification contractは `10_enhance_instruction/GXX/07_*.md` へ完全収束させる。
- Agentは本directoryから不足仕様を発見・補完してはならない。
- Repository/sourceは実装方法や監査証拠の確認には使用できるが、Execution Agentがnormative decisionを発見するためには使用しない。

## 2. Information flow

```text
Source static analysis / audit evidence
        ↓
40_operator_workflows/preflight_analysis/
        ↓
06_existing_implementation_design_alignment_review.md
        ↓
D1 / D2 / D3 remediation decision
        ↓
01 / 02 / 03 / 04 / 05 planning documents
        ↓
10 / 21 / 22 / 23 / 30 revised canonical documents
        ↓
NFR-019 documentation audit = PASS
        ↓
06 / Pxx implementation contract
07 test contract
        ↓
final ③-1 ↔ ① re-audit
```

## 3. Contents

| File | Role |
|---|---|
| `ENH-E5_nonchange_alignment_audit_report.md` | ③-1 ↔ ENH-E4実装の監査報告。元添付をcanonical nameで格納。 |
| `ENH-E5_nonchange_requirement_alignment_matrix.csv` | Requirement 215件の③-1/③-2分類とsource alignment evidence。 |
| `ENH-E5_nonchange_design_alignment_matrix.csv` | 10/21/22/23/30のcurrent-contract design audit evidence。 |
| `remediation_decision_log.md` | 人間向けD1/D2/D3裁定記録。 |
| `remediation_decision_matrix.csv` | 機械可読なsubstatement単位の裁定索引。 |
| `nfr_019_documentation_self_containment_audit.md` | NFR-019専用documentation audit。 |
| `findings/*.md` | root decision単位の詳細調査・影響分析。 |

## 4. Status vocabulary

### Alignment status

- `MATCH`
- `PARTIAL_MATCH`
- `MISMATCH`
- `UNVERIFIED`
- `TARGET_CHANGE`

### Remediation decision

- `D1 CURRENT_IMPLEMENTATION`
- `D2 E5_TARGET_CHANGE`
- `D3 DEFER`

### Requirement lifecycle / delivery

Requirement正本では、少なくとも以下を独立管理する。

```text
ID
Area
Requirement
Level
Requirement Status
Implementation Status
Delivery
```

`Requirement Status` と `Implementation Status` を分離し、`MUST`等のLevelへ時点依存の意味を混入させない。

## 5. Change discipline

1. preflight findingはまず本directoryにevidence付きで記録する。
2. 人間裁定後、`remediation_decision_log.md` / `.csv`を更新する。
3. D3は`90_technical_debt_and_future_enhancements.md`へtraceする。
4. D2の未確定仕様はpreflightでfreezeする。
5. 10/21/22/23/30へ反映する。
6. NFR-019を再監査してPASSさせる。
7. その後のみ06/Pxx・07へ収束する。
8. 最後に③-1 ↔ ①を再監査する。
