# ENH-E6 Enhancement Concept Approval Record

- Enhancement: `ENH-E6`
- Record status: `PARTIAL_APPROVAL / CONTRACT_REVIEW_PENDING`
- Date: `2026-08-13`

## Human owner directive captured

Human owner から以下が明示された。

1. ENH-E6 として Family tab / Family-local Stage が期待どおり実現されていない原因と根本原因を分析する。
2. 本来の要件を実現する方法を設計する。
3. `agentic_enhancement_workflow_template` に従う。
4. ENH-E6 の `00_enhance_background` から Gate contract 作成まで実行する。
5. production repository への反映はHuman ownerが行うため、Agentはlocal artifactを作成する。

## Approval boundary

上記は **planning作業の実行承認** として扱う。

本bundleで新規に具体化した以下は Human owner の final semantic approval が未記録のため、`PROPOSED` とする。

- legacy `Causal Discovery -> causal/discovery`
- legacy `Causal Inference -> causal/identification`
- Causal `setup/discovery -> discovery surface`, `identification+ -> inference surface`
- G01 06/07 の `APPROVED / FROZEN` 化

Human owner review前に Coding Agent を起動してはならない。
