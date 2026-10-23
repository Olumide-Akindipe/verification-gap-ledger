"""
04_site.py  Build the public browse-and-search website from the Ledger's own data.

Plain-language note: reads data/processed/*.csv and paper/stats.json and writes a
static website to site/: a searchable program list (index.html), one page per program
(programs/<ID>.html) with every rating and its source evidence, a method page, and the
downloadable data. Run after 01_build.py. Nothing on the site is typed by hand, so the
site always matches the released data.
Run:  python code/04_site.py
"""
import csv
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
PROC = os.path.join(ROOT, "data", "processed")
REPO = "https://github.com/Olumide-Akindipe/verification-gap-ledger"
CONCEPT_DOI = "10.5281/zenodo.23302897"
VERSION_DOI = "10.5281/zenodo.23302898"
ORCID = "0000-0002-1846-9662"

e = lambda s: html.escape(str(s), quote=True)

R_LABELS = ["Financial only", "Outputs", "Estimated outcomes", "Measured outcomes against a baseline", "Independent verification"]
C_LABELS = ["No public results", "Aggregate only", "Project-level outputs", "Project-level outcomes", "Open machine-readable project data"]
A_LABELS = ["No baseline", "Baseline or modeled counterfactual only", "Measured before and after", "Comparison group or impact evaluation"]
DIMS = [
    ("R", "R_required", 4, "Required verification", "What proof of results the program's rules require.", R_LABELS),
    ("C", "C_public", 4, "Public results", "What results anyone can see, not counting award announcements.", C_LABELS),
    ("A", "A_attributable", 3, "Attributability", "Whether an outside party could link outcomes to the funding.", A_LABELS),
]
STATUS_TEXT = {"active": "Active", "active_modified": "Active, modified", "closed": "Closed",
               "terminated_contested": "Terminated, contested in court", "terminated": "Terminated"}


