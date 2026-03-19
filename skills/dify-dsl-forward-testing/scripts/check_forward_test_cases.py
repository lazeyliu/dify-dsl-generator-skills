#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

FOUNDATIONS_SCRIPTS_DIR = CURRENT_DIR.parents[1] / "dify-dsl-foundations" / "scripts"
if str(FOUNDATIONS_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(FOUNDATIONS_SCRIPTS_DIR))

from fast_test_dsl import analyze_dsl, load_yaml_via_ruby


CANONICAL_ROUTES = (
    "skills/dify-dsl-foundations/SKILL.md",
    "skills/dify-dsl-nodes/SKILL.md",
    "skills/dify-dsl-templates/SKILL.md",
    "skills/dify-dsl-quality/SKILL.md",
    "skills/dify-dsl-governance/SKILL.md",
)

ENTRY_SKILLS = (
    "skills/using-dify-dsl/SKILL.md",
    "skills/dify-dsl-subagent-review/SKILL.md",
    "skills/dify-dsl-brainstorming/SKILL.md",
    "skills/dify-dsl-authoring/SKILL.md",
    "skills/dify-dsl-review/SKILL.md",
    "skills/dify-dsl-refactor/SKILL.md",
    "skills/dify-dsl-templates/SKILL.md",
    "skills/dify-dsl-governance/SKILL.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验一个或多个前向验证 case 目录")
    parser.add_argument("cases_roots", nargs="*", help="一个或多个 case 根目录")
    parser.add_argument("--repo-root", dest="repo_root", help="仓库根目录")
    return parser.parse_args()


def discover_case_roots(repo_root: Path) -> list[Path]:
    roots: list[Path] = []
    for path in sorted((repo_root / "skills").glob("*/tests/cases")):
        if path.exists():
            roots.append(path)
    return roots


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_target(repo_root: Path, case_dir: Path, raw_target: str | None) -> Path | None:
    if not raw_target:
        return None
    target_path = Path(raw_target)
    if target_path.is_absolute():
        return target_path
    candidate_from_case = (case_dir / target_path).resolve()
    if candidate_from_case.exists():
        return candidate_from_case
    return (repo_root / target_path).resolve()


