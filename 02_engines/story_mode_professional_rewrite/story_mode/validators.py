"""Validation helpers for generated story JSON."""
from __future__ import annotations
from .json_schema import StoryPackage
from .utils import word_count

def validate_story_package(pkg: StoryPackage, min_scenes: int = 5) -> list[str]:
    errors=[]
    if len(pkg.scenes)<min_scenes: errors.append('Not enough scenes')
    if not pkg.character_sheet.name: errors.append('Missing character name')
    if not pkg.world_sheet.world_name: errors.append('Missing world name')
    for s in pkg.scenes:
        if word_count(s.image_prompt)<180: errors.append(f'Scene {s.scene_number} prompt too short')
        if 'text' not in s.negative_prompt: errors.append(f'Scene {s.scene_number} negative prompt weak')
    return errors
