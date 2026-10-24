# Changelog

## 0.1.1 - 2026-10-24 (DOI 10.5281/zenodo.23622181)

Release adding analysis code and documents. The data tables (vgl_programs.csv, vgl_evidence.csv, vgl_reference_sources.csv) and stats.json are byte-identical to 0.1.0, so every code and count is unchanged.

- Added the two-column preprint (paper/preprint/vgl_preprint.tex and PDF) with nine Power BI style figures, and code/06_preprint_assets.py, which generates every figure, data table, number macro and the program-source bibliography from the released data. No data changes.
- 05_preprint_stats.py now stores p-values to four decimals (R and C: p = 0.2951, reported as 0.30).
- Added code/05_preprint_stats.py and paper/stats_preprint.json: reproduces the preprint's mean codes, Kendall tau-b associations, Tables 3 to 5 (federal and state split, confidence, sensitivity to low confidence codes) and the illustrative disclosure scenario from vgl_programs.csv. No data changes; stats.json unchanged.
- Added a public browse-and-search website (https://olumide-akindipe.github.io/verification-gap-ledger/), generated from the released data by code/04_site.py. No data changes.
- Added Zenodo DOIs to README, CITATION.cff and technical report.

## 0.1.0 - 2026-10-11 (DOI 10.5281/zenodo.23302898)

- First release: 24 programs (15 federal, 9 New York State), 80 evidence items, all confirmed by the maintainer against their sources.
- VGL-NY-006 (Municipal ZEV Rebate) recoded R1 to R2 after review of the October 2025 request for applications, which requires monitoring information documenting or estimating GHG reductions; authority recorded as ECL Article 54, Title 15 and 6 NYCRR Part 492.
- Defined R (0 to 4), C (0 to 4), and A (0 to 3) scales and the coding protocol.
- Figure 1 (required verification versus public results) and v0.1 technical report.
