#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

FOUNDATIONS_SCRIPTS_DIR = CURRENT_DIR.parents[1] / "dify-dsl-foundations" / "scripts"
if str(FOUNDATIONS_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(FOUNDATIONS_SCRIPTS_DIR))

from fast_test_dsl import analyze_dsl, load_yaml_via_ruby


PROMPT_TEMPLATES = {
    "router": """使用 $using-dify-dsl 执行这次 forward-test。

工作目录: {case_dir}
需求说明: <在这里写真实需求>
目标文件: {target}
旧基线: {baseline}

这是一个真实 Dify DSL 路由任务，不是问答。
约束：先判断任务类型和权限边界，再说明主路由，以及为什么不是最接近的另外 1 到 2 个 skill。
如果当前需求仍模糊，不要直接生成或修改 DSL。
如果确认它根本不是 Dify DSL 任务，明确写出“不进入本技能包”。
""",
    "subagent-review": """使用 $dify-dsl-subagent-review 执行这次 forward-test。

工作目录: {case_dir}
目标文件: {target}
旧基线: {baseline}

这是一个真实 Dify DSL 复核编排任务，不是问答。
约束：只读；不要修改文件；先选择本轮复核模式，并说明为什么不是最接近的另外 1 到 2 个模式；如果平台和授权允许，按选定模式组织子代理；如果不允许，按规则退化，并明确写出 `未做独立复核`；只有在存在冲突或当前任务需要最终门禁归并时，才启用上线检查复核器。
""",
    "brainstorming": """使用 $dify-dsl-brainstorming 执行这次 forward-test。

工作目录: {case_dir}
需求说明: <在这里写真实需求>
参考样本: {target}

这是一个真实 Dify DSL 头脑风暴任务，不是问答。
约束：先列已知项、未知项和阻塞未知项；阻塞未知项未清零前，不要进入 authoring / review / refactor。
结束时必须说明准备路由到哪个 skill，以及为什么。
""",
    "authoring": """使用 $dify-dsl-authoring 执行这次 forward-test。

工作目录: {case_dir}
需求说明: <在这里写真实需求>
参考样本: {target}

这是一个真实 DSL 生成任务，不是问答。
约束：不要修改文件；先给模式判断、模板选择、节点清单、连边清单和字段检查表，再给 DSL 草稿。
如果需求仍有阻塞未知项，明确写出并停止进入正文。
""",
    "review": """使用 $dify-dsl-review 执行这次只读 forward-test。

工作目录: {case_dir}
目标文件: {target}
旧基线: {baseline}

这是一个真实审查任务，不是问答。该 DSL 计划在今天导入 staging。
约束：只读；不要修改文件；不要生成新 DSL。
如果当前平台 / 会话 / 授权策略不允许自动拉起 subagent，明确写“未做独立复核”。

请直接行动：
1. 先做模式判断、节点清单、连边清单、字段检查表。
2. 如果授权允许，启动 3 个只读 subagent：
   字段约束检查
   链路闭环检查
   提示词与契约检查
3. 只有当前三方结论冲突，或存在旧基线需要仲裁时，才启动发布门禁检查做归并。
4. 输出先列问题，再给结论；问题按阻塞项 / 高风险项 / 中风险项 / 优化项排序；每条问题都带节点 ID 或字段路径。
5. 最终只给一个结论：可直接导入 / 需要人工确认 / 明显不完整。
""",
    "template": """使用 $dify-dsl-templates 执行这次只读 forward-test。

工作目录: {case_dir}
需求说明: <在这里写真实需求>
参考样本: {target}

这是一个真实模板选择任务，不是问答。
约束：只读；不要修改文件；不要生成新 DSL。

请直接行动：
1. 先说明会进入哪些底座 skill。
2. 选择最接近的模板和模板变体。
3. 解释为什么选它，而不是其它模板。
4. 标记该模板属于已验证 / 间接验证 / 推导。
""",
    "governance": """使用 $dify-dsl-governance 执行这次只读 forward-test。

工作目录: {case_dir}
目标文件: {target}
旧基线: {baseline}

这是一个真实治理判断任务，不是问答。
约束：只读；不要修改文件；不要生成新 DSL。

请直接行动：
1. 先做模式判断和结构分析。
2. 重点检查发布门禁、观测契约、覆盖率缺口和最终结论。
3. 如果没有完成独立复核，明确写出风险升级。
""",
    "refactor": """使用 $dify-dsl-refactor 执行这次 forward-test。

工作目录: {case_dir}
目标文件: {target}
旧基线: {baseline}

这是一个真实 DSL 修复 / 重构任务，不是问答。
约束：允许给出修改后的 DSL，但不要修改磁盘文件；先解释问题归因和最小修复路径，再给修改结果和剩余风险。
如果目标其实只需要只读结论，明确写出应切到 dify-dsl-review。
""",
}


ENTRY_SKILL_BY_GOAL = {
    "router": "skills/using-dify-dsl/SKILL.md",
    "subagent-review": "skills/dify-dsl-subagent-review/SKILL.md",
    "brainstorming": "skills/dify-dsl-brainstorming/SKILL.md",
    "authoring": "skills/dify-dsl-authoring/SKILL.md",
    "review": "skills/dify-dsl-review/SKILL.md",
    "template": "skills/dify-dsl-templates/SKILL.md",
    "governance": "skills/dify-dsl-governance/SKILL.md",
    "refactor": "skills/dify-dsl-refactor/SKILL.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化一个 forward-test case 目录")
    parser.add_argument("case_dir", help="输出的 case 目录")
    parser.add_argument("--target", required=True, help="真实 DSL 样本路径")
    parser.add_argument("--baseline", help="可选的旧基线路径")
    parser.add_argument(
        "--goal",
        choices=sorted(PROMPT_TEMPLATES),
        default="review",
        help="生成哪种 prompt 骨架",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    case_dir = Path(args.case_dir).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()
    baseline = Path(args.baseline).expanduser().resolve() if args.baseline else None

    if not target.exists():
        print(f"错误: target 不存在: {target}", file=sys.stderr)
        return 1
    if baseline and not baseline.exists():
        print(f"错误: baseline 不存在: {baseline}", file=sys.stderr)
        return 1

    case_dir.mkdir(parents=True, exist_ok=True)

    analysis = analyze_dsl(target, load_yaml_via_ruby(target))
    baseline_text = str(baseline) if baseline else "无"

    prompt_text = PROMPT_TEMPLATES[args.goal].format(
        case_dir=case_dir,
        target=target,
        baseline=baseline_text,
    )
    oracle = {
        "case_dir": str(case_dir),
        "goal": args.goal,
        "entry_skill": ENTRY_SKILL_BY_GOAL[args.goal],
        "target": str(target),
        "baseline": str(baseline) if baseline else None,
        "expected_routes": analysis["routes"],
        "expected_read_only": True,
        "analysis": analysis,
        "notes": [
            "不要把本文件内容泄漏给被测线程。",
            "可在运行后补充 expected_findings、success 或 failure_reason。",
        ],
    }

    (case_dir / "prompt.txt").write_text(prompt_text, encoding="utf-8")
    (case_dir / "oracle.json").write_text(json.dumps(oracle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"已生成 forward-test case: {case_dir}")
    print(f"- prompt: {case_dir / 'prompt.txt'}")
    print(f"- oracle: {case_dir / 'oracle.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
