# if-else 节点

## 作用

做显式条件分支。

## 必填字段

- `type: if-else`: 指定当前节点是显式条件分支节点。
- `cases`: 推荐使用的分支定义集合，用来描述每个命中分支的条件。

`cases[*]` 最少需要:

- `case_id`: 分支标识，也常用于边的句柄匹配。
- `logical_operator`: 多条件之间的组合方式，例如 `and` 或 `or`。
- `conditions`: 分支命中条件集合，决定流程走向。

旧字段 `conditions` 仍存在，但已是兼容路径，不建议新建 DSL 继续使用。

## 选填字段

- `title`: 需要区分多个分支节点时填写。
- `desc`: 需要补充分支业务含义时填写。
- `version`: 需要固定某种兼容写法时填写。
- 顶层 `logical_operator`: 旧兼容字段。当前新写法应优先把逻辑组合关系写在 `cases[*].logical_operator` 中。

## 贯通性分析

- 上游常接 `start`、`llm`、`tool`、`knowledge-retrieval`。
- 下游是多分支节点，常接 `code`、`llm`、`tool`、`end`。
- 关键是检查每个分支是否都有出口，以及是否存在默认未覆盖路径。

## 可承接上游节点

### 推荐

- `start`
- `llm`
- `tool`
- `knowledge-retrieval`
- `assigner`
- `code`

### 可用但需人工确认

- `template-transform`
- `list-operator`
- `parameter-extractor`

### 不推荐

- `end`
- `answer`
- 任意 `trigger-*`

## 可衔接下游节点

### 推荐

- `code`
- `llm`
- `tool`
- `end`
- `template-transform`
- `variable-aggregator`

### 可用但需人工确认

- `answer`
- `assigner`
- `human-input`
- `knowledge-index`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- 边的 `sourceHandle` 要与 `case_id` 或布尔分支句柄保持一致。
- 每个条件都要有可解析的变量选择器和比较值。
- 顶层 `conditions` 与顶层 `logical_operator` 主要用于兼容导入；新建 DSL 不建议继续作为主结构使用。
- 如果没有显式 false/default 路径，要在报告里说明未覆盖分支。

## 最小骨架

```yaml
data:
  title: IF/ELSE
  type: if-else
  cases:
    - case_id: "true"
      logical_operator: and
      conditions:
        - variable_selector: [start, switch]
          comparison_operator: "="
          value: "1"
          varType: number
```
