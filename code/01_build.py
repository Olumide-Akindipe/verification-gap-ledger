"""
01_build.py  Build the Verification Gap Ledger tables from the hand-coded entries.

Plain-language note: this script reads the coded program files in data/interim/,
checks them, and writes the public tables in data/processed/, a quality report,
and paper/stats.json (every number the report quotes). You do not need to open it.
Run:  python code/01_build.py
"""
import csv
import json
import glob
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERIM = os.path.join(ROOT, "data", "interim")
OUT = os.path.join(ROOT, "data", "processed")
PAPER = os.path.join(ROOT, "paper")
VERSION = "0.1.0"

R_LABELS = {0: "financial only", 1: "outputs", 2: "estimated outcomes",
            3: "measured outcomes vs baseline", 4: "independent M&V or evaluation"}
C_LABELS = {0: "no public results", 1: "aggregate only", 2: "project-level outputs",
            3: "project-level outcomes", 4: "machine-readable open project-level data"}
A_LABELS = {0: "no baseline", 1: "baseline or modeled counterfactual only",
            2: "measured pre/post", 3: "comparison group or impact evaluation"}
RANGES = {"R": (0, 4), "C": (0, 4), "A": (0, 3)}
STATUSES = {"active", "active_modified", "closed", "terminated_contested", "terminated"}
CONF = {"high", "medium", "low"}


