# loop / loop-start / loop-end 节点

## 作用

按条件重复执行容器内子图。

## loop 必填字段

- `type: loop`: 指定当前节点是循环容器。
- `loop_count`: 定义最大循环次数，防止无限循环。
- `break_conditions`: 定义跳出循环的条件。
- `logical_operator`: 定义多个跳出条件之间的组合关系。

执行必需字段:

- `start_node_id`: 指向容器内部起点节点；缺失时运行时会直接报错。

强烈建议显式写:

- `loop_variables`: 定义循环内维护的变量集合。

`logical_operator` 常见值说明:

- `and`: 所有跳出条件都满足时才结束循环。
- `or`: 任一跳出条件满足就结束循环。

## 选填字段

- `outputs`: 需要显式声明循环输出结果时填写。
- `desc`: 需要解释循环用途时填写。
- `version`: 需要固定兼容写法时填写。
- `retry_config`: 循环步骤允许重试时填写。

## loop-start / loop-end

内部边界节点类型:

- `loop-start`: 容器内部起点。
- `loop-end`: 容器内部结束边界。

## 贯通性分析

- 上游通常提供循环初始条件或初始变量。
- 容器内节点不断更新 `loop_variables`，直到 break 条件满足。
- 关键是检查 break 条件可收敛、循环变量可写、容器输出可被下游消费。

## 可承接上游节点

### 推荐

- `start`
- `assigner`
- `code`

### 可用但需人工确认

- `tool`
- `template-transform`
- 其他能提供循环初始值的节点

### 不推荐

- 任意 `trigger-*`
- `answer`
- `end`

## 可衔接下游节点

### 推荐

- `end`
- `template-transform`
- `llm`
- `code`

### 可用但需人工确认

- `answer`
- `tool`
- `variable-aggregator`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `start_node_id` 是执行必需字段，且必须指向容器内真实存在的 `loop-start`。
- `break_conditions` 必须引用循环变量或可在循环内解析的变量。
- `loop_variables[*]` 建议完整写 `label`、`var_type`、`value_type`、`value`。
- 若使用 `outputs`，要确保与容器外 `end` 或下游节点有稳定衔接。

## 最小骨架

```yaml
data:
  title: Loop
  type: loop
  loop_count: 10
  logical_operator: and
  break_conditions:
    - variable_selector: [loop_node, num]
      comparison_operator: "≥"
      value: "5"
      varType: number
  loop_variables:
    - label: num
      var_type: number
      value_type: constant
      value: 1
  start_node_id: loop_start
```
