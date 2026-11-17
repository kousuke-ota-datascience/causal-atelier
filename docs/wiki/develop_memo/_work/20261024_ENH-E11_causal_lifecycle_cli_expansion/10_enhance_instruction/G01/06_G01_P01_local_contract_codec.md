# ENH-E11 G01 P01 — Local Study, ContentRef, Canonical Codec

**Document class:** Primary Execution Contract  
**Self-containment:** MUST — Assigned Coding Agentが本書だけでpackageのnormative execution responsibilityを理解できること。

- Gate: G01
- Trial: Trial01（未開始）
- Package: P01
- Parent 06 (traceability): 06_Ariadne_ENH-E11_G01_implementation_instruction.md
- P00 Plan (traceability): 06_G01_P00_work_package_plan.md
- Depends on: NONE
- Status at issuance: DRAFT / CODING_NOT_AUTHORIZED

## 1. Purpose
strict Study/ContentRef、Question/Design/Method Profile、Canonical JCSとManifest Valueを定義する。

## 2. Effective Gate constraints applicable to this package

このpackageが守るべきGate-level semanticsを、Parent 06 / P00を読まなくても実行判断できる粒度で記載する。

G01は正式Gate IDでPxxはbounded Coding Unit。Local laneとProduct v2を分離し旧CLI/Web/API/DB/Workerは改変しない。strict version/Method/EstimatorとJCSのハッシュ対象を検証し、PAGをDAG/ATEへ変換しない。OS root/Privacy/Atomic Publishの不適格はfail-closed、SCI不確実性をPASSに変換しない。Coding Authorization前の実装は禁止。

## 3. In scope
`ContentRef.from_payload`の5字段(identity/relative_key/sha256/media_type/schema_version)とsafe relative keys、`LocalConfigDecoder.decode(raw, declared_format)`でduplicate YAML/JSON keys・unknown/versionless/legacy v2拒否。Question/Design/Study identity、Data列名・順序、FCI CI測定尺度と背景知識一致を照合。`GraphEvidence.from_canonical_json`と`LocalRunManifest.to_canonical_bytes`はstrict RFC8785 JCSを使い、request-hash/Graph semantic hash/File実bytes hashを区別。

## 4. Explicitly out of scope
他GateのMethod実装、旧Product v2変更、根拠なしのScience PASS、行出力自己許可、未承認ACL/mount、既存run上書き、Package外の便乗変更。

## 5. Entry criteria / required evidence
Gate 06/07のFreeze・Coding Authorization・固定branch HEAD確認。P01に先行する実装Packageは存在しないので依存Checkpointは不要。矛盾/依存未成立はBLOCKED。

dependency checkpoint / source state等はfactとして外部参照してよい。Entry rule自体は本書内に記載する。

## 6. Required implementation
`ContentRef.from_payload`の5字段(identity/relative_key/sha256/media_type/schema_version)とsafe relative keys、`LocalConfigDecoder.decode(raw, declared_format)`でduplicate YAML/JSON keys・unknown/versionless/legacy v2拒否。Question/Design/Study identity、Data列名・順序、FCI CI測定尺度と背景知識一致を照合。`GraphEvidence.from_canonical_json`と`LocalRunManifest.to_canonical_bytes`はstrict RFC8785 JCSを使い、request-hash/Graph semantic hash/File実bytes hashを区別。

## 7. Focused verification

| Check | Command / method | Required result |
|---|---|---|
| G01-07-01/02(lexical)/04；REF01〜04、SPEC01〜04、MAN01/02 | `uv run --no-sync python -m pytest tests/enhancement/enh_e11/g01 -q` | Valid/invalid schemaとJCS independent vectorsについてlossless・strictを実証し、旧v2 E11誤認ゼロ。 |

## 8. Protected contract / Transition Debt constraints
Product v2の既存CLI/Manifest/Result contractを回帰保護する。未完成のGraph/Science/個票認可を完成と見なさない。PREPARATION-03の技術判定はG01単一Gate維持（Owner承認待ち）。P02のOS/FS Publication、P04の独立FCI/PAG Science、P05のCLI統合・Privacy/旧v2回帰は別々の必須受入軸であり、全軸が同じFixed Candidate SHAで実証されるまでG01_999 PASS不可。OwnerのGate境界承認・06/07 Freeze/Coding AuthorizationまではPxx着手禁止。

## 9. Checkpoint / reporting rule

Package completion時:

1. implementation-affecting changeをcommitする。
2. implementation checkpoint full SHAを固定する。
3. `implementation_checkpoint_report`を作成する。
4. `*_in_progress.md`へexecution statusを記録する。
5. report-only commitが別ならcheckpoint SHAと区別する。

## 10. Package completion criteria
Valid/invalid schemaとJCS independent vectorsについてlossless・strictを実証し、旧v2 E11誤認ゼロ。 集中検証の証跡・実装checkpoint SHA・Package Reportを揃える。未検証はBLOCKEDで止める。

## 11. External reference policy

source / previous checkpoint / test output / provenanceは外部参照してよい。本書のimplementation rule、prohibited scope、completion criterionをParent 06 / P00へ委譲してはならない。

## 12. Stop rule

- package scope完了 -> `PACKAGE_COMPLETE`
- continuation不能 -> `PACKAGE_BLOCKED`
- Gate PASS / FAILは判定しない。
- next packageへ勝手に先行しない。
