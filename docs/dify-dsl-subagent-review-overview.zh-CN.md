# Dify DSL 子代理复核总览

这页只回答四个问题：

1. 什么时候该用 `dify-dsl-subagent-review`
2. 它和 `review / governance / authoring / refactor` 的边界是什么
3. 它到底有哪几种复核模式
4. 仓库里已经有哪些样本在验证这些模式

## 一句话定位

`dify-dsl-subagent-review` 不是新的“主业务 skill”，而是一个**复核编排 skill**。

它负责：

- 组织多方只读复核
- 决定走并行、串行、单子代理还是无子代理退化
- 在需要时把 review 侧和 governance 侧的结论做冲突归并

它不负责：

- 第一次路由
- 直接生成 DSL
- 直接修改 DSL
- 替代 `authoring / review / refactor / governance` 的主任务判断

## 一屏主路径

<!-- BEGIN ROUTE_MATRIX -->
| 用户目标 | 推荐入口 | 常见下一步 |
| --- | --- | --- |
| 需求还没收敛 | `using-dify-dsl` 或 `dify-dsl-brainstorming` | `dify-dsl-authoring / review / refactor` |
| 新建 DSL | `using-dify-dsl` 或 `dify-dsl-authoring` | 高复杂度时进入 `dify-dsl-subagent-review` |
| 只读审查已有 DSL | `using-dify-dsl` 或 `dify-dsl-review` | 需要多方复核时进入 `dify-dsl-subagent-review` |
| 修改已有 DSL | `using-dify-dsl` 或 `dify-dsl-refactor` | 修改后需要独立复核时进入 `dify-dsl-subagent-review` |
| 只想选模板 | `using-dify-dsl` 或 `dify-dsl-templates` | 如需正文再进入 `dify-dsl-authoring` |
| 只想判断能不能交付 | `using-dify-dsl` 或 `dify-dsl-governance` | 如果用户同时明确要求多方独立复核或冲突归并，再进入 `dify-dsl-subagent-review` |
| 明确要组织多方复核 | `using-dify-dsl` 或 `dify-dsl-subagent-review` | 按并行 / 串行 / 单子代理 / 无子代理退化 |
<!-- END ROUTE_MATRIX -->

可以把这条线理解成：

<!-- BEGIN MAIN_PATH -->
```text
using-dify-dsl
-> brainstorming / authoring / review / refactor / templates / governance / subagent-review
-> 必要时再进入 subagent-review 或 governance
```
<!-- END MAIN_PATH -->

## 什么时候用

适合：

- 已经有 DSL 草稿或已有 DSL
- 用户明确要求多方独立复核
- 你需要把字段、链路、提示词、门禁拆开看
- 你已经预期 review 结论和 governance 结论可能冲突
- 你需要在“有子代理 / 没子代理授权”之间稳定退化

不适合：

- 需求还没收敛
- 还没决定该走 `authoring / review / refactor`
- 只是想做一次普通只读审查
- 只是想直接重构，不关心复核流程

## 和其它 skill 的关系

- `using-dify-dsl`
  负责总入口路由；如果用户明确要“组织多方复核”，它会把任务转到这里。
- `dify-dsl-authoring`
  先生成草稿；高复杂度或高风险草稿建议下一步转到这里做复核。
- `dify-dsl-review`
  适合单线程只读审查；如果复杂度上升到需要正式多方复核，再转到这里。
- `dify-dsl-refactor`
  先修改；修改后如果需要独立复核，再转到这里。
- `dify-dsl-governance`
  负责最终门禁与交付判断；如果用户同时明确要求多方独立复核或冲突归并，再先由这里组织复核。

## 四种复核模式

### 1. 异步并行

适用：

- 同时涉及字段、链路、提示词、门禁多个面向
- 样本复杂度较高
- 目标就是尽快拿到多方意见

默认角色：

- 字段约束复核器
- 链路闭环复核器
- 提示词与输入输出约定复核器

按需追加：

- 上线检查复核器

### 2. 同步串行

适用：

- 必须先确认结构或字段是否成立，后面的判断才有意义
- 后续结论明显依赖前一轮结果
- 样本不大，但检查之间有强前后依赖

典型顺序：

1. 结构 / 字段
2. 提示词与输入输出约定
3. 按需门禁归并

### 3. 单子代理

适用：

- 风险面很窄
- 主要问题集中在一个角色范围里
- 多方复核只会重复同一个结论

典型样本：

- `broken-selector.yml`

### 4. 无子代理

适用：

- 平台不支持子代理
- 当前会话策略不允许
- 用户明确禁止

这时必须：

- 执行完整自检
- 明确写出 `未做独立复核`
- 把结论至少提升到 `需要人工确认`

## 当前角色集合

- `字段约束复核器`
- `链路闭环复核器`
- `提示词与输入输出约定复核器`
- `上线检查复核器`

其中前三个负责拿原始意见，最后一个只在“需要仲裁 / 需要门禁归并”时启用。

## 当前样本覆盖

### 理想路径

- `orchestrate-readonly-review`
- `merge-release-readiness`

### 退化路径

- `degrade-no-subagent`

### 冲突仲裁

- `merge-rag-review-vs-governance`
- `merge-chat-review-vs-governance`

### 模式选择

- `select-serial-chat-review`
- `select-single-graph-review`

### 上游接入

- `route-to-subagent-review`
- `route-full-lifecycle-rag`
- `knowledge-retrieval-authoring-needs-review`
- `refactor-retrieval-topk-needs-review`

## 推荐理解顺序

如果你是第一次看这套设计，按这个顺序读：

1. [using-dify-dsl](../skills/using-dify-dsl/SKILL.md)
2. [dify-dsl-subagent-review](../skills/dify-dsl-subagent-review/SKILL.md)
3. [mode-selection-matrix](../skills/dify-dsl-subagent-review/references/mode-selection-matrix.md)
4. [orchestration-playbook](../skills/dify-dsl-subagent-review/references/orchestration-playbook.md)
5. [subagent-review](../skills/dify-dsl-quality/references/subagent-review.md)

## 当前结论

到现在为止，这套子代理复核能力已经不是“概念上的增强建议”，而是：

- 有独立 skill
- 有模式决策表
- 有编排手册
- 有退化规则
- 有冲突仲裁路径
- 有上游 skill 接入点
- 有前向验证样本覆盖
