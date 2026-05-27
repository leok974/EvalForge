def generate_evens(limit: int) -> list[int]:
    # TODO: use a for-loop to collect even integers from 2 to limit (inclusive)
    pass


def main() -> None:
    evens = generate_evens(10)
    print(",".join(str(x) for x in evens))


if __name__ == "__main__":
    main()
