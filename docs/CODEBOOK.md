# Codebook: Verification Gap Ledger v0.1

*Plain-language note: this file explains every column in the Ledger's tables. Open it when you want to know what a column means or how a rating was decided.*

## Tables

| File | One row is | Rows (v0.1) |
|---|---|---|
| `data/processed/vgl_programs.csv` | one funding program | 24 |
| `data/processed/vgl_evidence.csv` | one piece of evidence behind one rating | 79 |
| `data/processed/vgl_reference_sources.csv` | one cross-cutting source (for example 2 CFR 200) | 4 |

## vgl_programs.csv

| Column | Meaning |
|---|---|
| `ledger_id` | Permanent ID. `VGL-F-###` federal, `VGL-NY-###` New York State. IDs are never reused. |
| `program_name` | Official program name. |
| `level` | `federal` or `state`. |
| `agency` | Administering agency. |
| `aln` | Federal Assistance Listing Number (formerly CFDA). Blank for state programs and tax credits. |
| `authority` | Statute, regulation, or order that creates or governs the program. |
| `vehicle` | Funding mechanism (formula grant, competitive grant, loan, rebate, tax credit). |
| `municipal_role` | How a municipality receives benefit: direct recipient, subrecipient, borrower, participant. |
| `asset_classes` | Infrastructure types the program funds. |
| `status` | `active`, `active_modified`, `closed`, `terminated_contested`, `terminated`. |
| `status_note` | Dated facts behind the status. |
| `R_required` | Required verification, 0 to 4 (scale below). |
| `C_public` | Results made public, 0 to 4 (scale below). |
| `A_attributable` | Outcome attributability, 0 to 3 (scale below). |
| `R_label`, `C_label`, `A_label` | Text labels for the codes. |
| `R_confidence`, `C_confidence`, `A_confidence` | Highest confidence among evidence items supporting the assigned code: `high`, `medium`, `low`. |
| `gap_rc` | `R_required - C_public`. Positive means the rules ask for more proof than is published. Negative means more is published than the rules require. |
| `gap_outcome` | `4 - max(R_required, C_public)`. Distance from independently verified, measured outcomes. 0 is best. |
| `evidence_items` | Count of evidence rows for the program. |
| `open_verify_items` | Evidence rows still awaiting author confirmation. Must be 0 before release. |
| `ledger_version` | Version of the Ledger the row belongs to. |

## The three scales

### R: required verification (what the rules demand of recipients)

| Code | Label | Test |
|---|---|---|
| 0 | Financial only | Only financial reports or eligibility documentation required. |
| 1 | Outputs | Recipients report activities or units delivered (projects completed, buses replaced, lights installed). |
| 2 | Estimated outcomes | Recipients or the agency report outcome quantities that are modeled, deemed, projected, or calculated (estimated kWh, CO2e, benefit cost ratio). |
| 3 | Measured outcomes against a baseline | Outcome data come from meters, bills, or operating records, compared with a pre-project baseline or measured operating performance. |
| 4 | Independent verification | Measurement and verification or impact evaluation performed by a party independent of the recipient (third-party evaluator, IPMVP-based M&V). |

### C: results made public (what anyone can see)

| Code | Label | Test |
|---|---|---|
| 0 | No public results | No public release of program results found. Award announcements and recipient lists do not count as results. |
| 1 | Aggregate only | Results published only as program totals or evaluation summaries. |
| 2 | Project-level outputs | Delivered outputs published per project or per recipient. |
| 3 | Project-level outcomes | Outcome quantities (estimated or measured) published per project. |
| 4 | Machine-readable open project data | Project-level outcome fields available as bulk machine-readable data with open terms. |

### A: outcome attributability (could an outside party link the result to the funding?)

| Code | Label | Test |
|---|---|---|
| 0 | No baseline | No baseline required or published. |
| 1 | Baseline or modeled counterfactual only | A baseline or business-as-usual case exists, but results are not measured against it, or the counterfactual is modeled. |
| 2 | Measured pre/post | Measured outcomes before and after, at project level. |
| 3 | Comparison group or impact evaluation | A comparison group, randomized or quasi-experimental design, or a net-to-gross impact evaluation. |

## vgl_evidence.csv

| Column | Meaning |
|---|---|
| `evidence_id` | `ledger_id` plus `E##`. |
| `dimension` | `R`, `C`, `A`, or `STATUS`. |
| `code` | The code this evidence supports (blank for STATUS). |
| `source` | Document title, author, and date. |
| `url` | Link to the document as accessed. |
| `locator` | Section, page, slide, or field the finding comes from. |
| `accessed` | Date the coder read the source (YYYY-MM-DD). |
| `note` | The finding in the coder's own words. No long quotations. |
| `confidence` | `high` (rule text read directly), `medium` (official secondary description or partial text), `low` (inferred from incomplete official material; must be confirmed). |
| `needs_author_verification` | `True` until the maintainer confirms the item against the source. |
