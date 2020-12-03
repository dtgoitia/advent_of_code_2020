from pathlib import Path, PosixPath
from textwrap import dedent

import pytest

from .logic import is_valid_entry, parse_entry, resolve


@pytest.fixture
def sample_input_path(tmp_path: PosixPath) -> Path:
    path = tmp_path / "sample_input"
    path.write_text(
        dedent(
            """
            1-3 a: abcde
            1-3 b: cdefg
            2-9 c: ccccccccc
            """.strip()
        )
    )

    return path


@pytest.mark.parametrize(
    ("raw_entry", "is_valid"),
    (
        ("1-3 a: abcde", True),
        ("1-3 b: cdefg", False),
        ("2-9 c: ccccccccc", False),
    ),
)
def test_is_valid_entry(raw_entry, is_valid):
    entry = parse_entry(raw_entry)
    assert is_valid_entry(entry) is is_valid


def test_resolve(sample_input_path):
    result = resolve(input_paths=[sample_input_path])

    assert result == 1
