# ENH-E4 E4-G06 P02 Structural Writer Cutover Instruction

- Project: Ariadne / causal-atelier
- Enhancement: ENH-E4 eliminate dual execution
- Branch: `refactor/ariadne_mvp_e4`
- Gate: `E4-G06`
- Gate Name: Lineage authority consolidation
- Trial: `01`
- Work Package: `P02`
- Package Name: Structural writer cutover
- Document Type: Coding Agent Work Package Instruction
- File:
  `10_enhance_instruction/G06/06_G06_P02_structural_writer_cutover_instruction.md`
- Governing Control Document:
  `10_enhance_instruction/G06/06_G06_P00_work_package_plan.md`
- Previous Package Instruction:
  `10_enhance_instruction/G06/06_G06_P01_authority_policy_instruction.md`
- Fixed G06 Architecture Baseline:
  `aae491519472f87bfbda88069eb1e65a858a9fcc`
- P01 Implementation Checkpoint:
  `ad982f55b73e9602ba7430f6a4820c1bd96b009d`
- P01 Documentation / Process-Deviation Checkpoint:
  `904ebfb58afd891319c73d974cfc356099352b97`
- Product Migration Head at P01 Completion:
  `20260809_product_0010`
- Transition Debt:
  `E4-TD-004 OPEN -> G06`

---

# 1. Instruction Status

本書は E4-G06 Trial01 の Coding Agent execution package `P02` を実行するための指示書である。

本書を単独で解釈してはならない。

必ず以下を先に読むこと。

```text
10_enhance_instruction/G06/
06_G06_P00_work_package_plan.md
```

```text
10_enhance_instruction/G06/
06_G06_P01_authority_policy_instruction.md
```

およびP01実績:

```text
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P01_implementation_checkpoint_report.md
```

P00はG06全体のgoverning control documentである。

P01はlineage authority classifier / generic-only admission policyを確立済みであり、P02はそのauthority semanticsを変更してはならない。

---

# 2. P02 Purpose

P02の目的は、

```text
TYPED_STRUCTURAL relation
```

について、

```text
canonical Product path
    ->
generic authoritative LineageEdgeOrm write
```

を停止することである。

Target:

```text
typed canonical authority
    = sole structural authority

generic persisted lineage
    != duplicate structural authority
```

P02完了時の必須状態:

```text
active canonical Product path:
structural generic NEW WRITE = 0
```

---

# 3. P02 Is Not the Whole G06

P02はE4-G06全体を完了させない。

P02終了時:

```text
E4-G06:
NOT_COMPLETE

Trial:
01

TD-004:
OPEN
```

でなければならない。

P02では以下を完了させない。

```text
P03:
generic-only writer convergence
unapproved/unknown generic writer convergence

P04:
typed lineage read reconstruction

P05:
closure / traversal / export projection convergence

P06:
retry / rerun / revise lineage regression
Gate-wide negative authority audit

P07:
Gate-wide completion / fixed candidate / READY_FOR_TEST
```

---

# 4. P02 Entry Rule

P01で発生したprocess deviationを繰り返してはならない。

P02実装は、

```text
06_G06_P02_structural_writer_cutover_instruction.md
```

がrepositoryへcommitされた後に開始する。

したがって本書に固定する:

```text
904ebfb58afd891319c73d974cfc356099352b97
```

は、

```text
P02 preparation baseline
```

であり、

```text
P02 Entry SHA
```

ではない。

P02 Entry SHAはCoding Agent開始時のactual HEADで取得する。

---

# 5. Start-of-Work Verification

最初に以下を実行する。

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git log --oneline -20
```

Expected branch:

```text
refactor/ariadne_mvp_e4
```

次に:

```bash
git merge-base --is-ancestor \
  904ebfb58afd891319c73d974cfc356099352b97 \
  HEAD
echo $?
```

Expected:

```text
0
```

P02 instructionがcommit済みであること:

```bash
git ls-files --error-unmatch \
  docs/wiki/develop_memo/_work/20260808-01_ENH-E4_eliminate_dual_execution/10_enhance_instruction/G06/06_G06_P02_structural_writer_cutover_instruction.md
echo $?
```

Expected:

```text
0
```

P02 Entry SHA:

```bash
git rev-parse HEAD
```

で取得し、Package Checkpoint Reportへ記録する。

---

# 6. Dirty Working Tree Rule

`git status --short` が空でない場合:

1. changed/untracked fileを列挙する。
2. operator/docs-only changeか、production/test changeかを区別する。
3. user/operatorの変更をsilentに破棄しない。
4. P02 implementationと競合する未説明production changeがある場合は開始しない。

その場合:

```text
G06-P02_BLOCKED
```

として報告する。

---

# 7. P01 Fixed Result

P02はP01で成立した以下を前提とする。

```text
LineageAuthority:
    TYPED_STRUCTURAL
    GENERIC_ONLY
    PROJECTION_ONLY
    OUT_OF_SCOPE
```

```text
classify_lineage_authority(
    source_type,
    relation_type,
    target_type,
)
```

```text
assert_generic_lineage_allowed(...)
```

P01でapprovedされたtyped structural tuples:

```text
Execution --GENERATED--> Result

Result --GENERATED--> Artifact

