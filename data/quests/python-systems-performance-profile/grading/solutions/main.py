from __future__ import annotations
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[A-Za-z]+")


def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
    tokens = [m.lower() for m in _TOKEN_RE.findall(text)]
    counts = Counter(tokens)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


def main() -> None:
    sample = "ok ok ERROR error warn error"
    top = most_common_tokens(sample, 3)
    for token, count in top:
        print(f"{token}={count}")


if __name__ == "__main__":
    main()
