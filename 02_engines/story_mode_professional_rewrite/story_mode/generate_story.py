"""CLI entry point for professional story generation."""
from __future__ import annotations
import argparse
from .config import StoryConfig, DEFAULT_STYLE_ALIASES
from .utils import make_rng, save_json
from .character_generator import generate_character
from .world_generator import generate_world
from .story_generator import build_story
from .scene_generator import generate_scenes
from .json_schema import StoryPackage
from .validators import validate_story_package

def generate(topic: str, cfg: StoryConfig) -> StoryPackage:
    rng=make_rng(cfg.seed)
    style_key=DEFAULT_STYLE_ALIASES.get(cfg.quality_preset.lower(), cfg.quality_preset)
    cfg.quality_preset=style_key
    character=generate_character(topic,rng)
    world=generate_world(topic,rng)
    title,logline,moral,beats,full_story=build_story(topic,character,world,rng)
    scenes=generate_scenes(topic,beats,character,world,cfg,rng)
    keywords=', '.join([topic,'kids story','moral story','cartoon','storybook','children video',world.environment_type,character.species])
    return StoryPackage(subject=topic,story_title=title,logline=logline,moral=moral,full_story=full_story,keywords=keywords,character_sheet=character,world_sheet=world,scenes=scenes)

def main():
    ap=argparse.ArgumentParser(description='Generate professional dynamic kids story scenes JSON')
    ap.add_argument('--topic',required=True)
    ap.add_argument('--out',default='scenes_story.json')
    ap.add_argument('--style',default='pixar')
    ap.add_argument('--seed',type=int,default=None)
    args=ap.parse_args()
    cfg=StoryConfig(output_path=args.out,quality_preset=args.style,seed=args.seed)
    pkg=generate(args.topic,cfg)
    errors=validate_story_package(pkg)
    if errors:
        print('Validation warnings:'); [print('-',e) for e in errors]
    save_json(args.out,pkg.to_output_dict(cfg.include_legacy_prompt_key))
    print(f'Saved professional story JSON: {args.out}')
if __name__=='__main__': main()
