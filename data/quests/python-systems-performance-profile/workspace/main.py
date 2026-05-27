from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"[A-Za-z]+")


def most_common_tokens(text: str, k: int) -> list[tuple[str, int]]:
    # TODO: extract all alphabetic sequences from text and lowercase them
    # TODO: count occurrences of each token
    # TODO: return the top-k as [(token, count)] sorted by count desc, then token asc
    raise NotImplementedError("TODO: implement most_common_tokens(text, k)")


def main() -> None:
    sample = "ok ok ERROR error warn error"
    top = most_common_tokens(sample, 3)
    for token, count in top:
        print(f"{token}={count}")


if __name__ == "__main__":
    main()
