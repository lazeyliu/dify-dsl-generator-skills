# 节点目录索引

这里是 `references/nodes/` 的入口。

适用方式：

- 新建 DSL：先在这里确定会用到哪些节点，再按需进入对应节点文档。
- 修复现有 DSL：只打开报错节点、上下游节点和相关容器节点，不要把整目录读满。
- 审核或重构：优先结合模式判断与链路骨架，按类别缩小要读的节点集合。

统一口径：

- 实体级字段：当前源码实体显式声明的字段。
- fixture 常见字段：本地样例中经常出现，但不一定是实体硬字段。
- 兼容字段：历史 DSL 或导出噪声中可能出现，审查时不能仅凭它们判错。

生成新 DSL 时，优先遵循“实体级字段 + 当前推荐写法”。
审核现有 DSL 时，要接受 fixture 常见字段和兼容字段的存在。

## 基础输出节点

- `start`: [node-start.md](node-start.md)
- `answer`: [node-answer.md](node-answer.md)
- `end`: [node-end.md](node-end.md)

## 模型与推理节点

- `llm`: [node-llm.md](node-llm.md)
- `agent`: [node-agent.md](node-agent.md)
- `parameter-extractor`: [node-parameter-extractor.md](node-parameter-extractor.md)
- `question-classifier`: [node-question-classifier.md](node-question-classifier.md)

## 条件、容器与变量节点

- `if-else`: [node-if-else.md](node-if-else.md)
- `iteration` / `iteration-start`: [node-iteration.md](node-iteration.md)
- `loop` / `loop-start` / `loop-end`: [node-loop.md](node-loop.md)
- `variable-aggregator`: [node-variable-aggregator.md](node-variable-aggregator.md)
- `assigner` 与旧版 `variable-assigner`: [node-variable-assigner.md](node-variable-assigner.md)
- `list-operator`: [node-list-operator.md](node-list-operator.md)

## 执行与转换节点

- `code`: [node-code.md](node-code.md)
- `template-transform`: [node-template-transform.md](node-template-transform.md)
- `http-request`: [node-http-request.md](node-http-request.md)
- `tool`: [node-tool.md](node-tool.md)
- `document-extractor`: [node-document-extractor.md](node-document-extractor.md)

## 知识与数据源节点

- `knowledge-retrieval`: [node-knowledge-retrieval.md](node-knowledge-retrieval.md)
- `knowledge-index`: [node-knowledge-index.md](node-knowledge-index.md)
- `datasource`: [node-datasource.md](node-datasource.md)

## 人工与触发器节点

- `human-input`: [node-human-input.md](node-human-input.md)
- `trigger-plugin`: [node-trigger-plugin.md](node-trigger-plugin.md)
- `trigger-schedule`: [node-trigger-schedule.md](node-trigger-schedule.md)
- `trigger-webhook`: [node-trigger-webhook.md](node-trigger-webhook.md)

## 建议读取顺序

- 简单 chatflow: `start` -> `llm` -> `answer`
- 普通 workflow: `start` -> 执行节点 -> `end`
- 带分支: 加载 `if-else` 或 `question-classifier`
- 带循环: 加载 `iteration` 或 `loop`
- 带 RAG Pipeline: 优先加载 `datasource`、`document-extractor` / `tool`、`knowledge-index`
- 带知识库问答: 优先加载 `knowledge-retrieval`、`llm`、`answer`
- 带人工审批: 加载 `human-input`
- 带外部事件: 加载三个 `trigger-*` 节点

## 典型请求

- “`if-else` 节点到底需要哪些字段？默认分支怎么配才不漂？”
- “`iteration` / `loop` 为什么老是闭不起来？容器内部起点和输出选择器该怎么写？”
- “给我一个最小的 `start -> llm -> answer` 或 `start -> code -> end` 节点组合。”
- “`tool`、`http-request`、`template-transform` 三种节点在这条链路里该怎么选？”
