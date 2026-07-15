"""
MoneyPrinterTurbo (MPT) API bridge.

This module can:
  1. Start the MPT API server in the background if it is not running.
  2. Submit a video generation task to MPT.
  3. Poll the task status.
  4. Download the final video(s) into the AutoCourse job folder.

MPT API docs are available at http://127.0.0.1:8080/docs when the server is running.
"""
from __future__ import annotations
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from backend.core.config import get_config


def _get_mpt_root() -> Optional[Path]:
    cfg = get_config()
    root = cfg.get("paths", {}).get("moneyprinter_root")
    if not root:
        return None
    return Path(root.replace("/", os.sep))


def _get_mpt_api_url() -> str:
    cfg = get_config()
    return cfg.get("paths", {}).get("moneyprinter_api_url", "http://127.0.0.1:8080")


def _get_mpt_python_exe(mpt_root: Path) -> str:
    """Find the best Python interpreter inside the MPT portable package."""
    candidates = [
        mpt_root / ".venv" / "Scripts" / "python.exe",
        mpt_root / "python" / "python.exe",
        mpt_root / "venv" / "Scripts" / "python.exe",
        mpt_root.parent / "python" / "python.exe",
        mpt_root.parent / "lib" / "python" / "python.exe",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return "python"


def _is_mpt_api_running(url: Optional[str] = None, timeout: int = 3) -> bool:
    url = url or _get_mpt_api_url()
    try:
        r = requests.get(f"{url}/docs", timeout=timeout)
        return r.status_code == 200
    except Exception as e:
        print(f"[_is_mpt_api_running] Failed to connect to {url}/docs: {e}")
        return False


def _start_mpt_api_server(mpt_root: Optional[Path] = None) -> Optional[subprocess.Popen]:
    """Start MPT API server as a background process."""
    mpt_root = mpt_root or _get_mpt_root()
    if not mpt_root or not mpt_root.exists():
        raise RuntimeError(
            "MoneyPrinterTurbo root not found. "
            "Set paths.moneyprinter_root in 01_main_app/config.json to the MPT folder."
        )

    main_py = mpt_root / "main.py"
    if not main_py.exists():
        raise RuntimeError(f"MoneyPrinterTurbo main.py not found at {main_py}")

    python_exe = _get_mpt_python_exe(mpt_root)
    env = os.environ.copy()
    # Avoid opening browser for API server
    env["MPT_WEBUI_AUTO_OPEN"] = "0"

    # Write logs to a file to prevent pipe buffer blocking
    log_file = open(mpt_root / "mpt_api.log", "w", encoding="utf-8")
    
    proc = subprocess.Popen(
        [python_exe, str(main_py)],
        cwd=str(mpt_root),
        env=env,
        stdout=log_file,
        stderr=log_file,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )

    # Wait up to 120 seconds for the API to become ready
    url = _get_mpt_api_url()
    for _ in range(120):
        time.sleep(1)
        if _is_mpt_api_running(url):
            return proc
    proc.terminate()
    raise RuntimeError("MoneyPrinterTurbo API server did not start within 120 seconds.")


def ensure_mpt_api_server() -> Optional[subprocess.Popen]:
    """Make sure MPT API is running. Start it if necessary (only on Windows)."""
    if os.environ.get("MPT_URL"):
        return None  # Trust that Docker is running it, fail at the POST request if not
        
    if _is_mpt_api_running():
        return None
        
    return _start_mpt_api_server()


def build_local_materials(clips: List[Path]) -> List[Dict[str, Any]]:
    """Build MPT MaterialInfo list from local clip paths."""
    materials = []
    for clip in clips:
        if not clip.exists():
            continue
        
        path_str = str(clip.resolve())
        # If running inside Docker, rewrite `/app/outputs/` to `storage/local_videos/`
        # so it bypasses MoneyPrinterTurbo's local path safety check.
        if os.environ.get("MPT_URL"):
            # Replace /app/outputs/ with storage/local_videos/
            # For robustness, we replace both forward and backward slashes (in case of Windows local dev mismatch, though Docker is Linux)
            url_str = path_str.replace("/app/outputs/", "storage/local_videos/").replace("\\app\\outputs\\", "storage/local_videos/")
        else:
            url_str = path_str

        materials.append({
            "provider": "local",
            "url": url_str,
            "duration": 0,  # MPT will detect duration
        })
    return materials


def submit_video_task(
    subject: str,
    script: str,
    keywords: str,
    clips: List[Path],
    aspect: str = "16:9",
    voice: str = "en-US-AndrewMultilingualNeural",
    clip_duration: int = 10,
    subtitle_enabled: bool = True,
    bgm_volume: float = 0.05,
    video_source: str = "local",
) -> str:
    """Submit a video generation task to MPT API. Returns task_id."""
    ensure_mpt_api_server()

    url = _get_mpt_api_url()
    payload: Dict[str, Any] = {
        "video_subject": subject,
        "video_script": script,
        "video_terms": keywords,
        "video_aspect": aspect,
        "voice_name": voice,
        "video_source": video_source,
        "video_clip_duration": clip_duration,
        "video_concat_mode": "sequential",
        "video_transition_mode": "FadeIn" if aspect == "9:16" else None,
        "subtitle_enabled": subtitle_enabled,
        "bgm_volume": bgm_volume,
        "video_count": 1,
        "n_threads": 2,
    }

    if video_source == "local":
        materials = build_local_materials(clips)
        if not materials:
            raise RuntimeError("No local clips provided for local video source.")
        payload["video_materials"] = materials

    try:
        resp = requests.post(f"{url}/api/v1/videos", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", {}).get("task_id") or data.get("task_id")
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(f"Cannot connect to MPT API at {url}. Make sure MPT is running.") from exc
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"MPT API rejected the request: {exc.response.text}") from exc


def poll_task_status(task_id: str, timeout: int = 1800, progress_callback=None) -> Dict[str, Any]:
    """Poll MPT task status until it completes or fails."""
    url = _get_mpt_api_url()
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f"{url}/api/v1/tasks/{task_id}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            task_data = data.get("data", data)
            state = task_data.get("state")
            progress = task_data.get("progress", 0)
            if progress_callback and progress > 0:
                progress_callback(f"MoneyPrinterTurbo rendering: {progress}% complete")
            if state == 1 and progress == 100:
                return task_data
            if state == -1 or task_data.get("error"):
                raise RuntimeError(f"MPT task failed: {task_data}")
        except requests.exceptions.RequestException:
            pass
        time.sleep(3)
    raise RuntimeError(f"MPT task {task_id} did not complete within {timeout} seconds.")


def download_videos(task_data: Dict[str, Any], output_dir: Path) -> List[Path]:
    """Download final video URLs from MPT into the output directory."""
    url = _get_mpt_api_url()
    videos = task_data.get("videos", []) or task_data.get("combined_videos", [])
    downloaded = []
    for i, video_url in enumerate(videos, 1):
        if not video_url:
            continue
        if video_url.startswith("/"):
            video_url = f"{url}{video_url}"
        try:
            resp = requests.get(video_url, timeout=60, stream=True)
            resp.raise_for_status()
            out = output_dir / f"final-{i}.mp4"
            with open(out, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            downloaded.append(out)
        except Exception as exc:
            raise RuntimeError(f"Failed to download video from {video_url}: {exc}") from exc
    return downloaded


def _prepare_local_clips(clips: List[Path], job_id: str) -> List[Path]:
    """
    Copy local clips to MoneyPrinterTurbo's storage/local_videos directory
    so they pass MPT's directory safety validation.
    Returns the new list of paths.
    """
    mpt_root = _get_mpt_root()
    if not mpt_root or os.environ.get("MPT_URL"):
        return clips

    local_videos_dir = mpt_root / "storage" / "local_videos"
    local_videos_dir.mkdir(parents=True, exist_ok=True)

    new_clips = []
    import shutil
    for idx, clip in enumerate(clips):
        if not clip.exists():
            continue
        new_name = f"autocourse_{job_id}_{idx:02d}_{clip.name}"
        target_path = local_videos_dir / new_name
        shutil.copy2(str(clip), str(target_path))
        new_clips.append(target_path)
    return new_clips


def generate_video(
    subject: str,
    script: str,
    keywords: str,
    clips: List[Path],
    output_dir: Path,
    aspect: str = "16:9",
    voice: str = "en-US-AndrewMultilingualNeural",
    clip_duration: int = 10,
    subtitle_enabled: bool = True,
    bgm_volume: float = 0.05,
    video_source: str = "local",
    progress_callback=None,
) -> List[Path]:
    """High-level helper: submit, poll, and download MPT final video(s)."""
    prepared_clips = clips
    if video_source == "local" and clips:
        prepared_clips = _prepare_local_clips(clips, output_dir.name)

    try:
        task_id = submit_video_task(
            subject=subject,
            script=script,
            keywords=keywords,
            clips=prepared_clips,
            aspect=aspect,
            voice=voice,
            clip_duration=clip_duration,
            subtitle_enabled=subtitle_enabled,
            bgm_volume=bgm_volume,
            video_source=video_source,
        )
        task_data = poll_task_status(task_id, progress_callback=progress_callback)
        return download_videos(task_data, output_dir)
    finally:
        if video_source == "local" and prepared_clips != clips:
            for c in prepared_clips:
                try:
                    if c.exists():
                        os.remove(c)
                except Exception:
                    pass

