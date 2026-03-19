# 前向验证资料索引

这里是 `dify-dsl-forward-testing` 的 `references/` 入口。

## 推荐读取顺序

1. 先读 [forward-test-playbook.md](forward-test-playbook.md)。
2. 再读 [validation-report-schema.md](validation-report-schema.md)，确认 JSON 报告和 diff 的字段约定。
3. 再根据目标 skill 决定要验证的是路由、模板、审查还是重构。

## 使用约束

- 这里验证的是 skill 协作质量，不是 DSL 业务结果本身。
- 不要把 `oracle.json` 里的预期答案泄漏给被测线程。
- 不要为了通过验证先改 prompt 去“哄对”结果。
