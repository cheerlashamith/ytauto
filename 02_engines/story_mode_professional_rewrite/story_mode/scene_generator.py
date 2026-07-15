"""Dynamic scene generator."""
from __future__ import annotations

import random
from .camera_system import choose_camera
from .lighting_system import choose_lighting
from .emotion_system import choose_emotion
from .environment_system import build_environment_spec
from .negative_prompt import build_negative_prompt
from .prompt_generator import build_image_prompt
from .quality_presets import get_preset
from .sound_music_system import choose_audio_mood
from .json_schema import SceneSpec, CharacterProfile, WorldProfile

TRANSITIONS = ["soft dissolve", "gentle fade", "storybook page turn", "slow magical shimmer", "warm crossfade"]
MUSIC = ["soft magical orchestral music", "gentle bedtime bells", "warm whimsical strings", "light piano with soft celesta", "playful woodwinds"]
SFX = ["soft wind", "tiny sparkles", "gentle footsteps", "distant birds", "leaf rustle", "soft magical chime"]

def generate_scenes(topic, beats, character: CharacterProfile, world: WorldProfile, cfg, rng: random.Random) -> list[SceneSpec]:
    preset = get_preset(cfg.quality_preset)
    scenes=[]
    for idx, beat in enumerate(beats, start=1):
        stage=beat['stage']; summary=beat['summary']; emotion=choose_emotion(stage, rng)
        env=build_environment_spec(world.environment_type)
        camera=choose_camera(emotion, summary, rng)
        lighting=choose_lighting(emotion, world.environment_type, rng)
        title=f"{stage}: {topic.title()}" if idx==1 else stage
        narration=summary
        action=f"{character.name} is shown during the {stage.lower()} of the story, acting out the key moment with clear body language."
        prompt=build_image_prompt(scene_title=title,narration=narration,action=action,emotion=emotion,character=character,world=world,environment=env,camera=camera,lighting=lighting,preset=preset,target_min_words=cfg.target_prompt_min_words,target_max_words=cfg.target_prompt_max_words,aspect=cfg.image_aspect)
        audio_mood = choose_audio_mood(emotion, rng)
        scenes.append(SceneSpec(
            scene_number=idx, title=title, narration=narration, emotion=emotion, environment=world.environment_type,
            characters=[character.name], objects=[character.magic_item], action=action, camera=camera, lighting=lighting,
            environment_details=env, mood=f"{emotion}, magical, child-safe, cinematic", duration=cfg.default_scene_duration,
            transition=rng.choice(TRANSITIONS), music=audio_mood.music, sfx=audio_mood.sfx,
            image_prompt=prompt, negative_prompt=build_negative_prompt()
        ))
    return scenes
