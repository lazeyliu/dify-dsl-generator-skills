# start 节点

## 作用

声明工作流入口变量。

## 必填字段

- `type: start`: 指定当前节点是普通流程入口，没有这个字段就无法被识别为 `start`。
- `variables`: 定义入口输入字段集合，下游节点读取的用户输入通常都从这里进入。

`variables[*]` 最小必填通常是:

- `variable`: 输入变量名，也是下游选择器里引用的名字。
- `label`: 输入项展示名，用于区分不同入口字段。
- `type`: 输入控件类型，决定这个字段按文本、数字、文件还是对象处理。

常见 `type`:

- `text-input`: 单行文本输入，适合短文本、关键词、ID、URL。
- `paragraph`: 多行文本输入，适合长文本、说明、上下文正文。
- `number`: 数字输入，适合计数、阈值、排序参数。
- `select`: 枚举选择输入，适合候选项固定的字段。
- `file`: 单文件输入，适合上传一个文档或图片。
- `file-list`: 多文件输入，适合批量文件处理。
- `checkbox`: 布尔输入，适合开关型字段。
- `json_object`: 对象输入，适合传结构化 JSON。
- `external_data_tool`: 较少见但受源码支持，适合把外部数据工具结果作为入口字段类型。

## 选填字段

- `required`: 需要强制用户填写时开启；不填通常按可空输入处理。
- `default`: 希望入口字段有默认值时填写；不填则由调用方显式提供。
- `max_length`: 需要限制输入长度时填写，常用于文本输入。
- `options`: 当 `type` 是选择类输入时填写，限定可选值集合。
- `allowed_file_types`: 当输入是文件时填写，用于限制文件大类。
- `allowed_file_extensions`: 需要限制文件后缀时填写。
- `allowed_file_upload_methods`: 需要限制上传方式时填写，例如本地上传或远程地址。
- `json_schema`: 当输入是对象结构时填写，用于约束 JSON 输入形态。

## 贯通性分析

- `start` 本身是入口，不依赖上游节点。
- 下游通常接 `llm`、`if-else`、`code`、`http-request`、`tool`。
- 关键是它声明的输入变量被下游真实消费，而不是只定义未使用。

## 可承接上游节点

### 推荐

- 无，`start` 本身就是普通流程入口。

### 可用但需人工确认

- 无。

### 不推荐

- 任意 `trigger-*`
- `datasource`
- 其他普通业务节点

## 可衔接下游节点

### 推荐

- `llm`
- `if-else`
- `code`
- `http-request`
- `tool`
- `template-transform`
- `question-classifier`
- `parameter-extractor`
- `knowledge-retrieval`

### 可用但需人工确认

- `assigner`
- `human-input`
- `iteration`
- `loop`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `start` 通常是普通 workflow 或 chatflow 的唯一入口。
- 若使用 `trigger-*` 节点，默认不要再保留 `start`，避免无意做成多入口。

## 最小骨架

```yaml
data:
  title: Start
  type: start
  variables:
    - variable: query
      label: Query
      type: text-input
      required: true
```
