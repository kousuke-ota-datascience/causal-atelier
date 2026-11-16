# DD-01 — E11 Local Physical Design 改訂・内部レビュー

**Document class:** FLOW / REVIEW（正本候補30系に直接格納しない）  
**Date:** 2026-11-16  
**Review state (Owner 2026-11-16):** `DD01_DESIGN_ADOPTED / STATIC_SELF_REVIEW_COMPLETE / NOT_IMPLEMENTED / CLASS_SOURCE_AND_SIGNATURE_FREEZE_PENDING`。

## 1. 範囲

| 詳細設計 | Class/Algorithm Responsibility | Interface/Trace |
|---|---|---|
| [30_61](../30_detailed_design/30_61_e11_local_domain_ports.md) | ContentRef、LocalStudySpec、GraphEvidence、IdentificationOutcome、EstimatorRequest、ARConfidenceSet、EffectOutcome、Local scientific Protocol | IF-01 §§2〜6 / FR-185/186/187/202 |
| [30_62](../30_detailed_design/30_62_e11_local_execution_publication.md) | E11LocalCausalUseCase、MethodCapabilityRegistry、ArtifactPublisher、ManifestReader、Privacy Policy、CLI entry | IF-01 §§2,5,7,8 / FR-195/201/203 |
| [30_63](../30_detailed_design/30_63_e11_method_adapters.md) | 41 Method ID、Backend family、estimand、inference、method-specific negative/validation、G01〜G10 | 10_32, SR04-F/DEC09 / FR-188〜200 |
| [Legacy Source](../30_detailed_design/30_60_cli_adapters.md) | `CliManifest` v2 source、既存Product PortとCLI、legacy behavior | NFR-014, D04 R2 |

E11 LocalはProduct/DB/WorkerのAuthorityとは別系統。現在のInterface Class/Port名は設計候補であり、実際にコード上に存在するとの主張ではない。

## 2. 41 MethodとGate mapping

全41 Method ID（P1 20 / P2 8 / P3 13）を30_63で一意に割当。DGP/NEG/REF/ACとの関係は10_32の登録を参照する。Methodのコード／科学的結果、Inferenceの実効API、Independent Referenceをこの静的設計レビューでPASS扱いしない。

| G | DD implementation responsibility | Independent evidence required |
|---|---|---|
| G01 | FCI/PAG Graph・Local Question/Design/Version | Graph oracle / unknown orientation negative |
| G02 | Identification/FD-A/Eligibility | Frontdoor/DoWhy API, true numerics and negative |
| G03 | IPW/AIPW/refutation/observed NCE/NCO/OLS RV | Propensity/balance/Refutation/negative null |
| G04 | CATE7 + separate DRIV-A | Estimand/Backend config, inference registry |
| G05 | CATE individual privacy/CI and support | row-level permission, pointwise coverage |
| G06 | PCMCI/PCMCI+/LPCMCI | time lag/edge endpoint/CI-test oracle |
| G07 | DiD/Event/ITS | identification/cluster/HAC/pretrend |
| G08 | Sharp/Fuzzy RD, Wald/B0/B1 and AR | weak IV, density, AR set topology/coverage |
| G09 | SCM/SDID | donor/fit, initial SCM point-only |
| G10 | Local Manifest/lock/atomic/old v2 | 5 profiles, fault injection, regression/SBOM |

## 3. Source-specific review

| Existing code | Confirmed behavior | New detail required |
|---|---|---|
| `interfaces/cli/scientific_stage.py` | Existing Domain/Port direct invocation + independent manifest text write | New E11 Use Case cannot claim atomicity from it |
| `interfaces/cli/estimation.py` | Existing v2 upstream manifest and status gates | R2 legacy path untouched, new fail-closed tests |
| `interfaces/cli/manifest.py` | frozen `CliManifest` with mutable nested containers, version 2.0 | New E11 typed immutable/safe codec |
| `product/ports/scientific_core.py` | Product typed ResultType/ScientificStatus | New Point/Inference/AR bridge needs independent Port |
| `product/ports/artifact_store.py` | Store/retrieve/exists/delete | Local multi-file atomic publisher & readback separate |
| `pyproject.toml` | Base + predictive-advanced extra; E11 absent | E11 functional extras/lock and profile-only test |

## 4. Detailed design findings

| ID | Severity | Finding | Owner/Independent review acceptance |
|---|---|---|---|
| DD01-F01 | BLOCKING | Proposed Module pathと既存Package/Portの重複/依存directionをまだfull source treeで検証していない | Actual module namespaceとreuse mapをOwner/Architecture確認 |
| DD01-F02 | BLOCKING | Interface候補の型・Port Return/Exception/fieldのPython signaturesはまだ実装されていない | Typed DTO/JSON schema code/contract testsの一致 |
| DD01-F03 | BLOCKING | Atomic no-clobber rename、secure dirfd、fsync、Crash recoveryは実環境未検証 | FS/OS-specific security and fault injection |
| DD01-F04 | BLOCKING | Method-scoped inference selection/AR inversionは数学・数値・推論の実装仕様が完全に確定していない | Reference/Method-specific config、weak-IV AR numerical cases |
| DD01-F05 | BLOCKING | 41 MethodのBackend exact import/API、Profile/uv.lock pin/optional isolation未実装 | All 5 env profiles + ENV-RD conditional |
| DD01-F06 | BLOCKING | Individual CATE row-level permission/exportのOS delegation policy未freeze | Threat model、sensitive output negative tests |
| DD01-F07 | BLOCKING | SR04-FのNumerical AC/CI Coverage/R/MC cost/Actual KをT2 pilot・Owner Freezeしていない | Gate07 pre-registration/independent Reference |
| DD01-F08 | BLOCKING | 30系既存Product各Class完全網羅レビュー（既存30_01等のsource audit）は別種の未完作業 | E11影響クラスと既存回帰の範囲を凍結 |
| DD01-F09 | DELIVERY | Customer-specific GPL/License/receiver assessment not approved | Legal Gate / distributed bundle SBOM |
| DD01-F10 | GATE | Independent Architecture/Schema/Science/Gate06/07/Coding未承認 | Owner Snapshot + independent review evidence |

## 5. Class review template conformance

Ownerが採用した[Class物理詳細テンプレート](../30_detailed_design/30_01_class_design_template.md)の7区分（責務、Field、Constructor、Methods、Flow、I/O/Error、Test）を30_61/62の各主要Class群へ適用する。ただしModule-levelの完全なSymbol/Line証拠、各methodの具体的Python signature、数値反転実装はコード／Freeze時に確定する。これを物理設計の完全実証と誤認しない。

## 6. 重要な非同一性

- Physical Design Draft ≠ Existing implemented classes
- Fully enumerated Method registry ≠ Validated Method Backend
- Estimated asymptotic covariance ≠ Weak-IV-robust confidence set
- Signed Request/Manifest hash ≠ Authorized row export
- Owner policy accepted ≠ Approved resource/law/independent Science
- Gate acceptance pending ≠ Coding authorization

**DD-01 status:** `DESIGN_ADOPTED / EXACT_PHYSICAL_FREEZE_PENDING`。本DDはOwner採用された設計基線だが、独立Architecture/Science、Code変更や品質Gate PASS、Coding許可を宣言しない。[Owner承認記録](../combined_review/91_20261116_doc01_if01_dd01_owner_approval_record.md)を参照。