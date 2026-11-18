# PREP-03 / OD-01–05 — Owner decision submission and implementation boundary

**Owner採用の結果（2026-11-19）:** 推奨OD-01=A/OD-02=A/OD-03=A/OD-05=Gate別Profile作成を採用。本文の選択肢表と「未採用」は提出時の履歴。別途残るDeployment Authority・Method Config/Runtime/Scienceの実証とFreezeは禁止事項を[122](122_20261119_dec_prep03_od01_od05_owner_adoption.md)に確定。

**Classification:** FLOW / Owner decision pack; candidate, not stock design / not Contract Freeze.  
**As-of baseline:** `68fb0b64021cc9ff372a0a7e3f13a406638da08f` (`prototype/ariadne_mvp`)  
**Existing accepted facts:** PREP03 Final Audit Owner-approved; Gate DAG, WORK_PACKAGE and 36 Pxx approved; PREP02 common design baseline F03–F07 frozen; scientific targets adopted wherever 10_32 and 30_63 already specify them.

## 1. Items available for Owner selection

| Decision | Recommended option | Decision content | Alternatives and effects | Source detail |
|---|---|---|---|---|
| **OD-01 P1-M05** | **A: B0-only conditional `LATE_COMPLIER` identification** | Explicit B0 Target/Design and typed assumptions; DoWhy provides compatible IV evidence only, not numerical effect; no silent relabel | B: B0+B1 requires extra DGP/config/evidence; C: review-only cannot claim positive identification | [118](118_20261118_prep03_od01_iv_target_decision_candidate.md) |
| **OD-02 Trust Authority** | **A: Ed25519 detached-payload signature + administrator-owned trusted registry/revocation** | Independent approving principal/role, key owner, revocation/expiry, run- and Study-bound signed policy, OS root and UID anti-substitution | B: online authorization service (new dependency); C: disable row export until a scope amendment | [119](119_20261118_prep03_od02_od03_row_export_design_candidate.md) §1 |
| **OD-03 Writer** | **A: separate `RowEffectsParquetWriter` + bounded serializer after `PrivacyDecision`** | Precise Factory/method/module; authorized bounded rows only; G01 Publisher alone stages/commits; independent readback | Combining writer into Publisher violates existing responsibility boundary and is not recommended | [119](119_20261118_prep03_od02_od03_row_export_design_candidate.md) §2 |
| **OD-05 Profiles** | **A: Method-owner Gate produces 40 remaining strict Profile schemas incrementally, preserving existing targets** | Config/Question/Design/Output/Inference versioned schema and negative tests; independent scientific truth stays with 07/T2/T3 | 40 ad hoc default configs or a new CLI estimator engine violate design | [120](120_20261118_prep03_od05_method_profile_gap_register.md) |

**OD-02 residual operational designation:** Choosing Ed25519 is not equivalent to nominating an approver or provisioning admin-controlled keys on the target OS. Owner must identify the accountable independent approval *role* and confirm actual deployment supports the trusted store + freshness model. If there is no available independent authority, **deny all row export**, do not allow a test or local user-signed policy to stand in.

**OD-05 scope:** This does not request the Owner to reapprove 40 statistical targets; when an actual inference formula/profile is missing or two authoritative records conflict, produce a narrow decision. In particular the HC1 AR realization's status between PREP02 proposed calculation (111) and detailed design (30_63) requires provenance reconciliation before G08 Freeze. 41 Method coverage must remain intact.

## 2. Concrete application order AFTER selections

1. Record the selected A/B/C for OD-01, OD-02, OD-03 and the independent approver/deployment prerequisite in append-only decision record, without fabricating an authorization signature.
2. Propagate adopted definitions to relevant revised RD/IF/DD *inside the Enhancement worktree* (do not promote `docs/wiki/requirement_definition/`).
3. Rewrite the impacted G02/G05/G10 06/07/Pxx standalone contracts; ensure nested Class/Method/Factory and positive/negative/typed errors are all directly embedded.
4. Verify strict Method config/Question/Design/Output schemas and only the actual per-Method unresolved inference choices, with acceptance code/negative tests held by the specific Gate.
5. Re-audit all affected 06/07/Pxx against design and legacy ABI. **Only then**, separately consider per-Gate Contract Freeze, upstream canonical 999 and Owner Coding Authorization.

## 3. Decision status, no false advancement

- `PREP03_OWNER_REVIEW_APPROVED` and `OD-04_GATE_DAG_PACKAGES_CLOSED` remain valid.
- `OD-01_OPEN`, `OD-02_OPEN`, `OD-03_OPEN` and `OD-05_PROFILE_AUTHORING_PENDING` remain so until actual selected decisions are recorded.
- No Scheme or Option in these three candidate documents silently supersedes source-of-truth design.
- No runtime code, test execution, `uv.lock`, Science PASS, Gate999 or Contract Freeze is authorized by preparing this pack.
