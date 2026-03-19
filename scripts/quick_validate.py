#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from validate_skill_repo import main as validate_main
from route_matrix_docs import main as validate_route_matrix_main


if __name__ == "__main__":
    status = validate_main()
    if status != 0:
        sys.exit(status)
    sys.exit(validate_route_matrix_main())
