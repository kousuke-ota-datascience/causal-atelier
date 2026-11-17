# ENH-E11 G01 P03 — PAG Endpoint, GraphVersion, Non-effect Bundle

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P03
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: P01
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
Graphの不確定性と版・同一性を損失なく保持する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope
`GraphEvidence.from_canonical_json/canonical_payload/make_revision`でTAIL/ARROW/CIRCLE/bidirected、source/targetとmark順序、unique nodes/edges、FCI PAG lag=null、version parent/rationale/assumptions、旧Graph不変を検証。内部content_hashは自己fieldを除くJCS意味射影、外側ContentRefはFile実bytes。`DISCOVER`は効果EstimandではないGRAPH_STRUCTURE targetを表し、Effect dummyを作らずManifest `schema_dispatch.result=null`とする。

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。Depends on P01の実装checkpoint full SHAとfocused検証を確認。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
`GraphEvidence.from_canonical_json/canonical_payload/make_revision`でTAIL/ARROW/CIRCLE/bidirected、source/targetとmark順序、unique nodes/edges、FCI PAG lag=null、version parent/rationale/assumptions、旧Graph不変を検証。内部content_hashは自己fieldを除くJCS意味射影、外側ContentRefはFile実bytes。`DISCOVER`は効果EstimandではないGRAPH_STRUCTURE targetを表し、Effect dummyを作らずManifest `schema_dispatch.result=null`とする。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| G01-07-03/04/07；GRAPH01/03/04、MAN03/04 | `uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01 -q` | 全部の定義済みPAG endpoint round-tripが100%で、PAG→DAG silent conversionも旧Graph mutateも0。 |

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。G01受入境界は再審査待ちで、勝手にGate acceptanceを変更しない。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
全部の定義済みPAG endpoint round-tripが100%で、PAG→DAG silent conversionも旧Graph mutateも0。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
