"""Emotion state system for consistent facial expression and posing."""
from __future__ import annotations

from dataclasses import dataclass
import random
from .utils import choose

EMOTIONS = ["happy", "curious", "scared", "hopeful", "excited", "sad", "relieved", "determined", "surprised", "proud"]

@dataclass(frozen=True, slots=True)
class EmotionPose:
    emotion: str
    facial_expression: str
    body_pose: str
    eye_direction: str
    gesture: str

POSES = {
    "happy": EmotionPose("happy", "bright smile, relaxed cheeks", "open welcoming posture", "looking warmly at friend", "small joyful wave"),
    "curious": EmotionPose("curious", "wide attentive eyes, slight smile", "leaning forward", "looking at mysterious object", "one hand near chin"),
    "scared": EmotionPose("scared", "wide eyes, tiny worried mouth", "shoulders raised", "looking toward danger", "hands held close to chest"),
    "hopeful": EmotionPose("hopeful", "soft smile and shining eyes", "standing upright", "looking toward light", "hands gently clasped"),
    "excited": EmotionPose("excited", "big sparkling smile", "bouncing energetic pose", "eyes focused forward", "arms lifted happily"),
    "sad": EmotionPose("sad", "downturned mouth and soft eyes", "slumped posture", "looking downward", "hands lowered"),
    "relieved": EmotionPose("relieved", "gentle relaxed smile", "shoulders soft", "looking at helper", "hand over heart"),
    "determined": EmotionPose("determined", "focused eyes and firm mouth", "heroic stance", "looking ahead", "one hand holding magic item"),
    "surprised": EmotionPose("surprised", "round eyes and open mouth", "leaning back slightly", "looking at discovery", "hands lifted"),
    "proud": EmotionPose("proud", "confident smile", "upright posture", "looking at friends", "hand on chest"),
}

def get_pose(emotion: str) -> EmotionPose:
    return POSES.get(emotion.lower(), POSES["happy"])

def choose_emotion(stage: str, rng: random.Random) -> str:
    stage = stage.lower()
    if "begin" in stage or "intro" in stage: return choose(rng, ["happy", "curious"])
    if "conflict" in stage: return choose(rng, ["scared", "sad", "surprised"])
    if "rising" in stage: return choose(rng, ["determined", "hopeful", "curious"])
    if "climax" in stage: return choose(rng, ["determined", "excited"])
    if "resolution" in stage: return choose(rng, ["relieved", "proud", "happy"])
    return choose(rng, EMOTIONS)
