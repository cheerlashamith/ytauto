"""Music and sound-effect system for children story scenes.

This module is intentionally separate from the visual prompt system so that
future renderers can use the same story plan to generate audio ambience,
background music, and sound effect cues.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List


@dataclass(frozen=True, slots=True)
class AudioMood:
    music: str
    sfx: List[str]
    ambience: str
    voice_direction: str


AUDIO_MOODS: Dict[str, AudioMood] = {
    "happy": AudioMood(
        music="gentle celesta, soft pizzicato strings, light flute melody, playful but not loud",
        sfx=["small bird chirps", "soft leaf rustle", "tiny sparkle chime"],
        ambience="peaceful outdoor ambience with warm forest air",
        voice_direction="bright, warm, smiling narration with gentle excitement",
    ),
    "curious": AudioMood(
        music="light marimba pulses, soft harp plucks, subtle magical question motif",
        sfx=["tiny magical twinkle", "soft footsteps", "distant stream"],
        ambience="quiet magical ambience with small mysterious details",
        voice_direction="curious and inviting narration, slightly slower on discoveries",
    ),
    "scared": AudioMood(
        music="very soft low strings, gentle suspense pad, child-safe tension only",
        sfx=["distant owl", "soft wind", "tiny branch creak"],
        ambience="mild suspenseful atmosphere, never horror, still safe for children",
        voice_direction="soft reassuring narration, careful pacing, not frightening",
    ),
    "hopeful": AudioMood(
        music="warm piano chords, rising soft strings, gentle bell highlights",
        sfx=["glowing shimmer", "soft breeze", "distant friendly birds"],
        ambience="open airy atmosphere with a feeling of possibility",
        voice_direction="encouraging, kind, emotionally warm narration",
    ),
    "excited": AudioMood(
        music="playful orchestral rhythm, bright xylophone accents, energetic strings",
        sfx=["happy sparkle burst", "quick footsteps", "little whoosh"],
        ambience="lively magical setting with cheerful movement",
        voice_direction="energetic but clear narration, joyful emphasis on action words",
    ),
    "sad": AudioMood(
        music="soft piano, gentle sustained strings, warm minor melody",
        sfx=["quiet wind", "soft water ripple", "small sigh-like ambience"],
        ambience="quiet emotional space with gentle sadness, still comforting",
        voice_direction="slow, tender narration with gentle empathy",
    ),
    "relieved": AudioMood(
        music="warm resolution chords, soft harp glissando, peaceful strings",
        sfx=["happy chime", "gentle breeze", "soft animal sounds"],
        ambience="calm safe atmosphere after the conflict resolves",
        voice_direction="relieved, peaceful narration with a smile",
    ),
    "determined": AudioMood(
        music="gentle heroic rhythm, warm brass pad, steady percussion very low",
        sfx=["firm footstep", "magic item glow", "soft rising whoosh"],
        ambience="focused heroic atmosphere, brave but child-friendly",
        voice_direction="confident narration, clear and inspiring tone",
    ),
}


def choose_audio_mood(emotion: str, rng: random.Random) -> AudioMood:
    """Return an audio mood for an emotion."""
    return AUDIO_MOODS.get(emotion.lower(), AUDIO_MOODS["happy"])
