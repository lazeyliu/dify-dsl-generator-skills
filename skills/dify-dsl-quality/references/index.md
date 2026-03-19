# 质量资料索引

这里是 `dify-dsl-quality` 的 `references/` 入口。

这个目录负责“怎么发现问题、怎么修、怎么审、怎么优化”。当任务已经进入结构检查、问题分级、修复策略、提示词质量或链路优化阶段时，从这里继续。

## 推荐读取顺序

1. 修复问题时，先读 [graph-validation-rules.md](graph-validation-rules.md)，必要时先运行 `../scripts/lint_dsl.py`，再读 [fix-strategies.md](fix-strategies.md) 和 [anti-patterns.md](anti-patterns.md)。
2. 只读审核时，先读 [review-checklist.md](review-checklist.md)，再读 [report-template.md](report-template.md)。
3. 需要独立复核分工时，读 [subagent-review.md](subagent-review.md)。
4. 需要问题分级、提示词质量或编排弹性口径时，读 [graded-review-model.md](graded-review-model.md)。
5. 需要优化链路和成本时，读 [mode-constraints.md](mode-constraints.md)、[connectivity-analysis.md](connectivity-analysis.md)、[optimization-playbook.md](optimization-playbook.md)、[tuning-playbook.md](tuning-playbook.md)。

## 按问题选文档

- “这属于硬校验错误还是启发式问题？”
  读 [graph-validation-rules.md](graph-validation-rules.md)。
- “我想先做 deterministic 硬校验，快速找 selector/edge/容器类硬错误。”
  先运行 `../scripts/lint_dsl.py <dsl.yml>`。
- “应该用最小修复还是结构重排？”
  读 [fix-strategies.md](fix-strategies.md)。
- “哪些写法经常把 DSL 搞坏？”
  读 [anti-patterns.md](anti-patterns.md)。
- “审核报告该怎么组织？”
  读 [report-template.md](report-template.md)。
- “审核时到底检查哪些项？”
  读 [review-checklist.md](review-checklist.md)。
- “子代理该怎么分工、何时退化？”
  读 [subagent-review.md](subagent-review.md)。
- “不要只看分工口径，直接帮我组织这轮多方复核。”
  转去 [../../dify-dsl-subagent-review/SKILL.md](../../dify-dsl-subagent-review/SKILL.md)。
- “当前有哪些正式角色文件可以直接拿来派发子代理？”
  读 [../agents/index.md](../agents/index.md)。
- “真实样本的前向验证该怎么写提示词、怎么防止泄漏？”
  转去 [../../dify-dsl-forward-testing/SKILL.md](../../dify-dsl-forward-testing/SKILL.md)。
- “风险怎么分级？提示词和编排质量怎么判？”
  读 [graded-review-model.md](graded-review-model.md)。
- “默认分支、失败输出和决策表怎么审？”
  读 [failure-output-patterns.md](failure-output-patterns.md) 与 [decision-tables.md](decision-tables.md)。
- “如何做结构优化、成本优化和稳定性优化？”
  读 [mode-constraints.md](mode-constraints.md)、[connectivity-analysis.md](connectivity-analysis.md)、[optimization-playbook.md](optimization-playbook.md)、[tuning-playbook.md](tuning-playbook.md)。

## 典型请求

- “这份 DSL 哪些地方会导致导入失败？先按阻塞项、高风险项分级。”
- “不要重写整条链路，先给我最小修复方案。”
- “帮我审提示词、状态污染、失败恢复和默认分支覆盖。”
- “这条链路太贵 / 太脆 / 太绕，帮我做结构优化并说明为什么。”
- “帮我设计一个真实样本的子代理前向验证，不要泄漏预期答案。”

## 使用约束

- 这里负责“发现问题”和“怎么修 / 怎么审”，不替代基础路由与模式判断。
- 如果问题是字段含义、selector 或输出字段目录，先回 [../../dify-dsl-foundations/SKILL.md](../../dify-dsl-foundations/SKILL.md)。
- 如果问题是发布结论、覆盖率、输入输出约定或升级条件，转去 [../../dify-dsl-governance/SKILL.md](../../dify-dsl-governance/SKILL.md)。
