---
name: using-dify-dsl
description: 在开始处理 Dify Workflow、Chatflow、RAG Pipeline DSL 相关任务时使用。用于识别用户意图、判断权限边界，并把请求路由到 dify-dsl-brainstorming、dify-dsl-authoring、dify-dsl-review、dify-dsl-refactor、dify-dsl-templates、dify-dsl-governance 或 dify-dsl-subagent-review。
---

# using-dify-dsl

这是整个 Dify DSL 技能包的总入口。

它只负责意图判断、权限边界判断、主 skill 路由和最小上下文收敛，不替代下游 skill 的具体专业判断。

## 先做什么

1. 先判断这是不是 Dify DSL 任务，或与 `workflow`、`advanced-chat`、`rag_pipeline` 直接相关的模板、审查、修复、交付判断任务。
2. 明确当前任务属于“需求仍模糊 / 新建 DSL / 只读审查 / 修复重构 / 模板选型 / 交付判断”中的哪一类。
2.1 如果用户明确要求多方独立复核、子代理复核编排或冲突归并，单独识别这一类需求。
3. 明确权限边界：只读还是允许修改；输出文本草稿还是允许直接落盘。
4. 只选择一个主 skill 进入；如果需要，再说明随后会联动哪些底座 skill。
5. 如果目标不清、权限不清、或多个意图冲突，优先转去 `dify-dsl-brainstorming`，不要硬判。
6. 如果确认当前任务根本不是 Dify DSL 任务，明确说明“不进入本技能包”，并停止向下游 skill 路由。

## 主路由规则

- 需求仍模糊、未知项多、目标互相冲突：
  进入 [../dify-dsl-brainstorming/SKILL.md](../dify-dsl-brainstorming/SKILL.md)
- 目标明确，要新建 DSL、从模板起手、或先输出 DSL 草稿：
  进入 [../dify-dsl-authoring/SKILL.md](../dify-dsl-authoring/SKILL.md)
- 已有 DSL 只做只读分析、风险分级、导入判断、发布结论：
  进入 [../dify-dsl-review/SKILL.md](../dify-dsl-review/SKILL.md)
- 已有 DSL 需要最小修复、结构优化、模板重排或直接修改：
  进入 [../dify-dsl-refactor/SKILL.md](../dify-dsl-refactor/SKILL.md)
- 用户明确只问“该选哪套模板 / 哪个骨架”，暂不进入正文：
  进入 [../dify-dsl-templates/SKILL.md](../dify-dsl-templates/SKILL.md)
- 用户明确只问“能不能交付 / 上线 / 发布”，且当前问题已经不是字段或结构排错：
  进入 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)
- 用户明确要求多方独立复核、子代理复核编排或复核冲突归并：
  进入 [../dify-dsl-subagent-review/SKILL.md](../dify-dsl-subagent-review/SKILL.md)
- 当前任务与 Dify DSL 无关：
  不进入本技能包，也不要强行贴到任何 `dify-dsl-*` skill 上。

## 判断细则

- 不要把“给我方案”误判成“允许改文件”。
- 不要把“帮我看看哪里错”误判成“直接重构”。
- 不要把“能不能导入 staging”误判成修复授权。
- 如果用户同时要“先判断问题，再直接改”，而且修改授权明确，优先进入 `dify-dsl-refactor`；如果修改授权不明确，先进入 `dify-dsl-review` 或 `dify-dsl-brainstorming`。
- 如果用户已经明确点名某个下游 skill，服从用户指定，不要重复路由。
- 如果当前已经进入某个下游 skill，只有在目标变化或路由明显错误时才回到本 skill。
- 如果用户显式指定了只读边界，不要因为你看见了可修复问题就擅自切到 `dify-dsl-refactor`。

## 最低输出

1. 当前任务分类
2. 权限边界
3. 主路由
4. 为什么不是最接近的另外 1 到 2 个 skill
5. 接下来预期会联动哪些底座 skill

如果不属于 Dify DSL 任务：

1. 明确说明“不进入本技能包”
2. 说明原因
3. 不再继续路由到任何下游 skill

## 约束

- 不要把所有 skill 一次性全读满。
- 不要在还没完成路由前直接给出大段 DSL 正文。
- 不要把“总入口”写成“大一统 skill”；细节仍应交给下游 skill 处理。
- 不要把普通编程、文档整理或通用问答任务误吸进本技能包。
