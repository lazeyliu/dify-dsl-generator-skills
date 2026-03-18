# 参考目录总览

这是整个 `references/` 的正式总入口。

如果你还不知道该读哪个子目录，不要直接扫完整个 `references/`；先从这里收敛，再进入对应目录的 `index.md`。

## 总体原则

- 先定模式、定任务类型，再决定读哪些参考资料。
- 先读入口页，再按需下钻，不要整库读满。
- 节点、模板、质量和交付判断是不同层级的问题，不要混着看。

## 推荐总路线

1. 先读 [foundations/index.md](foundations/index.md)。
2. 根据任务目标进入下一个目录：
   - 节点字段与节点组合：读 [nodes/index.md](nodes/index.md)
   - 模板选择与模板变体：读 [templates/index.md](templates/index.md)
   - 修复、审核、优化：读 [quality/index.md](quality/index.md)
   - 上线前检查、约定、覆盖率与交付判断：读 [governance/index.md](governance/index.md)

## 按任务快速路由

- 从零新建 DSL：
  先读 [foundations/index.md](foundations/index.md)，再进入 [nodes/index.md](nodes/index.md)；如果要从模板起手，再进入 [templates/index.md](templates/index.md)。
- 修复现有 DSL：
  先读 [foundations/index.md](foundations/index.md)，再进入 [quality/index.md](quality/index.md)，必要时回到 [nodes/index.md](nodes/index.md)。
- 只读审核或发布判断：
  先读 [foundations/index.md](foundations/index.md)，再进入 [quality/index.md](quality/index.md)；涉及检查项、输入输出约定或覆盖率时，再进入 [governance/index.md](governance/index.md)。
- 优化或重构：
  先读 [foundations/index.md](foundations/index.md)，再进入 [quality/index.md](quality/index.md)；涉及可观测性、能力块边界和发布结论时，再进入 [governance/index.md](governance/index.md)。

## 典型请求

- “帮我从零写一个 Dify workflow，输入用户问题后调用 HTTP 接口，再整理成结构化输出。”
- “这份 DSL 为什么导不进去？帮我找出节点字段和 selector 的问题。”
- “先不要改文件，只审核这份 Dify DSL，给我风险分级和发布结论。”
- “我想基于现有模板改成低成本版 / 高质量版，先帮我选模板和变体。”
- “这条链路太重了，帮我重构成更稳定、可观测、可维护的编排。”

## 子目录职责

- [foundations/index.md](foundations/index.md)
  共享底座、模式判断、任务路由、交付约定、选择器与字段口径。
- [nodes/index.md](nodes/index.md)
  节点目录入口与逐节点说明。
- [templates/index.md](templates/index.md)
  模板入口、模板变体、已验证骨架与模板状态。
- [quality/index.md](quality/index.md)
  修复策略、审核清单、分级审查、优化和独立复核。
- [governance/index.md](governance/index.md)
  上线前检查、变更影响、覆盖率、升级条件、观测字段约定和能力块边界约定。

## 使用约束

- 这里是总览，不替代各子目录入口页。
- 如果任务已经非常明确，允许直接进入对应子目录的 `index.md`。
- 如果结论涉及“可直接导入”“已精准校验”或发布判断，最终至少要经过 `quality` 与 `governance` 两层。
