# 编排模式说明

生成 Dify DSL 时，先判断属于哪一种编排模式，再决定入口、终点、节点组合和审核重点。

## 1. workflow 模式

### 适用场景

- 需要产出结构化结果
- 需要多步骤处理
- 需要显式分支、循环、工具调用

### 典型入口

- `start`

### 典型终点

- `end`

### 常用节点

- `start`
- `if-else`
- `code`
- `http-request`
- `tool`
- `assigner`
- `iteration`
- `loop`
- `end`

### 生成重点

- `end.outputs` 必须完整
- 所有中间变量都能被终点消费
- 多分支汇聚时要检查输出兼容性

## 2. advanced-chat 模式

### 适用场景

- 需要对话式输出
- 需要结合对话变量和上下文
- 需要直接给用户返回文本

### 典型入口

- `start`

### 典型终点

- `answer`

### 常用节点

- `start`
- `llm`
- `knowledge-retrieval`
- `template-transform`
- `question-classifier`
- `answer`

### 生成重点

- `answer.answer` 必须能引用真实上游文本
- `conversation_variables` 要与写入和读取逻辑一致
- 多个 `answer` 时要检查输出顺序和依赖关系

## 3. rag-pipeline 模式

### 适用场景

- 需要导入文档
- 需要清洗、分块、索引
- 需要构建知识库导入链路

### 典型入口

- `datasource`

### 典型终点

- `knowledge-index`

### 常用节点

- `datasource`
- `document-extractor`
- `if-else`
- `tool`
- `variable-aggregator`
- `knowledge-index`

### 生成重点

- `kind` 必须是 `rag_pipeline`
- `rag_pipeline` 顶层块必须完整
- `knowledge-index` 的 `chunk_structure`、`indexing_technique`、`retrieval_model` 要和上游输出匹配

## 4. 触发式模式

### 适用场景

- 需要由外部事件触发
- 需要 webhook、定时或插件事件入口

### 典型入口

- `trigger-webhook`
- `trigger-schedule`
- `trigger-plugin`

### 典型终点

- `end`
- `answer`
- 业务处理节点后的显式终点

### 常用节点

- `trigger-webhook`
- `trigger-schedule`
- `trigger-plugin`
- `if-else`
- `tool`
- `code`
- `end`

### 生成重点

- 不要和 `start` 混成双入口
- 入口参数定义要和下游消费字段一致
- 要明确失败路径和响应路径

## 5. 容器编排模式

### 适用场景

- 需要批量遍历
- 需要循环直到满足条件

### 子模式

- `iteration`
- `loop`

### 生成重点

- 容器本体与内部起点节点必须成套出现
- 容器内部边必须闭合
- 容器输出必须可被容器外节点消费

## 选型建议

- 只需要结构化结果，用 `workflow`
- 只需要对话回复，用 `advanced-chat`
- 需要知识入库，用 `rag-pipeline`
- 需要外部事件启动，用触发式模式
- 需要重复处理数组或状态，用容器编排模式
