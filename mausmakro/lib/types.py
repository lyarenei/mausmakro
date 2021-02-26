from typing import Any, List, Optional

from mausmakro.lib.enums import Opcode


class Instruction:

    opcode: Opcode


class Command(Instruction):

    arg: Any

    def __init__(self, opcode: Opcode, arg: Any = None):
        self.opcode = opcode
        self.arg = arg

    def __eq__(self, other):
        return self.opcode == other.opcode and self.arg == other.arg


class Conditional(Instruction):

    condition: Command
    negate = False
    end_label: str
    else_label: Optional[str]

    def __init__(self, opcode: Opcode):
        self.opcode = opcode


class Macro:

    name: str
    body: List[Instruction]

    def __init__(self, name: str):
        self.name = name


class Stack(list):

    def push(self, obj: Any):
        self.append(obj)

    def empty(self) -> bool:
        return len(self) == 0

    def top(self):
        return self[-1]
