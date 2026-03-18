---
name: dify-dsl-generator
description: 生成、审核、分析、优化、调整、校验与修复 Dify Workflow、Chatflow、RAG Pipeline DSL 编排的技能。用于用户要求创建新 DSL、修改现有 DSL、按节点重排工作流、选择模板或模板变体、补齐必填字段和选择器、做只读审核、输出治理与发布结论、降低成本、提高稳定性、修复错误链路、输出已验证骨架、生成审核报告或对当前 DSL 做头脑风暴分析时。
---

# dify-dsl-generator

先判断目标是 `kind: app` 下的 `workflow` / `advanced-chat`，还是 `kind: rag_pipeline`，再决定允许使用的节点集合、输出节点和变量域。

这个 skill 的职责不是只“写一份 DSL”，而是做完整编排工作：

- 选模式
- 选模板
- 选模板变体
- 校验模板来源
- 生成或调整节点链路
- 补字段、补选择器、补失败路径
- 做结构审查、分级审查与报告
- 审查提示词、状态、安全与编排弹性，并给出提精准度与提灵活度建议

## 使用顺序

默认不要全量读取全部 reference。先做最小路由，再按任务补读。

### 新建 DSL

1. 先读 [references/common-dsl.md](references/common-dsl.md)，确认“当前导出标准 / 历史 fixture 形状 / 编辑器字段”三层口径。
2. 再读 [references/orchestration-modes.md](references/orchestration-modes.md)，判断是 `workflow`、`advanced-chat` 还是 `rag_pipeline`。
3. 再读 [references/node-index.md](references/node-index.md)，只加载本次会用到的节点文档。
4. 若要从模板起手，再读 [references/template-validation-status.md](references/template-validation-status.md) 与 [references/validated-template-skeletons.md](references/validated-template-skeletons.md)。
5. 最后再按需补 [references/selector-templates.md](references/selector-templates.md)、[references/output-fields-catalog.md](references/output-fields-catalog.md)、[references/node-io-contracts.md](references/node-io-contracts.md)。

### 修复或纠错

1. 先读 [references/common-dsl.md](references/common-dsl.md)。
2. 再读 [references/graph-validation-rules.md](references/graph-validation-rules.md)，先区分“源码硬校验”和“启发式审查”。
3. 再读 [references/fix-strategies.md](references/fix-strategies.md) 与 [references/anti-patterns.md](references/anti-patterns.md)。
4. 最后只加载相关节点文档，不要把整套节点文档读满。

### 优化或调优

1. 先读 [references/common-dsl.md](references/common-dsl.md)。
2. 再读 [references/mode-constraints.md](references/mode-constraints.md) 与 [references/connectivity-analysis.md](references/connectivity-analysis.md)。
3. 若目标是成本、稳定性或效果优化，再读 [references/optimization-playbook.md](references/optimization-playbook.md) 与 [references/tuning-playbook.md](references/tuning-playbook.md)。
4. 若涉及审查口径、提示词质量、精准度或编排灵活度，再读 [references/graded-review-model.md](references/graded-review-model.md)。
5. 若涉及既有 DSL 变更、发布判断、观测契约或能力块化，再读 [references/change-impact-review.md](references/change-impact-review.md)、[references/evaluation-gates.md](references/evaluation-gates.md)、[references/observability-contract.md](references/observability-contract.md)、[references/capability-contracts.md](references/capability-contracts.md)。
6. 若涉及覆盖率、最小充分性、升级门或问题编码，再读 [references/coverage-matrix.md](references/coverage-matrix.md)、[references/minimal-sufficiency.md](references/minimal-sufficiency.md)、[references/escalation-policies.md](references/escalation-policies.md)、[references/issue-taxonomy.md](references/issue-taxonomy.md)。

### 输出要求

先产出节点清单、连边清单和贯通性分析，再写 DSL 正文。不要一上来直接写大 YAML。
最终输出前，必须完成 3 轮检查；这 3 轮都完成，才可以把结果表述为“已精准校验”。
校验结果先写给人看，再写给机器看；默认使用自然语言或表格，不要只给 `YAML_OK`、`STRUCTURE_OK`、`PY_CODE_OK` 这类裸状态码。
每一轮至少写清：检查项、结论、含义、依据。
如果检查未做、覆盖不完整或仍有风险，要明确写出来，不要用含糊缩写替代。
报告结尾要区分“已直接采纳的改进”“有条件但未执行项”和“待确认项”。
除非用户明确要求机器可读标签，否则不要输出纯 `OK` / `FAIL` 列表。

### 第 1 轮: YAML 语法校验

