from pathlib import Path
from typing import Any, Dict, Iterator, List, NewType

import attr

DEBUG = False

RawInstruction = NewType("RawInstruction", str)
Command = NewType("Command", str)
Argument = NewType("Argument", int)
LineNumber = NewType("LineNumber", int)
CallAmount = NewType("CallAmount", int)
History = NewType("History", Dict[LineNumber, bool])


@attr.s(auto_attribs=True, frozen=True)
class Instruction:
    command: Command
    argument: Argument

    def __str__(self) -> str:
        return f"<{self.command} {self.argument}>"


Cache = NewType("Cache", Dict[LineNumber, Instruction])


@attr.s(auto_attribs=True, frozen=True)
class ProgramLine:
    number: LineNumber
    instruction: Instruction

    def __str__(self) -> str:
        instruction = self.instruction
        return f"<{self.number} - {instruction.command} {instruction.argument}>"


def debug(*msg):
    if DEBUG:
        print(*msg)


def get_program_reader(path: Path) -> Iterator[Instruction]:
    with path.open("r") as f:
        for line in f:
            raw = RawInstruction(line.strip())

            if not raw:
                continue

            command, argument = raw.split(" ")

            yield Instruction(
                command=Command(command),
                argument=Argument(int(argument)),
            )


class Runner:
    def __init__(self, program_reader: Iterator[Instruction]) -> None:
        self._instruction_stream = enumerate(program_reader)
        self.last_loaded_line = LineNumber(0)
        self._cache: Cache = {}  # type: ignore
        self.history: History = {}  # type:ignore

    def load_next_line(self) -> None:
        debug("loading next instruction")
        try:
            i, instruction = next(self._instruction_stream)
            debug(i, instruction)
            loaded_line_number = LineNumber(i)
            self.last_loaded_line = loaded_line_number
            self._cache[loaded_line_number] = instruction
        except StopIteration:
            debug("program completely loaded==========================")
            pass

    def get_line(self, line_number: LineNumber) -> ProgramLine:
        debug(f"Line {line_number} requested")
        while self.last_loaded_line < line_number:
            self.load_next_line()

        instruction = self._cache[line_number]
        debug(f"{instruction} found in line {line_number}")
        return ProgramLine(number=line_number, instruction=instruction)

    def mark_line_as_executed(self, line: LineNumber) -> None:
        self.history[line] = True


def resolve(input_paths: List[Path]) -> Any:
    program_input_path = input_paths[0]

    acc = 0

    program_reader = get_program_reader(program_input_path)
    runner = Runner(program_reader)

    runner.load_next_line()

    execution_line: LineNumber = LineNumber(0)
    while True:
        debug("")
        debug(f"execution line: {execution_line}")

        if execution_line in runner.history:
            # line was already called... starting infinite loop!
            break
        debug(f"OK, line {execution_line} not executed before")

        runner.mark_line_as_executed(execution_line)

        line: ProgramLine = runner.get_line(execution_line)

        instruction = line.instruction
        debug(f"executing {instruction}")
        command = instruction.command
        if command == "acc":
            acc += instruction.argument
            execution_line += 1  # type: ignore
        elif command == "jmp":
            execution_line += instruction.argument  # type: ignore
        elif command == "nop":
            execution_line += 1  # type: ignore
        else:
            raise ValueError(f"Command {instruction.command} is not supported")

    return acc
