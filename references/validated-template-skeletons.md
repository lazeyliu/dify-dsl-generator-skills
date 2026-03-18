# 已验证模板骨架

只收录已由样例索引或参考骨架直接支撑的模板。这里的骨架不是完整成品，而是可填空的最小 DSL 框架。

## 使用规则

- 只把本页模板当作“可直接起手”的骨架。
- 需要更复杂链路时，在骨架上增量修改，不要反向删复杂模板。
- 若需求落不到本页模板，先回到 `templates-library` 与 `template-validation-status` 判断是否只能用推导模板。
- 本页骨架的节点组合来自当前参考体系中的样例索引与骨架归纳，但样例文件本身不一定随仓库一起分发；app DSL 的版本号已按当前导出标准归一化到 `0.6.0`。

## 1. 已验证最小 Chatflow

适用:

- 基础对话输出

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: advanced-chat
  name: your_chatflow
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 80, y: 282 }
        data:
          title: Start
          type: start
          variables: []
      - id: llm_node
        type: custom
        position: { x: 380, y: 282 }
        data:
          title: LLM
          type: llm
          model:
            provider: ""
            name: ""
            mode: chat
          prompt_template:
            - role: system
              text: ""
          context:
            enabled: false
            variable_selector: []
          vision:
            enabled: false
      - id: answer_node
        type: custom
        position: { x: 680, y: 282 }
        data:
          title: Answer
          type: answer
          answer: "{{#llm_node.text#}}"
    edges:
      - id: start-to-llm
        source: start_node
        sourceHandle: source
        target: llm_node
        targetHandle: target
      - id: llm-to-answer
        source: llm_node
        sourceHandle: source
        target: answer_node
        targetHandle: target
