# ENH-E11 — SR03-D01 IV異質効果の独立Estimand family採用：科学的判断記録

**文書区分:** `working_notes`／SR03-D01の独立した技術判断・比較根拠。正式なFR/NFR/AR、Architecture Review、Gate 06/07の承認文書ではない。  
**判断日:** 2026-11-01（JST）  
**判断状態:** `SR03-D01_A_OWNER_ACCEPTED / METHOD_SPECIFIC_CONTRACT_PENDING / SCIENTIFIC_ACCEPTANCE_NOT_RUN`  
**判断主体:** Human owner（本検討で明示されたA案採用）  
**調査・記録の参照Baseline:** `prototype/ariadne_mvp`、`019212bca83ec02b68d849eb32dd37e3a86a9922`。本記録はその後のD01方針決定を文書化したもので、現行実装の科学的受入Baselineをfreezeしたものではない。  
**関連:** `00_04` P2-09、P3-12、SR-03、SR-04／SR-07、Issue #16/#18/#22/#24。

## 0. 文書の責務・承認との関係

本ファイル（以下「ファイルD01」）は、**SR03-D01の科学的意味、A/B/C選択肢の比較・非採用理由、採用する不変条件、未決のMethod別契約、科学的検証への引渡し**を管理する唯一の詳細記録とする。

- **正式なオーナー判断の記録先:** [02_enhancement_concept_approval_record.md](../00_enhance_background/02_enhancement_concept_approval_record.md)。本ファイルは技術根拠を保持するが、02の承認権限を代行しない。02の全体状態 `PENDING_FULL_CONCEPT_APPROVAL` は維持する。
- **SR-03全体の横断契約・進捗:** [SR-03総合メモ](20261101_sr03_identification_estimand_estimator_contract_review.md)。Estimand互換行列・状態機械・他Decisionとの関係はここに残す。**D01固有の選択肢比較・科学的意味の根拠・非採用理由の更新責務は本ファイルに移譲する。**総合メモのD01行は参照・要約のみとする。
- **スコープ・要件・設計への反映先:** [00_04](../00_enhance_background/00_04_phase1_to_phase3_cli_scope_proposal.md)は採否・Phase境界、[03](../00_enhance_background/03_requirements_revision.md)は要件差分、[04](../00_enhance_background/04_design_revision.md)は設計責務をそれぞれ保持する。これらに本ファイルの詳細比較を複製しない。
- **隣接する別Decision:** [LATE推定器・EconML推論の検討](20261101_sr03_late_estimator_options_econml_inference_review.md)はSR03-D02/D03およびCI probeの根拠に留め、**D01の独立familyの科学的定義・比較は本ファイルを参照する**。

将来D01判断を変更する場合は本ファイルの比較と残余判断を改訂し、02に変更のオーナー決定を追記し、影響する横断契約・03/04へ差分を反映する。異なる文書を互いに独立したD01判断の正本としない。

## 1. 判断対象と事実／未実証の区別

**判断対象:** Phase 2に残すIV+ML（現行候補：EconML DRIV）による異質効果を、ATE/ATT/CATE/LATEと別のEstimand familyとして分類するか。これは「どのライブラリが計算できるか」「どのMethodが科学的に受け入れられたか」と異なる、**推定対象の意味を保存する契約上の判断**である。

**確認済みの技術事実:** SR-02のLinux／Python 3.12／EconML 0.17.0直接probeではDRIVの連続Treatmentを用いた `fit/effect` がAPI smokeとして成功した。ただし、**CLATE・complier LATEの識別、既知真値精度、推論区間被覆、Ariadne新Adapterの実装は実証していない**。[SR-02一次実行メモ](20261101_sr02_backend_runtime_probe_results.md)。

**科学的な制約:** IV推定は、Instrument、処置応答、識別仮定、対象母集団、conditioning、処置コントラストによって推定対象が変わる。`effect()`が数値を返すこと、DoWhy/EconMLが用いる内部ラベル、外部API上のクラス名のいずれも、Estimandの同一性の証明にならない。

## 2. 比較した選択肢と判断理由

