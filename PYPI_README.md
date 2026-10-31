# Verification Gap Ledger

The Verification Gap Ledger is an open, versioned register of federal and New York State programs that fund municipal energy and infrastructure. For each program it records what verification of results is required (R, 0 to 4), what results are made public (C, 0 to 4), and whether an external party could attribute outcomes to the funding (A, 0 to 3). Every code is tied to a cited source document and locator.

This package bundles the released data (24 programs, 80 evidence items, data version 0.1.0) with a small Python interface and a command line tool. It has no required dependencies.

- Browse online: https://olumide-akindipe.github.io/verification-gap-ledger/
- Data archive (all versions): https://doi.org/10.5281/zenodo.23302897
- Source, codebook and coding protocol: https://github.com/Olumide-Akindipe/verification-gap-ledger

## Install

```
pip install verification-gap-ledger
pip install "verification-gap-ledger[pandas]"   # optional, for DataFrames
```

## Python

```python
import verification_gap_ledger as vgl

rows = vgl.programs()                      # list of dicts, codes as integers
federal = vgl.programs(level="federal")
p = vgl.program("VGL-NY-006")
print(p["R_required"], p["C_public"], p["A_attributable"])

for e in vgl.evidence("VGL-NY-006", dimension="R"):
    print(e["source"], e["locator"], e["url"])

df = vgl.programs(as_frame=True)           # needs pandas
print(vgl.SCALES["R"])                     # scale definitions
print(vgl.stats()["n_programs"])           # released summary statistics
print(vgl.citation("bibtex"))
```

## Command line

```
vgl info                          # release, DOIs, counts, scale definitions
vgl list --level state            # programs with R, C and A codes
vgl list --r 3 --format csv       # filter by code; table, csv or json output
vgl show VGL-NY-006 --notes       # one program with its evidence and notes
vgl evidence VGL-F-001 --dimension C
vgl export ./vgl_data             # copy the released CSV and JSON files
vgl cite --bibtex
```

## Scales

- **R, required verification (0 to 4):** financial only, outputs, estimated outcomes, measured outcomes against a baseline, independent verification.
- **C, results made public (0 to 4):** none, aggregate only, project-level outputs, project-level outcomes, machine-readable open project data.
- **A, attributability (0 to 3):** no baseline, baseline or modeled counterfactual only, measured pre/post, comparison group or impact evaluation.

## Cite

Akindipe, S. O. (2026). *Verification Gap Ledger* (Version 0.1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23622181

## License

Code: MIT. Data: CC BY 4.0.
