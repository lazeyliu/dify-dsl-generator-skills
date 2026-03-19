# Dify DSL 公共结构

## 顶层骨架

需要同时区分三层口径:

- 当前导出标准: 以当前 Dify 导出实现为准。
- 历史 fixture 形状: 本地样例中仍可能保留旧版本结构。
- 编辑器字段: 为画布和导入体验服务，不等于运行时硬约束。

建议区分两套顶层 DSL:

- `kind: app`
- `kind: rag_pipeline`

### App DSL

```yaml
app:
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  mode: workflow | advanced-chat
  name: your_app_name
  use_icon_as_answer_icon: false
dependencies: []
kind: app
version: 0.6.0
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes: []
    edges: []
```

### RAG Pipeline DSL

```yaml
dependencies: []
kind: rag_pipeline
rag_pipeline:
  description: ""
  icon: "📙"
  icon_background: ""
  icon_type: emoji
  name: your_pipeline_name
version: 0.1.0
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes: []
    edges: []
```

## 节点公共字段

所有节点 `data` 共享这些字段:

- `type`: 节点类型，必填。
- `title`: 标题，建议始终显式写。
- `desc`: 描述，可空。
- `version`: 默认 `"1"`，仅在特殊节点需要版本切换时显式设置。
- `error_strategy`: 可选，典型值是 `fail-branch` 或 `default-value`。
- `default_value`: 可选，失败兜底值。
- `retry_config`: 可选，常见字段是 `max_retries`、`retry_interval`、`retry_enabled`。

## 节点外层包装

运行时核心关注:

- `id`
- `data`

fixture 或编辑器里常见，但不应默认抬成硬约束的字段:

- `type`
- `position.x`
- `position.y`
- `width`
- `height`
- `positionAbsolute`
- `selected`
- `sourcePosition`
- `targetPosition`
- `parentId`
- `zIndex`

新建 DSL 时可以保留导入和阅读需要的包装字段，但不要把这些编辑器字段误当成源码运行时硬要求。

## 边结构

运行时核心关注:

- `source`
- `sourceHandle`
- `target`

编辑器或样例里常见的字段:

- `id`
- `targetHandle`
- `data.sourceType`
- `data.targetType`
- `isInLoop`
- `isInIteration`

其中 `targetHandle` 更偏编辑器兼容字段；当前后端构图并不依赖它。

## 生成原则

1. 先定 `kind` 与模式，再定节点。
2. 先定节点 `id`，再写变量选择器。
3. 所有 `value_selector` / `variable_selector` / `query_variable_selector` 都必须引用已存在节点或变量域。
4. 容器节点必须先定义 `start_node_id`，再放内部起点节点。
5. `workflow` 模式优先收敛到 `end`；`advanced-chat` 优先收敛到 `answer`。
6. `rag-pipeline` 要额外检查 `rag_pipeline_variables` 与 `knowledge-index` 的衔接。
7. `start` 与 `trigger-*` 不要共存。

## 字段书写要求

每个节点文档都要同时给出:

- 必填字段
- 选填字段
- 贯通性分析

这里的“选填字段”不是装饰性罗列，而是要说明哪些字段在特定场景下建议补齐。

## 兼容性提醒

不同导出形态并不总是完全一致，常见差异:

- `retry_config` 常见 `enabled` 与 `retry_enabled` 两种写法。
- `tool_parameters`、`datasource_parameters` 有时会出现简写字符串写法，也有对象写法。
- 节点 `data` 允许 `extra=allow`，所以导出 DSL 常混入历史字段。
- 本地很多 app fixture 仍使用历史 `0.3.1` 形态，而当前 app DSL 导出版本已是 `0.6.0`。

结论:

- 新生成 DSL 优先写稳定、清晰的字段结构。
- 如果要模仿现有导出样例，必须在报告里标记为“兼容写法”。
