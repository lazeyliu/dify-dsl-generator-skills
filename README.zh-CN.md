# dify-dsl-generator

[English](README.md) | [简体中文](README.zh-CN.md)

一个面向 AI agent 的通用型 Dify DSL skill，用于生成、审核、分析、优化与修复：

- `kind: app` 下的 `workflow`
- `kind: app` 下的 `advanced-chat`
- `kind: rag_pipeline`

这个 skill 的目标不只是产出一份 YAML，而是把 Dify DSL 当作一个要被审核、调优、验证并判断能否交付的编排系统来处理。

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
- 输出结构化审查报告、上线前检查结果和调优建议

## 核心能力

- DSL 生成：选模式、选模板、补必填字段、补选择器、补失败路径
- DSL 修复：修复结构问题、兼容问题和图闭环问题
- DSL 审核：语法校验、实体校验、独立复核和分级审查
- DSL 分析：只读分析当前 DSL，输出风险、发现和优化建议
- DSL 优化：提升精准度、稳定性、可观测性和编排灵活度
- DSL 交付判断：支持变更影响面、覆盖率矩阵、上线前检查、观测字段约定和能力块边界约定

## 调用方式

在支持显式 skill 调用的 Codex 或兼容 agent 环境中，可以这样使用：

```text
使用 $dify-dsl-generator 审核这份 Dify DSL，并给出结构化建议。
```

常见用法包括：

- 只读审核现有 DSL，不修改文件
- 对当前 DSL 做头脑风暴，分析如何改进
- 在改动前列出节点、边、影响面和风险点
- 在改动后输出审查报告、上线前检查结果和调优建议

如果其他 agent 平台不支持同样的调用方式或元数据模型，建议退化为：

- 先读取 `SKILL.md`
- 从 `references/index.md` 开始看总入口
- 从 `references/foundations/task-routing.md` 开始路由
- 再按需读取 `references/` 里的文件
- 然后按只读审查、修改或分析模式执行对应流程

## 审核与交付判断特点

这个 skill 默认强调：

- 先给人类可读结论，再给结构化细节
- 关键问题按 `阻塞项 / 高风险项 / 中风险项 / 优化项` 分级
- 支持多子代理独立复核，并区分异步并行与同步串行模式
- 支持冲突仲裁，而不是简单拼接多份复核结果
- 支持变更影响面、覆盖率矩阵、是否已经够用、升级条件、问题编码和上线前检查等交付判断项

## 平台兼容性

这个仓库设计成可跨 agent 生态复用：

- OpenAI / Codex：
  使用 `agents/openai.yaml` 作为当前适配元数据。
- Claude / Qwen / 其他 agent：
  可以直接复用 `SKILL.md` 和 `references/` 作为核心工作流。
- 如果当前平台不支持子代理：
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
├── scripts/
│   ├── fast_test_dsl.py
│   ├── fast_test_suite.py
│   ├── check_forward_test_cases.py
│   ├── init_forward_test_case.py
│   ├── quick_validate.py
│   └── validate_skill_repo.py
├── tests/
│   ├── cases/
│   ├── prompts/
│   ├── fixtures/
│   │   └── dsl/
│   ├── expectations/
│   └── harness/
│       └── assert_output.py
└── references/
    ├── index.md
    ├── foundations/
    │   ├── index.md
    │   ├── common-dsl.md
    │   ├── task-routing.md
    │   └── validation-contract.md
    ├── nodes/
    │   ├── index.md
    │   ├── node-llm.md
    │   └── ...
    ├── templates/
    │   ├── index.md
    │   ├── template-validation-status.md
    │   └── ...
    ├── quality/
    │   ├── index.md
    │   ├── review-checklist.md
    │   ├── report-template.md
    │   ├── subagent-review.md
    │   └── ...
    └── governance/
        ├── index.md
        ├── evaluation-gates.md
        ├── coverage-matrix.md
        └── ...