def validate_case(repo_root: Path, case_dir: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    prompt_path = case_dir / "prompt.txt"
    oracle_path = case_dir / "oracle.json"

    if not prompt_path.exists():
        errors.append(f"{case_dir}: 缺少 prompt.txt")
    if not oracle_path.exists():
        errors.append(f"{case_dir}: 缺少 oracle.json")
        return errors, {}

    oracle = load_json(oracle_path)
    goal = oracle.get("goal")
    entry_skill = oracle.get("entry_skill")
    raw_expected_routes = oracle.get("expected_routes")
    allow_empty_routes = bool(oracle.get("allow_empty_routes"))

    if not goal:
        errors.append(f"{oracle_path}: 缺少 goal")
    if not entry_skill:
        errors.append(f"{oracle_path}: 缺少 entry_skill")
    elif entry_skill not in ENTRY_SKILLS:
        errors.append(f"{oracle_path}: entry_skill 非法 -> {entry_skill}")
    if raw_expected_routes is None:
        errors.append(f"{oracle_path}: 缺少 expected_routes")
        expected_routes = []
    elif not isinstance(raw_expected_routes, list):
        errors.append(f"{oracle_path}: expected_routes 必须是数组")
        expected_routes = []
    else:
        expected_routes = raw_expected_routes
    if not expected_routes and not allow_empty_routes:
        errors.append(f"{oracle_path}: expected_routes 必须是非空数组；如需空路由请显式设置 allow_empty_routes=true")

    for route in expected_routes:
        if route not in CANONICAL_ROUTES:
            errors.append(f"{oracle_path}: expected_routes 包含未知入口 {route}")

    target_path = resolve_target(repo_root, case_dir, oracle.get("target"))
    if oracle.get("target") and (not target_path or not target_path.exists()):
        errors.append(f"{oracle_path}: target 不存在 -> {oracle.get('target')}")

    expected_static_routes = oracle.get("expected_static_routes")
    if expected_static_routes is not None:
        if not isinstance(expected_static_routes, list) or not expected_static_routes:
            errors.append(f"{oracle_path}: expected_static_routes 必须是非空数组")
        elif target_path and target_path.exists():
            analysis = analyze_dsl(target_path, load_yaml_via_ruby(target_path))
            if analysis["routes"] != expected_static_routes:
                errors.append(
                    f"{oracle_path}: expected_static_routes 与 fast_test_dsl 输出不一致 -> "
                    f"expected={expected_static_routes}, actual={analysis['routes']}"
                )

    summary = {
        "case_dir": str(case_dir),
        "goal": goal,
        "entry_skill": entry_skill,
        "expected_routes": expected_routes,
        "target": str(target_path) if target_path else None,
    }
    return errors, summary


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else CURRENT_DIR.parents[2]
    cases_roots = [Path(raw).resolve() for raw in args.cases_roots] if args.cases_roots else discover_case_roots(repo_root)
    if not cases_roots:
        print(f"错误: 在 {repo_root} 下没有找到任何 case 根目录", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    summaries: list[dict] = []
    route_hits: dict[str, list[str]] = defaultdict(list)
    entry_hits: dict[str, list[str]] = defaultdict(list)

    for cases_root in cases_roots:
        if not cases_root.exists():
            all_errors.append(f"{cases_root}: case 根目录不存在")
            continue
        case_dirs = sorted(path for path in cases_root.iterdir() if path.is_dir())
        if not case_dirs:
            all_errors.append(f"{cases_root}: 下没有 case 目录")
            continue
        for case_dir in case_dirs:
            errors, summary = validate_case(repo_root, case_dir)
            all_errors.extend(errors)
            if summary:
                summaries.append(summary)
                entry_hits[summary["entry_skill"]].append(case_dir.name)
                for route in summary["expected_routes"]:
                    route_hits[route].append(case_dir.name)

    if all_errors:
        for error in all_errors:
            print(f"错误: {error}", file=sys.stderr)
        return 1

    print(f"case 数: {len(summaries)}")
    print("")
    print("case 摘要:")
    for summary in summaries:
        print(
            "- "
            + f"{Path(summary['case_dir']).name} | goal={summary['goal']} | "
            + f"entry_skill={summary['entry_skill']} | "
            + f"target={summary['target'] or '(none)'} | "
            + f"expected_routes={', '.join(summary['expected_routes'])}"
        )

    print("")
    print("入口 skill 覆盖矩阵:")
    for entry_skill in ENTRY_SKILLS:
        hits = entry_hits.get(entry_skill)
        if hits:
            print(f"- {entry_skill}: 已覆盖 ({', '.join(hits)})")
        else:
            print(f"- {entry_skill}: 未覆盖")

    print("")
    print("case 覆盖矩阵:")
    for route in CANONICAL_ROUTES:
        hits = route_hits.get(route)
        if hits:
            print(f"- {route}: 已覆盖 ({', '.join(hits)})")
        else:
            print(f"- {route}: 未覆盖")

    missing_routes = [route for route in CANONICAL_ROUTES if route not in route_hits]
    print("")
    missing_entry_skills = [entry_skill for entry_skill in ENTRY_SKILLS if entry_skill not in entry_hits]
    if missing_routes or missing_entry_skills:
        if missing_routes:
            print(f"结论: 仍缺这些底座 skill 路线覆盖 -> {', '.join(missing_routes)}")
        if missing_entry_skills:
            print(f"结论: 仍缺这些入口 skill 覆盖 -> {', '.join(missing_entry_skills)}")
    else:
        print("结论: case 目录已覆盖全部底座 skill 和入口 skill")
    return 0


if __name__ == "__main__":
    sys.exit(main())
