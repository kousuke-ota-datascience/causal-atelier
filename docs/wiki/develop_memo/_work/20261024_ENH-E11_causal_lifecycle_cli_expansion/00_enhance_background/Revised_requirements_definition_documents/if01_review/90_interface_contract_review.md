# IF-01 — E11 Local Interface 改訂・内部レビュー・未閉鎖事項

**Document class:** FLOW / REVIEW。正本候補に入れない。  
**Date:** 2026-11-16  
**Review state (Owner 2026-11-16):** `IF01_DESIGN_ADOPTED / STATIC_SELF_REVIEW_COMPLETE / SCHEMA_AND_PORT_FREEZE_PENDING / NO_RUNTIME_TESTS`。  
**Scope:** 23_41 Local CLI/Ports、23_42 Result/Manifest/Artifact、および既存23系への影響評価。

## 1. 対象Interfaceと合意済み方針への対応

| IF element | Source | DEC09/Requirement | 維持する制約 |
|---|---|---|---|
| E11別CLIと明示Version | [23_41](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md) §§1–3 | ARC09-04、FR-185/201、NFR-029/036 | old v2 caller/reader not reinterpreted |
| Strict Content Ref / preflight | 23_41 §§3–4 | ARC09-01/03、FR-185/187 | hash mismatch/nonidentified fail-closed |
| Domain Scientific Port | 23_41 §4 | ARC09-01/02、FR-187/193/194 | no Product SCI result alias |
| Method/Backend/Inference Registry | 23_41 §§6–7 | ARC09-02/06、FR-188〜200、NFR-030 | 41 Method scope preserved |
| Typed Result / AR / Graph | [23_42](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md) §§3–5 | ARC09-05、FR-186/202、AR-040/043 | no topology/endpoint loss |
| Manifest / atomic publish | 23_42 §§1–2,6–7 | ARC09-04/06、FR-201/203、NFR-031/034 | commit marker/hash/readback |
| Local privacy / Legal | 23_42 §8 | FR-195、ARC09-06 | Product RBAC not impersonated; GPL delivery blocked |
| Explicit negative/status/exit | 23_41 §5 | FR-187/202、AR-029/034 | science status not process status |
| Contract Test | 23_41 §8 / 23_42 §9 | Gate06 design | all tests NOT RUN |

## 2. 既存Sourceとの照合

- `src/ariadne/interfaces/cli/scientific_stage.py`：現在CLIは `ScientificCoreAdapter()` を直接生成し、result後 `CliManifest(manifest_version="2.0")` を `Path.write_text`。新Port/atomic publisherは現時点の実装ではない。
- `src/ariadne/interfaces/cli/estimation.py`：現行旧v2では `REQUIRES_REVIEW` とoverrideを条件付きで認める。この既存経路はD04 R2で回帰保護対象。新E11のfail-closedと意図的に別契約。
- `src/ariadne/product/ports/scientific_core.py`：Outputは `ScientificResultDescriptor(result_type,scientific_status,summary,payload,...)`。E11のpoint/inference/Science/AR集合をlosslessly示す保証は無い。
- `src/ariadne/product/ports/artifact_store.py`：単体store等のみ。Atomic multi-file TransactionをPort単体で保証しない。
- `pyproject.toml`：E11 extrasとCLI entry未追加。 `uv.lock` はE11採用Profileの変更・再検証未実施。

以上はsourceを静的に読んだGapの確認であり、実装済みやUnit Test PASSの証明ではない。

## 3. Internal review findingsとOwner審査事項

| Finding | Severity | 現状 | Combined reviewで確定すること |
|---|---|---|---|
| IF01-F01 | BLOCKING CONTRACT | CLI名称 `ariadne-causal-local`、config/result/manifest Version文字列は設計候補 | Schema/version/CLI grammarの採用か変更 |
| IF01-F02 | BLOCKING CONTRACT | JSON result/AR/Graphの形状とenumは定義。Schema validator・code generation未作成 | Tagged infinities/topology/Graph round-tripの正式凍結 |
| IF01-F03 | BLOCKING DESIGN | Manifest+Marker+no-clobber renameを選定。FS実効能力未検証 | Linux ext4等での対象・fsync/no-replace・recovery許容 |
| IF01-F04 | BLOCKING SECURITY | Local OS principal＋privacy policy、二重opt-inを要求。委譲Principal/共有volumeの最終Policy未確定 | Threat model、UID policy、個票Export scope |
| IF01-F05 | BLOCKING SCIENCE | 41 Methodのtarget/inference/matrixは10_32に追従。P1-M05 IV target未確定などが残る | MethodConfig/Estimator/CI API and compatibility approval |
| IF01-F06 | BLOCKING ENV | 5 ProfileとENV-RD candidateを保持。E11 extras/lockとactual ABI未導入 | Extra/version pin、Combined resolution、SBOM/Legal |
| IF01-F07 | BLOCKING ACCEPTANCE | 19 IF/IO Contract Test IDを設計、全部NOT_RUN | Gate06 test fixtures、Owner Freeze、independent results |
| IF01-F08 | DELIVERY | GPL系BackendのCustomer Deliveryは法務審査までBLOCKED | 受領者別Artifact/SBOM/LicenseのLegal Owner |

## 4. 重要な非同一性

- **Interface Draft完了** ≠ JSON Schema/CLI option正式採用・実装済み・Gate06 PASS。
- Methodの欄にIDがある ≠ Backend/Methodの科学的有効性・Coverage保証。
- EXIT 0またはcompleted marker ≠ Independent Science PASS。
- Linux OSのFile Ownerだけ ≠ Product ProjectMembership権限。
- Local Manifest ≠ Product DB Result/Lineage。
- Source codeで旧v2の `REQUIRES_REVIEW` が許可されている ≠ E11でoverride許可。

## 5. 受入時のチェックリスト

1. OwnerがIF01-F01〜F06の仕様選択と例外を確定する。
2. IF Test 10件＋IO Test 9件をmethod-specific implementation GateのContract baselineへ紐付ける。
3. 41 Method/10 UC/44 formal FR-NFR-ARとの双方向Traceと新旧互換を確認。
4. Independent Reviewerがactual code／Schema／negative testsを確認し、Gate06 Snapshotを別承認する。
5. Original canonical `docs/wiki/requirement_definition/` はE11の全対象テストPASSまで変更しない。

**IF-01 status:** `DESIGN_ADOPTED / FORMAL_SCHEMA_FREEZE_PENDING`。未実装・科学・Legal・Gateは独立した未閉鎖事項。[Owner承認記録](../combined_review/91_20261116_doc01_if01_dd01_owner_approval_record.md)を参照。