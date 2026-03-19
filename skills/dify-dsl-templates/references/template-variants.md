# 模板变体库

同一种编排模板，不同目标下应使用不同变体。默认按下面四类变体选型。

## 1. 最小版

### 目标

- 节点最少
- 先快速跑通
- 方便做最小验证

### 特征

- 只保留主链路
- 很少加兜底
- 很少加中间归一化节点
- 很少加人工确认

### 适用场景

- PoC
- 冒烟验证
- 先搭骨架再细化

### 风险

- 稳定性弱
- 空输出和异常路径覆盖不足

## 2. 稳定版

### 目标

- 主链路稳定
- 失败路径清楚
- 便于维护

### 特征

- 有明确终点
- 有必要的 `if-else`
- 外部依赖前后有检查
- 关键字段有兜底

### 适用场景

- 日常生产编排
- 需要长期维护的链路

### 风险

- 节点数会比最小版多

## 3. 低成本版

### 目标

- 降低 LLM 和工具调用成本
- 降低整体运行费用

### 特征

- 能不用 `llm` 就不用
- 优先用 `template-transform`
- 优先用 `if-else`
- 减少重复检索和重复工具调用

### 适用场景

- 高频调用
- 成本敏感场景

### 风险

- 灵活性下降
- 输出质量可能不如高质量版

## 4. 高质量版

### 目标

- 结果质量优先
- 解释性更强
- 允许更复杂链路

### 特征

- 允许增加 `knowledge-retrieval`
- 允许增加多步 `llm`
- 允许增加归一化、校验和人工确认
- 对失败路径要求更完整

### 适用场景

- 高价值问答
- 高价值审批
- 高价值知识处理

### 风险

- 成本更高
- 延迟更高

## 5. Chatflow 变体

### 最小版

```text
start -> llm -> answer
```

### 稳定版

```text
start -> knowledge-retrieval/template-transform -> llm -> if-else -> answer
```

### 低成本版

```text
start -> template-transform -> answer
```

说明:

- 只适合固定回复或轻模板生成。

### 高质量版

```text
start -> knowledge-retrieval -> llm -> assigner -> human-input/answer
```

## 6. Workflow 变体

### 最小版

```text
start -> code/tool -> end
```

### 稳定版

```text
start -> if-else -> code/tool -> end
```

### 低成本版

```text
start -> code -> end
```

### 高质量版

```text
start -> http-request/tool -> code -> if-else -> variable-aggregator -> end
```

## 7. HTTP 处理链变体

### 最小版

```text
start -> http-request -> end
```

### 稳定版

```text
start -> http-request -> if-else(status_code) -> tool/code -> end
```

### 低成本版

```text
start -> http-request -> code -> end
```

说明:

- 用代码做轻量解析，避免额外工具。

### 高质量版

```text
start -> http-request -> tool -> code -> if-else -> end
```

## 8. 分支模板变体

### 最小版

```text
start -> if-else -> end
```

### 稳定版

```text
start -> if-else -> code/tool -> variable-aggregator -> end
```

### 低成本版

```text
start -> if-else -> template-transform -> end
```

### 高质量版

```text
start -> question-classifier/if-else -> llm/tool -> variable-aggregator -> end/answer
```

## 9. RAG 问答变体

### 最小版

```text
start -> knowledge-retrieval -> answer
```

说明:

- 仅适合直接透出检索结果，不适合复杂回答。

### 稳定版

```text
start -> knowledge-retrieval -> llm -> answer
```

### 低成本版

```text
start -> knowledge-retrieval -> template-transform -> answer
```

### 高质量版

```text
start -> knowledge-retrieval -> llm -> if-else(empty check) -> human-input/answer
```

## 10. 文档入库变体

### 最小版

```text
datasource -> document-extractor -> knowledge-index
```

### 稳定版

```text
datasource -> if-else(file type) -> document-extractor/tool -> variable-aggregator -> knowledge-index
```

### 低成本版

```text
datasource -> document-extractor -> tool(general chunk) -> knowledge-index
```

### 高质量版

```text
datasource -> if-else -> document-extractor/tool -> variable-aggregator -> tool(parent-child or qa chunk) -> knowledge-index
```

## 11. 审批链变体

### 最小版

```text
llm/tool -> human-input -> end
```

### 稳定版

```text
llm/tool -> human-input -> assigner -> if-else -> end
```

### 低成本版

```text
template-transform/code -> human-input -> end
```

### 高质量版

```text
llm -> human-input -> assigner -> llm/code -> answer/end
```

## 12. Trigger 变体

### 最小版

```text
trigger-* -> end
```

### 稳定版

```text
trigger-* -> if-else -> code/tool -> end
```

### 低成本版

```text
trigger-* -> code -> end
```

### 高质量版

```text
trigger-* -> if-else -> tool -> code -> human-input/end
```

## 13. 选型规则

优先级建议:

1. 先定模式
2. 再定模板
3. 再定变体
4. 最后补字段、选择器和失败路径

默认建议:

- 不确定时先从 `稳定版` 开始
- 只做验证时用 `最小版`
- 高频调用时优先评估 `低成本版`
- 高价值链路优先评估 `高质量版`
