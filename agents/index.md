# 角色目录

这里放的是当前 skill 的正式角色定义，主要用于子代理分工和前向验证。

这些文件不是 UI 适配元数据；它们的作用是把角色职责、关注范围和输出要求固定下来，避免每次派发子代理都临时重写一遍角色说明。

## 角色列表

- [field-constraint-checker.md](field-constraint-checker.md)
  节点字段、实体约束、类型和值域检查。
- [graph-closure-checker.md](graph-closure-checker.md)
  连边、选择器、容器闭环、可达性和资源边界检查。
- [prompt-contract-checker.md](prompt-contract-checker.md)
  提示词、输入输出约定、状态污染、安全和可导入性结论检查。
- [release-readiness-checker.md](release-readiness-checker.md)
  变更影响、观测字段、上线前检查和冲突归并检查。

## 使用方式

- 如果当前平台支持把角色文件直接作为子代理提示底座，优先直接使用这些文件。
- 如果当前平台不支持，就把对应文件里的职责段和输出要求拼进派发提示。
- `release-readiness-checker.md` 不负责全量重审，默认只在前三个角色已有结论、且需要归并时启用。
