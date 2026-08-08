# 01 Runtime Entry Point Inventory — Architecture Review Prompt

## 1. Task

`ENH-E4 eliminate dual execution` の Architecture Review Phase 01 として、現在のRepositoryに存在する **Runtime Entry Point と、その到達先の最初のApplication / Execution境界**を静的コード調査によってInventory化する。

本Phaseの目的は、現在のコードベースについて以下を事実として確定することである。

1. application runtime を起動する入口は何か
2. Executionに到達し得る外部入口は何か
3. 各入口から最初にどのApplication Service / Use Case / Orchestratorへ到達するか
4. その経路が `legacy` / `product` / その他のどの実装へ接続しているか
5. 現在の標準的なruntime構成から到達可能な経路と、単にコードとして存在するだけの経路を区別できるか
6. 現時点の静的証拠だけでは判定できない経路は何か

このPhaseは **read-only architecture investigation** である。

Production code、test code、configuration、migration、dependency、runtime stateを変更してはならない。

唯一許可されるRepositoryへの書き込みは、指定されたresult文書の生成・更新だけである。

---

## 2. Positioning

本Phaseは実装Phaseではない。

また、Target Architectureを決定するPhaseでもない。

このPhaseでは、

> Current Architecture が実際にどのRuntime Entry Pointを持ち、そこからどのコードへ到達するか

だけを調査する。

以下は後続Phaseで扱うため、本Phaseでは決定しない。

* legacy codeを削除すべきか
* product architectureへ統一すべきか
* Execution modelをどのように再設計すべきか
* Result / Artifactのownershipをどう変更すべきか
* Lineage architectureをどう変更すべきか
* migrationをどう変更すべきか
* ENH-E4のGateをどう分割すべきか

本Phaseのresultは、これらの設計判断を行うための **evidence** として使用する。

---

## 3. Repository / Investigation Context

対象Repository:

```text
causal-atelier
```

対象branch:

```text
refactor/ariadne_mvp_e4
```

ENH-E4 work directory:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
```

本Phaseのresult出力先:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
40_operator_prompts/
architecture_review/
01_runtime_entrypoint_inventory_result.md
```

調査開始時点のcommit SHAを必ず記録すること。

---

## 4. Core Investigation Question

最終的に、以下の問いへコード上のevidence付きで回答できる状態にすること。

> 現在の標準的なAriadne runtimeに対して、ユーザー操作・HTTP request・CLI・worker・background process・その他外部triggerが入った場合、Executionに関係する処理はどの入口から入り、どのApplication / Execution implementationへ最初に到達するか。

特に、

```text
External Trigger
    ↓
Runtime Root
    ↓
Boundary Entry Point
    ↓
Application Service / Use Case
    ↓
Execution orchestration boundary
```

までを追跡する。

本Phaseでは原則として、

```text
Execution orchestration boundary
    ↓
Result
    ↓
Artifact
    ↓
Lineage
```

の詳細なlifecycle追跡までは行わない。

それらは後続Architecture Reviewで扱う。

ただしEntry Pointを分類するために必要な範囲で、その先の呼出先を確認することは許可する。

---

## 5. Terminology

### 5.1 Runtime Root

OS、container、process manager、framework、user、external system等からapplication runtimeが開始される最上流の入口。

例:

* Docker / Compose command
* Python module execution
* ASGI / WSGI application
* CLI command
* worker process
* scheduler process
* frontend application startup
* shell / task runnerから起動されるapplication process

---

### 5.2 Boundary Entry Point

application外部からruntime内部へ処理が入るhandler / command / endpoint等。

例:

* HTTP endpoint
* WebSocket endpoint
* CLI subcommand
* worker task handler
* scheduled task
* message consumer
* frontendからbackendへ送信されるExecution関連request

---

### 5.3 Execution-Relevant Entry Point

以下のいずれかに到達する可能性があるBoundary Entry Point。

* Execution作成
* Execution開始
* Execution再開
* Execution retry
* Execution cancel
* analysis / workflow / pipeline実行
* stage / task dispatch
* Result生成
* Artifact生成
* Execution state mutation

単なるhealth checkや静的metadata取得など、Execution architectureに関係しない入口は詳細追跡対象外としてよい。

ただしRuntime Root自体のInventoryから除外してはならない。

---

### 5.4 Active Runtime Reachable

