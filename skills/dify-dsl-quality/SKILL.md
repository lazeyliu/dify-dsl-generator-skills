---
name: dify-dsl-quality
description: Dify DSL 质量技能。用于问题发现、问题分级、修复策略、优化策略、子代理复核分工和审查报告组织；当任务进入审查、修复或优化阶段时使用。
---

# dify-dsl-quality

负责“怎么发现问题、怎么修、怎么审、怎么做独立复核”，不负责模式判断和最终发布门禁。

## 入口

先读 [references/index.md](references/index.md)。需要角色分工时，再读 [agents/index.md](agents/index.md)。

如果需要 deterministic 硬校验，优先运行 `scripts/lint_dsl.py`，先把 selector、edge、模式终点、容器起点和关键节点字段的明显错误筛出来，再进入更细的审查或修复策略。

## 路由边界

- 如果还没完成模式判断和基础字段口径收敛，先回 [../dify-dsl-foundations/SKILL.md](../dify-dsl-foundations/SKILL.md)
- 如果问题已经变成发布结论、覆盖率或观测字段，转去 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)
- 如果需要真实样本前向验证，转去 [../dify-dsl-forward-testing/SKILL.md](../dify-dsl-forward-testing/SKILL.md)
