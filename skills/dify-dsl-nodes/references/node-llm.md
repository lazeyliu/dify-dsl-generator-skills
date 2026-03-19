# llm 节点

## 作用

调用模型生成文本或结构化输出。

## 必填字段

- `type: llm`: 指定当前节点是模型调用节点。
- `model`: 指定要调用的模型与参数，没有它就无法发起推理。
- `prompt_template`: 定义提示词结构，没有它模型不知道如何生成。
- `context`: 控制是否启用上下文读取，影响记忆与对话连续性。

`model` 最小必填:

- `provider`: 模型供应方标识，决定到哪类模型服务发请求。
- `name`: 具体模型名，决定能力与成本。
- `mode`: 运行模式，通常决定按 chat 还是其他模式组织请求。

`context` 最少要有:

- `enabled`: 是否启用上下文；不写清容易导致链路对历史消息的假设失效。

## 选填字段

- `prompt_config`: 需要显式声明模板变量映射时填写。
- `memory`: 需要窗口记忆或上下文拼接时填写；不填通常按无记忆处理。
- `vision`: 需要图像输入时填写；纯文本流程可省略。
- `structured_output`: 需要模型按固定 schema 产出时填写。
- `structured_output_enabled`: 需要打开结构化输出开关时填写；只写 schema 但不开开关通常不会生效。
- `reasoning_format`: 需要控制思维内容输出形式时填写。

## 贯通性分析

- 上游通常接 `start` 输入、检索结果、模板转换结果、对话变量。
- 下游常接 `answer`、`end`、`if-else`、`assigner`、`template-transform`。
- 关键是 prompt 依赖变量是否齐全，以及下游消费的是 `text` 还是结构化输出。

## 可承接上游节点

### 推荐

- `start`
- `knowledge-retrieval`
- `template-transform`
- `assigner`

### 可用但需人工确认

- `code`
- `tool`
- `variable-aggregator`
- `question-classifier`
- 其他能提供文本、上下文或结构化提示词输入的节点

### 不推荐

- `end`
- `answer`
- `knowledge-index`

## 可衔接下游节点

### 推荐

- `answer`
- `end`
- `if-else`
- `assigner`
- `template-transform`

### 可用但需人工确认

- `code`
- `tool`
- `question-classifier`
- `human-input`
- `variable-aggregator`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `prompt_template` 在生产 DSL 中通常建议非空，但不要把“不能为空列表”当成源码硬约束。
- `mode` 要与模型能力匹配，常见是 `chat`。
- 若启用结构化输出，报告里要写清 schema 来源。

## 最小骨架

```yaml
data:
  title: LLM
  type: llm
  model:
    provider: openai
    name: gpt-4o-mini
    mode: chat
    completion_params: {}
  prompt_template:
    - role: system
      text: "你是助手。"
    - role: user
      text: "{{#sys.query#}}"
  context:
    enabled: false
```
