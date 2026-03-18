# 样例索引

这些样例名适合拿来对照 DSL 结构。

如果当前仓库中没有附带对应样例文件，应把它们视为“样例索引名称”而不是“本地可直接打开的 fixture 文件”。

## 推荐样例

- `basic_chatflow.yml`
  适合看 `start`、`llm`、`answer` 的最小闭环。

- `conditional_parallel_code_execution_workflow.yml`
  适合看 `if-else`、多分支 `code`、`end` 聚合。

- `http_request_with_json_tool_workflow.yml`
  适合看 `http-request`、`tool`、`end` 串接，也能看到兼容写法。

- `increment_loop_with_break_condition_workflow.yml`
  适合看 `loop`、`loop-start`、`assigner`、`end`。

- `update-conversation-variable-in-iteration.yml`
  适合看 `iteration`、`iteration-start`、`assigner`、对话变量更新。

- `conditional_streaming_vs_template_workflow.yml`
  适合看输出路径与模板类节点组合。

- `chatflow_time_tool_static_output_workflow.yml`
  适合看 chatflow 中 `tool` 与 `answer` 的组合。

- `file-general-economy.yml`
  适合看 `kind: rag_pipeline`、`datasource`、`document-extractor`、`tool`、`knowledge-index` 的基础链路。

- `file-general-high-quality.yml`
  适合看高质量索引下的 `knowledge-index` 字段组合。

- `notion-general-high-quality.yml`
  适合看在线文档数据源变体。

- `website-crawl-general-high-quality.yml`
  适合看站点抓取型数据源变体。

## 使用原则

- 样例优先用来观察“形状”和“连边”。
- 必填字段判断优先看稳定字段定义，不优先看样例。
- 样例出现但未确认的字段，放到报告的“兼容字段”栏目，不要直接当硬约束。
- `kind: app` 与 `kind: rag_pipeline` 的样例不要混看成同一顶层 DSL。
