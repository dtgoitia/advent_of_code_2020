from itertools import combinations
from pathlib import Path
from typing import Any, List

from puzzles.exceptions import PuzzleError

SUM_TARGET = 2020


def resolve(input_paths: List[Path]) -> Any:
    entries_path = input_paths[0]

    with entries_path.open() as f:

        entries = []
        for line in f:
            entry = int(line.strip())
            entries.append(entry)

    a_b_entries = combinations(iterable=entries, r=2)
    matches = set()
    for entry_a, entry_b in a_b_entries:
        entry_c = SUM_TARGET - entry_a - entry_b
        if entry_c in entries:
            match = tuple(sorted([entry_a, entry_b, entry_c]))
            matches.add(match)

    results = [match[0] * match[1] * match[2] for match in matches]

    if not results:
        raise PuzzleError("no matches found")

    return results[0]
