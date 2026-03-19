# end 节点

## 作用

声明 workflow 的结构化输出。

## 必填字段

- `type: end`: 指定当前节点是 workflow 终点节点。
- `outputs`: 定义流程最终产出的字段清单，没有它就无法稳定返回结构化结果。

`outputs[*]` 最少需要:

- `variable`: 最终输出字段名，供调用方读取。
- `value_selector`: 指向上游真实来源，没有它就无法把结果映射到终点输出。

建议始终显式写:

- `value_type`: 标明输出值类型，便于调用方和后续维护理解结果结构。

## 选填字段

- `title`: 需要在画布上区分多个终点时填写。
- `desc`: 需要说明终点用途时填写。
- `version`: 需要固定兼容写法时填写；多数情况下保持默认。
- `retry_config`: 只有终点存在重试语义时才考虑填写，普通场景通常不需要。

## 贯通性分析

- 上游通常接 `start`、`code`、`llm`、`tool`、`variable-aggregator` 等已完成计算的节点。
- 它是 `workflow` 的终点，关键是 `outputs` 是否都能从上游真实产出。
- 多分支汇聚时，要确认每个 `value_selector` 在可达路径上都成立，或接受为空。

## 可承接上游节点

### 推荐

- `start`
- `code`
- `llm`
- `tool`
- `variable-aggregator`
- `iteration`
- `loop`

### 可用但需人工确认

- `assigner`
- `template-transform`
- `knowledge-retrieval`
- `list-operator`
- 其他已形成稳定输出的节点

### 不推荐

- 任意 `trigger-*`
- `datasource`

## 可衔接下游节点

### 推荐

- 无，`end` 一般作为 workflow 终点。

### 可用但需人工确认

- 无。

### 不推荐

- 任意普通业务节点
- 任意 `trigger-*`
- `start`

## 编排约束

- `workflow` 模式建议至少一个 `end`。
- 最小 workflow 可以直接 `start -> end`，此时 `end.outputs` 可直接映射 `start` 输入字段。
- `outputs[*].value_selector` 必须能追溯到上游节点或容器输出。
- 如果多个分支汇总到同一个 `end`，要检查所有分支都能给出对应变量，或接受空值。

## 最小骨架

```yaml
data:
  title: End
  type: end
  outputs:
    - variable: result
      value_type: string
      value_selector: [llm, text]
```
