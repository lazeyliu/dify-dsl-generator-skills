# 模式约束矩阵

不同编排模式下，节点组合不是完全自由的。

## workflow

必须满足:

- 入口通常是 `start`
- 至少一个 `end`
- 输出字段能从上游真实追溯

推荐:

- `start -> 处理节点 -> end`

不推荐:

- 没有 `end`
- 只有中间节点，没有终点

## advanced-chat

必须满足:

- 入口通常是 `start`
- 至少一个 `answer` 或明确解释为何只用 `end`

推荐:

- `start -> llm -> answer`

不推荐:

- 复杂 workflow 终点全靠 `end`，却不返回对话文本

## rag-pipeline

必须满足:

- `kind: rag_pipeline`
- 有 `rag_pipeline` 顶层块
- 至少一条主路径到 `knowledge-index` 或用户定义终点

推荐:

- `datasource -> document-extractor/tool -> variable-aggregator -> knowledge-index`

不推荐:

- 普通 `start` 和 `datasource` 混成双入口

## trigger 模式

必须满足:

- 入口是某个 `trigger-*`
- 默认不再并列 `start`

推荐:

- `trigger-* -> 业务节点 -> end`

不推荐:

- 多个触发器无说明地并列存在

## 容器模式

必须满足:

- 容器本体和内部起点节点成套存在
- 容器输出能被外部消费

推荐:

- `数组来源 -> iteration -> 汇总节点`
- `初始变量 -> loop -> end`

不推荐:

- 容器内没有真实处理节点
