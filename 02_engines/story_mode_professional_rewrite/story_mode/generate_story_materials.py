"""Compatibility wrapper for existing downstream image pipeline.
This file expects scenes_story.json with scenes[].prompt or scenes[].image_prompt.
It does not add overlays in story mode.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--scenes',default='scenes_story.json')
    args=ap.parse_args()
    data=json.loads(Path(args.scenes).read_text(encoding='utf-8'))
    print('Story materials interface ready.')
    print('Scenes:', len(data.get('scenes',[])))
    print('Each scene contains prompt/image_prompt and negative_prompt for ComfyUI.')
    print('Use your existing ComfyUI generate_story_materials.py here if already working.')
if __name__=='__main__': main()
