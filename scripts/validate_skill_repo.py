#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


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
        data[f"{current_section}.{key}"] = value.strip('"')

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
    if allow_implicit and allow_implicit not in {"true", "false"}:
        errors.append(f"{path}: policy.allow_implicit_invocation 必须是 true 或 false")

    return data, errors


def collect_markdown_targets(path: Path) -> set[str]:
    content = read_text(path)
    targets: set[str] = set()
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


def validate_links(skill_root: Path) -> list[str]:
    errors: list[str] = []
    for markdown_path in sorted(skill_root.rglob("*.md")):
        for target in collect_markdown_targets(markdown_path):
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{markdown_path}: 链接目标不存在 -> {target}")
    return errors


def validate_skill(skill_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_path = skill_root / "SKILL.md"
    if not skill_path.exists():
        return [f"{skill_root}: 缺少 SKILL.md"], warnings

    frontmatter, frontmatter_errors = parse_frontmatter(skill_path)
    errors.extend(frontmatter_errors)

    skill_lines = read_text(skill_path).splitlines()
    if len(skill_lines) > 500:
        warnings.append(f"{skill_path}: 行数为 {len(skill_lines)}，建议控制在 500 行以内")

    openai_yaml_path = skill_root / "agents" / "openai.yaml"
    skill_name = frontmatter.get("name")
    if openai_yaml_path.exists():
        openai_yaml, yaml_errors = parse_openai_yaml(openai_yaml_path)
        errors.extend(yaml_errors)

        default_prompt = openai_yaml.get("interface.default_prompt", "")
        if skill_name and f"${skill_name}" not in default_prompt:
            errors.append(f"{openai_yaml_path}: interface.default_prompt 需要显式包含 ${skill_name}")
    elif skill_name and skill_name.startswith("using-"):
        warnings.append(f"{skill_root}: 未提供 agents/openai.yaml，将只做通用结构校验")

    errors.extend(validate_links(skill_root))
    return errors, warnings


def find_skill_dirs(target: Path) -> list[Path]:
    if (target / "SKILL.md").exists():
        return [target]

    skills_root = target / "skills"
    if not skills_root.exists():
        return []

    return sorted(path for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def run_deep_validator(skill_root: Path) -> tuple[list[str], list[str]]:
    validator = skill_root / "scripts" / "validate_skill_repo.py"
    current_script = Path(__file__).resolve()
    if not validator.exists() or validator.resolve() == current_script:
        return [], []

    result = subprocess.run(
        [sys.executable, str(validator), str(skill_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines() if line.strip()]
    messages = [f"[{skill_root.name}] {line}" for line in output]
    if result.returncode != 0:
        return messages, []
    return [], messages


def main() -> int:
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    skill_dirs = find_skill_dirs(target)
    if not skill_dirs:
        print(f"错误: 在 {target} 下没有找到可校验的 skill", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    for skill_root in skill_dirs:
        skill_errors, skill_warnings = validate_skill(skill_root)
        errors.extend(f"[{skill_root.name}] {message}" for message in skill_errors)
        warnings.extend(f"[{skill_root.name}] {message}" for message in skill_warnings)

        deep_errors, deep_notes = run_deep_validator(skill_root)
        errors.extend(deep_errors)
        notes.extend(deep_notes)

    for warning in warnings:
        print(f"警告: {warning}")

    for note in notes:
        print(note)

    if errors:
        for error in errors:
            print(f"错误: {error}")
        return 1

    if (target / "SKILL.md").exists():
        print(f"通过: {target} 的 skill 结构检查已完成")
    else:
        print(f"通过: {target} 下共校验 {len(skill_dirs)} 个 skill")
    return 0


if __name__ == "__main__":
    sys.exit(main())
