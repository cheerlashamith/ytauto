"""Configuration for the professional AI kids story generation pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import json


@dataclass(slots=True)
class StoryConfig:
    """Runtime configuration for story generation."""

    output_path: Path = Path("scenes_story.json")
    language: str = "English"
    min_words: int = 700
    max_words: int = 1500
    min_scenes: int = 8
    max_scenes: int = 15
    default_scene_duration: int = 8
    target_prompt_min_words: int = 250
    target_prompt_max_words: int = 500
    quality_preset: str = "pixar"
    age_group: str = "children ages 5 to 10"
    allow_mild_tension: bool = True
    seed: Optional[int] = None
    include_legacy_prompt_key: bool = True
    image_aspect: str = "vertical 9:16"
    prompt_style_version: str = "professional_v1"

    @classmethod
    def from_json(cls, path: str | Path) -> "StoryConfig":
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        if "output_path" in data:
            data["output_path"] = Path(data["output_path"])
        return cls(**data)

    def to_dict(self) -> Dict[str, object]:
        d = self.__dict__.copy()
        d["output_path"] = str(self.output_path)
        return d


DEFAULT_STYLE_ALIASES: Dict[str, str] = {
    "pixar": "pixar",
    "disney": "disney",
    "dreamworks": "dreamworks",
    "ghibli": "studio_ghibli",
    "studio ghibli": "studio_ghibli",
    "3d": "three_d_animation",
    "3d animation": "three_d_animation",
    "storybook": "storybook",
    "watercolor": "watercolor",
    "anime": "anime",
    "clay": "clay_animation",
    "clay animation": "clay_animation",
}


SUPPORTED_ENVIRONMENTS: List[str] = [
    "Enchanted Forest",
    "Magic Castle",
    "Candy Kingdom",
    "Ocean Kingdom",
    "Space Planet",
    "Snow Village",
    "Fairy Garden",
    "Jungle",
    "Dragon Mountain",
    "Cloud City",
    "Moonlit Meadow",
    "Crystal Cave",
]
