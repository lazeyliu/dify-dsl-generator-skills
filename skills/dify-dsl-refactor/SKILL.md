---
name: dify-dsl-refactor
description: 修复、优化与重构现有 Dify Workflow、Chatflow、RAG Pipeline DSL 的入口技能。用于最小修复、结构优化、模板重排和能力块重构；如果用户只要只读结论，转去 dify-dsl-review；如果目标仍模糊，先回 dify-dsl-brainstorming。
---

# dify-dsl-refactor

先诊断问题，再决定做最小修复、结构优化还是模板重排，不要一上来重写整份 DSL。

## 协作顺序

1. 先读 [../dify-dsl-foundations/SKILL.md](../dify-dsl-foundations/SKILL.md) 和 [../dify-dsl-quality/SKILL.md](../dify-dsl-quality/SKILL.md)，确定问题类别和修复路径。
2. 节点或容器细节需要补证时，读 [../dify-dsl-nodes/SKILL.md](../dify-dsl-nodes/SKILL.md)。
3. 需要模板重排或骨架替换时，读 [../dify-dsl-templates/SKILL.md](../dify-dsl-templates/SKILL.md)。
4. 需要变更影响、观测字段或上线前检查时，读 [../dify-dsl-governance/SKILL.md](../dify-dsl-governance/SKILL.md)。

## 最低输出

1. 问题归因
2. 最小修复或重构方案
3. 变更影响摘要
4. 修改后的 DSL
5. 仍待确认风险

## 约束

- 不要把“最小修复”无故升级成大重写。
- 不要在目标不明确时擅自决定重构方向。
- 如果用户只要只读审查，转去 [../dify-dsl-review/SKILL.md](../dify-dsl-review/SKILL.md)。
