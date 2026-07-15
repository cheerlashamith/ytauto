"""Camera selection system for cinematic children's stories."""
from __future__ import annotations

import random
from typing import Dict, List
from .json_schema import CameraSpec
from .utils import choose

CAMERA_LIBRARY: Dict[str, CameraSpec] = {
    "wide": CameraSpec("Wide Shot", "24mm cinematic lens", "eye level", "character small within environment", "slow gentle dolly", "rule of thirds with strong foreground depth"),
    "medium": CameraSpec("Medium Shot", "35mm lens", "eye level", "waist-up character framing", "subtle push-in", "centered emotional storytelling composition"),
    "close": CameraSpec("Close-up", "50mm lens", "eye level", "face and expression fill frame", "still camera", "soft background bokeh, eyes on upper third"),
    "extreme_close": CameraSpec("Extreme Close-up", "85mm macro lens", "eye level", "eyes or magic item detail", "slow micro push", "intimate emotional focus"),
    "birds_eye": CameraSpec("Bird's Eye View", "28mm lens", "top down", "character within patterned environment", "floating overhead drift", "geometric composition"),
    "low_angle": CameraSpec("Low Angle", "32mm lens", "low angle", "character appears brave and heroic", "slow upward tilt", "dramatic foreground framing"),
    "high_angle": CameraSpec("High Angle", "35mm lens", "high angle", "character appears small or uncertain", "gentle downward tilt", "protective storybook framing"),
    "tracking": CameraSpec("Tracking Shot", "35mm lens", "eye level", "character moving through scene", "smooth side tracking", "leading lines guide the eye"),
    "over_shoulder": CameraSpec("Over Shoulder", "50mm lens", "over shoulder", "viewer sees what character sees", "subtle handheld-like drift", "foreground shoulder silhouette"),
    "dutch": CameraSpec("Dutch Angle", "35mm lens", "slightly tilted", "moment of confusion or danger", "slow stabilizing motion", "diagonal tension composition"),
}


def choose_camera(emotion: str, action: str, rng: random.Random) -> CameraSpec:
    text = f"{emotion} {action}".lower()
    if any(k in text for k in ["discover", "arrive", "kingdom", "forest", "journey"]):
        return CAMERA_LIBRARY["wide"]
    if any(k in text for k in ["sad", "afraid", "scared", "worried", "tear"]):
        return CAMERA_LIBRARY["close"]
    if any(k in text for k in ["brave", "climb", "dragon", "hero", "protect"]):
        return CAMERA_LIBRARY["low_angle"]
    if any(k in text for k in ["confused", "mystery", "lost"]):
        return CAMERA_LIBRARY["dutch"]
    if any(k in text for k in ["run", "follow", "chase", "walk"]):
        return CAMERA_LIBRARY["tracking"]
    if any(k in text for k in ["look", "see", "watch"]):
        return CAMERA_LIBRARY["over_shoulder"]
    return choose(rng, [CAMERA_LIBRARY["medium"], CAMERA_LIBRARY["wide"], CAMERA_LIBRARY["close"]])
