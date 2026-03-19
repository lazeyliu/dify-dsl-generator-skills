---
name: dify-dsl-governance
description: Dify DSL 交付判断技能。用于发布结论、变更影响、覆盖率、升级条件、观测字段和能力块约定；当任务已经不只是“能不能跑”，而是要回答“能不能交付”时使用。
---

# dify-dsl-governance

只负责交付判断，不替代质量检查。

## 入口

先读 [references/index.md](references/index.md)，按需进入 `evaluation-gates / change-impact-review / coverage-matrix / observability-contract / capability-contracts`。

如果当前还没有多方复核结果，但用户明确要求由子代理复核后再统一发布结论，先转去 [../dify-dsl-subagent-review/SKILL.md](../dify-dsl-subagent-review/SKILL.md)。

## 约束

- 如果还没有结构检查、字段检查和风险分级，不要单独拿这里下结论。
- 如果问题还是“字段对不对、链路闭不闭、提示词合不合理”，先回 [../dify-dsl-quality/SKILL.md](../dify-dsl-quality/SKILL.md)。
