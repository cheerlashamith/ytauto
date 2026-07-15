"""Professional style presets for image prompt generation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True, slots=True)
class QualityPreset:
    name: str
    render_style: str
    texture_style: str
    character_style: str
    color_style: str
    quality_terms: str


PRESETS: Dict[str, QualityPreset] = {
    "pixar": QualityPreset(
        name="Pixar-inspired 3D Animation",
        render_style="premium 3D animated feature film look, expressive appealing shapes, cinematic depth",
        texture_style="soft tactile materials, rounded forms, clean surfaces, detailed fur and fabric textures",
        character_style="large expressive eyes, charming proportions, readable emotions, child friendly design",
        color_style="warm saturated palette with tasteful contrast, magical highlights and gentle gradients",
        quality_terms="high quality, ultra detailed, polished animation still, global illumination, soft shadows, HDR, cinematic composition",
    ),
    "disney": QualityPreset(
        name="Disney-like Fairytale Animation",
        render_style="classic fairytale animation mood, elegant character staging, magical storytelling atmosphere",
        texture_style="smooth painterly 3D surfaces with delicate storybook details",
        character_style="friendly heroic silhouette, expressive face, graceful pose language",
        color_style="warm golden highlights, dreamy pastels, royal storybook colors",
        quality_terms="feature animation quality, enchanting lighting, rich details, emotional clarity, cinematic framing",
    ),
    "dreamworks": QualityPreset(
        name="DreamWorks-style Adventure Animation",
        render_style="energetic adventure animation, dynamic poses, playful cinematic staging",
        texture_style="crisp stylized materials, detailed environments, strong silhouette readability",
        character_style="expressive comedic face, confident body language, lively appeal",
        color_style="bold colorful palette, dramatic rim light, vibrant atmosphere",
        quality_terms="professional animation still, dynamic composition, high detail, volumetric lighting, polished render",
    ),
    "studio_ghibli": QualityPreset(
        name="Studio Ghibli-inspired Storybook Painting",
        render_style="hand-painted animated film background, poetic magical realism, gentle emotional atmosphere",
        texture_style="watercolor-like brush textures, lush natural details, organic imperfections",
        character_style="soft expressive face, simple sincere design, natural movement pose",
        color_style="earthy greens, warm sunlight, soft sky colors, nostalgic ambience",
        quality_terms="beautiful hand-painted look, detailed background, soft light, atmospheric depth, whimsical charm",
    ),
    "storybook": QualityPreset(
        name="Premium Children's Storybook",
        render_style="luxury illustrated children's book spread, cinematic storybook composition",
        texture_style="soft paper texture, painterly brushwork, crisp character edges",
        character_style="adorable expressive child-friendly character, clear emotional acting",
        color_style="warm cream highlights, pastel accents, cozy magical palette",
        quality_terms="award-winning children's book illustration, high detail, beautiful composition, soft shadows, enchanting mood",
    ),
    "watercolor": QualityPreset(
        name="Watercolor Fairytale",
        render_style="delicate watercolor story illustration, airy and dreamy atmosphere",
        texture_style="visible watercolor wash, paper grain, soft pigment edges",
        character_style="gentle expressive character with simple readable features",
        color_style="transparent layered colors, soft blues, greens, golds and pinks",
        quality_terms="fine art watercolor, charming details, luminous atmosphere, gentle shadows, storybook quality",
    ),
    "anime": QualityPreset(
        name="Wholesome Anime Fantasy",
        render_style="clean wholesome anime film still, expressive character acting, detailed fantasy background",
        texture_style="crisp linework, soft cel shading, subtle painterly background",
        character_style="large expressive eyes, emotional pose, cute heroic silhouette",
        color_style="vibrant but gentle palette, glowing highlights, magical atmosphere",
        quality_terms="high quality anime movie frame, cinematic lighting, detailed environment, clean composition",
    ),
    "clay_animation": QualityPreset(
        name="Clay Animation",
        render_style="stop-motion clay animation look, handcrafted miniature world, tactile charm",
        texture_style="visible clay texture, handmade props, tiny fabric and paper details",
        character_style="cute clay character with expressive eyes and handmade costume",
        color_style="warm studio lighting, cozy colorful miniature set palette",
        quality_terms="professional stop motion still, tactile detail, soft shadows, miniature depth of field",
    ),
}


def get_preset(name: str) -> QualityPreset:
    return PRESETS.get(name.lower().strip(), PRESETS["pixar"])
