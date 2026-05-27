# Example: generate odd numbers using a for-loop (same pattern, different predicate)


def generate_odds(limit: int) -> list[int]:
    result = []
    for n in range(1, limit + 1):
        if n % 2 != 0:
            result.append(n)
    return result


def main() -> None:
    odds = generate_odds(10)
    print(",".join(str(x) for x in odds))


if __name__ == "__main__":
    main()
