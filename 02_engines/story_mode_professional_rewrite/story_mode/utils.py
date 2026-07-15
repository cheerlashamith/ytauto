"""Utility helpers for deterministic, varied story generation."""
from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Iterable, List, Sequence, TypeVar

T = TypeVar("T")


def make_rng(seed: int | None = None) -> random.Random:
    return random.Random(seed)


def choose(rng: random.Random, values: Sequence[T]) -> T:
    if not values:
        raise ValueError("Cannot choose from an empty sequence")
    return values[rng.randrange(len(values))]


def choose_many(rng: random.Random, values: Sequence[T], count: int) -> List[T]:
    if count <= 0:
        return []
    if count >= len(values):
        copy = list(values)
        rng.shuffle(copy)
        return copy
    return rng.sample(list(values), count)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "story"


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def save_json(path: str | Path, data: object) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def sentence_join(parts: Iterable[str]) -> str:
    cleaned = [p.strip() for p in parts if p and p.strip()]
    return " ".join(cleaned)


def clamp_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(" ,.;:") + "."


def expand_to_min_words(base: str, additions: Sequence[str], min_words: int) -> str:
    text = base.strip()
    i = 0
    while word_count(text) < min_words and additions:
        text += " " + additions[i % len(additions)].strip()
        i += 1
    return text
