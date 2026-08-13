# ENH-E6 Enhance構想承認記録

> **Document class:** Planning / Decision Artifact  
> **Self-containment:** MUST for own subject.

- Decision: `APPROVED`
- Decision timestamp: `2026-08-13` (Human owner review during ENH-E6 planning session)
- Decision authority: `Human owner / repository owner`
- Reviewed proposal: `00_enhance_background/01_enhancement_concept_and_requirement_revision_plan.md`

## Approved scope

- ENH-E5 `ANOM-E5-001`をENH-E6 bugfixとして回収する。
- canonical requirements/designは変更しない。
- navigation transition authority/lifecycle fragmentationを根治対象とする。
- legacy analytical left-navはcanonical compatibility shortcutへ降格する。
- Causal Discovery/Inferenceをstage-aware existing presentationへbindする。
- G01一つ、P01-P03 Work Package Modeで実装する。
- real-browser observable regressionをblocking verificationとする。

## Conditions / constraints

- `docs/wiki/requirement_definition/**`はread-only。
- ENH-E5 historical frozen evidenceはimmutable。
- Gate 06/07はHuman reviewとclean preflight後にfreezeする。
- Coding Agentはassigned Pxxのみをnormative implementation contractとして読み、Gate 07を含む非許可workflow文書を読まない。
- Package completeをGate PASSと扱わない。

## Explicit non-approval

- canonical requirement/designの改定
- broad UI redesign
- backend catalog redesign
- scientific operation semantics変更
- legacy left navigation完全撤去
- Family-only mappingを残したままrender callだけを追加する症状修正
- test assertion weakening / skipによるgreen化

## Required follow-up

1. Architecture Review evidenceを保存する。
2. API READY clean negative-control preflightを保存する。
3. 06/07をfreezeする。
4. Pxxをoperator promptのnormative-source isolationに準拠させる。
5. `G01/P01/Trial01`からCoding executionを開始する。
6. P01-P03後にCandidate Assembly -> Independent Verificationを行う。
