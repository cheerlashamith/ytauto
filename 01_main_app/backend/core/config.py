from __future__ import annotations
import json
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config.json"
EXAMPLE_PATH = ROOT / "config.example.json"

@lru_cache(maxsize=1)
def get_config() -> dict:
    path = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_PATH
    return json.loads(path.read_text(encoding="utf-8"))

def save_config(new_cfg: dict):
    CONFIG_PATH.write_text(json.dumps(new_cfg, indent=2), encoding="utf-8")
    get_config.cache_clear()

def project_root() -> Path:
    return ROOT

def outputs_root() -> Path:
    cfg = get_config()
    out = cfg.get("paths", {}).get("outputs_dir", "outputs")
    p = ROOT / out
    p.mkdir(parents=True, exist_ok=True)
    return p