DatasetVersion --USED_INPUT--> Execution

AnalysisView --USED_INPUT--> Execution

Result --USED_INPUT--> Execution

Result --DERIVED_FROM--> GraphVersion

Artifact --DERIVED_FROM--> DatasetVersion

Execution --DERIVED_FROM--> Execution

Execution --REVISED_FROM--> Execution
```

P02はこのclassifierを勝手に拡張・縮小しない。

authority contract修正が必要ならP02で暗黙変更せず、stop/escalateする。

---

# 8. P01 Residual Writer Inventory

P01 Checkpoint Reportでは少なくとも以下がP02 residual writerとして記録されている。

```text
src/ariadne/product/application/predictive_split_service.py::_lineage()

src/ariadne/product/application/predictive_workflow_service.py::_lineage()

src/ariadne/product/application/exploratory_service.py::_add_lineage()
```

ただし、P02はfile/helper単位で削除するのではなく、

```text
runtime reachability
+
semantic tuple
+
authority class
```

単位で切り替える。

---

# 9. Critical Distinction: Active Canonical vs Retired Unreachable Code

G05 PASS後、repositoryにはretired Family lifecycle implementation bodyが残っている。

例:

```text
raise LegacyProductAuthorityDisabled(...)
```

の後ろにhistorical codeが存在する。

P02のprimary acceptance targetは:

```text
active canonical Product write path
```

である。

したがってwriter inventoryでは必ず以下へ分類する。

```text
ACTIVE_CANONICAL

RETIRED_UNREACHABLE

GENERIC_ONLY_ACTIVE

UNCLASSIFIED_ACTIVE

OUT_OF_SCOPE_LEGACY
```

重要:

```text
sourceにLineageEdgeOrm文字列が残っている
```

ことだけで、

```text
active structural authorityが残っている
```

と判定してはならない。

逆に:

```text
retired codeだから無視
```

としてruntime path確認を省略してもならない。

---

# 10. P02 Scope

P02 primary scope:

```text
Causal
Exploratory
Predictive
```

の:

```text
active canonical Product write paths
```

におけるTYPED_STRUCTURAL generic duplicate write。

P02 secondary scope:

```text
retired/unreachable structural writerのclassification
```

まで。

broad legacy deletionはG07へ送る。

---

# 11. P02 Semantic Unit

writerのcutoverはhelper function単位ではなくsemantic tuple単位で行う。

例えばmixed helper:

```text
_lineage(...)
```

が:

```text
TYPED_STRUCTURAL
GENERIC_ONLY
UNCLASSIFIED
```

をすべて書いている場合、

```text
helper全部削除
```

を原則としない。

P02では:

```text
TYPED_STRUCTURAL calls
    ->
stop generic persistence
```

のみを確実に実施する。

GENERIC_ONLYはP03のauthority convergenceまで維持する。

UNCLASSIFIEDは勝手にGENERIC_ONLY扱いしない。

---

# 12. Formal Structural Writer Rule

P02の中心rule:

```text
if classify_lineage_authority(
    source_type,
    relation_type,
    target_type,
) == TYPED_STRUCTURAL:

    direct generic LineageEdgeOrm write
        = forbidden on active canonical Product path
```

許容される実装:

```text
call site removal

mixed helper call removal

typed sourceを使うようworkflow修正

structural generic write branch elimination
```

禁止:

```text
generic edgeを書いて後で削除

generic edgeを書いてinactive flagを立てる

same semanticsを別relation名でgeneric persist

classifierをGENERIC_ONLYへ書き換えてtestを通す

typed structural relationをevidence_jsonで偽装
```

---

# 13. Causal Scope

P01 residual reportではCausal active structural writerは明示されていない。

P02では:

```text
Causal:
no active structural generic writer
```

を推測でFactsにしてはならない。

actual source inventoryを行う。

最低限:

```bash
rg -n \
  "LineageEdgeOrm|USED_INPUT|GENERATED|DERIVED_FROM|REVISED_FROM" \
  src/ariadne/product \
  src/ariadne/web \
  src/ariadne/worker
