# trigger-schedule 节点

## 作用

按可视化频率或 cron 定时触发流程。

## 必填字段

- `type: trigger-schedule`: 指定当前节点是定时触发入口。

建议显式写:

- `mode`: 指定使用 cron 还是可视化调度方式。
- `timezone`: 指定调度所在时区。

## 按模式的额外字段

- `mode: visual`
  常配 `frequency` 与 `visual_config`，用于表达可视化调度规则。

- `mode: cron`
  需要 `cron_expression`，用于表达 cron 规则。

取值说明:

- `visual`: 适合用自然的小时、天、周、月配置表达调度，不需要手写 cron。
- `cron`: 适合复杂调度规则或需要和现有 cron 体系对齐时使用。

## 选填字段

- `frequency`: 使用可视化调度时填写。
- `cron_expression`: 使用 cron 调度时填写。
- `visual_config`: 需要补充具体时间、星期或日期配置时填写。

## 贯通性分析

- 它本身就是入口，不依赖 `start`。
- 下游通常接定时任务链路，如 `http-request`、`tool`、`llm`、`end`。
- 关键是调度模式、时区和下游任务的幂等性是否匹配。

## 可承接上游节点

### 推荐

- 无，`trigger-schedule` 本身就是触发入口。

### 可用但需人工确认

- 无。

### 不推荐

- `start`
- 任意普通业务节点
- `datasource`

## 可衔接下游节点

### 推荐

- `http-request`
- `tool`
- `llm`
- `code`
- `end`

### 可用但需人工确认

- `answer`
- `assigner`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `visual` 与 `cron` 二选一，不要混写成互相矛盾。
- 时区必须明确。

## 最小骨架

```yaml
data:
  title: Trigger Schedule
  type: trigger-schedule
  mode: cron
  cron_expression: "0 9 * * *"
  timezone: Asia/Shanghai
```
