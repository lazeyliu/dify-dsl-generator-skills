# question-classifier 节点

## 作用

让模型把输入路由到多个分类分支。

## 必填字段

- `type: question-classifier`: 指定当前节点是问题分类节点。
- `query_variable_selector`: 指定待分类文本来源。
- `model`: 指定用于分类的模型。
- `classes`: 定义分类集合。

`classes[*]` 最少需要:

- `id`: 分类唯一标识，常用于连接边句柄。
- `name`: 分类展示名和语义名。

## 选填字段

- `instruction`: 需要补充分类规则时填写。
- `memory`: 分类依赖上下文时填写。
- `vision`: 分类依赖图像输入时填写。

## 贯通性分析

- 上游通常接 `sys.query`、对话变量或上游文本结果。
- 下游是按类别分支的多个节点。
- 关键是检查分类 ID 与边句柄是否一致，以及每个类别是否有真正的去向。

## 可承接上游节点

### 推荐

- `start`
- `assigner`
- `template-transform`
- `llm`

### 可用但需人工确认

- `tool`
- `knowledge-retrieval`
- 其他能提供分类文本的节点

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `llm`
- `tool`
- `code`
- `answer`
- `end`

### 可用但需人工确认

- `if-else`
- `assigner`
- `human-input`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- 每个分类 `id` 应与后续边句柄设计保持一致。
- 类别列表不要留空。
- 与 `if-else` 的区别是它依赖模型判断，不是硬编码条件。

## 最小骨架

```yaml
data:
  title: Question Classifier
  type: question-classifier
  query_variable_selector: [sys, query]
  model:
    provider: openai
    name: gpt-4o-mini
    mode: chat
    completion_params: {}
  classes:
    - id: sales
      name: 销售
    - id: support
      name: 客服
```
