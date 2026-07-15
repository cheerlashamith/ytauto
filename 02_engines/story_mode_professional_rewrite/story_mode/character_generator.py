"""Persistent character sheet generator."""
from __future__ import annotations

import random
from .json_schema import CharacterProfile
from .utils import choose, choose_many

NAMES = ["Lumi", "Rumi", "Pip", "Milo", "Nila", "Tara", "Bobo", "Kiki", "Mina", "Oli", "Zuzu", "Fia"]
SPECIES = ["rabbit", "fox cub", "squirrel", "little fairy", "bear cub", "turtle", "mouse", "penguin", "dragon child", "kitten"]
HAIR = ["soft golden curls", "fluffy chestnut fur", "silky silver-blue hair", "short cocoa-brown hair", "cotton-white fur", "warm honey-colored fur"]
EYES = ["large emerald green eyes", "big warm brown eyes", "sparkling sky-blue eyes", "gentle violet eyes", "round amber eyes"]
CLOTHES = ["a tiny teal vest with cream stitching", "a sunflower-yellow scarf and little brown satchel", "a lavender cloak with star-shaped buttons", "a mint-green dress with soft gold trim", "a cozy blue jacket and red ribbon"]
ACCESSORIES = ["a small acorn necklace", "a moon-shaped hair clip", "round little spectacles", "a tiny compass charm", "a star bracelet"]
PERSONALITIES = ["kind, curious, and slightly shy", "brave but sometimes impatient", "cheerful, honest, and full of wonder", "gentle, clever, and loyal", "playful, imaginative, and easily excited"]
WEAKNESSES = ["gets nervous when the forest becomes too quiet", "sometimes rushes before thinking", "is afraid to ask for help", "worries about making mistakes", "gets distracted by shiny things"]
STRENGTHS = ["always tells the truth", "notices small details others miss", "helps friends even when scared", "keeps trying after mistakes", "uses kindness to solve problems"]
SPEAKING = ["speaks in short sincere sentences", "asks many curious questions", "uses gentle encouraging words", "speaks with bright playful excitement", "talks softly but bravely"]
MAGIC_ITEMS = ["a glowing pebble", "a tiny silver bell", "a golden leaf compass", "a star-tipped wand", "a crystal acorn", "a moonlit ribbon"]
COLORS = ["warm cream", "teal", "lavender", "soft gold", "mint green", "sky blue", "peach"]

def generate_character(topic: str, rng: random.Random) -> CharacterProfile:
    name = choose(rng, NAMES)
    species = choose(rng, SPECIES)
    colors = choose_many(rng, COLORS, 3)
    hair = choose(rng, HAIR)
    eyes = choose(rng, EYES)
    clothes = choose(rng, CLOTHES)
    accessories = choose(rng, ACCESSORIES)
    magic_item = choose(rng, MAGIC_ITEMS)
    face = f"round child-friendly face, soft cheeks, tiny nose, readable innocent expression, {eyes}"
    body = "small charming proportions, soft rounded silhouette, expressive hands, child-safe appealing design"
    anchor = f"{name} must always remain the same {species} with {hair}, {eyes}, {clothes}, {accessories}, and {magic_item}."
    return CharacterProfile(
        name=name, age="young childlike", gender="gentle child", species=species, height="small and adorable, about knee-high to an adult human", hair=hair, eyes=eyes,
        face=face, body=body, clothes=clothes, accessories=accessories, personality=choose(rng, PERSONALITIES),
        weakness=choose(rng, WEAKNESSES), strength=choose(rng, STRENGTHS), speaking_style=choose(rng, SPEAKING),
        signature_colors=colors, magic_item=magic_item, consistency_anchor=anchor
    )
