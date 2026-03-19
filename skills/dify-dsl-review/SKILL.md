---
name: dify-dsl-review
description: 只读审查现有 Dify Workflow、Chatflow、RAG Pipeline DSL 的入口技能。用于模式判断、结构分析、风险分级、导入判断和发布结论；如果用户要求修改 DSL 或目标仍然模糊，转去 dify-dsl-refactor 或 dify-dsl-brainstorming。
---

# dify-dsl-review

只做只读审查，不修改文件，不重写 DSL。

## 协作顺序

1. 先读 [../dify-dsl-foundations/SKILL.md](../dify-dsl-foundations/SKILL.md)。
2. 涉及具体节点时，读 [../dify-dsl-nodes/SKILL.md](../dify-dsl-nodes/SKILL.md)。
3. 进入问题发现、问题分级、子代理复核和优化判断时，读 [../dify-dsl-quality/SKILL.md](../dify-dsl-quality/SKILL.md)。
4. 需要发布结论、覆盖率、变更影响或观测字段判断时，读 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)。
5. 如果用户明确要求多方独立复核，或当前复杂度已经高到需要正式编排子代理复核，转去 [../dify-dsl-subagent-review/SKILL.md](../dify-dsl-subagent-review/SKILL.md)。

## 最低输出

1. 模式判断
2. 节点清单
3. 连边清单
4. 字段检查表
5. 风险分级
6. 最终结论

## 约束

- 不要修改文件。
- 不要把建议修复直接写成重构正文。
- 如果用户要“最小修复方案”或“直接帮我改”，转去 [../dify-dsl-refactor/SKILL.md](../dify-dsl-refactor/SKILL.md)。
- 如果目标不清、范围互相冲突，回到 [../dify-dsl-brainstorming/SKILL.md](../dify-dsl-brainstorming/SKILL.md)。
