from __future__ import annotations

import re
from collections import Counter


_TOKEN_RE = re.compile(r"[A-Za-z]+")


def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
  tokens = [m.group(0).lower() for m in _TOKEN_RE.finditer(text)]
  counts = Counter(tokens)
  items = list(counts.items())
  items.sort(key=lambda t: (-t[1], t[0]))
  return items[:k]


def main() -> None:
  sample = "OK ok ERROR error warn ERROR ok error"
  top = most_common_tokens(sample, 3)
  for token, count in top:
    print(f"{token}={count}")


if __name__ == "__main__":
  main()
