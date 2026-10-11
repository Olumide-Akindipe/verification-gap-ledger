*Completed. The maintainer confirmed every item against its source and approved publication on 2026-10-11. Part 4 decisions: all recommended options kept. Retained as the record of the v0.1 verification.*

# Your Verification Checklist: Ledger v0.1

*Before anything goes public under your name, you check it. Total time: about 2 to 3 hours, in two sittings if you like. Tick each box and add the date. Nothing is published until every box is ticked.*

**The big picture.** There are 57 evidence items marked "needs author verification" in `data/processed/vgl_evidence.csv` (column `needs_author_verification` = True). Parts 3 and 4 walk you through them. When you confirm or correct one, tell Claude and it updates the coded file, flips the flag, and rebuilds. The publish gate will not pass while any flag or `[VERIFY]` tag remains.

## Part 1: Make sure the results can be rebuilt (15 min)

Pick one:
- [ ] **Option A, run it yourself.** In a terminal in the project folder:
  ```
  pip install matplotlib python-docx
  npm install docx
  python code/01_build.py
  python code/02_figures.py
  node code/03_report.js
  ```
  The first command should print `Programs: 24 (federal 15, state 9)` and `Evidence items: 79` and `all passed`.
- [ ] **Option B, ask Claude.** In a new chat, upload the project folder and say: "Re-run this pipeline from scratch and give me the headline numbers." They should be: 24 programs, 79 evidence items, 12 programs at R1 or lower, 5 at R3 or higher, 0 at A3.

## Part 2: Check the sources load (15 min)

- [ ] Open `data/processed/vgl_evidence.csv` in Excel or Google Sheets. Click any 10 links in the `url` column. Each should still load.
- [ ] One link is not an official source: VGL-F-014 cites the 2021 OMB Compliance Supplement through a copy hosted by the North Carolina Treasurer. Find the current edition of the Compliance Supplement, Part 4, ALN 10.760, Section L, and confirm performance reporting is still "not applicable." ___

## Part 3: Check rows by hand (60 to 90 min)

For each: open `data/processed/vgl_programs.csv`, find the row, read the code, open the link, and confirm the finding in the `note` column of `vgl_evidence.csv`.

