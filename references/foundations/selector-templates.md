# 选择器模板手册

用于减少 `value_selector`、`variable_selector`、模板引用写错的概率。

## 1. 模板引用基础写法

### 引用 start 输入

```text
{{#start.query#}}
{{#start.file#}}
```

适用:

- `llm.prompt_template`
- `template-transform.template`
- `tool_parameters`
- `http-request.url`

### 引用普通节点输出

```text
{{#llm.text#}}
{{#code.result#}}
{{#http_request.body#}}
{{#tool.result#}}
```

适用:

- `answer.answer`
- `template-transform.template`
- `tool_parameters`
- `http-request.body`

### 引用共享变量域

```text
{{#conversation.answer#}}
{{#env.api_key#}}
{{#sys.query#}}
{{#sys.files#}}
```

适用:

- 对话变量
- 环境变量
- 系统变量

## 2. value_selector 基础模板

### 引用 start 输入

```yaml
value_selector: [start, query]
value_selector: [start, file]
```

### 引用普通节点输出

```yaml
value_selector: [llm, text]
value_selector: [code, result]
value_selector: [tool, result]
value_selector: [http_node, status_code]
```

### 引用嵌套字段

```yaml
value_selector: [http_node, body]
value_selector: [knowledge_node, result, 0, content]
value_selector: [datasource_node, output, extension]
```

说明:

- 嵌套对象和数组路径必须和真实输出结构一致。

## 3. variable_selector 基础模板

### 读取系统变量

```yaml
variable_selector: [sys, query]
variable_selector: [sys, files]
```

### 读取入口变量

```yaml
variable_selector: [start, query]
variable_selector: [start, switch]
```

### 读取对话变量

```yaml
variable_selector: [conversation, answer]
variable_selector: [conversation, summary]
```

### 读取节点输出

```yaml
variable_selector: [llm, text]
variable_selector: [tool, result]
variable_selector: [code, items]
```

## 4. query_variable_selector 模板

### 检索节点

```yaml
query_variable_selector: [sys, query]
query_variable_selector: [start, question]
```

### 分类节点

```yaml
query_variable_selector: [sys, query]
query_variable_selector: [template_node, text]
```

## 5. iterator_selector / output_selector 模板

### iteration 输入

```yaml
iterator_selector: [code, items]
iterator_selector: [tool, result]
iterator_selector: [knowledge_retrieval, result]
```

### iteration 输出

```yaml
output_selector: [code_in_iter, result]
output_selector: [assigner_in_iter, result]
```

## 6. index_chunk_variable_selector 模板

```yaml
index_chunk_variable_selector: [general_chunker_tool, result]
index_chunk_variable_selector: [tool_node, result]
index_chunk_variable_selector: [aggregator, output]
```

适用:

- `knowledge-index`

## 7. tool_parameters 模板

### 变量型

```yaml
tool_parameters:
  query:
    type: variable
    value: [start, query]
```

### 混合模板型

```yaml
tool_parameters:
  text:
    type: mixed
    value: "{{#llm.text#}}"
```

### 常量型

```yaml
tool_parameters:
  limit:
    type: constant
    value: 10
```

## 8. datasource_parameters 模板

```yaml
datasource_parameters:
  url:
    type: mixed
    value: "{{#rag.datasource_node.url#}}"
```

或

```yaml
datasource_parameters:
  limit:
    type: variable
    value: [rag, datasource_node, limit]
```

## 9. assigner.items 模板

### 写入变量值

```yaml
items:
  - variable_selector: [conversation, answer]
    input_type: variable
    operation: over-write
    value: [llm, text]
```

### 写入常量

```yaml
items:
  - variable_selector: [conversation, status]
    input_type: constant
    operation: over-write
    value: approved
```

## 10. end.outputs 模板

### 文本结果

```yaml
outputs:
  - variable: answer
    value_type: string
    value_selector: [llm, text]
```

### 对象结果

```yaml
outputs:
  - variable: parsed_data
    value_type: object
    value_selector: [tool, result]
```

### 数组结果

```yaml
outputs:
  - variable: items
    value_type: array[object]
    value_selector: [iteration_node, result]
```

## 11. 常见错误

- 把 `{{#...#}}` 写成普通字符串
- `value_selector` 指向不存在字段
- 容器输出选择器指向容器外节点
- `assigner.value` 用了模板字符串，但 `input_type` 不是 `mixed`
- `tool_parameters` 用变量写法却传了字符串

## 12. 使用建议

生成前先确认:

1. 这个字段需要模板字符串还是选择器数组
2. 上游节点真实输出字段名是什么
3. 变量是在系统域、对话域、环境域还是节点输出域
