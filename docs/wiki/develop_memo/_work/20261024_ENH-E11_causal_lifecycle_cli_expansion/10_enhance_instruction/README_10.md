# 10_enhance_instruction — Gate契約・実行指示の作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでGate / Trial / Work Packageと06 / 07 / P00 / Pxx / 08 / Rxx / 09の作り分けが分かること。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。


## 1. Purpose

`10_enhance_instruction/`には、各Gateについて**何を成立させるか、何をもってPASSとするか、実装作業をどのexecution unitへ分けるか、formal FAIL後にどうremediateするか**を定義する。

```text
G01/
  06 = Gate Coding Contract
  P00 = Work Package Plan (conditional)
  06_Gxx_Pxx = planned Coding execution package (conditional)
  07 = Gate Verification Contract
  08 = Trial Remediation Contract (formal FAIL後のみ; DELTA / CONSOLIDATED)
  08_Gxx_Rxx = remediation Coding execution package (conditional)
  09 = Gate Contract Amendment record (contract defect時のみ)
```

## 2. Gate / Trial / Work Package

### Gate — Acceptance Contract

Gateは、**作業結果が後続工程から契約上依存可能になったか**を判定するsemantic acceptance boundaryである。実装量・難易度・Agentが一度に扱える量だけを理由にGateを分割しない。

### Trial — Candidate Verification Attempt

Trialは、同一Gate contractに対してcandidateを作り、Fixed Trial Candidateとして固定し、Independent Verificationの正式判定を受けるtransactionである。Agent restartやpackage correctionだけでTrial番号を増やさない。

### Work Package — Coding Execution Unit

Work Packageは、Gateを成立させる実装をbounded execution unitへ分割したものである。Package COMPLETEはGate PASS、verified-state derivation、downstream unlockを意味しない。

## 3. Document self-containment rule

### Primary Execution Contract — MUST self-contained

以下はAgentへ直接与えるprimary contractなので、担当責務に必要なnormative semanticsを本文内に持つ。

- `06 Gate Coding Contract`
- `07 Gate Verification Contract`
- `Pxx planned Work Package instruction`
- `Rxx remediation Work Package instruction`

外部pathはfact / evidence / source / provenance / observation targetとして参照してよい。**別workflow文書を読まなければ実装規則・Acceptance Criteria・completion conditionが分からない状態を作らない。**

### Derived Contract

`08`と`09`は既存contractから派生するため、外部contractへのtraceabilityを保持する。ただし用途は異なる。

- `08` — formal FAIL後のnext Trial remediation。`DELTA` / `CONSOLIDATED`をFAIL evidence確定後に選ぶ。
- `09` — original Gate semantic contract / Acceptance Criteria自体の欠陥をHuman-approved changeとして記録する。09で直接実行を継続するのではなく、承認後にaffected primary contractsをre-baselineする。

## 4. 06 Gate Coding Contract — MUST

06はGate implementation semanticsの一次契約である。最低限以下を本文内に記載する。

- Gate objective / downstream usable result after PASS
- required implementation semantics
- allowed / prohibited scope
- Execution Mode: `SINGLE_EXECUTION` or `WORK_PACKAGE`
- protected passed-Gate contracts
- Transition Debt constraints
- schema / migration / API / runtime policy
- Coding-side verification obligations
- Candidate Assembly requirement
- required outputs / stop condition

Control Sheet、requirements、design、previous Gate Decision等へのpathはprovenance / verified fact取得用であり、06のnormative implementation semanticsを外部へ委譲しない。

## 5. 07 Gate Verification Contract — MUST

07はGate Acceptance Criteriaの一次契約である。最低限以下を本文内に記載する。

- Gate acceptance claim
- Acceptance Criteria
- Test Item plan / primary test layer allocation
- Browser E2E critical journey plan（applicableな場合。canonical Gate blocking suite全体は原則3〜5本程度、各Gateはrelevant subsetのみ）
- Browser E2E canonical command / hermetic environment / synchronization / failure evidence requirements（applicableな場合）
- Fixed Trial Candidate identity rule
- protected passed-Gate regression requirement
- Transition Debt acceptance expectation
- evidence requirements
- PASS / FAIL / BLOCKED semantics
- Test Agent prohibited work
- required outputs