```

## 目录说明

- `SKILL.md`
  可移植的核心工作流与执行说明。
- `agents/openai.yaml`
  面向 OpenAI / Codex 的适配元数据，用于该平台下的展示与调用。
- `references/`
  按主题拆分的按需加载资料，避免主 skill 和 reference 一起膨胀；总入口是 `references/index.md`。
- `references/foundations/`
  入口文档、任务路由、交付约定、选择器和共享字段口径，正式入口是 `references/foundations/index.md`。
- `references/nodes/`
  节点目录入口与逐节点说明，正式入口是 `references/nodes/index.md`。
- `references/templates/`
  模板入口、模板变体和已验证骨架，正式入口是 `references/templates/index.md`。
- `references/quality/`
  审核、修复、优化和独立复核规则，正式入口是 `references/quality/index.md`。
- `references/governance/`
  上线前检查、覆盖率、约定和交付判断相关资料，正式入口是 `references/governance/index.md`。
- `scripts/validate_skill_repo.py`
  本地结构校验脚本，用于检查 frontmatter、适配元数据和 Markdown 链接完整性。
- `scripts/quick_validate.py`
  与标准 skill 维护流程对齐的兼容验证入口。
- `scripts/fast_test_dsl.py`
  只读快速验证脚本，用真实 Dify DSL 样本检查它命中了哪些入口路由和复杂度信号。
- `scripts/fast_test_suite.py`
  对一组真实 DSL 样本汇总快速验证覆盖率，显示哪些入口路线还没有被样本命中。
- `scripts/check_forward_test_cases.py`
  校验仓库内的前向验证用例，并汇总它们声明的路线覆盖。
- `scripts/init_forward_test_case.py`
  初始化一个可复用的前向验证用例目录，自动生成 `prompt.txt` 和 `oracle.json`。
- `tests/cases/`
  由提示词、样本和对照结果组成的可复用前向验证用例目录。
- `tests/prompts/`
  最小提示词语料，覆盖显式 skill 请求、多轮跟进、降级压力和模板路线任务。
- `tests/fixtures/dsl/`
  本地 YAML 样本，覆盖 workflow、advanced-chat、rag pipeline 和故意损坏的结构样本。
- `tests/expectations/`
  轻量预期文件，覆盖默认输出顺序、降级措辞和最终结论判定。
- `tests/harness/assert_output.py`
  通用文本断言脚本，用于对捕获输出做 contains / order 检查。
- `README.md`
  面向 GitHub 读者和维护者的英文说明。
- `README.zh-CN.md`
  面向 GitHub 读者和维护者的中文说明。
- `LICENSE`
  仓库许可证文件。

## 维护建议

- 调整审查口径时，优先把细节放进 `references/`，不要持续膨胀 `SKILL.md`
- 修改报告格式或交付判断规则时，注意同步 `references/quality/report-template.md`、`references/quality/review-checklist.md` 和 `references/quality/subagent-review.md`
- 引入新的默认约定时，同时更新 `SKILL.md` 和相关 reference
- 移动 reference 文件或修改交叉链接后，运行 `python3 scripts/quick_validate.py` 或 `python3 scripts/validate_skill_repo.py`
- 用真实样本做快速冒烟时，运行 `python3 scripts/fast_test_dsl.py <sample.yml>`
- 对多个样本做入口覆盖汇总时，运行 `python3 scripts/fast_test_suite.py <sample.yml|directory> [...]`
- 要生成可复用的前向验证用例骨架时，运行 `python3 scripts/init_forward_test_case.py <case-dir> --target <sample.yml>`
- 要校验仓库内的前向验证用例并汇总路线覆盖时，运行 `python3 scripts/check_forward_test_cases.py`
- 要用轻量预期校验捕获输出时，运行 `python3 tests/harness/assert_output.py <expectation.json> <output.txt>`
- 如果要支持新的 agent 平台，优先在 `agents/` 下增加独立适配文件，而不是直接改动核心工作流

## 许可证

当前仓库使用 [MIT License](LICENSE)。
