# http-request 节点

## 作用

发起 HTTP 请求并把响应暴露给下游节点。

## 必填字段

- `type: http-request`: 指定当前节点是 HTTP 请求节点。
- `method`: 请求方法，决定调用语义。
- `url`: 请求地址，没有它无法发起调用。
- `authorization`: 鉴权配置，决定如何访问外部服务。
- `headers`: 请求头集合，常用于传认证、上下文或内容类型。
- `params`: 查询参数集合，常用于 GET 或混合参数调用。

`authorization` 是两层结构:

- 外层 `authorization.type` 当前只区分 `no-auth` 和 `api-key`。
- 具体鉴权样式写在 `authorization.config.type`，常见兼容值包括 `basic`、`bearer`、`custom`。

`authorization.type` 常见值:

- `no-auth`: 目标接口无需鉴权时使用。
- `api-key`: 目标接口需要显式凭证时使用。

若是 `api-key`，还要补 `config`，否则请求鉴权信息不完整。
不要把 `authorization.type` 直接写成 `basic` 或 `bearer`。

## 选填字段

- `body`: 请求需要提交正文时填写；GET 或空体调用时可省略。
- `timeout`: 需要控制超时时间时填写，避免外部服务拖垮链路。
- `ssl_verify`: 需要显式控制证书校验时填写。

## 贯通性分析

- 上游常接 `start`、`template-transform`、`assigner`，为 URL、headers、body 提供变量。
- 下游常接 `tool`、`code`、`end`、`if-else`。
- 关键是请求体类型和下游消费字段一致，例如下游到底需要 `body`、`text`、`status_code` 还是文件响应。

## 可承接上游节点

### 推荐

- `start`
- `template-transform`
- `assigner`

### 可用但需人工确认

- `code`
- `llm`
- `tool`
- `parameter-extractor`
- 其他能提供请求参数的节点

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `tool`
- `code`
- `end`
- `if-else`
- `template-transform`

### 可用但需人工确认

- `llm`
- `assigner`
- `answer`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 兼容性提醒

- `headers`、`params` 常见为字符串字段。
- `body.data` 有时会出现空字符串，这属于兼容写法。
- `retry_config.enabled` 与 `retry_enabled` 可能混用，生成新 DSL 时不要无脑照抄。

## 最小骨架

```yaml
data:
  title: HTTP Request
  type: http-request
  method: GET
  url: "{{#start.url#}}"
  authorization:
    type: no-auth
  headers: ""
  params: ""
  body:
    type: none
    data: []
```
