# Professional Story Mode Architecture

## 1. Purpose

This rewrite replaces the old hardcoded story generator with a modular pipeline.
The downstream image generation pipeline can continue reading `scene["prompt"]`,
but the prompts are now generated through character, world, camera, lighting,
emotion, environment, quality, and negative prompt systems.

## 2. Pipeline

```text
User topic
  -> generate_story.py
  -> story_generator.py
  -> character_generator.py
  -> world_generator.py
  -> scene_generator.py
  -> prompt_generator.py
  -> scenes_story.json
  -> existing generate_story_materials.py
  -> ComfyUI
  -> clips
```

## 3. Main modules

- `config.py`: runtime options.
- `json_schema.py`: dataclasses and output schema.
- `character_generator.py`: persistent character sheet.
- `world_generator.py`: persistent world sheet.
- `story_generator.py`: unique story arc.
- `scene_generator.py`: dynamic scene list.
- `prompt_generator.py`: 250-500 word professional prompts.
- `camera_system.py`: camera language.
- `lighting_system.py`: cinematic lighting.
- `emotion_system.py`: expression and pose control.
- `environment_system.py`: reusable world environments.
- `quality_presets.py`: Pixar, Disney, DreamWorks, Ghibli, Storybook, Anime, Watercolor, Clay.
- `negative_prompt.py`: clean negative prompt.
- `validators.py`: quality checks.
- `storyboard.py`: storyboard preview.

## 4. Character consistency

Every generated story has a `character_sheet`. The prompt generator repeats
identity details in every prompt: name, species, hair/fur, eyes, clothes,
accessories, signature colors, magic item, face and body.

## 5. World consistency

Every story has a `world_sheet` containing the kingdom, environment, weather,
plants, animals, magic rules, lore, palette and recurring landmarks.

## 6. Prompt quality

Each prompt includes:

- main character
- face, eyes, expression, pose
- clothes and accessories
- magic item
- environment foreground/midground/background
- camera language
- lighting language
- mood and colors
- rendering style
- quality terms
- negative text rule

## 7. Compatibility

Every scene includes both:

```json
"image_prompt": "...",
"prompt": "..."
```

The `prompt` key is kept for your existing ComfyUI pipeline.
