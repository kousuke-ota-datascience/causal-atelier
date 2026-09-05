# ENH-E9 Gate G04 — Causal Diagnostics Backend Contract Completion

- Contract status: `DRAFT_NOT_FROZEN`
- Execution mode: `WORK_PACKAGE`
- Dependency: G03 final PASS

## Semantic claim

estimatorにapplicableなdiagnosticsがstable structured `DIAGNOSTICS_RESULT`として保存され、Frontendが文字列parseや推測を行わず利用できる。

## Minimum design questions to freeze

- Effective Sample Size contract
- actual analysis weight diagnostics
- weight scale / normalization semantics
- balance before/after distinction
- extreme-weight rule representation
- estimator applicability matrix
- AIPW weighting-component semantics

## Methodological invariant

all estimatorへ同一diagnostic setを強制しない。AIPW全体の単一final weightを捏造しない。

## Requirement authority

- FR-044
- FR-048

FR-048 current Implementation Status=`IMPLEMENTED`の整合性はbaseline evidenceで再評価する。
