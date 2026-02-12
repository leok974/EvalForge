"""
Quest: python-loop

Implement a simple loop-based generator.

Requirements:
- Implement generate_evens(limit) using a loop.
- generate_evens(limit) returns even integers from 2..limit inclusive.
- Implement main() to print the evens for limit=10 as comma-separated values:
  "2,4,6,8,10"
"""

from __future__ import annotations


def generate_evens(limit: int) -> list[int]:
  """Return all even numbers from 2..limit inclusive."""
  raise NotImplementedError("TODO: implement generate_evens(limit)")


def main() -> None:
  evens = generate_evens(10)
  print(",".join(str(x) for x in evens))


if __name__ == "__main__":
  main()
