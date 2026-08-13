

---

## AMEND-001: G01 Operation Availability Contract completion

### Status

- Amendment status: `APPROVED`
- Amendment type: `CONTRACT_DEFECT_CORRECTION`
- Approved / applied date: `2026-08-12`

### Trigger

G01 / P02 / Trial01 の Package Coding Agent が `BLOCKED_CONTRACT_AMBIGUITY` を報告した。

Evidence:

- GATE_ID: `G01`
- PACKAGE_ID: `P02`
- TRIAL_NO: `01`
- START_SHA: `4800fabd1ab9d44ab6e64797a51278d38fb97564`
- Detection / evidence commit: `e5035b7e9d6d954eaba9373a27b564ce070821a7`
- Evidence file: `20_implementation_reports/G01/Trial01/packages/E5-G01_01_P02__status.md`

### Detected contract defect

Operation Availability Contract について、実装時に次の事項が normative に一意でなかった。

1. canonical operation key set
2. `resource_type × operation` mapping
3. operation ごとの authorization class
4. scientific/domain prerequisite authority
5. `resource_type / resource_id / route` の必須・任意条件
6. resource 未指定時 semantics
7. unknown resource / unsupported operation semantics
8. `reason_code` taxonomy

### Upstream assessment

Operation availability 自体は既存 ENH-E5 approved requirement/design に含まれており、G01 への誤混入ではない。

したがって本 amendment は requirement / scope の追加ではなく、既存 requirement を implementation-ready な normative contract へ収束させる defect correction とする。

### Decision

次を canonical contract として固定する。

- canonical operation key set: `RUN / EDIT / EXPORT`
- resource structural support matrix を固定する。
- operation authorization class を既存 ProjectMembership authorization matrix へ接続する。
- scientific/domain prerequisite の authority は実 command と同じ Application/Domain lifecycle/policy/validator とする。
- `resource_type` と `resource_id` は pair とする。
- resource pair 未指定時は `route` を必須とし、route から resource ID を暗黙推測しない。
- unknown resource / unsupported operation の error semantics を固定する。
- operation item `reason_code` を closed taxonomy とする。
- Stage visibility と action availability を別 contract として維持する。

### Modified normative documents

Canonical design:

- `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design.md`
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design.md`

Execution / verification contract:

- `10_enhance_instruction/G01/06_G01_P02_navigation_shell_ui.md`
- `10_enhance_instruction/G01/07_Ariadne_ENH-E5_G01_test_instruction.md`

Document-state normalization is also applied across:

- `00_enhance_background/**/*.md`
- `10_enhance_instruction/**/*.md`

### Semantic impact

- ENH-E5 scope change: `NO`
- G01 semantic claim change: `NO`
- P02 responsibility change: `NO`
- Existing approved operation-availability requirement removal: `NO`
- Normative contract clarification/completion: `YES`
- Production implementation performed before blocker: `NO` based on Trial01 blocker evidence

### Evidence handling

`E5-G01_01_P02__status.md` の `BLOCKED_CONTRACT_AMBIGUITY` は削除・上書きしない。

当該 Trial01 は contract defect を検出した有効な historical evidence として保持する。Amendment 適用後の package execution result は別の実行証跡として記録する。

### Git traceability

- Defect detection commit: `e5035b7e9d6d954eaba9373a27b564ce070821a7`
- Amendment application commit: 本ファイルを導入・変更した Git commit history を authority とする。

自己参照 commit SHA を同一 commit 内へ埋め込むことは行わない。明示的な SHA 台帳が必要な場合は、amendment application commit 後の独立 traceability commit で追記する。

---

## AMEND-001 Traceability Classification Addendum

This addendum records the per-document trace classification introduced after the initial AMEND-001 remediation package. It does not rewrite the original AMEND-001 decision record.

### Normative semantic changes

The following documents contain normative contract clarification/completion under AMEND-001:

- `00_enhance_background/Revised_requirements_definition_documents/23_api_interface_design.md`
- `00_enhance_background/Revised_requirements_definition_documents/30_detailed_design.md`
- `10_enhance_instruction/G01/06_G01_P02_navigation_shell_ui.md`
- `10_enhance_instruction/G01/07_Ariadne_ENH-E5_G01_test_instruction.md`

Classification:

- Amendment role: `CONTRACT_DEFECT_CORRECTION`
- Normative semantic change: `YES`
- ENH-E5 scope change: `NO`
- G01 semantic claim change: `NO`

### Metadata-only instruction changes

The following instruction documents receive an AMEND-001 local trace for document-state normalization / traceability convergence. Their normative requirements, behavior, acceptance criteria, and implementation responsibilities are unchanged:

- `(none)`

Classification:

- Amendment role: `DOCUMENT_METADATA_NORMALIZATION`
- Normative semantic change: `NO`

### Immutable evidence

The following blocker evidence remains unmodified and is referenced, not rewritten:

- `20_implementation_reports/G01/Trial01/packages/E5-G01_01_P02__status.md`

Classification:

- Amendment role: `IMMUTABLE_EVIDENCE`
- Historical result: `BLOCKED_CONTRACT_AMBIGUITY`
- Mutation by this amendment: `NO`