```

占位字段说明:

- `app.name`: 填你的应用名，建议用能反映业务目的的短名。
- `llm_node.data.model.provider`: 填模型提供方。
- `llm_node.data.model.name`: 填具体模型名。
- `llm_node.data.prompt_template[0].text`: 填系统提示词。
- `answer_node.data.answer`: 默认直接引用 `{{#llm_node.text#}}`，除非你明确要换成别的上游输出。

## 2. 已验证最小 Workflow

适用:

- 输入一个文本，模型生成一个结构化结果字段

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: workflow
  name: your_workflow
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 30, y: 227 }
        data:
          title: Start
          type: start
          variables:
            - variable: query
              label: query
              type: text-input
              required: true
      - id: llm_node
        type: custom
        position: { x: 334, y: 227 }
        data:
          title: LLM
          type: llm
          model:
            provider: ""
            name: ""
            mode: chat
          prompt_template:
            - role: system
              text: ""
            - role: user
              text: "{{#start_node.query#}}"
          context:
            enabled: false
            variable_selector: []
      - id: end_node
        type: custom
        position: { x: 638, y: 227 }
        data:
          title: End
          type: end
          outputs:
            - variable: answer
              value_type: string
              value_selector: [llm_node, text]
    edges:
      - id: start-to-llm
        source: start_node
        sourceHandle: source
        target: llm_node
        targetHandle: target
      - id: llm-to-end
        source: llm_node
        sourceHandle: source
        target: end_node
        targetHandle: target
```

占位字段说明:

- `app.name`: 填你的 workflow 名称。
- `start_node.data.variables[0].variable`: 填入口字段名。
- `start_node.data.variables[0].label`: 填入口展示名。
- `llm_node.data.model.provider`: 填模型提供方。
- `llm_node.data.model.name`: 填模型名。
- `llm_node.data.prompt_template[*].text`: 填提示词正文。
- `end_node.data.outputs[0].variable`: 填最终输出字段名。
- `end_node.data.outputs[0].value_selector`: 通常保持 `[llm_node, text]`，除非你换了上游输出源。

## 3. 已验证稳定 HTTP 处理链

适用:

- 调外部接口，再解析结果返回

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: workflow
  name: your_http_workflow
  description: ""
  icon: "🔧"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 30, y: 227 }
        data:
          title: Start
          type: start
          variables:
            - variable: url
              label: url
              type: text-input
              required: true
      - id: http_node
        type: custom
        position: { x: 334, y: 227 }
        data:
          title: HTTP Request
          type: http-request
          method: GET
          url: "{{#start_node.url#}}"
          authorization:
            type: no-auth
          headers: ""
          params: ""
          body:
            type: none
            data: []
      - id: tool_node
        type: custom
        position: { x: 638, y: 227 }
        data:
          title: Tool
          type: tool
          provider_id: builtin
          provider_type: builtin
          provider_name: Builtin Tools
          tool_name: json_parse
          tool_label: JSON Parse
          tool_configurations: {}
          tool_parameters:
            json_string:
              type: mixed
              value: "{{#http_node.body#}}"
      - id: end_node
        type: custom
        position: { x: 942, y: 227 }
        data:
          title: End
          type: end
          outputs:
            - variable: status_code
              value_type: number
              value_selector: [http_node, status_code]
            - variable: parsed_data
              value_type: object
              value_selector: [tool_node, result]
    edges:
      - id: start-to-http
        source: start_node
        sourceHandle: source
        target: http_node
        targetHandle: target
      - id: http-to-tool
        source: http_node
        sourceHandle: source
        target: tool_node
        targetHandle: target
      - id: tool-to-end
        source: tool_node
        sourceHandle: source
        target: end_node
        targetHandle: target
```

占位字段说明:

- `start_node.data.variables[0].variable`: 通常是 `url`，也可改成别的请求入口参数。
- `http_node.data.method`: 按接口要求填 `GET`、`POST` 等。
- `http_node.data.url`: 默认引用入口变量，也可改成固定地址。
- `http_node.data.authorization`: 无鉴权就保留 `no-auth`，有鉴权时改成对应配置。
- `tool_node.data.tool_name`: 填你真正要调用的工具。
- `tool_node.data.tool_parameters`: 参数写法要和工具 schema 对齐。
- `end_node.data.outputs`: 按最终要暴露的返回值调整。

## 4. 已验证稳定条件分支

适用:

- 一个入口变量，按规则分流到不同终点

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: workflow
  name: your_branch_workflow
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 30, y: 263 }
        data:
          title: Start
          type: start
          variables:
            - variable: query
              label: query
              type: text-input
              required: true
      - id: if_node
        type: custom
        position: { x: 364, y: 263 }
        data:
          title: IF/ELSE
          type: if-else
          cases:
            - case_id: "true"
              logical_operator: and
              conditions:
                - variable_selector: [start_node, query]
                  comparison_operator: contains
                  value: hello
                  varType: string
      - id: end_true
        type: custom
        position: { x: 766, y: 161 }
        data:
          title: End True
          type: end
          outputs:
            - variable: "true"
              value_type: string
              value_selector: [start_node, query]
      - id: end_false
        type: custom
        position: { x: 766, y: 363 }
        data:
          title: End False
          type: end
          outputs:
            - variable: "false"
              value_type: string
              value_selector: [start_node, query]
    edges:
      - id: start-to-if
        source: start_node
        sourceHandle: source
        target: if_node
        targetHandle: target
      - id: if-true-to-end
        source: if_node
        sourceHandle: "true"
        target: end_true
        targetHandle: target
      - id: if-false-to-end
        source: if_node
        sourceHandle: "false"
        target: end_false
        targetHandle: target
```

占位字段说明:

- `start_node.data.variables[0].variable`: 填待判断的入口变量名。
- `if_node.data.cases[0].conditions[0].comparison_operator`: 填判断方式，如 `contains`、`=`。
- `if_node.data.cases[0].conditions[0].value`: 填分支命中值。
- `end_true.data.outputs[0].variable`: 填 true 分支输出字段名。
- `end_false.data.outputs[0].variable`: 填 false 分支输出字段名。

## 5. 已验证稳定多分支聚合

适用:

- 多分支结果需要统一汇聚

骨架:

```text
start -> if-else(多组) -> template-transform/code -> variable-aggregator -> end
```

最小落地规则:

- 至少两个分支节点
- 至少两个上游输出进入 `variable-aggregator`
- `end` 只读聚合结果

占位字段说明:

- 每个分支节点的输出字段要统一命名或至少统一类型。
- `variable-aggregator.output_type`: 按最终结果填数组、对象或字符串。
- `end.outputs[*].value_selector`: 指向聚合节点输出，而不是某一条分支的临时结果。

## 6. 已验证稳定 Iteration

适用:

- 数组逐项处理后输出汇总结果

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: workflow
  name: your_iteration_workflow
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 80, y: 282 }
        data:
          title: Start
          type: start
          variables: []
      - id: code_node
        type: custom
        position: { x: 384, y: 282 }
        data:
          title: Code
          type: code
          code_language: python3
          code: |
            def main():
                return {"result": [1, 2, 3]}
          variables: []
          outputs:
            result:
              type: array[number]
              children: null
      - id: iteration_node
        type: custom
        position: { x: 684, y: 282 }
        data:
          title: Iteration
          type: iteration
          iterator_selector: [code_node, result]
          output_selector: [template_node, output]
          output_type: array[string]
          start_node_id: iteration_start
          is_parallel: false
          parallel_nums: 10
          error_handle_mode: terminated
      - id: iteration_start
        type: custom-iteration-start
        data:
          title: ""
          type: iteration-start
      - id: template_node
        type: custom
        data:
          title: Template
          type: template-transform
          template: "output: {{ arg1 }}"
          variables:
            - variable: arg1
              value_selector: [iteration_node, item]
              value_type: string
      - id: end_node
        type: custom
        position: { x: 1080, y: 282 }
        data:
          title: End
          type: end
          outputs:
            - variable: output
              value_type: array[string]
              value_selector: [iteration_node, output]
```

