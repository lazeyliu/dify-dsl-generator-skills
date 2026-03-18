# document-extractor 节点

## 作用

从文件或文档变量中抽取文本。

## 必填字段

- `type: document-extractor`: 指定当前节点是文档抽取节点。
- `variable_selector`: 指定要抽取的文件或文档变量来源。

## 选填字段

- `title`: 需要在画布上清晰区分用途时填写。
- `desc`: 需要解释抽取目的时填写。
- `version`: 需要固定兼容写法时填写。
- `retry_config`: 抽取步骤可能失败且允许重试时填写。

## 贯通性分析

- 上游通常接文件输入、`datasource` 或文件型变量。
- 下游常接 `variable-aggregator`、`tool`、`knowledge-index`、`llm`。
- 关键是确认它输出的是文本/文档结构，而不是原始文件句柄。

## 可承接上游节点

### 推荐

- `datasource`

### 可用但需人工确认

- `start`
- `tool`
- 其他能提供文件型变量的节点

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `variable-aggregator`
- `tool`
- `knowledge-index`

### 可用但需人工确认

- `llm`
- `code`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `variable_selector` 必须指向文件或文档类型输入。
- 在 RAG 或文件处理流程里常作为 `datasource`、上传输入后的早期节点。

## 最小骨架

```yaml
data:
  title: Document Extractor
  type: document-extractor
  variable_selector: [start, file]
```
