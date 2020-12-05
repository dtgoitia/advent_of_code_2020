from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterator, List


def get_boarding_passes(path: Path) -> Iterator[str]:
    with path.open("r") as f:
        for line in f:
            yield line.strip()


def resolve(input_paths: List[Path]) -> Any:
    boarding_pass_input_path = input_paths[0]

    seat_ids: List[int] = []
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

    sorted_ids = sorted(seat_ids)
    amount = len(sorted_ids)

    i_range = [0, amount - 1]
    is_last_iteration = False
    while True:
        i_peek = (i_range[0] + i_range[1]) // 2  # middle of i_range
        peeked_id = sorted_ids[i_peek]
        expected_id = sorted_ids[0] + i_peek

        if peeked_id == expected_id:
            # range    0 1 2 3 4 5 6 (all OK so far)
            # expected 0 1 2 3 4 5 6
            # missing seat ID is after the peeked seat
            if is_last_iteration:
                seat_id = sorted_ids[i_peek] + 1
                break
            i_range[0] = i_peek
        else:
            # range    0 1 2 3|5 6 7 (missing ID on the left)
            # expected 0 1 2 3 4 5 6
            # missing seat ID is before the peeked seat
            if is_last_iteration:
                seat_id = sorted_ids[i_peek] - 1
                break
            i_range[1] = i_peek

        if i_range[0] + 1 == i_range[1]:
            is_last_iteration = True

    return seat_id
