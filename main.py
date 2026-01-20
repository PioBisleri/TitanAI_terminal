#!/usr/bin/env python3
import sys
from src.utils import check_dependencies

# 1. Pre-flight checks
check_dependencies()

# 2. Launch Application
if __name__ == "__main__":
    from src.app import TitanTerminal
    app = TitanTerminal()
    try:
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