```

actual directoryが異なる場合はrepository treeに合わせる。

Causal canonical submit/process pathを特定し、

```text
TYPED_STRUCTURAL generic new-write:
0
```

を確認する。

既に0ならproduction change不要。

---

# 14. Exploratory Active Canonical Submit Path

verified P01-completion sourceでは:

```text
ExploratoryWorkspaceService.submit_execution()
```

のcanonical branchが:

```text
ExecutionService.create_family_execution(...)
```

でcanonical Executionを作成した後に:

```text
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
```

を `_add_lineage()` でgeneric persistする。

これらはP01 policy上:

```text
TYPED_STRUCTURAL
```

である。

P02ではactive canonical submit pathからこのgeneric writeを停止する。

---

# 15. Exploratory Typed Authority Preservation

generic writeを削除した結果、typed authorityそのものを失ってはならない。

少なくともcanonical Executionには:

```text
dataset_version_id
```

が存在する。

Exploratory family-specific canonical snapshotには:

```text
analysis_view_id
execution_plan_id
family_spec
```

等が保持される。

P02では:

```text
DatasetVersion -> Execution
AnalysisView -> Execution
```

のgeneric duplicate rowを停止するが、

```text
canonical Execution state
```

を変更・消去しない。

read reconstructionはP04で行う。

---

# 16. Exploratory Retired Body

`submit_execution()` のcanonical return後にはretired Family ORM branchが残っている。

また:

```text
claim_next()
process_execution()
```

は`LegacyProductAuthorityDisabled`で拒否され、その後ろにhistorical bodyが残る。

P02では:

```text
broad dead-code deletion
```

を必須としない。

ただしPackage Reportで:

```text
retired unreachable structural writers
```

として列挙する。

G07 boundaryへ送る。

---

# 17. Predictive Active Canonical Submit Path

verified P01-completion sourceでは:

```text
PredictiveWorkflowService._canonical_submission()
```

がcanonical Executionを作成した後:

```text
ResearchContextVersion --USED_INPUT--> Execution
DatasetVersion --USED_INPUT--> Execution
AnalysisSpecification --USED_INPUT--> Execution
ExecutionPlan --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
```

をdirect `_lineage()` helperでpersistする。

P02では、この集合を一括して「全部structural」と推測して削除してはならない。

P01 classifierを使ってtupleごとに分類する。

---

# 18. Predictive Formally TYPED_STRUCTURAL Calls

P01 policyで明示的にTYPED_STRUCTURALなのは少なくとも:

```text
DatasetVersion --USED_INPUT--> Execution

AnalysisView --USED_INPUT--> Execution
```

である。

したがってactive canonical predictive submit pathにおけるこの2 relationのgeneric writeは必ず停止する。

Expected:

```text
canonical Predictive submit succeeds

product_lineage_edge:
DatasetVersion USED_INPUT Execution = 0

product_lineage_edge:
AnalysisView USED_INPUT Execution = 0
```

ただしcanonical Executionのinput identityは保持する。

---

# 19. Predictive Unclassified USED_INPUT Calls

P01 fixed classifierでは少なくとも以下はTYPED_STRUCTURAL tupleに含まれていない。

```text
ResearchContextVersion --USED_INPUT--> Execution

AnalysisSpecification --USED_INPUT--> Execution

ExecutionPlan --USED_INPUT--> Execution
```

P02でこれらを:

```text
GENERIC_ONLY
```

へ勝手に分類してはならない。

また:

```text
P02だからstructuralだろう
```

という推測だけでclassifierを拡張してはならない。

P02では以下のいずれかにする。

### Case A — Formal contract / existing approved designからauthorityが一意に解決できる

そのauthorityに従う。

ただしP01 policy修正が必要なら:

```text
P01 contract correction needed
```

として明示し、scope impactを評価する。

### Case B — authorityが一意に解決できない

```text
UNCLASSIFIED_ACTIVE
```

としてPackage Reportへ記録し、P03/P04またはoperator decisionへ送る。

P02 completionを阻害するかは:

```text
AC-003 structural generic dual-write
```

に該当する確証があるかで判断する。

---

# 20. Predictive Mutation Relation

retired Family branchには:

```text
Execution --DERIVED_FROM/REVISED_FROM--> Execution
```

generic writerが存在する。

P01 policy上:

```text
TYPED_STRUCTURAL
```

である。

しかしactive canonical mutation authorityはcanonical Executionの:

```text
base_execution_id
revision_kind
change_reason
```

で保持される。

P02では:

1. active canonical mutation pathがgeneric structural edgeを書いていないか確認する。
2. 書いているなら停止する。
3. retired/unreachable Family branchのwriterはbroad cleanupせずclassification可能。

mutation semanticのfull acceptanceはP06。

---

# 21. Execution -> Result / Result -> Artifact

P01 policy上:

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
```

はTYPED_STRUCTURAL。

G04/G05後のcanonical Product authorityでは:

```text
Result.execution_id
Artifact.result_id / execution ownership
```

等がauthorityである。

P02ではactive canonical Result/Artifact persistence pathをinventoryし、

```text
same semantic relation
    ->
LineageEdgeOrm generic duplicate write
```

が存在しないことを確認する。

存在する場合は停止する。

---

# 22. Retired Family Output Writers

Predictive / Exploratory historical `process_execution()` bodiesには:

```text
Execution --GENERATED--> Result
Result --GENERATED--> Artifact
```

等のgeneric writesが残る。

これらが:

```text
LegacyProductAuthorityDisabled
```

によりruntime到達不能であることを確認する。

P02ではG07 broad legacy deletionへ越境しない。

ただし:

```text
RETIRED_UNREACHABLE
```

としてPackage Reportへ明示する。

---

# 23. PredictiveSplitService Boundary

`PredictiveSplitService.validate_and_save()` はG05後:

```text
raise LegacyProductAuthorityDisabled(...)
```

でretired mutation authorityを拒否している。

そのhistorical bodyには:

```text
DatasetVersion --USED_INPUT--> Execution
AnalysisView --USED_INPUT--> Execution
Execution --GENERATED--> Artifact
```

等のgeneric writesが存在する。

P02では:

```text
active canonical Product path
```

ではないことを確認する。

broad historical implementation deletionはG07へ送る。

ただしsource-level negative auditでfalse positiveにならないようPackage Reportで:

```text
retired/unreachable exemption
```

を明記する。

---

# 24. Generic-only Preservation Rule

