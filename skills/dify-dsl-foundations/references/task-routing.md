# 任务路由

先用本页决定应该进入哪个入口 skill，不要一上来把所有底座资料都读满。

## 总入口

1. 先读 [common-dsl.md](common-dsl.md)。
2. 读 [orchestration-modes.md](orchestration-modes.md)，先判模式。
3. 判断任务类型：新建、模板起手、只读审核、修复 / 优化 / 重构。
4. 根据任务类型切到对应入口 skill。

## 新建 DSL

适用于从零生成 `workflow`、`advanced-chat` 或 `rag_pipeline`。

- 入口 skill：
  [../../dify-dsl-authoring/SKILL.md](../../dify-dsl-authoring/SKILL.md)
- 需要补读的底座文档：
  [selector-templates.md](selector-templates.md)、[output-fields-catalog.md](output-fields-catalog.md)、[node-io-contracts.md](node-io-contracts.md)
- 需要节点知识时：
  [../../dify-dsl-nodes/SKILL.md](../../dify-dsl-nodes/SKILL.md)

## 模板起手

适用于“先挑模板，再做裁剪、补字段或重排”。

- 入口 skill：
  [../../dify-dsl-authoring/SKILL.md](../../dify-dsl-authoring/SKILL.md)
- 模板底座：
  [../../dify-dsl-templates/SKILL.md](../../dify-dsl-templates/SKILL.md)

## 只读审核或发布判断

适用于不直接改 DSL，只做结构分析、问题分级、交付判断或上线前检查结论。

- 入口 skill：
  [../../dify-dsl-review/SKILL.md](../../dify-dsl-review/SKILL.md)
- 审查与问题分级：
  [../../dify-dsl-quality/SKILL.md](../../dify-dsl-quality/SKILL.md)
- 发布结论、覆盖率与观测字段：
  [../../dify-dsl-governance/SKILL.md](../../dify-dsl-governance/SKILL.md)

## 修复、优化或重构

适用于最小修复、结构优化、成本优化、能力块重构或模板重排。

- 入口 skill：
  [../../dify-dsl-refactor/SKILL.md](../../dify-dsl-refactor/SKILL.md)
- 修复与优化策略：
  [../../dify-dsl-quality/SKILL.md](../../dify-dsl-quality/SKILL.md)
- 节点细节：
  [../../dify-dsl-nodes/SKILL.md](../../dify-dsl-nodes/SKILL.md)
- 模板重排：
  [../../dify-dsl-templates/SKILL.md](../../dify-dsl-templates/SKILL.md)
- 变更影响与上线前检查：
  [../../dify-dsl-governance/SKILL.md](../../dify-dsl-governance/SKILL.md)

## 任务切换规则

- 如果任务目标仍模糊，先回 [../../dify-dsl-brainstorming/SKILL.md](../../dify-dsl-brainstorming/SKILL.md)。
- 同时出现“先生成再审查”时，先完成 authoring，再进入 review。
- 同时出现“先修复再优化”时，先消除阻塞问题，再讨论结构优化。
- 如果问题本质上是模式判断错误，不要在错误模式上继续修字段，先回到 [orchestration-modes.md](orchestration-modes.md) 重判。
