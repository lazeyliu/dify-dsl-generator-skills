---
name: dify-dsl-authoring
description: 从明确需求生成 Dify Workflow、Chatflow、RAG Pipeline DSL 草稿的入口技能。用于模式判断、模板起手、节点组合、字段补齐和草稿输出；如果阻塞未知项尚未澄清，先回 dify-dsl-brainstorming。
---

# dify-dsl-authoring

只负责“把已经明确的目标写成 Dify DSL 草稿”，不负责发布结论。

## 进入条件

- 任务目标已经明确。
- 已知是新建 DSL，或从模板起手生成新骨架。
- 如果用户显式经过头脑风暴，阻塞未知项已经清零。

如果这些条件不成立，先回 [../dify-dsl-brainstorming/SKILL.md](../dify-dsl-brainstorming/SKILL.md)。

## 协作顺序

1. 先读 [../dify-dsl-foundations/SKILL.md](../dify-dsl-foundations/SKILL.md)，完成模式判断、任务路由、字段口径和输出契约收敛。
2. 需要从模板起手时，读 [../dify-dsl-templates/SKILL.md](../dify-dsl-templates/SKILL.md)。
3. 确定节点和节点组合时，读 [../dify-dsl-nodes/SKILL.md](../dify-dsl-nodes/SKILL.md)。

## 最低输出

1. 模式判断
2. 模板选择与未选理由（如果走模板路线）
3. 节点清单
4. 连边清单
5. 字段检查表
6. DSL 草稿
7. 仍待确认项

## 约束

- 不要在需求仍模糊时硬写 DSL。
- 不要跳过模式判断直接写长 YAML。
- 不要宣称“可直接导入”或“已精准校验”；如果需要这类结论，转去 [../dify-dsl-review/SKILL.md](../dify-dsl-review/SKILL.md)。
