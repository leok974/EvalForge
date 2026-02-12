def main() -> None:
    # Print even numbers from 1..10 inclusive, each on its own line.
    count = 0
    for i in range(1, 11):
        if i % 2 == 0:
            print(i)
            count += 1
    # Then print the summary line: EVEN_COUNT=5
    print(f"EVEN_COUNT={count}")

if __name__ == "__main__":
    main()
