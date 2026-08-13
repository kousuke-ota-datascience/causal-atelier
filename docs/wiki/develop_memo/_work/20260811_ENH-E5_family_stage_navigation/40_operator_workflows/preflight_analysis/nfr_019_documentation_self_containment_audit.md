# NFR-019 Documentation Self-Containment Audit

> **Non-normative preflight evidence.** 最終Requirement/Design contractは10/21/22/23/30を正本とする。

## 1. Requirement

`NFR-019`: 現行の正本requirements/design snapshotだけで機能・データ・API・詳細設計を理解できる。

## 2. Why source alignment audit could not verify it

NFR-019はsoftware source implementationの真偽ではなく、documentation artifact自体のself-containmentを要求する。そのため③-1 ↔ ① source auditでは`UNVERIFIED`であった。

## 3. Documentation audit result

**Current v5: PARTIAL_MATCH / FAIL**

主要文書10/21/22/23/30はcurrent contractの展開度が高い一方、以下が残るため完成snapshotとしてPASSできない。

- G00/G01等の下流Gate contractへtarget design決定を委譲する記述が残る。
- Architecture/Human Review待ちのnormative decisionが残る。
- navigation catalog authority/default Stage等、正本文書内で一意にfreezeされていないtarget designがある。
- 今回確定したD1/D2/D3 remediationがまだ正本文書へ反映されていない。
- Case B由来のcurrent/target混同がv5内に残っている。

## 4. Remediation decision

`NFR-019 → D2 E5_TARGET_CHANGE (Documentation Remediation)`

これはsoftware feature追加ではなく、ENH-E5完了時の正本文書セット自体をNFR-019へ適合させる変更である。

## 5. Final acceptance criteria

- **DOC-019-01**: 10/21/22/23/30だけを入力として、機能・Data Resource・API・詳細設計を説明可能。
- **DOC-019-02**: 「ENH-E4を参照」「sourceを参照」「既存contractを参照」だけで済ませたnormative statementが0件。
- **DOC-019-03**: ADR / 06 / Pxx / repositoryを読まなければ決定できないtarget design statementが0件。
- **DOC-019-04**: Architecture Review / Human Review / Gate freezeで後決めするとされた未確定normative decisionが0件。
- **DOC-019-05**: D1項目がcurrent contractとして本文へ反映済み。
- **DOC-019-06**: D2項目がE5 target contractとして本文へ具体化済み。
- **DOC-019-07**: D3項目がcurrent targetから分離され、Requirement Status / Deliveryと`90_technical_debt_and_future_enhancements.md`へtrace可能。
- **DOC-019-08**: 10↔21↔22↔23↔30で同一Resource / field / enum / state / API terminologyに矛盾がない。

## 6. Gate to downstream instruction generation

`DOC-019-01 ... DOC-019-08 = all PASS`になる前に06/Pxx/07へ不足仕様を流してはならない。

```text
10 / 21 / 22 / 23 / 30 freeze
        ↓
NFR-019 re-audit = PASS
        ↓
06 / Pxx / 07
```