| 選択肢 | 内容 | 利点 | 科学上・契約上の問題 | D01処遇 |
|---|---|---|---|---|
| **A：独立family** | `IV_HETEROGENEOUS_EFFECT` を `ATE/ATT/CATE/LATE` と別分類し、Method固有の識別対象を別途明記 | IV前提を保持し、誤ったCATE/LATE表記を防ぎながらDRIV候補を維持 | family名だけでは対象が定義されないためMethod別の数式・識別条件・testが必要 | **採用** |
| **B：一般CATEへ包含** | `estimand=CATE` にIV strategyを付与する | 外形schemaは単純 | CATEという表示から通常の無交絡CATEを連想し、IV固有の識別対象・仮定・対象集団を見失う。識別条件の異なるMethod間の同等性を無根拠に示唆 | **非採用** |
| **C：IV異質効果を後続送り** | Phase 2からDRIV等の初期候補を外す | 初期契約は小さくなる | Phase 2の列挙IV+ML候補維持方針を縮小し、SR-01の再承認が必要。API smokeだけでは採用の科学的証拠にはならないが、未検証を理由に自動除外もしない | **非採用** |

**オーナー決定（2026-11-01）:** **Aを採用**。決定範囲はEstimand familyの分類方針まで。DRIVに対する特定の数式・推論アルゴリズム・Result schemaの正式採用とは分ける。

## 3. 科学的対象の区別

代表的な二値処置の潜在結果を `Y(1),Y(0)` とし、共変量を `X`、二値Instrumentを `Z`、実際の処置を `A` とする。

- **ATE:** `E[Y(1)-Y(0)]`。指定した対象母集団の平均処置効果。
- **CATE:** `E[Y(1)-Y(0)|X=x]`。指定した `X=x` における通常の条件付き処置効果。
- **LATE:** `E[Y(1)-Y(0)|A(1)>A(0)]`。ここで `A(z)` は二値Instrument割当 `z` 下の潜在処置。二値Z/AのIV独立性、除外制約、関連性、単調性、consistency等の条件に依存する。
- **Conditional LATE（CLATE）の一例:** `E[Y(1)-Y(0)|X=x, A(1)>A(0)]`。条件付きInstrument割当の正当化、各 `x` でのfirst stageとpositivity、exclusion・monotonicity等が追加で必要。通常CATEとは対象集団が異なる。
- **IV heterogeneous effect family:** 単一の普遍的な数式ではない。`theta_IV(x)`を具体的なMethod／研究Designに応じた条件付きモーメントまたは構造モデル・処置コントラストで**別途定義**する。

例として二値Z/Aで条件付き識別条件が成立し、条件付きfirst stageが非ゼロなら、reduced-form差とfirst-stage差の比
`{E[Y|Z=1,X=x]-E[Y|Z=0,X=x]}/{E[A|Z=1,X=x]-E[A|Z=0,X=x]}`
は条件付きcomplier効果に対応し得る。しかし、この例は**EconML DRIVのあらゆる処置・Instrument構成のEstimandを規定するものではない**。一般の線形IV係数や連続Treatmentに対する条件付き効果を、この二値Z/AのLATE式へ無条件に読み替えない。

**採用する不変条件:** `IV_HETEROGENEOUS_EFFECT` は「識別方法と対象を詳細に記述しなければならないfamily」という分類であり、`CATE`・`LATE`・`CLATE`との数値的一致・統計的同等性・因果的同一性を自動的に保証するものではない。追加仮定により等価性を主張するなら、対応する識別式と適格性をMethodごとに示す。