P02は以下のapproved generic-only relationを削除しない。

例:

```text
Artifact --DERIVED_FROM--> Artifact

Result --SUMMARIZES--> Result

Result --SUMMARIZES--> Artifact

approved DOCUMENTS

approved EVIDENCE_FOR / SUPPORTED_BY

approved MOTIVATED

approved SELECTED / REJECTED
```

P02の目的は:

```text
generic lineage row数を減らすこと
```

ではない。

目的は:

```text
structural duplicate authorityをなくすこと
```

である。

---

# 25. P03 Boundary

以下はP03で行う。

```text
generic-only direct writerをP01 central policyへ収束

annotation SELECTED/REJECTED writer convergence

Predictive EVIDENCE_FOR/DOCUMENTS/SUMMARIZES writer convergence

Exploratory MOTIVATED writer convergence

unapproved generic direct writer handling
```

P02でこれらを全面変更しない。

---

# 26. P04 Boundary

P02でstructural generic writerを止めると、

```text
existing readerがgeneric edge依存
```

している場合、一時的にread projectionが欠ける可能性がある。

P02ではread correctnessのためにgeneric structural writerを復活させない。

P04が:

```text
typed authority
    ->
structural lineage projection
```

を担当する。

ただしP02 focused testは:

```text
canonical source stateが保持されている
```

ことを確認する。

---

# 27. P05 Boundary

以下はP05。

```text
closure source_class
export source_class
synthetic projection
projection-only semantics
```

P02でclosure/exportを修正しない。

---

# 28. P06 Boundary

以下はP06。

```text
retry/rerun/revise end-to-end lineage semantics

Gate-wide static negative writer audit

Gate-wide runtime negative authority audit
```

P02ではpackage-local negative auditまで。

---

# 29. Database / Migration Boundary

P02は原則:

```text
Migration:
NONE
```

とする。

理由:

```text
duplicate generic writerの停止
```

はexisting schemaのwrite-path correctionであり、schema changeを必要としない。

P02ではhistorical generic structural rowsのbackfill/delete migrationを追加しない。

clean bootstrap / migration cleanupはG07/G08 boundaryを尊重する。

---

# 30. Historical Row Rule

P02 acceptanceは:

```text
new Product write
```

のauthority cutover。

existing test DB / historical row cleanupをP02のためにproduction migrationとして実装しない。

もしexisting persisted structural edgeがread testを壊す場合:

```text
test database reset
```

と:

```text
production historical migration requirement
```

を区別する。

後者が本当に必要ならFacts/Interpretationとして報告する。

---

# 31. Recommended Implementation Strategy

推奨順序:

```text
1. writer inventory

2. active / retired reachability classification

3. classify_lineage_authority()でsemantic tuple分類

4. active TYPED_STRUCTURAL call siteだけをcutover

5. generic-only calls preserve

6. unclassified calls record, do not guess

7. focused unit/static test

8. real PostgreSQL runtime negative-write test

9. protected G05 submit/lifecycle regressions

10. checkpoint commit

11. package checkpoint report
```

---

# 32. Do Not Use Generic Guard as Runtime Suppression Hack

P01の:

```text
assert_generic_lineage_allowed()
```

をdirect system writerの前に置いて、

```text
InvalidSchemaをcatchして無視
```

するだけの実装は禁止。

P02 targetは:

```text
structural generic write pathそのものをなくす
```

ことである。

禁止例:

```python
try:
    assert_generic_lineage_allowed(...)
    self._lineage(...)
except InvalidSchema:
    pass
```

これはauthority cutoverではなくerror suppressionである。

---

# 33. Canonical Source State Must Remain Complete

P02でgeneric duplicate edgeを削除する際、

```text
canonical typed/snapshot authority
```

を失わない。

最低限:

```text
Execution.dataset_version_id

Execution.input_result_id

Execution.base_execution_id

Execution.revision_kind

Result.execution_id

Artifact.result_id / execution ownership
```

等のG02-G05 canonical authorityを保全する。

non-causal snapshot fieldsも既存G05 semanticsを保持する。

---

# 34. No Authority Expansion

P02のtestが失敗したからといって:

```text
_TYPED_STRUCTURAL_TUPLES
```

からtupleを削除してはならない。

また:

```text
_GENERIC_ONLY_TUPLES
```

へstructural tupleを移動してはならない。

P01 contractが誤っている証拠がある場合はstop/escalateする。

---

# 35. Required New Tests

P02 focused testを新規作成する。

推奨:

```text
tests/product/
test_enh_e4_g06_p02_structural_writer_cutover.py
```

```text
tests/product/
test_enh_e4_g06_p02_structural_writer_cutover_postgres.py
```

必要ならfamily-specific fileへ分割してよい。

例:

```text
test_enh_e4_g06_p02_exploratory_writer_postgres.py

test_enh_e4_g06_p02_predictive_writer_postgres.py
```

ただしpackage ID `p02` をfile名から識別可能にする。

---

# 36. Required Static/Unit Test — Writer Classification

少なくとも以下を表形式またはparameterized testで固定する。

