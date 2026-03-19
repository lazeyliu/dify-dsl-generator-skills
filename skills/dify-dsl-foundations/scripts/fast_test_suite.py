#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from fast_test_dsl import analyze_dsl, load_yaml_via_ruby


CANONICAL_ROUTES = (
    "skills/dify-dsl-foundations/SKILL.md",
    "skills/dify-dsl-nodes/SKILL.md",
    "skills/dify-dsl-templates/SKILL.md",
    "skills/dify-dsl-quality/SKILL.md",
    "skills/dify-dsl-governance/SKILL.md",
)


def collect_yaml_files(args: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in args:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(str(path))
        if path.is_file():
            if path.suffix.lower() in {".yml", ".yaml"}:
                files.append(path)
            continue
        files.extend(sorted(p for p in path.rglob("*") if p.suffix.lower() in {".yml", ".yaml"}))
    unique_files: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        if path not in seen:
            seen.add(path)
            unique_files.append(path)
    return unique_files


def render_suite_report(analyses: list[dict]) -> str:
    route_hits: dict[str, list[str]] = defaultdict(list)
    for analysis in analyses:
        for route in analysis["routes"]:
            route_hits[route].append(analysis["path"])

    missing_routes = [route for route in CANONICAL_ROUTES if route not in route_hits]
    lines = [
        f"样本数: {len(analyses)}",
        "",
        "样本摘要:",
    ]
    for analysis in analyses:
        lines.append(
            "- "
            + f"{analysis['path']} | {analysis['kind']} / {analysis['mode']} | "
            + f"节点 {analysis['node_count']} | 边 {analysis['edge_count']} | "
            + f"入口 {', '.join(analysis['routes'])}"
        )

    lines.extend(
        [
            "",
            "入口覆盖矩阵:",
        ]
    )
    for route in CANONICAL_ROUTES:
        hits = route_hits.get(route)
        if hits:
            lines.append(f"- {route}: 已覆盖 ({len(hits)} 个样本)")
        else:
            lines.append(f"- {route}: 未覆盖")

    lines.extend(
        [
            "",
            "覆盖结论:",
        ]
    )
    if missing_routes:
        lines.append(f"- 当前样本池仍缺这些入口覆盖: {', '.join(missing_routes)}")
    else:
        lines.append("- 当前样本池已覆盖全部 canonical routes。")

    template_samples = [
        analysis["path"]
        for analysis in analyses
        if "skills/dify-dsl-templates/SKILL.md" in analysis["routes"]
    ]
    if template_samples:
        lines.append(f"- 已有模板路线样本: {', '.join(template_samples)}")
    else:
        lines.append("- 目前还没有命中 templates 入口的真实样本。")

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 scripts/fast_test_suite.py <sample.yml|directory> [...]", file=sys.stderr)
        return 1

    try:
        files = collect_yaml_files(sys.argv[1:])
    except FileNotFoundError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    if not files:
        print("错误: 未找到任何 .yml 或 .yaml 样本", file=sys.stderr)
        return 1

    analyses: list[dict] = []
    for path in files:
        try:
            data = load_yaml_via_ruby(path)
        except Exception as exc:
            print(f"错误: 解析 {path} 失败: {exc}", file=sys.stderr)
            return 1
        analyses.append(analyze_dsl(path, data))

    print(render_suite_report(analyses))
    return 0


if __name__ == "__main__":
    sys.exit(main())
