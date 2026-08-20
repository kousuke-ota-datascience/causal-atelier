# Architecture Discovery Prompt

ENH-E8の承認済みUI-only boundaryが成立せず、runtime lifecycle、authority/ownership、persistence/schema、legacy-path integration、source-of-truth等を変更する必要が判明した場合のみ使用する。

Discovery Agentは:

1. repository evidenceからcurrent architectureを記述する。
2. exact design conflictを特定する。
3. observed factとproposed architectureを分離する。
4. affected canonical document / Gate contractを列挙する。
5. implementationへ進まず停止する。
