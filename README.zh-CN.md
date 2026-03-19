# tee

[English](README.md)

`tee` 是一个面向 `Dify DSL` 的技能仓库。

它不是业务应用仓库，也不是单纯的模板集合。它提供的是一整套给 AI agent 使用的 skill、参考资料、样本和验证脚本，用来稳定地处理 `Dify Workflow`、`Chatflow` 和 `RAG Pipeline` DSL。

## 项目是什么

这个项目把 `Dify DSL` 当成一个需要被设计、生成、审查、修复、重构和验证的编排系统来处理。

它的核心价值有三点：

- 把 DSL 相关能力拆成职责清晰、可组合的 skill，而不是堆在一个大 prompt 里
- 把节点、模板、校验、交付判断这些知识沉淀成可复用的底座
- 把“看起来会做”变成“有样本、有 case、有 replay、有报告的可验证能力”

## 项目解决什么问题

直接处理 Dify DSL 时，最常见的问题不是“不会写 YAML”，而是：

- 模式判断不清，`workflow / advanced-chat / rag_pipeline` 混用
- 节点字段、选择器、连边和容器闭环容易出错
- 模板、节点知识、审查规则和交付判断混在一起，导致上下文膨胀
- 给得出结论，但没有证据链，也没有回归验证

这个仓库就是为这些问题准备的。

## 支持范围

当前技能体系覆盖：

- `kind: app` + `app.mode: workflow`
- `kind: app` + `app.mode: advanced-chat`
- `kind: rag_pipeline`

## 技能组成

### 总入口 skill

- [using-dify-dsl](skills/using-dify-dsl/SKILL.md)  
  处理意图识别、权限边界判断和主 skill 路由；当你把整个仓库作为一个技能包安装时，优先从这里进入。

当前只有这个总入口保留 `agents/openai.yaml`；其余 `dify-dsl-*` skill 仍会通过各自的 `SKILL.md` 被发现。

### 入口 skill

- [dify-dsl-subagent-review](skills/dify-dsl-subagent-review/SKILL.md)  
  处理多方独立复核编排、子代理退化和冲突归并的场景。
- [dify-dsl-brainstorming](skills/dify-dsl-brainstorming/SKILL.md)  
  处理需求不清、未知项未收敛、需要先比较方案的场景。
- [dify-dsl-authoring](skills/dify-dsl-authoring/SKILL.md)  
  处理从明确需求生成 DSL 草稿的场景。
- [dify-dsl-review](skills/dify-dsl-review/SKILL.md)  
  处理只读审查、风险分级、导入判断和发布结论的场景。
- [dify-dsl-refactor](skills/dify-dsl-refactor/SKILL.md)  
  处理最小修复、优化和重构的场景。

### 底座 skill

- [dify-dsl-foundations](skills/dify-dsl-foundations/SKILL.md)  
  模式判断、任务路由、字段口径、输出契约、校验契约。
- [dify-dsl-nodes](skills/dify-dsl-nodes/SKILL.md)  
  节点知识、节点组合、容器和选择器规则。
- [dify-dsl-templates](skills/dify-dsl-templates/SKILL.md)  
  模板库、模板骨架、模板状态和模板变体。
- [dify-dsl-quality](skills/dify-dsl-quality/SKILL.md)  
  审查、修复、优化、子代理复核分工。
- [dify-dsl-governance](skills/dify-dsl-governance/SKILL.md)  
  发布判断、变更影响、覆盖率、观测字段和能力块约定。

### 验证 skill

- [dify-dsl-forward-testing](skills/dify-dsl-forward-testing/SKILL.md)  
  用真实样本、真实 prompt 和 replay 断言验证 skill 是否真的按预期协作。

### 子代理复核总览

- [Dify DSL 子代理复核总览](docs/dify-dsl-subagent-review-overview.zh-CN.md)  
  一页看懂什么时候进入 `dify-dsl-subagent-review`、四种复核模式、角色分工和当前样本覆盖。

## 怎么使用这个项目

如果你把整个仓库当成一个技能包安装，最简单的用法是先调用 [using-dify-dsl](skills/using-dify-dsl/SKILL.md)，让它根据用户意图自动判断应该进入哪个下游 skill。

### 主路径速览

<!-- BEGIN ROUTE_MATRIX -->
| 用户目标 | 推荐入口 | 常见下一步 |
| --- | --- | --- |
| 需求还没收敛 | `using-dify-dsl` 或 `dify-dsl-brainstorming` | `dify-dsl-authoring / review / refactor` |
| 新建 DSL | `using-dify-dsl` 或 `dify-dsl-authoring` | 高复杂度时进入 `dify-dsl-subagent-review` |
| 只读审查已有 DSL | `using-dify-dsl` 或 `dify-dsl-review` | 需要多方复核时进入 `dify-dsl-subagent-review` |
| 修改已有 DSL | `using-dify-dsl` 或 `dify-dsl-refactor` | 修改后需要独立复核时进入 `dify-dsl-subagent-review` |
| 只想选模板 | `using-dify-dsl` 或 `dify-dsl-templates` | 如需正文再进入 `dify-dsl-authoring` |
| 只想判断能不能交付 | `using-dify-dsl` 或 `dify-dsl-governance` | 如果用户同时明确要求多方独立复核或冲突归并，再进入 `dify-dsl-subagent-review` |
| 明确要组织多方复核 | `using-dify-dsl` 或 `dify-dsl-subagent-review` | 按并行 / 串行 / 单子代理 / 无子代理退化 |
<!-- END ROUTE_MATRIX -->

