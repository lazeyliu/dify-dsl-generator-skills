---
name: dify-dsl-generator
description: 生成、审查、修复、优化与重构 Dify Workflow、Chatflow、RAG Pipeline DSL 的技能。用于从零创建 DSL、只读审核现有 DSL、修补节点/连边/选择器错误、按模板重排工作流、输出交付判断与发布结论，或在改写前先对当前 DSL 做结构分析。
---

# dify-dsl-generator

把 Dify DSL 当成“要设计、审核、验证并判断能否交付的编排系统”，不要把任务简化成“直接写一份 YAML”。

## 先确定入口

先看 [references/index.md](references/index.md) 把整个参考目录收敛到正确子树。
任何任务都先读 [references/foundations/common-dsl.md](references/foundations/common-dsl.md)，分清当前导出标准、历史兼容形状和 UI 噪声字段。
共享底座、选择器和字段口径集中在 [references/foundations/index.md](references/foundations/index.md)。

随后按任务类型读 [references/foundations/task-routing.md](references/foundations/task-routing.md)：

- 新建 DSL
- 修复或纠错
- 只读审核 / 发布判断
- 优化或重构
- 模板起手

涉及具体节点时，再读 [references/nodes/index.md](references/nodes/index.md) 并只加载本次会用到的节点文档。
只有在需要模板、selector、输出字段、约定或交付结论时，才补读对应 reference，不要整库读满。

## 核心原则

- 先判断顶层模式，再决定允许节点集合、终点节点和变量域。
- 先产出模式判断、节点清单、连边清单和字段检查表，再写 DSL 正文。
- 新建 DSL 时优先稳定字段；不要盲目复制 `selected`、`height`、`width`、`positionAbsolute`、`zIndex`、`isInLoop`、`isInIteration` 等 UI 或导出噪声字段。
- 修改既有 DSL 时，补做变更影响、回归差异和上线前检查判断。
- 报告先写给人看，再给结构化明细；除非用户明确要求，不要只输出裸状态码。
- 独立复核优先使用子代理，但必须服从当前平台和会话的授权策略；如果策略不允许自动拉起子代理，就退化为自检并明确写出风险。

## 模式快速判断

- `kind: app` + `app.mode: workflow`：适合纯流程输出，终点通常是 `end`。
- `kind: app` + `app.mode: advanced-chat`：适合多轮对话，终点通常是 `answer`，并检查 `conversation_variables`。
- `kind: rag_pipeline`：顶层使用 `rag_pipeline`，图仍在 `workflow.graph` 下，优先围绕 `datasource`、`document-extractor` / `tool`、`knowledge-index` 组织。

如果模式尚不明确，先输出候选模式与理由，不要直接写大段 YAML。

## 交付约定

按 [references/foundations/output-contract.md](references/foundations/output-contract.md) 组织输出。默认先给这些中间产物：

1. 模式判断
2. 节点清单
3. 连边清单
4. 字段检查表
5. 贯通性分析
6. 优化 / 修复建议

按 [references/foundations/validation-contract.md](references/foundations/validation-contract.md) 完成最少 3 轮检查：

1. YAML 语法校验
2. 实体 / 模型级校验
3. 独立复核

如果任何一轮没做，明确写出缺口，并把结论降级为“需要人工确认”或“明显不完整”，不要表述为“已精准校验”。

## 按需补读

- 模板与变体：先读 `references/templates/index.md`，再按需补 `references/templates/template-validation-status.md`、`references/templates/validated-template-skeletons.md`、`references/templates/template-variants.md`、`references/templates/templates-library.md`
- 基础底座与共享约定：先读 `references/foundations/index.md`，再按需补 `common-dsl / orchestration-modes / selector-templates / output-fields-catalog / node-io-contracts`
- 选择器与字段：`references/foundations/selector-templates.md`、`references/foundations/output-fields-catalog.md`、`references/foundations/node-io-contracts.md`
- 审核、修复与优化：先读 `references/quality/index.md`，再按需补 `review-checklist / report-template / subagent-review / mode-constraints / connectivity-analysis / optimization-playbook / tuning-playbook / graded-review-model`
- 发布、约定与交付判断：先读 `references/governance/index.md`，再按需补 `change-impact-review / evaluation-gates / observability-contract / capability-contracts / coverage-matrix / minimal-sufficiency / escalation-policies / issue-taxonomy`

## 明确不要做的事

- 不要混写 `kind: app` 与 `kind: rag_pipeline`。
- 不要默认让 `start` 与多个 `trigger-*` 共存，除非用户明确接受多入口。
- 不要把历史兼容字段、导出噪声字段和运行时必需字段混成同一层硬约束。
- 不要跳过中间分析，直接生成长 YAML。
