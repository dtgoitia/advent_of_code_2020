from pathlib import Path
from typing import Any, Dict, Iterator, List

PersonAnswers = str


def get_forms(path: Path) -> Iterator[List[PersonAnswers]]:
    form_lines: List[PersonAnswers] = []
    with path.open("r") as f:
        for line in f:
            if line == "\n":
                yield form_lines
                form_lines = []
            else:
                form_lines.append(line.strip())
        else:
            yield form_lines


def did_person_answer_yes(answer: "str", person_answers: Dict[str, bool]) -> bool:
    try:
        return person_answers[answer]
    except KeyError:
        return False


def resolve(input_paths: List[Path]) -> Any:
    forms_input_path = input_paths[0]

    answer_amount_per_group = []
    for form in get_forms(forms_input_path):
        common_answers = set()
        answers_per_person: List[Dict[str, bool]] = []

        for person_answers in form:
            answers = {}

            for answer in person_answers:
                common_answers.add(answer)
                answers[answer] = True

            answers_per_person.append(answers)

        everyone_yes_counter = 0
        for answer in common_answers:
            everyone_said_yes = all(
                did_person_answer_yes(answer, person_answers)
                for person_answers in answers_per_person
            )
            if everyone_said_yes:
                everyone_yes_counter += 1

        answer_amount_per_group.append(everyone_yes_counter)

    return sum(answer_amount_per_group)
