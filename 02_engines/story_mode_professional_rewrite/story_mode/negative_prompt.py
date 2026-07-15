"""Negative prompt builder for safe, clean children's visuals."""
from __future__ import annotations

DEFAULT_NEGATIVE = [
    "text", "letters", "captions", "subtitles", "watermark", "logo", "signature",
    "bad anatomy", "extra limbs", "extra fingers", "deformed hands", "distorted face",
    "scary", "horror", "violence", "blood", "weapons", "creepy expression",
    "low resolution", "blurry", "pixelated", "noisy", "overexposed", "underexposed",
    "ugly", "uncanny", "adult content", "realistic human photo", "harsh shadows",
]


def build_negative_prompt(extra: list[str] | None = None) -> str:
    values = list(DEFAULT_NEGATIVE)
    if extra:
        values.extend(extra)
    return ", ".join(dict.fromkeys(values))