06を読まなければACが分からない構造にしない。Completion Report、source、runtime、previous test evidence等はobservation / evidenceとして参照してよい。

Test planningでは各requirement / ACへ最適なtest layerを割り当てる。Browser E2Eはdetailed correctnessの一次証明ではなく、少数のcritical user journeyがreal system boundaryを跨いで成立することの最終確認に使う。共通authoring policyは`40_operator_workflows/BROWSER_E2E_GATE_POLICY.md`を参照してよいが、Gate固有のblocking E2E item、command、environment、synchronization、assertion、evidence、decision semanticsは07本文へ具体化する。

## 6. Work Package Mode

### 発動条件

次のいずれかが成立し、1 execution unitではfailure localization / restart / focused verificationが不安定になる場合に使用する。

- execution scopeが大きい
- semantic implementation boundaryが複数ある
- dependency DAGがある
- intermediate checkpointが必要
- subsystem / authority boundaryを跨ぐ
- packageごとにfocused verificationが必要

### P00 — orchestration plan

P00はimplementation packageではない。P00自身の責務についてself-containedにし、次を記載する。

- Work Package mode採用理由
- Gate semantic boundaryの要約
- package map / dependency DAG
- package entry / exit criteria
- checkpoint / restart policy
- Candidate Assembly rule
- Trial completion condition

### Pxx — primary execution contract

PxxはAssigned Agentへ直接渡せる状態にする。Parent 06 / P00 pathはtraceabilityとして残してよいが、Pxx実行に必要なeffective constraintsはPxx本文へ記載する。

## 7. 06 / 07 freeze

06 / 07はGate execution開始前にfreezeする。implementation failure、package都合、Test FAILを理由に、過去Trialが依拠したcontractをsilent rewriteしない。

## 8. 08 Trial Remediation Contract — formal FAIL後のみ

08の目的は、original 06 / 07をimmutableに保持したままnext Trialのremediationを定義することである。

### Step 1 — Contract validity check

FAIL evidence確定後、まずoriginal Gate semantic claim / Acceptance Criteriaが依然として正しいか確認する。

- 正しい -> 08を作成する。
- 誤っている -> 08で再定義せず09を作成する。

### Step 2 — Mode selection

`08`のheaderに`Remediation Mode: DELTA / CONSOLIDATED`を明記する。

**DELTA**を選ぶ条件:

- 06 / 07の大部分がそのまま有効
- failure / correction scopeが局所的
- required parent sectionsが少ない
- `parent context + 08 delta`の方が小さく明確

DELTAでは、参照必須となる06 / 07 / failed decisionを明示し、failure facts、correction delta、forbidden workaround、追加verification、next candidate ruleを記載する。

**CONSOLIDATED**を選ぶ条件:

- remediationが複数領域へ及ぶ
- Work Package decomposition / execution orderが大きく変わる
- implementation / verification requirementsを多数横断する
- 1文書へ統合した方がcontext fragmentation / ambiguityが小さい

CONSOLIDATEDでは、next Trialに必要なeffective implementation semantics、verification requirements、scope、prohibitions、protected constraints、completion conditionを08内へ統合する。


### Operational resolution rule — current Trial 08

formal FAIL後にAgent executionへ入る場合、`GATE_ID + TRIAL_NO`からcurrent Trialの08を**exactly one**へ解決できなければならない。canonical pathは次とする。

```text
10_enhance_instruction/G01/
  08_ENH-E11_G01_{{TRIAL_NO}}_Remediation_Instruction.md
```

0件または複数候補の場合は推測・fallbackせず`BLOCKED_REMEDIATION_CONTRACT_MISSING`または`BLOCKED_CONTRACT_AMBIGUITY`とする。旧Trialの08を代用しない。

`40_fail_remediation_01_fail_rework_coding_agent_prompt.md`へ直接渡す08は、normative-source isolationを成立させるため`CONSOLIDATED`かつ`SINGLE_EXECUTION`とし、current 08だけでrework implementation / verification / completion conditionを一意に判断できる状態にする。`DELTA`またはRxx decompositionを選択する場合は、当該direct entry promptをそのまま使用しない。

