---
name: dify-dsl-subagent-review
description: 当 Dify Workflow、Chatflow、RAG Pipeline DSL 任务已经进入生成后复核、只读审查、修复后复核或交付判断阶段，并且需要多方独立复核、冲突归并或按授权退化时使用。
---

# dify-dsl-subagent-review

这是 Dify DSL 的子代理复核编排 skill。

它不负责第一次路由，不替代 `authoring / review / refactor / governance` 的主任务判断；它只负责把“独立复核怎么组织、何时退化、何时做冲突归并”稳定下来。

## 进入条件

- 主任务已经明确属于生成后复核、只读审查、修复后复核或交付判断。
- 当前任务目标已经不是“先判断该走哪个入口 skill”。
- 用户明确要求多方独立复核，或当前任务复杂度已经高到需要多方复核才能提高结论可信度。

如果这些条件不成立，先回对应主 skill：

- 需求仍模糊：回 [../dify-dsl-brainstorming/SKILL.md](../dify-dsl-brainstorming/SKILL.md)
- 新建 DSL：回 [../dify-dsl-authoring/SKILL.md](../dify-dsl-authoring/SKILL.md)
- 只读审查：回 [../dify-dsl-review/SKILL.md](../dify-dsl-review/SKILL.md)
- 修复 / 重构：回 [../dify-dsl-refactor/SKILL.md](../dify-dsl-refactor/SKILL.md)
- 单独交付判断：回 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)

## 协作顺序

1. 先读 [references/index.md](references/index.md)。
2. 先按 [references/mode-selection-matrix.md](references/mode-selection-matrix.md) 选择本轮复核模式。
3. 需要正式角色定义时，读 [../dify-dsl-quality/agents/index.md](../dify-dsl-quality/agents/index.md)。
4. 如果选的是 `异步并行`，默认优先组织 3 个只读复核器并行复核：
   - `字段约束复核器`
   - `链路闭环复核器`
   - `提示词与输入输出约定复核器`
5. 如果选的是 `同步串行`，按“结构 / 字段 -> 提示词与输入输出约定 -> 按需门禁归并”的顺序推进。
6. 只有在前三方结论冲突，或当前任务已经明确带有发布门禁 / 覆盖率 / 观测字段归并目标时，才启用 `上线检查复核器`。
7. 如果平台、会话或用户授权不允许自动拉起 3 个子代理，按 `3 -> 1 -> 0` 顺序退化。

## 复核模式

- `异步并行`
  默认模式。适合字段、图结构、提示词与风险结论可相对独立检查的场景。
- `同步串行`
  适合后一轮判断明显依赖前一轮结论，例如先确认结构闭环，再审提示词与交付风险。
- `单子代理`
  适合风险面很窄、样本很小或当前环境不适合多方复核的情况。
- `无子代理`
  仅在当前平台没有子代理能力，或授权不允许时使用。必须明确标记“未做独立复核”，并提高风险等级。

## 最低输出

1. 当前主任务类别
2. 本轮复核模式
3. 选择该模式的原因，以及为什么不是最接近的另外 1 到 2 个模式
4. 实际启用的复核角色数量和名称
5. 每个角色的主要问题摘要
6. 冲突点与仲裁结果（如果有）
7. 最终统一结论
8. 剩余风险与退化说明

## 约束

- 不要让复核子代理修改文件。
- 不要把所有检查项塞给一个“万能子代理”再假装完成多方复核。
- 不要在前三方结论还没形成时就提前用 `上线检查复核器` 代替全流程。
- 如果当前环境没有子代理能力，不要伪装成“已独立复核通过”。
- 对 authoring 场景，它只负责“草稿后的复核”，不负责替代 authoring 本身去写 DSL。