必须至少做一次语法校验，确认 DSL 文本本身可被 YAML 解析；若当前环境无法执行解析器，要在报告里明确标记“未做语法校验”。

### 第 2 轮: 实体/模型级校验

必须至少做一次实体/模型级校验，优先用当前模式涉及的 Dify 节点实体去校验关键节点数据。校验目标不是只抓某几个小场景，而是系统性排除这类“YAML 能解析，但 `NodeData` / Pydantic 会拒绝”的大类错误:

- 字段值域错误
  例如枚举值、字面量、比较运算符不在允许集合内。
- 字段存在性错误
  例如必填字段缺失、必填数组为空、关键配置块未提供。
- 字段类型错误
  例如应为 `list`、`dict`、`bool`、`number` 却写成字符串。
- 字段形状错误
  例如列表字段给成对象、对象字段给成字符串 JSON、嵌套结构层级不对。
- 字段组合关系错误
  例如两个字段单独都合法，但组合起来不合法。
- 变量类型兼容性错误
  例如操作符、输入类型、目标变量类型三者之间不兼容。
- 运行时与内容一致性错误
  例如声明 `code_language: python3`，实际代码却是 Ruby、JavaScript 或其他不属于该运行时的语法。
- 兼容写法失配
  例如历史字段写法与当前实体写法混用，导致当前实体无法通过校验。

上面这些大类里，常见表现包括：

- `Input type constant is not supported for operation over-write`
- `Operation set is not supported for type array[string]`
- `default_value` 应为 `list` 却给了字符串 JSON
- Python 运行时里混入 Ruby 语法，导致 `SyntaxError: invalid syntax`

若当前环境无法执行实体校验，要在报告里明确标记“未做实体校验”。

### 第 3 轮: 独立复核

必须至少做一次独立复核。只要当前环境支持 subagent，就默认自动拉起 3 个只读 subagent 做交叉检查，不需要用户额外指令；如果环境不支持 3 个 subagent，至少要自动拉起 1 个只读 subagent；如果完全没有 subagent 能力，就退化为“自检 + 在报告里明确标记未做独立复核”。

### 分级审查

3 轮检查之外，最终报告还必须补 1 层分级审查，按 `阻塞项 / 高风险项 / 中风险项 / 优化项` 归类。
涉及提示词或模型节点时，至少审查：精炼性与可执行性、指令冲突、变量准确性、业务合理性、结果准确性、多语言一致性、失败兜底与恢复、安全与注入。
涉及复杂状态、工具链或多轮对话时，再审查：数据契约、状态污染、前置条件、决策覆盖、证据来源、多轮一致性、时效性、可观测性、成本时延、编排职责边界、副作用与幂等性、资源边界与终止性、回退契约一致性、敏感信息最小暴露、依赖与版本假设。
更细的分级口径、示例和提准/提灵活度抓手见 [references/graded-review-model.md](references/graded-review-model.md)。

## 关键约束

- 优先使用稳定、明确的字段，不要盲目复制导出 DSL 里的 UI 噪声字段。
- `kind: app` 与 `kind: rag_pipeline` 是两套顶层 DSL，不能混写。
- 优先保留运行时和导入所需字段，不要把编辑器字段、历史字段或 UI 噪声当成硬约束。
- 导出样例里常见的 `selected`、`height`、`width`、`positionAbsolute`、`zIndex`、`isInLoop`、`isInIteration` 大多是 UI 或运行时辅助信息。新建 DSL 时除非明确需要，否则不要主动生成。
- `retry_config`、`tool_parameters`、`datasource_parameters` 等区域存在历史写法和运行时写法差异。优先写稳定结构，并在报告里标记兼容性风险。
- 容器节点先定义容器本体，再定义内部起点，再定义容器内节点，再补齐容器内边和容器外边。
- `start` 与 `trigger-*` 默认不要共存，除非用户明确要求多入口并接受人工确认。

## 模式选择

- `workflow`: 优先使用 `start` + `end`，适合纯流程输出。
- `advanced-chat`: 优先使用 `start` + `answer`，需要考虑 `conversation_variables`、上下文和对话变量。
- `rag-pipeline`: 使用 `kind: rag_pipeline` 与 `rag_pipeline` 顶层块；节点仍放在 `workflow.graph` 下，优先围绕 `datasource`、`document-extractor`、`tool`、`knowledge-index` 组织，并检查 `rag_pipeline_variables`。

## 按任务优先加载的参考

