# 节点输入输出契约

生成或调整编排时，不只看字段是否齐全，还要看节点的输入输出契约是否匹配。

## 1. 文本生成节点

常见节点:

- `llm`
- `answer`
- `template-transform`

输入契约:

- 接受文本、模板文本、对话变量、检索结果摘要。

输出契约:

- 主要输出文本，或可直接被模板消费的文本片段。

常见问题:

- 上游传入对象或数组，下游却按纯文本消费。
- `answer` 直接引用了并不存在的文本字段。

## 2. 模型路由与结构化抽取节点

常见节点:

- `parameter-extractor`
- `question-classifier`

输入契约:

- 接受文本、模板文本或可转成文本的上游结果。

输出契约:

- `parameter-extractor` 主要输出结构化参数字段，以及成功/失败辅助字段。
- `question-classifier` 主要输出分类结果字段，例如类别 ID、类别名或对应路由信息。

常见问题:

- 把这两类节点误当成“文本输出节点”来设计下游。
- 下游只按 `text` 消费，忽略真实结构化字段。

## 3. 结构化结果节点

常见节点:

- `code`
- `tool`
- `end`
- `assigner`
- `variable-aggregator`

输入契约:

- 接受变量、对象、数组、工具参数或显式选择器。

输出契约:

- 输出对象、数组或稳定字段集合。

常见问题:

- `code.outputs` 与真实返回值不一致。
- `end.outputs.value_selector` 指向了不存在的字段。

## 4. 检索与知识节点

常见节点:

- `knowledge-retrieval`
- `document-extractor`
- `knowledge-index`
- `datasource`

输入契约:

- 接受查询文本、文件、文档、分块结果。

输出契约:

- 检索片段、抽取文本、分块结果、索引写入输入。

常见问题:

- 文档还没抽取就直接索引。
- `knowledge-index.chunk_structure` 与上游结果结构不匹配。

## 5. 条件与控制节点

常见节点:

- `if-else`
- `question-classifier`
- `iteration`
- `loop`
- `list-operator`

输入契约:

- 需要可判断、可迭代、可比较的数据。

输出契约:

- 输出分支路径、汇总结果、过滤后的列表或容器结果。

常见问题:

- `iteration` 输入不是数组。
- `loop` 无法收敛。
- `if-else` 条件值与变量类型不一致。

## 6. 外部触发与交互节点

常见节点:

- `trigger-webhook`
- `trigger-schedule`
- `trigger-plugin`
- `human-input`
- `http-request`

输入契约:

- 接受事件参数、表单输入、请求参数、外部响应。

输出契约:

- 输出事件载荷、人工表单结果、HTTP 响应字段。

常见问题:

- 入口字段定义与下游消费字段不一致。
- `human-input` 动作恢复路径不完整。

## 契约检查顺序

1. 先判断上游输出类型。
2. 再判断当前节点是否能消费该类型。
3. 再判断当前节点输出是否被下游正确消费。
4. 最后检查空值、失败值、默认值是否会破坏链路。
