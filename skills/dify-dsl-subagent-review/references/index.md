# 子代理复核编排索引

这里是 `dify-dsl-subagent-review` 的 `references/` 入口。

这个 skill 自身不重新发明角色和复核口径，而是把现有质量体系中的子代理复核规则固定成一个可直接调用的编排入口。

## 推荐读取顺序

1. 先读 [mode-selection-matrix.md](mode-selection-matrix.md)
2. 再读 [orchestration-playbook.md](orchestration-playbook.md)
3. 再读 [../../dify-dsl-quality/references/subagent-review.md](../../dify-dsl-quality/references/subagent-review.md)
4. 再读 [../../dify-dsl-quality/agents/index.md](../../dify-dsl-quality/agents/index.md)
5. 如果当前任务需要最终门禁归并，再补 [../../dify-dsl-governance/references/evaluation-gates.md](../../dify-dsl-governance/references/evaluation-gates.md)

## 适用问题

- “这份 DSL 我想让 3 个只读子代理分别复核，再统一结论。”
- “我需要多方复核，但平台或授权可能不允许，帮我按规则退化。”
- “我已经有几方复核结果了，帮我判断是否需要启用上线检查复核器做冲突归并。”

## 不适用问题

- “我还不知道该走 authoring / review / refactor 哪条路。”
- “请直接帮我生成 DSL。”
- “请直接重构 DSL，不要复核。”
