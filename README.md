# Verification Gap Ledger

[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23302897.svg)](https://doi.org/10.5281/zenodo.23302897)

**Status: Release 0.1.1, 2026-10-24 (data unchanged from 0.1.0, released 2026-10-11). Concept DOI (all versions): [10.5281/zenodo.23302897](https://doi.org/10.5281/zenodo.23302897). Release 0.1.1 DOI: [10.5281/zenodo.23622181](https://doi.org/10.5281/zenodo.23622181). Version 0.1.0 DOI: [10.5281/zenodo.23302898](https://doi.org/10.5281/zenodo.23302898). Maintainer: Stephen Olumide Akindipe (ORCID [0000-0002-1846-9662](https://orcid.org/0000-0002-1846-9662)).**

> The Verification Gap Ledger (VGL) is an open versioned register containing federal and New York State programs targeted towards funding municipal energy and infrastructure. For each program, the VGL records three distinct parameters: what verification of results is required (R), what results are actually made publicly available (C), and whether an external party could attribute outcomes to the funding (A). Every rating is directly linked to the exact source document and section.

**Browse and search the Ledger online:** https://olumide-akindipe.github.io/verification-gap-ledger/

**View and download preprint:** https://doi.org/10.5281/zenodo.23622181

## Why

Municipal energy programs offer the benefits of energy, cost, and emissions savings. However, these programs differ widely in the proof of results they require and in what they publish. There is no single public record of those differences. The Ledger provides one, allowing municipal officials to evaluate programs based on the evidence they produce, and enabling program auditors and researchers to see where verification is thin.

## What v0.1 contains

| File | Contents |
|---|---|
| `data/processed/vgl_programs.csv` | One row per program with R, C, A codes, confidence, gaps, status |
| `data/processed/vgl_evidence.csv` | One row per evidence item: source, URL, section, access date, note |
| `data/processed/vgl_reference_sources.csv` | Cross-cutting sources (2 CFR 200, OMB Compliance Supplement, NYS Comptroller) |
| `data/processed/qa_report.txt` | Structural checks, distributions, spot checks |
| `paper/stats.json` | Every number the report quotes |
| `paper/figures/fig1_gap_matrix.png` | Programs by required verification and public results |
| `paper/VGL_v0.1_Technical_Report.docx` | Method and first findings |
| `docs/CODEBOOK.md`, `docs/CODING_PROTOCOL.md` | Column definitions, scales, decision rules |
| `docs/LIMITATIONS.md` | What the Ledger cannot tell you |

## The scales

- **R, required verification (0 to 4):** financial only, outputs, estimated outcomes, measured outcomes against a baseline, independent verification.
- **C, results made public (0 to 4):** none, aggregate only, project-level outputs, project-level outcomes, machine-readable open project data.
- **A, attributability (0 to 3):** no baseline, baseline or modeled counterfactual only, measured pre/post, comparison group or impact evaluation.

Full definitions are in `docs/CODEBOOK.md`.

## Rebuild

Requires Python 3.9 or later and matplotlib (`pip install matplotlib python-docx`).

```
python code/01_build.py      # tables, QA report, stats.json
python code/02_figures.py    # Figure 1 (add --final after verification)
node code/03_report.js       # technical report (add --final after verification; needs: npm install docx)
python code/04_site.py       # browse-and-search website, written to site/
python code/05_preprint_stats.py  # preprint numbers not in stats.json (sections 5 and 6), written to paper/stats_preprint.json; needs scipy
python code/06_preprint_assets.py # preprint figures (Power BI style), number macros, data tables and source bibliography, written to paper/preprint/
cd paper/preprint && latexmk -pdf vgl_preprint.tex   # typeset the two-column preprint PDF
```

The coded entries live in `data/interim/coded_batch*.json`. Edit those, never the processed CSVs.

## Sources

Program rules, guidance, reporting templates, evaluation reports, and public data catalogs from DOE, EPA, DOT (FHWA, FTA), HUD, USDA, FEMA, Treasury and IRS, NYSERDA, NYSDEC, NYS EFC, NYPA, GAO, the Congressional Research Service, and the NYS Office of the State Comptroller. Each is listed with URL and access date in `vgl_evidence.csv`. All were accessed in October 2026.

## License

Data and documents: CC BY 4.0 (`LICENSE-DATA`). Code: MIT (`LICENSE`).

## Cite

See `CITATION.cff`. 
Akindipe, S. O. (2026). *Verification Gap Ledger* (Version 0.1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23622181

To cite the Ledger across versions, use the concept DOI: https://doi.org/10.5281/zenodo.23302897

## Versions

0.1 (Oct 2026), 0.5 (Feb 2027), 1.0 (May 2027), 2.0 (Dec 2027). See `docs/NEXT_STEPS.md` and `CHANGELOG.md`.


