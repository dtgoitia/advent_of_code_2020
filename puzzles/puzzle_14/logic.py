import re
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterator, List

RawRule = str
Colour = str
BagAmount = int


def get_rules(path: Path) -> Iterator[RawRule]:
    with path.open("r") as f:
        for line in f:
            line = line.rstrip(".\n")
            if line:
                yield line


def get_content(colour: Colour, map: defaultdict) -> BagAmount:
    inner_bag_amount = 0
    for inner_colour, bag_amount in map[colour].items():
        content = get_content(inner_colour, map)
        inner_bag_amount += bag_amount * (1 + content)

    return inner_bag_amount


def resolve(input_paths: List[Path]) -> Any:
    rules_input_path = input_paths[0]

    # key is wrapped by value
    content_map: DefaultDict[Colour, Dict[Colour, BagAmount]] = defaultdict(dict)

    colours_regex = re.compile(r"^(\d*)\s([\w\s]+) bags?")

    for rule in get_rules(rules_input_path):
        outer_colour, raw_inner_colours = rule.split(" bags contain ")
        for raw_inner_colour in raw_inner_colours.split(", "):
            matches = colours_regex.match(raw_inner_colour)
            if not matches:  # leave node reached
                content_map[outer_colour] = {}
                continue
            inner_amount: BagAmount = int(matches.group(1))
            inner_colour: Colour = matches.group(2)

            if content_map[outer_colour].get(inner_colour):
                raise KeyError("cannot override inner colour")

            content_map[outer_colour].update({inner_colour: inner_amount})

    amount: BagAmount = get_content(colour="shiny gold", map=content_map)

    return amount
