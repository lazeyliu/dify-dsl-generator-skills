#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from validate_skill_repo import main as validate_main


if __name__ == "__main__":
    sys.exit(validate_main())
