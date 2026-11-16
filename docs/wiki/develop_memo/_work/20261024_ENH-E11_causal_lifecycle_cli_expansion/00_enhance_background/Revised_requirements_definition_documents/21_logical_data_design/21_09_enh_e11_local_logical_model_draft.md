# ENH-E11 — Local Scientific Logical Data Model (LDD)

**文書状態:** `WORKING_DRAFT / OWNER_SEMANTIC_POLICY_APPROVED / FORMAL_PUBLICATION_PENDING`. 本文の仮ID・候補Schema/Port/classは正式なFR/NFR/AR、ADR、Gate Freezeではない。Owner決定DEC01〜09を変更せず詳細化する。

## 1. Authority boundary

- E11のlocal versions、Result、Manifestは既存Product canonical DBのEntityではない。Project DBと同期済み・GAP-C01〜04の解消済みとみなさない。
- Domain/Scientific Coreは科学的識別対象と仮定、Graph fidelity、confidence set typeを定義し、外部engine internal objectsの永続化を禁止する。
- 識別情報は`Question → Estimand → Design/Graph → Identification → Estimator → Result`を辿り、各段のimmutable identity/hashを持つ。

## 2. Local logical value catalog（ID/fieldは設計草案）

| Logical type | 主要field（物理Schema名・型は未freeze） | 必須constraint | Authority |
|---|---|---|---|
| LocalStudyIdentity | schema_version, question_ref/hash, design_ref/hash, dataset_ref/hash, source_versions | upstream hash一致、旧v2暗黙移行禁止 | Local Scientific Domain |
| CausalQuestion | estimand_family, treatment, outcome, contrast, population, decision_use, time_zero | targetを明示、Predictive subgroupとは別 | Domain |
| CausalDesign | strategy, assumptions, eligibility, adjustment, instrument, mediator, temporal_structure | Strategyごとのprecondition | Domain |
| GraphEvidence | graph_kind, nodes, edge_endpoints, lag, provenance, parent_graph_ref, status | DAG/MAG/CPDAG/PAG/Temporalの型を保持 | Domain |
| IdentificationOutcome | target_estimand, graph/design/question refs, validity, proof/evidence, reasons | 非識別/REQUIRES_REVIEWを自動点推定へ渡さない | Domain |
| EstimatorRequest | method_id, target_estimand, identification_ref, backend_requirements, inference_mode | estimator適格性再確認、IV family分離 | Domain |
| EffectOutcome | point_availability/value, uncertainty_availability, scientific_status, diagnostic_refs | No-CIならnull+reason、成功偽装禁止 | Domain |
| ConfidenceSet | topology, component intervals, level, method, validity_conditions | bounded/unbounded/disconnected/ALL_REAL。正常ARはEMPTY禁止 | Domain |
| LocalRunManifest | source/input/output hashes, effective_versions, backend, seed/split, lock, scientific_state | 完全な再現metadata、DB lineageの代替ではない | CLI/Artifact |
| BackendAvailability | method, backend, package version, extra/profile, API probe, reason | unavailable時は該当Methodのみ無効 | Adapter/Runtime |

## 3. 状態・不変条件

- `EXECUTION_TECHNICAL_STATUS`、`IDENTIFICATION_STATUS`、`POINT_AVAILABILITY`、`UNCERTAINTY_AVAILABILITY`、`SCIENCE_ACCEPTANCE`は互いに独立した論理概念。具体enum文字列はADR/Schema待ち。
- Graph再固定は元Graphを書き換えず新GraphVersionとparent/edit rationale/assumptionを保持し、必ず再識別する。
- weak-IV AR反転の`ALL_REAL`は全実数集合であって不正なnull・有限CIではない。正常ARで`EMPTY`を生成したら数値/適格性異常を検査する。
- 個票CATEは特別な最小化とexport/roleの契約を持ち、一般Result summaryで暗黙公開しない。

## 4. Data model review negative cases

1. DAGへの黙示変換、unknown endpoint喪失、lagの符号消失。
2. 非識別Resultsのpoint-only昇格、B1 structural slopeをcomplier LATEと表示。
3. finite CIが存在しないのに確率区間を生成、ARのnonconnectedを単一区間に丸める。
4. `causal-analysis-spec/2`を新local E11 schemaとして自動読み込み。
5. Product canonical Result/Lineageとlocal manifestを同一authorityとして扱う。

## 5. 追跡

- [03 要件意味差分](../../03_requirements_revision.md)
- [04 Architecture改定方針](../../04_design_revision.md)
- [DEC09 Owner承認](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md)
- [Scope68](../../00_04_phase1_to_phase3_cli_scope_proposal.md)