## 9. Rxx Remediation Work Package — primary execution contract

Work Package remediation時はoriginal Pxx identityを再利用せず`R01-R99`を使う。RxxはAgentへ直接渡すため**self-contained MUST**とし、Parent 08のmodeにかかわらず、担当Rxxを実行するためのeffective constraintsを本文内に記載する。

## 10. 09 Gate Contract Amendment

09は、original 06 / 07のsemantic contractそのものが不適切と判明した場合のexplicit Human-approved amendment recordである。

最低限:

- contract defect
- why remediation is insufficient
- Before / After semantic change
- affected Acceptance Criteria
- protected passed-Gate impact
- invalidated P00 / package instructions
- Trial handling
- approval evidence
- required re-baseline artifacts

09自体を「失敗したのでACを緩める」手段にしてはならない。承認後はaffected primary contractsを明示的にre-baselineする。

APPROVED / APPLIED amendmentは`00_enhance_background/80_contract_amendment_log.md`にもappend-onlyで記録し、09・re-baseline artifacts・Git traceabilityを相互参照可能にする。80 ledgerはnormative execution authorityではない。

## 11. Authority summary

```text
06 = implementation semantic authority
07 = acceptance authority
P00 = execution decomposition authority
Pxx / Rxx = bounded execution authority; 06/07 semantic contractをsilent overrideしない
08 = next-Trial remediation authority; DELTA / CONSOLIDATED
09 = explicit contract-change decision authority
999 Gate Decision = final independent PASS / FAIL / BLOCKED authority
```

<!-- BEGIN MANAGED: V005_LOCAL_AUTHORITY -->
## v0.05 runtime authority

Gate local READMEはHuman navigation / canonical artifact index専用であり、execution eligibilityを変更しない。

Normal-path routing authority:

```text
Gate dependency declaration = Gate 06 `Depends on`
Execution mode              = Gate 06 `Execution mode`
Required package set        = Gate 06 `Required packages`
Verification authority      = Gate 07
Package dependency          = each assigned Pxx `Depends on`
```

P00は存在してもoptional authoring / audit artifactであり、preflight / Candidate Assembly / Orchestratorのruntime authorityにはしない。
<!-- END MANAGED: V005_LOCAL_AUTHORITY -->


## 12. G02-G10 implementation draft review register (2026-11-17)

**状態:** PREP-03 review DRAFT。G01〜G10はいずれもCODING_NOT_AUTHORIZED。G02〜G10の06/P00/Pxxと07は作成済みだが未Freeze、未承認、試験未実施。各Gateの依存/Required PackagesはOwner未承認の提案で、現行Pxxの実装着手を許可しない。正本`docs/wiki/requirement_definition/`への昇格は行わない。

**受入Authority:** Gate 06=Implementation WHAT、Gate 07=Independent Verification WHAT、P00=計画、各Pxx=実装Execution Unit、40 Operator=テスト実配置/発見/Command、999=正式独立判定。後続Gateの06/07とPxxは同じGate IDを使用する。

