# 23_30_worker_runtime


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
