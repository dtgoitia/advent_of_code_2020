import re
from pathlib import Path
from typing import Any, Iterator, List

Passport = str

WHITE_SPACE = " "
REQUIRED_FIELDS_KEY = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}  # no 'cid'
HCL_REGEX = re.compile(r"^#[0-9a-f]{6}$")
PID_REGEX = re.compile(r"^[0-9]{9}$")


def validate_byr(byr: str) -> None:
    assert len(byr) == 4
    assert 1920 <= int(byr) <= 2002


def validate_iyr(iyr: str) -> None:
    assert len(iyr) == 4
    assert 2010 <= int(iyr) <= 2020


def validate_eyr(eyr: str) -> None:
    assert len(eyr) == 4
    assert 2020 <= int(eyr) <= 2030


def validate_hgt(hgt: str) -> None:
    units = hgt[-2:]
    value = hgt[:-2]
    if units == "cm":
        assert 150 <= int(value) <= 193
        return
    if units == "in":
        assert 59 <= int(value) <= 76
        return

    raise Exception("unexpected units")


def validate_hcl(hcl: str) -> None:
    assert HCL_REGEX.match(hcl)


def validate_ecl(ecl: str) -> None:
    assert ecl in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def validate_pid(pid: str) -> None:
    assert PID_REGEX.match(pid)


def validate_cid(cid: str) -> None:
    assert True


field_to_validator_map = {
    "byr": validate_byr,
    "iyr": validate_iyr,
    "eyr": validate_eyr,
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
    "cid": validate_cid,
}


def validate(passport: Passport) -> None:
    fields_key = set()

    for field in passport.split(WHITE_SPACE):
        key, value = field.split(":")
        validator = field_to_validator_map[key]
        validator(value)

        fields_key.add(key)

    assert REQUIRED_FIELDS_KEY <= fields_key


def read_passports(path: Path) -> Iterator[Passport]:
    passport_lines: List[str] = []
    with path.open("r") as f:
        for line in f:
            if line == "\n":
                yield WHITE_SPACE.join(passport_lines)
                passport_lines = []
            else:
                passport_lines.append(line.strip())
        else:
            yield WHITE_SPACE.join(passport_lines)


def resolve(input_paths: List[Path]) -> Any:
    batch_input_path = input_paths[0]

    valid_passport_amount = 0
    for passport in read_passports(batch_input_path):
        try:
            validate(passport)
            valid_passport_amount += 1
        except Exception:
            pass

    return valid_passport_amount
