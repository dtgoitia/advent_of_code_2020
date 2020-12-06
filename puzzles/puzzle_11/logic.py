from pathlib import Path
from typing import Any, Iterator, List

PersonAnswer = str


def get_forms(path: Path) -> Iterator[PersonAnswer]:
    form_lines: List[PersonAnswer] = []
    with path.open("r") as f:
        for line in f:
            if line == "\n":
                yield "".join(form_lines)
                form_lines = []
            else:
                form_lines.append(line.strip())
        else:
            yield "".join(form_lines)


def resolve(input_paths: List[Path]) -> Any:
    forms_input_path = input_paths[0]

    answer_amount_per_group = []
    for form in get_forms(forms_input_path):
        answers = {answer for answer in form}
        answer_amount_per_group.append(len(answers))

    return sum(answer_amount_per_group)
