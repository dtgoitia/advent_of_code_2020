import re
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Iterator, List, Set

RawRule = str
Colour = str


def get_rules(path: Path) -> Iterator[RawRule]:
    with path.open("r") as f:
        for line in f:
            line = line.rstrip(".\n")
            if line:
                yield line


def get_containers(entry: Colour, map: defaultdict) -> Iterator[Colour]:
    for container in map[entry]:
        yield container
        yield from get_containers(container, map)


def resolve(input_paths: List[Path]) -> Any:
    rules_input_path = input_paths[0]

    container_map: DefaultDict[Colour, Set[Colour]] = defaultdict(set)

    colours_regex = re.compile(r"^[0-9\s]*([\w\s]+) bags?")

    for rule in get_rules(rules_input_path):
        outer_colour, raw_inner_colours = rule.split(" bags contain ")
        for raw_inner_colour in raw_inner_colours.split(", "):
            matches = colours_regex.match(raw_inner_colour)
            assert matches
            inner_colour: Colour = matches.group(1)
            container_map[inner_colour].add(outer_colour)

    colours: Set[Colour] = set(get_containers(entry="shiny gold", map=container_map))

    return len(colours)
