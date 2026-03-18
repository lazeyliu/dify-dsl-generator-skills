# human-input 节点

## 作用

暂停流程并等待人工填写表单或点击动作。

## 必填字段

- `type: human-input`: 指定当前节点是人工输入节点。
- `delivery_methods`: 至少要有一个启用的投递方式。
- `user_actions`: 至少要有一个动作按钮。

下面这些字段当前实体提供了默认值，但建议在手写 DSL 时显式写清:

- `form_content`
- `inputs`
- `timeout`
- `timeout_unit`

`inputs[*]` 最少需要:

- `type`: 指定输入控件类型。
- `output_variable_name`: 指定该输入最终写出的字段名。

`inputs[*].type` 常见值说明:

- `text-input`: 适合短文本填写，例如审批意见、标签、编号。
- `paragraph`: 适合长文本填写，例如详细说明、反馈正文。

`user_actions[*]` 最少需要:

- `id`: 动作标识，也是后续分支恢复时的关键值。
- `title`: 动作展示名。

`delivery_methods[*].type` 常见值说明:

- `webapp`: 适合在产品内直接展示人工表单。
- `email`: 适合通过邮件发送人工操作入口。

`timeout_unit` 常见值说明:

- `hour`: 适合小时级审批或确认流程。
- `day`: 适合天级等待的人工作业。

## 选填字段

- `desc`: 需要解释人工输入目的时填写。
- `version`: 需要固定兼容写法时填写。
- `delivery_methods[*].config`: 某种投递方式需要额外配置时填写。
- `inputs[*].default`: 需要给表单输入默认值时填写。
- `user_actions[*].button_style`: 需要区分按钮样式时填写。

## 贯通性分析

- 上游通常接审批前的模型结果、提取结果或上下文变量。
- 下游根据用户动作分支继续执行，也可能把表单输出写回变量域。
- 关键是暂停后的恢复路径、动作句柄和表单输出字段必须和后续边、变量选择器一致。

## 可承接上游节点

### 推荐

- `llm`
- `tool`
- `code`
- `if-else`

### 可用但需人工确认

- `assigner`
- `template-transform`
- 其他需要人工确认后再继续的节点

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 可衔接下游节点

### 推荐

- `assigner`
- `llm`
- `tool`
- `end`

### 可用但需人工确认

- `answer`
- `if-else`
- `code`
- 其他按动作分支恢复执行的节点

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `delivery_methods` 至少要有一个启用项。
- `user_actions[*].id` 必须唯一，且符合标识符规则。
- `inputs[*].output_variable_name` 必须唯一。
- `form_content` 中引用的 `{{#$output.xxx#}}` 要与 `inputs` 输出名一致。
- 除了按 `user_actions[*].id` 恢复分支，还要考虑真实存在的超时分支 `__timeout`。
- 需要邮件投递时，补齐 `delivery_methods[type=email].config`。

## 最小骨架

```yaml
data:
  title: Human Input
  type: human-input
  delivery_methods:
    - type: webapp
      enabled: true
      config: {}
  form_content: "请补充信息"
  inputs:
    - type: text-input
      output_variable_name: comment
  user_actions:
    - id: approve
      title: 通过
  timeout: 36
  timeout_unit: hour
```
