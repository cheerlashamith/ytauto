"""
Standalone story scene generator for the story_mode engine.

This script can either:
  A) Call your local Ollama AI to generate a real story from the topic
  B) Use a fast template-based fallback if Ollama is not running

Usage:
  python generate_story_scenes.py --topic "A fox who learns honesty" --out scenes_story.json
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


def safe(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_") or "scene"


def _template_story(topic: str) -> dict:
    """Fast local template story. Used only when Ollama is not available."""
    subject = topic.strip()
    script = (
        f"Once upon a time, in a bright and friendly world, a little character learned an important lesson about {subject}.\n\n"
        "One sunny day, the character faced a small problem.\n\n"
        "The character had to make a choice.\n\n"
        "With courage and kindness, the character asked friends for help.\n\n"
        "Together, they found the right answer.\n\n"
        "In the end, everyone was happy because kindness made the world better."
    )
    defs = [
        ("Magical Beginning", "peaceful world", "main character appears", "warm morning"),
        ("Happy Day", "cheerful moment", "beautiful place", "playful mood"),
        ("A Surprise", "unexpected discovery", "curious moment", "soft magic"),
        ("Big Choice", "thinking carefully", "right or wrong", "emotional pause"),
        ("Asking Friends", "friendly helpers", "kind conversation", "community"),
        ("Right Decision", "brave choice", "honest action", "warm glow"),
        ("Happy Ending", "friends celebrate", "problem solved", "joyful scene"),
        ("Moral", "kindness wins", "trust grows", "peaceful ending"),
    ]
    scenes = []
    for i, (t, b1, b2, b3) in enumerate(defs, 1):
        scenes.append({
            "name": f"scene_{i:02d}_{safe(t)}",
            "title": t,
            "bullets": [b1, b2, b3],
            "prompt": (
                f"Vertical 9:16 premium children's storybook illustration for '{subject}', "
                f"scene: {t}, {b1}, {b2}, {b3}, adorable expressive characters, "
                f"cinematic soft lighting, colorful magical environment, warm emotional mood, "
                f"high quality cartoon animation style, no text, no letters, no captions, "
                f"no watermark, no logo."
            ),
            "narration": f"In this scene, {b1}, {b2}, {b3}.",
        })
    return {
        "render_mode": "story",
        "subject": subject,
        "keywords": "kids story, moral story, cartoon, bedtime story, children story, animated story",
        "moneyprinter_script": script,
        "scenes": scenes,
    }


def _ollama_story(topic: str, model: str = "qwen2.5:7b", url: str = "http://127.0.0.1:11434") -> dict:
    """Generate a story plan using the local Ollama AI."""
    if requests is None:
        raise RuntimeError("Python package 'requests' is not installed. Run: pip install requests")

    prompt = f"""You are an expert children's story writer and video planner. Create a warm, moral, age-appropriate story based on the topic below.

Topic: {topic}

Rules:
1. Create exactly 4-6 scenes: Beginning, Problem/Rising Action, Choice/Turning Point, Resolution, Happy Ending, Optional Moral Summary.
2. Each scene must have a title, a short 2-3 sentence narration, and a detailed vertical 9:16 image prompt for Stable Diffusion.
3. Image prompts must include: art style, characters, setting, emotion, lighting, color palette, and the rule: "no text, no letters, no numbers, no captions, no watermark, no UI elements".
4. Provide a full continuous voiceover script (moneyprinter_script) that tells the story aloud in 150-250 words. Use simple language suitable for ages 5-10.
5. Provide 8-12 comma-separated SEO keywords in the "keywords" field.
6. Return ONLY a valid JSON object. No markdown code fences, explanations, or  Süd reasoning tags.

Required JSON format:
{{
  "render_mode": "story",
  "subject": "{topic}",
  "keywords": "story, kids, moral, animation, ...",
  "moneyprinter_script": "Once upon a time...",
  "scenes": [
    {{
      "name": "scene_01_beginning",
      "title": "The Magical Beginning",
      "prompt": "Vertical 9:16 children's storybook illustration... no text, no watermark",
      "narration": "Once upon a time...",
      "bullets": ["point 1", "point 2", "point 3"]
    }}
  ]
}}