| Gate | Functional boundary | Method count | Gate 06 | Gate 07 | P00 | Previous 06 package proposal | Current Pxx count |
|---|---|---:|---|---|---|---:|---:|
| G02 | Identification / DoWhy / FD-A | 6 | [06](G02/06_Ariadne_ENH-E11_G02_implementation_instruction.md) | [07](G02/07_Ariadne_ENH-E11_G02_test_instruction.md) | [P00](G02/06_G02_P00_work_package_plan.md) | 4 | 4 |
| G03 | Native Effects / Refutation / Sensitivity | 13 | [06](G03/06_Ariadne_ENH-E11_G03_implementation_instruction.md) | [07](G03/07_Ariadne_ENH-E11_G03_test_instruction.md) | [P00](G03/06_G03_P00_work_package_plan.md) | 5 | 6 |
| G04 | CATE / EconML / DRIV | 8 | [06](G04/06_Ariadne_ENH-E11_G04_implementation_instruction.md) | [07](G04/07_Ariadne_ENH-E11_G04_test_instruction.md) | [P00](G04/06_G04_P00_work_package_plan.md) | 5 | 4 |
| G05 | HTE Diagnostics / Privacy / authorized row | 0 | [06](G05/06_Ariadne_ENH-E11_G05_implementation_instruction.md) | [07](G05/07_Ariadne_ENH-E11_G05_test_instruction.md) | [P00](G05/06_G05_P00_work_package_plan.md) | 4 | 4 |
| G06 | Temporal Discovery / PCMCI | 3 | [06](G06/06_Ariadne_ENH-E11_G06_implementation_instruction.md) | [07](G06/07_Ariadne_ENH-E11_G06_test_instruction.md) | [P00](G06/06_G06_P00_work_package_plan.md) | 4 | 3 |
| G07 | DiD / Event Study / ITS | 3 | [06](G07/06_Ariadne_ENH-E11_G07_implementation_instruction.md) | [07](G07/07_Ariadne_ENH-E11_G07_test_instruction.md) | [P00](G07/06_G07_P00_work_package_plan.md) | 4 | 3 |
| G08 | RDD / IV / AR | 5 | [06](G08/06_Ariadne_ENH-E11_G08_implementation_instruction.md) | [07](G08/07_Ariadne_ENH-E11_G08_test_instruction.md) | [P00](G08/06_G08_P00_work_package_plan.md) | 5 | 4 |
| G09 | SCM / SDID | 2 | [06](G09/06_Ariadne_ENH-E11_G09_implementation_instruction.md) | [07](G09/07_Ariadne_ENH-E11_G09_test_instruction.md) | [P00](G09/06_G09_P00_work_package_plan.md) | 4 | 3 |
| G10 | Full Replay / Science / Compatibility | All 41 | [06](G10/06_Ariadne_ENH-E11_G10_implementation_instruction.md) | [07](G10/07_Ariadne_ENH-E11_G10_test_instruction.md) | [P00](G10/06_G10_P00_work_package_plan.md) | 4 | 5 |

### 12.1. Review重点（先行06との差分）

