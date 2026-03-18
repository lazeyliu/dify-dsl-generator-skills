# 模板源码校验状态

这份文档只回答一件事: 某个模板是否能在现有本地源码中找到直接样例支撑。

## 标记规则

- `已由源码样例直接验证`
  当前本地源码里存在同类型 fixture 或导出模板。

- `已由源码模板间接验证`
  本地源码里没有完全同名样例，但存在非常接近的链路组合，可支撑该模板。

- `基于节点能力推导`
  本地源码里没有直接样例，只能基于节点能力和约束推导，不应宣称为“已验证模板”。

## templates-library 校验结果

### 已由源码样例直接验证

- 基础 Chatflow 模板
  参考: `basic_chatflow.yml`

- 基础 Workflow 模板
  参考: `basic_llm_chat_workflow.yml`、`simple_passthrough_workflow.yml`

- HTTP 处理链模板
  参考: `http_request_with_json_tool_workflow.yml`

- 条件分支模板
  参考: `conditional_parallel_code_execution_workflow.yml`、`conditional_hello_branching_workflow.yml`

- 多分支聚合模板
  参考: `dual_switch_variable_aggregator_workflow.yml`

- 变量更新模板
  参考: `test_streaming_conversation_variables.yml`、`update-conversation-variable-in-iteration.yml`

- Iteration 模板
  参考: `array_iteration_formatting_workflow.yml`、`iteration_flatten_output_enabled_workflow.yml`

- Loop 模板
  参考: `increment_loop_with_break_condition_workflow.yml`、`search_dify_from_2023_to_2025.yml`

- 文档入库模板
  参考: `file-general-economy.yml`、`file-parentchild.yml`、`notion-general-high-quality.yml`

### 已由源码模板间接验证

- RAG 问答模板
  说明:
  当前本地源码里能看到 `knowledge-retrieval` 节点定义，但没有现成的完整 `start -> knowledge-retrieval -> llm -> answer` fixture。

### 基于节点能力推导

- 审批链模板
  说明:
  本地源码能看到 `human-input` 节点定义与测试，但没有现成完整审批链 fixture。

- Webhook 触发模板
  说明:
  本地源码能看到 trigger 节点定义，但未发现完整 `trigger-webhook -> ...` fixture。

- 定时任务模板
  说明:
  本地源码能看到 trigger 节点定义，但未发现完整 `trigger-schedule -> ...` fixture。

## template-variants 校验结果

### 可直接宣称为“已验证变体”的范围

- 最小版 Chatflow
- 最小版/稳定版 Workflow
- 稳定版 HTTP 处理链
- 稳定版 条件分支
- 稳定版 多分支聚合
- 稳定版 Iteration
- 稳定版 Loop
- 稳定版 文档入库

### 只能宣称为“能力推导变体”的范围

- 低成本版 与 高质量版的大多数变体
- 所有审批链变体
- 所有 trigger 变体
- RAG 问答变体

原因:

- 这些变体体现的是设计策略，不是本地源码中已有的一比一样例。

## 使用要求

生成时必须明确标记模板来源:

- 已验证
- 间接验证
- 推导

如果用户要求“精准无误”，优先使用 `已由源码样例直接验证` 的模板和变体。
