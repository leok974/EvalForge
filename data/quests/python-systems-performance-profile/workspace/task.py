"""
Quest: python-systems-performance-profile

Implement a fast "top-k tokens" function.

Rules:
- Tokenize by extracting contiguous alphabetic sequences (A-Z/a-z).
- Lowercase tokens.
- most_common_tokens(text, k) -> list[(token, count)] sorted:
    1) count desc
    2) token asc
- main() prints the top 3 tokens for the provided sample text:
    error=3
    ok=2
    warn=1
"""

from __future__ import annotations

import re


_TOKEN_RE = re.compile(r"[A-Za-z]+")


def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
  raise NotImplementedError("TODO: implement most_common_tokens(text, k)")


def main() -> None:
  sample = "OK ok ERROR error warn ERROR ok error"
  top = most_common_tokens(sample, 3)
  for token, count in top:
    print(f"{token}={count}")


if __name__ == "__main__":
  main()
