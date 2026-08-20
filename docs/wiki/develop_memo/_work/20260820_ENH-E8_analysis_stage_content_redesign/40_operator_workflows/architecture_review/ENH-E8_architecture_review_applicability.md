# ENH-E8 Architecture Review Applicability

Decision: `N/A_FOR_CURRENT_SCOPE`

ENH-E8はfrontend UI/IA conformanceのみを対象とし、runtime lifecycle、authority/ownership、persistence/schema、API、backend semanticsを変更しない。

実装中にこれらの変更が必要と判明した場合はscopeを暗黙拡張せず、contractを`BLOCKED`としてArchitecture Reviewへescalateする。
