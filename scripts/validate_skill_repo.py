#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


SKILL_LINK_REQUIREMENTS = (
    "references/index.md",
    "references/foundations/index.md",
    "references/foundations/common-dsl.md",
    "references/foundations/task-routing.md",
    "references/nodes/index.md",
    "references/templates/index.md",
    "references/quality/index.md",
    "references/governance/index.md",
    "references/foundations/output-contract.md",
    "references/foundations/validation-contract.md",
)

REFERENCE_INDEX_REQUIREMENTS = {
    "references": {
        "index": "index.md",
        "required_links": (
            "foundations/index.md",
            "nodes/index.md",
            "templates/index.md",
            "quality/index.md",
            "governance/index.md",
        ),
        "allow_unlinked": (),
        "required_headings": ("## 按任务快速路由", "## 使用约束"),
    },
    "references/foundations": {
        "index": "index.md",
        "required_links": (
            "common-dsl.md",
            "task-routing.md",
            "output-contract.md",
            "validation-contract.md",
            "orchestration-modes.md",
            "selector-templates.md",
            "output-fields-catalog.md",
            "node-io-contracts.md",
            "field-explanations.md",
            "fixture-index.md",
        ),
        "allow_unlinked": (),
        "required_headings": ("## 按问题选文档", "## 典型请求", "## 使用约束"),
    },
    "references/nodes": {
        "index": "index.md",
        "required_links": (
            "node-start.md",
            "node-answer.md",
            "node-end.md",
            "node-llm.md",
            "node-agent.md",
            "node-parameter-extractor.md",
            "node-question-classifier.md",
            "node-if-else.md",
            "node-iteration.md",
            "node-loop.md",
            "node-variable-aggregator.md",
            "node-variable-assigner.md",
            "node-list-operator.md",
            "node-code.md",
            "node-template-transform.md",
            "node-http-request.md",
            "node-tool.md",
            "node-document-extractor.md",
            "node-knowledge-retrieval.md",
            "node-knowledge-index.md",
            "node-datasource.md",
            "node-human-input.md",
            "node-trigger-plugin.md",
            "node-trigger-schedule.md",
            "node-trigger-webhook.md",
        ),
        "allow_unlinked": ("node-index.md",),
        "required_headings": ("## 建议读取顺序", "## 典型请求"),
    },
    "references/templates": {
        "index": "index.md",
        "required_links": (
            "templates-library.md",
            "template-validation-status.md",
            "validated-template-skeletons.md",
            "template-variants.md",
        ),
        "allow_unlinked": (),
        "required_headings": ("## 按问题选文档", "## 典型请求", "## 使用约束"),
    },
    "references/quality": {
        "index": "index.md",
        "required_links": (
            "graph-validation-rules.md",
            "fix-strategies.md",
            "anti-patterns.md",
            "review-checklist.md",
            "report-template.md",
            "subagent-review.md",
            "forward-test-playbook.md",
            "graded-review-model.md",
            "failure-output-patterns.md",
            "decision-tables.md",
            "mode-constraints.md",
            "connectivity-analysis.md",
            "optimization-playbook.md",
            "tuning-playbook.md",
        ),
        "allow_unlinked": (),
        "required_headings": ("## 按问题选文档", "## 典型请求", "## 使用约束"),
    },
    "references/governance": {
        "index": "index.md",
        "required_links": (
            "evaluation-gates.md",
            "change-impact-review.md",
            "coverage-matrix.md",
            "minimal-sufficiency.md",
            "escalation-policies.md",
            "observability-contract.md",
            "capability-contracts.md",
            "issue-taxonomy.md",
        ),
        "allow_unlinked": (),
        "required_headings": ("## 按问题选文档", "## 典型请求", "## 使用约束"),
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    content = read_text(path)
    if not content.startswith("---\n"):
        return {}, [f"{path}: 缺少 YAML frontmatter 起始分隔线"]

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return {}, [f"{path}: YAML frontmatter 不完整"]

    raw_frontmatter = parts[1].strip().splitlines()
    data: dict[str, str] = {}
    for line in raw_frontmatter:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if not match:
            errors.append(f"{path}: 无法解析 frontmatter 行: {line}")
            continue
        key, value = match.groups()
        data[key] = value

    allowed_keys = {"name", "description"}
    extra_keys = sorted(set(data) - allowed_keys)
    if extra_keys:
        errors.append(f"{path}: frontmatter 只允许 name/description，发现额外字段: {', '.join(extra_keys)}")

    if not data.get("name"):
        errors.append(f"{path}: frontmatter 缺少 name")
    elif not re.fullmatch(r"[a-z0-9-]+", data["name"]):
        errors.append(f"{path}: name 只能包含小写字母、数字和连字符")

    if not data.get("description"):
        errors.append(f"{path}: frontmatter 缺少 description")

    return data, errors


def parse_openai_yaml(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    data: dict[str, str] = {}
    current_section = ""

    for raw_line in read_text(path).splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if re.fullmatch(r"[A-Za-z0-9_-]+:", line):
            current_section = line[:-1]
            continue
        match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*(.+?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip('"')
        data[f"{current_section}.{key}"] = value

    required_keys = (
        "interface.display_name",
        "interface.short_description",
        "interface.default_prompt",
        "policy.allow_implicit_invocation",
    )
    for key in required_keys:
        if not data.get(key):
            errors.append(f"{path}: 缺少 {key}")

    allow_implicit = data.get("policy.allow_implicit_invocation")
    if allow_implicit not in {"true", "false"}:
        errors.append(f"{path}: policy.allow_implicit_invocation 必须是 true 或 false")

    return data, errors


def collect_markdown_files(root: Path) -> list[Path]:
    files = [root / "SKILL.md"]
    files.extend(sorted((root / "references").rglob("*.md")))
    files.extend(sorted(root.glob("README*.md")))
    return [path for path in files if path.exists()]


def validate_links(path: Path) -> list[str]:
    errors: list[str] = []
    content = read_text(path)
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = raw_target.split("#", 1)[0].strip()
        if not target:
            continue
        if re.match(r"^[a-z]+://", target):
            continue
        if target.startswith("mailto:"):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: 链接目标不存在 -> {raw_target}")
    return errors


def validate_skill_links(path: Path) -> list[str]:
    content = read_text(path)
    errors: list[str] = []
    for required_link in SKILL_LINK_REQUIREMENTS:
        if required_link not in content:
            errors.append(f"{path}: 缺少核心引用 {required_link}")
    return errors


def collect_markdown_targets(path: Path) -> set[str]:
    targets: set[str] = set()
    content = read_text(path)
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = raw_target.split("#", 1)[0].strip()
        if not target:
            continue
        if re.match(r"^[a-z]+://", target):
            continue
        if target.startswith("mailto:"):
            continue
        targets.add(target)
    return targets


def validate_reference_indexes(root: Path) -> list[str]:
    errors: list[str] = []

    for dir_name, config in REFERENCE_INDEX_REQUIREMENTS.items():
        directory = root / dir_name
        index_path = directory / config["index"]

        if not directory.exists():
            errors.append(f"{directory}: 目录不存在")
            continue
        if not index_path.exists():
            errors.append(f"{index_path}: 缺少目录入口 index")
            continue

        index_content = read_text(index_path)
        linked_targets = collect_markdown_targets(index_path)
        for required_link in config["required_links"]:
            if required_link not in linked_targets:
                errors.append(f"{index_path}: 缺少到 {required_link} 的入口链接")

        for heading in config.get("required_headings", ()):
            if heading not in index_content:
                errors.append(f"{index_path}: 缺少必要章节 {heading}")

        allow_unlinked = set(config["allow_unlinked"])
        for file_path in sorted(directory.glob("*.md")):
            if file_path.name == config["index"]:
                continue
            if file_path.name in allow_unlinked:
                continue
            if file_path.name not in linked_targets:
                errors.append(f"{index_path}: 未覆盖同目录文档 {file_path.name}")

    alias_path = root / "references" / "nodes" / "node-index.md"
    if alias_path.exists():
        alias_targets = collect_markdown_targets(alias_path)
        if "index.md" not in alias_targets:
            errors.append(f"{alias_path}: 兼容入口必须指向 index.md")

    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []
    warnings: list[str] = []

    skill_path = root / "SKILL.md"
    openai_yaml_path = root / "agents" / "openai.yaml"

    if not skill_path.exists():
        print(f"错误: {skill_path} 不存在", file=sys.stderr)
        return 1
    if not openai_yaml_path.exists():
        print(f"错误: {openai_yaml_path} 不存在", file=sys.stderr)
        return 1

    frontmatter, frontmatter_errors = parse_frontmatter(skill_path)
    errors.extend(frontmatter_errors)

    openai_yaml, yaml_errors = parse_openai_yaml(openai_yaml_path)
    errors.extend(yaml_errors)

    skill_name = frontmatter.get("name")
    default_prompt = openai_yaml.get("interface.default_prompt", "")
    if skill_name and f"${skill_name}" not in default_prompt:
        errors.append(f"{openai_yaml_path}: interface.default_prompt 需要显式包含 ${skill_name}")

    skill_lines = read_text(skill_path).splitlines()
    if len(skill_lines) > 500:
        warnings.append(f"{skill_path}: 行数为 {len(skill_lines)}，建议控制在 500 行以内")

    errors.extend(validate_skill_links(skill_path))
    errors.extend(validate_reference_indexes(root))
    for markdown_path in collect_markdown_files(root):
        errors.extend(validate_links(markdown_path))

    if warnings:
        for warning in warnings:
            print(f"警告: {warning}")

    if errors:
        for error in errors:
            print(f"错误: {error}")
        return 1

    print(f"通过: {root} 的 skill 结构检查已完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
