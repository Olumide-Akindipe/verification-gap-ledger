"""Loaders for the bundled Ledger tables. Standard library only; pandas is optional."""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_VERSION = "0.1.0"
DOI = "10.5281/zenodo.23622181"  # release 0.1.1
CONCEPT_DOI = "10.5281/zenodo.23302897"  # all versions

# Short labels as stored in the R_label, C_label and A_label columns (A 3 from docs/CODEBOOK.md,
# since no program in this release is coded A 3). Full definitions are in the codebook.
SCALES: Dict[str, Dict[int, str]] = {
    "R": {
        0: "financial only",
        1: "outputs",
        2: "estimated outcomes",
        3: "measured outcomes vs baseline",
        4: "independent M&V or evaluation",
    },
    "C": {
        0: "no public results",
        1: "aggregate only",
        2: "project-level outputs",
        3: "project-level outcomes",
        4: "machine-readable open project-level data",
    },
    "A": {
        0: "no baseline",
        1: "baseline or modeled counterfactual only",
        2: "measured pre/post",
        3: "comparison group or impact evaluation",
    },
}

_FILES = {
    "programs": "vgl_programs.csv",
    "evidence": "vgl_evidence.csv",
    "reference_sources": "vgl_reference_sources.csv",
    "stats": "stats.json",
}

_INT_COLUMNS = {
    "R_required",
    "C_public",
    "A_attributable",
    "gap_rc",
    "gap_outcome",
    "evidence_items",
    "open_verify_items",
    "code",
}
_BOOL_COLUMNS = {"needs_author_verification"}


def data_path(name: str) -> Path:
    """Return the filesystem path of a bundled file.

    ``name`` is one of ``programs``, ``evidence``, ``reference_sources`` or ``stats``.
    """
    if name not in _FILES:
        raise ValueError(f"unknown table {name!r}; choose from {sorted(_FILES)}")
    return Path(str(files("verification_gap_ledger") / "data" / _FILES[name]))


def _convert(row: Dict[str, str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in row.items():
        if key in _INT_COLUMNS:
            out[key] = int(value) if value not in ("", None) else None
        elif key in _BOOL_COLUMNS:
            out[key] = str(value).strip().lower() == "true"
        else:
            out[key] = value
    return out


@lru_cache(maxsize=None)
def _read(name: str) -> tuple:
    with open(data_path(name), newline="", encoding="utf-8") as fh:
        return tuple(_convert(r) for r in csv.DictReader(fh))


def _finish(rows: List[Dict[str, Any]], as_frame: bool):
    rows = [dict(r) for r in rows]
    if not as_frame:
        return rows
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "as_frame=True needs pandas: pip install 'verification-gap-ledger[pandas]'"
        ) from exc
    return pd.DataFrame(rows)


def programs(level: Optional[str] = None, as_frame: bool = False):
    """All coded programs, one record per program.

    ``level`` filters to ``"federal"`` or ``"state"``. ``as_frame=True`` returns a pandas DataFrame.
    """
    rows = list(_read("programs"))
    if level is not None:
        if level not in ("federal", "state"):
            raise ValueError("level must be 'federal' or 'state'")
        rows = [r for r in rows if r["level"] == level]
    return _finish(rows, as_frame)


def program(ledger_id: str) -> Dict[str, Any]:
    """One program by its Ledger identifier, for example ``"VGL-F-001"``."""
    for r in _read("programs"):
        if r["ledger_id"] == ledger_id:
            return dict(r)
    raise KeyError(f"no program with ledger_id {ledger_id!r}")


def evidence(
    ledger_id: Optional[str] = None,
    dimension: Optional[str] = None,
    as_frame: bool = False,
):
    """Evidence items (source, URL, locator, note) behind the codes.

    Filter by ``ledger_id`` and by ``dimension`` (``"R"``, ``"C"``, ``"A"`` or ``"STATUS"``).
    """
    rows = list(_read("evidence"))
    if ledger_id is not None:
        rows = [r for r in rows if r["ledger_id"] == ledger_id]
    if dimension is not None:
        rows = [r for r in rows if r["dimension"] == dimension]
    return _finish(rows, as_frame)


def reference_sources(as_frame: bool = False):
    """Cross-cutting reference sources (for example 2 CFR 200)."""
    return _finish(list(_read("reference_sources")), as_frame)


def stats() -> Dict[str, Any]:
    """The summary statistics released with the data (stats.json)."""
    with open(data_path("stats"), encoding="utf-8") as fh:
        return json.load(fh)


def citation(style: str = "apa") -> str:
    """Citation for the release. ``style`` is ``"apa"`` or ``"bibtex"``."""
    from . import __version__

    if style == "apa":
        return (
            f"Akindipe, S. O. (2026). Verification Gap Ledger (Version {__version__}) "
            f"[Data set]. Zenodo. https://doi.org/{DOI}"
        )
    if style == "bibtex":
        return (
            "@dataset{akindipe2026vgl,\n"
            "  author    = {Akindipe, Stephen Olumide},\n"
            "  title     = {Verification Gap Ledger},\n"
            "  year      = {2026},\n"
            f"  version   = {{{__version__}}},\n"
            "  publisher = {Zenodo},\n"
            f"  doi       = {{{DOI}}},\n"
            f"  url       = {{https://doi.org/{DOI}}}\n"
            "}"
        )
    raise ValueError("style must be 'apa' or 'bibtex'")