- **旧提案の保存/差分Authority:** G02〜G10の先行06/P00/07案は[Git commit `9ec6e198`](https://github.com/kousuke-ota-datascience/causal-atelier/commit/9ec6e198d3d621a27fe8210adf8bf5808ed434f2)、今回の54件Gate06/P00/Pxx具体化は[Git commit `4bf03058`](https://github.com/kousuke-ota-datascience/causal-atelier/commit/4bf03058382203e94059624111958017660ae950)。06とP00は両案の差分をOwner Review対象とし、新Package数を自動承認済みと扱わない。
- **Work Package数の変更:** G03=5→6、G04=5→4、G06=4→3、G07=4→3、G08=5→4、G09=4→3、G10=4→5。G02/G05=4のまま。各案の実装Class ownership、DAG、DoD、Science受入と互換性を比較し、最終06/P00/Pxxを確定する。
- **Gate07は既存DRAFT:** 全9 Gateに07は存在するが未Freeze。Method ID・DD・positive/negative・Science条件の整合は形式的作成では完了しない。今回作成したPxx/06に追随させて独立照合する。
- **G07/G08依存修正:** 両07の依存先`G01 PASS, G02 PASS`に合わせ、今回06/P00も修正済み。先行G01の実装確定や999 PASSを意味しない。
- **未決の明示対象:** G02 P1-M05 IV target、G03 AIPW/NCE/NCO/RV実測Science、G04 EconML Inference/DRIV、G05独立Policy Authority・row Writer Class、G06 Temporal Oracle、G07 DiD/ITS Covariance、G08 AR HC1独立Reference、G09 SCM point-only/SDID、G10全41科学BenchmarkとLicense境界。

### 12.2. Review・Freeze・Coding Authorizationの順序

1. 全Gateの06/P00/Pxxと既存07のMethod/DGP/NEG/REF/AC/依存/実装Class/Source再利用をまとめて監査・Owner判断する。
2. 対象Gateの06/07/PxxにOwner判断を反映し、正本ではなくEnhancement worktree内で正式Freezeする。
3. 対象Gateのupstream canonical 999、実装Source/lock full SHA、依存環境、40 preflightを確認し、**対象Gateごとに**Coding Authorizationを明示する。
4. Authorized GateでのみCoding Agent→Candidate Assembly→Independent Test→999。文書作成や静的整合確認をScience PASSとしない。

### 12.3. PREP-03 document independency 再監査・是正台帳（2026-11-17）

**Audit scope / source baseline:** `prototype/ariadne_mvp` @ `2cf28f59a3248ee89c12ba8f541846a0b3245f82`。G02〜G10の**36 Pxxを全件確認**し、各Gateの06/P00/07（各9件）、G01 P04/README、`src/ariadne/scientific/{core_adapter,discovery,identification,inference,refutation,sensitivity}/adapter.py`、`product/ports/scientific_core.py`、`causal/inference/estimators/treatment_effect.py`、`product/application/graph_version_service.py`の現行ABIと照合した。Git treeでの文書是正はこの節を含むCommitに収録する。ここでの「確認」は静的文書レビュー／実Source署名照合であり、実行確認・Backend実測・科学Referenceの実証を含まない。

| ID | 発見事象 | 静的是正 | 未証明・Freezeへの影響 |
|---|---|---|---|
| IND-01 | 36 Pxx中、設計中ClassやTyped Portを既存Sourceと混同し得る。旧Product `run(input_,output_dir)`とE11 StagingSinkの違いが委譲先のDDに依存 | 全36 Pxxの§2AにGate/Methodごとの既存Source署名・Design-only境界・reuse/owner/bridgeの禁止事項を本文へ記載 | Concrete Bridge、effective Backend、独立Science契約は別途確定。ABI一意性のテスト未実行 |
| IND-02 | Protocol仕様内の「具体Adapter/Runtimeは30_63/30_62参照」がprimary contractの外部規範依存になっていた | 該当句を各Pxxにて本文内の所有・validated request・typed result・staging・停止規則へ置換 | 所有者/具体署名が未決のものは推測せずBLOCKED |
| IND-03 | LocalCausalUseCaseを含むPxxでOperation別Artifact契約を`23_42 §2.1`へ外部委譲 | 全36 Pxxの§2Bに6 Operationの必須/禁止Artifact、schema_dispatch、JCS request_hash、manifest/marker/readback/privacy規則を自己完結で記載。該当Class処理の規範参照を§2Bへ変更 | Method別内部Profile Schemaの詳細未承認は引き続きBLOCKED |
| IND-04 | GateごとのPxx数/依存/Method coverageの相互参照 | 06↔P00のPxx集合・依存をG02〜G10で照合。G02=4/G03=6/G04=4/G05=4/G06=3/G07=3/G08=4/G09=3/G10=5。G02〜G09の07 Method IDs、G10/07の41 ID表を再確認 | 提案DAGのOwner承認未実施 |
| IND-05 | DGP/NEG/REF/AC IDだけでは数値的oracleと閾値の仕様を保証できない | 未生成Fixture、未承認Config、K/R/MC-SE/coverage/Licenseを推測させずSTOPする既存規則を保持 | **meaningful executable standalone / Freeze PASSは未証明**。Methodごとの事前登録・独立Referenceを確定後、再監査が必要 |

**Quality classification:** 全36件は`REVISED_DRAFT`。静的な既存ABI・Operation Bundleの外部規範依存は是正したが、**「36件すべてがCoding Agentへそのまま投入できる」や「Document Independency全数PASS」は宣言しない**。未承認のMethod Schema/Backend/Inference/DGP truth/negative expected outcome/quantitative thresholdやG05のPrivacy Authority/Writerは、実装に必要な規範的空白であり、単なる文面展開で埋まらない。

| Gate | 要Owner判断・追加調停（未解消なら対象ScopeはBLOCKED） |
|---|---|
| G02 | P1-M05 IV targetとDoWhy Backend実効API、FD-A conditional estimation/variance |
| G03 | AIPW nuisance/crossfit/CI、OLS contrast/covariance、refutation/sensitivity kernel Bridge、NCE/NCO null、RV適格範囲 |
| G04 | EconML method config/fit/inference 実効API、X/W roles、DRIV独立IV slope reference |
| G05 | **独立Approval Authority：署名・鍵Owner・Scope・有効期限・失効・anti-replay・Verifier Class/Method、Parquet Row Writer Class/Factory/Method**。deny時row bytesゼロ |
| G06 | Temporal lag/time index、Tigramite実効API、PCMCI+/LPCMCI endpoint独立Oracle |
| G07 | DiD 2x2/staggeredとEvent reference/cluster covariance、ITS HAC/serial-correlation policy |
| G08 | RD bandwidth/kernel/inference、B0/B1別Target、HC1 Anderson–Rubin全実数集合・退化・独立Oracle |
| G09 | SCM point-only policy、SDID estimator/inferenceとdonor contamination/pre-fit/weights |
| G10 | 41 Method×10 UCのT2/T3 prereg K/R/MC-SE・coverage・FWER=.05・fixed candidate replay・SBOM/License・Product v2互換 |

**Owner review rule:** 個別未決は(1) Owner意思決定、(2)設計修正、(3)effective Runtime実測、(4)Independent Testでしか確証できない事項、(5)後続Gate依存に分類し、無関係Gateを一律BLOCKしない。判定後は該当06/07/Pxx内に完全な採用値・positive/negative・failure semanticsを戻し、self-containedの再監査を行う。未承認のFreeze、Coding Authorization、Source/test/uv.lock変更、独立07/999の代行は禁止。

### 12.4. PREP-03 semantic authority correction — 36 Pxx design-semantics transcription

**訂正:** §12.3の「実装に必要な意味論が未確定」という一般化は過大であった。詳細設計30_61/30_62/30_63には多数のMethod/Port/State/Algorithmの採用済み規則が既に存在している。未生成Fixtureや独立Referenceを、Method Target/数理・Port責務が未決である証拠として扱わない。

**是正:** G02〜G10の36 Pxx全件に、当該Packageに適用される詳細設計上の意味論を§4末尾・§5直前へ本文規範として展開。従来の§3 Class/Field/Constructor/Methodと§4処理順序は保持し、既存Source ABI/共通Port/Operation Bundle契約（§2A/§2B）とも併用する。設計書・Requirementのpathはprovenance/evidence用であり、Coding Agentの未記載normative semantics取得用ではない。各PxxはAssigned Class/Method以外の実装を追加しない。

| Category | 判定 | 例 |
|---|---|---|
| A: **設計書で規定済みの意味論** | Pxxへ本文転記。Ownerに無条件の再決定を求めない | Frontdoor識別とFD-A数値推定の分離、IPW/AIPWのTargetとscore、DRIV `theta_IV(x)`、DiD 2×2/staggered分離、B0/B1のEstimand、HC1/χ²(1) AR full-real inversion、SCM point-only |
| B: **設計書に本当に未指定の契約** | 該当ScopeのFreeze blocker / Owner設計判断を要する | P1-M05 DoWhy IVのTarget、G05の独立Approval Authority実装契約・鍵/失効/Verifier・row Parquet WriterのClass/Factory/Method、各Methodのstrict Config/Profileでまだ未定義なschema・optional API policy |
| C: **設計の決定とは別の未生成Evidence** | Method固有のIndependent Science／Backend verificationで取得。設計既決事項を再決定しない | 実効Library/API probe、DGP/NEG fixtures、独立Reference、K/R/Compute、MC-SE/CI coverage、実Candidate回帰/Reader/License evidence |
| D: **齟齬・衝突** | Pxxと詳細設計・実Sourceに真の矛盾を発見したときだけOwnerに設計変更提起 | 署名/Owner不一致、物理Schema矛盾、統計量の式と採用推論Profileの非整合 |

**実装可能性との区別:** 36件に意味論の規範的展開を行ったことは、未承認Method Schemaや証拠を「存在する」ものに変えない。全Pxxは`REVISED_DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED`。静的な展開の確認はScience Test PASSでもGate999 PASSでもない。Owner一括ReviewではAを再議決するのでなくB/Dのみに焦点を当て、CをIndependent Verification計画に配置する。Category Aの既決契約は採用済み値としてPxxに保持する。

**Provenance:** 30_63 §§1〜10、30_62 §8、30_61 §§6〜7、23_42 §2.1、10_32全41 Method Scope。既存Sourceの旧Product公開ABIについては当該Pxx §2Aの実Source照合を保持する。

### 12.5. PREP-03 Final Audit — static closure and Owner review

Final Audit record: [PREP03_final_audit.md](PREP03_final_audit.md) (review only, no runtime authority). G02–G10の36 Pxxに対してClass subsection header正規化、他Gateの未決を本GateのSTOPに一律適用しない修正、Publisher実署名の記載、40 READMEのCLI-only scope/文書実在状況更新を実施した。

**Final static disposition:** `STATIC_CORRECTIONS_APPLIED / OPEN_CONTRACT_DECISIONS / NOT_READY_FOR_FREEZE`。06/P00/Pxx/07のPxx依存・Method集合・G10 41 Method表は静的照合済み。科学実測や独立Reference未生成、G02 IV target/G05 independent Authority/Row Writer未決、未承認Gate DAGがあるため「全36件Coding-ready」や「全Gate PASS」を宣言しない。Owner reviewは[Audit OD-01〜OD-07](PREP03_final_audit.md)に限定して整理する。Freeze/Coding Authorization/Source/Test/999は未実施。

### 12.6. PREP-03 Owner consolidated review approval（2026-11-18 JST）
**Owner directive:** `Owner一括レビュー：承認する`（2026-11-18 07:57:48 JST）。[PREP-03 Final Audit §6](PREP03_final_audit.md)に承認範囲・非承認範囲・Control Plane判定を記録。**承認対象はFinal Static Audit、G02〜G10の依存DAG、WORK_PACKAGE実行方式、全36 Pxx構成、既決意味論の継承である。** OD-04=OWNER_APPROVED/CLOSED。G02〜G10 06/P00/07にはOwner Reviewを反映し、`DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED`を保持。

**Open Decisions remain:** OD-01（P1-M05 IV Target）、OD-02（G05 independent Row Approval Authority/Verifier）、OD-03（G05 Row Writer Class/Factory/Method）、OD-05の真のMethod Config/Inference Profile gaps。独立Science/Backend/License evidence（OD-06/07）は実行／Legal段階で取得する。**レビュー承認は未決の値を補完せず、Freeze、Coding Authorization、Source/Test変更、999 PASSを許可しない。** 正本への昇格も未実施。

### 12.7. OD-01〜03/05 design candidate preparation（2026-11-18 JST）

Owner一括レビューで**承認されていない**具体設計の採用候補を、Final Audit [§7](PREP03_final_audit.md)および以下のFLOW判断候補に分離して記録。

- [OD-01: IV Target選択候補](../00_enhance_background/Revised_requirements_definition_documents/combined_review/118_20261118_prep03_od01_iv_target_decision_candidate.md) — B0-only LATE条件付き識別を推奨。Owner選択待ち。
- [OD-02/03: Row trust and writer](../00_enhance_background/Revised_requirements_definition_documents/combined_review/119_20261118_prep03_od02_od03_row_export_design_candidate.md) — Ed25519独立署名とRow Writer Concrete Class/Method。独立承認主体・鍵運用・Class最終選択はOwner待ち。
- [OD-05: Method Profile41件棚卸](../00_enhance_background/Revised_requirements_definition_documents/combined_review/120_20261118_prep03_od05_method_profile_gap_register.md) — 既決数理と未作成Config/Schema/Science Evidenceを区分。
- [Owner decision submission](../00_enhance_background/Revised_requirements_definition_documents/combined_review/121_20261118_prep03_owner_decision_submission.md) — 申請用比較表。未承認候補は正式Pxxに採用しない。

**文書欠陥是正:** G05/P02の混入G01 FCI dispatch説明を除去、G05/P03外部DDへのOperation規範委譲を§2Bへ、G05/G10 Gate06 Publisher概要署名を既存詳細設計に一致させた。引き続き `PREP03_OWNER_REVIEW_APPROVED / OD04_CLOSED / OD01_OD02_OD03_OPEN / OD05_PROFILE_OPEN / GATES_NOT_FROZEN / CODING_NOT_AUTHORIZED`。
