"""Parameter matrix -> 336 workflow JSONs."""
import json
from pathlib import Path

REPO = Path(__file__).parent.parent

PLACEHOLDERS = {"PROMPT", "SEED", "SECONDS", "FRAMES", "FPS", "STEPS", "CFG",
                "BATCH_SIZE", "CONTROL_TYPE", "MASK", "EXPAND", "UPSCALE_SCALE",
                "STYLE", "ASPECT", "MODEL", "START_FRAME", "MOTION_FRAMES",
                "ERROR_RECYCLING", "DIALOGUE", "IP_ADAPTER_FACE", "LORA_INJECT",
                "STYLE_REFERENCE", "VOICE_CLONE"}

MATRIX = {
    "image/basics": {
        "base": "t2i",
        "models": ["sd35-medium", "sd35-large", "flux2-dev", "flux2-pro",
                   "flux2-turbo", "z-image-turbo", "qwen-image", "glm-image",
                   "ideogram-4", "recraft-v4"],
        "variants": {"standard": {}, "batch": {"batch_size": 4},
                     "hires": {"hires_fix": True, "steps": 40},
                     "steps-8": {"steps": 8}, "steps-25": {"steps": 25},
                     "steps-50": {"steps": 50}},
    },
    "image/control": {
        "base": "t2i_control",
        "models": ["sd35-medium", "sd35-large", "flux2-dev", "flux2-pro", "qwen-image"],
        "variants": {c: {"control_type": c} for c in
                     ["depth", "openpose", "canny", "lineart", "seg", "mlsd",
                      "normalmap", "scribble", "ipface", "style-ref"]},
    },
    "image/edit": {
        "base": "inpaint",
        "models": ["sd35-medium", "flux2-dev", "flux2-pro", "qwen-image", "ideogram-4"],
        "variants": {"inpaint": {}, "outpaint-256": {"expand": 256},
                     "outpaint-512": {"expand": 512}, "layers": {"layer_mode": "subject_background"},
                     "bg-replace": {"edit": "background"}, "object-remove": {"edit": "remove"},
                     "color-grade": {"edit": "color"}, "upscale-2x": {"upscale_scale": 2}},
    },
    "image/style": {
        "base": "t2i_style",
        "models": ["sd35-medium", "flux2-dev", "flux2-pro", "qwen-image", "recraft-v4"],
        "variants": {s: {"style": s} for s in
                     ["photoreal", "anime", "oil-paint", "cyberpunk", "watercolor",
                      "3d-render", "pixel-art", "sketch", "film-noir", "vintage",
                      "minimal-flat", "isometric"]},
    },
    "video/short": {
        "base": "t2v",
        "models": ["wan22-14b", "wan22-5b", "ltx-video", "hunyuan-15",
                   "minimax-h3", "cogvideox-5b", "mochi-1", "h3-turbo"],
        "variants": {"standard": {}, "ref-guided-3": {"references": 3},
                     "ref-guided-9": {"references": 9},
                     "low-latency": {"steps": 12},
                     "high-quality": {"steps": 40, "cfg": 7.0},
                     "portrait-9x16": {"aspect": "720x1280"},
                     "wide-21x9": {"aspect": "1920x822"}},
    },
    "video/long": {
        "base": "i2v_chain",
        "models": ["wan22-14b", "ltx-25"],
        "variants": {**{f"{s}@{d}": {"engine": s, "target_seconds": d}
                     for s in ["svi-infinite", "ltx-multishot", "hierarchical"]
                     for d in ["10s", "20s", "30s", "60s", "infinite"]},
                     **{f"stitched@{d}": {"engine": "stitched", "target_seconds": d,
                                          "_base": "t2v_chain"}
                        for d in ["10s", "20s", "30s", "60s", "infinite"]}},
    },
    "av/full": {
        "base": "av_pipeline",
        "models": ["ltx-25", "wan22-14b", "minimax-h3"],
        "variants": {"dialogue": {"audio": ["tts"], "lipsync": True},
                     "sfx-music": {"audio": ["sfx", "music"]},
                     "full-mix": {"audio": ["tts", "sfx", "music"],
                                  "lipsync": True, "upscale": "4k"},
                     "narration": {"audio": ["tts"]},
                     "podcast": {"audio": ["tts"], "speakers": 2}},
    },
    "batch/pipelines": {
        "base": "batch",
        "models": ["z-image-turbo", "sd35-medium", "glm-image"],
        "variants": {"csv-100": {"batch_units": 100}, "csv-1000": {"batch_units": 1000},
                     "webhook": {"notify": "webhook"}, "priority-queue": {"priority": True},
                     "night-batch": {"schedule": "0 2 * * *"}},
    },
}

