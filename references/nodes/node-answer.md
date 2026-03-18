# answer 节点

## 作用

向 chatflow 流式输出文本。

## 必填字段

- `type: answer`: 指定当前节点是对话输出节点。
- `answer`: 输出模板正文，通常直接引用上游文本结果。

`answer` 通常写成模板字符串，例如 `{{#llm.text#}}`，如果引用错字段，用户会看到空输出或错误内容。

## 选填字段

- `title`: 需要在画布上清楚表达用途时填写；不填也不影响执行。
- `desc`: 需要补充节点说明时填写，主要帮助维护。

## 贯通性分析

- 上游通常接 `start`、`llm`、`template-transform`、`code` 或任意能产出字符串的节点。
- 它通常就是用户可见终点。
- 如果一个流程里有多个 `answer`，要分析输出顺序、依赖关系和是否会重复回复。

## 可承接上游节点

### 推荐

- `start`
- `llm`
- `template-transform`
- `code`

### 可用但需人工确认

- `tool`
- `assigner`
- `variable-aggregator`
- 其他能稳定产出字符串结果的节点

### 不推荐

- 任意 `trigger-*`
- `datasource`

## 可衔接下游节点

### 推荐

- 无，`answer` 一般作为对话输出终点。

### 可用但需人工确认

- `llm`
- `tool`
- `if-else`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`
- `knowledge-index`

## 编排约束

- `answer` 适合 `advanced-chat`。
- 最小 chatflow 可以直接 `start -> answer`，此时 `answer` 常直接引用 `sys.query` 或 `start` 输入。
- 若一个流程里有多个 `answer`，要额外审查输出顺序和依赖关系。
- `answer` 常作为终点，但也可能只是中间响应节点，需结合连边确认。

## 最小骨架

```yaml
data:
  title: Answer
  type: answer
  answer: "{{#llm.text#}}"
```
