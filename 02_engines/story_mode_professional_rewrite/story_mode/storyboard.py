"""Storyboard utilities for checking visual continuity.

The storyboard layer helps future UI/debug tools show the planned story before
ComfyUI starts rendering expensive images. It is also useful for mentor demos:
you can print a compact table of scene number, title, emotion, camera, lighting,
and prompt length.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List
from .json_schema import StoryPackage
from .utils import word_count


@dataclass(slots=True)
class StoryboardRow:
    number: int
    title: str
    emotion: str
    camera: str
    lighting: str
    environment: str
    duration: int
    prompt_words: int


def build_storyboard_rows(pkg: StoryPackage) -> List[StoryboardRow]:
    rows: List[StoryboardRow] = []
    for scene in pkg.scenes:
        rows.append(
            StoryboardRow(
                number=scene.scene_number,
                title=scene.title,
                emotion=scene.emotion,
                camera=scene.camera.shot_type,
                lighting=scene.lighting.lighting_type,
                environment=scene.environment,
                duration=scene.duration,
                prompt_words=word_count(scene.image_prompt),
            )
        )
    return rows


def storyboard_markdown(pkg: StoryPackage) -> str:
    rows = build_storyboard_rows(pkg)
    lines = [
        f"# Storyboard: {pkg.story_title}",
        "",
        f"Logline: {pkg.logline}",
        "",
        "| # | Title | Emotion | Camera | Lighting | Environment | Seconds | Prompt Words |",
        "|---|---|---|---|---|---|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r.number} | {r.title} | {r.emotion} | {r.camera} | {r.lighting} | {r.environment} | {r.duration} | {r.prompt_words} |"
        )
    return "\n".join(lines)
