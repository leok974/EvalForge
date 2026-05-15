import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Example CLI tool")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    if args.count < 0:
        print("error: --count must be >= 0", file=sys.stderr)
        sys.exit(1)
    if args.verbose:
        print(f"Running {args.count} time(s)")

if __name__ == "__main__":
    main()
