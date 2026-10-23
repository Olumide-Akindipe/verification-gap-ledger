"""
06_preprint_assets.py  Figures, number macros and data tables for the preprint.

Plain-language note: reads the released tables (data/processed/*.csv) and the two stats
files (paper/stats.json, paper/stats_preprint.json, from 01_build.py and 05_preprint_stats.py)
and writes everything the LaTeX preprint pulls in to paper/preprint/:
  figures/*.pdf   Power BI style charts
  numbers.tex     every number quoted in the text, as LaTeX macros
  tab_*.tex       every data table
No number in the preprint is typed by hand. Run 01, 05, then this script, then
latexmk -pdf vgl_preprint.tex inside paper/preprint/.
"""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "preprint")
FIG = os.path.join(OUT, "figures")
os.makedirs(FIG, exist_ok=True)

S = json.load(open(os.path.join(ROOT, "paper", "stats.json")))
P = json.load(open(os.path.join(ROOT, "paper", "stats_preprint.json")))
rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "processed", "vgl_programs.csv"), encoding="utf-8")))
ev = list(csv.DictReader(open(os.path.join(ROOT, "data", "processed", "vgl_evidence.csv"), encoding="utf-8")))

# ---------------------------------------------------------------- Power BI look
FONT = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
PBI = ["#118DFF", "#12239E", "#E66C37", "#6B007B", "#E044A7", "#744EC2", "#D9B300", "#D64550"]
INK, INK2, GRID, CARD = "#252423", "#605E5C", "#E1DFDD", "#FFFFFF"
plt.rcParams.update({
    "font.family": FONT, "font.size": 8, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 9.5, "pdf.fonttype": 3,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
})


def pbi_axes(ax, title, ygrid=True, xgrid=False, pad=10):
    ax.set_title(title, loc="left", color=INK, fontweight="semibold", pad=pad)
    ax.tick_params(length=0)
    ax.spines["bottom"].set_color(GRID)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=0.7)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.7)
    ax.set_axisbelow(True)


def legend_top(ax, handles_labels, ncol=None, y=1.0):
    hs, ls = handles_labels
    ax.legend(hs, ls, loc="lower left", bbox_to_anchor=(0, y), ncol=ncol or len(ls), frameon=False,
              handlelength=0.8, handleheight=0.8, handletextpad=0.4, columnspacing=1.2,
              fontsize=7.5, labelcolor=INK2)


def card(fig, rect, value, label, color=PBI[0]):
    ax = fig.add_axes(rect)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.02, 0.04), 0.96, 0.92, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=CARD, ec=GRID, lw=0.8, transform=ax.transAxes))
    ax.add_patch(plt.Rectangle((0.02, 0.04), 0.012, 0.92, color=color, transform=ax.transAxes))
    ax.text(0.5, 0.58, value, ha="center", va="center", fontsize=18, fontweight="semibold", color=INK, transform=ax.transAxes)
    ax.text(0.5, 0.22, label, ha="center", va="center", fontsize=7, color=INK2, transform=ax.transAxes)


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"), facecolor="white")
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=200, facecolor="white")
    plt.close(fig)


def bar_labels(ax, bars, fmt="{:.0f}", inside=False, size=7):
    for b in bars:
        h = b.get_height()
        if h == 0:
            ax.text(b.get_x() + b.get_width() / 2, 0.15, "0", ha="center", va="bottom", fontsize=size, color=INK2)
            continue
        ax.text(b.get_x() + b.get_width() / 2, h + 0.15, fmt.format(h), ha="center", va="bottom", fontsize=size, color=INK)


