"""
02_figures.py  Figure 1: where programs sit on required verification (R) versus
public collection (C).

Plain-language note: draws the one chart in the v0.1 report. Each square counts how
many programs share that pair of ratings. Squares above the dashed line are programs
whose rules ask for more proof than is published. Stamped DRAFT unless run with --final.
Run:  python code/02_figures.py [--final]
"""
import csv
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL = "--final" in sys.argv
OUTDIR = os.path.join(ROOT, "paper", "figures")
os.makedirs(OUTDIR, exist_ok=True)

INK, INK2, GRID, SURFACE = "#1f1f1e", "#5f5e5a", "#d9d8d4", "#ffffff"
RAMP = ["#f4f3f0", "#b7d3f6", "#6da7ec", "#2a78d6", "#1c5cab", "#104281"]  # 0,1,2,3,4,5+

R_TXT = ["R0 financial\nonly", "R1 outputs", "R2 estimated\noutcomes", "R3 measured vs\nbaseline", "R4 independent\nM&V"]
C_TXT = ["C0 none\npublic", "C1 aggregate\nonly", "C2 project\noutputs", "C3 project\noutcomes", "C4 open\nmicrodata"]

with open(os.path.join(ROOT, "data", "processed", "vgl_programs.csv"), encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

cells = defaultdict(list)
for r in rows:
    cells[(int(r["R_required"]), int(r["C_public"]))].append(r["ledger_id"].replace("VGL-", ""))

fig, ax = plt.subplots(figsize=(8.6, 6.8), dpi=200)
fig.patch.set_facecolor(SURFACE)
cmap = ListedColormap(RAMP)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 99], cmap.N)
grid = [[len(cells[(rr, cc)]) for cc in range(5)] for rr in range(5)]
ax.imshow(grid, origin="lower", cmap=cmap, norm=norm, extent=(-0.5, 4.5, -0.5, 4.5))

# 2px surface gaps between cells
for k in range(6):
    ax.axhline(k - 0.5, color=SURFACE, lw=2.5)
    ax.axvline(k - 0.5, color=SURFACE, lw=2.5)

for (rr, cc), ids in list(cells.items()):
    n = len(ids)
    if n == 0:
        continue
    dark = n >= 3
    ax.text(cc, rr + 0.18, str(n), ha="center", va="center", fontsize=15, fontweight="bold",
            color="#ffffff" if dark else INK)
    label = "\n".join([", ".join(ids[i:i + 2]) for i in range(0, len(ids), 2)])
    ax.text(cc, rr - 0.2, label, ha="center", va="center", fontsize=5.6,
            color="#ffffff" if dark else INK2, linespacing=1.1)

ax.plot([-0.5, 4.5], [-0.5, 4.5], ls=(0, (4, 3)), color=INK2, lw=1)
ax.text(0, 4, "Rules require\nmore than is\npublished", fontsize=7.5, color=INK2, ha="center", va="center", style="italic")
ax.text(4, 0, "Published\nbeyond what\nrules require", fontsize=7.5, color=INK2, ha="center", va="center", style="italic")

ax.set_xticks(range(5), C_TXT, fontsize=7.5, color=INK2)
ax.set_yticks(range(5), R_TXT, fontsize=7.5, color=INK2)
ax.set_xlabel("C: what results are made public", fontsize=9.5, color=INK, labelpad=8)
ax.set_ylabel("R: what verification the rules require", fontsize=9.5, color=INK, labelpad=8)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)

n_fed = sum(r["level"] == "federal" for r in rows)
fig.suptitle(f"Required verification versus public results, {len(rows)} programs",
             x=0.06, ha="left", fontsize=12.5, color=INK, fontweight="bold")
fig.text(0.06, 0.915, f"{n_fed} federal and {len(rows) - n_fed} New York State programs funding municipal energy and infrastructure. "
         "Number = programs in cell; IDs below.", fontsize=7.8, color=INK2)
fig.text(0.06, 0.02, "Source: Verification Gap Ledger v0.1, coded from program rules, guidance and public data accessed Oct. 2026. "
         "See data/processed/vgl_evidence.csv.", fontsize=6.5, color=INK2)
if not FINAL:
    fig.text(0.5, 0.5, "DRAFT", fontsize=90, color="#c0392b", alpha=0.12, ha="center", va="center", rotation=30)
fig.subplots_adjust(left=0.2, right=0.97, top=0.88, bottom=0.15)
out = os.path.join(OUTDIR, "fig1_gap_matrix.png")
fig.savefig(out, facecolor=SURFACE)
print("wrote", out)
