# 贯通性分析

生成 Dify DSL 时，不只检查单个节点字段，还要检查整条链路能否真正跑通。

## 分析顺序

1. 入口分析
2. 上下游字段分析
3. 连边分析
4. 容器节点闭环分析
5. 终点可达分析
6. 变量域分析

## 入口分析

- 普通 `workflow` / `advanced-chat` 通常从 `start` 进入。
- 触发式流程通常从 `trigger-webhook`、`trigger-schedule`、`trigger-plugin` 进入。
- `rag_pipeline` 常从 `datasource` 进入。
- `start` 与 `trigger-*` 默认不要共存。

## 上下游字段分析

对每个节点至少回答:

- 它从哪里拿输入。
- 它对下游暴露哪些输出字段。
- 下游是否真的消费了这些输出。

## 连边分析

- 每个 `source`、`target` 都能映射到真实节点。
- 条件节点的每个分支都应有落点。
- 汇聚节点要检查不同分支输出是否兼容。

## 容器节点闭环分析

### iteration

- `iterator_selector` 必须是数组来源。
- `start_node_id` 必须指向真实 `iteration-start`。
- `output_selector` 必须指向容器内部真实输出。

### loop

- `start_node_id` 必须指向真实 `loop-start`。
- `loop_variables` 必须可初始化。
- `break_conditions` 必须可解析且可能收敛。

## 终点可达分析

- `workflow` 至少有一条路径到 `end`。
- `advanced-chat` 至少有一条路径到 `answer`。
- `rag_pipeline` 至少有一条主路径到 `knowledge-index` 或用户声明的最终处理节点。

## 变量域分析

重点区分:

- `sys.*`
- `start.variables`
- `conversation_variables`
- `environment_variables`
- 容器变量
- 上游节点输出

## 输出建议

在最终 DSL 前先给一段简短贯通性分析，至少包括:

- 入口节点
- 主链路
- 分支链路
- 容器链路
- 终点节点
- 风险点