short = {
    "VGL-F-001": "EECBG", "VGL-F-002": "Grid Resilience 40101(d)", "VGL-F-003": "Clean Water SRF",
    "VGL-F-004": "Drinking Water SRF", "VGL-F-005": "Solar for All", "VGL-F-006": "CMAQ",
    "VGL-F-007": "NEVI Formula", "VGL-F-008": "CFI Discretionary", "VGL-F-009": "Elective Pay (6417)",
    "VGL-F-010": "Low or No Emission", "VGL-F-011": "Clean School Bus", "VGL-F-012": "BRIC",
    "VGL-F-013": "CDBG Entitlement", "VGL-F-014": "USDA Water and Waste", "VGL-F-015": "CPRG Implementation",
    "VGL-NY-001": "Clean Energy Communities", "VGL-NY-002": "Real Time Energy Mgmt", "VGL-NY-003": "Clean Green Schools",
    "VGL-NY-004": "Charge Ready NY 2.0", "VGL-NY-005": "Climate Smart Communities", "VGL-NY-006": "Municipal ZEV Rebate",
    "VGL-NY-007": "Municipal ZEV Infrastructure", "VGL-NY-008": "Smart Street Lighting NY", "VGL-NY-009": "Green Innovation Grant",
}

# ------------------------------------------------- Fig 1: overview dashboard page
fig = plt.figure(figsize=(7.1, 3.6))
n = S["n_programs"]
card(fig, [0.00, 0.72, 0.245, 0.27], f"{n}", f"Programs ({S['n_federal']} federal, {S['n_state']} NY State)", PBI[0])
card(fig, [0.25, 0.72, 0.245, 0.27], f"{S['n_evidence']}", "Source-linked evidence items", PBI[1])
card(fig, [0.50, 0.72, 0.245, 0.27], f"{S['pct_R_at_most_outputs']}%", f"Require outputs or less ({S['n_R_at_most_outputs']} of {n})", PBI[2])
card(fig, [0.75, 0.72, 0.245, 0.27], f"{S['n_R_measured_and_C_outcomes_public']}", "Measure and publish outcomes", PBI[3])
ax = fig.add_axes([0.06, 0.09, 0.92, 0.48])
levels = [0, 1, 2, 3, 4]
w = 0.26
series = [("R  Required verification", S["R_distribution"], PBI[0]),
          ("C  Public results", S["C_distribution"], PBI[1]),
          ("A  Attributability", S["A_distribution"], PBI[2])]
hl = ([], [])
for k, (lab, dist, col) in enumerate(series):
    vals = [dist.get(str(l), 0) for l in levels]
    xs = [l + (k - 1) * w for l in levels]
    if lab.startswith("A"):
        xs, vals = xs[:4], vals[:4]
    b = ax.bar(xs, vals, width=w * 0.92, color=col)
    bar_labels(ax, b)
    hl[0].append(b[0]); hl[1].append(lab)
ax.set_xticks(levels, ["Level 0", "Level 1", "Level 2", "Level 3", "Level 4"])
ax.set_ylabel("Programs")
ax.set_ylim(0, 18.5)
pbi_axes(ax, "Programs by scale level", pad=20)
legend_top(ax, hl, y=1.01)
save(fig, "fig1_overview")

# --------------------------------------------------------- Fig 2: R x C matrix
cells = {}
for r in rows:
    cells.setdefault((int(r["R_required"]), int(r["C_public"])), []).append(r["ledger_id"])
fig, ax = plt.subplots(figsize=(3.45, 3.25))
maxc = max(len(v) for v in cells.values())
import matplotlib.colors as mcolors
cmap = mcolors.LinearSegmentedColormap.from_list("pbi", ["#FFFFFF", "#118DFF"])
for rr in range(5):
    y = 4 - rr
    for cc in range(5):
        k = len(cells.get((rr, cc), []))
        ax.add_patch(plt.Rectangle((cc - 0.5, y - 0.5), 1, 1, fc=cmap(0.15 + 0.85 * k / maxc) if k else "#FAF9F8", ec="white", lw=1.5))
        if k:
            ax.text(cc, y, str(k), ha="center", va="center", fontsize=9, fontweight="semibold", color="white" if k / maxc > 0.55 else INK)
        if rr >= 3 and cc >= 3:
            ax.add_patch(plt.Rectangle((cc - 0.46, y - 0.46), 0.92, 0.92, fill=False, ec=PBI[2], lw=1.2, ls=(0, (2, 1.5))))
    ax.text(5.35, y, str(sum(len(cells.get((rr, cc), [])) for cc in range(5))), ha="center", va="center", fontsize=8, fontweight="semibold", color=INK)
