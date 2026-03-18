# 决策表

遇到问题时，优先用决策表选节点，而不是直接凭直觉。

## 文本生成

- 需要自然语言生成: `llm`
- 需要简单文本拼接: `template-transform`
- 需要最终回复用户: `answer`

## 条件判断

- 明确规则判断: `if-else`
- 需要模型分类: `question-classifier`

## 数据处理

- 自定义结构化逻辑: `code`
- 调外部能力: `tool`
- 调 HTTP 服务: `http-request`

## 变量处理

- 更新变量: `assigner`
- 聚合多个输出: `variable-aggregator`
- 处理列表: `list-operator`

## 批量处理

- 遍历数组: `iteration`
- 直到满足条件: `loop`

## 知识相关

- 查询知识库: `knowledge-retrieval`
- 文档抽取: `document-extractor`
- 写入索引: `knowledge-index`

## 入口选择

- 用户手动输入: `start`
- 外部事件: `trigger-*`
- 知识导入入口: `datasource`
