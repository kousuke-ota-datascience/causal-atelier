# G01 — Provisional S10 Contract Freeze: Owner approval record

**Owner decision:** `G01-S10-PROVISIONAL / APPROVED`.
**Date of approval:** 2026-11-23 JST.
**Human authorization source:** Owner's explicit reply 「採用する。進めよ」 to the immediately preceding request: **「G01の暫定S10契約固定を承認するか」**. The approval is for the provisional G01-S10 only. It is **not** an approval of S11, S09, Gate999, a scientific algorithm, an installed Backend, or production usage.
**Authority:** Previously adopted `DEC-G01-EXEC-01`, recorded in `177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`; Owner review details in `178_20261123_g01_provisional_s10_limited_s11_owner_approval_docket.md`. Other Gates retain `DEC-PREPCODE-01=B`.

## 1. Immutable frozen source identity

- **Gate and scope:** `GATE_ID=G01`, Local scientific CLI `DISCOVER` / `P1-M06` FCI, five bounded Coding Work Packages `P01,P02,P03,P04,P05`; `P00` planning only.
- **Frozen full Git commit SHA:** `a05fd072cbb82a7c6e43f45e7208e078f0784a2b` (branch `prototype/ariadne_mvp` at selection, but the immutable commit, not the moving branch, is normative).
- **Frozen `uv.lock` Git blob SHA:** `2b83110e86b26b7969fbddf8f98a727370ae19f7` as fetched from the frozen commit. This is a Git blob object SHA, **not** SHA-256 of exact lockfile bytes. Obtain and record `sha256sum uv.lock` in the future authorized runtime; the current chat has not observed a Linux VM or packages.
- **Frozen source manifest:** `combined_review/s09_post_reconciliation_document_snapshot_draft14.json` (402 unique normative paths); **G01 candidate classification** `combined_review/s09_g01_scoped_review_inventory_draft8.json` (11 OWN_GATE, 69 COMMON_SHARED, 5 IMPACT_SAMPLE, 317 DEFERRED_OTHER_GATE). Historical reviewed `source_full_commit_sha=2eaaf9432b36c85a5edfef9f5f1568ef845da003` in the inventory is the last normative-file modification commit before index creation; the **Owner-frozen source commit is the later full commit `a05fd072...`**, which includes that inventory. Do not confuse these identities.
- **Current-branch drift inspection at S10:** the six commits between `a05fd072...` and the status-check HEAD `32e8f68bd74c4650c15ffc05e2eb969dc973a131` modified *only* the author review/readiness/docket artifacts `159`, `165`, `174`, `178`, and `s05_current_blockers_draft4.json`, not the 402 normative sources or `uv.lock`. Source/index full path/blob parity was checked 402/402 at draft14/draft8 creation, **author source-integrity check only**, not independent S09 PASS.

## 2. G01 contract that Owner provisionally freezes

- `10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md`; `06_G01_P00_work_package_plan.md`; `06_G01_P01_local_contract_codec.md`, `06_G01_P02_atomic_publication_reader.md`, `06_G01_P03_pag_graph_version.md`, `06_G01_P04_fci_backend_oracle.md`, `06_G01_P05_cli_use_case_privacy.md`; and `07_Ariadne_ENH-E11_G01_test_instruction.md`, all **from the frozen full commit**.
- The common E11 v1 Local Study/ContentRef, graph endpoint and JCS hash identity, Status/Manifest/Marker/optional output rules, named `causal-learn` FCI `fisherz/chisq/gsq` and 3 active P1-M06 profiles, Linux private same-UID atomic staging/publication/Reader, correct typed errors, G01 mandatory row-export denial and no fake Effect, Product v2 `causal-analysis-spec/2` protection and independent `07/999` criteria remain intact.
- Work Order `P01 → (P02,P03) → P04 → P05` with P00 not a Coding Package. No G02+ scientific Method implementation and no implicit downstream Gate999 acceptance.
- Known tagged `causal-learn 0.1.4.8` non-null BackgroundKnowledge bug: **all non-null BK including empty BK structurally recognized but typed `BACKEND_SEMANTICS_UNVERIFIED` exit4 refused before FCI call** until independently accepted correction and stdout containment. The **eventual positive BK science obligation remains mandatory**.
- Frozen docs may contain a contemporaneous “S10/S11 NOT_FROZEN/NOT_AUTHORIZED” header: this expresses status **as of the frozen draft**, now superseded for S10 **only** by this separate Owner record. **Do not rewrite frozen WHAT merely to update a status label.**

## 3. Explicit outstanding evidence / non-waiver ledger

| Obligation | Status at provisional S10 | Mandatory decision boundary |
| --- | --- | --- |
| Independent G01/common scoped **S09** | `EXTERNAL_PENDING / NOT_RUN` | Before G01_999 |
| Python3.12 real **B02** nine active G01 schemas and strict positives/negatives | `EXTERNAL_PENDING / NOT_RUN` | Before G01_999 |
| Real **B03** cross-artifact Reader/FS and private atomic publication | `NOT_IMPLEMENTED / NOT_RUN` | Before G01_999 |
| Python3.12 real `ENV-BASE` **B04** `fisherz/chisq/gsq` fitted Backend/API/console | `EXTERNAL_PENDING / NOT_RUN` | Before G01_999 |
| Independent MAG/PAG/latent/BK **B05**, validated science protocols, T2→preregistered T3 | `EXTERNAL_PENDING / NOT_ACCEPTED` | Before G01_999 |
| Independent **07** Test Agent, actual candidate SHA, privacy/OS/legacy-v2 regression, **999** | `NOT_RUN` | Before G01_999 |

None of these is a provisional-S10 denial criterion *solely because no external session is accessible* under Owner `DEC-G01-EXEC-01`. None is waived or deemed successful; an unsupported/uncertain result is `BLOCKED` at the required Gate acceptance boundary. A scientific or API discrepancy that materially changes the frozen WHAT must follow formal contract defect/change impact and Owner reapproval, **not** a silent code-side assumption.

## 4. Authorization and next required Owner decision

- **Provisional G01-S10: `APPROVED`.**
- **Limited G01-S11 Coding Authorization: `NOT_AUTHORIZED / OWNER_SEPARATE_DECISION_REQUIRED`.**
- `src/`, `tests/`, `pyproject.toml`, `uv.lock` and execution of Coding/Independent Test Agents are **not authorized by this S10 record alone**.
- Next Owner decision: whether to issue the **separate G01-S11 limited coding authorization** for only `G01/P01..P05` from `a05fd072...`, using frozen G01 06/Pxx/07 and `uv.lock` Git blob above, and enforcing all non-waived obligations before `G01_999`. Other Gate S11 permissions are not implied.
