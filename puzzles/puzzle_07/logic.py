from pathlib import Path
from typing import Any, Iterator, List

Passport = str

WHITE_SPACE = " "
REQUIRED_FIELDS_KEY = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}  # no 'cid'


def read_passports(path: Path) -> Iterator[Passport]:
    passport: List[Passport] = []
    with path.open("r") as f:
        for line in f:
            if line == "\n":
                yield WHITE_SPACE.join(passport)
                passport = []
            else:
                passport.append(line.strip())


def resolve(input_paths: List[Path]) -> Any:
    batch_input_path = input_paths[0]

    valid_passport_amount = 0
    for passport in read_passports(batch_input_path):
        fields_key = {field.split(":")[0] for field in passport.split(WHITE_SPACE)}
        if REQUIRED_FIELDS_KEY <= fields_key:
            valid_passport_amount += 1

    return valid_passport_amount
