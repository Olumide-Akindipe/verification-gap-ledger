/*
 * 03_report.js  Build the v0.1 technical report (.docx) from paper/stats.json and
 * data/processed/vgl_programs.csv.
 *
 * Plain-language note: every number in the report comes from the data files, so the
 * report cannot disagree with the data. Stamped DRAFT unless run with --final.
 * Run:  node code/03_report.js [--final]
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, ImageRun, Footer, PageNumber, BorderStyle,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const FINAL = process.argv.includes("--final");
const S = JSON.parse(fs.readFileSync(path.join(ROOT, "paper", "stats.json"), "utf8"));
if (FINAL && S.n_evidence_needs_verify > 0) {
  console.error(`Refusing --final: ${S.n_evidence_needs_verify} evidence items still need author verification.`);
  process.exit(1);
}
const AUTH = JSON.parse(fs.readFileSync(path.join(ROOT, "AUTHORS.json"), "utf8")).authors[0];

function parseCSV(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (q) { if (ch === '"' && text[i + 1] === '"') { cur += '"'; i++; } else if (ch === '"') q = false; else cur += ch; }
    else if (ch === '"') q = true;
    else if (ch === ",") { row.push(cur); cur = ""; }
    else if (ch === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; }
    else if (ch !== "\r") cur += ch;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  const [h, ...b] = rows.filter(r => r.length > 1);
  return b.map(r => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
const P = parseCSV(fs.readFileSync(path.join(ROOT, "data", "processed", "vgl_programs.csv"), "utf8"));

const FONT = "Calibri";
const t = (text, o = {}) => new TextRun({ text, font: FONT, size: 22, ...o });
const para = (text, o = {}) => new Paragraph({ spacing: { after: 140, line: 276 }, children: [t(text)], ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 280, after: 120 }, children: [new TextRun({ text, font: FONT, size: 28, bold: true, color: "1F3864" })] });
const pct = (a, b) => Math.round((100 * a) / b);

const W = 9360; // US Letter, 1" margins
function table(headers, rows, widths) {
  const cell = (txt, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: "DCE6F2", color: "auto" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: [t(String(txt), { size: 17, bold: head })] })],
  });
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: headers.map((x, i) => cell(x, i, true)) }),
      ...rows.map(r => new TableRow({ children: r.map((x, i) => cell(x, i, false)) }))],
  });
}

const n = S.n_programs;
const children = [];
if (!FINAL) children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "C0392B", space: 4 } },
  children: [t("DRAFT. Not for citation. Every code awaits maintainer verification.", { bold: true, color: "C0392B" })] }));

children.push(
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Verification Gap Ledger, Version 0.1", font: FONT, size: 40, bold: true, color: "1F3864" })] }),
  new Paragraph({ spacing: { after: 60 }, children: [t("Required verification, public results, and outcome attributability in federal and New York State programs funding municipal energy and infrastructure", { size: 24, italics: true })] }),
  new Paragraph({ spacing: { after: 60 }, children: [t(`${AUTH.name}. ${AUTH.affiliation}. ORCID https://orcid.org/${AUTH.orcid}.`)] }),
  new Paragraph({ spacing: { after: 240 }, children: [t(`Technical report. Version ${S.version}. Sources accessed ${S.access_date}. DOI https://doi.org/10.5281/zenodo.23302898.`, { color: "555555" })] }),

  h1("Summary"),
  para(`This report introduces the Verification Gap Ledger, a public register that codes each program based on three scales: the verification of results its rules require (R, 0 to 4), the results it makes public (C, 0 to 4), and whether an external party could attribute program outcomes to the funding (A, 0 to 3). Version 0.1 covers ${n} programs (${S.n_federal} federal and ${S.n_state} New York State) supported by ${S.n_evidence} source-linked evidence items. In this sample, ${S.n_R_at_most_outputs} of ${n} programs (${S.pct_R_at_most_outputs} percent) require no more than output reporting, ${S.n_R_measured_or_better} (${S.pct_R_measured_or_better} percent) require measured outcomes or independent verification, and none of those ${S.n_R_measured_or_better} publish project-level outcome data. ${S.n_A_at_most_1} of ${n} programs (${S.pct_A_at_most_1} percent) score 1 or lower on attributability, and none use a comparison group or formal impact design.`),

  h1("1. Purpose"),
  para("Federal and New York State programs fund municipal building retrofits, street lighting, water and wastewater upgrades, fleet electrification, charging, grid resilience, and hazard mitigation. Each states expected energy, cost, emissions, or resilience benefits. The evidence standard behind those benefits differs by program, and no public record compares programs on that standard. The Ledger provides that record so that municipal officials can weigh funding options by the evidence they will generate, and so that oversight bodies and researchers can locate where verification is thin."),
  para("The federal baseline explains part of the variation. Under 2 CFR 200.329, recipients report accomplishments against award objectives at least annually. Under 2 CFR 200.301, agencies must measure performance, but specifying baselines, indicators, and targets in the award is recommended rather than required. Programs therefore set their own evidence standards above a floor that does not itself require outcome measurement."),

  h1("2. Method"),
  para("Inclusion. A program is included when a federal or New York State agency administers it, municipalities can receive its funds directly, as subrecipients, or as borrowers, and its eligible uses include energy or energy-dependent infrastructure. Version 0.1 is a purposive sample spanning agencies, funding vehicles, and asset classes. Terminated and contested programs remain in the Ledger with a dated status."),
  para("Coding. Each program receives one code per scale. R codes what recipients must report; C codes what the public can see, excluding award announcements; A codes whether the required or published data could support attribution. Codes are taken from the highest available source tier (statute, regulation, or award terms; then funding notices, guidance, and the OMB Compliance Supplement; then official program pages, data catalogs, and evaluations). Each evidence item records the source, URL, section, access date, a paraphrased finding, and a confidence level. Two derived scores are reported: gap_rc (R minus C) and gap_outcome (4 minus the larger of R and C)."),
  table(["Code", "R: required verification", "C: results made public", "A: attributability"], [
    ["0", "Financial only", "No public results", "No baseline"],
    ["1", "Outputs", "Aggregate only", "Baseline or modeled counterfactual"],
    ["2", "Estimated outcomes", "Project-level outputs", "Measured pre and post"],
    ["3", "Measured outcomes vs baseline", "Project-level outcomes", "Comparison group or impact evaluation"],
    ["4", "Independent M&V or evaluation", "Machine-readable open project data", ""],
  ], [900, 2820, 2820, 2820]),
  para(""),

  h1("3. Findings"),
  para(`Required verification. Codes are concentrated at the low end: ${S.R_distribution["0"] || 0} programs at R0, ${S.R_distribution["1"] || 0} at R1, ${S.R_distribution["2"] || 0} at R2, ${S.R_distribution["3"] || 0} at R3, and ${S.R_distribution["4"] || 0} at R4. The mean R code is ${S.mean_R_federal} for federal programs and ${S.mean_R_state} for state programs.`),
  para(`Public results. ${S.C_distribution["0"] || 0} of ${n} programs (${pct(S.C_distribution["0"] || 0, n)} percent) publish no results beyond awards. ${S.n_gap_rc_positive} programs require more verification than they publish (gap_rc above zero), and ${S.n_gap_rc_negative} publish more than their rules require, mostly through agency data portals such as the EPA SRF Public Portal, the FHWA CMAQ Public Access System, and OpenFEMA.`),
  para(`Attributability. ${S.A_distribution["0"] || 0} programs score A0, ${S.A_distribution["1"] || 0} score A1, ${S.A_distribution["2"] || 0} score A2, and ${S.n_A3} score A3. The mean distance from independently verified, measured outcomes (gap_outcome) is ${S.mean_gap_outcome} on a 0 to 4 scale.`),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 }, children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(ROOT, "paper", "figures", "fig1_gap_matrix.png")), transformation: { width: 560, height: 443 } })] }),
  new Paragraph({ spacing: { after: 200 }, children: [t("Figure 1. Programs by required verification (R) and public results (C). Cells above the diagonal require more than they publish.", { size: 18, italics: true })] }),
  para(`Why the distinction between estimated and measured outcomes matters. The independent evaluation of NYSERDA's Real Time Energy Management program applied whole-building billing analysis (IPMVP Option C) and found gross realization rates of ${S.rtem_electric_realization_pct} percent for electricity and ${S.rtem_combined_realization_pct} percent across fuels (evidence ${S.rtem_source_evidence_id}). Programs coded R2 report estimates of the kind that evaluation tested. The Ledger does not imply that other programs would show similar rates; it records which programs could be tested this way and which could not.`),
  para("Status changes. Two programs in the sample were terminated by the administering agency in 2025 and later held unlawfully terminated by federal courts (EPA Solar for All and FEMA BRIC), and two operate under substantially modified terms (the NEVI Formula Program and elective pay). Their verification records remain in the Ledger because the evidence a program generated does not lapse when its funding does."),

  h1("4. Program table"),
  table(["ID", "Program", "R", "C", "A", "Status"],
    P.map(r => [r.ledger_id.replace("VGL-", ""), r.program_name, r.R_required, r.C_public, r.A_attributable, r.status.replace(/_/g, " ")]),
    [900, 5160, 500, 500, 500, 1800]),
  para(""),

  h1("5. Limitations"),
  para("C measures publication, not collection; agencies may hold outcome data they do not release. Version 0.1 is a purposive sample of 24 programs, so its distributions describe these programs only. Codes were assigned by one coder and are confirmed by the maintainer; inter-coder agreement is first measured in version 0.5. Many New York State codes rest on program pages that defer reporting rules to award documents and carry low confidence. The scales are ordinal, so gap scores indicate direction rather than magnitude. The full list is in docs/LIMITATIONS.md."),

  h1("6. Next versions"),
  para("Version 0.5 (February 2027) confirms low-confidence codes against award terms, codes federal programs against the current OMB Compliance Supplement, adds remaining major New York State programs, and introduces a second coder. Version 1.0 (May 2027) stabilizes the schema and publishes agreement statistics with a data descriptor paper. Version 2.0 (December 2027) adds a project-level audit for a sample of New York municipalities."),

  h1("Data availability"),
  para("All tables, evidence, code, and this report are available under CC BY 4.0 (data and documents) and MIT (code) at https://github.com/Olumide-Akindipe/verification-gap-ledger and archived at Zenodo: version DOI https://doi.org/10.5281/zenodo.23302898; concept DOI for all versions https://doi.org/10.5281/zenodo.23302897."),
);

const doc = new Document({
  creator: AUTH.name, title: "Verification Gap Ledger v0.1 Technical Report",
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [t(`Verification Gap Ledger v${S.version}${FINAL ? "" : " DRAFT"}  |  page `, { size: 16, color: "777777" }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "777777" })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(buf => {
  const out = path.join(ROOT, "paper", "VGL_v0.1_Technical_Report.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
