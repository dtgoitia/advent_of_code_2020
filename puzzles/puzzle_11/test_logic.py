from pathlib import PosixPath
from textwrap import dedent

from .logic import resolve


def test_resolve(tmp_path: PosixPath) -> None:
    # 1 person per line
    # groups split by empty line

    forms_input_path = tmp_path / "input_1_forms"
    forms_input_path.write_text(
        dedent(
            """
            abc

            a
            b
            c

            ab
            ac

            a
            a
            a
            a

            b
            """
        ).strip()
    )

    result = resolve(input_paths=[forms_input_path])

    assert result == 11
