# trigger-plugin 节点

## 作用

由插件事件触发工作流。

## 必填字段

- `type: trigger-plugin`: 指定当前节点是插件触发入口。
- `plugin_id`: 指定触发插件。
- `provider_id`: 指定提供方标识。
- `event_name`: 指定触发事件名。
- `subscription_id`: 指定订阅标识。
- `plugin_unique_identifier`: 指定插件唯一实例标识。
- `event_parameters`: 定义触发事件携带的参数。

## 选填字段

- `title`: 需要在画布上明确标识该触发器用途时填写。
- `desc`: 需要解释触发场景时填写。
- `version`: 需要固定兼容写法时填写。

## 贯通性分析

- 它本身就是入口，不依赖 `start`。
- 下游通常接业务处理节点，例如 `tool`、`llm`、`if-else`、`end`。
- 关键是事件参数 schema 和下游业务假设一致。

## 可承接上游节点

### 推荐

- 无，`trigger-plugin` 本身就是触发入口。

### 可用但需人工确认

- 无。

### 不推荐

- `start`
- 任意普通业务节点
- `datasource`

## 可衔接下游节点

### 推荐

- `tool`
- `llm`
- `if-else`
- `code`
- `end`

### 可用但需人工确认

- `answer`
- `assigner`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `event_parameters` 当前逻辑只支持常量输入，不能随意写变量型输入。
- 这是入口节点，通常不再同时配普通 `start` 作为主入口。

## 最小骨架

```yaml
data:
  title: Trigger Plugin
  type: trigger-plugin
  plugin_id: plugin_x
  provider_id: provider_x
  event_name: on_created
  subscription_id: sub_x
  plugin_unique_identifier: provider/plugin:1.0.0
  event_parameters: {}
```
