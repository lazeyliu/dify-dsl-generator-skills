# 常见输出字段字典

用于在编排时快速判断“一个节点通常会产出什么字段”，以及下游该接什么。

## 1. start

常见输出:

- `start.<variable>`: 每个入口变量都会按变量名暴露到下游。

常见引用:

- `{{#start.query#}}`
- `value_selector: [start, query]`

## 2. llm

常见输出:

- `text`: 主文本输出
- `reasoning_content`: 推理内容，启用对应能力时常见

常见下游:

- `answer`
- `end`
- `template-transform`
- `if-else`

## 3. code

常见输出:

- 由 `outputs` 中声明的字段决定，例如:
  - `result`
  - `items`
  - `status`

常见下游:

- `end`
- `iteration`
- `loop`
- `template-transform`

## 4. http-request

常见输出:

- `status_code`
- `headers`
- `body`
- `text`
- 文件响应时的文件型输出

常见下游:

- `tool`
- `code`
- `if-else`
- `end`

## 5. tool

常见输出:

- 工具返回的主结果字段，常见是:
  - `result`
  - `text`
  - `documents`
  - `images`

注意:

- 实际输出字段受具体工具定义影响。

## 6. template-transform

常见输出:

- 通常是模板拼装后的文本结果

常见下游:

- `llm`
- `answer`
- `http-request`

## 7. knowledge-retrieval

常见输出:

- 检索结果集合
- 文本片段
- 文档片段元信息

常见下游:

- `llm`
- `answer`
- `template-transform`
- `end`

## 8. document-extractor

常见输出:

- 提取后的文本
- 文档结构化内容

常见下游:

- `variable-aggregator`
- `tool`
- `knowledge-index`

## 9. variable-aggregator

常见输出:

- 按顺序选择到的首个非空结果
- 启用分组时，每组各自选择到的首个非空结果

常见下游:

- `end`
- `template-transform`
- `knowledge-index`

## 10. assigner

常见输出:

- 它的核心价值不是产出新字段，而是更新变量域。

常见影响:

- 后续节点读取到被改写的变量值。

## 11. list-operator

常见输出:

- 过滤、排序、截断后的列表

常见下游:

- `code`
- `template-transform`
- `end`

## 12. parameter-extractor

常见输出:

- 每个参数名对应的抽取结果
- 常见还会带成功与失败相关字段

常见下游:

- `if-else`
- `assigner`
- `end`

## 13. question-classifier

常见输出:

- 分类结果
- 命中的类别标识

常见下游:

- 分支边
- `if-else`
- `end`

## 14. human-input

常见输出:

- 表单输入字段
- 用户动作 ID

常见下游:

- `assigner`
- `if-else`
- `end`

## 15. iteration / loop

常见输出:

- 容器汇总结果
- 容器变量结果

常见下游:

- `end`
- `template-transform`
- `llm`
- `variable-aggregator`

## 16. knowledge-index

常见输出:

- 通常不作为普通业务输出节点使用。
- 它更像主链路尾部动作，而不是供下游消费的数据节点。

## 使用方式

编排时先确认三件事:

1. 确认上游节点能输出什么字段
2. 确认下游节点需要什么字段
3. 确认选择器是否准确指向那个字段