def load():
    programs, refs = [], []
    for path in sorted(glob.glob(os.path.join(INTERIM, "coded_batch*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        refs.extend(d.get("reference_sources", []))
        for p in d["programs"]:
            p["_file"] = os.path.basename(path)
            programs.append(p)
    return programs, refs


def check(programs):
    problems = []
    ids = Counter(p["ledger_id"] for p in programs)
    for i, n in ids.items():
        if n > 1:
            problems.append(f"duplicate ledger_id {i}")
    for p in programs:
        pid = p["ledger_id"]
        if p["status"] not in STATUSES:
            problems.append(f"{pid}: unknown status {p['status']}")
        for dim, (lo, hi) in RANGES.items():
            v = p[dim]
            if not isinstance(v, int) or not lo <= v <= hi:
                problems.append(f"{pid}: {dim}={v} out of range")
            ev = [e for e in p["evidence"] if e["dim"] == dim]
            if not ev:
                problems.append(f"{pid}: no evidence for {dim}")
            elif not any(e["code"] == v for e in ev):
                problems.append(f"{pid}: {dim}={v} not supported by any evidence item with that code")
        for e in p["evidence"]:
            if e["confidence"] not in CONF:
                problems.append(f"{pid}: bad confidence {e['confidence']}")
            if e["dim"] != "STATUS" and not e["url"].startswith("http"):
                problems.append(f"{pid}: evidence for {e['dim']} lacks a URL")
    return problems


def confidence_of(p, dim):
    order = {"low": 0, "medium": 1, "high": 2}
    ev = [e for e in p["evidence"] if e["dim"] == dim and e["code"] == p[dim]]
    return max(ev, key=lambda e: order[e["confidence"]])["confidence"]


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PAPER, exist_ok=True)
    programs, refs = load()
    problems = check(programs)

    prog_rows, ev_rows = [], []
    for p in programs:
        verify_open = sum(1 for e in p["evidence"] if e.get("needs_verify"))
        row = {
            "ledger_id": p["ledger_id"], "program_name": p["program_name"], "level": p["level"],
            "agency": p["agency"], "aln": p["aln"], "authority": p["authority"],
            "vehicle": p["vehicle"], "municipal_role": p["municipal_role"],
            "asset_classes": p["asset_classes"], "status": p["status"], "status_note": p["status_note"],
            "R_required": p["R"], "R_label": R_LABELS[p["R"]], "R_confidence": confidence_of(p, "R"),
            "C_public": p["C"], "C_label": C_LABELS[p["C"]], "C_confidence": confidence_of(p, "C"),
            "A_attributable": p["A"], "A_label": A_LABELS[p["A"]], "A_confidence": confidence_of(p, "A"),
            "gap_rc": p["R"] - p["C"],
            "gap_outcome": 4 - max(p["R"], p["C"]),
            "evidence_items": len(p["evidence"]),
            "open_verify_items": verify_open,
            "ledger_version": VERSION,
        }
        prog_rows.append(row)
        for k, e in enumerate(p["evidence"], 1):
            ev_rows.append({
                "evidence_id": f"{p['ledger_id']}-E{k:02d}", "ledger_id": p["ledger_id"],
                "dimension": e["dim"], "code": "" if e["code"] is None else e["code"],
                "source": e["source"], "url": e["url"], "locator": e["locator"],
                "accessed": e["accessed"], "note": e["note"], "confidence": e["confidence"],
                "needs_author_verification": bool(e.get("needs_verify")),
            })

    prog_rows.sort(key=lambda r: r["ledger_id"])
    for name, rows in (("vgl_programs.csv", prog_rows), ("vgl_evidence.csv", ev_rows)):
        with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    with open(os.path.join(OUT, "vgl_reference_sources.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ref_id", "title", "url", "accessed", "note"])
        w.writeheader()
        w.writerows(refs)

    # ---- stats for documents ----
    n = len(prog_rows)
    fed = [r for r in prog_rows if r["level"] == "federal"]
    ny = [r for r in prog_rows if r["level"] == "state"]
    cnt = lambda rows, key: {str(k): v for k, v in sorted(Counter(r[key] for r in rows).items())}
    pct = lambda a, b: round(100 * a / b) if b else 0
    measured_req = [r for r in prog_rows if r["R_required"] >= 3]
    measured_pub = [r for r in prog_rows if r["R_required"] >= 3 and r["C_public"] >= 3]
    low_or_none_attr = [r for r in prog_rows if r["A_attributable"] <= 1]
    rtem = next(e for e in ev_rows if e["ledger_id"] == "VGL-NY-002" and e["dimension"] == "R")
    stats = {
        "version": VERSION,
        "n_programs": n, "n_federal": len(fed), "n_state": len(ny),
        "n_evidence": len(ev_rows),
        "n_evidence_needs_verify": sum(e["needs_author_verification"] for e in ev_rows),
        "n_programs_contested_or_terminated": sum(r["status"].startswith("terminated") for r in prog_rows),
        "n_programs_modified": sum(r["status"] == "active_modified" for r in prog_rows),
        "R_distribution": cnt(prog_rows, "R_required"),
        "C_distribution": cnt(prog_rows, "C_public"),
        "A_distribution": cnt(prog_rows, "A_attributable"),
        "n_R_measured_or_better": len(measured_req),
        "pct_R_measured_or_better": pct(len(measured_req), n),
        "n_R_measured_and_C_outcomes_public": len(measured_pub),
        "n_R_at_most_outputs": sum(r["R_required"] <= 1 for r in prog_rows),
        "pct_R_at_most_outputs": pct(sum(r["R_required"] <= 1 for r in prog_rows), n),
        "n_A_at_most_1": len(low_or_none_attr), "pct_A_at_most_1": pct(len(low_or_none_attr), n),
        "n_A3": sum(r["A_attributable"] == 3 for r in prog_rows),
        "n_gap_rc_positive": sum(r["gap_rc"] > 0 for r in prog_rows),
        "n_gap_rc_negative": sum(r["gap_rc"] < 0 for r in prog_rows),
        "mean_gap_outcome": round(sum(r["gap_outcome"] for r in prog_rows) / n, 2),
        "mean_R_federal": round(sum(r["R_required"] for r in fed) / len(fed), 2),
        "mean_R_state": round(sum(r["R_required"] for r in ny) / len(ny), 2),
        "rtem_electric_realization_pct": 20, "rtem_combined_realization_pct": 24,
        "rtem_source_evidence_id": rtem["evidence_id"],
        "access_date": max(e["accessed"] for e in ev_rows),
    }
    with open(os.path.join(PAPER, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    # ---- QA report ----
    lines = [f"Verification Gap Ledger v{VERSION}  QA report", "=" * 50,
             f"Programs: {n} (federal {len(fed)}, state {len(ny)})",
             f"Evidence items: {len(ev_rows)}; open author-verification items: {stats['n_evidence_needs_verify']}",
             "", "Structural checks:"]
    lines += [f"  PROBLEM: {x}" for x in problems] or ["  all passed (ids unique, codes in range, every code backed by evidence with a URL)"]
    lines += ["", "Distributions:", f"  R {stats['R_distribution']}", f"  C {stats['C_distribution']}",
              f"  A {stats['A_distribution']}", "", "Confidence of the code-bearing evidence:"]
    for dim in ("R", "C", "A"):
        lines.append(f"  {dim}: {dict(Counter(r[dim + '_confidence'] for r in prog_rows))}")
    lines += ["", "Spot checks for the author (verify against the source by hand):"]
    for pid in ("VGL-NY-002", "VGL-F-007", "VGL-F-012", "VGL-F-014", "VGL-NY-001"):
        r = next(x for x in prog_rows if x["ledger_id"] == pid)
        lines.append(f"  {pid} {r['program_name']}: R{r['R_required']} C{r['C_public']} A{r['A_attributable']}")
    lines += ["", "Programs ordered by open verification items:"]
    for r in sorted(prog_rows, key=lambda x: -x["open_verify_items"]):
        lines.append(f"  {r['ledger_id']:11s} {r['open_verify_items']} open  {r['program_name']}")
    with open(os.path.join(OUT, "qa_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))
    if problems:
        raise SystemExit(f"{len(problems)} structural problems; see qa_report.txt")


if __name__ == "__main__":
    main()
