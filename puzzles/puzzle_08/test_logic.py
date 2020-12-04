from pathlib import PosixPath
from textwrap import dedent

import pytest

from .logic import (
    resolve,
    validate_byr,
    validate_ecl,
    validate_hcl,
    validate_hgt,
    validate_pid,
)


@pytest.mark.parametrize(
    ("validator", "value", "is_valid"),
    (
        (validate_byr, "2002", True),
        (validate_byr, "2003", False),
        (validate_hgt, "60in", True),
        (validate_hgt, "190cm", True),
        (validate_hgt, "190in", False),
        (validate_hgt, "190", False),
        (validate_hcl, "#123abc", True),
        (validate_hcl, "#123abz", False),
        (validate_hcl, "123abc", False),
        (validate_ecl, "brn", True),
        (validate_ecl, "wat", False),
        (validate_pid, "000000001", True),
        (validate_pid, "0123456789", False),
    ),
)
def test_validates(validator, value, is_valid):
    try:
        validator(value)
        assert is_valid
    except Exception:
        assert not is_valid


def test_resolve_valid_passports(tmp_path: PosixPath) -> None:
    batch_input_path = tmp_path / "input_1_batch"
    batch_input_path.write_text(
        dedent(
            """
            pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
            hcl:#623a2f

            eyr:2029 ecl:blu cid:129 byr:1989
            iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

            hcl:#888785
            hgt:164cm byr:2001 iyr:2015 cid:88
            pid:545766238 ecl:hzl
            eyr:2022

            iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
            """
        ).strip()
    )

    valid_passport_amount = resolve(input_paths=[batch_input_path])

    assert valid_passport_amount == 4


def test_resolve_invalid_passports(tmp_path: PosixPath) -> None:
    batch_input_path = tmp_path / "input_1_batch"
    batch_input_path.write_text(
        dedent(
            """
            eyr:1972 cid:100
            hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

            iyr:2019
            hcl:#602927 eyr:1967 hgt:170cm
            ecl:grn pid:012533040 byr:1946

            hcl:dab227 iyr:2012
            ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

            hgt:59cm ecl:zzz
            eyr:2038 hcl:74454a iyr:2023
            pid:3556412378 byr:2007
            """
        ).strip()
    )

    valid_passport_amount = resolve(input_paths=[batch_input_path])

    assert valid_passport_amount == 0
