from puzzles.filesystem import get_input_paths

from .logic import resolve


def main() -> None:
    input_paths = get_input_paths()

    result = resolve(input_paths=input_paths)

    print("Result:")
    print(result)


if __name__ == "__main__":
    main()