for cc in range(5):
    ax.text(cc, 5.3, str(sum(len(cells.get((rr, cc), [])) for rr in range(5))), ha="center", va="center", fontsize=8, fontweight="semibold", color=INK)
ax.text(5.35, 5.3, str(n), ha="center", va="center", fontsize=8, fontweight="bold", color=INK)
ax.plot([-0.5, 5.7], [4.8, 4.8], color=INK2, lw=0.8)
ax.plot([4.8, 4.8], [-0.5, 5.6], color=INK2, lw=0.8)
ax.set_xlim(-0.5, 5.75); ax.set_ylim(5.65, -0.55)
ax.set_xticks(list(range(5)) + [5.35], ["C0", "C1", "C2", "C3", "C4", "Total"])
ax.set_yticks(list(range(5)) + [5.3], ["R4", "R3", "R2", "R1", "R0", "Total"])
ax.xaxis.tick_top()
for s_ in ax.spines.values():
    s_.set_visible(False)
ax.tick_params(length=0)
ax.set_title("Matrix: R (rows) by C (columns)", loc="left", color=INK, fontweight="semibold", fontsize=9, pad=18)
fig.subplots_adjust(left=0.14, right=0.97, top=0.84, bottom=0.03)
save(fig, "fig2_matrix")

# ------------------------------------------------- Fig 3: gap by program (bar)
gp = sorted(rows, key=lambda r: (int(r["gap_rc"]), r["ledger_id"]))
fig, ax = plt.subplots(figsize=(3.45, 4.6))
ys = range(len(gp))
vals = [int(r["gap_rc"]) for r in gp]
cols = [PBI[2] if v > 0 else (PBI[0] if v < 0 else "#C8C6C4") for v in vals]
b = ax.barh(list(ys), vals, color=cols, height=0.68)
for y, v in zip(ys, vals):
    ax.text(v + (0.08 if v >= 0 else -0.08), y, f"{v:+d}" if v else "0", va="center", ha="left" if v >= 0 else "right", fontsize=6.5, color=INK)
ax.set_yticks(list(ys), [short[r["ledger_id"]] + ("  (NY)" if r["level"] == "state" else "") for r in gp], fontsize=6.4)
ax.axvline(0, color=INK2, lw=0.8)
ax.set_xlim(-3, 3.9)
ax.set_xlabel("Required minus public (R minus C)")
pbi_axes(ax, "Gap by program (R minus C)", ygrid=False, xgrid=True)
fig.subplots_adjust(left=0.43, right=0.97, top=0.93, bottom=0.09)
save(fig, "fig3_gap")

# ------------------------------------------------------ Fig 4: federal vs state
T3 = P["table_3_by_level"]
fig, ax = plt.subplots(figsize=(3.45, 2.5))
mets = [("mean_R", "Mean R"), ("mean_C", "Mean C"), ("mean_A", "Mean A"), ("mean_outcome_gap", "Mean outcome gap")]
w = 0.36
hl = ([], [])
for k, (lv, lab, col) in enumerate([("federal", f"Federal (n = {T3['federal']['programs']})", PBI[0]), ("state", f"New York State (n = {T3['state']['programs']})", PBI[1])]):
    xs = [i + (k - 0.5) * w for i in range(len(mets))]
    vs = [T3[lv][m] for m, _ in mets]
    bb = ax.bar(xs, vs, width=w * 0.92, color=col)
    for x, v in zip(xs, vs):
        ax.text(x, v + 0.04, f"{v:.2f}", ha="center", va="bottom", fontsize=6.5, color=INK)
    hl[0].append(bb[0]); hl[1].append(lab)
ax.set_xticks(range(len(mets)), [l for _, l in mets], fontsize=7)
ax.set_ylim(0, 2.5)
pbi_axes(ax, "Mean codes by level of government", pad=18)
legend_top(ax, hl, y=1.0)
fig.subplots_adjust(left=0.09, right=0.98, top=0.8, bottom=0.11)
save(fig, "fig4_level")

