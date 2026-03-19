#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import sys
from collections import defaultdict
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

QUALITY_SCRIPTS_DIR = CURRENT_DIR.parents[1] / "dify-dsl-quality" / "scripts"
if str(QUALITY_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(QUALITY_SCRIPTS_DIR))

import check_forward_test_cases as case_check
import check_replay_outputs as replay_check
import compare_validation_reports as compare_reports
import lint_dsl


REPORT_SCHEMA_VERSION = "1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="一键运行 Dify DSL 前向验证套件")
    parser.add_argument("cases_roots", nargs="*", help="一个或多个 case 根目录")
    parser.add_argument("--repo-root", dest="repo_root", help="仓库根目录")
    parser.add_argument("--skip-replay", action="store_true", help="只做 case 结构校验，不做回放断言")
    parser.add_argument("--json-out", dest="json_out", help="把汇总报告写入 JSON 文件")
    parser.add_argument("--baseline-report", dest="baseline_report", help="上一份 JSON 报告，用于输出对比结果")
    parser.add_argument("--diff-json-out", dest="diff_json_out", help="把和 baseline 的 diff 写入 JSON 文件")
    return parser.parse_args()


def discover_case_roots(repo_root: Path, raw_roots: list[str]) -> list[Path]:
    if raw_roots:
        return [Path(raw).resolve() for raw in raw_roots]
    return case_check.discover_case_roots(repo_root)


def collect_case_dirs(cases_roots: list[Path]) -> tuple[list[str], list[Path]]:
    errors: list[str] = []
    case_dirs: list[Path] = []
    for cases_root in cases_roots:
        if not cases_root.exists():
            errors.append(f"{cases_root}: case 根目录不存在")
            continue
        root_case_dirs = sorted(path for path in cases_root.iterdir() if path.is_dir())
        if not root_case_dirs:
            errors.append(f"{cases_root}: 下没有 case 目录")
            continue
        case_dirs.extend(root_case_dirs)
    return errors, case_dirs


def build_report(
    repo_root: Path,
    cases_roots: list[Path],
    summaries: list[dict],
    route_hits: dict[str, list[str]],
    entry_hits: dict[str, list[str]],
    structure_errors: list[str],
    lint_errors: list[str],
    replay_errors: list[str],
    skip_replay: bool,
) -> dict:
    missing_routes = [route for route in case_check.CANONICAL_ROUTES if route not in route_hits]
    missing_entry_skills = [entry_skill for entry_skill in case_check.ENTRY_SKILLS if entry_skill not in entry_hits]
    structure_ok = not structure_errors
    lint_ok = not lint_errors
    replay_ok = True if skip_replay else not replay_errors
    suite_ok = structure_ok and lint_ok and replay_ok and not missing_routes and not missing_entry_skills

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "cases_roots": [str(path) for path in cases_roots],
        "case_count": len(summaries),
        "skip_replay": skip_replay,
        "cases": summaries,
        "entry_skill_coverage": {
            entry_skill: entry_hits.get(entry_skill, [])
            for entry_skill in case_check.ENTRY_SKILLS
        },
        "route_coverage": {
            route: route_hits.get(route, [])
            for route in case_check.CANONICAL_ROUTES
        },
        "structure_errors": structure_errors,
        "lint_errors": lint_errors,
        "replay_errors": replay_errors,
        "missing_routes": missing_routes,
        "missing_entry_skills": missing_entry_skills,
        "structure_ok": structure_ok,
        "lint_ok": lint_ok,
        "replay_ok": replay_ok,
        "suite_ok": suite_ok,
    }


