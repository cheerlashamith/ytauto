"""Persistent world generator."""
from __future__ import annotations

import random
from .json_schema import WorldProfile
from .environment_system import choose_environment, ENVIRONMENTS
from .utils import choose_many

WORLD_NAMES = ["Whisperbloom", "Sunberry Vale", "Moonpetal Woods", "Glitterfern Hollow", "Kindlelight Kingdom", "Mossybell Meadow"]
KINGDOMS = ["a gentle kingdom where animals and tiny magical beings live together", "a hidden valley protected by old friendly trees", "a cozy woodland village ruled by kindness", "a sparkling fairy province beside a singing river"]
MAGIC_RULES = ["magic only works when someone acts with kindness", "glowing plants shine brighter when friends tell the truth", "lost objects softly hum when their owner is near", "the forest paths open only for brave and honest hearts"]
LORE = ["Long ago, the first firefly promised to guide lost children home.", "Every season, the oldest tree gives one golden leaf to the kindest heart.", "The river remembers every good deed and sparkles when kindness is shown.", "The moon watches over the valley and rewards courage with gentle light."]

def generate_world(topic: str, rng: random.Random) -> WorldProfile:
    env = choose_environment(topic, rng)
    e = ENVIRONMENTS[env]
    name = rng.choice(WORLD_NAMES)
    palette = e["color_mood"].split(", ")[:5]
    landmarks = choose_many(rng, ["singing river", "ancient moon tree", "crystal bridge", "tiny lantern village", "golden meadow", "sparkle cave"], 3)
    anchor = f"All scenes stay in {name}, with recurring landmarks: {', '.join(landmarks)} and the same {env} visual identity."
    return WorldProfile(
        world_name=name, environment_type=env, kingdom=rng.choice(KINGDOMS), forest=e["midground"], buildings=e.get("background", "storybook cottages"),
        weather=e["weather"], time_period="timeless fairytale morning-to-evening world", plants=e["foreground"], animals=e.get("animals", "friendly birds, butterflies, squirrels and tiny glowing creatures"),
        magic_rules=rng.choice(MAGIC_RULES), background_lore=rng.choice(LORE), color_palette=palette,
        recurring_landmarks=landmarks, consistency_anchor=anchor
    )
