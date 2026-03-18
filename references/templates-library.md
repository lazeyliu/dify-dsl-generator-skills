# 典型编排模板库

这份文档提供高频可复用的编排骨架。使用时先选最接近的模板，再按节点、字段、变量和选择器做局部调整。

## 1. 基础 Chatflow 模板

### 适用场景

- 简单问答
- 单轮或轻上下文对话
- 直接返回文本结果

### 推荐骨架

```text
start -> llm -> answer
```

### 推荐节点

- `start`
- `llm`
- `answer`

### 关键字段

- `llm.model`
- `llm.prompt_template`
- `answer.answer`

### 常见调整点

- 加 `memory`
- 加 `knowledge-retrieval`
- 加 `template-transform`

### 风险点

- `answer` 引用了不存在的 `llm.text`
- prompt 依赖变量未补齐

## 2. 基础 Workflow 模板

### 适用场景

- 需要结构化输出
- 需要 API 结果或工具结果回传

### 推荐骨架

```text
start -> code/tool/http-request -> end
```

### 推荐节点

- `start`
- `code` 或 `tool` 或 `http-request`
- `end`

### 关键字段

- 中间节点输出字段
- `end.outputs`

### 常见调整点

- 在中间加入 `if-else`
- 在末端前加 `template-transform`

### 风险点

- `end.value_selector` 指向错误
- 中间节点返回结构和 `end` 不匹配

## 3. HTTP 处理链模板

### 适用场景

- 调外部接口
- 对响应做解析再输出

### 推荐骨架

```text
start -> http-request -> tool/code -> end
```

### 推荐节点

- `start`
- `http-request`
- `tool` 或 `code`
- `end`

### 常见调整点

- 先用 `if-else` 判断 `status_code`
- 失败时走兜底分支

### 风险点

- 外部接口超时
- `body` 格式和解析节点不匹配

## 4. 条件分支模板

### 适用场景

- 明确规则分流
- 多输出路径处理

### 推荐骨架

```text
start -> if-else -> branch_a/branch_b -> end
```

### 推荐节点

- `start`
- `if-else`
- `code` / `tool` / `llm`
- `end`

### 常见调整点

- 分支后使用 `variable-aggregator` 汇总
- 某个分支直接终点输出

### 风险点

- 分支无落点
- 多分支结果汇总不兼容

## 5. 多分支聚合模板

### 适用场景

- 多路结果需要统一输出
- 多个工具或多分支并行产出结果

### 推荐骨架

```text
start -> if-else/并行节点 -> variable-aggregator -> end
```

### 推荐节点

- `if-else`
- `code`
- `tool`
- `variable-aggregator`
- `end`

### 常见调整点

- 聚合后接 `template-transform`
- 聚合后接 `knowledge-index`

### 风险点

- 聚合前各路输出类型不一致

## 6. 变量更新模板

### 适用场景

- 需要更新对话变量
- 需要维护中间状态

### 推荐骨架

```text
start -> llm/tool -> assigner -> answer/end
```

### 推荐节点

- `assigner`

### 常见调整点

- 把 `assigner` 放到 `iteration` 或 `loop` 内部

### 风险点

- 写入变量域不正确
- 写入后下游未消费

## 7. Iteration 模板

### 适用场景

- 批量处理数组
- 对每个元素重复执行相同逻辑

### 推荐骨架

```text
start/code/tool -> iteration -> end/template-transform
```

### 容器内部骨架

```text
iteration-start -> code/tool/assigner
```

### 常见调整点

- 开启并行
- 设置错误处理模式

### 风险点

- 输入不是数组
- 容器输出选择器写错

## 8. Loop 模板

### 适用场景

- 直到满足条件才结束
- 需要维护循环变量

### 推荐骨架

```text
start -> loop -> end
```

### 容器内部骨架

```text
loop-start -> assigner/code -> loop
```

### 常见调整点

- 增加更多循环变量
- 让循环结果进入 `llm`

### 风险点

- break 条件不收敛
- 循环变量不可写

## 9. RAG 问答模板

### 适用场景

- 基于知识库回答用户问题

### 推荐骨架

```text
start -> knowledge-retrieval -> llm -> answer
```

### 推荐节点

- `knowledge-retrieval`
- `llm`
- `answer`

### 常见调整点

- 检索前加 `template-transform`
- 检索后加 `if-else` 处理空结果

### 风险点

- 检索为空却直接喂给 `llm`

## 10. 文档入库模板

### 适用场景

- 文档上传
- 文本抽取
- 分块并入知识库

### 推荐骨架

```text
datasource -> document-extractor/tool -> variable-aggregator -> tool/chunker -> knowledge-index
```

### 推荐节点

- `datasource`
- `document-extractor`
- `variable-aggregator`
- `tool`
- `knowledge-index`

### 常见调整点

- 先用 `if-else` 区分不同文件类型
- 切换 `text_model` / `hierarchical_model`

### 风险点

- 上游块结构和 `knowledge-index` 不匹配

## 11. 审批链模板

### 适用场景

- 需要人工确认后再继续

### 推荐骨架

```text
llm/tool/code -> human-input -> assigner/if-else -> end/answer
```

### 推荐节点

- `human-input`
- `assigner`
- `if-else`

### 常见调整点

- 超时走另一条分支
- 邮件和站内双投递

### 风险点

- 表单字段和下游恢复路径不一致

## 12. Webhook 触发模板

### 适用场景

- 外部系统推送数据触发流程

### 推荐骨架

```text
trigger-webhook -> if-else/code/tool -> end
```

### 常见调整点

- 先验签或校验参数
- 再调用工具或代码处理

### 风险点

- 入口参数定义和下游字段消费不一致

## 13. 定时任务模板

### 适用场景

- 定时轮询
- 定时同步
- 定时汇总

### 推荐骨架

```text
trigger-schedule -> http-request/tool/code -> end
```

### 风险点

- cron/visual 模式配置错误
- 任务幂等性不足

## 14. 选择模板的方法

1. 先看目标是输出文本、输出结构化结果、写知识库还是触发外部流程。
2. 再看入口是用户输入、外部事件还是数据源。
3. 再看是否需要分支、容器、人工确认。
4. 最后从最短模板开始，只在必要处加节点。
