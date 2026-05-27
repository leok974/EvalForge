from __future__ import annotations

import re
from collections import Counter

# Example: count word frequencies in a string (same idea, simpler approach).
# Your task requires alphabetic-only tokenisation and a specific sort order.

_WORD_RE = re.compile(r"\b\w+\b")


def word_frequencies(text: str) -> dict[str, int]:
    """Return a {word: count} mapping for all words in text (lowercased)."""
    words = _WORD_RE.findall(text.lower())
    return dict(Counter(words))


def top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the n most-frequent entries, sorted by count desc then key asc."""
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


# Usage:
# text = "the quick brown fox jumps over the lazy dog the fox"
# freq = word_frequencies(text)
# print(top_n(freq, 3))  # [('the', 3), ('fox', 2), ('brown', 1)]