# ------------------------------------------------ Fig 5: confidence 100% stacked
T4 = P["table_4_confidence"]
fig, ax = plt.subplots(figsize=(3.45, 1.9))
dims = [("R", "R  Required verification"), ("C", "C  Public results"), ("A", "A  Attributability")]
lefts = [0, 0, 0]
hl = ([], [])
for lvl, col in [("high", PBI[1]), ("medium", PBI[0]), ("low", PBI[2])]:
    vs = [T4[d].get(lvl, 0) for d, _ in dims]
    bb = ax.barh(range(3), vs, left=lefts, color=col, height=0.6, edgecolor="white", lw=1)
    for i, (v, l) in enumerate(zip(vs, lefts)):
        if v:
            ax.text(l + v / 2, i, str(v), ha="center", va="center", fontsize=7, color="white", fontweight="semibold")
    lefts = [a + b for a, b in zip(lefts, vs)]
    hl[0].append(bb[0]); hl[1].append(lvl.capitalize())
ax.set_yticks(range(3), [l for _, l in dims])
ax.invert_yaxis()
ax.set_xlim(0, n)
ax.set_xlabel("Programs")
pbi_axes(ax, "Evidence confidence by scale", ygrid=False, xgrid=True, pad=18)
legend_top(ax, hl, y=1.0)
fig.subplots_adjust(left=0.37, right=0.97, top=0.74, bottom=0.2)
save(fig, "fig5_confidence")

# ------------------------------------------------------- Fig 6: RTEM realization
rtem_note = next(e["note"] for e in ev if e["evidence_id"] == S["rtem_source_evidence_id"])
import re
rr_vals = {k: int(v) for k, v in re.findall(r"(electric|fossil|combined) (\d+) percent", rtem_note)}
assert rr_vals["electric"] == S["rtem_electric_realization_pct"] and rr_vals["combined"] == S["rtem_combined_realization_pct"]
fig, ax = plt.subplots(figsize=(3.45, 2.3))
labs = ["Electric", "Fossil fuel", "Combined"]
vs = [rr_vals["electric"], rr_vals["fossil"], rr_vals["combined"]]
bb = ax.bar(labs, vs, color=[PBI[0], PBI[1], PBI[2]], width=0.55)
for b_, v in zip(bb, vs):
    ax.text(b_.get_x() + b_.get_width() / 2, v + 2, f"{v}%", ha="center", fontsize=8, fontweight="semibold", color=INK)
ax.axhline(100, color=PBI[7], lw=1.1, ls=(0, (4, 2)))
ax.text(2.33, 103, "Estimated savings = 100%", ha="right", fontsize=6.8, color=PBI[7])
ax.set_ylim(0, 115)
ax.set_ylabel("Gross realization rate (%)")
pbi_axes(ax, "RTEM gross realization rates")
fig.subplots_adjust(left=0.15, right=0.97, top=0.87, bottom=0.11)
save(fig, "fig6_rtem")

# ----------------------------------------------------- Fig 7: Kendall matrix
tau = P["section_5_3_kendall_tau_b"]
fig, ax = plt.subplots(figsize=(3.45, 2.2))
names = ["R", "C", "A"]
mat = {("R", "C"): tau["R_C"], ("R", "A"): tau["R_A"], ("C", "A"): tau["C_A"]}
for i, a in enumerate(names):
    for j, b2 in enumerate(names):
        if i == j:
            val, txt, ptxt = 1.0, "1.00", ""
        else:
            d = mat.get((a, b2)) or mat.get((b2, a))
            val, txt = d["tau_b"], f"{d['tau_b']:.2f}"
            ptxt = "p < 0.001" if d["p"] < 0.001 else f"p = {d['p']:.2f}"
        ax.add_patch(plt.Rectangle((j, 2 - i), 1, 1, fc=cmap(0.1 + 0.9 * val) if i != j else "#F3F2F1", ec="white", lw=2))
        ax.text(j + 0.5, 2 - i + 0.58, txt, ha="center", va="center", fontsize=9, fontweight="semibold", color="white" if (val > 0.55 and i != j) else INK)
        if ptxt:
            ax.text(j + 0.5, 2 - i + 0.28, ptxt, ha="center", va="center", fontsize=6.3, color="white" if val > 0.55 else INK2)