本調査では、単にPythonからimport可能であることを「active」とみなしてはならない。

`ACTIVE_RUNTIME_REACHABLE` は、現在のRepositoryに存在する標準的な起動構成・routing・dependency wiring等の静的証拠から、

```text
Runtime Root
→ Boundary Entry Point
→ target implementation
```

の到達経路を示せるものとする。

---

## 6. Reachability Classification

各Entry Point / pathは以下のいずれかに分類すること。

### `ACTIVE_RUNTIME_REACHABLE`

現在の標準runtime構成から到達可能であることを、静的コード・設定の連鎖で確認できる。

### `CONDITIONALLY_REACHABLE`

feature flag、configuration、registry selection、runtime parameter等の条件により到達可能。

条件を必ず記録すること。

### `TOOLING_ONLY`

developer utility、migration utility、maintenance script等であり、通常application runtimeからは使用されない。

### `TEST_ONLY`

test、fixture、test helper等からのみ到達することが確認できる。

### `UNREFERENCED_CANDIDATE`

定義は存在するが、Repository内の現在のruntime root / wiringから参照を確認できなかった。

これは「dead code」と同義ではない。

### `UNKNOWN`

静的調査だけでは到達可能性を確定できない。

---

## 7. Architecture Classification

各Execution-Relevant pathについて、最初に到達するExecution implementationを以下で分類すること。

### `LEGACY`

Executionに関係する最初の実装境界が `ariadne.legacy` 配下に存在する。

### `PRODUCT`

Executionに関係する最初の実装境界が `ariadne.product` 配下に存在する。

### `SHARED_OR_OTHER`

上記以外の共有層・別architectureへ到達する。

### `MIXED`

一つのruntime pathの中で、Execution orchestrationへ到達するまでにlegacy/product双方への実質的な依存が確認される。

### `UNKNOWN`

静的証拠だけでは分類不能。

---

## 8. Important Classification Rule

directory名だけでactive / inactiveを判定してはならない。

特に、

```text
src/ariadne/legacy/
```

に存在するという理由だけで、

```text
obsolete
unused
dead
delete candidate
```

と判定してはならない。

同様に、

```text
src/ariadne/product/
```

に存在するという理由だけで、

```text
canonical
active
target
current
```

と判定してはならない。

判定根拠は必ず、

```text
runtime configuration
→ registration / wiring
→ import / dependency
→ callable
```

のコード上の到達証拠とすること。

---

## 9. Investigation Scope

Repository全体を入口探索対象とする。

`src/ariadne/` のみを検索して終了してはならない。

少なくとも以下を確認すること。

### 9.1 Process / Deployment Roots

* Dockerfile
* Compose files
* container command / entrypoint
* Makefile / task runner
* shell scripts
* process startup configuration
* Python module startup
* application server startup
* worker startup

---

### 9.2 Python Packaging / CLI Roots

* `pyproject.toml`
* console scripts
* project scripts
* `__main__.py`
* CLI framework registration
* argparse / click / typer等のcommand registration
* direct executable modules

---

### 9.3 HTTP / Application Interface

* ASGI / WSGI application creation
* FastAPI / router registration等
* API route registration
* Execution関連endpoint
* dependency injection / application service wiring
* handlerからExecution implementationへの呼出経路

---

### 9.4 Worker / Background Execution

存在する場合は以下を確認する。

* worker process root
* task registration
* queue consumer
* background task
* scheduler
* dispatcher
* executor
* task handler

---

### 9.5 Frontend / UI

Repository内にfrontend / UI implementationが存在する場合、

* frontend runtime root
* analysis / execution開始操作
* 呼び出すbackend endpoint

までを確認する。

UI component内部の詳細状態管理は本Phaseの対象外としてよい。

目的は、

> 画面上のanalysis実行操作が、backendのどのBoundary Entry Pointへ到達するか

を確認することである。

静的に対応付けられない場合は `UNKNOWN` とする。

---

### 9.6 Legacy / Product Wiring

少なくとも以下を横断的に検索する。

```text
ariadne.legacy
ariadne.product
```

および相対importによる同等の参照。

特に、

* runtime rootからlegacyへの直接import
* runtime rootからproductへの直接import
* interface layerからlegacy/productへのimport
* dependency injection
* factory
* registry
* adapter selection
* worker wiring

を確認すること。

---

## 10. Investigation Method

