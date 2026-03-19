---
name: dify-dsl-foundations
description: Dify DSL 共享底座技能。用于模式判断、任务路由、selector 模板、稳定字段口径、输出契约和校验门槛；在 authoring、review、refactor 之前都应先用它收敛基础判断。
---

# dify-dsl-foundations

先解决“这是什么模式、该走哪条路线、字段和输出口径怎么统一”，再进入节点、模板、审查或交付判断。

## 入口

先读 [references/index.md](references/index.md)，再按需补 `common-dsl / task-routing / orchestration-modes / selector-templates / output-contract / validation-contract`。

## 路由边界

- 节点字段与节点组合，转去 [../dify-dsl-nodes/SKILL.md](../dify-dsl-nodes/SKILL.md)
- 模板选择与模板变体，转去 [../dify-dsl-templates/SKILL.md](../dify-dsl-templates/SKILL.md)
- 审查、修复、优化策略，转去 [../dify-dsl-quality/SKILL.md](../dify-dsl-quality/SKILL.md)
- 发布结论、覆盖率、变更影响，转去 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)