```text
Exploratory canonical:
DatasetVersion USED_INPUT Execution
    -> active + TYPED_STRUCTURAL + generic write forbidden

Exploratory canonical:
AnalysisView USED_INPUT Execution
    -> active + TYPED_STRUCTURAL + generic write forbidden

Predictive canonical:
DatasetVersion USED_INPUT Execution
    -> active + TYPED_STRUCTURAL + generic write forbidden

Predictive canonical:
AnalysisView USED_INPUT Execution
    -> active + TYPED_STRUCTURAL + generic write forbidden
```

さらにactive canonical Causal pathをinventoryし:

```text
structural generic writer count = 0
```

をtestまたはexplicit auditで証明する。

---

# 37. Required Runtime Test — Exploratory Submit

real PostgreSQLでcanonical Exploratory submitを実行する。

Expected:

```text
canonical Execution:
created

analysis_family:
EXPLORATORY

dataset_version_id:
correct

analysis_view_id snapshot:
preserved if provided

product_lineage_edge:
DatasetVersion USED_INPUT Execution
    = 0

product_lineage_edge:
AnalysisView USED_INPUT Execution
    = 0
```

submission自体が成功すること。

---

# 38. Required Runtime Test — Predictive Submit

real PostgreSQLでcanonical Predictive submitを実行する。

Expected:

```text
canonical Execution:
created

analysis_family:
PREDICTIVE

dataset_version_id:
correct

analysis_view_id:
preserved

analysis_specification_id:
preserved in canonical snapshot

execution_plan_id:
preserved in canonical snapshot

product_lineage_edge:
DatasetVersion USED_INPUT Execution
    = 0

product_lineage_edge:
AnalysisView USED_INPUT Execution
    = 0
```

P02でunclassified predictive USED_INPUT tuplesを残す場合、そのrow有無を明示的にassert/reportする。

silentに無視しない。

---

# 39. Required Runtime Test — Typed Ownership Output

active canonical Product processing pathについて、最低1 familyで:

```text
Execution -> Result
Result -> Artifact
```

のgeneric duplicate rowが新規作成されないことを確認する。

Expected:

```text
canonical Result ownership:
exists

canonical Artifact ownership:
exists where artifact is produced

product_lineage_edge:
Execution GENERATED Result
    = 0

product_lineage_edge:
Result GENERATED Artifact
    = 0
```

既存G04/G05 test fixtureを再利用してよい。

---

# 40. Required Runtime Test — Mutation Structural Duplicate

P02ではmutation full semanticsをP06へ残すが、active canonical rerun/revise submitで:

```text
Execution DERIVED_FROM Execution

Execution REVISED_FROM Execution
```

のgeneric edgeが新規作成されないことを可能な範囲で確認する。

既存G05 rerun/revise testを利用してよい。

P02で新しいmutation semanticsを作らない。

---

# 41. Required Retired-Path Test

少なくとも以下がstill rejectedであることを確認する。

```text
PredictiveSplitService.validate_and_save()

PredictiveWorkflowService.claim_next/process_execution legacy facade

ExploratoryWorkspaceService.claim_next/process_execution legacy facade
```

全部をP02新規testに複製する必要はない。

G05 existing shutdown regressionsを利用する。

目的:

```text
retired bodyにgeneric writerが残っても
Product runtime authorityではない
```

ことを維持する。

---

# 42. Protected Regression — G05 Submission Convergence

最低限:

```text
tests/product/test_enh_e4_g05_submission_convergence.py
```

からP02変更に関連するCausal/Exploratory/Predictive submit nodeを選定する。

exact node IDをinventoryして実行する。

---

# 43. Protected Regression — Exploratory

最低限:

```text
tests/product/test_enh_e4_g05_phase_b_exploratory_postgres.py
```

のcanonical submission/read lifecycleに関係するnodeを選ぶ。

P02でExploratory submitを壊していないことを確認する。

---

# 44. Protected Regression — Predictive

最低限:

```text
tests/product/test_enh_e4_g05_phase_c_authority_audit_postgres.py
```

または:

```text
test_enh_e4_g05_phase_c_rerun_postgres.py
test_enh_e4_g05_phase_c_revise_postgres.py
```

からP02 affected pathを覆うnodeを選ぶ。

P02のためにretry queue semantics等を変更してはならない。

---

# 45. P01 Regression

P01 policyを壊していないことを確認する。

Pure:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p01_lineage_authority_policy.py
```

PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p01_authority_policy_postgres.py \
  -q
```

---

# 46. Standard P02 Verification Commands

推奨pure/static:

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run pytest -q \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py
```

real PostgreSQL:

```bash
scripts/test/run_product_postgres_tests.sh \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover_postgres.py \
  -q
```

family別に分けた場合はactual file名へ置換する。

---

# 47. Standard PostgreSQL Rule

real PostgreSQL acceptance evidenceは:

```text
scripts/test/run_product_postgres_tests.sh
```

を標準entry pointとする。

acceptance evidenceの主経路として以下を使用しない。

```text
manual docker run
manual network/IP
manual DSN
manual psql bootstrap
manual Alembic
manual external pytest
```

各runner invocationについて:

```text
exact command
exit code
passed
failed
skipped
evidence directory
tested SHA/state
```

を記録する。

---

# 48. Clean Semantic Partition Rule

G05で確認されたstate contaminationを考慮し、以下を必要に応じて分割する。

```text
P02 focused tests

