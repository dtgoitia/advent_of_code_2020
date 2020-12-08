from pathlib import PosixPath
from textwrap import dedent

from .logic import resolve


def test_resolve(tmp_path: PosixPath) -> None:
    program_input_path = tmp_path / "input_1_forms"
    program_input_path.write_text(
        dedent(
            """
            nop +0
            acc +1
            jmp +4
            acc +3
            jmp -3
            acc -99
            acc +1
            jmp -4
            acc +6
            """
        ).strip()
    )

    result = resolve(input_paths=[program_input_path])

    assert result == 5
