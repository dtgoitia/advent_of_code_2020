from pathlib import Path
from puzzles.exceptions import PuzzleError
from typing import Any, Dict, Iterator, List, NewType, Optional

import attr

DEBUG = True

RawInstruction = NewType("RawInstruction", str)
Command = NewType("Command", str)
Argument = NewType("Argument", int)
LineNumber = NewType("LineNumber", int)
CallAmount = NewType("CallAmount", int)
Executed = NewType("History", Dict[LineNumber, bool])


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


ACC = Command("acc")
JMP = Command("jmp")
NOP = Command("nop")


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
        self.executed: Executed = {}  # type:ignore
        self.history: List[LineNumber] = []  # type:ignore
        # self._last_executed_line_number = None

    def load_next_line(self) -> bool:
        debug("loading next instruction")
        try:
            i, instruction = next(self._instruction_stream)
            debug(i, instruction)
            loaded_line_number = LineNumber(i)
            self.last_loaded_line = loaded_line_number
            self._cache[loaded_line_number] = instruction
        except StopIteration:
            debug("\nend of program reached")
            return True

    def get_line(self, line_number: LineNumber) -> Optional[ProgramLine]:
        # debug(f"Line {line_number} requested")

        while self.last_loaded_line < line_number:
            is_completed = self.load_next_line()
            if is_completed:
                return

        # if line_number == 7:
        #     self.patch()

        instruction = self._cache[line_number]
        # debug(f"{instruction} found in line {line_number}")
        return ProgramLine(number=line_number, instruction=instruction)

    def mark_line_as_executed(self, line: LineNumber) -> None:
        # self._last_executed_line_number = line
        self.history.append(line)
        self.executed[line] = True
        debug(f"line number {line} marked as executed")

    def fix_last_line(self) -> ProgramLine:
        line_number = self.history[-1]
        debug(f"fixing last executed line (number: {line_number})")
        new_instruction = Instruction(NOP, 0)
        self._cache[line_number] = new_instruction

        # delete last execution from history, to be able to re-execute
        del self.executed[line_number]

        return ProgramLine(number=line_number, instruction=new_instruction)

    def patch(self) -> ProgramLine:
        debug("patching line 7")
        new_instruction = Instruction(NOP, 0)
        self._cache[7] = new_instruction


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

        if execution_line in runner.executed:
            # pass
            debug(f"execution line {execution_line} exists in history")
            for line_number in runner.history:
                runned = runner.get_line(line_number)
                if runned.instruction.command == JMP:
                    next_line = runned.number + runned.instruction.argument
                    next_line = f"--> {next_line}"
                else:
                    next_line = ""

                debug(line_number, runned, next_line)
            raise PuzzleError(f"infinite loop started with line {execution_line}")
            # line was already called... starting infinite loop!
        #     # fix last line, and reset current execution to updated line
        #     updated_line = runner.fix_last_line()
        #     execution_line = updated_line.number
        #     debug(f"execution line amended to : {execution_line}")
        # if execution_line == 7:
        #     # line was already called... starting infinite loop!
        #     # fix last line, and reset current execution to updated line
        #     runner.patch()
        #     breakpoint()
        else:
            debug(f"OK, line {execution_line} not executed before")

        runner.mark_line_as_executed(execution_line)

        line: ProgramLine = runner.get_line(execution_line)
        if not line:
            break

        instruction = line.instruction
        debug(f"executing {instruction}")
        command = instruction.command
        if command == ACC:
            debug(
                f"acc = {acc} + {instruction.argument} = {acc + instruction.argument}"
            )
            acc += instruction.argument
            execution_line += 1  # type: ignore
        elif command == JMP:
            execution_line += instruction.argument  # type: ignore
        elif command == NOP:
            execution_line += 1  # type: ignore
        else:
            raise ValueError(f"Command {instruction.command} is not supported")
        debug(f"next execution line: {execution_line}")

    return acc
