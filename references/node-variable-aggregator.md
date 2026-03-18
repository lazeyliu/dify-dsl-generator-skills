# variable-aggregator 节点

## 作用

从多个候选变量中按顺序选择第一个非空结果输出。

启用分组时，不是把所有变量合并成一个大结果，而是“每个分组各自选择第一个非空结果”。

当前正式节点类型是 `variable-aggregator`。旧兼容名 `variable-assigner` 指向的是这个聚合器，不是赋值节点。

## 必填字段

- `type: variable-aggregator`: 指定当前节点是变量聚合节点。
- `output_type`: 指定聚合后输出类型，供下游判断如何消费。
- `variables`: 指定要聚合的变量集合。

## 选填字段

- `advanced_settings`: 需要按分组聚合、分组命名或设置组级输出类型时填写。

## 贯通性分析

- 上游通常来自并行分支、条件分支、多个 LLM 或多个工具节点。
- 下游常接 `end`、`template-transform`、`knowledge-index`。
- 关键不是“把所有值拼起来”，而是候选值的顺序、空值语义，以及下游是否接受“首个有效结果”这种输出方式。

## 可承接上游节点

### 推荐

- `llm`
- `tool`
- `code`
- `document-extractor`
- `if-else` 分支后的多个节点

### 可用但需人工确认

- `iteration`
- `loop`
- `list-operator`
- 其他并行分支输出节点

### 不推荐

- `start`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `end`
- `template-transform`
- `knowledge-index`
- `llm`

### 可用但需人工确认

- `answer`
- `tool`
- `code`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `variables` 是变量选择器数组的数组。
- 如果启用 `advanced_settings.group_enabled`，就要补齐每个分组的 `group_name`、`output_type`、`variables`。
- 如果遇到旧 DSL 的 `type: variable-assigner`，优先按“聚合器旧别名”理解，并在报告里标记兼容迁移。

## 最小骨架

```yaml
data:
  title: Variable Aggregator
  type: variable-aggregator
  output_type: array[string]
  variables:
    - [llm_1, text]
    - [llm_2, text]
```
