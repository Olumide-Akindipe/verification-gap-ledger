"""Command line interface: ``vgl``."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import textwrap
from pathlib import Path

from . import __version__
from ._data import (
    CONCEPT_DOI,
    DATA_VERSION,
    DOI,
    SCALES,
    citation,
    data_path,
    evidence,
    program,
    programs,
    stats,
)

_LIST_COLS = ["ledger_id", "level", "R_required", "C_public", "A_attributable", "program_name"]


def _print_table(rows, cols, width=None):
    heads = {"R_required": "R", "C_public": "C", "A_attributable": "A"}
    names = [heads.get(c, c) for c in cols]
    cells = [[("" if r[c] is None else str(r[c])) for c in cols] for r in rows]
    widths = [max([len(n)] + [len(row[i]) for row in cells]) for i, n in enumerate(names)]
    term = width or shutil.get_terminal_size((120, 20)).columns
    used = sum(widths[:-1]) + 2 * (len(widths) - 1)
    widths[-1] = max(10, min(widths[-1], term - used))

    def fmt(vals):
        return "  ".join(v[: widths[i]].ljust(widths[i]) for i, v in enumerate(vals)).rstrip()

    print(fmt(names))
    print(fmt(["-" * w for w in widths]))
    for row in cells:
        print(fmt(row))


def _emit(rows, fmt, cols=None):
    if fmt == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif fmt == "csv":
        fields = cols or (list(rows[0]) if rows else [])
        w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    else:
        _print_table(rows, cols or _LIST_COLS)


def cmd_info(args):
    s = stats()
    print(f"Verification Gap Ledger, package {__version__}, data version {DATA_VERSION}")
    print(f"Programs: {s['n_programs']} ({s['n_federal']} federal, {s['n_state']} New York State)")
    print(f"Evidence items: {s['n_evidence']}")
    print(f"Release DOI: https://doi.org/{DOI}")
    print(f"Concept DOI (all versions): https://doi.org/{CONCEPT_DOI}")
    print("Browse online: https://olumide-akindipe.github.io/verification-gap-ledger/")
    print("\nScales")
    for dim, levels in SCALES.items():
        print(f"  {dim}: " + "; ".join(f"{k} {v}" for k, v in levels.items()))


def cmd_list(args):
    rows = programs(level=args.level)
    for dim, val in (("R_required", args.r), ("C_public", args.c), ("A_attributable", args.a)):
        if val is not None:
            rows = [r for r in rows if r[dim] == val]
    _emit(rows, args.format, None if args.format == "json" else (None if args.format == "csv" else _LIST_COLS))


def cmd_show(args):
    try:
        p = program(args.ledger_id)
    except KeyError as exc:
        sys.exit(str(exc))
    if args.format == "json":
        p["evidence"] = evidence(args.ledger_id)
        print(json.dumps(p, indent=2, ensure_ascii=False))
        return
    print(f"{p['ledger_id']}  {p['program_name']}")
    print(f"{p['agency']} ({p['level']}), status: {p['status']}")
    for dim, key, conf in (("R", "R_required", "R_confidence"), ("C", "C_public", "C_confidence"), ("A", "A_attributable", "A_confidence")):
        print(f"  {dim} = {p[key]}  {SCALES[dim][p[key]]}  (confidence: {p[conf]})")
    print(f"  Gap R minus C = {p['gap_rc']}; outcome gap = {p['gap_outcome']}")
    print("\nEvidence")
    for e in evidence(args.ledger_id):
        print(f"- [{e['dimension']} {'' if e['code'] is None else e['code']}] {e['source']}, {e['locator']}")
        print(f"  {e['url']}")
        if args.notes and e["note"]:
            print(textwrap.indent(textwrap.fill(e["note"], 96), "  "))


def cmd_evidence(args):
    rows = evidence(ledger_id=args.ledger_id, dimension=args.dimension)
    cols = ["evidence_id", "dimension", "code", "source", "locator", "url"]
    _emit(rows, args.format, None if args.format == "json" else cols if args.format == "table" else None)


def cmd_export(args):
    out = Path(args.directory)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("programs", "evidence", "reference_sources", "stats"):
        src = data_path(name)
        shutil.copyfile(src, out / src.name)
        print(f"wrote {out / src.name}")


def cmd_cite(args):
    print(citation("bibtex" if args.bibtex else "apa"))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="vgl",
        description="Query the Verification Gap Ledger: required verification (R), public results (C) "
        "and attributability (A) of federal and New York State municipal energy and infrastructure programs.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} (data {DATA_VERSION})")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("info", help="release, DOIs, counts and scale definitions").set_defaults(func=cmd_info)

    p = sub.add_parser("list", help="list programs with their R, C and A codes")
    p.add_argument("--level", choices=["federal", "state"])
    p.add_argument("--r", type=int, metavar="N", help="only programs with R = N")
    p.add_argument("--c", type=int, metavar="N", help="only programs with C = N")
    p.add_argument("--a", type=int, metavar="N", help="only programs with A = N")
    p.add_argument("--format", choices=["table", "csv", "json"], default="table")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="one program with its codes and evidence")
    p.add_argument("ledger_id", help="for example VGL-NY-006")
    p.add_argument("--notes", action="store_true", help="include the coder's note for each evidence item")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("evidence", help="list evidence items")
    p.add_argument("ledger_id", nargs="?")
    p.add_argument("--dimension", choices=["R", "C", "A", "STATUS"])
    p.add_argument("--format", choices=["table", "csv", "json"], default="table")
    p.set_defaults(func=cmd_evidence)

    p = sub.add_parser("export", help="copy the released CSV and JSON files to a folder")
    p.add_argument("directory")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("cite", help="print the citation")
    p.add_argument("--bibtex", action="store_true")
    p.set_defaults(func=cmd_cite)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
