from pathlib import PosixPath

import pytest

from .logic import resolve


@pytest.mark.parametrize(
    ("boarding_pass", "seat_id"),
    (
        ("FBFBBFFRLR", 357),
        ("BFFFBBFRRR", 567),
        ("FFFBBBFRRR", 119),
        ("BBFFBBFRLL", 820),
    ),
)
def test_resolve_seat_id(tmp_path: PosixPath, boarding_pass: str, seat_id: int) -> None:
    boarding_pass_input_path = tmp_path / "input_1_batch"
    boarding_pass_input_path.write_text(boarding_pass)

    result = resolve(input_paths=[boarding_pass_input_path])

    assert result == seat_id