- 总是优先读: [references/common-dsl.md](references/common-dsl.md)
- 生成时优先读: [references/orchestration-modes.md](references/orchestration-modes.md)、[references/node-index.md](references/node-index.md)
- 修复时优先读: [references/graph-validation-rules.md](references/graph-validation-rules.md)、[references/fix-strategies.md](references/fix-strategies.md)
- 优化时优先读: [references/mode-constraints.md](references/mode-constraints.md)、[references/connectivity-analysis.md](references/connectivity-analysis.md)
- 涉及分级审查、提示词质量、精准度或编排灵活度时，再读: [references/graded-review-model.md](references/graded-review-model.md)
- 涉及变更影响、发布门禁、观测字段或能力块化时，再读: [references/change-impact-review.md](references/change-impact-review.md)、[references/evaluation-gates.md](references/evaluation-gates.md)、[references/observability-contract.md](references/observability-contract.md)、[references/capability-contracts.md](references/capability-contracts.md)
- 涉及覆盖率、最小充分性、升级门或问题编码时，再读: [references/coverage-matrix.md](references/coverage-matrix.md)、[references/minimal-sufficiency.md](references/minimal-sufficiency.md)、[references/escalation-policies.md](references/escalation-policies.md)、[references/issue-taxonomy.md](references/issue-taxonomy.md)
- 需要模板时再读: [references/template-validation-status.md](references/template-validation-status.md)、[references/validated-template-skeletons.md](references/validated-template-skeletons.md)

## 生成策略

先输出下面四个中间产物，再输出最终 DSL：

1. 模式判断
2. 节点清单
3. 连边清单
4. 字段检查表
5. 贯通性分析
6. 优化/修复建议

如果用户要求“全节点编排”，在节点清单里把未使用节点也列为“可选未启用”，并说明为什么不启用。

## 审核策略

- 自检关注字段完整性、选填字段是否需要补齐、变量选择器、容器节点闭环、输出节点、触发器唯一性。
- 最终必须完成 3 轮检查: YAML 语法校验、实体/模型级校验、独立复核。
- 报告里的校验结论必须先给“校验摘要”，逐项说明检查项、结论、含义和依据；禁止只给状态码列表。
- 报告里还必须给“分级审查摘要”，至少覆盖结构可导入性、运行时代码、提示词质量、业务合理性和结果准确性。
- 第 1 轮要确认生成结果不是语法层面的坏 YAML。
- 第 2 轮要确认生成结果不是 `NodeData` / Pydantic 层面的坏配置，覆盖字段值域、字段存在性、字段类型、字段形状、字段组合关系、变量类型兼容性、运行时与内容一致性和兼容写法失配问题。
- 第 3 轮独立复核只要环境支持，就默认自动使用 3 个只读 subagent；关注“是否遗漏节点必填字段”“是否混入明显错误的历史字段”“是否存在无法闭合的边或悬空选择器”“贯通路径是否真实可达”。
- 独立复核要优先使用角色分工明确的独立提示词；视任务复杂度选择异步并行复核或同步串行复核，并在报告里写清模式与原因。
- 若多方复核结论冲突，要追加冲突归并与仲裁结论，明确采纳项、未采纳项和原因。
- 若未显式指定，默认策略按 `strict` 解释；覆盖率通过标准为适用路径 `>= 95%`，且主路径、fallback 路径、外部异常路径不得缺测；面向用户阅读的默认输出为 `纯文本`，面向 API 或 DSL 流程消费的默认输出为 `JSON`，可选输出形态为 `Markdown`、`HTML`。
- 修改既有 DSL 时，要补做变更影响面与回归差异审查；准备宣称“可直接导入”前，要补做发布门禁审查。
- 对带提示词的节点，不只审查“能不能跑”，还要审查“是否说得清楚、是否说得合理、是否容易说错”。
- 除了找问题，还要给 1 到 3 个最高收益的提准或提灵活度建议，优先规则护栏、中间语义层、置信度门、样例回放、模板分层、能力块化编排与适配层。
- 对“黄金样例与对抗回放、置信度门与拒答门、运行期自修复、能力裁剪、输出形态切换”这 5 类条件项，满足条件时应直接执行或纳入设计；不满足时要在报告里写清未执行原因。
- 复杂链路还应补：内部语义对象最小 schema、输入归一化、证据快照和决定性边界，不要让关键判断长期漂浮在自由文本里。
- 关键链路还应补：观测契约、能力块契约与最小暴露原则，避免可调试性、复用边界和敏感信息控制长期漂浮在口头约束里。
- 修改既有 DSL 或准备交付前，还应补：覆盖率矩阵、最小充分性判断、升级门与问题编码；这些属于治理层硬项，不要只作为口头建议。
- 报告末尾要明确哪些改进已直接采纳，哪些因条件不足暂未执行，哪些仍依赖样例、运行环境或业务口径确认。
- 报告必须给出“可直接导入 / 需要人工确认 / 明显不完整”三档结论。
