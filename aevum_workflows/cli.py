import json, re, sys
from pathlib import Path
from aevum_workflows.build import build_all, CATEGORIES, PLACEHOLDERS

def validate(wf_dir="workflows") -> int:
    bad = 0
    for p in Path(wf_dir).rglob("*.json"):
        if p.name == "manifest.json":
            continue
        try:
            wf = json.loads(p.read_text())
            classes = {v.get("class_type") for v in wf.values() if isinstance(v, dict)}
            if not classes & {"SaveImage", "SaveVideo"}:
                print(f"FAIL {p}: no save node"); bad += 1
            if "_meta" not in wf:
                print(f"FAIL {p}: no _meta"); bad += 1
            for ph in set(re.findall(r"__([A-Z_]+)__", p.read_text())):
                if ph not in PLACEHOLDERS:
                    print(f"FAIL {p}: unknown placeholder __{ph}__"); bad += 1
        except Exception as e:
            print(f"FAIL {p}: {e}"); bad += 1
    total = len([p for p in Path(wf_dir).rglob("*.json") if p.name != "manifest.json"])
    print(f"validated {total - bad}/{total} ok")
    return bad

def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "build"
    if cmd == "build":
        n = build_all(args[1] if len(args) > 1 else None)
        print(f"built {n} workflows across {len(CATEGORIES)} categories")
    elif cmd == "validate":
        sys.exit(1 if validate(args[1] if len(args) > 1 else "workflows") else 0)
    elif cmd == "list":
        for c in CATEGORIES:
            print(f"{c}: {len(list(Path('workflows', c).glob('*.json')))} workflows")

if __name__ == "__main__":
    main()