調査方法は静的解析を基本とする。

使用してよいもの:

* `git`
* `git grep`
* `rg`
* `grep`
* `find`
* `sed`
* `cat`
* `head`
* `tail`
* `awk`
* `tree`
* tracked source/configurationの閲覧
* Python AST等を利用したread-only解析
* その他、Repository内容を変更しないread-only command

必要な追加検索はAgent自身で行ってよい。

ただし、検索は本Taskの範囲内に限定すること。

---

## 11. Prohibited Operations

以下を行ってはならない。

* production code変更
* test code変更
* configuration変更
* migration変更
* dependency変更
* dependency install
* formatter実行
* linterのauto-fix
* code generation
* database変更
* database reset
* migration実行
* container作成・削除
* volume変更
* application起動
* worker起動
* frontend起動
* test実行
* benchmark実行
* external API access
* network経由の調査
* source moduleをimportしてapplication codeを実行すること
* architecture変更
* refactoring
* bug fix
* unused code削除
* import整理
* documentationの修正

唯一許可される書き込み:

```text
01_runtime_entrypoint_inventory_result.md
```

およびその生成に不可欠なparent directoryの作成のみ。

---

## 12. Do Not Use Runtime Behavior as Evidence

本Phaseではapplicationを実行して到達経路を確認してはならない。

以下は禁止する。

```text
uvicorn ...
python -m <application module>
docker compose up
worker startup
frontend startup
curl against application
pytest
```

本Phaseの目的は、まず **Current Architectureの静的構造** を独立して取得することである。

runtime verificationが必要だと判明した場合は、resultの `Unresolved Items` に記録する。

Agent自身でruntime verificationへ進んではならない。

---

## 13. Investigation Procedure

以下の順序で調査すること。

### Step 1. Record Investigation Baseline

最初に以下を取得する。

* repository root
* current branch
* HEAD commit SHA
* working tree status
* investigation start time

current branchが

```text
refactor/ariadne_mvp_e4
```

でない場合は、それ以上のArchitecture調査を行わない。

resultに

```text
BLOCKED_WRONG_BRANCH
```

と記録して停止する。

working treeに既存変更がある場合は、それを記録する。

既存変更をstash、reset、checkout、restoreしてはならない。

---

### Step 2. Discover Runtime Roots

Repository全体からruntime起動候補を探索する。

候補例:

```text
Docker / Compose
ASGI / WSGI
uvicorn / gunicorn
__main__
console script
CLI
worker
scheduler
frontend startup
shell / task runner
```

候補を見つけたら、単にfile名を列挙するのではなく、

```text
external invocation
→ configured command
→ module
→ callable
```

を可能な限り特定する。

---

### Step 3. Discover Boundary Entry Points

各Runtime Rootから登録されるBoundary Entry Pointを確認する。

Execution-Relevantかどうかを分類する。

Execution-Relevantでないものについては、存在と分類のみ記録し、詳細なcall-chain追跡は不要。

---

### Step 4. Trace Execution-Relevant Paths

Execution-Relevant Entry Pointについて、

```text
Boundary Entry Point
→ handler
→ application service / use case
→ execution orchestration boundary
```

まで静的に追跡する。

各edgeについてコード上の証拠を残すこと。

---

### Step 5. Resolve Dependency Wiring

call先がinterface / protocol / factory / dependency provider / registry等で抽象化されている場合、その場で追跡を終了してはならない。

現在のruntime configurationにより実際に選択されるimplementationを可能な限り解決する。

特に、

```text
dependency injection
factory
registry
router registration
worker registration
configuration selection
```

を追跡する。

静的に一意に決められない場合は、条件と候補を示して `CONDITIONALLY_REACHABLE` または `UNKNOWN` とする。

---

### Step 6. Search Legacy / Product References

Runtime RootおよびExecution-Relevant Entry Pointから、

```text
ariadne.legacy
ariadne.product
```

への到達可能性を調査する。

単純な全文検索結果だけで判定しない。

import先が実際にruntime wiringへ組み込まれているか確認する。

---

### Step 7. Search Reverse Reachability

重要なlegacy/product Execution componentについて、逆方向にも参照元を確認する。

目的は、

> definitionが存在するがruntimeから参照されていない

というケースを識別することである。

ただし、参照を発見できなかったことだけを理由にdead codeと断定しない。

---

### Step 8. Record Unknowns

