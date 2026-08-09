# Operator Prompts

作業指示者がAgentへ渡す最小入口プロンプト。

詳細な作業契約は `10_enhance_instruction/` に一本化し、
外側promptへ重複仕様を書かない。

Test Agentには07に加え、具体的なimplementation completion report pathを必ず指定する。
FAIL修正Coding Agentには06に加え、具体的なprevious Gate Decision report pathを指定する。