def read(name):
    with open(os.path.join(PROC, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def steps(value, maximum, dim, flag=False):
    v = int(value)
    cells = "".join(f'<i class="{"on" if k < v else "off"}"></i>' for k in range(maximum))
    cls = "steps gap" if flag else "steps"
    return f'<span class="{cls}" role="img" aria-label="{dim} {v} of {maximum}">{cells}</span>'


def page(title, body, depth=0, desc=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or 'Open register of federal and New York State programs funding municipal energy and infrastructure, rated on required verification, public results, and attributability.')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,500;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="mark" href="{up}index.html">Verification Gap Ledger</a>
  <nav aria-label="Site">
    <a href="{up}index.html">Programs</a>
    <a href="{up}method.html">Method</a>
    <a href="{up}method.html#data">Data and citation</a>
    <a href="{REPO}">Source code</a>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <p>Version {e(VER)} &nbsp;|&nbsp; Maintained by Stephen Olumide Akindipe, <a href="https://orcid.org/{ORCID}">ORCID {ORCID}</a> &nbsp;|&nbsp; Data and documents CC BY 4.0, code MIT &nbsp;|&nbsp; <a href="https://doi.org/{CONCEPT_DOI}">doi.org/{CONCEPT_DOI}</a></p>
</footer>
</body>
</html>
"""


def build():
    global VER
    programs = read("vgl_programs.csv")
    evidence = read("vgl_evidence.csv")
    with open(os.path.join(ROOT, "paper", "stats.json"), encoding="utf-8") as f:
        S = json.load(f)
    VER = S["version"]
    n = S["n_programs"]

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "programs"))
    os.makedirs(os.path.join(OUT, "assets"))
    os.makedirs(os.path.join(OUT, "data"))
    for fn in ("vgl_programs.csv", "vgl_evidence.csv", "vgl_reference_sources.csv"):
        shutil.copy(os.path.join(PROC, fn), os.path.join(OUT, "data", fn))
    shutil.copy(os.path.join(ROOT, "assets_site", "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(ROOT, "assets_site", "filter.js"), os.path.join(OUT, "assets", "filter.js"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    agencies = sorted({p["agency"] for p in programs})

    # ---------- index ----------
    rows = []
    for p in sorted(programs, key=lambda x: x["ledger_id"]):
        gap = int(p["gap_rc"]) > 0
        search = " ".join([p["ledger_id"], p["program_name"], p["agency"], p["asset_classes"], p["aln"]]).lower()
        rows.append(f"""<tr data-level="{e(p['level'])}" data-agency="{e(p['agency'])}" data-status="{e(p['status'])}" data-r="{p['R_required']}" data-c="{p['C_public']}" data-a="{p['A_attributable']}" data-gap="{'1' if gap else '0'}" data-search="{e(search)}">
  <td class="name"><a href="programs/{e(p['ledger_id'])}.html">{e(p['program_name'])}</a><span class="sub">{e(p['agency'])}{(' | ALN ' + e(p['aln'])) if p['aln'] else ''}</span></td>
  <td class="lvl">{'Federal' if p['level'] == 'federal' else 'New York State'}</td>
  <td class="score"><span class="num">{p['R_required']}</span>{steps(p['R_required'], 4, 'Required verification', gap)}</td>
  <td class="score"><span class="num">{p['C_public']}</span>{steps(p['C_public'], 4, 'Public results')}</td>
  <td class="score"><span class="num">{p['A_attributable']}</span>{steps(p['A_attributable'], 3, 'Attributability')}</td>
  <td class="st">{e(STATUS_TEXT.get(p['status'], p['status']))}</td>
</tr>""")

    agency_opts = "".join(f'<option value="{e(a)}">{e(a)}</option>' for a in agencies)
    index_body = f"""
<section class="intro">
  <h1>What proof do public energy programs ask for, and what do they show?</h1>
  <p class="lede">The Ledger rates {n} federal and New York State programs that fund municipal energy and infrastructure on three questions. Every rating links to the document and section it comes from.</p>
  <dl class="key">
    <div><dt>R</dt><dd><strong>Required verification.</strong> From financial reports only (0) to independent verification (4).</dd></div>
    <div><dt>C</dt><dd><strong>Public results.</strong> From nothing published (0) to open project-level data (4).</dd></div>
    <div><dt>A</dt><dd><strong>Attributability.</strong> From no baseline (0) to a comparison group or impact evaluation (3).</dd></div>
  </dl>
  <p class="finding">In version {e(VER)}, {S['n_R_at_most_outputs']} of {n} programs require no more than output reporting. Of the {S['n_R_measured_or_better']} that require measured or independently verified outcomes, none publish project-level outcome data.</p>
</section>

<section class="browse" aria-labelledby="browse-h">
  <h2 id="browse-h">Programs</h2>
  <form class="filters" role="search" onsubmit="return false">
    <label class="q">Search<input id="q" type="search" placeholder="Program, agency, asset type or ALN" autocomplete="off"></label>
    <label>Level<select id="f-level"><option value="">All</option><option value="federal">Federal</option><option value="state">New York State</option></select></label>
    <label>Agency<select id="f-agency"><option value="">All</option>{agency_opts}</select></label>
    <label>Status<select id="f-status"><option value="">All</option>{''.join(f'<option value="{k}">{v}</option>' for k, v in STATUS_TEXT.items() if any(p['status'] == k for p in programs))}</select></label>
    <label class="check"><input id="f-gap" type="checkbox"> Rules require more than is published</label>
  </form>
  <p class="count" id="count" aria-live="polite">Showing {n} of {n} programs</p>
  <div class="tablewrap">
  <table class="programs" id="programs">
    <thead><tr>
      <th scope="col"><button type="button" data-sort="name">Program</button></th>
      <th scope="col"><button type="button" data-sort="level">Level</button></th>
      <th scope="col" class="score"><button type="button" data-sort="r">R</button></th>
      <th scope="col" class="score"><button type="button" data-sort="c">C</button></th>
      <th scope="col" class="score"><button type="button" data-sort="a">A</button></th>
      <th scope="col">Status</th>
    </tr></thead>
    <tbody>
{''.join(rows)}
    </tbody>
  </table>
  </div>
  <p class="empty" id="empty" hidden>No programs match these filters. Clear the search or set a filter back to All.</p>
  <p class="legend"><span class="steps gap"><i class="on"></i><i class="off"></i></span> An ochre R bar marks a program whose rules require more verification than it publishes.</p>
</section>
<script src="assets/filter.js"></script>
"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Verification Gap Ledger", index_body))

    # ---------- program pages ----------
    by_prog = {}
    titles = {}
    for ev in evidence:
        # Some v0.1 evidence rows abbreviate a repeated source as "Same" or "Same report".
        # Show the full title of that URL instead, without changing the data.
        if not ev["source"].startswith("Same") and ev["url"]:
            titles.setdefault(ev["url"], ev["source"])
    for ev in evidence:
        if ev["source"].startswith("Same") and ev["url"] in titles:
            ev = dict(ev, source=titles[ev["url"]])
        by_prog.setdefault(ev["ledger_id"], []).append(ev)

    for p in programs:
        pid = p["ledger_id"]
        evs = by_prog.get(pid, [])
        gap = int(p["gap_rc"]) > 0
        blocks = []
        for d, col, mx, title, explain, labels in DIMS:
            v = int(p[col])
            items = [x for x in evs if x["dimension"] == d]
            lis = []
            for x in items:
                assigned = x["code"] != "" and int(x["code"]) == v
                lis.append(f"""<li class="{'assigned' if assigned else 'context'}">
  <p class="ev-note">{e(x['note'])}</p>
  <p class="ev-src"><a href="{e(x['url'])}">{e(x['source'])}</a><span>{e(x['locator'])}. Read {e(x['accessed'])}. Supports code {e(x['code'])}. Confidence: {e(x['confidence'])}.</span></p>
</li>""")
            blocks.append(f"""<section class="dim" aria-labelledby="h-{d}">
  <div class="dim-head">
    <h2 id="h-{d}">{title}</h2>
    <p class="dim-score"><span class="big">{v}</span><span class="of">of {mx}</span>{steps(v, mx, title, gap and d == 'R')}</p>
  </div>
  <p class="dim-label">{e(labels[v])}</p>
  <p class="dim-explain">{explain}</p>
  <ol class="evidence">{''.join(lis)}</ol>
</section>""")
        status_evs = [x for x in evs if x["dimension"] == "STATUS"]
        status_html = ""
        if p["status_note"] or status_evs:
            src = "".join(f'<li><a href="{e(x["url"])}">{e(x["source"])}</a></li>' for x in status_evs if x["url"])
            status_html = f"""<section class="status-note"><h2>Program status</h2><p>{e(STATUS_TEXT.get(p['status'], p['status']))}. {e(p['status_note'])}</p>{('<ul>' + src + '</ul>') if src else ''}</section>"""
        facts = [("Ledger ID", pid), ("Level", "Federal" if p["level"] == "federal" else "New York State"),
                 ("Agency", p["agency"]), ("Assistance Listing", p["aln"] or "Not applicable"),
                 ("Authority", p["authority"]), ("Funding vehicle", p["vehicle"]),
                 ("How municipalities take part", p["municipal_role"]), ("Eligible assets", p["asset_classes"]),
                 ("Gap, required minus public", p["gap_rc"]), ("Distance from verified measured outcomes", f'{p["gap_outcome"]} of 4')]
        facts_html = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts)
        body = f"""
<p class="crumb"><a href="../index.html">All programs</a></p>
<article class="record">
  <header class="record-head">
    <h1>{e(p['program_name'])}</h1>
    <p class="record-sub">{e(p['agency'])}. {e(STATUS_TEXT.get(p['status'], p['status']))}.</p>
  </header>
  <div class="record-grid">
    <div class="dims">{''.join(blocks)}{status_html}</div>
    <aside class="facts" aria-label="Program facts"><dl>{facts_html}</dl>
      <p class="cite">Cite this record: Akindipe, S. O. (2026). Verification Gap Ledger (Version {e(VER)}), record {e(pid)} [Data set]. Zenodo. <a href="https://doi.org/{VERSION_DOI}">https://doi.org/{VERSION_DOI}</a></p>
    </aside>
  </div>
</article>
"""
        with open(os.path.join(OUT, "programs", f"{pid}.html"), "w", encoding="utf-8") as f:
            f.write(page(f"{p['program_name']} | Verification Gap Ledger", body, depth=1,
                         desc=f"{p['program_name']}: required verification {p['R_required']} of 4, public results {p['C_public']} of 4, attributability {p['A_attributable']} of 3, with source evidence."))

    # ---------- method ----------
    def scale_table(labels, mx):
        return "".join(f"<tr><th scope='row'>{k}</th><td>{steps(k, mx, 'level')}</td><td>{e(t)}</td></tr>" for k, t in enumerate(labels))
    method_body = f"""
<article class="prose">
  <h1>How the Ledger rates programs</h1>
  <p>Each program receives one rating on each of three scales, taken from the program's statute, regulations, award terms, funding notices, guidance, official data catalogs and evaluations. Every rating cites the document and section it rests on, with the date it was read. The full rules are in the <a href="{REPO}/blob/main/docs/CODING_PROTOCOL.md">coding protocol</a> and every column is defined in the <a href="{REPO}/blob/main/docs/CODEBOOK.md">codebook</a>.</p>

  <h2>Required verification (R)</h2>
  <p>What recipients must report about results. This rates the obligation, not what happens in practice.</p>
  <table class="scale"><tbody>{scale_table(R_LABELS, 4)}</tbody></table>

  <h2>Public results (C)</h2>
  <p>What anyone can see. Award announcements and recipient lists are not results.</p>
  <table class="scale"><tbody>{scale_table(C_LABELS, 4)}</tbody></table>

  <h2>Attributability (A)</h2>
  <p>Whether the required or published data could let an outside party link outcomes to the funding.</p>
  <table class="scale"><tbody>{scale_table(A_LABELS, 3)}</tbody></table>

  <h2>What the Ledger cannot tell you</h2>
  <ul>
    <li>Public results measure publication, not collection. Agencies may hold outcome data they do not release.</li>
    <li>Version {e(VER)} covers {n} programs chosen to span agencies, funding types and assets. It is not a complete or random sample.</li>
    <li>The scales are ordinal. A gap of 2 is not twice a gap of 1.</li>
    <li>The Ledger rates program design, not whether any project saved energy.</li>
  </ul>
  <p>The full list is in <a href="{REPO}/blob/main/docs/LIMITATIONS.md">LIMITATIONS.md</a>.</p>

  <h2 id="data">Data and citation</h2>
  <p>Download the tables for this version:</p>
  <ul>
    <li><a href="data/vgl_programs.csv">vgl_programs.csv</a>: one row per program with all ratings</li>
    <li><a href="data/vgl_evidence.csv">vgl_evidence.csv</a>: one row per piece of evidence, with source links</li>
    <li><a href="data/vgl_reference_sources.csv">vgl_reference_sources.csv</a>: sources that apply across programs</li>
  </ul>
  <p>Cite this version: Akindipe, S. O. (2026). <em>Verification Gap Ledger</em> (Version {e(VER)}) [Data set]. Zenodo. <a href="https://doi.org/{VERSION_DOI}">https://doi.org/{VERSION_DOI}</a></p>
  <p>To cite the Ledger across versions, use the concept DOI: <a href="https://doi.org/{CONCEPT_DOI}">https://doi.org/{CONCEPT_DOI}</a></p>
  <p>Releases follow a published schedule: 0.5 in February 2027, 1.0 in May 2027 and 2.0 in December 2027. Changes between versions are listed in the <a href="{REPO}/blob/main/CHANGELOG.md">changelog</a>.</p>
</article>
"""
    with open(os.path.join(OUT, "method.html"), "w", encoding="utf-8") as f:
        f.write(page("Method | Verification Gap Ledger", method_body))
    print(f"site built: {len(programs)} program pages, index, method -> {OUT}")


if __name__ == "__main__":
    build()
