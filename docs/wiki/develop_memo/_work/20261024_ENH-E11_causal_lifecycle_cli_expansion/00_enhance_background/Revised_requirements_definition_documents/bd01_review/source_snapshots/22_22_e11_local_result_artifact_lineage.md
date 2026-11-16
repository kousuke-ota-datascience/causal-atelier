# 22_22 — ENH-E11 Local Result / Artifact / Manifest / Publication

**State:** `BD01_REVISED_DESIGN / OWNER_ARCHITECTURE_POLICY_ACCEPTED / INDEPENDENT_REVIEW_PENDING / IF_DD_SCHEMA_UNFROZEN / NOT_IMPLEMENTED`  
**Date:** 2026-11-16. **Authority:** [DEC-SR04-09](../../../working_notes/20261116_sr04_dec09_scope_requirements_architecture_gate_integrated_owner_approval.md), [formal RD-03 trace](../96_rd03_formal_requirement_traceability.md), [RD-04 audit](../98_rd04_consistency_verification.md). 本文のPort名・層は論理的な責務名称であり実装済Class/Schemaを意味しない。

## 1. 独立する2種の正本

| Aspect | Existing Product (unchanged) | ENH-E11 Local (added) |
|---|---|---|
| Identity | Project/Execution/StageExecution/Result/ArtifactのDB正本 | content-addressed local Question/Design/Graph/Dataset/Run/Result参照（論理仕様） |
| Persistent location | Product Metadata DB＋ArtifactStore | Local JSON/Parquet/Manifest (Filesystem-based) |
| Authority | Product Domain/Application/Worker | Local Scientific Domain/Application＋Artifact Publisher |
| Scientific status | Product schemaと既存Review/Override | E11 typed outcome（point/inference/science独立） |
| Lineage | Product FK/LineageEdge/projection | Manifestでlocal refs/hashes/effective environmentを辿る |
| Cross-lane migration | 旧readerは旧仕様を読む | E11へ旧v2 Manifestを暗黙変換しない。双方向自動同期しない |

Domainは現行Productの`ArtifactStorePort`と設計概念を再利用できるが、Local ArtifactをProduct `Artifact`行に自動登録してはならない。Portの共有可否は既存Repoの実装調査によりDDで決める。

## 2. Local Result semantics（wire field名は未確定）

- **Identity and provenance:** Study identity、Question/Design/Estimand、Data snapshot、GraphVersion、Identification/Estimator specification、parent run、Method、effective backend/API、runtime。
- **Typed effect:** point estimate availability/value、target population/contrast、diagnostics、Identification result、scientific status／review reasons。
- **Typed inference:** `not requested`／`supported and valid`／`unsupported`／`calculation failed`／`scientifically ineligible`を区別。区間の存在と科学的受入は同義でない。
- **AR confidence set:** disjoint component intervals、非有界端点、全実数、confidence level、assumption・method/Referenceを損失なくserializeする。JSONにInfinityを裸数値として書くか否かなどのwire仕様はIF-01へ委譲する。
- **Data minimization:** aggregate summaryとrow-level CATE/individual local explanationを別Artifact classificationとし、制御応答・Manifestに個票を暗黙埋込しない。

## 3. Publish flow / commit boundary

1. CLI/Applicationが入力・上流hash・実効Environmentを検証し、局所出力候補をPlanする。
2. Publisherが指定Root配下の安全な`relative artifact keys`へstagingし、出力内容のchecksumを計算する。Traversal／symlink／外部Pathを拒否する。
3. JSON/Parquet/Manifestの型とSource SHA、Effective Method/Environment/seed/split、Scientific Status、Artifact refs、サイズ/checksumを照合する。
4. Staged contentをreadbackし、byte identity・hash・link整合性を確認。**失敗なら正常Run Manifestを公開しない**。
5. Success/科学的negativeが適切な状態で揃った場合のみ、publish上のcommit marker／complete manifestを外部から認識可能にする。部分書込を完全成功と見せない。
6. 再試行は同一入力identityと実効seed/Backend条件で比較し、既存正本の内容差異は競合として扱う。変更があれば新Run/versionへ明示移行する。

**Atomicity caveat:** 複数ファイルの移動が単一OS操作で原子的になる保証はない。実装では同一Filesystemのrename/transaction-like marker等の方式とcrash-recovery/readbackをIF/DDでFreezeし、原子的publishの意味（可視状態の判定単位）をテストする。技術失敗後のstaging残骸を正本と認識させない。

## 4. Manifestの最低限の意味

| Group | Information required |
|---|---|
| Source identity | input dataset hashes、Question/Design/Graph refs、Method/Estimand、Config/Schema Version、Git/source SHA |
| Effective environment | Python patch、OS/arch/CPU、Backend/distribution API/version、lock/pyproject hash、Native ABI/BLAS/thread info、selected Extras/Profile |
| Reproducibility | effective parameter、seed derivation/role、split/fold、upstream-run refs、analysis mode |
| Result validity | identification/eligibility status、point/CI availability、Science status、negative reasons、limiting assumptions |
| Artifacts | relative keys、media type、size、output checksum、readback/complete status、privacy classification |

Manifestは科学的根拠と実行条件の来歴であり、実行結果のbitwise再現や科学的有効性を保証した宣言ではない。SBOM／License provenanceは法務Gateへ独立Traceする。

## 5. Trace & acceptance

ARC09-04/05/06、E11-A-04/05/06；FR-185/201/202、NFR-029/030/031/033、AR-035/040/042/043。負例はpartial output、Manifestだけ先行公開、hash mismatch、PAG loss、disconnected CI flatten、個票漏洩、旧v2自動upgrade。具体Result schema・marker/commit APIはIF-01、障害回復方法はDD-01でFreezeする。
