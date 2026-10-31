"""Copy the released data into the Python package (src/verification_gap_ledger/data).

Run after 01_build.py whenever the data change, then bump the version in pyproject.toml
and src/verification_gap_ledger/__init__.py. tests/test_package.py fails if the copies drift.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "src" / "verification_gap_ledger" / "data"
SOURCES = [
    ROOT / "data" / "processed" / "vgl_programs.csv",
    ROOT / "data" / "processed" / "vgl_evidence.csv",
    ROOT / "data" / "processed" / "vgl_reference_sources.csv",
    ROOT / "paper" / "stats.json",
]

DEST.mkdir(parents=True, exist_ok=True)
for src in SOURCES:
    shutil.copyfile(src, DEST / src.name)
    print(f"copied {src.relative_to(ROOT)} -> {(DEST / src.name).relative_to(ROOT)}")
