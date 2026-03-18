# parameter-extractor 节点

## 作用

从输入文本里抽取结构化参数。

## 必填字段

- `type: parameter-extractor`: 指定当前节点是参数抽取节点。
- `model`: 指定抽取用模型。
- `query`: 指定要抽取参数的文本来源。
- `parameters`: 定义待抽取参数清单。
- `reasoning_mode`: 指定抽取采用函数式还是提示词式推理。

`parameters[*]` 最少需要:

- `name`: 参数名，也是下游引用的字段名。
- `type`: 参数类型，决定抽取后如何校验和消费。
- `description`: 参数语义说明，用于约束抽取方向。
- `required`: 指定参数是否必须成功抽出。

## 选填字段

- `instruction`: 需要补充抽取规则时填写。
- `memory`: 需要结合上下文进行抽取时填写。
- `vision`: 需要从图像型输入抽取参数时填写。

## 贯通性分析

- 上游通常接用户输入、文档文本或检索结果。
- 下游常接 `if-else`、`assigner`、`end`、`tool`。
- 关键是确认抽取参数名、类型与下游字段引用保持一致。

## 可承接上游节点

### 推荐

- `start`
- `document-extractor`
- `knowledge-retrieval`
- `template-transform`
- `llm`

### 可用但需人工确认

- `tool`
- `assigner`

### 不推荐

- `end`
- `answer`
- `knowledge-index`

## 可衔接下游节点

### 推荐

- `if-else`
- `assigner`
- `end`
- `tool`

### 可用但需人工确认

- `llm`
- `code`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- 参数名不能是 `__reason` 或 `__is_success`。
- `query` 通常是变量选择器列表，不要写成不可解析文本。
- `reasoning_mode` 常见值是 `function_call` 或 `prompt`。

## 最小骨架

```yaml
data:
  title: Parameter Extractor
  type: parameter-extractor
  model:
    provider: openai
    name: gpt-4o-mini
    mode: chat
    completion_params: {}
  query: [sys, query]
  reasoning_mode: function_call
  parameters:
    - name: city
      type: string
      description: 城市名
      required: true
```
