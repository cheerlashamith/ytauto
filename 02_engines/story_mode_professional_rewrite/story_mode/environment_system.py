"""Reusable environment generation system."""
from __future__ import annotations

from dataclasses import dataclass
import random
from .json_schema import EnvironmentSpec
from .utils import choose

ENVIRONMENTS = {
    "Enchanted Forest": {
        "foreground": "mossy stones, tiny glowing mushrooms, dew-covered grass, curled fern leaves",
        "midground": "ancient trees with spiral bark, hanging lantern flowers, a narrow sparkling path",
        "background": "misty tree layers, distant fairy lights, soft hills, hidden woodland cottages",
        "weather": "gentle floating mist and mild breeze",
        "particles": "golden pollen, fireflies, drifting leaf motes",
        "textures": "velvety moss, satin petals, rough bark, glassy dew drops",
        "color_mood": "emerald green, warm gold, soft teal, lavender shadows",
    },
    "Magic Castle": {
        "foreground": "polished marble steps, tiny banners, jewel-toned flowers in silver pots",
        "midground": "tall castle gates, glowing crystal windows, carved moon symbols",
        "background": "floating towers, rainbow clouds, distant mountains",
        "weather": "clear magical air with sparkling breeze",
        "particles": "crystal sparkles, soft golden dust, floating magic runes without readable text",
        "textures": "smooth stone, velvet banners, crystal glass, metallic trim",
        "color_mood": "royal blue, cream gold, violet, pearl white",
    },
    "Candy Kingdom": {
        "foreground": "gumdrop flowers, sugar crystal pebbles, frosting swirls",
        "midground": "candy cane bridges, cookie cottages, chocolate path",
        "background": "cotton candy hills, caramel waterfalls, pastel clouds",
        "weather": "sweet sparkling air",
        "particles": "sugar glitter, tiny candy sparkles",
        "textures": "glossy candy, soft marshmallow, crumbly cookie, silky frosting",
        "color_mood": "pastel pink, mint, vanilla cream, strawberry red",
    },
    "Ocean Kingdom": {
        "foreground": "coral branches, pearl shells, waving sea grass",
        "midground": "friendly fish, bubble trails, underwater archways",
        "background": "glowing palace under the sea, sunbeams through water, distant whales",
        "weather": "calm underwater currents",
        "particles": "bubbles, shimmering plankton, light caustics",
        "textures": "smooth shells, soft coral, glassy bubbles, flowing water",
        "color_mood": "aqua, turquoise, pearl, sea green, soft gold",
    },
    "Space Planet": {
        "foreground": "soft alien grass, glowing stones, tiny crater flowers",
        "midground": "friendly rounded spaceships, crystal domes, floating moon rocks",
        "background": "ringed planets, star fields, colorful nebula clouds",
        "weather": "gentle cosmic breeze",
        "particles": "stardust, glowing specks, floating tiny comets",
        "textures": "smooth metallic ships, fuzzy alien plants, crystalline rocks",
        "color_mood": "deep indigo, cyan, violet, silver, neon green",
    },
}

def choose_environment(topic: str, rng: random.Random) -> str:
    text = topic.lower()
    if any(k in text for k in ["ocean", "fish", "mermaid", "sea"]): return "Ocean Kingdom"
    if any(k in text for k in ["space", "star", "planet", "rocket"]): return "Space Planet"
    if any(k in text for k in ["castle", "princess", "king", "queen"]): return "Magic Castle"
    if any(k in text for k in ["candy", "sweet", "chocolate"]): return "Candy Kingdom"
    return choose(rng, list(ENVIRONMENTS.keys()))

def build_environment_spec(name: str) -> EnvironmentSpec:
    data = ENVIRONMENTS.get(name, ENVIRONMENTS["Enchanted Forest"])
    return EnvironmentSpec(name=name, **data)
