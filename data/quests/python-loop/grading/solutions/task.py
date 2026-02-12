from __future__ import annotations


def generate_evens(limit: int) -> list[int]:
  out: list[int] = []
  n = 2
  while n <= limit:
    out.append(n)
    n += 2
  return out


def main() -> None:
  evens = generate_evens(10)
  print(",".join(str(x) for x in evens))


if __name__ == "__main__":
  main()
