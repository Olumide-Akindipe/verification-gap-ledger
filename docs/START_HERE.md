# Start Here: The Verification Gap Ledger

*Read this first. It explains your project in plain language. Words in bold are explained in [GLOSSARY.md](GLOSSARY.md).*

## What you are building

A free public table that lists the government programs that pay for city and town energy projects, and shows, for each one, what proof of results the program asks for, what proof actually gets collected and published, and whether anyone could tell if the money caused the result.

## Why it matters

Federal and New York State programs send billions of dollars to municipalities for things like LED streetlights, efficient boilers, solar on town halls, and upgrades to water plants. Each program says it will save energy, cut costs, or reduce emissions. But the rules for proving those results differ widely. Some programs ask only for receipts. Some ask for estimated savings. Very few ask for metered results compared against a baseline.

The gap between what was promised and what can be shown is the "verification gap." Right now nobody keeps one place that records it, program by program. A municipal official choosing between programs, a state auditor, or a researcher has to read dozens of rulebooks to find out. This project does that reading once, records every finding with its source, and publishes it so anyone can reuse it.

Think of it like a nutrition label, but for the evidence behind a public program.

## Where the information comes from

All sources are free and public. Nothing here needs special permission.

| Source | In plain terms | What one entry looks like | Link |
|---|---|---|---|
| Federal Assistance Listings (SAM.gov) | The government's official catalog of every federal grant and loan program | One program: number, agency, purpose, reporting rules | https://sam.gov/content/assistance-listings |
| Uniform Guidance, 2 CFR 200 (eCFR) | The baseline federal rulebook for how grant recipients report performance | One rule section, such as performance reporting | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 |
| Program funding notices and guidance | Each program's own rulebook: what it pays for and what recipients must report | One notice: eligible uses, reporting and evaluation requirements | Agency websites (DOE, EPA, DOT, HUD) |
| USAspending.gov | Federal spending records, including who received money | One award: recipient, amount, dates, description | https://www.usaspending.gov |
| NYSERDA and NYS agency program pages and open data | New York's own energy and infrastructure programs and their published results | One program or one reported project | https://www.nyserda.ny.gov and https://data.ny.gov |
| GAO and Inspector General reports | Independent audits of how programs track results | One finding about a program's reporting | https://www.gao.gov and https://www.oversight.gov |

## What you will have at the end

- [ ] **A public project page** on GitHub where anyone can see and reuse the Ledger: https://github.com/Olumide-Akindipe/verification-gap-ledger
- [ ] **A permanent citation number (DOI)** from Zenodo, one for the Ledger overall and one for each version: 10.5281/zenodo.23302897 (all versions), 10.5281/zenodo.23302898 (v0.1.0)
- [ ] **The Ledger itself**: a spreadsheet (CSV) with one row per program, every rating linked to the exact source page
- [ ] **A codebook and method note** explaining how every rating was decided, so others can check or challenge it
- [ ] **A short technical report** summarizing what version 0.1 found
- [ ] **A FAIRsharing record** listing the Ledger as a public database (see the note on re3data below)

## How it connects to your work

Your proposed endeavor is a decision-support system that helps small and mid-sized municipalities choose, carry out, and evaluate energy and infrastructure investments. The Ledger is the evidence layer underneath that system: it shows which funding programs can actually prove results, which is exactly what a municipality needs to know before it picks one, and it extends the evaluation logic of your TE3 Engine from single projects to the funding programs themselves.

## What you need to do

| Your task | When | Time |
|---|---|---|
| Create accounts (ORCID, GitHub, Zenodo) | Now | 15 min |
| Answer five setup questions | Done |  |
| Check the ratings using the checklist | When the draft is ready | 2 to 3 hours |
| Approve publishing | After checking | 5 min |
| Create the FAIRsharing record using the guide | After the DOI exists | 20 min |

Everything else is built for you.

## The steps ahead

1. **Program list collected.** We assemble the list of programs and save every source document's location and date.
2. **Rules read and coded.** For each program, we record what proof the rules require, with the exact section.
3. **Collection and attribution coded.** We record what results are actually published and whether the design could show cause and effect.
4. **Quality checks.** A second, independent pass re-codes a sample, and we report how often the two passes agree.
5. **First figure and draft report.** You see the gap across all programs in one chart.
6. **Ready for your check.** You verify, then we publish version 0.1.

*You are here: verified and approved 2026-10-11. Published on GitHub and Zenodo 2026-10-11. FAIRsharing is next.*
