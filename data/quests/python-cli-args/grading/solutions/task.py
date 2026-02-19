import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("--count", type=int, default=1, help="number of times to repeat")
    
    args = parser.parse_args()
    
    if args.count < 0:
        print("Count cannot be negative", file=sys.stderr)
        sys.exit(1)
        
    for i in range(args.count):
        if args.verbose:
            print(f"Processing {i+1}/{args.count}...")
        print("Hello World")

if __name__ == '__main__':
    main()
