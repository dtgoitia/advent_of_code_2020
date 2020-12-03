from pathlib import Path
from typing import Any, List, NewType

import attr

RawSlope = str


# def read_all_entries(path: Path) -> List[RawSlope]:
#     with path.open() as f:
#         content = [line.strip() for line in f.readlines()]

#     return content


@attr.s(auto_attribs=True, frozen=True)
class Slope:
    right: int
    down: int


def parse_slope(slope_spec: RawSlope) -> Slope:
    raw_right, raw_down = slope_spec.split(", ")

    right = raw_right.split(" ")[1]
    down = raw_down.split(" ")[1]

    slope = Slope(right=int(right), down=int(down))
    return slope


MapPatternRow = NewType("MapPatternRow", str)
MapPattern = NewType("MapPattern", List[MapPatternRow])


@attr.s(auto_attribs=True, frozen=True)
class Position:
    row: int  # 0-based index
    column: int  # 0-based index


TREE = "#"
NO_TREE = "."


class Map:
    def __init__(self, pattern: str) -> None:
        rows = [MapPatternRow(row.strip()) for row in pattern.strip().split("\n")]
        map_pattern = MapPattern(rows)
        self.pattern = map_pattern

    @property
    def row_amount(self) -> int:
        return len(self.pattern)

    @property
    def pattern_width(self) -> int:
        any_row = self.pattern[0]
        return len(any_row)

    def has_tree(self, position: Position) -> bool:
        # a slope might cover the width of the map mattern multiple times

        # column from the left edge of the last horizontally repeated pattern
        if position.column >= self.pattern_width:
            column = position.column % self.pattern_width
        else:
            column = position.column

        map_value = self.pattern[position.row][column]

        return map_value == TREE


def is_position_inside_map(map: Map, position: Position) -> bool:
    return 0 <= position.row < map.row_amount


@attr.s(auto_attribs=True, frozen=True)
class Step:
    position: Position
    has_tree: bool


def slide(map: Map, starting_position: Position, slope: Slope) -> Position:
    next_position = Position(
        row=starting_position.row + slope.down,
        column=starting_position.column + slope.right,
    )

    return next_position


def traverse_map(map: Map, slope: Slope) -> List[Step]:
    starting_position = Position(row=0, column=0)
    starting_step = Step(
        position=starting_position,
        has_tree=map.has_tree(position=starting_position),
    )

    path: List[Step] = [starting_step]

    last_position = starting_position

    is_inside_map = True
    while is_inside_map:
        current_position = slide(map=map, starting_position=last_position, slope=slope)
        last_position = current_position

        is_inside_map = is_position_inside_map(map=map, position=current_position)

        if not is_inside_map:
            break

        has_tree = map.has_tree(position=current_position)

        step = Step(position=current_position, has_tree=has_tree)
        path.append(step)

    return path


def read_map(path: Path) -> Map:
    pattern = path.read_text().strip()
    map = Map(pattern=pattern)
    return map


def read_specs(path: Path) -> List[str]:
    specs = [spec.strip() for spec in path.read_text().strip().split("\n")]
    return specs


def resolve(input_paths: List[Path]) -> Any:
    map_path, specs_path = input_paths

    map = read_map(map_path)
    specs = read_specs(specs_path)

    result = 1
    for slope_spec in specs:
        slope = parse_slope(slope_spec=slope_spec)

        path = traverse_map(map=map, slope=slope)
        tree_amount = sum(1 for step in path if step.has_tree)
        result = result * tree_amount

    return result
