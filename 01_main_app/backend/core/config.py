from __future__ import annotations
import json
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config.json"
EXAMPLE_PATH = ROOT / "config.example.json"

import os

@lru_cache(maxsize=1)
def get_config() -> dict:
    path = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_PATH
    cfg = json.loads(path.read_text(encoding="utf-8"))
    
    # Inject Docker environment variables if present
    if "providers" not in cfg:
        cfg["providers"] = {}
    if os.environ.get("OLLAMA_URL"):
        cfg["providers"]["ollama_url"] = os.environ.get("OLLAMA_URL")
    if os.environ.get("COMFYUI_URL"):
        cfg["providers"]["comfyui_url"] = os.environ.get("COMFYUI_URL")
        
    if "paths" not in cfg:
        cfg["paths"] = {}
    if os.environ.get("MPT_URL"):
        cfg["paths"]["moneyprinter_api_url"] = os.environ.get("MPT_URL")
        
    return cfg

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