ax.set_xlim(0, 3); ax.set_ylim(0, 3)
ax.set_xticks([0.5, 1.5, 2.5], ["R", "C", "A"]); ax.set_yticks([2.5, 1.5, 0.5], ["R", "C", "A"])
ax.xaxis.tick_top()
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
ax.set_aspect("equal")
ax.set_title(f"Kendall's tau-b between scales (n = {tau['n']})", loc="left", color=INK, fontweight="semibold", fontsize=8.5, pad=16)
fig.subplots_adjust(left=0.05, right=0.95, top=0.82, bottom=0.02)
save(fig, "fig7_tau")

# -------------------------------------------------- Fig 8: sensitivity (shares)
T5 = P["table_5_sensitivity"]
treat = [("base", "Base"), ("a_exclude_low_conf_R", "(a) Excl. low-conf. R"), ("b_exclude_any_low_conf", "(b) Excl. any low-conf."),
         ("c_low_conf_raised_1", "(c) Low-conf. +1"), ("d_low_conf_lowered_1", "(d) Low-conf. -1")]
inds = [("R_at_most_1", "R at most 1"), ("R_at_least_3", "R at least 3"), ("C_eq_0", "C = 0"), ("A_at_most_1", "A at most 1"),
        ("positive_gap", "Positive gap"), ("R_ge3_and_C_ge3", "R and C at least 3")]
fig, ax = plt.subplots(figsize=(7.1, 2.7))
w = 0.16
hl = ([], [])
for k, ((tk, tl), col) in enumerate(zip(treat, [INK2, PBI[0], PBI[1], PBI[2], PBI[3]])):
    xs = [i + (k - 2) * w for i in range(len(inds))]
    sh = [100 * T5[tk][ik] / T5[tk]["programs"] for ik, _ in inds]
    bb = ax.bar(xs, sh, width=w * 0.9, color=col)
    for x, v, (ik, _) in zip(xs, sh, inds):
        ax.text(x, v + 1.5, f"{T5[tk][ik]}", ha="center", fontsize=5.8, color=INK)
    hl[0].append(bb[0]); hl[1].append(f"{tl} (n = {T5[tk]['programs']})")
ax.set_xticks(range(len(inds)), [l for _, l in inds])
ax.set_ylabel("Share of programs in sample (%)")
ax.set_ylim(0, 105)
pbi_axes(ax, "Headline indicators by treatment of low-confidence codes (labels show counts)", pad=30)
legend_top(ax, hl, ncol=3, y=1.0)
fig.subplots_adjust(left=0.07, right=0.99, top=0.78, bottom=0.1)
save(fig, "fig8_sensitivity")

# ----------------------------------------------------- Fig 9: disclosure scenario
SC = P["section_6_2_disclosure_scenario"]
fig = plt.figure(figsize=(3.45, 2.75))
ax = fig.add_axes([0.1, 0.1, 0.88, 0.5])
mets = [("R_ge3_and_C_ge3", "Measure and\npublish outcomes"), ("positive_gap", "Positive\ngap"), ("C_eq_0", "No public\nresults")]
w = 0.36
hl = ([], [])
for k, (key, lab, col) in enumerate([("before", "Current codes", PBI[0]), ("after", "Scenario", PBI[2])]):
    xs = [i + (k - 0.5) * w for i in range(len(mets))]
    vs = [SC[key][m] for m, _ in mets]
    bb = ax.bar(xs, vs, width=w * 0.92, color=col)
    bar_labels(ax, bb, size=7)
    hl[0].append(bb[0]); hl[1].append(lab)
ax.set_xticks(range(len(mets)), [l for _, l in mets], fontsize=7)
ax.set_ylim(0, 16.5)
ax.set_ylabel("Programs")
pbi_axes(ax, "")
legend_top(ax, hl, y=1.0)
card(fig, [0.02, 0.73, 0.47, 0.25], f"{SC['before']['mean_C']:.2f} → {SC['after']['mean_C']:.2f}", "Mean C (public results)", PBI[1])
card(fig, [0.51, 0.73, 0.47, 0.25], f"{SC['before']['mean_outcome_gap']:.2f} → {SC['after']['mean_outcome_gap']:.2f}", "Mean outcome gap (unchanged)", INK2)
save(fig, "fig9_scenario")

