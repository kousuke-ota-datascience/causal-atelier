# ENH-E10 向け Test Architecture Handoff

**状態:** `ACTIVE_HANDOFF`  
**対象:** ENH-E10 planning / implementation / verification / operator workflow authoring  
**前提:** repository-wide Comprehensive Test Code MigrationはENH-E12以降へdefer

## 1. Handoffの目的と設計起点

ENH-E10は、repository全体のtest code migration完了を待たずに開始・完了してよい。ただしtest estateは過渡期であり、新architectureと旧配置が共存する。

本handoffで最も重要な設計起点は次である。

> **Browser E2Eでproduct semanticsと本質的に無関係な要因によりGateを止めない。**

AriadneではBrowser E2Eが長期間、stale locator、obsolete navigation、historical runner、Docker/build context、fixture、service/environment drift等によって、本来検証したいproduct behaviorへ到達する前に停止する鬼門になっていた。

ENH-E10ではこの問題をtest architecture / verification workflow側の設計責務として扱う。具体的には、Browser E2Eの責務をcritical cross-layer connectivityへ限定し、詳細なcorrectnessをlower deterministic layerへ寄せ、test-side failureをproduct failureから明確に分離する。

## 2. ENH-E10で採用するmigration policy

ENH-E10でrepository全体のtest estateを先に再編しない。

minimum rule:

- ENH-E10で新規作成またはmaterially rebuiltするtestは新architectureを使用する;
- ENH-E10で実際に必要な既存testだけをbatch単位で移行してよい;
- current invariantか未判定の既存testは旧pathに残してよい;
- 「ENH-E10で使わない」だけを理由にarchiveしない;
- historical / supersededと確認できたtestのみ `legacy_archive` 対象とする;
- moveに伴うdependencyは同一batchでatomicに修正する;
- feature implementationとrepository-wide cleanupを混同しない。

Comprehensive Test Code Migration / Repository-wide Test Architecture ReconciliationはENH-E12以降の独立scopeとする。

## 3. Classification model — regression観点と配置を分ける

Test分類は少なくとも次の2軸を分ける。

### 3.1. Lifecycle / authority axis

```text
regression
ancement
characterization
benchmark
support
legacy
```

### 3.2. Verification layer axis

```text
unit
contract
integration
frontend
browser_e2e
```

重要なのは、**regression観点を持つtestが必ず `tests/regression/` に置かれるわけではない**ことである。

ENH-E10で新しいbehaviorを追加・変更する際、既存behaviorのregression protectionを同時に確認するtestでも、ENH-E10由来のstaging testであれば原則として `tests/enhancement/enh_e10/...` から開始してよい。

`tests/regression/` は、Enhancement provenanceを超えて今後もcurrent authoritative product behaviorとして恒久的に守るtestのauthorityである。

したがって:

```text
regression-like assertion != tests/regression lifecycle authority
```

と理解する。

## 4. Target structureとENH-E10で許容するtransition state

### 4.1. Target structure

最終的なtargetは次を基本とする。

```text
tests/
├── regression/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   ├── frontend/
│   └── browser_e2e/
├── enhancement/
│   └── <enhancement>/<gate>/
│       ├── unit/
│       ├── contract/
│       ├── integration/
│       ├── frontend/
│       └── browser_e2e/
├── characterization/
│   └── scientific/
├── benchmarks/
│   └── scientific/
├── support/
│   ├── fixtures/
│   ├── factories/
│   └── helpers/
└── legacy_archive/
```

### 4.2. ENH-E10で新規・変更testを置く場所

```text
tests/enhancement/enh_e10/<gate>/<layer>/
```

例:

```text
tests/enhancement/enh_e10/g01/unit/
tests/enhancement/enh_e10/g01/contract/
tests/enhancement/enh_e10/g02/frontend/
tests/enhancement/enh_e10/g02/browser_e2e/
```

### 4.3. ENH-E10期間中に許容する共存

```text
tests/enhancement/...   # new architecture
tests/product/...       # existing / unrecertified current tests
tests/browser_e2e/...   # historical runnersを含み得る
tests/integration/...
tests/scientific/...
tests/legacy_archive/...
```

この共存状態をtarget architecture完成とはみなさない。

`tests/regression/` は空directoryを作ること自体を目的にしない。明確なcurrent invariantをPROMOTE / REWRITE / MERGEするsemantic decisionが生じた時点で実体化してよい。

## 5. Existing testを移動・再構築するときのatomic rule

Test fileだけをmoveしてはならない。必要に応じて同一batchで次を確認・修正する。

