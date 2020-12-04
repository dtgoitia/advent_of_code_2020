from pathlib import PosixPath
from textwrap import dedent

from .logic import resolve


def test_resolve(tmp_path: PosixPath) -> None:
    batch_input_path = tmp_path / "input_1_batch"
    batch_input_path.write_text(
        dedent(
            """
            ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
            byr:1937 iyr:2017 cid:147 hgt:183cm

            iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
            hcl:#cfa07d byr:1929

            hcl:#ae17e1 iyr:2013
            eyr:2024
            ecl:brn pid:760753108 byr:1931
            hgt:179cm

            hcl:#cfa07d eyr:2025 pid:166559648
            iyr:2011 ecl:brn hgt:59in
            """
        ).strip()
    )

    valid_passport_amount = resolve(input_paths=[batch_input_path])

    assert valid_passport_amount == 2