# ---------------------------------------------------------------- numbers.tex
def pct(a, b):
    return round(100 * a / b)

M = {
    "nProg": n, "nFed": S["n_federal"], "nNY": S["n_state"], "nEvid": S["n_evidence"],
    "nRzero": S["R_distribution"].get("0", 0), "nRone": S["R_distribution"].get("1", 0), "nRtwo": S["R_distribution"].get("2", 0),
    "nRthree": S["R_distribution"].get("3", 0), "nRfour": S["R_distribution"].get("4", 0),
    "nCzero": S["C_distribution"].get("0", 0), "nCone": S["C_distribution"].get("1", 0), "nCtwo": S["C_distribution"].get("2", 0),
    "nCthree": S["C_distribution"].get("3", 0), "nCfour": S["C_distribution"].get("4", 0),
    "nAzero": S["A_distribution"].get("0", 0), "nAone": S["A_distribution"].get("1", 0), "nAtwo": S["A_distribution"].get("2", 0), "nAthree": S["n_A3"],
    "nRleOne": S["n_R_at_most_outputs"], "pctRleOne": S["pct_R_at_most_outputs"],
    "nRgeThree": S["n_R_measured_or_better"], "pctRgeThree": S["pct_R_measured_or_better"],
    "pctCzero": pct(S["C_distribution"].get("0", 0), n), "pctAzero": pct(S["A_distribution"].get("0", 0), n),
    "nAleOne": S["n_A_at_most_1"], "pctAleOne": S["pct_A_at_most_1"], "nBoth": S["n_R_measured_and_C_outcomes_public"],
    "nGapPos": S["n_gap_rc_positive"], "pctGapPos": pct(S["n_gap_rc_positive"], n), "nGapNeg": S["n_gap_rc_negative"],
    "nGapZero": P["section_5_2"]["zero_gap"],
    "meanR": f"{P['section_5_1']['mean_R']:.2f}", "meanC": f"{P['section_5_1']['mean_C']:.2f}", "meanA": f"{P['section_5_1']['mean_A']:.2f}",
    "meanOG": f"{P['section_5_2']['mean_outcome_gap']:.2f}",
    "tauRC": f"{tau['R_C']['tau_b']:.2f}", "pRC": f"{tau['R_C']['p']:.2f}", "tauRA": f"{tau['R_A']['tau_b']:.2f}",
    "tauCA": f"{tau['C_A']['tau_b']:.2f}", "pCA": f"{tau['C_A']['p']:.2f}",
    "rtemElec": rr_vals["electric"], "rtemFossil": rr_vals["fossil"], "rtemComb": rr_vals["combined"],
    "nLowR": T4["R"].get("low", 0), "nLowC": T4["C"].get("low", 0), "nLowA": T4["A"].get("low", 0),
    "nLowRState": P["section_6_1_low_conf_R_state_programs"],
    "nTermContested": S["n_programs_contested_or_terminated"], "nModified": S["n_programs_modified"],
    "scBothAfter": SC["after"]["R_ge3_and_C_ge3"], "scGapAfter": SC["after"]["positive_gap"], "scCzeroAfter": SC["after"]["C_eq_0"],
    "scMeanCAfter": f"{SC['after']['mean_C']:.2f}", "scAffected": len(SC["affected_programs"]),
    "sensRleOneMin": min(T5[k]["R_at_most_1"] for k in ("base", "c_low_conf_raised_1", "d_low_conf_lowered_1")),
    "sensRleOneMax": max(T5[k]["R_at_most_1"] for k in ("base", "c_low_conf_raised_1", "d_low_conf_lowered_1")),
    "sensAleOneMin": min(T5[k]["A_at_most_1"] for k in ("base", "c_low_conf_raised_1", "d_low_conf_lowered_1")),
    "sensBProg": T5["b_exclude_any_low_conf"]["programs"], "sensBAleOne": T5["b_exclude_any_low_conf"]["A_at_most_1"],
    "accessDate": S["access_date"], "vglVersion": S["version"],
}
with open(os.path.join(OUT, "numbers.tex"), "w") as f:
    f.write("% Generated by code/06_preprint_assets.py from stats.json and stats_preprint.json. Do not edit.\n")
    for k, v in M.items():
        f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")

