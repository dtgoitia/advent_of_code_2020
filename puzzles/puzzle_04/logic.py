from pathlib import Path
from typing import Any, List, NewType

import attr

from puzzles.exceptions import PuzzleError

RawEntry = str


def read_all_entries(path: Path) -> List[RawEntry]:
    with path.open() as f:
        content = [line.strip() for line in f.readlines()]

    return content


@attr.s(auto_attribs=True, frozen=True)
class Policy:
    position_a: int
    position_b: int
    character: str


Password = NewType("Password", str)


@attr.s(auto_attribs=True, frozen=True)
class Entry:
    policy: Policy
    password: Password


def parse_entry(line: RawEntry) -> Entry:
    raw_policy, raw_password = line.split(":")

    raw_positions, character = raw_policy.split(" ")
    position_a, position_b = raw_positions.split("-")
    policy = Policy(
        position_a=int(position_a),
        position_b=int(position_b),
        character=character,
    )

    password = Password(raw_password.strip())

    return Entry(policy=policy, password=password)


def is_valid_entry(entry: Entry) -> bool:
    policy = entry.policy
    password = entry.password
    target_char = policy.character

    # CAUTION: positions are 1-based index
    char_is_in_position_a = password[policy.position_a - 1] == target_char
    char_is_in_position_b = password[policy.position_b - 1] == target_char

    return char_is_in_position_a ^ char_is_in_position_b


def resolve(input_paths: List[Path]) -> Any:
    entries_path = input_paths[0]
    input = read_all_entries(entries_path)

    entries = (parse_entry(raw_entry) for raw_entry in input)

    matches = [entry for entry in entries if is_valid_entry(entry)]

    if not matches:
        raise PuzzleError("no matches found")

    result = len(matches)

    return result
