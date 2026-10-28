"""Allow ``python3 -m shift_pay`` to run the CLI."""

from __future__ import annotations

import sys

from shift_pay.cli import main

if __name__ == "__main__":
    main()