```text
file path
import
fixture / conftest resolution
Path(__file__) / repository-root resolution
pytest marker / collection
Dockerfile COPY
.dockerignore
compose / Browser entrypoint
CI command / path reference
output / evidence path
```

固定directory depthへ依存する `Path(__file__).parents[N]` は移動に弱いため、repository marker（例: `pyproject.toml`）等からrootを探索する方式を優先する。

Browser E2Eを新architectureへ置く場合は、source fileだけでなくBrowser imageのbuild contextに含まれることまで確認する。

Migrationはtest architecture workであり、product semantic change、Acceptance Criteria変更、frozen verification contract変更を伴ってはならない。

## 6. `10_enhance_instruction/` authoringで守ること

基本原則:

```text
10 = WHAT must be implemented / verified
40 = WHERE / HOW execution discovers and runs it
```

### 6.1. Gate 06

Gate-level 06は次をauthorityとして定義する。

- Gate claim
- required behavior
- protected semantics / regression protection
- dependency
- execution mode
- required package set

Testのphysical pathをGate semanticsにしない。

### 6.2. Pxx

Pxxはassigned implementation scopeとfocused verification casesをself-containedにする。

書くべきもの:

- input / state / output behavior
- protected invariant
- negative behavior
- deterministic verification case
- completion / stop condition

原則として次のようなhistorical path固定は避ける。

```text
tests/product/some_old_test.py を実行せよ
```

新規test placementは40側のCoding Agent operational policyに任せる。

### 6.3. 07

07はIndependent Verificationの **WHAT to verify** のauthorityとする。

記述対象:

- Acceptance Criteria
- protected regression
- required verification layer
- Browser E2Eがmandatoryか
- mandatoryならcritical journey
- numeric/scientific correctnessのprimary proof layer

07をtest-file-path authorityにしない。test directory migrationだけを理由にfrozen 07を変更しない。

## 7. `40_operator_workflows/` authoringで守ること

### 7.1. Coding Agent

Coding Agent promptには、ENH-E10で新規またはmaterially rebuiltするtestを原則として次へ置くruleを持たせる。

```text
tests/enhancement/enh_e10/<gate>/<layer>/
```

assigned Package / Gateと無関係なexisting testのrepo-wide migrationは行わせない。

### 7.2. Independent Test Agent

Independent Test Agentはcurrent repository stateからtest implementationをdiscoverする。

第一探索先:

```text
tests/enhancement/enh_e10/<gate>/
```

必要に応じてtransition stateとして次も探索してよい。

```text
tests/product/
tests/integration/
tests/scientific/
tests/browser_e2e/
```

Completion Report、過去Test Evidence、過去Enhancement文書に記載されたtest path / commandはhistorical evidenceであり、current physical location authorityではない。

実行前にpath existence / collection / current runner suitabilityを確認する。

### 7.3. Candidate後のtest-side change

Fixed Candidate後にtest code / orchestration / documentationが変化していても、それだけでproduct candidateを再freezeしない。

post-candidate diffを少なくとも次へ分類する。

```text
PRODUCT_SEMANTIC_CHANGE
TEST_IMPLEMENTATION_CHANGE
TEST_ORCHESTRATION_CHANGE
TEST_INFRASTRUCTURE_CHANGE
DOCUMENTATION_ONLY
```

product semantic impactを一意に否定できない場合だけcandidate identityをBLOCKEDとする。

### 7.4. Test Agentはtest-side repairを実装しない

Independent Test Agentがtest implementation / orchestration / environment defectを検出した場合、product FAILへ短絡せずBLOCKEDとしてrepair owner/actionを明示する。

repairは別execution responsibilityへ分離し、修復後にIndependent Verificationを再開する。

ENH-E9で作成した `31_blocked_test_repair_01_test_infrastructure_agent_prompt.md` はG02 Trial01専用special handlingであり、ENH-E10へ標準promptとしてコピーしてはならない。

ENH-E10で同種の事象が実際に発生した場合、その具体的blockerに対してEnhancement-specific special handlingを設計するか、別途generic routeを設計する。

## 8. Browser E2E policy — 非本質的停止をGate failureにしない

### 8.1. Browser E2Eの主責務

Browser E2Eは少数のcritical user journeyに限定し、主に次を証明する。

```text
UI
-> routing/state
-> API
-> worker/execution
-> persistence/result
-> user-visible continuation
```

詳細なbusiness/scientific/numeric correctness、細かいbranch logic、網羅的validationはlower deterministic layerをprimary proofとする。

