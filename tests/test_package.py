import hashlib
import json
from pathlib import Path

import pytest

import verification_gap_ledger as vgl
from verification_gap_ledger.cli import main

REPO = Path(__file__).resolve().parents[1]


def test_counts_match_stats():
    s = vgl.stats()
    assert len(vgl.programs()) == s["n_programs"] == 24
    assert len(vgl.programs(level="federal")) == s["n_federal"]
    assert len(vgl.programs(level="state")) == s["n_state"]
    assert len(vgl.evidence()) == s["n_evidence"]
    assert s["version"] == vgl.DATA_VERSION


def test_types_and_ranges():
    for p in vgl.programs():
        assert 0 <= p["R_required"] <= 4
        assert 0 <= p["C_public"] <= 4
        assert 0 <= p["A_attributable"] <= 3
        assert p["gap_rc"] == p["R_required"] - p["C_public"]
        assert p["gap_outcome"] == 4 - max(p["R_required"], p["C_public"])
        assert vgl.SCALES["R"][p["R_required"]] == p["R_label"]
        assert vgl.SCALES["C"][p["C_public"]] == p["C_label"]
        assert vgl.SCALES["A"][p["A_attributable"]] == p["A_label"]
    ids = {p["ledger_id"] for p in vgl.programs()}
    assert all(e["ledger_id"] in ids for e in vgl.evidence())


def test_program_lookup():
    p = vgl.program("VGL-NY-006")
    assert p["R_required"] == 2
    assert vgl.evidence("VGL-NY-006", dimension="R")
    with pytest.raises(KeyError):
        vgl.program("VGL-XX-999")


def test_returned_rows_are_copies():
    vgl.programs()[0]["R_required"] = 99
    assert vgl.programs()[0]["R_required"] != 99


def test_citation():
    assert vgl.DOI in vgl.citation()
    assert vgl.citation("bibtex").startswith("@dataset{")


@pytest.mark.skipif(not (REPO / "data" / "processed").exists(), reason="repository data not present")
def test_bundled_data_identical_to_release():
    pairs = [
        ("programs", REPO / "data/processed/vgl_programs.csv"),
        ("evidence", REPO / "data/processed/vgl_evidence.csv"),
        ("reference_sources", REPO / "data/processed/vgl_reference_sources.csv"),
        ("stats", REPO / "paper/stats.json"),
    ]
    for name, src in pairs:
        a = hashlib.sha256(vgl.data_path(name).read_bytes()).hexdigest()
        b = hashlib.sha256(src.read_bytes()).hexdigest()
        assert a == b, f"{name} differs from {src}; run python code/07_sync_package_data.py"


def test_cli(capsys, tmp_path):
    main(["info"])
    assert "24 (15 federal, 9 New York State)" in capsys.readouterr().out
    main(["list", "--format", "json"])
    assert len(json.loads(capsys.readouterr().out)) == 24
    main(["show", "VGL-NY-006"])
    assert "R = 2" in capsys.readouterr().out
    main(["export", str(tmp_path)])
    assert (tmp_path / "vgl_programs.csv").exists()