**Five you know from your own work**
- [ ] **VGL-NY-001 Clean Energy Communities: R4 C2 A1.** Open the [CEC impact evaluation summary](https://www.nyserda.ny.gov/-/media/Project/Nyserda/Files/Publications/PPSER/Program-Evaluation/Clean-Energy-CommunitiesImpactEvaluation-ExecutiveSummary-March-2026.pdf). Confirm it was done by Opinion Dynamics and reports verified gross savings with no comparison group. ___
- [ ] **VGL-NY-008 Smart Street Lighting NY: R2 C2 A0.** Open the [NYPA Amsterdam release](https://www.nypa.gov/News/Press-Releases/2024/20241105-led). Confirm savings are stated as expected, not measured. From your Albany contacts, do you know whether NYPA verifies post-installation consumption? If yes, R may rise. ___
- [ ] **VGL-F-001 EECBG: R2 C0 A0.** Open the [EECBG BIL Reporting Guidance](https://www.energy.gov/sites/default/files/2023-08/EECBG-BIL-Reporting-Guidance.pdf), Section 4.3c and Attachment 2. Confirm metrics include energy savings and no metered baseline is required. ___
- [ ] **VGL-F-003 Clean Water SRF: R1 C2 A0.** Open the [EPA SRF Public Portal](https://sdwis.epa.gov/ords/sfdw_pub/r/sfdw/owsrf_public/reports). Confirm you can download a project-level report for New York from 2021 or later. ___
- [ ] **VGL-F-007 NEVI: R3 C1 A1.** Read [23 CFR 680.112](https://www.ecfr.gov/current/title-23/chapter-I/subchapter-G/part-680/section-680.112). Confirm the quarterly kWh, session and uptime requirement. Then search for any published national or New York aggregate of that data. If none exists, change C to 0. ___

**Five extreme values**
- [ ] **VGL-NY-002 Real Time Energy Management: R4.** Open the [DNV evaluation](https://www.nyserda.ny.gov/-/media/Migrated/Files/Publications/PPSER/Program-Evaluation/NYSERDA-2017-Q12020-Real-Time-Energy-Management-Impact-Final-Report.pdf). Find the 20 percent electric and 24 percent combined realization rates. These numbers appear in the report summary, so they must be exact. ___
- [ ] **VGL-F-012 BRIC: C4.** Open the [OpenFEMA dataset page](https://www.fema.gov/openfema-data-page/hazard-mitigation-assistance-projects-v4). Confirm the `benefitCostRatio` field and CSV download exist. ___
- [ ] **VGL-F-009 Elective Pay: R0.** Confirm on the [IRS page](https://www.irs.gov/credits-deductions/elective-pay-and-transferability) that claims are substantiated by eligibility and cost, not performance. ___
- [ ] **VGL-F-014 USDA Water and Waste: R0.** Covered in Part 2. ___
- [ ] **VGL-F-002 Grid Resilience 40101(d): R3, A2.** Open the [DOE metrics slides](https://www.energy.gov/sites/default/files/2023-10/Grid%20Resilience%20Formula%20Grant%20Metrics%20Guidance%20Webinar%20Updated%20508%20Presentation%20Slides.pdf), slide 15. Confirm SAIDI and SAIFI are reported before and after. ___

**Five random rows** (chosen by computer, seed 42)
- [ ] VGL-NY-006 Municipal ZEV Rebate: R1 C0 A0. Open the [DEC grants page](https://dec.ny.gov/environmental-protection/climate-change/resources-for-local-governments/grants-for-climate-action) and the current rebate application. Does it require any vehicle usage reporting? ___
- [ ] VGL-F-004 Drinking Water SRF: R1 C2 A0. Same portal as Clean Water SRF. ___
- [ ] VGL-F-001 EECBG (already above).
- [ ] VGL-NY-009 Green Innovation Grant Program: R1 C0 A0. Open the [GIGP page](https://efc.ny.gov/gigp) and the application instructions PDF. Does it require energy or water savings estimates? If yes, R becomes 2. ___
- [ ] VGL-F-009 Elective Pay (already above).

**All remaining low-confidence items.** Filter `vgl_evidence.csv` to `confidence = low`. For each New York program among them, the fastest route is the program's request for applications or terms and conditions. You may also know staff at DEC, EFC, or NYSERDA who can confirm in one email.

## Part 4: Your decisions (15 min)

The build made these choices provisionally. Agree or change each one.

- [ ] **Do program-level evaluations count as R4?** RTEM and CEC are coded R4 because NYSERDA commissions independent evaluations under the Clean Energy Fund order, even though individual participants are not required to perform M&V. Option A (recommended): keep R4, with the note. Option B: code R by participant obligation only, which drops both to R2 and leaves no R4 programs. Your choice: ___
- [ ] **Do award lists count as public results?** Coded as not counting. Keep (recommended), or count them, which raises 6 to 8 programs from C0 to C1. Your choice: ___
- [ ] **School districts as municipalities.** Clean School Bus and Clean Green Schools are included. Keep (recommended, consistent with your decision-support scope), or drop. Your choice: ___
- [ ] **Elective pay in a grants ledger.** Included as a funding route municipalities use. Keep (recommended) or move to a separate tax-credit table in v0.5. Your choice: ___
- [ ] **Status wording for terminated and contested programs.** Solar for All and BRIC are coded `terminated_contested`. Confirm the dates in each `status_note` against the cited sources. ___

## Part 5: Before it goes public (20 min)

- [ ] Rewrite the README summary and the report Summary in your own words. Both are marked `[VERIFY]`.
- [ ] Add your ORCID iD and confirm affiliation in `AUTHORS.json`. Claude will copy them everywhere.
- [ ] Read `docs/LIMITATIONS.md` and agree with it.
- [ ] Claude regenerates the figure and report with `--final`, and `code/publish_gate.py` passes.

**When every box is ticked, reply to Claude in your own words that you have checked the package and approve publishing.**
