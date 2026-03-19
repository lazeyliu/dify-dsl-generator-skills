---
name: dify-dsl-forward-testing
description: Dify DSL 技能前向验证技能。用于用真实样本、真实提示词和最小泄漏原则验证 dify-dsl-authoring、dify-dsl-review、dify-dsl-refactor、dify-dsl-templates 等技能是否真的按预期协作；当你要验证 skill 本身而不是验证 DSL 功能时使用。
---

# dify-dsl-forward-testing

把 skill 当成被测对象，而不是把 prompt 当成答案提示器。

## 入口

先读 [references/index.md](references/index.md)，再按需运行当前目录下的脚本。

## 脚本

- `python3 skills/dify-dsl-foundations/scripts/fast_test_dsl.py <sample.yml>`
- `python3 skills/dify-dsl-foundations/scripts/fast_test_suite.py <sample.yml|directory> [...]`
- `python3 skills/dify-dsl-forward-testing/scripts/init_forward_test_case.py <case-dir> --target <sample.yml>`
- `python3 skills/dify-dsl-forward-testing/scripts/check_forward_test_cases.py <cases-root> [repo-root]`
- `python3 skills/dify-dsl-forward-testing/scripts/check_replay_outputs.py <case-dir> [...] [--repo-root <repo-root>]`
- `python3 skills/dify-dsl-forward-testing/scripts/run_validation_suite.py [<cases-root> ...] [--repo-root <repo-root>] [--json-out <report.json>]`
- `python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py <old.json> <new.json> [--json-out <diff.json>]`

## 约束

- 不要把 `oracle.json` 的预期答案泄漏给被测线程。
- 不要为了让 case 通过，先改 prompt 去“哄对”结果。
- 只验证一个主要目标：路由、审查、模板选择或重构策略，不要一轮混多个目标。
- 如果要把真实回放结果变成机器可判定资产，把 `replay-output.txt` 和 `expectation_files` 绑定到 case，而不是只靠人工肉眼回看。
- 日常回归优先跑 `run_validation_suite.py`，它会同时检查 case 结构和 replay 断言。
- 如果要给 CI 或其他 agent 平台消费验证结果，使用 `--json-out` 产出机器可读报告。
- 如果要看本次验证相对上次是变好还是变坏，用 `compare_validation_reports.py` 对比两份 JSON 报告。
- 如果你已经有上一份报告，也可以直接给 `run_validation_suite.py` 传 `--baseline-report` 和 `--diff-json-out`，一次拿到本轮结果和 diff。
