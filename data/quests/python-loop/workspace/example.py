def main() -> None:
    even_numbers = [n for n in range(1, 11) if n % 2 == 0]
    for n in even_numbers:
        print(n)
    print(f"EVEN_COUNT={len(even_numbers)}")


if __name__ == "__main__":
    main()
