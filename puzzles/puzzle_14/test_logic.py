from pathlib import PosixPath
from textwrap import dedent

import pytest

from .logic import resolve


@pytest.mark.parametrize(
    ("input", "expected_result"),
    (
        pytest.param(
            dedent(
                """
                shiny gold bags contain 2 dark red bags.
                dark red bags contain 2 dark orange bags.
                dark orange bags contain 2 dark yellow bags.
                dark yellow bags contain 2 dark green bags.
                dark green bags contain 2 dark blue bags.
                dark blue bags contain 2 dark violet bags.
                dark violet bags contain no other bags.
                """
            ).strip(),
            126,
            id="example_1",
        ),
        pytest.param(
            dedent(
                """
                shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
                faded blue bags contain no other bags.
                dotted black bags contain no other bags.
                vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
                dark olive bags contain 3 faded blue bags, 4 dotted black bags.
                """
            ).strip(),
            32,
            id="example_2",
        ),
    ),
)
def test_resolve(tmp_path: PosixPath, input: str, expected_result: int) -> None:
    forms_input_path = tmp_path / "input_1_forms"
    forms_input_path.write_text(input)

    result = resolve(input_paths=[forms_input_path])

    assert result == expected_result