Exploratory regression

Predictive regression

mutation regression

legacy shutdown regression
```

一つの巨大pytest invocationを必須にしない。

combined failureが発生した場合:

```text
isolated PASSだけでfixture defect確定
```

としてはならない。

---

# 49. Required Static Audit

P02実装後:

```bash
rg -n \
  "LineageEdgeOrm|USED_INPUT|GENERATED|DERIVED_FROM|REVISED_FROM" \
  src/ariadne/product
```

を実行する。

結果を以下に分類する。

```text
ACTIVE_CANONICAL_TypedStructural
ACTIVE_CANONICAL_GenericOnly
ACTIVE_CANONICAL_Unclassified
RETIRED_UNREACHABLE
PROJECTION_READ
TEST_ONLY / NONE
```

P02 complete時:

```text
ACTIVE_CANONICAL_TypedStructural
    = 0
```

でなければならない。

---

# 50. Required Runtime Negative Audit

focused PostgreSQL testで最低限:

```text
canonical Exploratory submit
canonical Predictive submit
```

後に:

```sql
product_lineage_edge
```

をqueryし、

P01 policyでTYPED_STRUCTURALと分類されるrowが新規作成されていないことをassertする。

可能ならtest helperで:

```text
classify_lineage_authority(row.source_type, row.relation_type, row.target_type)
```

を使い:

```text
TYPED_STRUCTURAL row count = 0
```

を検証する。

ただしhistorical fixture rowとcurrent transaction rowを混同しない。

clean DB runnerを利用する。

---

# 51. Generic-only Row Preservation Check

P02変更対象serviceにgeneric-only output writerが同居する場合、P02変更で削除されていないことを確認する。

例:

```text
Artifact DERIVED_FROM Artifact
```

等。

ただしgeneric-only writerのpolicy convergence自体はP03。

P02では:

```text
accidental deletionがない
```

ことを見る。

---

# 52. Unknown / Unclassified Row Reporting

P02 static/runtime auditで:

```text
classify_lineage_authority(...) == None
```

となるactive direct generic writerを発見した場合、必ずreportする。

Required fields:

```text
source type
relation
target type
writer path
runtime reachability
current evidence payload
canonical source state if any
why P02 did/did not modify it
recommended owner package
```

P02で勝手にauthorityを決めない。

---

# 53. Current Predictive Unclassified Candidates

P02開始時点のknown candidates:

```text
ResearchContextVersion --USED_INPUT--> Execution

AnalysisSpecification --USED_INPUT--> Execution

ExecutionPlan --USED_INPUT--> Execution
```

これらはP01 fixed classifier上unapproved/unclassified。

P02 Agentはactual P02 Entry SHAで再確認する。

これらについて:

```text
GENERIC_ONLY
```

と断定してはならない。

---

# 54. Current Retired Structural Candidates

known retired/unreachable candidates:

```text
PredictiveSplitService historical writer

PredictiveWorkflowService legacy Family submit/process body

ExploratoryWorkspaceService legacy Family submit/process body
```

P02では:

```text
runtime unreachable evidence
```

を確保する。

G07 broad source retirementへ送る。

---

# 55. No Broad Helper Deletion Rule

`_lineage()` / `_add_lineage()` helperを削除するとgeneric-only writerまで壊れる場合:

```text
helperを残す
```

または:

```text
generic-only helperへ縮小
```

する。

P03でcentral generic-only writerへconvergeする余地を残す。

---

# 56. No Read-side Fix in P02

P02で既存lineage response testが失敗し、

```text
structural generic edgeが消えたためread結果が減った
```

場合、そのfailureを:

```text
writer復活
```

で解決しない。

分類:

```text
expected transitional read gap
    -> P04 target

unexpected protected API contract break
    -> assess whether P04 must be advanced or package blocked
```

とする。

P00 package boundaryを無視してP04 full implementationへ越境しない。

---

# 57. No Closure Fix in P02

closure/export testがstructural generic edge removalで失敗しても:

```text
closureへgeneric writerを追加
```

しない。

P05 targetとして記録する。

---

# 58. P02 Production Change Candidates

Primary:

```text
src/ariadne/product/application/exploratory_service.py
```

```text
src/ariadne/product/application/predictive_workflow_service.py
```

Potentially, active writer inventoryにより:

```text
other Product application/workflow modules
```

が追加される。

`predictive_split_service.py` はretired/unreachable boundaryであるため、production modificationは必須ではない。

---

# 59. Domain Policy Change Rule

P02で:

```text
src/ariadne/product/domain/lineage.py
```

を変更するのは原則避ける。

P01 policyはfixed package result。

変更が必要な場合:

```text
why P01 classification is insufficient
formal source
impact on P01 tests
```

を明示する。

semantic authority変更ならlocal P02 fixではなくcontract escalation候補。

---

# 60. Migration Rule

Expected:

```text
Migration:
NONE
```

new migrationを作成した場合、P02 complete前に:

```text
necessity
scope
why G07/G08では遅いか
```

をreportする。

単にold rowsを消したいという理由では追加しない。

---

# 61. Expected P02 Tests

最低限:

```text
1. Exploratory canonical submit creates zero typed-structural generic edges.

2. Predictive canonical submit creates zero P01-classified typed-structural generic edges.