def validate_lint_case(repo_root: Path, case_dir: Path) -> tuple[list[str], dict]:
    oracle_path = case_dir / "oracle.json"
    if not oracle_path.exists():
        return [], {
            "lint_status": "skipped",
            "lint_error_count": 0,
            "lint_warning_count": 0,
            "lint_error_codes": [],
        }

    try:
        oracle = case_check.load_json(oracle_path)
    except json.JSONDecodeError as exc:
        return [f"{case_dir}: oracle.json 解析失败 -> {exc}"], {
            "lint_status": "failed",
            "lint_error_count": 0,
            "lint_warning_count": 0,
            "lint_error_codes": [],
        }

    target = oracle.get("target")
    if not target:
        return [], {
            "lint_status": "skipped",
            "lint_error_count": 0,
            "lint_warning_count": 0,
            "lint_error_codes": [],
        }

    target_path = case_check.resolve_target(repo_root, case_dir, target)
    if not target_path or not target_path.exists():
        return [f"{case_dir}: lint 目标不存在 -> {target}"], {
            "lint_status": "failed",
            "lint_error_count": 0,
            "lint_warning_count": 0,
            "lint_error_codes": [],
        }

    try:
        data = lint_dsl.load_yaml_via_ruby(target_path)
    except Exception as exc:
        return [f"{case_dir}: lint 解析失败 -> {exc}"], {
            "lint_status": "failed",
            "lint_error_count": 0,
            "lint_warning_count": 0,
            "lint_error_codes": [],
        }

    lint_report = lint_dsl.lint_dsl(target_path, data)
    actual_status = "issues" if lint_report["error_count"] > 0 else "clean"
    expected_status = oracle.get("expected_lint_status") or "clean"
    expected_error_codes = oracle.get("expected_lint_error_codes")
    actual_error_codes = sorted(
        {
            issue["code"]
            for issue in lint_report["issues"]
            if issue["severity"] == "error"
        }
    )

    errors: list[str] = []
    if expected_status != actual_status:
        errors.append(
            f"{case_dir}: expected_lint_status 不一致 -> expected={expected_status}, actual={actual_status}"
        )

    if expected_error_codes is not None:
        expected_error_codes = sorted(expected_error_codes)
        if expected_error_codes != actual_error_codes:
            errors.append(
                f"{case_dir}: expected_lint_error_codes 不一致 -> "
                f"expected={expected_error_codes}, actual={actual_error_codes}"
            )

    return errors, {
        "lint_status": actual_status,
        "lint_error_count": lint_report["error_count"],
        "lint_warning_count": lint_report["warning_count"],
        "lint_error_codes": actual_error_codes,
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else CURRENT_DIR.parents[2]
    cases_roots = discover_case_roots(repo_root, args.cases_roots)
    if not cases_roots:
        print(f"错误: 在 {repo_root} 下没有找到任何 case 根目录", file=sys.stderr)
        return 1

    root_errors, case_dirs = collect_case_dirs(cases_roots)
    if root_errors:
        for error in root_errors:
            print(f"错误: {error}", file=sys.stderr)
        return 1

    structure_errors: list[str] = []
    lint_errors: list[str] = []
    replay_errors: list[str] = []
    summaries: list[dict] = []
    route_hits: dict[str, list[str]] = defaultdict(list)
    entry_hits: dict[str, list[str]] = defaultdict(list)

    for case_dir in case_dirs:
        case_errors, summary = case_check.validate_case(repo_root, case_dir)
        structure_errors.extend(case_errors)
        if summary:
            summary["structure_ok"] = not case_errors
            entry_hits[summary["entry_skill"]].append(case_dir.name)
            for route in summary["expected_routes"]:
                route_hits[route].append(case_dir.name)
        else:
            summary = {
                "case_dir": str(case_dir),
                "goal": "(unknown)",
                "entry_skill": "(unknown)",
                "expected_routes": [],
                "target": None,
                "structure_ok": False,
            }

        case_lint_errors, lint_summary = validate_lint_case(repo_root, case_dir)
        lint_errors.extend(case_lint_errors)
        summary.update(lint_summary)

        if args.skip_replay:
            summary["replay_status"] = "skipped"
        else:
            case_replay_errors, replay_notes = replay_check.validate_case(case_dir, repo_root)
            replay_errors.extend(case_replay_errors)
            if case_replay_errors:
                summary["replay_status"] = "failed"
            elif any("跳过" in note for note in replay_notes):
                summary["replay_status"] = "skipped"
            else:
                summary["replay_status"] = "passed"

        summaries.append(summary)

    report = build_report(
        repo_root=repo_root,
        cases_roots=cases_roots,
        summaries=summaries,
        route_hits=route_hits,
        entry_hits=entry_hits,
        structure_errors=structure_errors,
        lint_errors=lint_errors,
        replay_errors=replay_errors,
        skip_replay=args.skip_replay,
    )

    diff: dict | None = None
    if args.baseline_report:
        baseline_report = compare_reports.load_report(args.baseline_report)
        diff = compare_reports.build_diff(baseline_report, report)

    if args.json_out:
        json_out_path = Path(args.json_out).expanduser().resolve()
        json_out_path.parent.mkdir(parents=True, exist_ok=True)
        json_out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.diff_json_out and diff is not None:
        diff_out_path = Path(args.diff_json_out).expanduser().resolve()
        diff_out_path.parent.mkdir(parents=True, exist_ok=True)
        diff_out_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"case 根目录数: {len(cases_roots)}")
    print(f"case 数: {len(case_dirs)}")
    print("")
    print("case 摘要:")
    for summary in summaries:
        print(
            "- "
            + f"{Path(summary['case_dir']).name} | goal={summary['goal']} | "
            + f"entry_skill={summary['entry_skill']} | "
            + f"target={summary['target'] or '(none)'} | "
            + f"structure={'通过' if summary['structure_ok'] else '失败'} | "
            + f"lint={summary['lint_status']} | "
            + f"replay={summary['replay_status']}"
        )

    print("")
    print("入口 skill 覆盖矩阵:")
    for entry_skill in case_check.ENTRY_SKILLS:
        hits = entry_hits.get(entry_skill)
        if hits:
            print(f"- {entry_skill}: 已覆盖 ({', '.join(hits)})")
        else:
            print(f"- {entry_skill}: 未覆盖")

    print("")
    print("底座 skill 覆盖矩阵:")
    for route in case_check.CANONICAL_ROUTES:
        hits = route_hits.get(route)
        if hits:
            print(f"- {route}: 已覆盖 ({', '.join(hits)})")
        else:
            print(f"- {route}: 未覆盖")

    print("")
    if structure_errors:
        print("结构校验错误:")
        for error in structure_errors:
            print(f"- {error}")
    else:
        print("结构校验: 通过")

    if lint_errors:
        print("lint 校验错误:")
        for error in lint_errors:
            print(f"- {error}")
    else:
        print("lint 校验: 通过")

    if args.skip_replay:
        print("回放断言: 已跳过")
    elif replay_errors:
        print("回放断言错误:")
        for error in replay_errors:
            print(f"- {error}")
    else:
        print("回放断言: 通过")

    if diff is not None:
        print("")
        compare_reports.print_diff(diff)

    missing_routes = report["missing_routes"]
    missing_entry_skills = report["missing_entry_skills"]

    print("")
    if structure_errors or replay_errors or missing_routes or missing_entry_skills:
        if missing_routes:
            print(f"结论: 仍缺这些底座 skill 覆盖 -> {', '.join(missing_routes)}")
        if missing_entry_skills:
            print(f"结论: 仍缺这些入口 skill 覆盖 -> {', '.join(missing_entry_skills)}")
        if structure_errors:
            print("结论: case 结构校验未通过")
        if lint_errors:
            print("结论: lint 校验未通过")
        if replay_errors:
            print("结论: 回放断言未通过")
        if args.json_out:
            print(f"JSON 报告: {Path(args.json_out).expanduser().resolve()}")
        if args.diff_json_out and diff is not None:
            print(f"JSON diff: {Path(args.diff_json_out).expanduser().resolve()}")
        return 1

    print("结论: 前向验证套件通过")
    if args.json_out:
        print(f"JSON 报告: {Path(args.json_out).expanduser().resolve()}")
    if args.diff_json_out and diff is not None:
        print(f"JSON diff: {Path(args.diff_json_out).expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
