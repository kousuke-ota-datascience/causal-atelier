# ENH-E11 — Local CLI & Scientific Port Interface Draft (API)

**文書状態:** `WORKING_DRAFT / OWNER_SEMANTIC_POLICY_APPROVED / FORMAL_PUBLICATION_PENDING`. 本文の仮ID・候補Schema/Port/classは正式なFR/NFR/AR、ADR、Gate Freezeではない。Owner決定DEC01〜09を変更せず詳細化する。

## 1. Contract boundary

追加対象は**Local CLI / Scientific Adapter Port / persistent local file**。既存Web API `/api/v1`、Worker内部API、Product DB schemaへE11の新APIを追加しない。旧`causal-analysis-spec/2`のreaderはそのまま保護する。

## 2. Interface objects（provisional）

| Contract | Inputs | Outputs | Validation / error |
|---|---|---|---|
| Version Dispatcher | explicit schema_version, operation, config | version-selected parser | unknown/reinterpreted legacy拒否 |
| Local Preflight | question/design/graph/dataset refs, method, backend req | typed eligibility / errors | hash mismatch、欠落、path安全、privacy |
| Scientific Identification Port | estimand, design, graph, data metadata, assumptions | normalized identification outcome | NONIDENTIFIED/REQUIRES_REVIEWが推定へ漏れない |
| Method Estimation Port | validated estimator request, split, seed, data | effect/CI diagnostics and backend evidence | Method/estimand mismatch、bad support |
| Local Artifact Writer | staged files, relative keys, media types | hashes/commit result/manifest | partial failure、traversal、rollback |
| Manifest Writer/Reader | complete provenance, versions, source hashes | JSON + readback status | noncanonical/untrusted content拒否 |

## 3. Normative interface rules

1. CLIが選択したMethod以外をfallback実行しない。Backend unavailableは原因・利用可否として明示する。
2. Scientific negative Resultはtechnical exceptionと独立のcategoryを返す。具体exit code値は正式IFとして別途freezeする。
3. JSON/Parquet/Markdown成果物は再読込時もEffect point、uncertainty availability、confidence set topology、scientific stateを保持する。
4. 出力Referenceはpath traversalを禁止し、canonical relative artifact keysに正規化する。private row-level CATEのデフォルト外部公開を禁止する。
5. InputHash、schema_version、upstream ref、backend/library/version、lock fingerprint、effective seed/split、output SHAをManifestへ保存する。
6. Normalized formatの実際のJSON property/enum名・CLI option名称は未freeze。例示された概念名はwire-compatibility保証ではない。

## 4. Interface-specific acceptance

| Test group | Pass condition | Negative |
|---|---|---|
| Schema/version | legacy v2 read unchanged、新E11は明示dispatch | v2 auto-upgrade拒否 |
| Method/Backend | method別effective API、5 profile/optional extrasで適切なavailability | uninstalled extrasでcore継続 |
| Identification | upstream consistency, estimator matching, GraphVersion fidelity | wrong design/weak-IV/nonidentified |
| Inference | AR component intervals、point vs science status、pointwise CI | disjointを単一CIに丸めない |
| Atomic/Privacy | staged publish, readback, hash, path/permissions | failure residue無し、個票流出無し |

- [03 要件意味差分](../../03_requirements_revision.md)
- [04 Architecture改定方針](../../04_design_revision.md)
- [DEC09 Owner承認](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- [Scope68](../../00_04_phase1_to_phase3_cli_scope_proposal.md)
