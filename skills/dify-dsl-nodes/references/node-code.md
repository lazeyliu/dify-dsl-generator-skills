# code 节点

## 作用

执行代码并返回结构化结果。

## 必填字段

- `type: code`: 指定当前节点是代码执行节点。
- `variables`: 定义代码可读取的输入变量映射。
- `code_language`: 指定执行语言，决定运行环境。
- `code`: 代码正文，没有它就没有可执行逻辑。
- `outputs`: 声明代码输出结构，供下游稳定引用。

`code_language` 当前实体明确支持:

- `python3`: 适合数据处理、文本处理、结构化转换，通常是默认首选。
- `javascript`: 适合需要 JS 语法或与前端逻辑接近的处理场景。

## 选填字段

- `desc`: 需要解释代码节点用途时填写。
- `version`: 需要显式锁定节点写法时填写。
- `retry_config`: 代码节点可能失败且允许自动重试时填写。
- `dependencies`: 代码执行依赖外部库时填写；不填则只能使用默认环境。

## 贯通性分析

- 上游通常接 `start`、`assigner`、`http-request`、`tool` 或容器内部节点输出。
- 下游可接 `end`、`answer`、`template-transform`、`iteration`、`loop`。
- 最关键的贯通点是 `outputs` 要与下游 `value_selector` 一一对应。

## 可承接上游节点

### 推荐

- `start`
- `assigner`
- `http-request`
- `tool`
- `iteration-start`
- `loop-start`

### 可用但需人工确认

- `llm`
- `template-transform`
- `knowledge-retrieval`
- `list-operator`
- 其他能提供变量输入的节点

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `end`
- `template-transform`
- `iteration`
- `loop`
- `if-else`
- `assigner`

### 可用但需人工确认

- `answer`
- `tool`
- `llm`
- `variable-aggregator`
- `list-operator`

### 不推荐

- `start`
- 任意 `trigger-*`
- `datasource`

## 编排约束

- `outputs` 必须与 `main()` 返回字段对齐。
- `outputs[*].type` 必须属于允许类型，如 `string`、`number`、`object`、`array[string]`。
- 若声明了 `dependencies`，要确认运行环境实际支持。
- `code_language` 必须和代码内容一致；例如 `python3` 代码不应混入 Ruby、JavaScript 或其他运行时语法。
- 最终审核时，至少做一次与 `code_language` 对应的静态语法检查；若无法执行，要在报告中明确标记未校验。

## 最小骨架

```yaml
data:
  title: Code
  type: code
  variables: []
  code_language: python3
  code: |
    def main():
        return {"result": "ok"}
  outputs:
    result:
      type: string
      children: null
```
