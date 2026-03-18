# dify-dsl-generator

[English](./README.md) | [简体中文](./README.zh-CN.md)

一个面向 AI agent 的通用型 Dify DSL skill，用于生成、审核、分析、优化与修复：

- `kind: app` 下的 `workflow`
- `kind: app` 下的 `advanced-chat`
- `kind: rag_pipeline`

这个 skill 的目标不只是产出一份 YAML，而是把 Dify DSL 当作一个可以被审核、调优、验证和治理的编排系统来处理。

它的核心工作流是平台中立的：

- `SKILL.md` 与 `references/` 是可移植的核心层
- `agents/openai.yaml` 是当前面向 OpenAI / Codex 的适配元数据
- 其他 agent 平台即使不识别这份适配文件，也可以复用核心工作流

## 适用场景

这个 skill 适合这些任务：

- 从零创建新的 Dify DSL
- 修改现有 DSL
- 只读审核当前 DSL，不修改文件
- 在改动前对当前 DSL 做头脑风暴与分析
- 输出结构化审查报告、发布门禁和调优建议

## 核心能力

- DSL 生成：选模式、选模板、补必填字段、补选择器、补失败路径
- DSL 修复：修复结构问题、兼容问题和图闭环问题
- DSL 审核：语法校验、实体校验、独立复核和分级审查
- DSL 分析：只读分析当前 DSL，输出风险、发现和优化建议
- DSL 优化：提升精准度、稳定性、可观测性和编排灵活度
- DSL 治理：支持变更影响面、覆盖率矩阵、发布门禁、观测契约和能力块契约

## 调用方式

在支持显式 skill 调用的 Codex 或兼容 agent 环境中，可以这样使用：

```text
使用 $dify-dsl-generator 审核这份 Dify DSL，并给出结构化建议。
```

常见用法包括：

- 只读审核现有 DSL，不修改文件
- 对当前 DSL 做头脑风暴，分析如何改进
- 在改动前列出节点、边、影响面和风险点
- 在改动后输出审查报告、发布门禁结果和调优建议

如果其他 agent 平台不支持同样的调用方式或元数据模型，建议退化为：

- 先读取 `SKILL.md`
- 再按需读取 `references/` 里的文件
- 然后按只读审查、修改或分析模式执行对应流程

## 审核与治理特点

这个 skill 默认强调：

- 先给人类可读结论，再给结构化细节
- 关键问题按 `阻塞项 / 高风险项 / 中风险项 / 优化项` 分级
- 支持多 subagent 独立复核，并区分异步并行与同步串行模式
- 支持冲突仲裁，而不是简单拼接多份复核结果
- 支持变更影响面、覆盖率矩阵、最小充分性、升级门、问题编码和发布门禁等治理项

## 平台兼容性

这个仓库设计成可跨 agent 生态复用：

- OpenAI / Codex：
  使用 `agents/openai.yaml` 作为当前适配元数据。
- Claude / Qwen / 其他 agent：
  可以直接复用 `SKILL.md` 和 `references/` 作为核心工作流。
- 如果当前平台不支持 subagent：
  退化为串行复核或自检，不默认假设一定能多 agent 复核。
- 如果需要平台特有元数据：
  优先新增独立适配文件，而不是改动可移植的核心层。

换句话说：

- skill 定义本体在 `SKILL.md`
- 操作细节和审查口径在 `references/`
- 平台适配元数据放在 `agents/`

当前仓库自带的是 OpenAI / Codex 适配层，但 skill 本身并不只服务于 OpenAI / Codex。

## 默认约定

- 默认策略档位：`strict`
- 覆盖率通过标准：适用路径覆盖率 `>= 95%`，且主路径、fallback 路径、外部异常路径不得缺测
- 面向用户阅读的默认输出：`纯文本`
- 面向 API 或 DSL 流程消费的默认输出：`JSON`
- 可选输出形态：`Markdown`、`HTML`

## 目录结构

```text
dify-dsl-generator/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── agents/
│   └── openai.yaml
└── references/
    ├── common-dsl.md
    ├── graded-review-model.md
    ├── report-template.md
    ├── review-checklist.md
    ├── subagent-review.md
    ├── evaluation-gates.md
    ├── coverage-matrix.md
    ├── observability-contract.md
    ├── capability-contracts.md
    └── ...
```

## 目录说明

- `SKILL.md`
  可移植的核心工作流与执行说明。
- `agents/openai.yaml`
  面向 OpenAI / Codex 的适配元数据，用于该平台下的展示与调用。
- `references/`
  按需加载的参考资料、审查规则、模板和治理说明。
- `README.md`
  面向 GitHub 读者和维护者的英文说明。
- `README.zh-CN.md`
  面向 GitHub 读者和维护者的中文说明。
- `LICENSE`
  仓库许可证文件。

## 维护建议

- 调整审查口径时，优先把细节放进 `references/`，不要持续膨胀 `SKILL.md`
- 修改报告格式或治理规则时，注意同步 `report-template.md`、`review-checklist.md` 和 `subagent-review.md`
- 引入新的默认约定时，同时更新 `SKILL.md` 和相关 reference
- 如果要支持新的 agent 平台，优先在 `agents/` 下增加独立适配文件，而不是直接改动核心工作流

## 许可证

当前仓库使用 [MIT License](./LICENSE)。