3. Causal canonical path has zero active typed-structural generic writer.

4. canonical Execution input state remains present.

5. canonical Result/Artifact ownership remains present.

6. P01 generic-only manual writer still works.

7. P01 structural manual writer still rejects.

8. retired Family mutation/process facade remains disabled.

9. active typed-structural direct-writer static inventory = 0.
```

---

# 62. P02 Package Completion Conditions

以下を全て満たした場合のみ:

```text
G06-P02_COMPLETE
```

とする。

```text
1. P02 governing instruction was committed before execution.

2. P02 Entry SHA is recorded.

3. active canonical writer inventory is complete for Causal/Exploratory/Predictive.

4. every active direct generic writer is classified by reachability and semantic authority.

5. active canonical TYPED_STRUCTURAL generic write call sites are removed/disabled.

6. Exploratory DatasetVersion USED_INPUT Execution generic write is gone.

7. Exploratory AnalysisView USED_INPUT Execution generic write is gone.

8. Predictive DatasetVersion USED_INPUT Execution generic write is gone.

9. Predictive AnalysisView USED_INPUT Execution generic write is gone.

10. active canonical Execution GENERATED Result duplicate generic write is absent.

11. active canonical Result GENERATED Artifact duplicate generic write is absent.

12. active canonical Execution base/revision duplicate generic write is absent.

13. generic-only relations are not accidentally deleted.

14. unclassified active generic writers are explicitly reported, not guessed.

15. retired/unreachable writers are separately classified.

16. P01 authority policy tests remain PASS.

17. focused P02 tests PASS.

18. focused real PostgreSQL tests PASS.

19. relevant G05 protected regressions PASS.

20. standard PostgreSQL evidence is recorded.

21. no unauthorized migration.

22. implementation checkpoint commit is created.

23. P02 Package Checkpoint Report is created.

24. E4-G06 remains NOT_COMPLETE.

25. TD-004 remains OPEN.
```

---

# 63. Implementation Checkpoint Commit

P02 production/test changesとfocused verificationが完了したらimplementation checkpoint commitを作成する。

禁止:

```bash
git add .
```

actual changed filesを明示的にstageする。

例:

```bash
git add \
  src/ariadne/product/application/exploratory_service.py \
  src/ariadne/product/application/predictive_workflow_service.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover.py \
  tests/product/test_enh_e4_g06_p02_structural_writer_cutover_postgres.py
```

actual file構成に合わせる。

commit message例:

```text
E4-G06 P02 cut over structural lineage writers
```

commit後:

```bash
git rev-parse HEAD
```

を取得する。

これを:

```text
P02 Implementation Checkpoint SHA
```

とする。

---

# 64. P02 Package Checkpoint Report

P02完了時:

```text
docs/wiki/develop_memo/_work/
20260808-01_ENH-E4_eliminate_dual_execution/
20_implementation_reports/G06/Trial01/packages/
E4-G06_01_P02_implementation_checkpoint_report.md
```

を作成する。

P00 Package Checkpoint Report contractに従う。

---

# 65. Required P02 Report Fields

最低限:

```text
Gate:
E4-G06

Trial:
01

Package:
P02

Package Status:
COMPLETE / BLOCKED

G06 Architecture Baseline:
aae491519472f87bfbda88069eb1e65a858a9fcc

P01 Implementation Checkpoint:
ad982f55b73e9602ba7430f6a4820c1bd96b009d

P01 Docs/Process Checkpoint:
904ebfb58afd891319c73d974cfc356099352b97

P02 Entry SHA:
<actual>

P02 Implementation Checkpoint SHA:
<actual>

Product Migration Head:
<actual>

Changed Production Files:
<exact paths>

Changed Test Files:
<exact paths>

Migration:
NONE / exact migration

Active Canonical Writer Inventory:
<exact table>

Retired/Unreachable Writer Inventory:
<exact table>

Unclassified Active Writer Inventory:
<exact table>

Causal Active Structural Generic Write:
0 / nonzero

Exploratory Active Structural Generic Write:
0 / nonzero

Predictive Active Structural Generic Write:
0 / nonzero

Generic-only Preservation:
PASS / FAIL / NOT_RUN

P01 Regression:
<exact commands/results>

P02 Focused Tests:
<exact commands/results>

PostgreSQL Evidence:
<exact commands/results/evidence directories>

G05 Protected Regressions:
<exact commands/results>

Facts:
...

Interpretation:
...

Unknown / Unconfirmed:
...

Residual P03 Work:
...

Residual P04 Work:
...

Residual G07 Legacy Work:
...

TD-004:
OPEN

Gate Status:
E4-G06 NOT_COMPLETE

Next Package:
P03

git status --short:
<exact output>
```

---

# 66. Report Commit

P02 Package Checkpoint Report作成後、report-only commitを作成してよい。

ただし:

```text
report commit SHA
    !=
P02 Implementation Checkpoint SHA
```

tested implementation identityは:

```text
P02 Implementation Checkpoint SHA
```

で固定する。

---

# 67. P02 Final Agent Output

Coding Agentは終了時に以下を報告する。

```text
Package status:
G06-P02_COMPLETE
or
G06-P02_BLOCKED

Gate status:
E4-G06 NOT_COMPLETE

