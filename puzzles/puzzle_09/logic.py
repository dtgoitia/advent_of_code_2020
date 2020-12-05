from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterator, List


def get_boarding_passes(path: Path) -> Iterator[str]:
    with path.open("r") as f:
        for line in f:
            yield line.strip()


def resolve(input_paths: List[Path]) -> Any:
    boarding_pass_input_path = input_paths[0]

    seat_ids = []
    for boarding_pass in get_boarding_passes(boarding_pass_input_path):
        row_code, column_code = boarding_pass[:7], boarding_pass[7:]

        row_range = [0, 127]
        column_range = [0, 7]
        for i, (row_char, column_char) in enumerate(zip_longest(row_code, column_code)):
            row_span = 2 ** (7 - i - 1)
            if row_char == "F":
                row_range[1] -= row_span
            else:  # char == "B"
                row_range[0] += row_span

            if not column_char:
                continue

            column_span = 2 ** (3 - i - 1)
            if column_char == "L":
                column_range[1] -= column_span
            else:  # char == "B"
                column_range[0] += column_span

        row = row_range[0]
        column = column_range[0]

        seat_id = int(row * 8 + column)
        seat_ids.append(seat_id)

    return max(seat_ids)
