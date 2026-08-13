# ENH-E6 Technical Debt / Follow-up Ledger

**Document class:** Planning / State-support Artifact  
**Self-containment:** MUST for ENH-E6 debt/follow-up decisions.

## 1. Source anomaly inheritance

### ANOM-E5-001 — Family Tab Observable UI Gap

- Source enhancement: `ENH-E5`
- Source status: `OPEN_FOLLOW_UP`
- ENH-E6 status: `IN_SCOPE / NOT YET RESOLVED`
- Target Gate: `G01`

Resolution requires G01 final independent PASS, including observable Family tabs in clean environment, actual Family/Stage operations, history/deep-link/legacy compatibility, stage-aware presentation, and protected regression.

Package completion, candidate assembly, or Coding Agent self-check must not mark this resolved.

## 2. Accepted temporary compatibility boundary

Legacy analytical left-nav remains as compatibility surface in ENH-E6. Its state authority must be removed, but visual removal/restructuring is not required. This is accepted temporary architecture, not proof of unresolved G01 defect if canonical shortcut behavior passes.

## 3. Potential follow-up excluded from ENH-E6

- full replacement/removal of legacy analytical left navigation IA
- Family-specific complete Stage screen redesign
- per-stage URL-owned microfrontend decomposition
- removal of all legacy `/explore|/predictive|/causal` route compatibility
- broader navigation visual design refresh

## 4. Exit / promotion rule

Only G01 final PASS can close `ANOM-E5-001` in ENH-E6 Current State. Future-scope items remain outside G01 and must not be smuggled into P01-P03 without explicit enhancement/contract decision.