静的調査で解決不能な点を無理に推測しない。

以下を記録する。

* 何が不明か
* どこまでは確認できたか
* なぜ静的に確定できないか
* 確定するには何の追加evidenceが必要か

追加evidenceの種類は記載してよいが、その調査自体は実行しない。

---

## 14. Evidence Standard

Architecture上の主要な主張には必ずRepository内の証拠を付ける。

最低形式:

```text
<repository-relative-path>:<line or line-range>
Symbol: <module/class/function/variable>
Evidence: <what this proves>
```

例:

```text
src/.../api.py:42-58
Symbol: create_app
Evidence: the router containing the execution endpoint is registered here.
```

可能な場合はcall-chainの各edgeに証拠を付ける。

```text
A → B
Evidence: path/to/file.py:123, symbol foo()

B → C
Evidence: path/to/other.py:45, symbol bar()
```

---

## 15. Evidence Rules

以下を厳守すること。

### 15.1 Fact

コード・configurationから直接確認できる内容。

例:

```text
FACT:
router X registers endpoint Y.
```

---

### 15.2 Inference

複数のFactから合理的に導くが、直接記述されていない内容。

例:

```text
INFERENCE:
given the current router registration and dependency provider,
this endpoint appears runtime-reachable.
```

Inferenceには必ず根拠Factを併記する。

---

### 15.3 Unknown

証拠不足で判定不能な内容。

```text
UNKNOWN:
runtime configuration may select either implementation;
static configuration does not determine the value.
```

---

### 15.4 Prohibited Conclusion

以下のような証拠を超えた表現は禁止する。

```text
legacy is no longer needed
product is the correct architecture
this code should be deleted
this is definitely dead code
ENH-E4 should remove this component
```

これらは本Phaseの責務外である。

---

## 16. Required Result Structure

`01_runtime_entrypoint_inventory_result.md` は以下の構造で作成すること。

```markdown
# 01 Runtime Entry Point Inventory Result

## 1. Metadata

- Prompt:
- Repository root:
- Branch:
- HEAD:
- Working tree status:
- Started at:
- Finished at:
- Phase status:

## 2. Executive Inventory

### 2.1 Runtime Roots

| Root ID | Surface | Invocation | Definition / Config | Reachability | Evidence |
|---|---|---|---|---|---|

### 2.2 Execution-Relevant Entry Points

| Entry ID | Runtime Root | External Trigger | Boundary Entry Point | First Execution Boundary | Architecture | Reachability |
|---|---|---|---|---|---|---|

## 3. Runtime Root Details

### E4-ROOT-001 ...

#### Invocation

#### Registration / Wiring

#### Evidence

#### Reachability Classification

## 4. Execution-Relevant Entry Point Details

### E4-EP-001 ...

#### External Trigger

#### Runtime Root

#### Boundary Entry Point

#### Static Call Chain

#### First Execution Orchestration Boundary

#### Architecture Classification

#### Reachability Classification

#### Evidence

#### Unknowns

## 5. UI → Backend Execution Paths

| UI Action | Frontend Location | Backend Request | Backend Entry ID | Classification | Evidence |
|---|---|---|---|---|---|

If no repository-managed UI exists:

`N/A`

If static mapping cannot be established:

`UNKNOWN`

## 6. CLI Execution Paths

| CLI Command | Registration | Handler | Entry ID | Architecture | Reachability |
|---|---|---|---|---|---|

If none:

`NONE_CONFIRMED`

## 7. Worker / Background Execution Paths

| Worker / Task | Process Root | Registration | Handler | Architecture | Reachability |
|---|---|---|---|---|---|

If none:

`NONE_CONFIRMED`

## 8. Legacy / Product Runtime Exposure Matrix

| Component / Boundary | Legacy | Product | Runtime Reachability | Entry IDs | Evidence |
|---|---:|---:|---|---|---|

## 9. Observed Path Convergence / Divergence

Record only observed topology.

Examples:

- multiple external entry points converge on the same execution boundary
- one entry point can resolve to multiple implementations
- different entry points reach different implementations
- legacy and product components appear in the same call chain

Do not interpret these observations as a design defect or recommend a target architecture.

## 10. Unreferenced / Non-runtime Candidates

| Component | Classification | Search Performed | Evidence | Limitation |
|---|---|---|---|---|

Use `UNREFERENCED_CANDIDATE`, never `DEAD`, unless deadness is independently and conclusively established by evidence.

## 11. Unresolved Items

| ID | Question | Confirmed Facts | Why Unresolved | Additional Evidence Needed |
|---|---|---|---|---|

## 12. Facts

Number facts as:

- `E4-OBS-001`
- `E4-OBS-002`
- ...

Each observation must contain evidence.

## 13. Inferences

Number inferences as:

- `E4-INF-001`
- `E4-INF-002`
- ...

Each inference must reference the supporting `E4-OBS-*`.

If none:

`NONE`

## 14. Phase Conclusion

State only:

1. how many runtime roots were confirmed
2. how many Execution-Relevant entry points were confirmed
3. architecture classification counts:
   - LEGACY
   - PRODUCT
   - SHARED_OR_OTHER
   - MIXED
   - UNKNOWN
4. reachability classification counts
5. unresolved item count
6. whether the evidence is sufficient to proceed to the next Architecture Review phase

Do not recommend implementation changes.

## 15. Completion Status

One of:

- `COMPLETED`
- `COMPLETED_WITH_UNKNOWNS`
- `BLOCKED_WRONG_BRANCH`
- `BLOCKED`

```

