# tool 节点

## 作用

调用 Dify 工具或插件工具。

## 必填字段

- `type: tool`: 指定当前节点是工具调用节点。
- `provider_id`: 工具提供方标识，用于定位工具来源。
- `provider_type`: 提供方类型，用于区分内置或插件来源。
- `provider_name`: 提供方展示名，便于识别具体来源。
- `tool_name`: 工具内部名称，决定实际调用哪个工具。
- `tool_label`: 工具展示名，便于画布识别。
- `tool_configurations`: 工具配置项，控制工具运行方式。
- `tool_parameters`: 工具入参映射，没有它通常无法完成实际调用。

## 选填字段

- `credential_id`: 工具需要绑定凭证时填写。
- `plugin_unique_identifier`: 工具来自插件市场或插件实例时填写。
- `tool_node_version`: 当前推荐显式写，通常为 `"2"`；旧 DSL 缺失该字段时，编辑器和运行时可能进入兼容解析路径。

## 贯通性分析

- 上游通常提供工具参数、文件、文本或结构化对象。
- 下游常接 `end`、`llm`、`code`、`knowledge-index`。
- 关键是动态参数 schema 与当前传入值类型一致，下游也要知道消费哪个工具输出字段。

## 可承接上游节点

### 推荐

- `start`
- `http-request`
- `template-transform`
- `assigner`
- `document-extractor`

### 可用但需人工确认

- `llm`
- `code`
- `knowledge-retrieval`
- `human-input`

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `end`
- `llm`
- `code`
- `knowledge-index`
- `variable-aggregator`
- `if-else`

### 可用但需人工确认

- `answer`
- `assigner`
- `template-transform`
- `human-input`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 兼容性提醒

- `tool_parameters.<name> = { type, value }` 是更清晰的结构。
- 也可能直接写成 `tool_parameters.json_string: "{{#http.body#}}"` 这种简写。
- 生成新 DSL 时优先显式对象写法；如果跟随旧样例，报告里标记为兼容写法。

## 最小骨架

```yaml
data:
  title: Tool
  type: tool
  tool_node_version: "2"
  provider_id: builtin
  provider_type: builtin
  provider_name: Builtin Tools
  tool_name: json_parse
  tool_label: JSON Parse
  tool_configurations: {}
  tool_parameters:
    json_string:
      type: mixed
      value: "{{#http_node.body#}}"
```
