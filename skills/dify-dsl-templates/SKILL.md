---
name: dify-dsl-templates
description: Dify DSL 模板技能。用于从模板起手、选择骨架、比较模板变体，并标记模板属于已验证、间接支撑还是能力推导；当任务明确涉及模板路线时使用。
---

# dify-dsl-templates

模板只负责“选起点”，不替代字段检查、节点检查和发布判断。

## 入口

先读 [references/index.md](references/index.md)，依次收敛模板库、模板状态、可落地骨架和模板变体。

## 约束

- 模板路线仍然需要配合 [../dify-dsl-foundations/SKILL.md](../dify-dsl-foundations/SKILL.md) 做模式与字段口径判断。
- 如果用户其实要直接生成 DSL 草稿，入口应是 [../dify-dsl-authoring/SKILL.md](../dify-dsl-authoring/SKILL.md)。
- 如果模板状态不是已验证，报告里必须标记证据等级。
