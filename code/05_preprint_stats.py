"""
05_preprint_stats.py  Every number the preprint quotes that is not already in stats.json.

Plain-language note: reads data/processed/vgl_programs.csv (the released v0.1.0 table)
and writes paper/stats_preprint.json. It covers the preprint's mean codes (5.1), the
Kendall tau-b associations (5.3), Table 3 (federal versus state), Table 4 (confidence),
Table 5 (sensitivity to low confidence codes, 6.1) and the disclosure scenario (6.2).
It changes no data and leaves stats.json, which matches the archived release, untouched.
Run:  python code/05_preprint_stats.py
Requires: scipy (for Kendall's tau-b).
"""
import csv
import json
import os
from collections import Counter

from scipy.stats import kendalltau

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "processed", "vgl_programs.csv")
OUT = os.path.join(ROOT, "paper", "stats_preprint.json")
MAX = {"R": 4, "C": 4, "A": 3}
COL = {"R": "R_required", "C": "C_public", "A": "A_attributable"}


def load():
    with open(SRC, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    progs = []
    for r in rows:
        progs.append({
            "id": r["ledger_id"], "name": r["program_name"], "level": r["level"],
            "R": int(r["R_required"]), "C": int(r["C_public"]), "A": int(r["A_attributable"]),
            "conf": {d: r[f"{COL[d]}"[0] + "_confidence"] for d in "RCA"},
        })
    return progs


def indicators(progs):
    """Headline indicators defined in preprint section 4.5."""
    n = len(progs)
    return {
        "programs": n,
        "R_at_most_1": sum(p["R"] <= 1 for p in progs),
        "R_at_least_3": sum(p["R"] >= 3 for p in progs),
        "C_eq_0": sum(p["C"] == 0 for p in progs),
        "A_at_most_1": sum(p["A"] <= 1 for p in progs),
        "R_ge3_and_C_ge3": sum(p["R"] >= 3 and p["C"] >= 3 for p in progs),
        "positive_gap": sum(p["R"] - p["C"] > 0 for p in progs),
        "zero_gap": sum(p["R"] - p["C"] == 0 for p in progs),
        "negative_gap": sum(p["R"] - p["C"] < 0 for p in progs),
        "mean_R": round(sum(p["R"] for p in progs) / n, 2) if n else None,
        "mean_C": round(sum(p["C"] for p in progs) / n, 2) if n else None,
        "mean_A": round(sum(p["A"] for p in progs) / n, 2) if n else None,
        "mean_outcome_gap": round(sum(4 - max(p["R"], p["C"]) for p in progs) / n, 2) if n else None,
    }


def shift_low(progs, step):
    """Move every low confidence code by `step` levels, kept inside each scale's range."""
    out = []
    for p in progs:
        q = dict(p)
        for d in "RCA":
            if p["conf"][d] == "low":
                q[d] = min(MAX[d], max(0, p[d] + step))
        out.append(q)
    return out


def tau(progs, x, y):
    t, pval = kendalltau([p[x] for p in progs], [p[y] for p in progs], variant="b")
    return {"tau_b": round(float(t), 2), "p": round(float(pval), 4)}


def main():
    progs = load()
    fed = [p for p in progs if p["level"] == "federal"]
    ny = [p for p in progs if p["level"] == "state"]

    # 6.1 sensitivity (Table 5)
    sensitivity = {
        "base": indicators(progs),
        "a_exclude_low_conf_R": indicators([p for p in progs if p["conf"]["R"] != "low"]),
        "b_exclude_any_low_conf": indicators([p for p in progs if "low" not in p["conf"].values()]),
        "c_low_conf_raised_1": indicators(shift_low(progs, +1)),
        "d_low_conf_lowered_1": indicators(shift_low(progs, -1)),
    }
    low_R_state = sum(1 for p in progs if p["conf"]["R"] == "low" and p["level"] == "state")

    # 6.2 disclosure scenario: programs requiring R3 or R4 publish project-level outcomes (C at least 3)
    affected = [p for p in progs if p["R"] >= 3]
    scen = [dict(p, C=max(p["C"], 3)) if p["R"] >= 3 else p for p in progs]

    stats = {
        "source": "data/processed/vgl_programs.csv (Verification Gap Ledger v0.1.0)",
        "section_5_1": {"mean_R": indicators(progs)["mean_R"], "mean_C": indicators(progs)["mean_C"],
                        "mean_A": indicators(progs)["mean_A"]},
        "section_5_2": {k: indicators(progs)[k] for k in ("positive_gap", "zero_gap", "negative_gap", "mean_outcome_gap")},
        "section_5_3_kendall_tau_b": {"R_C": tau(progs, "R", "C"), "R_A": tau(progs, "R", "A"), "C_A": tau(progs, "C", "A"), "n": len(progs)},
        "table_3_by_level": {"federal": indicators(fed), "state": indicators(ny), "all": indicators(progs)},
        "table_4_confidence": {d: dict(Counter(p["conf"][d] for p in progs)) for d in "RCA"},
        "table_5_sensitivity": sensitivity,
        "section_6_1_low_conf_R_state_programs": low_R_state,
        "section_6_2_disclosure_scenario": {
            "rule": "Programs with R at least 3 have C raised to at least 3; nothing else changes.",
            "affected_programs": [p["id"] + " " + p["name"] for p in affected],
            "before": indicators(progs), "after": indicators(scen),
            "A_distribution_unchanged": Counter(p["A"] for p in progs) == Counter(p["A"] for p in scen),
            "affected_with_A2": [p["id"] for p in affected if p["A"] == 2],
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
