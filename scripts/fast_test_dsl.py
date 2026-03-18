#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def load_yaml_via_ruby(path: Path) -> dict:
    ruby_code = """
require "yaml"
require "json"

path = ARGV[0]
data = YAML.load_file(path)
puts JSON.generate(data)
"""
    result = subprocess.run(
        ["ruby", "-e", ruby_code, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Ruby YAML 解析失败")
    return json.loads(result.stdout)


def get_node_type(node: dict) -> str:
    if not isinstance(node, dict):
        return "unknown"
    data = node.get("data")
    if isinstance(data, dict):
        node_type = data.get("type")
        if isinstance(node_type, str) and node_type:
            return node_type
    node_type = node.get("type")
    if isinstance(node_type, str) and node_type:
        return node_type
    return "unknown"


def classify_routes(kind: str, mode: str, node_types: set[str], dependency_count: int, conversation_var_count: int) -> list[str]:
    routes = ["references/index.md", "references/foundations/index.md"]

    if node_types:
        routes.append("references/nodes/index.md")

    if kind == "app" and mode == "advanced-chat":
        if "question-classifier" in node_types or "knowledge-retrieval" in node_types or conversation_var_count > 0:
            routes.append("references/quality/index.md")
            routes.append("references/governance/index.md")

    if dependency_count > 0 or conversation_var_count > 0:
        if "references/governance/index.md" not in routes:
            routes.append("references/governance/index.md")

    return routes


def build_complexity_signals(node_types: Counter[str], dependency_count: int, conversation_var_count: int, edge_count: int) -> list[str]:
    signals: list[str] = []
    if conversation_var_count > 0:
        signals.append(f"存在 {conversation_var_count} 个 conversation variables，属于多轮状态链路。")
    if dependency_count > 0:
        signals.append(f"存在 {dependency_count} 个插件依赖，需要纳入版本与兼容性审查。")
    if node_types.get("question-classifier", 0):
        signals.append("包含 question-classifier，默认分支覆盖与分类结果约束要重点审查。")
    if node_types.get("knowledge-retrieval", 0):
        signals.append("包含 knowledge-retrieval，需要补证据来源、检索失败和结果一致性检查。")
    if node_types.get("assigner", 0):
        signals.append("包含 assigner，需核对变量写入域、写入时机和下游消费关系。")
    if node_types.get("code", 0) >= 3:
        signals.append(f"包含 {node_types['code']} 个 code 节点，运行时与内容一致性要纳入实体校验。")
    if edge_count >= 20:
        signals.append(f"当前图有 {edge_count} 条边，已超过轻量链路，建议按质量与治理双层路线审查。")
    return signals


def analyze_dsl(path: Path, data: dict) -> dict:
    kind = data.get("kind", "")
    app = data.get("app") or {}
    workflow = data.get("workflow") or {}
    graph = workflow.get("graph") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    dependencies = data.get("dependencies") or []
    conversation_variables = workflow.get("conversation_variables") or []

    node_types = Counter(get_node_type(node) for node in nodes)
    unique_node_types = sorted(node_types)
    mode = app.get("mode", "")
    routes = classify_routes(kind, mode, set(unique_node_types), len(dependencies), len(conversation_variables))
    complexity_signals = build_complexity_signals(node_types, len(dependencies), len(conversation_variables), len(edges))

    return {
        "path": str(path),
        "kind": kind or "(unknown)",
        "mode": mode or "(unknown)",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "dependency_count": len(dependencies),
        "conversation_variable_count": len(conversation_variables),
        "routes": routes,
        "node_types": dict(node_types),
        "complexity_signals": complexity_signals,
    }


def render_report(path: Path, data: dict) -> str:
    analysis = analyze_dsl(path, data)

    lines = [
        f"样本: {analysis['path']}",
        f"kind: {analysis['kind']}",
        f"mode: {analysis['mode']}",
        f"节点数: {analysis['node_count']}",
        f"边数: {analysis['edge_count']}",
        f"依赖数: {analysis['dependency_count']}",
        f"conversation variables: {analysis['conversation_variable_count']}",
        "",
        "命中的目录入口:",
    ]
    lines.extend(f"- {route}" for route in analysis["routes"])
    lines.extend(
        [
            "",
            "节点类型分布:",
        ]
    )
    lines.extend(
        f"- {node_type}: {analysis['node_types'][node_type]}"
        for node_type in sorted(analysis["node_types"])
    )
    lines.extend(
        [
            "",
            "复杂度信号:",
        ]
    )
    if analysis["complexity_signals"]:
        lines.extend(f"- {signal}" for signal in analysis["complexity_signals"])
    else:
        lines.append("- 未发现明显高复杂度信号。")

    lines.extend(
        [
            "",
            "fast-test 结论:",
            "- 这个样本适合做 advanced-chat、多轮状态、分类分支、检索链路和治理门禁的快速回归样本。",
        ]
    )
    if "references/templates/index.md" not in analysis["routes"]:
        lines.append("- 这个样本不会直接覆盖模板入口；模板路线仍需单独样本补齐。")

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python3 scripts/fast_test_dsl.py <dsl-path>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"错误: {path} 不存在", file=sys.stderr)
        return 1

    try:
        data = load_yaml_via_ruby(path)
    except Exception as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    print(render_report(path, data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
