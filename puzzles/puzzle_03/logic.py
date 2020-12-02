from pathlib import Path
from typing import Any, List, NewType

import attr


class PuzzleError(Exception):
    pass


def get_input_path() -> Path:
    path = Path(__file__).parent / "input"
    return path


RawEntry = str


def read_all_entries(path: Path) -> List[RawEntry]:
    with path.open() as f:
        content = [line.strip() for line in f.readlines()]

    return content


@attr.s(auto_attribs=True, frozen=True)
class Policy:
    min: int
    max: int
    letter: str


Password = NewType("Password", str)


@attr.s(auto_attribs=True, frozen=True)
class Entry:
    policy: Policy
    password: Password


def parse_entry(line: RawEntry) -> Entry:
    raw_policy, raw_password = line.split(":")

    raw_min_max, letter = raw_policy.split(" ")
    min, max = raw_min_max.split("-")
    policy = Policy(min=int(min), max=int(max), letter=letter)

    password = Password(raw_password.strip())

    return Entry(policy=policy, password=password)


def is_valid_entry(entry: Entry) -> bool:
    policy = entry.policy
    password = entry.password

    count = password.count(policy.letter)

    return policy.min <= count <= policy.max


def resolve(input_path: Path) -> Any:
    input = read_all_entries(input_path)

    entries = (parse_entry(raw_entry) for raw_entry in input)

    matches = [entry for entry in entries if is_valid_entry(entry)]

    if not matches:
        raise PuzzleError("no matches found")

    result = len(matches)

    return result
