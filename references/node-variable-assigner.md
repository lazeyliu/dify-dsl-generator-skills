# assigner 节点

## 作用

更新流程变量、循环变量或对话变量。

## 推荐使用

优先使用新版 `type: assigner`，`version: "2"`。

注意:

- `assigner` 才是当前变量赋值节点。
- `variable-assigner` 不是它的旧类型名，而是变量聚合器的旧兼容名。

## 新版必填字段

- `type: assigner`: 指定当前节点是变量赋值节点。
- `version: "2"`: 指定使用新版赋值结构，避免和旧字段组混淆。
- `items`: 赋值动作集合，每一项描述一次写入行为。

`items[*]` 最少需要:

- `variable_selector`: 指定要写入的目标变量。
- `input_type`: 指定写入值来自变量或常量。
- `operation`: 指定写入方式。
- `value`: 真正写入的值或值选择器。

`input_type` 当前新版只支持:

- `input_type: variable`: 写入值来自另一个变量。
- `input_type: constant`: 写入值是显式常量。

新建 DSL 不要写 `input_type: mixed`，那不是当前新版 `assigner` 的合法取值。

`operation` 当前支持:

- `over-write`
- `clear`
- `append`
- `extend`
- `set`
- `+=`
- `-=`
- `*=`
- `/=`
- `remove-first`
- `remove-last`

## 旧版 assigner 兼容字段

旧版赋值节点仍然是 `type: assigner`，但字段常见为:

- `assigned_variable_selector`: 旧版目标变量选择器。
- `write_mode`: 旧版写入模式。
- `input_variable_selector`: 旧版输入变量来源。

需要注意:

- 当前仓库里的部分 `version: "2"` fixture 仍可能携带旧兼容字段。
- 这是因为节点基类允许保留额外字段，不能仅凭出现旧字段就判定 DSL 无效。
- 新建 DSL 仍应优先使用 `items` 结构，不建议继续生成旧字段组。

## 选填字段

- `desc`: 需要说明赋值用途时填写。
- `retry_config`: 赋值步骤可能失败且允许重试时填写。
- `default_value`: 需要在失败时回退到默认值时填写。

## 贯通性分析

- 上游通常提供待写入值或上下文变量。
- 下游常接 `llm`、`answer`、`end` 或容器内部后续节点。
- 关键是目标变量在当前作用域中可写，且写入后的变量会被后续节点真实消费。

## 可承接上游节点

### 推荐

- `start`
- `llm`
- `tool`
- `code`
- `iteration-start`
- `loop-start`

### 可用但需人工确认

- `template-transform`
- `knowledge-retrieval`
- `human-input`
- 其他能提供写入值的节点

### 不推荐

- `end`
- `answer`
- `knowledge-index`

## 可衔接下游节点

### 推荐

- `llm`
- `end`
- `template-transform`
- `if-else`
- 容器内部后续节点

### 可用但需人工确认

- `answer`
- `tool`
- `human-input`
- `code`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- 变量选择器必须指向可写变量域，例如对话变量、循环变量。
- 在 `iteration` 或 `loop` 容器内使用时，要检查变量域是否在容器上下文中可见。
- 不仅要校验单个字段是否合法，还要校验字段组合关系是否合法，例如 `input_type + operation`、`operation + variable_type`。
- 要特别防止这类通过 YAML 解析、但会被运行时拒绝的错误，例如 `Input type constant is not supported for operation over-write`、`Operation set is not supported for type array[string]`。
- 报告里注明是“新版 assigner”还是“旧版 assigner 字段组”。

## 最小骨架

```yaml
data:
  title: Variable Assigner
  type: assigner
  version: "2"
  items:
    - variable_selector: [conversation, answer]
      input_type: variable
      operation: over-write
      value: [sys, query]
```
