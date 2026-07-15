"""Dataclasses and JSON serialization schema for story mode."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class CharacterProfile:
    name: str
    age: str
    gender: str
    species: str
    height: str
    hair: str
    eyes: str
    face: str
    body: str
    clothes: str
    accessories: str
    personality: str
    weakness: str
    strength: str
    speaking_style: str
    signature_colors: List[str]
    magic_item: str
    consistency_anchor: str

    def to_prompt_block(self) -> str:
        colors = ", ".join(self.signature_colors)
        return (
            f"Main character: {self.name}, a {self.age} {self.gender} {self.species}. "
            f"Height and build: {self.height}, {self.body}. Hair/fur: {self.hair}. "
            f"Eyes: {self.eyes}. Face: {self.face}. Clothes: {self.clothes}. "
            f"Accessories: {self.accessories}. Signature colors: {colors}. "
            f"Magic item: {self.magic_item}. Personality: {self.personality}. "
            f"Always keep this exact identity consistent: {self.consistency_anchor}."
        )


@dataclass(slots=True)
class WorldProfile:
    world_name: str
    environment_type: str
    kingdom: str
    forest: str
    buildings: str
    weather: str
    time_period: str
    plants: str
    animals: str
    magic_rules: str
    background_lore: str
    color_palette: List[str]
    recurring_landmarks: List[str]
    consistency_anchor: str

    def to_prompt_block(self) -> str:
        palette = ", ".join(self.color_palette)
        landmarks = ", ".join(self.recurring_landmarks)
        return (
            f"World: {self.world_name}, a {self.environment_type}. Kingdom/region: {self.kingdom}. "
            f"Landscape: {self.forest}. Buildings: {self.buildings}. Weather: {self.weather}. "
            f"Time period: {self.time_period}. Plants: {self.plants}. Animals: {self.animals}. "
            f"Magic rules: {self.magic_rules}. Lore: {self.background_lore}. "
            f"Palette: {palette}. Recurring landmarks: {landmarks}. "
            f"Keep the world consistent: {self.consistency_anchor}."
        )


@dataclass(slots=True)
class CameraSpec:
    shot_type: str
    lens: str
    angle: str
    framing: str
    movement: str
    composition: str


@dataclass(slots=True)
class LightingSpec:
    lighting_type: str
    key_light: str
    fill_light: str
    shadows: str
    atmosphere: str
    render_notes: str


@dataclass(slots=True)
class EnvironmentSpec:
    name: str
    foreground: str
    midground: str
    background: str
    weather: str
    particles: str
    textures: str
    color_mood: str


@dataclass(slots=True)
class SceneSpec:
    scene_number: int
    title: str
    narration: str
    emotion: str
    environment: str
    characters: List[str]
    objects: List[str]
    action: str
    camera: CameraSpec
    lighting: LightingSpec
    environment_details: EnvironmentSpec
    mood: str
    duration: int
    transition: str
    music: str
    sfx: List[str]
    image_prompt: str
    negative_prompt: str

    def to_output_dict(self, include_legacy_prompt_key: bool = True) -> Dict[str, Any]:
        data = asdict(self)
        data["camera"] = asdict(self.camera)
        data["lighting"] = asdict(self.lighting)
        data["environment_details"] = asdict(self.environment_details)
        if include_legacy_prompt_key:
            data["prompt"] = self.image_prompt
        return data


@dataclass(slots=True)
class StoryPackage:
    subject: str
    story_title: str
    logline: str
    moral: str
    full_story: str
    keywords: str
    character_sheet: CharacterProfile
    world_sheet: WorldProfile
    scenes: List[SceneSpec]

    def to_output_dict(self, include_legacy_prompt_key: bool = True) -> Dict[str, Any]:
        return {
            "render_mode": "story",
            "subject": self.subject,
            "story_title": self.story_title,
            "logline": self.logline,
            "moral": self.moral,
            "keywords": self.keywords,
            "moneyprinter_script": "\n\n".join(scene.narration for scene in self.scenes),
            "full_story": self.full_story,
            "character_sheet": asdict(self.character_sheet),
            "world_sheet": asdict(self.world_sheet),
            "scenes": [s.to_output_dict(include_legacy_prompt_key) for s in self.scenes],
        }
