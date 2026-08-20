# ENH-E8 Requirement / Design Consistency & Traceability Review

- Status: `APPROVED`

| Requirement / Invariant | Design realization | Gate | Acceptance focus |
|---|---|---|---|
| FR-163, FR-166, NFR-022, E8-DI-01 | Selected Project parent navigation -> `/projects` | G01 | visible action, canonical route, direct entry, Back/Forward |
| FR-153–156, FR-174, E8-DI-02/03/05 | Causal current-stage identity / responsibility separation | G02 | positive/negative visibility, guidance, control/result ownership |
| FR-149–152, FR-174, FR-176, E8-DI-02/03/06 | Predictive Stage responsibility separation | G02 | stage-specific purpose/result, existing spec semantics |
| FR-057, FR-150, E8-DI-06/09 | Dataset-schema-backed Predictive feature selector | G02 | schema-derived option, checkbox Confirm/Cancel, exact `feature_spec.feature_columns` mapping, Train/Predict read-only |
| E8-DI-04 | presentation-only Causal grouping | G02 | group labelがroute/persistent/runtime authorityではない |
| E8-DI-07 | vertical semantic flow | G02 | desktop/narrow rendering、section composition起因のpage-level overflowなし |
| FR-177, E8-DI-08 | compatibility boundary | G01/G02 | API/schema/backend/runtime/algorithm semantic diffなし |
| NFR-026, E8-DI-06/09 | draft/state continuity | G02 | Stage switchingでvalid draft/feature selectionを失わない |

## Consistency decision

Requirement revisionを必要とする矛盾は確認されていない。

Predictive feature selectorも、UI interactionのみを変更し、submitted analytical specificationとvalidation authorityを維持するため、既存feature-set contractと整合する。