BASE = {
"t2i": {"3": {"class_type": "KSampler", "inputs": {"seed": "__SEED__",
        "steps": "__STEPS__", "cfg": "__CFG__", "batch_size": "__BATCH_SIZE__",
        "positive": "__PROMPT__"}},
        "8": {"class_type": "SaveImage", "inputs": {"filename_prefix": "aevum"}}},
"t2i_control": {"3": {"class_type": "KSampler", "inputs": {"seed": "__SEED__"}},
        "7": {"class_type": "ControlNetApply", "inputs": {"control_type": "__CONTROL_TYPE__",
              "strength": 0.8}},
        "8": {"class_type": "SaveImage", "inputs": {}}},
"t2i_style": {"2": {"class_type": "StyleApply", "inputs": {"style": "__STYLE__"}},
        "3": {"class_type": "KSampler", "inputs": {"seed": "__SEED__"}},
        "8": {"class_type": "SaveImage", "inputs": {}}},
"inpaint": {"4": {"class_type": "InpaintModelConditioning",
        "inputs": {"positive": "__PROMPT__", "mask": "__MASK__"}},
        "5": {"class_type": "KSampler", "inputs": {"seed": "__SEED__"}},
        "8": {"class_type": "SaveImage", "inputs": {}}},
"t2v": {"1": {"class_type": "WanVideoModelLoader", "inputs": {"model": "__MODEL__"}},
        "4": {"class_type": "EmptyHunyuanLatentVideo",
              "inputs": {"width": 1280, "height": 720, "length": "__FRAMES__"}},
        "5": {"class_type": "KSampler", "inputs": {"seed": "__SEED__", "steps": "__STEPS__",
              "cfg": "__CFG__", "motion_reference": "__MOTION_FRAMES__"}},
        "6": {"class_type": "SaveVideo", "inputs": {}}},
"i2v_chain": {"0": {"class_type": "LoadImage", "inputs": {"image": "__START_FRAME__"}},
        "5": {"class_type": "KSampler", "inputs": {"seed": "__SEED__",
              "error_recycling": "__ERROR_RECYCLING__"}},
        "9": {"class_type": "SaveVideo", "inputs": {"fps": "__FPS__"}}},
"t2v_chain": {"4": {"class_type": "EmptyHunyuanLatentVideo",
        "inputs": {"width": 1280, "height": 720, "length": "__FRAMES__"}},
        "5": {"class_type": "KSampler", "inputs": {"seed": "__SEED__"}},
        "9": {"class_type": "SaveVideo", "inputs": {"fps": "__FPS__"}}},
"av_pipeline": {"10": {"class_type": "CosyVoiceTTS", "inputs": {"text": "__DIALOGUE__"}},
        "11": {"class_type": "LatentSync", "inputs": {}},
        "12": {"class_type": "SaveVideo", "inputs": {"has_audio": True}}},
"batch": {"20": {"class_type": "AevumBatchLoader", "inputs": {"source": "csv"}},
        "3": {"class_type": "KSampler", "inputs": {"seed": "__SEED__"}},
        "8": {"class_type": "SaveImage", "inputs": {}}},
}

DEFAULTS = {"STEPS": 25, "CFG": 6.0, "BATCH_SIZE": 1, "FRAMES": 121, "FPS": 24,
            "UPSCALE_SCALE": 1, "EXPAND": 0, "STYLE": "none", "CONTROL_TYPE": "depth"}

CATEGORIES = list(MATRIX.keys())

def build_all(out_dir=None) -> int:
    out = Path(out_dir) if out_dir else REPO / "workflows"
    manifest = []
    n = 0
    for cat, cfg in MATRIX.items():
        for model in cfg["models"]:
            for vname, vparams in cfg["variants"].items():
                wf = json.loads(json.dumps(BASE[vparams.get("_base", cfg["base"])]))
                kv = {"MODEL": model}
                for k, v in vparams.items():
                    kk = k.upper()
                    if kk in PLACEHOLDERS:
                        kv[kk] = v
                s = json.dumps(wf)
                for ph in PLACEHOLDERS:
                    if f"__{ph}__" in s and ph not in kv and ph in DEFAULTS:
                        kv[ph] = DEFAULTS[ph]
                for node in wf.values():
                    if isinstance(node, dict):
                        for k, v in list(node.get("inputs", {}).items()):
                            if isinstance(v, str) and v.startswith("__") and v.endswith("__"):
                                key = v.strip("_")
                                if key in kv:
                                    node["inputs"][k] = kv[key]
                wf["0_params"] = {"class_type": "AevumParams", "inputs": dict(vparams)}
                wf["_meta"] = {"category": cat, "model": model, "variant": vname,
                               "params": vparams, "source": "aevum-workflows v2.0.0",
                               "api_equivalent": f"POST /v1/{'videos' if 'video' in cat or cat.startswith('av') else 'images'}/generations"}
                path = out / cat / f"{model}--{vname}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
                manifest.append({"file": str(path.relative_to(out)), "category": cat,
                                 "model": model, "variant": vname})
                n += 1
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    return n
