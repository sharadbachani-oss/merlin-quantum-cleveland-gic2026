# -*- coding: utf-8 -*-
"""Cleveland Dirac geometry leftover. Does not relabel AQT FAIL as Dirac."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_dirac_advantage as R
if __name__ == "__main__":
    raise SystemExit(R.main())
