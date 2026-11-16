<!-- ENH-E11 split working copy: not a formal approval. -->
# 23 — worker cli

**Status:** `STRUCTURAL_COPY_DRAFT` (existing baseline text, not E11 canonical publication)

**Source:** [23_api_interface_design.md](https://github.com/kousuke-ota-datascience/causal-atelier/blob/3ba5fe2465ec591f0da7f998c21a5241984b73dc/docs/wiki/requirement_definition/23_api_interface_design.md) · blob `131467f02222f105a49e6dfdbcec0f49cadb0f41`  
**Index:** [Revised document inventory](../README_00_Revised_requirements_definition_documents.md)

---

## 6. Worker / Runtime Internal Interface

Worker claimはpublic Web APIではなく、worker processとExecution repository / Unit of Work間の内部interfaceである。

### 6.1 Execution claim / lease

Repository-level interface:

```python
def claim_next(
    worker_token: str,
    *,
    worker_id: str | None = None,
    lease_seconds: int = 1800,
) -> Execution | None: ...
```

Claim対象:

- `QUEUED`
- `RUNNING`かつexpired lease

Selection/mutation:

- `requested_at`順
- row lock + skip locked
- `status = RUNNING`
- `started_at = now`
- `lease_owner = worker_id or worker_token`
- `lease_expires_at = now + lease_seconds`

Worker processはprocess-local UUID `worker_token`を生成し、current runnerでは`claim_next(worker_token, worker_id=worker_token)`を呼ぶ。`claim_token`というpublic/domain resourceは存在しない。

### 6.2 Lease renewal / ownership

```python
renew_lease(execution_id, owner, lease_seconds=1800)
```

positive duration、Execution存在、`lease_owner == owner`、`status == RUNNING`を要求する。lease ownerが設定されたExecutionのupdate/completeもowner一致を要求する。

### 6.3 Completion boundary

Executionを`SUCCEEDED`としてcompleteする場合、StageExecutionが1件以上あり、全件が`SUCCEEDED`または`SKIPPED_DUE_TO_PREREQUISITE`でなければならない。

### 6.4 Stage runtime contract

`StageExecution` status:

```text
PENDING
READY
RUNNING
SUCCEEDED
FAILED
SKIPPED_DUE_TO_PREREQUISITE
CANCELLED
```

Attemptは`stage_attempt_id / attempt_number / worker_id / effective_random_seed / started_at / finished_at / error`をappend-only履歴として保持する。`effective_random_seed`はstochastic Stageのactual seed、deterministic Stageはnull。同一logical Stageのtechnical retryでは同じeffective seedを再利用する。

### 6.5 Runner contract

Current protocol:

```python
class StageRunner(Protocol):
    stage_type: StageType
    def validate(self, context: StageContext) -> None: ...
    def run(self, context: StageContext) -> StageRunResult: ...
```

`StageRunResult`:

```text
output_bindings
results: ResultDraft*
artifacts: ArtifactDraft*
warnings
metrics
effective_random_seed: int | null
```

`ResultDraft`と`ArtifactDraft`は`schema_version`を持つが、canonical persistent Result/Artifactが同一fieldを直接持つことを意味しない。Runner/output adapterでcanonical persistence contractへ変換する。

Execution `runtime_version_json`は最低限`ariadne_code_version / python_version / platform_system / platform_release / machine / libraries`を含む。`libraries`は実際に利用したregistered runner dependencyのversionをcaptureする。

### 6.6 Runtime state observation / event policy

現行実装に独立したpublic`ExecutionEventPublisher / StageEventPublisher`はない。runtime lifecycle authorityはpersistent `Execution / StageExecution` stateである。

Family tab/Navigation route changeをruntime lifecycle eventへ変換しない。

## 7. CLI / Library Interface

現行実装のproduct script entry pointは次である。

```text
ariadne-discover
ariadne-estimate
ariadne-identify
ariadne-refute
ariadne-sensitivity
ariadne-api
ariadne-worker
```

scientific CLIの既存境界:

- `ariadne-discover`はstandalone discovery CLIであり、**Web/API Execution IDを作成しない**。
- `ariadne-identify` / `ariadne-refute` / `ariadne-sensitivity`は共通local scientific-stage implementationを利用し、`--config`でYAMLを読み、domain analysis-spec validation後に`ScientificCoreAdapter`を直接呼び出す。
- `ariadne-estimate`もlocal estimation commandとして提供される。
- CLIは実行manifest等のlocal outputを生成するが、browser route / sidebar stateを入力契約にしない。

したがってCurrent contractでは、存在しない次のようなgeneric Resource CLIをcurrent interfaceとして捏造しない。

```text
ariadne project list
ariadne execution submit
ariadne result show
```

将来generic product CLIを追加する場合は別scopeでinterface contractを設計する。Current mandatory contractでは、既存headless scientific CLIおよびPython/backend use caseへ`current_family` / `navigation_stage` / browser routeをrequired inputとして追加しない。

禁止例:

```text
ariadne-identify --navigation-stage identification --config ...
```

`AnalysisFamily` / `ExecutionOperation`等のdomain discriminatorと、UI Navigation Stageを区別する。