**根拠:** [Imbens & Angrist (1994), LATE](https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects)、[EconML公式IV estimation](https://www.pywhy.org/EconML/spec/estimation_iv.html)（公式公開説明の版と実probe採用候補0.17.0は区別）。

## 4. 採用する契約上の不変条件（schema名は提案）

1. **familyとMethod-specific estimandの2層:** Domainは `estimand_family=IV_HETEROGENEOUS_EFFECT` を独立分類できること。ただし具体的な `estimand_definition`／識別モーメント・Target population・conditioning・Treatment contrast等が欠けるとき、科学的に推定可能とは認めない。これらのfield名・enum値・版番号自体は正式schemaで未承認。
2. **Questionが先:** Estimatorの選択前に分析者が対象集団、単位・時間、Treatment/Comparator、effect modifiers、Instrument、Estimandの意味を確定する。Estimator APIの出力後に対象を都合よく付け替えない。
3. **EligibilityはMethod別:** Instrumentの割当条件・relevance、exclusion、対象に応じた単調性／構造モデル、support、nuisanceモデル、cross-fittingなど、**各Estimandに必要なものだけ**を検証し、宣言された仮定と機械検証済み事実を区別する。
4. **誤変換を禁止:** DRIVで `fit/effect` が成功しただけで `ATE/CATE/LATE/CLATE` として保存しない。別対象への再分類には追加仮定と識別根拠の明示が必要。
5. **失敗時の意味:** Method固有定義・必要な識別根拠が欠ければ推定を許可せず `REQUIRES_REVIEW` 等へ引き渡す案とする。実装上のconfig error、optional dependency欠落と科学的非識別は区別する。statusの具体enum/exit codeはD04・設計04で確定する。
6. **出力の追跡性:** Question／Design／IdentificationResult／EstimatorSpec／EffectResultが同じ対象を参照し、使用したbackend version・データ／Graph hash・推論可用性を保持する。authorityとManifest schemaはD04・Architecture Reviewで決定する。

## 5. SR-03内で責務を分ける判断・実装への引渡し

| 関連判断 | D01で確定すること | D01で承認しないこと（引渡し先） |
|---|---|---|
| SR03-D03（LATE） | 独立IV familyはLATEと別の対象分類。二値Z/AのWald・2SLS採用を変更しない | 2SLS拡張の対象、弱IV頑健推論・confidence set、C案の時期（D03） |
| SR03-D04（接続・互換性） | familyのみでは推定許可せず、Method固有定義と識別根拠を要求 | 正式Domain enum、versioned schema、adapter/CLI/Manifest、旧v2互換、review authority（D04／Architecture Review） |
| SR03-D05（CATE/DRIV CI） | Backdoor型CATEとIV異質効果を同一Method契約へ潰さない | DRIVの具体的 `theta_IV(x)`・識別モーメントとtreatment/instrument構成、CIの必須水準・Bootstrap校正（D05／SR-04） |
| SR03-D06（PAG/CPDAG） | family分類はGraphの不確定性を自動解消しない | `REQUIRES_REVIEW`／部分識別からの許可境界、review override（D06／Architecture Review） |
| SR-04／Gate 07 | 必要となる既知真値・負例の検証観点を引き渡す | 数値誤差・CI coverage・seed/反復数・Method採用・独立Science PASS |

## 6. 検証計画（未実行・未freeze）

| 検証観点 | 試験条件／期待 |
|---|---|
| D01-T01：異質効果の対象差 | 既知真値で通常CATEとcomplier条件付き効果を異ならせ、誤った同一ラベルへの保存を拒否 |
| D01-T02：DRIVのMethod固有契約 | 連続T/Z構成と二値Z/A構成を分離し、対象のモーメント・contrastが明示されない場合は実行・科学的結果認定を拒否 |
| D01-T03：識別条件の不足 | independence／exclusion／relevance／support等の不足・疑義を可視化し、family名だけで `IDENTIFIED` にしない |
| D01-T04：異なるEstimandの上流流用 | Question／Design／Estimandのhash不一致を検出し、IV結果のCATE/LATEへの黙示流用を拒否 |
| D01-T05：追加仮定に基づく等価性 | 条件付きcomplier効果に対応すると主張する場合、仮定と識別式を明示し、Methodごとの既知真値fixtureで検証 |
| D01-T06：旧経路回帰 | Native ATE/ATT・Backdoorと従来CLIを維持し、IV分類追加だけで旧Resultを再解釈しない |

既存の[SR-03総合メモ §6](20261101_sr03_identification_estimand_estimator_contract_review.md) の `SR03-T07/T08/T11/T12` との重複は、**本節をD01固有の検証意図、総合メモを横断fixture一覧・Gate引渡しの参照表**として扱う。Test IDの正式採番・定量閾値・独立実行はSR-04／Gate 07で統合してから固定する。現時点で数値Benchmark PASSとは主張しない。

## 7. 未決事項・閉鎖条件

**完了した判断:** `SR03-D01` の **選択肢A（独立Estimand family）のオーナー採用**。

**未承認／未実施:** 正式なfamily enum・schema version、DRIVのMethod別estimandの厳密な数式と識別モーメント、必要な仮定・対応する処置／Instrument型、旧config互換、推論区間の採否、数値Benchmark・Science Gate、全体構想承認、コード実装。

**D01個別判断の記録完了条件:** 本ファイルが比較・制約・未決を記録し、02に個別オーナー判断、SR-03総合メモにD01参照、00_04/03/04に採用方針への参照が存在すること。これは**D01の分類判断についての記録整備**を意味し、**SR-03全体・SR-04科学検証・00_04スコープ承認の完了条件ではない**。