### 8.2. Authoritative runner selection

Historical runnerをfilenameや過去Enhancement名だけでcurrent authorityとみなさない。

runnerは次を満たす必要がある。

- current UI/navigationへ到達できる;
- current API/runtimeと整合する;
- 07のcritical journey responsibilityを満たす;
- stale locator / obsolete routeへ依存しない;
- failure時にlast successful checkpoint / route / screenshot / trace / log等を残せる。

### 8.3. Failure classification

Browser failure時は少なくとも次へ分類する。

```text
PRODUCT_DEFECT
TEST_IMPLEMENTATION_DEFECT
TEST_ORCHESTRATION_DEFECT
TEST_ENVIRONMENT_DEFECT
UNKNOWN
```

`TEST_IMPLEMENTATION_DEFECT`、`TEST_ORCHESTRATION_DEFECT`、`TEST_ENVIRONMENT_DEFECT`、`UNKNOWN`でproduct correctnessを判断できない場合はproduct `FAIL` とせず `BLOCKED` とする。

### 8.4. Synchronization / environment

fixed sleepをprimary synchronizationにしない。route、visible element、enabled state、network/output condition、execution/result state等のobservable conditionを優先する。

Browser image / service / fixture / datasetは可能な限りhermeticかつ再現可能にする。

### 8.5. Acceptance Criteriaを弱めない

Historical runnerがcurrent workflowへ到達できない場合、Acceptance Criteriaを削る・testをskipする・assertionを弱めるのではなく、test implementation / orchestrationをcurrent journeyへ追従させる。

これが「Browser E2Eで本質的ではないところでコケたくない」という設計目的の直接的な運用ルールである。

## 9. ENH-E10終了時のtest disposition

ENH-E10のtestをすべて即座に `tests/regression/` へ移す必要はない。

Enhancement終了時には少なくとも概念上、次のdispositionを意識する。

```text
PROMOTE
REWRITE
MERGE
SPLIT
RETIRE
ARCHIVE
KEEP_ENHANCEMENT
```

明確にEnhancement provenanceを超えてcurrent product invariantとして恒久保護すべきtestを先行PROMOTEしてもよい。ただしsemantic decisionとして記録する。

repository-wide全件の再認証とcanonical regression suite全面再構築はE12以降へ残す。

## 10. ENH-E10でblocking prerequisiteにしないこと

Feature scope上必要でない限り、次をENH-E10開始/完了のblocking prerequisiteにしない。

- E1-E9 test全件の再分類;
- `tests/regression/` の全面構築;
- historical Browser runner全件の統廃合;
- `tests/product/` 等の旧directory完全撤去;
- fixture / conftest / CI / Docker体系の全面再編。

## 11. ENH-E12以降への引き継ぎ

Comprehensive Test Code Migration / Repository-wide Test Architecture Reconciliationで次を行う。

- E1以降の既存test全件をcurrent requirements / current behaviorと再照合;
- PROMOTE / REWRITE / MERGE / SPLIT / RETIRE / ARCHIVEをfile-by-file確定;
- canonical regression suiteを再構成;
- historical Browser runnerからcurrent critical journeyを抽出・統廃合;
- fixture / conftest / CI / Docker / marker体系を整理;
- 旧test directoryを段階的に撤去;
- target architectureへの収束をverificationする。

## 12. ENH-E10開始時チェックリスト

```text
[ ] 新規/materially rebuilt testのplacement ruleを40へ反映した
[ ] 06/Pxx/07がhistorical physical test pathをAcceptance authorityにしていない
[ ] Independent Test Agentがcurrent repositoryからtestをdiscoverする
[ ] Browser E2Eをcritical connectivityへ限定した
[ ] Browser failure classification / BLOCKED semanticsを40へ反映した
[ ] Test Agentとtest-side repair responsibilityを分離した
[ ] test move時のPath/import/fixture/Docker/CI dependencyをatomicに扱う
[ ] regression観点と tests/regression lifecycle authorityを混同していない
[ ] E9 G02専用31 promptを標準promptとしてコピーしていない
[ ] repository-wide comprehensive migrationをENH-E10のblocking prerequisiteにしていない
```

## 13. Authority boundary

本handoffはAriadne repository固有のtest architecture transition ruleであり、ENH-E10のcanonical requirement、Gate 06/Pxx/07、Gate Decisionをoverrideしない。

また、このtransition debt固有のruleをgeneric enhancement workflow templateのproduct semanticsへ混入させない。
