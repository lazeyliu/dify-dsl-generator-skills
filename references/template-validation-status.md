# 模板源码校验状态

这份文档只回答一件事: 某个模板是否能在当前参考体系中找到样例索引或结构支撑。

## 标记规则

- `已由样例索引直接支撑`
  当前参考体系中存在同类型样例名称或样例索引记录，但这些样例文件不一定随仓库一起分发。

- `已由模板结构间接支撑`
  当前仓库中没有完全同名样例文件，但存在非常接近的链路组合或骨架，可支撑该模板。

- `基于节点能力推导`
  当前仓库中没有直接样例或索引支撑，只能基于节点能力和约束推导，不应宣称为“已验证模板”。

## templates-library 校验结果

### 已由样例索引直接支撑

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

### 已由模板结构间接支撑

- RAG 问答模板
  说明:
  当前参考体系中能看到 `knowledge-retrieval` 节点定义，但没有现成的完整 `start -> knowledge-retrieval -> llm -> answer` 样例文件。

### 基于节点能力推导

- 审批链模板
  说明:
  当前参考体系中能看到 `human-input` 节点定义与测试说明，但没有现成完整审批链样例文件。

- Webhook 触发模板
  说明:
  当前参考体系中能看到 trigger 节点定义，但未发现完整 `trigger-webhook -> ...` 样例文件。

- 定时任务模板
  说明:
  当前参考体系中能看到 trigger 节点定义，但未发现完整 `trigger-schedule -> ...` 样例文件。

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

- 这些变体体现的是设计策略，不是当前仓库里附带的一比一样例文件。

## 使用要求

生成时必须明确标记模板来源:

- 已验证
- 间接验证
- 推导

如果用户要求“精准无误”，优先使用 `已由样例索引直接支撑` 的模板和变体；如果当前仓库未附带对应样例文件，要在报告里明确这一点。
