# ENH-E11 G03 P03 — refutation_methods

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G03 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G03_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G03_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 既存run(input_,output_dir) API不変。M12/M13実装再利用、M14/M15不足Kernel追加、seedと元Effect hash必須。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**科学/Designの必須制約:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 既存run(input_,output_dir) API不変。M12/M13実装再利用、M14/M15不足Kernel追加、seedと元Effect hash必須。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `RefutationAdapter` | `ariadne.scientific.refutation.adapter.RefutationAdapter` | Method Adapter ownership | `run(self, input_: RefutationInput, output_dir: Path)` → `list[ScientificResultDescriptor]` |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約がField/Constructor/公開Method/前後条件/失敗時の一次規範。所有するAdapterだけにMethod-specific preflight/executeを実装し、既存`RefutationAdapter`/`SensitivityAdapter`の公開`run` ABIを維持する。統合専用Packageは新Adapterを作らず、Product Scientific Kernelを共有する。

**Responsibility:** Method Adapterを担当するClassは `RefutationAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class contracts — normative here

次のField/Constructor/Method/Pre-Post/FailureはこのPxxの実装Contractを構成する。DDは由来情報に限り、実装Agentへの仕様補完委譲は禁止。実在Source/ABIは開始時に照合し、Designed Classを既存と断定しない。

### 3.1. `RefutationAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.refutation.adapter.RefutationAdapter`。 共通Field/Constructor表はtyped Bridge側の依存候補であり、既存Classに未実装Fieldを既成事実として追加しない。 DiagnosticのMethod実行Adapter。担当Method仕様：`P1-M12, P1-M13, P1-M14, P1-M15`。**既存Sourceの実装済みはP1-M12（PLACEBO_TREATMENT）とP1-M13（DATA_SUBSET）のみ。P1-M14（RANDOM_COMMON_CAUSE）とP1-M15（BOOTSTRAP）は本Class/Facadeでの新規実装が必要で、既存機能と称さない。 **再利用:** 既存RefutationAdapter.runはそのまま維持。必要ならMethod用typed façadeから共有処理を呼ぶ。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

**既存ABI契約:** 現行Classに宣言済みのInstance Fieldはない。MethodDescriptor/BackendFactory/ScientificContextは既存実装の属性ではなく、型付きPortから呼び出す新規Facade／Bridgeの依存として定義する。既存Classへの無断Field追加を前提にしない。

#### Constructor / Factory

**既存ABI契約:** ariadne.scientific.refutation.adapter.RefutationAdapter に明示的`__init__`はない。公開`run(input_, output_dir)`は変更しない。typed Facadeは別Classに配置し、旧ClassのConstructor ABIにDescriptorを注入しない。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `run(self, input_: RefutationInput, output_dir: Path)` | `list[ScientificResultDescriptor]` | **既存v2公開API**。互換維持。typed façadeは既存runを無検証castせず検証済み中間表現へ変換する |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M12` | placebo treatment | 事前指定置換ルール、null診断、再現seed |
| `P1-M13` | data subset | Subset規則、sample/support、差分の解釈 |
| `P1-M14` | random common cause | 摂動DGP/seed、条件付き安定性 |
| `P1-M15` | bootstrap refutation | resampling unit/CI可用性、同一DGP |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

既存`run(input_,output_dir)`のPath I/O/DTOはv2専用。Local型付き実行は共通の純粋計算Kernelを抽出する互換Bridgeから再利用し、新Portが旧Path writerを直接呼んでStaging制約を迂回してはならない。旧v2は従来のPath出力、新型付きAdapterは`StagingArtifactSink`だけに書く。旧DTOからの無検証CASTは禁止。Scientific Negativeとtechnical errorを分離。

#### 検証

