# 失败输出与空输出处理

生成或调整编排时，不能只看成功输出，还要提前考虑空输出、异常输出和失败恢复路径。

## 1. LLM 节点

常见风险:

- `text` 为空
- 结构化输出不符合预期
- 推理内容存在但主文本为空

下游建议:

- 接 `answer` 前先确认 `text` 是否一定存在
- 接 `if-else` 时避免直接拿可能为空的字段做硬判断
- 需要兜底时优先接 `assigner` 或失败分支

## 2. HTTP Request 节点

常见风险:

- 非 2xx 状态码
- `body` 为空
- 返回格式与预期不一致
- 超时

下游建议:

- 先接 `if-else` 判断 `status_code`
- 再决定是否进入 `tool`、`code` 或 `end`
- 对关键外部依赖建议补 timeout 和兜底路径

## 3. Tool 节点

常见风险:

- 工具返回空结果
- 工具输出字段不稳定
- 工具抛异常

下游建议:

- 对动态工具结果优先接 `code` 或 `if-else` 做归一化
- 不要直接把不稳定输出接到 `answer`

## 4. Code 节点

常见风险:

- 返回值字段和 `outputs` 声明不一致
- 返回 `null`
- 运行异常

下游建议:

- 在 `end` 前确认关键字段一定存在
- 对不稳定输出优先接 `if-else`、`assigner` 或默认值逻辑

## 5. Knowledge Retrieval 节点

常见风险:

- 检索结果为空
- 召回文本过少
- 附件检索失败

下游建议:

- 进入 `llm` 前考虑空检索分支
- 需要显式兜底时可接 `if-else` 或模板节点

## 6. Document Extractor / Knowledge Index

常见风险:

- 抽取文本为空
- 分块结果不符合索引结构
- 索引阶段缺少必要配置

下游建议:

- `knowledge-index` 前优先确认输入块存在
- 对空抽取结果不要直接落索引

## 7. Human Input 节点

常见风险:

- 超时
- 用户未提交
- 提交字段缺失

下游建议:

- 对 timeout 路径单独建恢复策略
- 不要假设所有表单字段都一定有值

## 8. Iteration / Loop

常见风险:

- 单项失败
- 容器输出为空
- 循环不收敛

下游建议:

- 明确 `error_handle_mode`
- 容器后接 `end` 前确认输出是否一定存在

## 9. Answer / End

常见风险:

- 引用字段为空
- 输出字段选择器失效

下游建议:

- `answer` 前优先确认上游文本字段稳定
- `end` 前优先确认所有 `value_selector` 都可达

## 通用策略

优先考虑下面几种兜底手段:

- `if-else` 分流
- `assigner` 写默认值
- `default_value`
- `retry_config`
- `human-input`
- 终点前做格式归一化
