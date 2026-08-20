# Formal FAIL Remediation Coding Agent Prompt

canonical `999 Gate Decision = FAIL` の場合のみ使用する。

1. failed candidateとfailure evidenceを固定する。
2. applicable `08` remediation contractだけをnormative remediation scopeとして実装する。
3. frozen 06/07のsemanticsを変更しない。
4. contract defectが判明した場合は停止し、`09` amendmentへescalateする。
5. remediation evidenceを記録し、新しいFixed Trial Candidateは次Trialとして扱う。
