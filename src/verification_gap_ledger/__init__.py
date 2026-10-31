"""Verification Gap Ledger: an open, source-coded register of federal and New York State
programs that fund municipal energy and infrastructure.

Each program is coded on three ordinal scales:

* R, required verification (0 to 4)
* C, results made public (0 to 4)
* A, attributability (0 to 3)

Every code is tied to a cited source document and locator in the evidence table.

Quick start::

    import verification_gap_ledger as vgl

    vgl.programs()                   # list of program records (dicts)
    vgl.program("VGL-NY-006")        # one program
    vgl.evidence("VGL-NY-006")       # evidence items behind its codes
    vgl.programs(as_frame=True)      # pandas DataFrame (needs pandas)
    print(vgl.citation())

The bundled data are byte-identical to the archived release; see ``DOI`` and ``CONCEPT_DOI``.
"""

from ._data import (
    CONCEPT_DOI,
    DATA_VERSION,
    DOI,
    SCALES,
    citation,
    data_path,
    evidence,
    program,
    programs,
    reference_sources,
    stats,
)

__version__ = "0.1.1"

__all__ = [
    "__version__",
    "DATA_VERSION",
    "DOI",
    "CONCEPT_DOI",
    "SCALES",
    "programs",
    "program",
    "evidence",
    "reference_sources",
    "stats",
    "citation",
    "data_path",
]
