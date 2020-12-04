from pathlib import PosixPath
from textwrap import dedent

from .logic import Map, Position, Slope, Step, parse_slope, resolve, traverse_map


def test_parse_slope():
    slope_spec = "right 3, down 1"
    slope = parse_slope(slope_spec)
    assert slope == Slope(right=3, down=1)


def test_traverse_map():
    map_pattern = dedent(
        """
        ..##.......
        #...#...#..
        .#....#..#.
        ..#.#...#.#
        .#...##..#.
        ..#.##.....
        .#.#.#....#
        .#........#
        #.##...#...
        #...##....#
        .#..#...#.#
        """.strip()
    )
    slope_spec = "right 3, down 1"

    map = Map(pattern=map_pattern)
    slope = parse_slope(slope_spec=slope_spec)

    path = traverse_map(map=map, slope=slope)

    assert path == [
        Step(position=Position(row=0, column=0), has_tree=False),
        Step(position=Position(row=1, column=3), has_tree=False),
        Step(position=Position(row=2, column=6), has_tree=True),
        Step(position=Position(row=3, column=9), has_tree=False),
        Step(position=Position(row=4, column=12), has_tree=True),
        Step(position=Position(row=5, column=15), has_tree=True),
        Step(position=Position(row=6, column=18), has_tree=False),
        Step(position=Position(row=7, column=21), has_tree=True),
        Step(position=Position(row=8, column=24), has_tree=True),
        Step(position=Position(row=9, column=27), has_tree=True),
        Step(position=Position(row=10, column=30), has_tree=True),
    ]

    tree_amount = sum(1 for step in path if step.has_tree)

    assert tree_amount == 7


def test_resolve(tmp_path: PosixPath) -> None:
    map_input_path = tmp_path / "input_1_map"
    map_input_path.write_text(
        dedent(
            """
            ..##.......
            #...#...#..
            .#....#..#.
            ..#.#...#.#
            .#...##..#.
            ..#.##.....
            .#.#.#....#
            .#........#
            #.##...#...
            #...##....#
            .#..#...#.#
            """.strip()
        )
    )

    spec_input_path = tmp_path / "input_2_spec"
    spec_input_path.write_text("right 3, down 1\n")

    result = resolve(
        input_paths=[
            map_input_path,
            spec_input_path,
        ]
    )

    assert result == 7
