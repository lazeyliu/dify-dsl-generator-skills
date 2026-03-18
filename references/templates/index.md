# 模板目录索引

这里是 `references/templates/` 的入口。

只有当任务明确要求“从模板起手”“挑模板”“选模板变体”或“基于模板重排”时，才进入这个目录；如果只是修一个已有 DSL，优先回到 `references/foundations/task-routing.md` 走修复路线。

## 推荐读取顺序

1. 不确定该选哪类模板时，先读 [templates-library.md](templates-library.md)。
2. 需要判断模板是否能宣称为“已验证”时，读 [template-validation-status.md](template-validation-status.md)。
3. 需要直接拿最小可落地骨架起手时，读 [validated-template-skeletons.md](validated-template-skeletons.md)。
4. 需要在最小版 / 稳定版 / 低成本版 / 高质量版之间切换时，读 [template-variants.md](template-variants.md)。

## 按问题选文档

- “我该选什么模板？”
  读 [templates-library.md](templates-library.md)。
- “这个模板能不能说已经验证过？”
  读 [template-validation-status.md](template-validation-status.md)。
- “给我一个可以直接填空的骨架。”
  读 [validated-template-skeletons.md](validated-template-skeletons.md)。
- “同一个模板怎么切稳定版或低成本版？”
  读 [template-variants.md](template-variants.md)。

## 按场景快速定位

- 基础对话 / 轻问答：`基础 Chatflow 模板`
- 普通结构化流程：`基础 Workflow 模板`
- 外部接口处理：`HTTP 处理链模板`
- 规则分流：`条件分支模板`
- 多路输出汇总：`多分支聚合模板`
- 会话变量更新：`变量更新模板`
- 批量数组处理：`Iteration 模板`
- 循环与早停：`Loop 模板`
- 文档入库：`文档入库模板`
- 知识问答 / RAG：先看 `RAG 问答模板`，再核对是否属于已验证或能力推导范围
- 审批流 / 触发流：先看库和状态页，不要默认宣称为“已验证模板”

## 典型请求

- “给我一个可以直接填空的最小 chatflow / workflow 骨架。”
- “我想从模板起手，但需要明确哪些模板是真的已验证、哪些只是能力推导。”
- “把这条链路改成低成本版 / 稳定版 / 高质量版，先帮我选模板变体。”
- “审批链或 webhook 触发链有没有现成模板？如果没有，风险怎么标记？”

## 使用约束

- 模板只用来选起点，不替代节点字段检查、选择器检查和 3 轮校验。
- 如果模板状态是“间接支撑”或“基于节点能力推导”，报告里必须显式标记来源级别。
- 如果用户要求“精准无误”或“可直接导入”，优先选 `已由样例索引直接支撑` 的模板与变体。
