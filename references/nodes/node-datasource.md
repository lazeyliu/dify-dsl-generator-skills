# datasource 节点

## 作用

作为 RAG Pipeline 或文档流程的数据源入口。

`datasource-empty` 更像占位节点，不建议把它当成手写 DSL 的真实业务节点。

## 必填字段

- `type: datasource`: 指定当前节点是数据源入口。
- `plugin_id`: 指定具体数据源提供方或插件标识。
- `provider_name`: 提供方名称，用于识别数据源来源。
- `provider_type`: 数据源分类，例如本地文件、在线文档或站点抓取。

## 选填字段

- `datasource_name`: 需要区分同类数据源时填写。
- `datasource_configurations`: 需要额外配置数据源行为时填写。
- `plugin_unique_identifier`: 数据源来自插件实例时填写。
- `datasource_parameters`: 数据源需要动态输入参数时填写。

## 贯通性分析

- 它通常是 `rag_pipeline` 的入口，不依赖普通 `start`。
- 下游常接 `document-extractor`、`if-else`、`tool`、`knowledge-index`。
- 关键是数据源产出类型必须能被下游文档抽取、转换或索引节点消费。

## 可承接上游节点

### 推荐

- 无，`datasource` 本身通常就是 `rag_pipeline` 入口。

### 可用但需人工确认

- 无。

### 不推荐

- `start`
- 任意 `trigger-*`
- 其他普通业务节点

## 可衔接下游节点

### 推荐

- `document-extractor`
- `if-else`
- `tool`

### 可用但需人工确认

- `knowledge-index`
- `variable-aggregator`

### 不推荐

- `answer`
- `start`
- 任意 `trigger-*`

## 编排约束

- 通常与 `document-extractor` 或 `knowledge-index` 搭配。
- 如果数据源来自插件，建议同时保留 `plugin_unique_identifier`。
- `datasource_parameters` 的值类型要与实体约束匹配。

## 最小骨架

```yaml
data:
  title: Data Source
  type: datasource
  plugin_id: langgenius/file
  provider_name: file
  provider_type: local_file
  datasource_name: upload-file
```
