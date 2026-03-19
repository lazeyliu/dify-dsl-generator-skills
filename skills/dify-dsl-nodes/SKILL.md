---
name: dify-dsl-nodes
description: Dify DSL 节点知识技能。用于选择节点、理解节点字段、排查节点组合与容器闭环问题，以及补充逐节点文档依据；当问题已经进入具体节点层面时使用。
---

# dify-dsl-nodes

只在已经进入具体节点层面后使用，不要用它替代模式判断或模板路由。

## 入口

先读 [references/index.md](references/index.md)，再只加载本次会用到的节点文档。

## 约束

- 新建 DSL 时，优先遵循实体级字段和当前推荐写法。
- 审核或修复既有 DSL 时，要区分实体字段、fixture 常见字段和兼容字段。
- 如果问题其实是模式判断、任务路由或交付结论，退回对应 skill。
