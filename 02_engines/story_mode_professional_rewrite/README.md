# Professional Story Mode Rewrite

This is a complete modular rewrite of the kids story generation pipeline.

## Run

```bash
python -m story_mode.generate_story --topic "A fairy learns honesty" --out scenes_story.json --style pixar
```

## Output

`scenes_story.json` contains:

- render_mode
- subject
- story_title
- full_story
- character_sheet
- world_sheet
- scenes[]
  - title
  - narration
  - emotion
  - camera
  - lighting
  - environment
  - music
  - sfx
  - image_prompt
  - negative_prompt
  - prompt legacy key for existing ComfyUI pipeline

## Compatibility

Downstream code can continue reading:

```python
scene["prompt"]
```

because every scene also includes the legacy `prompt` key.