占位字段说明:

- `code_node.data.code`: 填生成数组的代码。
- `code_node.data.outputs.result.type`: 填数组输出类型。
- `iteration_node.data.iterator_selector`: 指向数组来源。
- `iteration_node.data.output_selector`: 指向容器内最终输出节点。
- `template_node.data.template`: 填每个元素的格式化模板。
- `template_node.data.variables[0].value_selector`: 通常指向 `[iteration_node, item]`。
- `end_node.data.outputs[0].value_selector`: 通常指向迭代容器输出。

## 7. 已验证稳定 Loop

适用:

- 循环更新变量直到满足退出条件

骨架:

```yaml
kind: app
version: 0.6.0
app:
  mode: workflow
  name: your_loop_workflow
  description: ""
  icon: "🤖"
  icon_background: "#FFEAD5"
  use_icon_as_answer_icon: false
dependencies: []
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    nodes:
      - id: start_node
        type: custom
        position: { x: 30, y: 303 }
        data:
          title: Start
          type: start
          variables: []
      - id: loop_node
        type: custom
        position: { x: 334, y: 303 }
        data:
          title: Loop
          type: loop
          loop_count: 10
          logical_operator: and
          break_conditions:
            - variable_selector: [loop_node, num]
              comparison_operator: "≥"
              value: "5"
              varType: number
          loop_variables:
            - label: num
              var_type: number
              value_type: constant
              value: 1
          start_node_id: loop_start
      - id: loop_start
        type: custom-loop-start
        data:
          title: ""
          type: loop-start
      - id: assigner_node
        type: custom
        data:
          title: Variable Assigner
          type: assigner
          version: "2"
          items:
            - variable_selector: [loop_node, num]
              input_type: constant
              operation: +=
              value: 1
      - id: end_node
        type: custom
        position: { x: 902, y: 303 }
        data:
          title: End
          type: end
          outputs:
            - variable: num
              value_type: number
              value_selector: [loop_node, num]
```

占位字段说明:

- `loop_node.data.loop_count`: 填最大循环次数，避免无限循环。
- `loop_node.data.break_conditions[*]`: 填退出条件。
- `loop_node.data.loop_variables[*]`: 填循环变量初始值。
- `assigner_node.data.items[*].operation`: 填循环内变量更新方式。
- `end_node.data.outputs[*].value_selector`: 指向循环结束后的稳定变量。

## 8. 已验证稳定文档入库

适用:

- 文档抽取、分块、写入知识库

骨架:

```text
datasource -> if-else(file type) -> document-extractor/tool -> variable-aggregator -> chunk tool -> knowledge-index
```

最小落地规则:

- `kind: rag_pipeline`
- 必须有 `rag_pipeline` 顶层块
- 必须有 `datasource`
- 必须有 `knowledge-index`
- 中间至少有一个文本抽取或分块步骤

占位字段说明:

- `datasource`: 选本次文档来源类型。
- `if-else(file type)`: 只有混合文件类型时才需要。
- `document-extractor/tool`: 二选一或组合，用于拿到可分块文本。
- `variable-aggregator`: 用于统一不同来源的文本结果。
- `tool/chunker`: 填具体分块工具或转换工具。
- `knowledge-index.chunk_structure`: 与分块结果结构保持一致。
- `knowledge-index.index_chunk_variable_selector`: 指向分块后的最终结果。

## 使用要求

- 只把本页骨架用于 `template-validation-status` 中标记为 `已由样例索引直接支撑` 的模板。
- 对 `间接验证` 或 `推导` 模板，不要直接复制成本页骨架后宣称“已验证”。
