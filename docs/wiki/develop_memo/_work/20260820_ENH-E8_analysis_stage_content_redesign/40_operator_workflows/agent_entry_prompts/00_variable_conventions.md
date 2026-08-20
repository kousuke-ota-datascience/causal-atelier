# Agent Prompt Variable Convention

主なplaceholder:

- `{{GATE_ID}}`: `G01`, `G02`
- `{{TRIAL_NO}}`: `01` 等
- `{{PACKAGE_ID}}`: `P01`, `P02`, `P03`
- `{{SHA}}`: Fixed Trial Candidate commit SHA
- `{{WORK_ROOT}}`: ENH-E8 workflow root
- `{{REMEDIATION_PACKAGE_ID}}`: remediation package identity

placeholderはAgent起動前にHuman operatorが具体値へ解決する。

未解決placeholderをnormative instructionとしてAgentへ渡さない。
