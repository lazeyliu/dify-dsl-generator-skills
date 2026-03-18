# template-transform 节点

## 作用

把多个变量按模板拼成新文本。

## 必填字段

- `type: template-transform`: 指定当前节点是模板文本转换节点。
- `variables`: 定义模板中可引用的变量映射。
- `template`: 模板正文，没有它就无法生成新文本。

## 选填字段

- `title`: 需要在画布中更直观地表达用途时填写。
- `desc`: 需要说明模板转换意图时填写。
- `version`: 需要固定兼容写法时填写。
- `retry_config`: 模板转换通常不需要；只有把它视作可重试步骤时才填写。

## 贯通性分析

- 上游通常接 `llm`、`knowledge-retrieval`、`assigner`、`start` 输入。
- 下游常接 `llm`、`answer`、`http-request`、`end`。
- 关键是模板里用到的占位变量必须都能由 `variables` 映射提供。

## 可承接上游节点

### 推荐

- `start`
- `llm`
- `knowledge-retrieval`
- `assigner`
- `tool`

### 可用但需人工确认

- `code`
- `variable-aggregator`
- `list-operator`

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `llm`
- `answer`
- `http-request`
- `end`
- `tool`

### 可用但需人工确认

- `if-else`
- `assigner`
- `code`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `variables[*]` 要与模板里使用的变量一致。
- 适合纯文本重组，不适合复杂逻辑判断。

## 最小骨架

```yaml
data:
  title: Template Transform
  type: template-transform
  variables:
    - variable: text
      value_selector: [llm, text]
  template: "结果：{{ text }}"
```