`DD-E11-METH-P112`（`P1-M12`）、`DD-E11-METH-P113`（`P1-M13`）、`DD-E11-METH-P114`（`P1-M14`）、`DD-E11-METH-P115`（`P1-M15`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `DiagnosticPort` — standalone Class/Method contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.DiagnosticPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...
```

#### 処理仕様

診断結果を型付きで正規化し、未検証Science PASSにしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_causal_method_adapters.md)、Runtime/Publicationは[30_62](30_62_local_execution_publication.md)参照。

#### 検証

DD-E11-METH-P101〜P313。

## 4. Required execution — method-specific coding order (G03/P03)

1. **Entry/preflight:** G03/G02 upstream canonical 999、Frozen06/07/Pxx、Owner Coding Authorization、Source/lock SHA、依存Pxx checkpointを確認。Method×Operation×Design×Estimand×Inference×Backendをstrictに検証し、失敗時はtyped negativeまたはtechnical errorを返す。
2. 既存`RefutationAdapter.run(input_, output_dir)`は公開Product ABIとして変更せず、typed DiagnosticPortからのbridgeを別責務として配置。
3. `P1-M12` Placeboは元Effect/Design hashを固定して置換機構/seedを明示。`P1-M13` Subsetは選定前のRuleと支持条件、`P1-M14` random common causeは扰動DGP/seed、`P1-M15` bootstrapは再標本化単位/繰返し/CIの適格性を記録。
4. Refutation統計量・差分とその科学的解釈を分け、refutationで有意差がなかったことを因果識別の証明にしない。
5. **Postconditions:** Placebo/Subsetting/Random common cause/Bootstrapは変更条件とベースEffect hash、Seed/Resampling Unitを固定。検定結果≠因果識別。
6. **Publication & compatibility:** Kernel結果をtyped portable Effect/Diagnosticに正規化し、G01のStagingSink/Publisherを使用。自己publish、Resultへのraw model/行データ混入、未承認row export、旧v2 API変更、silent Backend fallbackは禁止。
7. **Error boundaries:** illegitimate negative/unsupported CI, invalid config, numerical nonconvergence, missing dependency, FS/Policy denialを別Status/Reasonとし、Technical SUCCESSからScience PASSを推論しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M12` Placebo Treatment refutation／null診 | `DD-E11-METH-P112` | DGP-022; NEG-014 | REF-R01 | AC-D01, AC-R01, AC-T01 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M13` Data Subset refutation／安定性 | `DD-E11-METH-P113` | DGP-001, DGP-002; NEG-015 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M14` Random Common Cause refutation／摂動安 | `DD-E11-METH-P114` | DGP-002; NEG-017 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M15` Bootstrap refutation／再標本化安定性 | `DD-E11-METH-P115` | DGP-001, DGP-002; NEG-016 | REF-R01 | AC-D01, AC-D03, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |

**Proof boundary:** 本Pxx§5のDGP/NEG/REF/ACは全件独立科学検証義務である。IDの列挙は実Fixture/独立Reference生成済みやPASSを意味しない。Backend自己出力を真値としない。FWER=.05・K/R/Compute/MC-SE/CI coverageと閾値はFreeze前に決定し、未確定はBLOCKED。別文書を読んで値を推測・補完しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g03/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Method-specific acceptance and observation

- §5の各Methodに対しDGP/NEG/独立REF/DD IDをすべて実行義務として追跡する。登録IDがあることはTest fixtureが実在・PASSしたことを意味しない。
- **Required test semantics:** 既存`RefutationAdapter.run(input_, output_dir)`は公開Product ABIとして変更せず、typed DiagnosticPortからのbridgeを別責務として配置。 `P1-M12` Placeboは元Effect/Design hashを固定して置換機構/seedを明示。`P1-M13` Subsetは選定前のRuleと支持条件、`P1-M14` random common causeは扰動DGP/seed、`P1-M15` bootstrapは再標本化単位/繰返し/CIの適格性を記録。 Refutation統計量・差分とその科学的解釈を分け、refutationで有意差がなかったことを因果識別の証明にしない。
- Schema+Method validation（unit）、Class.Port/Result provenance（contract）、実有効Backend/CLI/Publisher/旧v2（integration）を区別。Independent scientific DGP/Oracleは適格な真値から導出し、Estimator自己出力をReferenceにしない。
- Evidenceにsource/lock/fixture SHA、Method/Estimand/Inference、positive+negativeのexpected/observed、実効Backend/API/config/seed、collect済path/command/Resultを残す。Filesystem/科学証拠が未取得ならBLOCKED、期待値緩和によるPASSは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P06。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Self-contained freeze review boundary

- 本文§3で必要なClassのConstructor・Field・公開Method・処理責務、§4で実装順序/分岐、§5〜6でMethod別のScience/Testを保持する。外部DDやGate06を読ませて不足仕様を推測させない。
- **未確定事項:** 既存RefutationAdapter ABI Bridgeと各Methodのresampling・統計判定。 未解決のBackend API、Method Config、DGP/NEG/Reference/quantitative Science、Owner Decisionは該当MethodをBLOCKEDとし、Freeze前に閉じる。
