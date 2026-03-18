# 基础目录索引

这是 `references/foundations/` 的正式入口页。

这个目录只放共享底座：模式判断、任务路由、交付约定、选择器模板、输出字段目录和字段口径。只要任务还没进入具体节点、模板或交付判断细则，优先在这里完成第一次收敛。

## 推荐读取顺序

1. 先读 [common-dsl.md](common-dsl.md)，统一当前导出标准、历史兼容形状和 UI 噪声字段口径。
2. 再读 [task-routing.md](task-routing.md)，决定是新建、修复、审核、优化还是模板起手。
3. 需要明确输出顺序时，读 [output-contract.md](output-contract.md)。
4. 需要确认 3 轮检查和结论门槛时，读 [validation-contract.md](validation-contract.md)。

## 按问题选文档

- “这到底是 `workflow`、`advanced-chat` 还是 `rag_pipeline`？”
  读 [orchestration-modes.md](orchestration-modes.md)。
- “我现在该走哪条处理路线？”
  读 [task-routing.md](task-routing.md)。
- “输出里应该先写什么、后写什么？”
  读 [output-contract.md](output-contract.md)。
- “什么情况下能说已精准校验？”
  读 [validation-contract.md](validation-contract.md)。
- “selector 应该怎么写？”
  读 [selector-templates.md](selector-templates.md)。
- “节点输出字段都有哪些稳定写法？”
  读 [output-fields-catalog.md](output-fields-catalog.md)。
- “上下游节点的输入输出约定怎么看？”
  读 [node-io-contracts.md](node-io-contracts.md)。
- “字段含义、fixture 线索和样例索引去哪看？”
  读 [field-explanations.md](field-explanations.md) 与 [fixture-index.md](fixture-index.md)。

## 典型请求

- “先别写 YAML，帮我判断这个需求应该做成 workflow、chatflow 还是 rag pipeline。”
- “我需要一个明确的输出顺序，先给模式判断、节点清单和连边，再给 DSL。”
- “selector 怎么写才稳定？哪些字段是导出噪声，哪些是运行时必需？”
- “我现在不知道该走修复、审核还是优化路线，先帮我路由。”

## 使用约束

- 这里解决的是“怎么路由、怎么判断、怎么写口径”，不是替代节点文档或模板文档。
- 如果已经明确是某个节点字段问题，转去 `references/nodes/`。
- 如果已经明确是选模板问题，转去 `references/templates/`。
- 如果已经进入审查、修复、优化和门禁判断，转去 `references/quality/` 或 `references/governance/`。