Trial:
01

G06 architecture baseline:
aae491519472f87bfbda88069eb1e65a858a9fcc

P01 implementation checkpoint:
ad982f55b73e9602ba7430f6a4820c1bd96b009d

P02 preparation baseline:
904ebfb58afd891319c73d974cfc356099352b97

P02 entry SHA:
<sha>

P02 implementation checkpoint SHA:
<sha>

Product migration head:
<value>

Changed production files:
<exact paths>

Changed/new test files:
<exact paths>

Migration:
NONE
or exact migration

Causal active typed-structural generic writer:
0 / nonzero

Exploratory active typed-structural generic writer:
0 / nonzero

Predictive active typed-structural generic writer:
0 / nonzero

Unclassified active generic writers:
<exact tuples/paths or NONE>

Retired/unreachable structural writers:
<exact paths/tuples or NONE>

Pure/static tests:
<exact commands/results>

PostgreSQL tests:
<exact commands/results/evidence directories>

P01 regressions:
<exact commands/results>

G05 protected regressions:
<exact commands/results>

TD-004:
OPEN

Package report:
<exact path>

git status --short:
<exact output>
```

---

# 68. P02 Must Not Declare

P02終了時に以下を宣言してはならない。

```text
E4-G06 PASS

READY_FOR_TEST

TD-004 CLOSED

all generic-only writers converged

typed read reconstruction complete

closure/export convergence complete

mutation lineage complete

legacy lineage source retired
```

---

# 69. Stop / Escalation — Authority Contradiction

以下の場合、推測で変更しない。

```text
same source/relation/target tuple
```

について:

```text
P01 fixed classifier
```

と:

```text
formal approved lineage contract
```

が矛盾する場合。

その場合:

```text
G06-P02_BLOCKED
```

として:

```text
Facts
P01 classification
Formal contract
Observed writer
Why P02 cannot safely cut over
Required decision
```

を報告する。

---

# 70. Stop / Escalation — Read Contract Hard Dependency

TYPED_STRUCTURAL generic writeを停止すると、current externally required Product APIが重大に壊れ、

```text
P04を待つことができない
```

というformal dependencyが存在する場合:

```text
writerを復活
```

させず、

```text
PACKAGE_BLOCKED
```

としてP04 sequencing decisionを要求する。

単なるexisting test failureだけではblockと決めない。

---

# 71. Stop / Escalation — Missing Typed Authority

P01がTYPED_STRUCTURALと分類するrelationについて、

```text
generic writerを削除すると
canonical source stateからrelation identityを再構成不能
```

であることがactual codeで判明した場合:

```text
generic writeを残す
```

のではなくstopする。

これは:

```text
P01/P00 authority contract
vs
actual canonical model
```

の矛盾候補。

Factsを提示する。

---

# 72. Facts / Interpretation / Unknown

P02 reportでは必ず:

```text
Facts
Interpretation
Unknown / Unconfirmed
```

を分離する。

例:

```text
Fact:
Predictive canonical submit writes DatasetVersion USED_INPUT Execution.

Fact:
P01 classifier marks the tuple TYPED_STRUCTURAL.

Fact:
canonical Execution stores dataset_version_id.

Interpretation:
generic edge is duplicate structural authority.

Action:
remove generic write in P02.
```

対して:

```text
Fact:
Predictive canonical submit writes ResearchContextVersion USED_INPUT Execution.

Fact:
P01 classifier returns None for this tuple.

Fact:
research context id is present in family snapshot.

Unknown:
whether the formal target authority intends this relation to be a typed
structural projection or a non-authoritative snapshot-only reference.

Action:
do not invent authority in P02; report for follow-up.
```

---

# 73. Root Cause Rule

test failureが発生してもroot causeを証拠なしに断定しない。

許容:

```text
NOT_REPRODUCED
ROOT_CAUSE_UNCONFIRMED
```

禁止:

```text
probably fixture issue
```

だけでtestを書き換えること。

---

# 74. No Test-fitting

禁止例:

```text
test projectだけLineageEdgeOrm writeをskip

specific execution IDだけskip

pytest環境変数でstructural writerを無効化

relation_typeを別文字列に変更してclassifierを回避

generic edgeをcommit後にtest内でdelete

read testを通すためstructural writerを復活
```

---

# 75. P02 Expected Exit State

successful P02 completion時:

```text
Package:
P02 COMPLETE

P01 central authority policy:
PRESERVED

Active canonical structural generic writer:
0

Generic-only writer convergence:
NOT YET COMPLETE

Unclassified direct generic writers:
EXPLICITLY INVENTORIED

Typed read reconstruction:
NOT YET COMPLETE

Closure/export projection:
NOT YET COMPLETE

Mutation lineage full audit:
NOT YET COMPLETE

Legacy historical structural writer source:
MAY REMAIN RETIRED/UNREACHABLE

E4-G06:
NOT_COMPLETE

TD-004:
OPEN
```

---

# 76. Immediate Next Package

P02 COMPLETE後は停止する。

次package:

```text
G06-P03
Generic-only authority convergence
```

planned instruction:

```text
10_enhance_instruction/G06/
06_G06_P03_generic_only_convergence_instruction.md
```

P02 Coding AgentがP03へ自動継続してはならない。
