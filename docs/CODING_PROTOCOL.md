# Coding Protocol: Verification Gap Ledger

*Plain-language note: these are the rules for deciding each rating. Anyone who follows them on the same sources should reach the same codes. If you disagree with a code, this is the file to argue with.*

## 1. Inclusion rule

A program is in scope when all three hold:

1. It is administered by a federal agency or a New York State agency or authority.
2. Municipalities (cities, towns, villages, counties, school districts, municipal utilities, or local public authorities) can receive its funds or benefits directly, as subrecipients, or as borrowers.
3. Eligible uses include energy, energy-dependent infrastructure, or infrastructure resilience (buildings, street lighting, water and wastewater, fleets and charging, grid, mitigation of hazards to public facilities).

Programs remain in the Ledger after termination. Their status changes; their record does not disappear.

## 2. Unit and parent programs

One row per program as the funder defines it. Where a portfolio contains named programs (for example the NYSERDA Clean Energy Fund), the named programs are coded, not the portfolio, to avoid double counting.

## 3. Source hierarchy

Code from the highest available tier and record the tier through the `confidence` field.

1. Statute, regulation, or award terms and conditions.
2. Funding notice, program guidance, reporting templates, or OMB Compliance Supplement Part 4.
3. Official program pages, agency data catalogs, evaluation reports.
4. Independent oversight (GAO, Inspectors General, NYS Comptroller) and reputable secondary sources, used for status and context, and for C only when they describe what is published.

## 4. Decision rules

- **R is about obligation, not practice.** Code what recipients must report. If only the application stage requires an estimate (for example a benefit cost ratio), code R2 and say so in the note.
- **C is about publication, not collection.** Code what any member of the public can see. Awards, selections and recipient lists are not results.
- **A is about design.** Code whether the required or published data could support attribution, independent of whether anyone has done the analysis.
- **When sources conflict**, the higher tier governs; record both.
- **When evidence is missing**, assign the lowest code the available evidence supports, mark confidence `low`, and set `needs_author_verification`.
- **Notes are paraphrase.** Quote no more than a short phrase where exact wording matters.

## 5. Versioning

Codes change only through a new Ledger version. `CHANGELOG.md` lists every code change with its reason. Ledger IDs are permanent.

## 6. Reliability

From v0.5, a second coder independently codes a random 20 percent sample of programs without seeing the first codes. Agreement is reported as percent agreement and weighted kappa for each dimension. v0.1 is single-coder with maintainer verification of every item.