# ------------------------------------------------------------------ tables
def tex(s):
    return (str(s).replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#"))

STATUS = {"active": "Active", "active_modified": "Active, modified", "closed": "Closed",
          "terminated_contested": "Terminated, contested", "terminated": "Terminated"}
AG = {"U.S. Department of Energy": "DOE", "U.S. Environmental Protection Agency": "EPA",
      "U.S. Department of Transportation, FHWA and FTA": "DOT (FHWA, FTA)", "U.S. Department of Transportation, FHWA": "DOT (FHWA)",
      "U.S. Department of Transportation, FTA": "DOT (FTA)", "U.S. Department of the Treasury, Internal Revenue Service": "Treasury (IRS)",
      "Federal Emergency Management Agency": "FEMA", "U.S. Department of Housing and Urban Development": "HUD",
      "U.S. Department of Agriculture, Rural Development": "USDA (RD)", "NYSERDA": "NYSERDA",
      "NYS Department of Environmental Conservation": "NYSDEC", "New York Power Authority": "NYPA",
      "NYS Environmental Facilities Corporation": "NYS EFC"}

# primary source per program (first listed evidence item supporting the assigned R code);
# programs sharing a source document share one bibliography entry
SRC, SRCKEY = {}, {}
for r in sorted(rows, key=lambda x: x["ledger_id"]):
    e = [x for x in ev if x["ledger_id"] == r["ledger_id"] and x["dimension"] == "R" and x["code"] == r["R_required"]][0]
    SRC[r["ledger_id"]] = e
    SRCKEY[r["ledger_id"]] = next((SRCKEY[k] for k, v in SRC.items() if v["url"] == e["url"] and k in SRCKEY),
                                  "src" + r["ledger_id"].replace("VGL-", "").replace("-", ""))

with open(os.path.join(OUT, "tab_programs.tex"), "w") as f:
    for r in sorted(rows, key=lambda x: x["ledger_id"]):
        f.write(f"{r['ledger_id']} & {tex(r['program_name'])} & {tex(AG.get(r['agency'], r['agency']))} & {tex(r['aln']) or '--'} & {tex(r['vehicle'])} & {tex(STATUS[r['status']])} & \\cite{{{SRCKEY[r['ledger_id']]}}} \\\\\n")

c = lambda d, k: d.get(str(k), 0)
with open(os.path.join(OUT, "tab_dist.tex"), "w") as f:
    for lab, d, mx in (("R, required verification", S["R_distribution"], 4), ("C, public results", S["C_distribution"], 4), ("A, attributability", S["A_distribution"], 3)):
        cellsv = [str(c(d, k)) for k in range(5)]
        if mx == 3:
            cellsv[4] = "--"
        mean = {"R": P["section_5_1"]["mean_R"], "C": P["section_5_1"]["mean_C"], "A": P["section_5_1"]["mean_A"]}[lab[0]]
        f.write(f"{lab} & " + " & ".join(cellsv) + f" & {mean:.2f} \\\\\n")

with open(os.path.join(OUT, "tab_level.tex"), "w") as f:
    spec = [("Mean $R$", "mean_R", "{:.2f}"), ("Mean $C$", "mean_C", "{:.2f}"), ("Mean $A$", "mean_A", "{:.2f}"),
            ("$R \\le 1$ (outputs or less)", "R_at_most_1", "{}"), ("$R \\ge 3$ (measured or verified)", "R_at_least_3", "{}"),
            ("$C = 0$ (no public results)", "C_eq_0", "{}"), ("$A \\le 1$", "A_at_most_1", "{}"),
            ("$R \\ge 3$ and $C \\ge 3$", "R_ge3_and_C_ge3", "{}"), ("Positive gap $G_i > 0$", "positive_gap", "{}"),
            ("Mean outcome gap $\\bar{O}$", "mean_outcome_gap", "{:.2f}")]
    for lab, k, fm in spec:
        f.write(f"{lab} & " + " & ".join(fm.format(T3[l][k]) for l in ("federal", "state", "all")) + " \\\\\n")

with open(os.path.join(OUT, "tab_conf.tex"), "w") as f:
    for d, lab in (("R", "$R$, required verification"), ("C", "$C$, public results"), ("A", "$A$, attributability")):
        f.write(f"{lab} & {T4[d].get('high', 0)} & {T4[d].get('medium', 0)} & {T4[d].get('low', 0)} \\\\\n")

with open(os.path.join(OUT, "tab_tau.tex"), "w") as f:
    for key, lab in (("R_C", "$R$ and $C$"), ("R_A", "$R$ and $A$"), ("C_A", "$C$ and $A$")):
        d = tau[key]
        ptxt = "$<0.001$" if d["p"] < 0.001 else f"{d['p']:.3f}"
        f.write(f"{lab} & {d['tau_b']:.2f} & {ptxt} & {tau['n']} \\\\\n")

with open(os.path.join(OUT, "tab_sens.tex"), "w") as f:
    labels = {"base": "Base (v0.1.0 codes)", "a_exclude_low_conf_R": "(a) Exclude low-confidence $R$",
              "b_exclude_any_low_conf": "(b) Exclude any low-confidence code", "c_low_conf_raised_1": "(c) Low-confidence codes $+1$",
              "d_low_conf_lowered_1": "(d) Low-confidence codes $-1$"}
    for k, lab in labels.items():
        t = T5[k]
        f.write(f"{lab} & {t['programs']} & {t['R_at_most_1']} & {t['R_at_least_3']} & {t['C_eq_0']} & {t['A_at_most_1']} & {t['R_ge3_and_C_ge3']} & {t['positive_gap']} \\\\\n")

with open(os.path.join(OUT, "tab_scen.tex"), "w") as f:
    spec = [("$R \\ge 3$ and $C \\ge 3$", "R_ge3_and_C_ge3", "{}"), ("Positive gap $G_i > 0$", "positive_gap", "{}"),
            ("Zero gap", "zero_gap", "{}"), ("Negative gap", "negative_gap", "{}"), ("$C = 0$", "C_eq_0", "{}"),
            ("Mean $C$", "mean_C", "{:.2f}"), ("$A \\le 1$", "A_at_most_1", "{}"), ("Mean outcome gap $\\bar{O}$", "mean_outcome_gap", "{:.2f}")]
    for lab, k, fm in spec:
        f.write(f"{lab} & {fm.format(SC['before'][k])} & {fm.format(SC['after'][k])} \\\\\n")

conf_ab = {"high": "H", "medium": "M", "low": "L"}
with open(os.path.join(OUT, "tab_appendix.tex"), "w") as f:
    for r in sorted(rows, key=lambda x: x["ledger_id"]):
        cf = "/".join(conf_ab[r[d + "_confidence"]] for d in ("R", "C", "A"))
        f.write(f"{r['ledger_id']} & {tex(r['program_name'])} & {r['R_required']} & {r['C_public']} & {r['A_attributable']} & ${int(r['gap_rc']):+d}$ & {r['gap_outcome']} & {cf} & {r['evidence_items']} \\\\\n".replace("+0", "0"))

# ------------------------------------------- bibliography of primary program sources
# One entry per program: the first listed evidence item supporting its assigned R code.
order = {"high": 0, "medium": 1, "low": 2}
def bibesc(t):
    return t.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#")
with open(os.path.join(OUT, "refs_programs.bib"), "w", encoding="utf-8") as f:
    done = set()
    for pid, e in SRC.items():
        key = SRCKEY[pid]
        if key in done:
            continue
        done.add(key)
        url = e["url"].replace("%", "\\%")
        loc = bibesc(e['locator']); loc = loc[0].upper() + loc[1:]
        yr = re.findall(r"(?:19|20)\d\d", e["source"])
        year = yr[-1] if yr else "n.d"  # style adds the final period
        f.write(f"@misc{{{key},\n  title = {{{{{bibesc(e['source'])}}}}},\n  year = {{{year}}},\n  note = {{\\url{{{url}}}. {loc}. Accessed {e['accessed']}}}\n}}\n\n")

print("assets written to", OUT)
