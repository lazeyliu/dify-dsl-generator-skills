# 交付判断目录索引

这是 `references/governance/` 的正式入口页。

这个目录负责“是否可以交付、证据是否充分、约定是否完整、观测字段是否够用”。当任务已经不只是“能不能跑”，而是要回答“能不能宣称可直接导入、如何通过上线前检查、还缺什么交付证据”时，从这里继续。

## 推荐读取顺序

1. 需要做发布判断时，先读 [evaluation-gates.md](evaluation-gates.md)。
2. 修改既有 DSL 时，读 [change-impact-review.md](change-impact-review.md)。
3. 需要说明覆盖率、是否已经够用和升级条件时，读 [coverage-matrix.md](coverage-matrix.md)、[minimal-sufficiency.md](minimal-sufficiency.md)、[escalation-policies.md](escalation-policies.md)。
4. 需要说明观测字段、能力块边界和输入输出约定时，读 [observability-contract.md](observability-contract.md) 与 [capability-contracts.md](capability-contracts.md)。
5. 需要稳定问题编码时，读 [issue-taxonomy.md](issue-taxonomy.md)。

## 按问题选文档

- “现在能不能说可直接导入？”
  读 [evaluation-gates.md](evaluation-gates.md)。
- “这次改动影响了哪些节点、selector、变量或 fallback？”
  读 [change-impact-review.md](change-impact-review.md)。
- “主路径、fallback 和异常路径的覆盖率怎么表达？”
  读 [coverage-matrix.md](coverage-matrix.md)。
- “当前结构是过重、合理还是过轻？”
  读 [minimal-sufficiency.md](minimal-sufficiency.md)。
- “证据缺失或高风险动作何时必须升级？”
  读 [escalation-policies.md](escalation-policies.md)。
- “关键决策节点最少该带哪些观测字段？”
  读 [observability-contract.md](observability-contract.md)。
- “能力块该怎么声明输入、输出、副作用和失败语义？”
  读 [capability-contracts.md](capability-contracts.md)。
- “问题编码怎么保持稳定？”
  读 [issue-taxonomy.md](issue-taxonomy.md)。

## 典型请求

- “现在这份 DSL 能不能宣称可直接导入？缺的证据是什么？”
- “这次改动对节点、selector、输出约定和 fallback 的影响面有多大？”
- “覆盖率矩阵、是否已经够用和升级条件该怎么写，哪些项还没过？”
- “关键决策节点最少需要哪些观测字段和能力块边界约定？”

## 使用约束

- 交付判断不能替代质量检查；没有结构检查和实体校验，不应只靠上线前检查表下结论。
- 如果问题还是“字段对不对、链路闭不闭、提示词合不合理”，先回 `references/quality/`。
- 如果只是路由和模式判断不清，先回 `references/foundations/`。
