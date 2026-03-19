#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
HARNESS_DIR = CURRENT_DIR.parent / "tests" / "harness"
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

from assert_output import load_expectation, validate_expectation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="批量校验前向验证回放输出")
    parser.add_argument("case_dirs", nargs="*", help="一个或多个 case 目录")
    parser.add_argument("--repo-root", dest="repo_root", help="仓库根目录")
    return parser.parse_args()


def load_oracle(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def discover_case_dirs(repo_root: Path) -> list[Path]:
    case_dirs: list[Path] = []
    for cases_root in sorted((repo_root / "skills").glob("*/tests/cases")):
        if not cases_root.exists():
            continue
        for case_dir in sorted(path for path in cases_root.iterdir() if path.is_dir()):
            case_dirs.append(case_dir)
    return case_dirs


def resolve_path(case_dir: Path, repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    case_candidate = (case_dir / candidate).resolve()
    if case_candidate.exists():
        return case_candidate
    return (repo_root / candidate).resolve()


def validate_case(case_dir: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    oracle_path = case_dir / "oracle.json"
    if not oracle_path.exists():
        return [f"{case_dir}: 缺少 oracle.json"], notes

    oracle = load_oracle(oracle_path)
    expectation_files = oracle.get("expectation_files") or []
    if not expectation_files:
        notes.append(f"{case_dir.name}: 未配置 expectation_files，跳过输出断言")
        return errors, notes

    output_file = oracle.get("replay_output_file", "replay-output.txt")
    output_path = resolve_path(case_dir, repo_root, output_file)
    if not output_path.exists():
        return [f"{case_dir}: 回放输出不存在 -> {output_file}"], notes

    text = output_path.read_text(encoding="utf-8")
    for raw_expectation in expectation_files:
        expectation_path = resolve_path(case_dir, repo_root, raw_expectation)
        if not expectation_path.exists():
            errors.append(f"{case_dir}: expectation 不存在 -> {raw_expectation}")
            continue
        expectation = load_expectation(str(expectation_path))
        expectation_errors = validate_expectation(expectation, text)
        errors.extend(f"{case_dir.name} | {expectation_path.name}: {error}" for error in expectation_errors)

    if not errors:
        notes.append(f"{case_dir.name}: 输出断言通过")
    return errors, notes


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else CURRENT_DIR.parents[2]
    case_dirs = [Path(raw).resolve() for raw in args.case_dirs] if args.case_dirs else discover_case_dirs(repo_root)
    if not case_dirs:
        print(f"错误: 在 {repo_root} 下没有找到任何 case 目录", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    notes: list[str] = []
    for case_dir in case_dirs:
        case_errors, case_notes = validate_case(case_dir, repo_root)
        all_errors.extend(case_errors)
        notes.extend(case_notes)

    for note in notes:
        print(note)

    if all_errors:
        for error in all_errors:
            print(f"错误: {error}", file=sys.stderr)
        return 1

    print(f"通过: 共校验 {len(case_dirs)} 个回放输出")
    return 0


if __name__ == "__main__":
    sys.exit(main())
