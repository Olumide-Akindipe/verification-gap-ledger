# Build Spec: Verification Gap Ledger v0.1

*Plain-language note: this is the one-page plan the whole build follows. You do not need to edit it; you confirm or correct it once. If the project changes shape, this file changes first.*

```
PROJECT:        Verification Gap Ledger (VGL). Archetypes: open dataset (primary),
                annual/versioned report (secondary), technical report per major version.

QUESTION:       For each federal and New York State program that funds municipal
                energy and infrastructure, what verification of results do the rules
                require, what is actually collected and made public, and could an
                outside party attribute outcomes to the funding?

SOURCES:        1. SAM.gov Assistance Listings (program catalog, ALN numbers)
                2. eCFR 2 CFR 200 (Uniform Guidance), esp. 200.301, 200.328, 200.329
                3. Program statutes, NOFOs, program guidance, reporting templates
                   (DOE, EPA, DOT, HUD, USDA, Treasury/IRS for elective pay)
                4. USAspending.gov award records (scale; recipient type)
                5. NYSERDA, NYS DEC, NYS EFC, NYPA, DOS program documents;
                   data.ny.gov and NYS Clean Energy Dashboard (published results)
                6. GAO and Inspector General reports (independent evidence on collection)
                Vintage and access date recorded per document in data/raw/PROVENANCE.txt.
                Note: the build sandbox cannot reach these sites by script; documents are
                read through the web reader and each is logged with URL and access date.

UNIT:           One program (a federal Assistance Listing or a named NYS program).
                Secondary table: one row per piece of evidence (program x dimension x source).

MEASURES:       R  Required verification (what the rules demand), ordinal 0 to 4
                   R0 financial reporting only
                   R1 activity/output reporting (units installed, projects completed)
                   R2 estimated outcomes (modeled or deemed savings, emissions calculators)
                   R3 measured outcomes against a baseline (metered or billed data)
                   R4 independent measurement and verification or third-party evaluation
                C  Actual collection made public, ordinal 0 to 4
                   C0 no public evidence of outcome data collected
                   C1 program-level aggregate totals only
                   C2 project-level outputs public
                   C3 project-level outcomes public
                   C4 machine-readable project-level outcome data, openly licensed
                A  Outcome attributability, ordinal 0 to 3
                   A0 no baseline required or published
                   A1 baseline exists, no counterfactual
                   A2 measured pre/post at project level
                   A3 comparison group, counterfactual design, or formal impact evaluation
                GAP_RC = R minus C (positive = rules require more than is shown publicly)
                GAP_OUTCOME = 4 minus max(R, C) (distance from measured, verified outcomes)
                Every code carries: source URL, section/page, access date, coder note
                (own words, no long quotes), confidence (high/medium/low).

OUTPUTS:        data/processed/vgl_programs.csv          one row per program
                data/processed/vgl_evidence.csv          one row per evidence item
                data/processed/qa_report.txt
                docs/CODEBOOK.md, docs/CODING_PROTOCOL.md, docs/LIMITATIONS.md
                paper/stats.json, paper/figures/fig1_gap_matrix.png
                paper/VGL_v0.1_technical_report.docx
                CITATION.cff, AUTHORS.json, LICENSE, README.md, CHANGELOG.md

VENUES:         1. GitHub repository (public), tagged release v0.1.0
                2. Zenodo: concept DOI for the Ledger + version DOI per release
                3. FAIRsharing: database record pointing to the concept DOI
                4. re3data: deferred (see VERIFY POINTS)
                5. v1.0: data descriptor paper (target chosen at v0.5)

VERIFY POINTS:  - Program universe and inclusion rule
                - Every R, C, A code for every program (author rules on each)
                - Inter-coder agreement sample: author re-codes about 20 percent blind
                - Treatment of programs terminated, frozen, or rescinded since 2025
                - Wording of the README summary and report abstract (author's own voice)

LICENSE:        Data and documents CC BY 4.0. Code MIT.

ASSUMPTIONS:    Proceeding with about 30 programs for v0.1 (about 18 federal, 12 NYS),
                author listed as Independent Researcher, Albany, NY, until answers arrive.
```

## Version roadmap

| Version | Target | Adds |
|---|---|---|
| 0.1 | Nov 2026 | About 30 programs, coding scale, evidence table, method note |
| 0.5 | Feb 2027 | Full federal universe in scope; all major NYS programs; blind second coder on 20 percent sample |
| 1.0 | May 2027 | Stable schema, agreement statistics published, data descriptor paper submitted |
| 2.0 | Dec 2027 | Project-level collection audit for a sample of NY municipalities; optional web lookup |

## Plain-language version

| Spec line | What it means for you |
|---|---|
| Question | The one thing the Ledger answers, program by program. |
| Unit | Every row in the main table is one funding program. |
| R, C, A | Three ratings per program: what proof is required, what proof is published, and whether cause and effect could be shown. |
| Gap | A simple score: how far the published evidence falls short of what the rules ask, and how far both fall short of real measured results. |
| Evidence table | Every rating points to the exact document and section, so anyone can check it. |
| Verify points | The places where your expert judgment decides, not mine. |
| Venues | Where it gets published, in order. |
| License | Anyone can reuse it if they credit you. |
