# 任务路由

先用本页决定最小读取集合，不要一上来把整个 `references/` 读满。

## 总入口

1. 先读 [common-dsl.md](common-dsl.md)。
2. 判断任务类型：新建、修复、审核、优化 / 重构、模板起手。
3. 走本页对应路线。
4. 只有在确定会用到某个节点后，才去 [index.md](../nodes/index.md) 继续加载节点文档。

## 新建 DSL

适用于从零生成 `workflow`、`advanced-chat` 或 `rag_pipeline`。

1. 读 [orchestration-modes.md](orchestration-modes.md)，先判模式。
2. 读 [index.md](../nodes/index.md)，只加载本次会用到的节点文档。
3. 需要 selector、字段目录或上下游约定时，再补 [selector-templates.md](selector-templates.md)、[output-fields-catalog.md](output-fields-catalog.md)、[node-io-contracts.md](node-io-contracts.md)。

这一路最后至少要给：

- 模式判断
- 节点清单
- 连边清单
- 字段检查表
- 贯通性分析

常见问法：

- “帮我从零写一个 workflow，输入 query 后调用工具并输出结构化结果。”
- “我要一个最小 chatflow 骨架，先给模式判断和节点清单。”

## 模板起手

适用于“先挑模板，再做裁剪、补字段或重排”。

1. 先走“新建 DSL”路线。
2. 先读 [index.md](../templates/index.md) 做模板路由。
3. 再读 [template-validation-status.md](../templates/template-validation-status.md) 确认模板来源状态。
4. 读 [validated-template-skeletons.md](../templates/validated-template-skeletons.md) 选择可落地骨架。
5. 需要同类变体或替代模板时，再读 [template-variants.md](../templates/template-variants.md) 与 [templates-library.md](../templates/templates-library.md)。

这一路最后至少要给：

- 选中模板与未选模板的取舍理由
- 模板中保留 / 删除 / 改写的节点
- 兼容性与风险说明

常见问法：

- “不要从零写，先给我一个最接近的模板骨架。”
- “把现有需求映射成低成本版 / 稳定版模板变体。”

## 修复或纠错

适用于 YAML 能看懂但结构、字段、选择器、链路或运行时配置明显有问题的场景。

1. 先读 [index.md](../quality/index.md) 做质量路由。
2. 读 [graph-validation-rules.md](../quality/graph-validation-rules.md)，先区分硬校验与启发式问题。
3. 读 [fix-strategies.md](../quality/fix-strategies.md) 与 [anti-patterns.md](../quality/anti-patterns.md)，决定修复路径。
4. 再按问题位置补读节点文档，不要把整套节点文档全读一遍。
5. 涉及代码节点、工具节点、外部请求或复杂容器时，再补读相关节点文档与 [node-io-contracts.md](node-io-contracts.md)。

这一路最后至少要给：

- 错误归因
- 最小修复方案
- 修复后链路闭环
- 仍未消除的兼容性风险

常见问法：

- “这份 DSL 导不进去，先找出会被实体校验拒绝的地方。”
- “不要重做，帮我修最小必要字段和断边。”

## 只读审核或发布判断

适用于不直接改 DSL，只做结构分析、问题分级、交付判断或上线前检查结论。

1. 先读 [index.md](../quality/index.md) 做审核路由。
2. 读 [review-checklist.md](../quality/review-checklist.md)。
3. 读 [validation-contract.md](validation-contract.md)。
4. 读 [output-contract.md](output-contract.md)。
5. 需要完整报告格式时，再读 [report-template.md](../quality/report-template.md)。
6. 需要独立复核分工或提示词时，再读 [subagent-review.md](../quality/subagent-review.md)。
7. 涉及上线前检查、变更影响、覆盖率或输入输出约定时，再读 [index.md](../governance/index.md)。

这一路最后至少要给：

- 校验摘要
- 分级审查摘要
- 最终结论
- 已直接采纳 / 有条件未执行 / 待确认项

常见问法：

- “先不要改文件，只审核并给我能不能上线的结论。”
- “帮我做上线前检查判断和风险分级。”

## 优化或重构

适用于降低成本、提升稳定性、增强可观测性、拆分职责边界、引入更清晰的中间语义层，或对既有 DSL 做较大结构调整。

1. 先读 [index.md](../quality/index.md) 做优化路由。
2. 读 [mode-constraints.md](../quality/mode-constraints.md) 与 [connectivity-analysis.md](../quality/connectivity-analysis.md)。
3. 针对成本、稳定性和效果，读 [optimization-playbook.md](../quality/optimization-playbook.md) 与 [tuning-playbook.md](../quality/tuning-playbook.md)。
4. 涉及提示词质量、结果准确性、编排灵活度和交付判断建议时，读 [graded-review-model.md](../quality/graded-review-model.md)。
5. 涉及变更影响、上线前检查、观测字段约定或能力块化时，先读 [index.md](../governance/index.md)，再读 [change-impact-review.md](../governance/change-impact-review.md)、[evaluation-gates.md](../governance/evaluation-gates.md)、[observability-contract.md](../governance/observability-contract.md)、[capability-contracts.md](../governance/capability-contracts.md)。
6. 涉及覆盖率、是否已经够用、升级条件或问题编码时，再补 [coverage-matrix.md](../governance/coverage-matrix.md)、[minimal-sufficiency.md](../governance/minimal-sufficiency.md)、[escalation-policies.md](../governance/escalation-policies.md)、[issue-taxonomy.md](../governance/issue-taxonomy.md)。

这一路最后至少要给：

- 为什么当前结构需要优化或重构
- 哪些节点 / 约定 / 语义层会变化
- 哪些交付判断项必须同步补齐

常见问法：

- “这条链路成本太高，帮我改成低成本版但别牺牲主路径稳定性。”
- “帮我把现有 DSL 重构成更清晰的能力块，顺便补观测字段约定。”

## 任务切换规则

- 同时出现“先生成再审查”时，先按“新建 DSL”路线完成结构草稿，再补“只读审核或发布判断”。
- 同时出现“先修复再优化”时，先消除阻塞导入问题，再讨论性能、成本和弹性优化。
- 如果问题本质上是模式判断错误，不要在错误模式上继续修字段，先回到 [orchestration-modes.md](orchestration-modes.md) 重判。