Generate the JSON now."""

    # Read configurable timeout
    try:
        config_path = Path(__file__).parent.parent.parent / "config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            timeout_val = json.load(f).get("brain_manager", {}).get("timeout_seconds", 900)
    except Exception:
        timeout_val = 900

    try:
        resp = requests.post(
            f"{url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "top_p": 0.9, "num_ctx": 4096},
            },
            timeout=timeout_val,
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Ollama is not running at {url}. Start it with: ollama serve")

    # Extract JSON from response
    text = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
    if "<think>" in text and "</think>" not in text:
        text = text.split("<think>")[0]
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    m = re.search(r"(\{.*\})", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            pass
    raise RuntimeError("Ollama returned a story, but we could not extract valid JSON from it.")


def _clean_story(plan: dict, topic: str) -> dict:
    """Ensure the story plan has all required fields."""
    plan.setdefault("render_mode", "story")
    plan.setdefault("subject", topic)
    kw = plan.get("keywords", "")
    if isinstance(kw, list):
        plan["keywords"] = ", ".join(kw)
    elif not isinstance(kw, str):
        plan["keywords"] = "kids story, moral story, cartoon, bedtime story"
    script = plan.get("moneyprinter_script", "")
    if isinstance(script, dict):
        script = script.get("full_voiceover") or "\n\n".join(script.get("paragraphs", []))
    plan["moneyprinter_script"] = str(script).strip()

    scenes = plan.get("scenes", [])
    if not isinstance(scenes, list):
        scenes = []
    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            scene = {}
            scenes[i] = scene
        scene.setdefault("name", f"scene_{i+1:02d}_{safe(scene.get('title', 'scene'))}")
        scene.setdefault("title", f"Scene {i+1}")
        scene.setdefault("bullets", [])
        if not isinstance(scene.get("bullets"), list):
            scene["bullets"] = []
        if not scene["bullets"]:
            scene["bullets"] = [f"Story moment: {scene['title']}"]
        scene.setdefault("narration", f"In this scene, {scene['title']}.")
        scene.setdefault("prompt", (
            f"Vertical 9:16 premium children's storybook illustration for '{topic}', "
            f"scene: {scene['title']}, adorable expressive characters, cinematic soft lighting, "
            f"colorful magical environment, no text, no letters, no captions, no watermark."
        ))
    plan["scenes"] = scenes
    return plan


def build(topic: str, use_ai: bool = True, model: str = "qwen2.5:7b", url: str = "http://127.0.0.1:11434") -> dict:
    """Build a story plan. Tries Ollama first, falls back to template only if AI is unavailable."""
    if use_ai:
        try:
            plan = _ollama_story(topic, model=model, url=url)
            return _clean_story(plan, topic)
        except RuntimeError as e:
            print(f"[WARNING] Ollama story generation failed: {e}", file=sys.stderr)
            print("[WARNING] Falling back to local template story. Start Ollama for AI-generated stories.", file=sys.stderr)
    return _template_story(topic)


def main():
    ap = argparse.ArgumentParser(description="Generate a story scene plan")
    ap.add_argument("--topic", required=True, help="Story topic, e.g. 'A fox who learns honesty'")
    ap.add_argument("--out", default="scenes_story.json", help="Output JSON file")
    ap.add_argument("--no-ai", action="store_true", help="Use local template instead of Ollama")
    ap.add_argument("--model", default="qwen2.5:7b", help="Ollama model name")
    ap.add_argument("--url", default="http://127.0.0.1:11434", help="Ollama base URL")
    args = ap.parse_args()

    plan = build(args.topic, use_ai=not args.no_ai, model=args.model, url=args.url)
    Path(args.out).write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {args.out} with {len(plan['scenes'])} scenes.")


if __name__ == "__main__":
    main()
