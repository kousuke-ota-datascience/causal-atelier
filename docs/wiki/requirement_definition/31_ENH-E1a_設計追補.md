# 31 ENH-E1a 設計追補

- 文書状態: ENH-E1a是正実装用最小追補
- 作成日: 2026-08-06
- 上位文書: `10_要件定義.md`
- 対象要件: FR-050、FR-054、FR-062、FR-063、FR-064〜FR-067
- 対象監査: AUD-E1-002、AUD-E1-004〜AUD-E1-009

> 本追補は要件を変更しない。`08_ariadne_ENH-E1a_再実装ならびに再テスト指示書.md` 9.2で未定義だった、既存7 Entity上の保存位置とcontractのみを固定する。

## 1. 変更しない構造

- 主要EntityとTableは追加しない。
- ExecutionとExecution Snapshotは送信後不変とする。
- Snapshot schema versionは`causal-analysis-spec/2`を維持する。旧v2 payloadは読取可能とする。
- 新規の任意Fieldはstrict allow-listに追加し、未知Field rejectを維持する。

## 2. Data EligibilityとEstimator compatibility

Identificationが保存するData Eligibility Result payloadに次を追加する。

```json
{
  "inferred_types": {
    "treatment": {"type": "BINARY", "evidence": {}},
    "outcome": {"type": "CONTINUOUS", "evidence": {}}
  }
}
```

- Treatment: `BINARY | UNSUPPORTED`
- Outcome: `CONTINUOUS | BINARY | UNSUPPORTED`
- evidenceに外部libraryのtype objectを含めない。
- 不適格checkに依存する後続checkは`SKIPPED_DUE_TO_PREREQUISITE`または`NOT_APPLICABLE`と根拠を保存する。
- Estimation受付は保存済みIdentification/Data Eligibility Resultだけを根拠とし、4軸、parameter、adjustment、diagnostics前提を共通validatorで検証する。

## 3. Identification status

Statusは全reason収集後に決定する。確定的入力不整合・DAG cycle・確定的識別条件違反を`REQUIRES_REVIEW`より優先する。ColliderはTreatment–Outcome間のback-door path上のcolliderまたはその子孫としてのみ理由化する。

## 4. Revised Execution

API受付の任意入力として`base_execution_id`と`change_reason`を設ける。受付時に基準Executionと新条件を比較し、Snapshotの任意`revision_context`に次を決定論的に保存する。

```json
{
  "base_execution_id": "<id>",
  "base_snapshot_hash": "<sha256>",
  "revision_kind": "REVISED",
  "change_reason": "<required when changed>",
  "changed_dimensions": ["analysis_spec.causal_question.outcome"]
}
```

- 同一条件の単純再実行は`revision_kind = RERUN`、`changed_dimensions = []`とする。
- 条件差分がある場合は非空の`change_reason`を必須とする。
- Actorと作成時刻はExecutionの`requested_by`と`requested_at`を使用する。
- 旧値は`base_execution_id`、新値は現Execution Snapshotから復元する。
- Lineageは専用Tableを追加せず、`revision_context.base_execution_id`からExecution間edgeを生成する。

## 5. 探索後推論警告

CONFIRMATORY Estimation受付時、同一Project/Dataset Versionの先行Discovery Executionを検索する。警告はSnapshotの任意`scientific_warnings`に保存する。

```json
{
  "warning_code": "POST_SELECTION_INFERENCE_RISK",
  "message": "...",
  "source_discovery_execution_ids": ["<id>"],
  "dataset_version_id": "<id>",
  "rationale": "..."
}
```

- source IDは重複除去した昇順とする。
- WarningはScientific StatusやExecutionの成否を変更しない。
- API response、prefill、Lineage、Web UIは同じ保存済みpayloadを表示する。
- CLIは同一warning schemaをmanifestに保存する。履歴を持たないローカルCLIが独自に履歴を推測しない。

## 6. Migration方針

既存JSON Snapshot、Execution参照、Result payload内で表現するためDB migrationは不要とする。
