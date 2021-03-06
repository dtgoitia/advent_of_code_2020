from pathlib import Path
from typing import Any, List


class PuzzleError(Exception):
    pass


SUM_TARGET = 2020


def resolve(input_paths: List[Path]) -> Any:
    entries_path = input_paths[0]

    with entries_path.open() as f:

        entries = []
        peers = []
        for line in f:
            entry = int(line.strip())

            entries.append(entry)
            peers.append(SUM_TARGET - entry)

    pairs = set()
    for peer in peers:
        if peer in entries:
            pair = tuple(sorted([SUM_TARGET - peer, peer]))
            pairs.add(pair)

    for pair in pairs:
        print(pair)
        result = pair[0] * pair[1]
        print(result)

    return result