可以把主路径理解成这一条：

<!-- BEGIN MAIN_PATH -->
```text
using-dify-dsl
-> brainstorming / authoring / review / refactor / templates / governance / subagent-review
-> 必要时再进入 subagent-review 或 governance
```
<!-- END MAIN_PATH -->

如果你已经明确知道目标，也可以直接点名入口 skill：

- 需求还不清楚：先看 [dify-dsl-brainstorming](skills/dify-dsl-brainstorming/SKILL.md)
- 要新建 DSL：先看 [dify-dsl-authoring](skills/dify-dsl-authoring/SKILL.md)
- 只想只读审查 DSL：先看 [dify-dsl-review](skills/dify-dsl-review/SKILL.md)
- 要修改已有 DSL：先看 [dify-dsl-refactor](skills/dify-dsl-refactor/SKILL.md)
- 要组织多方独立复核并归并结论：先看 [dify-dsl-subagent-review](skills/dify-dsl-subagent-review/SKILL.md)
- 要验证 skill 自身是否可靠：先看 [dify-dsl-forward-testing](skills/dify-dsl-forward-testing/SKILL.md)

## 安装到 Codex

推荐把整个仓库作为一个技能包安装，而不是把每个 skill 分散挂到 `~/.codex/skills/` 顶层。

详细步骤见 [.codex/INSTALL.md](.codex/INSTALL.md)。

如果你已经是散装安装，也可以直接运行：

```bash
bash scripts/install_codex_bundle.sh
```

即使已经按 bundle 安装，当前 Codex 版本的技能面板仍可能列出多个 `dify-dsl-*` 子 skill；把 `using-dify-dsl` 视为推荐入口，不要把它当成“唯一可见卡片”。

## 仓库结构

```text
tee/
├── .codex/INSTALL.md
├── .github/workflows/validate.yml
├── docs/
│   ├── dify-dsl-subagent-review-overview.md
│   └── dify-dsl-subagent-review-overview.zh-CN.md
├── scripts/
│   ├── install_codex_bundle.sh
│   ├── quick_validate.py
│   ├── validate_skill_repo.py
│   └── validate_forward_testing.py
├── skills/
│   ├── using-dify-dsl/
│   ├── dify-dsl-subagent-review/
│   ├── dify-dsl-brainstorming/
│   ├── dify-dsl-authoring/
│   ├── dify-dsl-review/
│   ├── dify-dsl-refactor/
│   ├── dify-dsl-foundations/
│   ├── dify-dsl-nodes/
│   ├── dify-dsl-templates/
│   ├── dify-dsl-quality/
│   ├── dify-dsl-governance/
│   └── dify-dsl-forward-testing/
├── tests/
│   └── fixtures/dsl/
└── .forward-testing/
```

## 共享资源

共享 DSL 样本放在 `tests/fixtures/dsl/`。

前向验证产物默认放在 `.forward-testing/`：

- `last-good.json`
- `latest-report.json`
- `latest-diff.json`

## 常用命令

校验整个仓库结构：

```bash
python3 scripts/quick_validate.py
```

运行整套前向验证：

```bash
python3 scripts/validate_forward_testing.py
```

首次建立或更新稳定基线：

```bash
python3 scripts/validate_forward_testing.py --promote-current
```

如果只想直接跑 skill 内部验证脚本：

```bash
python3 skills/dify-dsl-foundations/scripts/fast_test_dsl.py <sample.yml>
python3 skills/dify-dsl-foundations/scripts/fast_test_suite.py <sample.yml|directory> [...]
python3 skills/dify-dsl-forward-testing/scripts/run_validation_suite.py [--json-out <report.json>]
python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py <old.json> <new.json> [--json-out <diff.json>]
```

## 自动化校验

GitHub Actions 工作流在 [validate.yml](.github/workflows/validate.yml)。

它分成两个 job：

- `structure`  
  运行 `python3 scripts/quick_validate.py`
- `forward-testing`  
  运行 `python3 scripts/validate_forward_testing.py`

`forward-testing` job 会上传 `.forward-testing/latest-report.json` 作为 artifact。

## 维护约定

- 总入口 skill 固定为 `skills/using-dify-dsl/`
- 领域 skill 统一放到 `skills/dify-dsl-*`
- 共享 fixture 统一放到 `tests/fixtures/dsl/`
- 如果改了主路径速览或一屏主路径，运行 `python3 scripts/route_matrix_docs.py --write` 回写文档
- 新增或修改 case 时，尽量同时补：
  - `oracle.json`
  - `replay-output.txt`
  - `expectation_files`
- 如果改动影响 skill 协作路径，至少跑一次：

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_forward_testing.py
```
