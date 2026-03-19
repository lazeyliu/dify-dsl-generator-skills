#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_SCRIPT = REPO_ROOT / "skills" / "dify-dsl-forward-testing" / "scripts" / "run_validation_suite.py"
DEFAULT_REPORT_DIR = REPO_ROOT / ".forward-testing"
LAST_GOOD_REPORT_NAME = "last-good.json"
LATEST_REPORT_NAME = "latest-report.json"
LATEST_DIFF_NAME = "latest-diff.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从仓库根目录运行 Dify DSL 前向验证套件")
    parser.add_argument("cases_roots", nargs="*", help="可选：一个或多个 case 根目录")
    parser.add_argument("--skip-replay", action="store_true", help="只做 case 结构校验，不做回放断言")
    parser.add_argument("--baseline-report", dest="baseline_report", help="上一份 JSON 报告路径")
    parser.add_argument("--no-auto-baseline", action="store_true", help="即使存在 `.forward-testing/last-good.json` 也不要自动对比")
    parser.add_argument("--json-out", dest="json_out", help="当前报告输出路径")
    parser.add_argument("--diff-json-out", dest="diff_json_out", help="diff 报告输出路径")
    parser.add_argument("--last-good-path", dest="last_good_path", help="last-good 基线路径，默认是 `.forward-testing/last-good.json`")
    parser.add_argument("--promote-current", action="store_true", help="如果本轮验证通过，把当前报告提升为新的 last-good 基线")
    parser.add_argument(
        "--report-dir",
        dest="report_dir",
        help="默认报告目录；未传 `--json-out` / `--diff-json-out` 时使用，默认是仓库下的 `.forward-testing/`",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_dir = Path(args.report_dir).expanduser().resolve() if args.report_dir else DEFAULT_REPORT_DIR
    json_out = Path(args.json_out).expanduser().resolve() if args.json_out else report_dir / LATEST_REPORT_NAME
    last_good_path = (
        Path(args.last_good_path).expanduser().resolve()
        if args.last_good_path
        else report_dir / LAST_GOOD_REPORT_NAME
    )

    baseline_report = None
    if args.baseline_report:
        baseline_report = Path(args.baseline_report).expanduser().resolve()
    elif not args.no_auto_baseline and last_good_path.exists():
        baseline_report = last_good_path

    diff_json_out = None
    if baseline_report:
        diff_json_out = (
            Path(args.diff_json_out).expanduser().resolve()
            if args.diff_json_out
            else report_dir / LATEST_DIFF_NAME
        )

    cmd = [
        sys.executable,
        str(SUITE_SCRIPT),
        "--repo-root",
        str(REPO_ROOT),
        "--json-out",
        str(json_out),
    ]
    if args.skip_replay:
        cmd.append("--skip-replay")
    if baseline_report:
        cmd.extend(["--baseline-report", str(baseline_report)])
    if diff_json_out:
        cmd.extend(["--diff-json-out", str(diff_json_out)])
    cmd.extend(str(Path(raw).expanduser().resolve()) for raw in args.cases_roots)

    result = subprocess.run(cmd, check=False)
    if result.returncode == 0 and args.promote_current:
        last_good_path.parent.mkdir(parents=True, exist_ok=True)
        if json_out != last_good_path:
            shutil.copy2(json_out, last_good_path)
        print(f"已提升当前报告为基线: {last_good_path}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
