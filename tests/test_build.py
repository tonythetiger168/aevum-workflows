import json, re, sys, tempfile
from pathlib import Path
sys.path.insert(0, ".")
from aevum_workflows.build import build_all, MATRIX, CATEGORIES, PLACEHOLDERS

def test_count():
    with tempfile.TemporaryDirectory() as d:
        n = build_all(d)
        assert n >= 300, f"only {n}"
        print(f"PASS count: {n} >= 300")

def test_structure():
    with tempfile.TemporaryDirectory() as d:
        build_all(d)
        for p in Path(d).rglob("*.json"):
            if p.name == "manifest.json":
                continue
            wf = json.loads(p.read_text())
            assert "_meta" in wf and "api_equivalent" in wf["_meta"]
            assert "0_params" in wf, "params echo node missing"
            classes = {v.get("class_type") for v in wf.values() if isinstance(v, dict)}
            assert classes & {"SaveImage", "SaveVideo"}
        print("PASS structure")

def test_placeholder_whitelist():
    with tempfile.TemporaryDirectory() as d:
        build_all(d)
        for p in Path(d).rglob("*.json"):
            if p.name == "manifest.json":
                continue
            used = set(re.findall(r"__([A-Z_]+)__", p.read_text()))
            unknown = used - PLACEHOLDERS
            assert not unknown, f"{p}: {unknown}"
        print("PASS placeholder whitelist")

def test_model_filled():
    with tempfile.TemporaryDirectory() as d:
        build_all(d)
        wf = json.loads((Path(d) / "video" / "short" / "wan22-14b--standard.json").read_text())
        assert wf["1"]["inputs"]["model"] == "wan22-14b", "MODEL not injected"
        st = json.loads((Path(d) / "video" / "long" / "wan22-14b--stitched@30s.json").read_text())
        assert "0" not in st, "stitched should use t2v_chain (no LoadImage node 0)"
        assert "4" in st, "t2v_chain missing EmptyHunyuanLatentVideo"
        print("PASS MODEL filled + t2v_chain")

def test_matrix():
    assert len(CATEGORIES) == 8
    total = sum(len(v["models"]) * len(v["variants"]) for v in MATRIX.values())
    assert total >= 300
    print(f"PASS matrix: {total} across 8 categories")

test_count(); test_structure(); test_placeholder_whitelist(); test_model_filled(); test_matrix()
print("ALL WORKFLOW V2 TESTS PASSED")
