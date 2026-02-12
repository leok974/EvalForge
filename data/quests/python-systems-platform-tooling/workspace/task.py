"""
Quest: python-systems-platform-tooling

Build a tiny deterministic CLI (no sys.exit).

Implement:
- main(argv=None) -> int
Commands:
1) greet --name <NAME>
   prints: Hello, <NAME>!
2) sum <A> <B>
   prints: a+b=<SUM>   (A and B are integers)
Errors:
- return 2 on invalid args
- print a one-line usage string on errors or --help:
    usage: tool greet --name NAME | tool sum A B
"""

from __future__ import annotations


def main(argv: list[str] | None = None) -> int:
  raise NotImplementedError("TODO: implement main(argv)")


if __name__ == "__main__":
  raise SystemExit(main())
