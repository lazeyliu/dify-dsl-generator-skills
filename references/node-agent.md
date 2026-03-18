# agent 节点

## 作用

执行 Agent 策略，并可接入工具参数。

## 必填字段

- `type: agent`
- `agent_strategy_provider_name`: 指定 agent 策略提供方。
- `agent_strategy_name`: 指定要执行的 agent 策略名称。
- `agent_strategy_label`: 指定策略展示名，便于区分不同 agent 节点。
- `agent_parameters`: 定义 agent 执行时所需参数集合。

## 选填字段

- `memory`: 需要让 agent 结合上下文历史推理时填写。
- `tool_node_version`: 当前推荐显式写，通常为 `"2"`；它不仅是兼容字段，也会影响 agent 工具参数的解析路径。

## 贯通性分析

- 上游通常提供用户输入、上下文变量或工具选择结果。
- 下游通常消费 agent 最终文本、结构化结果或 agent 中间轨迹摘要。
- 若 `agent_parameters` 中引用工具选择器或变量选择器，要确认上游节点真的产出了对应结构。

## 可承接上游节点

### 推荐

- `start`
- `assigner`
- `template-transform`
- `knowledge-retrieval`
- `tool`

### 可用但需人工确认

- `llm`
- `human-input`
- `variable-aggregator`
- 其他能提供上下文、参数或工具选择结果的节点

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `answer`
- `end`
- `if-else`
- `assigner`
- `template-transform`
- `code`

### 可用但需人工确认

- `tool`
- `human-input`
- `variable-aggregator`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `agent_parameters` 至少要与所选策略需要的参数名匹配。
- 若参数中引用工具选择器或变量选择器，要保证上游已定义。
- 与 `tool` 节点不同，`agent` 更像“策略执行器”而不是单次工具调用。

## 最小骨架

```yaml
data:
  title: Agent
  type: agent
  tool_node_version: "2"
  agent_strategy_provider_name: builtin
  agent_strategy_name: react
  agent_strategy_label: ReAct
  agent_parameters: {}
```
