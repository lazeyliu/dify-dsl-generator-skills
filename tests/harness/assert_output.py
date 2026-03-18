#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def load_expectation(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("用法: python3 tests/harness/assert_output.py <expectation.json> [text-file]", file=sys.stderr)
        return 1

    expectation = load_expectation(sys.argv[1])
    text = read_text(sys.argv[2] if len(sys.argv) == 3 else None)
    errors: list[str] = []

    for marker in expectation.get("ordered_markers", []):
        if marker not in text:
            errors.append(f"缺少顺序标记: {marker}")
    ordered_markers = expectation.get("ordered_markers", [])
    if ordered_markers:
        positions = [text.find(marker) for marker in ordered_markers if marker in text]
        if positions != sorted(positions):
            errors.append("ordered_markers 顺序不正确")

    must_contain_any = expectation.get("must_contain_any", [])
    if must_contain_any and not any(marker in text for marker in must_contain_any):
        errors.append(f"至少应包含其中之一: {must_contain_any}")

    for marker in expectation.get("must_not_contain", []):
        if marker in text:
            errors.append(f"不应包含: {marker}")

    if errors:
        for error in errors:
            print(f"错误: {error}", file=sys.stderr)
        return 1

    print("通过: 输出符合预期")
    return 0


if __name__ == "__main__":
    sys.exit(main())
