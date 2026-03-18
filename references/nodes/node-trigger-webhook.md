# trigger-webhook 节点

## 作用

暴露 webhook 入口，由 HTTP 请求触发流程。

## 必填字段

- `type: trigger-webhook`: 指定当前节点是 webhook 入口。

通常还应显式写:

- `method`: 指定允许的请求方法。
- `content_type`: 指定请求体内容类型。
- `headers`: 定义允许接收的请求头参数。
- `params`: 定义允许接收的查询参数。
- `body`: 定义请求体参数结构。

常见取值说明:

- `method: get`: 适合无请求体的拉取式触发。
- `method: post`: 适合提交正文的常规触发。
- `method: put/patch/delete`: 适合与外部系统动作语义保持一致时使用。

- `content_type: application/json`: 最常见，适合对象型请求体。
- `content_type: multipart/form-data`: 适合文件上传。
- `content_type: application/x-www-form-urlencoded`: 适合表单键值提交。
- `content_type: text/plain`: 适合纯文本请求体。
- `content_type: application/octet-stream`: 适合二进制文件或裸字节流 webhook。

## 选填字段

- `status_code`: 需要自定义响应状态码时填写。
- `response_body`: 需要自定义响应体模板时填写。
- `timeout`: 需要限制 webhook 等待时长时填写。

## 贯通性分析

- 它本身是外部入口，不依赖 `start`。
- 下游通常接参数校验、`if-else`、`tool`、`code`、`end`。
- 关键是请求方法、参数定义和下游预期字段一致，并且响应模板能覆盖主要结果。

## 可承接上游节点

### 推荐

- 无，`trigger-webhook` 本身就是触发入口。

### 可用但需人工确认

- 无。

### 不推荐

- `start`
- 任意普通业务节点
- `datasource`

## 可衔接下游节点

### 推荐

- `if-else`
- `tool`
- `code`
- `llm`
- `end`

### 可用但需人工确认

- `answer`
- `assigner`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `headers` 只支持字符串类型。
- `params` 支持字符串、数字、布尔。
- `body` 支持文本、数字、布尔、对象、数组和文件。
- 这是入口节点，通常不再并列普通 `start`。
- 可能出现 `webhook_url` 等辅助字段，但它更偏运行时或界面辅助，不要当成手写 DSL 的核心硬字段。

## 最小骨架

```yaml
data:
  title: Trigger Webhook
  type: trigger-webhook
  method: post
  content_type: application/json
  headers: []
  params: []
  body:
    - name: payload
      type: object
      required: true
  status_code: 200
  response_body: "{\"ok\": true}"
```
