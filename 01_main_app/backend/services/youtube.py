"""
YouTube video extraction utilities.

Uses yt-dlp to fetch video metadata and subtitles, or falls back to a generic
summary if the URL is unavailable.
"""
from __future__ import annotations
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional
import re
import sys


def _extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from a URL."""
    patterns = [
        r"(?:v=|/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _run_yt_dlp(args: list, timeout: int = 60) -> str:
    """Run yt-dlp with given args and return stdout."""
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    # Try running via Python module first
    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "yt_dlp"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creationflags,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            if proc.returncode == 0:
                return stdout
            if "No module named" in stderr or "Error while finding module" in stderr:
                pass
            else:
                raise RuntimeError(f"yt-dlp failed: {stderr[-1000:]}")
        except subprocess.TimeoutExpired:
            proc.kill()
            raise RuntimeError("yt-dlp timed out")
    except Exception:
        pass

    # Fallback to standalone command-line tool
    proc = subprocess.Popen(
        ["yt-dlp"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=creationflags,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise RuntimeError("yt-dlp timed out")
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {stderr[-1000:]}")
    return stdout


def fetch_metadata(url: str) -> Dict[str, Any]:
    """Fetch YouTube video metadata using yt-dlp."""
    try:
        stdout = _run_yt_dlp(
            ["--dump-json", "--no-playlist", "--skip-download", url],
            timeout=60,
        )
        data = json.loads(stdout.strip().splitlines()[0])
        return {
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "channel": data.get("channel", ""),
            "duration": data.get("duration", 0),
            "tags": data.get("tags", []),
            "categories": data.get("categories", []),
        }
    except Exception as exc:
        raise RuntimeError(f"Failed to fetch YouTube metadata: {exc}") from exc


def fetch_transcript(url: str) -> str:
    """
    Try to fetch auto-generated or manual subtitles for a YouTube video.
    Falls back to a short description if no subtitles are available.
    """
    video_id = _extract_video_id(url)
    if not video_id:
        raise RuntimeError(f"Could not extract video ID from URL: {url}")

    # Try to download English subtitles first, then auto-generated English
    for lang in ["en", "en-US", "en-GB"]:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "sub"
                _run_yt_dlp(
                    [
                        "--write-sub",
                        "--sub-langs", lang,
                        "--convert-subs", "srt",
                        "--skip-download",
                        "-o", str(out),
                        url,
                    ],
                    timeout=60,
                )
                srt_files = list(Path(tmp).glob("*.srt"))
                if srt_files:
                    text = srt_files[0].read_text(encoding="utf-8")
                    # Strip SRT timing and line numbers, keep only text
                    lines = []
                    for line in text.splitlines():
                        if line.strip() and not line.strip().isdigit() and " --> " not in line:
                            lines.append(line.strip())
                    return " ".join(lines)
        except Exception:
            continue

    # Try auto-generated subtitles
    for lang in ["en", "en-US", "en-GB"]:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "sub"
                _run_yt_dlp(
                    [
                        "--write-auto-sub",
                        "--sub-langs", lang,
                        "--convert-subs", "srt",
                        "--skip-download",
                        "-o", str(out),
                        url,
                    ],
                    timeout=60,
                )
                srt_files = list(Path(tmp).glob("*.srt"))
                if srt_files:
                    text = srt_files[0].read_text(encoding="utf-8")
                    lines = []
                    for line in text.splitlines():
                        if line.strip() and not line.strip().isdigit() and " --> " not in line:
                            lines.append(line.strip())
                    return " ".join(lines)
        except Exception:
            continue

    raise RuntimeError(
        "No subtitles available for this YouTube video. "
        "Use a video with captions, or install whisper for audio transcription."
    )


def summarize_video(url: str) -> Dict[str, str]:
    """Return a dict with title, transcript, and summary prompt context."""
    metadata = fetch_metadata(url)
    transcript = fetch_transcript(url)
    return {
        "title": metadata.get("title", "YouTube video"),
        "description": metadata.get("description", "")[:1000],
        "transcript": transcript[:4000],
        "channel": metadata.get("channel", ""),
    }
