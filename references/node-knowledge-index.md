# knowledge-index 节点

## 作用

把上游分块结果写入知识库索引。

## 必填字段

- `type: knowledge-index`: 指定当前节点是知识索引写入节点。
- `chunk_structure`: 指定上游块结构类型，必须与输入结果匹配。
- `index_chunk_variable_selector`: 指向要写入索引的块结果来源。

## 核心字段与扩展字段

当前节点实体明确声明的核心字段是:

- `type`
- `chunk_structure`
- `index_chunk_variable_selector`
- `indexing_technique`
- `summary_index_setting`

常见但应视为扩展/兼容字段的有:

- `retrieval_model`
- `embedding_model`
- `embedding_model_provider`
- `keyword_number`

其中后几类字段经常出现在本地 transform fixture 中，但不应和实体级字段混写成同一层“硬必填”。

`chunk_structure` 常见值说明:

- `text_model`: 普通文本块结构，适合一般文档切分。
- `hierarchical_model`: 父子分块结构，适合大块和小块联动检索。
- `qa_model`: 问答对结构，适合问答型知识组织。

## 选填字段

- `summary_index_setting`: 需要摘要索引时填写。

## 贯通性分析

- 上游通常接 `document-extractor`、`tool`、`variable-aggregator` 或分块节点输出。
- 在 `rag_pipeline` 中它通常是主链路尾部，负责把结构化块写入知识库。
- 关键是上游输出结构、`chunk_structure`、索引方式和检索配置必须互相一致。

## 可承接上游节点

### 推荐

- `document-extractor`
- `tool`
- `variable-aggregator`

### 可用但需人工确认

- `code`
- `list-operator`
- 其他能输出分块结果的节点

### 不推荐

- `start`
- 任意 `trigger-*`
- `answer`

## 可衔接下游节点

### 推荐

- 无，`knowledge-index` 一般作为 `rag_pipeline` 主链路尾部。

### 可用但需人工确认

- 无。

### 不推荐

- 任意普通业务节点
- `answer`
- `start`

## 编排约束

- `index_chunk_variable_selector` 必须指向上游分块或抽取结果。
- 在 `rag-pipeline` 中通常位于链路尾部。
- `chunk_structure` 要与上游输出结构一致，实际值应使用 `text_model`、`hierarchical_model`、`qa_model`。
- `indexing_technique`、`retrieval_model`、`embedding_model` 等字段若来自 fixture，应在报告里标记为“模板常见扩展字段”或“兼容字段”。

## 最小骨架

```yaml
data:
  title: Knowledge Index
  type: knowledge-index
  chunk_structure: text_model
  index_chunk_variable_selector: [general_chunker_tool, result]
  indexing_technique: economy
```
