#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from fast_test_dsl import analyze_dsl, load_yaml_via_ruby


CANONICAL_ROUTES = (
    "references/index.md",
    "references/foundations/index.md",
    "references/nodes/index.md",
    "references/templates/index.md",
    "references/quality/index.md",
    "references/governance/index.md",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_target(root: Path, case_dir: Path, raw_target: str | None) -> Path | None:
    if not raw_target:
        return None
    target_path = Path(raw_target)
    if target_path.is_absolute():
        return target_path
    candidate_from_case = (case_dir / target_path).resolve()
    if candidate_from_case.exists():
        return candidate_from_case
    return (root / target_path).resolve()


def validate_case(root: Path, case_dir: Path) -> tuple[list[str], dict]:
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
    expected_routes = oracle.get("expected_routes") or []

    if not goal:
        errors.append(f"{oracle_path}: 缺少 goal")
    if not isinstance(expected_routes, list) or not expected_routes:
        errors.append(f"{oracle_path}: expected_routes 必须是非空数组")

    for route in expected_routes:
        if route not in CANONICAL_ROUTES:
            errors.append(f"{oracle_path}: expected_routes 包含未知入口 {route}")

    target_path = resolve_target(root, case_dir, oracle.get("target"))
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
        "expected_routes": expected_routes,
        "target": str(target_path) if target_path else None,
    }
    return errors, summary


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    cases_root = root / "tests" / "cases"
    if not cases_root.exists():
        print(f"错误: {cases_root} 不存在", file=sys.stderr)
        return 1

    case_dirs = sorted(path for path in cases_root.iterdir() if path.is_dir())
    if not case_dirs:
        print(f"错误: {cases_root} 下没有 case 目录", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    summaries: list[dict] = []
    route_hits: dict[str, list[str]] = defaultdict(list)

    for case_dir in case_dirs:
        errors, summary = validate_case(root, case_dir)
        all_errors.extend(errors)
        if summary:
            summaries.append(summary)
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
            + f"target={summary['target'] or '(none)'} | "
            + f"expected_routes={', '.join(summary['expected_routes'])}"
        )

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
    if missing_routes:
        print(f"结论: 仍缺这些 case 路线覆盖 -> {', '.join(missing_routes)}")
    else:
        print("结论: case 目录已覆盖全部 canonical routes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
