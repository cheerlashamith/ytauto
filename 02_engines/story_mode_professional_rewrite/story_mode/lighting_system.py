"""Lighting system for cinematic prompt engineering."""
from __future__ import annotations

import random
from .json_schema import LightingSpec
from .utils import choose

LIGHTING_PRESETS = {
    "golden_hour": LightingSpec("Golden Hour", "warm low sun key light", "soft peach bounce fill", "long soft shadows", "floating dust motes and warm haze", "Pixar-style warm global illumination, HDR, gentle rim light"),
    "blue_hour": LightingSpec("Blue Hour", "cool twilight key light", "soft lavender fill", "soft blue shadows", "misty evening atmosphere", "cinematic blue hour lighting with subtle magical glow"),
    "sunrise": LightingSpec("Sunrise", "fresh golden sunrise key", "pale sky fill", "soft awakening shadows", "dew sparkle and morning fog", "volumetric sunrise rays, soft ambient occlusion"),
    "sunset": LightingSpec("Sunset", "orange sunset key", "rose colored fill", "soft dramatic shadows", "warm floating particles", "god rays through trees, HDR warm highlights"),
    "moonlight": LightingSpec("Moonlight", "silver moon key light", "deep blue fill", "soft night shadows", "fireflies and glowing mist", "gentle moonlit volumetric rays, magical rim light"),
    "volumetric": LightingSpec("Volumetric Rays", "bright directional god rays", "soft global fill", "layered soft shadows", "visible light beams through fog", "cinematic volumetric lighting, high dynamic range"),
    "pixar": LightingSpec("Pixar Lighting", "large soft key light", "warm bounce fill", "soft contact shadows", "clean magical atmosphere", "global illumination, ambient occlusion, soft rim light, polished 3D render"),
}


def choose_lighting(emotion: str, environment: str, rng: random.Random) -> LightingSpec:
    text = f"{emotion} {environment}".lower()
    if any(k in text for k in ["happy", "excited", "relieved", "hope"]):
        return choose(rng, [LIGHTING_PRESETS["golden_hour"], LIGHTING_PRESETS["sunrise"], LIGHTING_PRESETS["pixar"]])
    if any(k in text for k in ["sad", "lonely", "scared", "mystery"]):
        return choose(rng, [LIGHTING_PRESETS["blue_hour"], LIGHTING_PRESETS["moonlight"]])
    if any(k in text for k in ["magic", "fairy", "dragon", "castle"]):
        return choose(rng, [LIGHTING_PRESETS["volumetric"], LIGHTING_PRESETS["sunset"], LIGHTING_PRESETS["moonlight"]])
    return choose(rng, list(LIGHTING_PRESETS.values()))
