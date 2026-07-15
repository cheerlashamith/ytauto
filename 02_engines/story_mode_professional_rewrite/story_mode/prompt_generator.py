"""Professional 250-500 word prompt generator."""
from __future__ import annotations

from .json_schema import CharacterProfile, WorldProfile, CameraSpec, LightingSpec, EnvironmentSpec
from .emotion_system import get_pose
from .quality_presets import QualityPreset
from .utils import expand_to_min_words, clamp_words

DETAIL_EXPANSIONS = [
    "The image should feel like a single polished frame from a premium animated children's film, with clear staging and instantly readable emotion.",
    "Keep the character identity consistent across the entire story, especially the face, eyes, clothing, accessory, color palette and magic item.",
    "The environment should look rich but not cluttered, with foreground, midground and background layers guiding the eye toward the main action.",
    "The mood should be safe, warm, magical and child-friendly, avoiding scary or uncanny details.",
    "Use cinematic depth, soft atmospheric perspective, detailed textures and expressive body language.",
    "Do not include written text, captions, logos, watermarks, speech bubbles, signs or readable letters inside the image.",
]

def build_image_prompt(
    *,
    scene_title: str,
    narration: str,
    action: str,
    emotion: str,
    character: CharacterProfile,
    world: WorldProfile,
    environment: EnvironmentSpec,
    camera: CameraSpec,
    lighting: LightingSpec,
    preset: QualityPreset,
    target_min_words: int = 250,
    target_max_words: int = 500,
    aspect: str = "vertical 9:16",
) -> str:
    pose = get_pose(emotion)
    base = (
        f"Create a {aspect} children's story illustration for the scene titled '{scene_title}'. "
        f"Story moment: {narration} Visual action: {action}. "
        f"{character.to_prompt_block()} In this scene, {character.name} feels {emotion}; show {pose.facial_expression}, {pose.body_pose}, "
        f"{pose.eye_direction}, and {pose.gesture}. "
        f"{world.to_prompt_block()} Current environment: {environment.name}. Foreground details: {environment.foreground}. "
        f"Midground details: {environment.midground}. Background details: {environment.background}. Weather: {environment.weather}. "
        f"Particles and atmosphere: {environment.particles}. Textures: {environment.textures}. Color mood: {environment.color_mood}. "
        f"Camera language: {camera.shot_type}, {camera.lens}, {camera.angle}, {camera.framing}, {camera.movement}, {camera.composition}. "
        f"Lighting: {lighting.lighting_type}, {lighting.key_light}, {lighting.fill_light}, {lighting.shadows}, {lighting.atmosphere}, {lighting.render_notes}. "
        f"Rendering style: {preset.name}; {preset.render_style}; {preset.texture_style}; {preset.character_style}; {preset.color_style}. "
        f"Quality: {preset.quality_terms}. Composition should use layered depth, appealing silhouettes, rule of thirds, cinematic framing and a clear focal point. "
        f"Make the scene emotionally readable for children, magical, wholesome, polished and visually consistent with the rest of the story. "
        f"No text, no letters, no captions, no watermark, no logo."
    )
    expanded = expand_to_min_words(base, DETAIL_EXPANSIONS, target_min_words)
    return clamp_words(expanded, target_max_words)
