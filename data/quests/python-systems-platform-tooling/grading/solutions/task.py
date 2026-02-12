from __future__ import annotations


_USAGE = "usage: tool greet --name NAME | tool sum A B"


def _print_usage() -> None:
  print(_USAGE)


def main(argv: list[str] | None = None) -> int:
  if argv is None:
    import sys
    argv = sys.argv[1:]

  if not argv or argv[0] in ("-h", "--help"):
    _print_usage()
    return 0

  cmd = argv[0]

  if cmd == "greet":
    if len(argv) == 3 and argv[1] == "--name":
      print(f"Hello, {argv[2]}!")
      return 0
    _print_usage()
    return 2

  if cmd == "sum":
    if len(argv) == 3:
      try:
        a = int(argv[1])
        b = int(argv[2])
      except ValueError:
        _print_usage()
        return 2
      print(f"a+b={a + b}")
      return 0
    _print_usage()
    return 2

  _print_usage()
  return 2


if __name__ == "__main__":
  raise SystemExit(main())