---

## 17. Identifier Rules

Runtime Root:

```text
E4-ROOT-001
E4-ROOT-002
...
```

Execution-Relevant Entry Point:

```text
E4-EP-001
E4-EP-002
...
```

Observed Fact:

```text
E4-OBS-001
E4-OBS-002
...
```

Inference:

```text
E4-INF-001
E4-INF-002
...
```

Unresolved Item:

```text
E4-UNK-001
E4-UNK-002
...
```

IDはresult内で一意かつ安定して使用すること。

---

## 18. Completeness Criteria

本Phaseは以下をすべて満たした場合のみ `COMPLETED` または `COMPLETED_WITH_UNKNOWNS` とする。

### C1

Repository全体からRuntime Root候補を探索している。

### C2

確認したRuntime Rootについて起動command / module / callableの対応を可能な限り特定している。

### C3

Execution-Relevant Boundary Entry Pointを列挙している。

### C4

各Execution-Relevant Entry Pointについて、最初のExecution orchestration boundaryまで静的call-chainを追跡している。

### C5

各pathを `LEGACY / PRODUCT / SHARED_OR_OTHER / MIXED / UNKNOWN` に分類している。

### C6

各pathをreachability classificationに分類している。

### C7

主要な判断に `path + line + symbol` evidenceがある。

### C8

Fact / Inference / Unknownを分離している。

### C9

legacy/productというdirectory名だけからactive/inactiveを判断していない。

### C10

設計変更・削除提案・Target Architecture決定を行っていない。

### C11

source / test / configuration / migrationを変更していない。

### C12

指定されたresult文書以外を変更していない。

---

## 19. Final Self-Check

result生成後、以下のみ確認すること。

```text
git status --short
git diff --stat
git diff -- <result file>
```

期待されるRepository変更は、

```text
01_runtime_entrypoint_inventory_result.md
```

および必要ならそのparent directoryだけである。

既存working tree変更が調査開始時から存在していた場合、それらを自分の変更として扱わないこと。

既存変更を修正・restore・resetしてはならない。

---

## 20. Agent Response

作業完了時の最終応答は簡潔に以下を報告すること。

```text
01_runtime_entrypoint_inventory_result.md を生成しました。

Phase status: <COMPLETED | COMPLETED_WITH_UNKNOWNS | BLOCKED_WRONG_BRANCH | BLOCKED>
Runtime roots: <count>
Execution-relevant entry points: <count>
Unresolved items: <count>

Source/configuration/test/migration codeは変更していません。
```

詳細な分析内容はchat responseではなくresult文書を正本とする。

---

## 21. Stop Condition

以下のいずれかで停止する。

1. `01_runtime_entrypoint_inventory_result.md` を生成し、Final Self-Checkを完了した
2. branch不一致を確認した
3. Repositoryを静的に調査できないblocking issueが発生した
4. result以外のRepository変更なしでは調査を継続できないことが判明した

停止後、以下へ進んではならない。

* runtime verification
* Phase 02
* implementation
* refactoring
* deletion
* architecture redesign
* additional ENH-E4 work

次の作業は人間によるresult review後に別promptとして指示される。
