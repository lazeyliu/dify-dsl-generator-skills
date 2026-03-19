# list-operator 节点

## 作用

对列表做筛选、排序、截断、抽取。

## 必填字段

- `type: list-operator`: 指定当前节点是列表处理节点。
- `variable`: 指向要处理的数组来源。
- `filter_by`: 定义过滤规则；即便不启用，也要有稳定结构。
- `order_by`: 定义排序规则；即便不启用，也要有稳定结构。
- `limit`: 定义截断规则；即便不启用，也要有稳定结构。

## 选填字段

- `extract_by`: 需要从列表中进一步抽取指定序号或子项时填写。

`order_by.value` 常见值说明:

- `asc`: 升序排列。
- `desc`: 降序排列。

## 贯通性分析

- 上游必须提供数组型输入。
- 下游常接 `end`、`template-transform`、`code` 或另一个列表处理节点。
- 关键是经过过滤、排序、截断后，下游是否仍然接受当前列表形态。

## 可承接上游节点

### 推荐

- `code`
- `tool`
- `knowledge-retrieval`
- `iteration`

### 可用但需人工确认

- `variable-aggregator`
- `loop`
- 其他能输出数组的节点

### 不推荐

- `start`
- 任意 `trigger-*`
- `answer`

## 可衔接下游节点

### 推荐

- `end`
- `template-transform`
- `code`
- 另一个 `list-operator`

### 可用但需人工确认

- `llm`
- `variable-aggregator`

### 不推荐

- `start`
- 任意 `trigger-*`

## 编排约束

- `variable` 应引用数组类型上游输出。
- 即便不启用过滤、排序或截断，也要提供对应对象结构。
- `extract_by.enabled` 为 true 时要确认提取序号是否合理。

## 最小骨架

```yaml
data:
  title: List Operator
  type: list-operator
  variable: [code, result]
  filter_by:
    enabled: false
    conditions: []
  order_by:
    enabled: false
    key: ""
    value: asc
  limit:
    enabled: false
    size: -1
```
