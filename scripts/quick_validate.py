#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from validate_skill_repo import main as validate_main
from route_matrix_docs import main as validate_route_matrix_main


def run_skill_md_final_validation() -> int:
    validator = CURRENT_DIR / "validate_skill_md.rb"
    args = [str(validator), *sys.argv[1:]]
    result = subprocess.run(["ruby", *args], capture_output=True, text=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    status = run_skill_md_final_validation()
    if status != 0:
        sys.exit(status)
    status = validate_main()
    if status != 0:
        sys.exit(status)
    sys.exit(validate_route_matrix_main())
