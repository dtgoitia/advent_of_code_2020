from puzzles.filesystem import get_input_path

from .logic import resolve


def main() -> None:
    input_path = get_input_path()

    result = resolve(input_path=input_path)

    print("Result:")
    print(result)


if __name__ == "__main__":
    main()
