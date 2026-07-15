"""Professional dynamic children's story generator."""
from __future__ import annotations

import random
from dataclasses import dataclass
from .json_schema import CharacterProfile, WorldProfile

CONFLICTS = [
    "finds a lost magical object and must return it to its owner",
    "hears a frightened cry from a hidden place and must decide whether to help",
    "accidentally breaks something precious and must choose honesty over fear",
    "gets lost while chasing a sparkle and learns to ask for help",
    "meets someone lonely and learns that kindness can be brave",
]
MORALS = [
    "honesty brings trust and happiness",
    "kindness is strongest when it is difficult",
    "asking for help is a brave choice",
    "sharing makes small hearts grow big",
    "courage means doing the right thing even when afraid",
]

def build_story(topic: str, character: CharacterProfile, world: WorldProfile, rng: random.Random) -> tuple[str, str, str, list[dict[str,str]]]:
    conflict = rng.choice(CONFLICTS)
    moral = rng.choice(MORALS)
    title = topic.strip().title() if topic.strip() else f"{character.name}'s Brave Little Choice"
    logline = f"In {world.world_name}, {character.name} {conflict} and learns that {moral}."
    beats = [
        {"stage":"Beginning", "summary":f"{character.name} enjoys a peaceful day in {world.world_name}."},
        {"stage":"Inciting Incident", "summary":f"{character.name} {conflict}."},
        {"stage":"Rising Action", "summary":f"The choice becomes difficult, and {character.name}'s weakness appears: {character.weakness}."},
        {"stage":"Helper Moment", "summary":f"A friendly creature reminds {character.name} of their strength: {character.strength}."},
        {"stage":"Climax", "summary":f"{character.name} chooses the honest and kind action."},
        {"stage":"Resolution", "summary":f"The world responds warmly and the problem is solved."},
        {"stage":"Moral", "summary":f"The story teaches that {moral}."},
    ]
    paragraphs = [
        f"Once upon a time in {world.world_name}, there lived {character.name}, a {character.species} known for being {character.personality}.",
        f"Every morning, {character.name} walked past {', '.join(world.recurring_landmarks[:2])}, carrying {character.magic_item} and greeting every friend with {character.speaking_style}.",
        f"One bright day, {character.name} {conflict}. At first, the choice seemed small, but deep inside, {character.name} knew it mattered.",
        f"The path became confusing. {character.name} remembered the old rule of the land: {world.magic_rules}. Still, {character.weakness}, and the little hero almost turned away.",
        f"Then a gentle friend appeared near {world.recurring_landmarks[-1]} and reminded {character.name} that {character.strength}. The words felt like a warm lantern in the heart.",
        f"With a deep breath, {character.name} stepped forward and chose what was right. The air shimmered, the flowers leaned closer, and even the river seemed to sparkle with approval.",
        f"Soon, the problem was solved. Everyone in {world.world_name} smiled, not because magic had fixed everything, but because a small honest choice had made the whole world brighter.",
        f"From that day on, {character.name} remembered the lesson: {moral}. And whenever another hard choice appeared, the little hero knew exactly what to do.",
    ]
    return title, logline, moral, beats, "\n\n".join(paragraphs)
