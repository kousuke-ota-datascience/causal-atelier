# ENH-E6 G01 P02 — Stage-aware Presentation and Legacy Compatibility

- Status: `DRAFT`

## Outcome

`(family, stage)` から existing presentation surfaceをdeterministically bindし、legacy analytical left-navをcanonical compatibility shortcutへ限定する。

## Binding

- exploratory/* -> explore
- predictive/* -> predictive
- causal/setup|discovery -> discovery
- causal/identification|estimation|effects|diagnostics|sensitivity -> inference

## Legacy shortcuts

- Explore -> exploratory/profile
- Predictive -> predictive/setup
- Causal Discovery -> causal/discovery
- Causal Inference -> causal/identification

## Prohibited

- `causal -> discovery` のFamily-only canonical mapping
- missing bindingのsilent default
- legacy buttonが独立にworkspace/history/navigation stateを成立させること
