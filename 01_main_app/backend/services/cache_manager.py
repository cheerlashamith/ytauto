from __future__ import annotations
import json
import hashlib
from pathlib import Path
from backend.core.config import get_config

CACHE_DIR = Path(__file__).resolve().parents[2] / "cache"

class CacheManager:
    @staticmethod
    def _is_enabled() -> bool:
        return get_config().get("features", {}).get("enable_cache", True)

    @staticmethod
    def _get_key(model_name: str, task_type: str, prompt: str, prompt_version: str = "1.0", system_prompt_version: str = "1.0") -> str:
        raw = f"{model_name}|{task_type}|{prompt}|{prompt_version}|{system_prompt_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def get(model_name: str, task_type: str, prompt: str, prompt_version: str = "1.0", system_prompt_version: str = "1.0") -> str | None:
        if not CacheManager._is_enabled():
            return None
            
        key = CacheManager._get_key(model_name, task_type, prompt, prompt_version, system_prompt_version)
        path = CACHE_DIR / task_type / f"{key}.json"
        
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("result")
            except:
                pass
        return None

    @staticmethod
    def set(model_name: str, task_type: str, prompt: str, result: str, prompt_version: str = "1.0", system_prompt_version: str = "1.0"):
        if not CacheManager._is_enabled():
            return
            
        key = CacheManager._get_key(model_name, task_type, prompt, prompt_version, system_prompt_version)
        folder = CACHE_DIR / task_type
        folder.mkdir(parents=True, exist_ok=True)
        
        path = folder / f"{key}.json"
        path.write_text(json.dumps({"result": result}, indent=2), encoding="utf-8")
    @staticmethod
    def get_cache_stats() -> dict:
        total_size = 0
        total_files = 0
        tasks = {}
        if CACHE_DIR.exists():
            for task_dir in CACHE_DIR.iterdir():
                if task_dir.is_dir():
                    count = 0
                    size = 0
                    for f in task_dir.glob("*.json"):
                        count += 1
                        size += f.stat().st_size
                    tasks[task_dir.name] = {"count": count, "size_bytes": size}
                    total_files += count
                    total_size += size
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "tasks": tasks
        }
