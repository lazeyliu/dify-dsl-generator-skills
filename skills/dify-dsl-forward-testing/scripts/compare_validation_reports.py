#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="对比两次 Dify DSL 前向验证 JSON 报告")
    parser.add_argument("old_report", help="旧报告 JSON")
    parser.add_argument("new_report", help="新报告 JSON")
    parser.add_argument("--json-out", dest="json_out", help="把 diff 写入 JSON 文件")
    return parser.parse_args()


def load_report(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def case_map(report: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for case in report.get("cases", []):
        case_dir = case.get("case_dir")
        if isinstance(case_dir, str):
            result[case_dir] = case
    return result


def diff_case(old_case: dict, new_case: dict) -> dict:
    changed_fields: dict[str, dict[str, object]] = {}
    for field in (
        "goal",
        "entry_skill",
        "target",
        "structure_ok",
        "lint_status",
        "lint_error_count",
        "lint_warning_count",
        "replay_status",
    ):
        old_value = old_case.get(field)
        new_value = new_case.get(field)
        if old_value != new_value:
            changed_fields[field] = {"old": old_value, "new": new_value}
    return changed_fields


def build_diff(old_report: dict, new_report: dict) -> dict:
    old_cases = case_map(old_report)
    new_cases = case_map(new_report)

    old_case_dirs = set(old_cases)
    new_case_dirs = set(new_cases)
    added_cases = sorted(new_case_dirs - old_case_dirs)
    removed_cases = sorted(old_case_dirs - new_case_dirs)

    changed_cases: dict[str, dict] = {}
    for case_dir in sorted(old_case_dirs & new_case_dirs):
        changed_fields = diff_case(old_cases[case_dir], new_cases[case_dir])
        if changed_fields:
            changed_cases[case_dir] = changed_fields

    old_entry_coverage = old_report.get("entry_skill_coverage", {})
    new_entry_coverage = new_report.get("entry_skill_coverage", {})
    all_entry_skills = sorted(set(old_entry_coverage) | set(new_entry_coverage))
    entry_coverage_changes: dict[str, dict] = {}
    for entry_skill in all_entry_skills:
        old_hits = set(old_entry_coverage.get(entry_skill, []))
        new_hits = set(new_entry_coverage.get(entry_skill, []))
        if old_hits != new_hits:
            entry_coverage_changes[entry_skill] = {
                "added": sorted(new_hits - old_hits),
                "removed": sorted(old_hits - new_hits),
            }

    old_route_coverage = old_report.get("route_coverage", {})
    new_route_coverage = new_report.get("route_coverage", {})
    all_routes = sorted(set(old_route_coverage) | set(new_route_coverage))
    route_coverage_changes: dict[str, dict] = {}
    for route in all_routes:
        old_hits = set(old_route_coverage.get(route, []))
        new_hits = set(new_route_coverage.get(route, []))
        if old_hits != new_hits:
            route_coverage_changes[route] = {
                "added": sorted(new_hits - old_hits),
                "removed": sorted(old_hits - new_hits),
            }

    top_level_changes: dict[str, dict[str, object]] = {}
    for field in ("schema_version", "case_count", "skip_replay", "structure_ok", "lint_ok", "replay_ok", "suite_ok"):
        old_value = old_report.get(field)
        new_value = new_report.get(field)
        if old_value != new_value:
            top_level_changes[field] = {"old": old_value, "new": new_value}

    return {
        "old_report": old_report.get("generated_at_utc"),
        "new_report": new_report.get("generated_at_utc"),
        "top_level_changes": top_level_changes,
        "added_cases": added_cases,
        "removed_cases": removed_cases,
        "changed_cases": changed_cases,
        "entry_coverage_changes": entry_coverage_changes,
        "route_coverage_changes": route_coverage_changes,
        "old_missing_routes": old_report.get("missing_routes", []),
        "new_missing_routes": new_report.get("missing_routes", []),
        "old_missing_entry_skills": old_report.get("missing_entry_skills", []),
        "new_missing_entry_skills": new_report.get("missing_entry_skills", []),
    }


def print_diff(diff: dict) -> None:
    print("报告对比:")
    print(f"- old_report: {diff['old_report'] or '(unknown)'}")
    print(f"- new_report: {diff['new_report'] or '(unknown)'}")
    print("")

    if diff["top_level_changes"]:
        print("顶层状态变化:")
        for field, change in diff["top_level_changes"].items():
            print(f"- {field}: {change['old']} -> {change['new']}")
    else:
        print("顶层状态变化: 无")

    print("")
    if diff["added_cases"]:
        print(f"新增 case: {', '.join(diff['added_cases'])}")
    else:
        print("新增 case: 无")

    if diff["removed_cases"]:
        print(f"移除 case: {', '.join(diff['removed_cases'])}")
    else:
        print("移除 case: 无")

    print("")
    if diff["changed_cases"]:
        print("case 变化:")
        for case_dir, changed_fields in diff["changed_cases"].items():
            print(f"- {case_dir}")
            for field, change in changed_fields.items():
                print(f"  {field}: {change['old']} -> {change['new']}")
    else:
        print("case 变化: 无")

    print("")
    if diff["entry_coverage_changes"]:
        print("入口 skill 覆盖变化:")
        for entry_skill, change in diff["entry_coverage_changes"].items():
            print(f"- {entry_skill}: +{change['added']} -{change['removed']}")
    else:
        print("入口 skill 覆盖变化: 无")

    print("")
    if diff["route_coverage_changes"]:
        print("底座 skill 覆盖变化:")
        for route, change in diff["route_coverage_changes"].items():
            print(f"- {route}: +{change['added']} -{change['removed']}")
    else:
        print("底座 skill 覆盖变化: 无")


def main() -> int:
    args = parse_args()
    old_report = load_report(args.old_report)
    new_report = load_report(args.new_report)
    diff = build_diff(old_report, new_report)

    if args.json_out:
        out_path = Path(args.json_out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print_diff(diff)
    if args.json_out:
        print("")
        print(f"JSON diff: {Path(args.json_out).expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
